# Bước 4c: đo chất lượng truy xuất trên bộ eval, cho 6 tổ hợp {dieu, window} × {dense, bm25, hybrid}
#   Chạy: python -X utf8 -m src.eval_retrieval   -> results/retrieval_{config}_{mode}.json + bảng so sánh
import json
import time
from collections import defaultdict
from datetime import datetime

import numpy as np
from google.genai import errors

from src.embed import DIM, MODEL, ROOT, embed_query
from src.retrieve import load, search

EVAL = ROOT / "eval" / "questions.jsonl"  # bộ eval chính thức (đã duyệt)
if not EVAL.exists():
    EVAL = ROOT / "eval" / "questions_draft.jsonl"  # chưa duyệt xong thì tạm dùng bản nháp
KS, MRR_K = [1, 3, 5], 10
CONFIGS, MODES = ["dieu", "window"], ["dense", "bm25", "hybrid"]


def squash(s):
    return "".join(s.split())  # bỏ MỌI khoảng trắng: PDF ngắt dòng khác nhau không làm trượt phép so khớp


def covered(chunk, evidence):
    """Các câu evidence nằm trọn trong chunk. Chunk chứa >= 1 câu evidence = chunk LIÊN QUAN."""
    text = squash(chunk["text"])
    return {e for e in evidence if squash(e) in text}


def stats(xs):
    return {"mean": round(float(np.mean(xs)), 4), "min": round(float(min(xs)), 4), "max": round(float(max(xs)), 4)}


def evaluate(questions, config, mode, embed_ms):
    load(config)  # nạp index + dựng BM25 trước, để không tính vào thời gian tìm kiếm
    per_q, search_ms = [], []
    for q in questions:
        top1_dense = search(q["question"], k=1, mode="dense", config=config)[0][1]  # cosine của chunk gần nhất
        row = {"id": q["id"], "type": q["type"], "top1_dense": round(top1_dense, 4)}
        if q["type"] != "no_answer":  # câu không có đáp án: không có chunk liên quan để chấm hạng
            t0 = time.perf_counter()
            hits = search(q["question"], k=MRR_K, mode=mode, config=config)
            search_ms.append((time.perf_counter() - t0) * 1000)
            ranks = [r for r, (c, _) in enumerate(hits, 1) if covered(c, q["evidence"])]
            found = set().union(*(covered(c, q["evidence"]) for c, _ in hits[:5]))
            row |= {"rank": ranks[0] if ranks else None,  # hạng của chunk liên quan đầu tiên (None = ngoài top 10)
                    "evidence_recall@5": round(len(found) / len(q["evidence"]), 4),
                    "top5": [c["id"] for c, _ in hits[:5]]}
        per_q.append(row)

    ans = [r for r in per_q if r["type"] != "no_answer"]
    hit = lambda r, k: r["rank"] is not None and r["rank"] <= k
    metrics = {f"hit@{k}": round(np.mean([hit(r, k) for r in ans]), 4) for k in KS}
    metrics[f"mrr@{MRR_K}"] = round(np.mean([1 / r["rank"] if r["rank"] else 0 for r in ans]), 4)
    metrics["evidence_recall@5"] = round(np.mean([r["evidence_recall@5"] for r in ans]), 4)
    by_type = defaultdict(list)
    for r in ans:
        by_type[r["type"]].append(hit(r, 5))
    metrics["hit@5_by_type"] = {t: round(float(np.mean(v)), 4) for t, v in by_type.items()}
    return {
        "eval_file": EVAL.relative_to(ROOT).as_posix(), "config": config, "mode": mode,
        "embed_model": f"{MODEL} ({DIM} chiều)", "k": KS, "mrr_k": MRR_K,
        "n_answerable": len(ans), "n_no_answer": len(per_q) - len(ans), "metrics": metrics,
        # Ngưỡng từ chối sau này: so cosine top-1 của câu không có đáp án với câu có đáp án
        "top1_dense_score": {"answerable": stats([r["top1_dense"] for r in ans]),
                             "no_answer": stats([r["top1_dense"] for r in per_q if r["type"] == "no_answer"])},
        # embed: lần gọi API thật đầu tiên cho từng câu (lấy từ cache); search: phần tính trên máy, đo ở lần chạy này
        "latency_ms": {"query_embedding": round(float(np.mean([embed_ms[r["id"]] for r in per_q])), 1),
                       "search": round(float(np.mean(search_ms)), 3)},
        "per_question": per_q, "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


def main():
    questions = [json.loads(line) for line in EVAL.open(encoding="utf-8")]
    print(f"Bộ eval: {EVAL.relative_to(ROOT)} ({len(questions)} câu)")
    try:  # embed mỗi câu hỏi 1 lần (cache trên đĩa), lần chạy sau không tốn quota
        embed_ms = {q["id"]: embed_query(q["question"])[1] for q in questions}
    except errors.APIError as e:
        if e.code != 429:
            raise
        raise SystemExit("Lỗi 429: hết quota free tier. Đợi vài phút rồi chạy lại (câu đã embed được giữ trong cache).")
    (ROOT / "results").mkdir(exist_ok=True)
    qtypes = list(dict.fromkeys(q["type"] for q in questions if q["type"] != "no_answer"))
    print(f"{'config':<7}{'mode':<7}{'Hit@1':>6}{'Hit@3':>6}{'Hit@5':>6}{'MRR':>6}{'EvR@5':>6} | Hit@5: "
          + " ".join(f"{t[:6]:>6}" for t in qtypes) + " | search ms")
    for config in CONFIGS:
        for mode in MODES:
            res = evaluate(questions, config, mode, embed_ms)
            out = ROOT / "results" / f"retrieval_{config}_{mode}.json"
            out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
            m = res["metrics"]
            print(f"{config:<7}{mode:<7}" + "".join(f"{m[x]:>6.2f}" for x in ["hit@1", "hit@3", "hit@5", "mrr@10",
                  "evidence_recall@5"]) + " | " + " " * 7 + " ".join(f"{m['hit@5_by_type'][t]:>6.2f}" for t in qtypes)
                  + f" | {res['latency_ms']['search']:.2f}")
        s = res["top1_dense_score"]
        print(f"  {config}: cosine top-1 (dense) câu có đáp án mean {s['answerable']['mean']:.3f} "
              f"min {s['answerable']['min']:.3f} | câu không có đáp án mean {s['no_answer']['mean']:.3f} "
              f"max {s['no_answer']['max']:.3f}")
    print(f"Embedding câu hỏi (gọi API, lần đầu): trung bình {res['latency_ms']['query_embedding']:.0f} ms/câu. "
          f"Kết quả: results/retrieval_*.json")


if __name__ == "__main__":
    main()

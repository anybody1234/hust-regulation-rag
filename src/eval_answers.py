# Bước 7: chấm tự động câu trả lời của bot trên bộ eval + tạo phiếu chấm tay eval/GRADING.md
#   Chạy: python -X utf8 -m src.eval_answers [config] [mode] [--runs N] [--questions F1 F2 ...] [--only q11,q28]
#   (mặc định: dieu hybrid, k=5, 1 lần; config/mode đặt TRƯỚC --questions vì --questions nhận nhiều file)
#   -> results/answers_{config}_{mode}.jsonl (cache từng lần hỏi), results/answers_{config}_{mode}[_runsN][_partial].json (metric)
#   Lần eval cuối: python -X utf8 -m src.eval_answers dieu hybrid --runs 3 --questions eval/questions.jsonl eval/questions_extra.jsonl
import argparse
import hashlib
import json
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import numpy as np
from google.genai import errors

from src import generate
from src.embed import ROOT, chunks_path, file_sha256
from src.eval_retrieval import EVAL, covered  # cùng file eval và cùng cách so khớp evidence (bỏ mọi khoảng trắng)
from src.generate import SYSTEM, answer

K = 5
# Giá tham khảo nếu dùng bản trả phí, gemini-3.5-flash-lite (trang giá Gemini, xem ngày 16/11/2026), USD / 1 triệu token.
# Giả định: token thinking tính tiền như token output (Google tính thinking vào phần output).
PRICE_IN, PRICE_OUT = 0.30, 2.50
PAUSE = 4  # giây nghỉ sau mỗi lần gọi LLM: giữ dưới 15 request/phút cho nhẹ quota free tier
FIELDS = ["run", "refused", "cited_evidence", "retrieved_evidence", "invalid_citations", "model", "model_version",
          "latency_ms", "usage"]  # các trường của từng lần chạy ghi vào file metric

_last = {}  # model_version của lần gọi LLM gần nhất


def _call_llm(prompt, _orig=generate.call_llm):
    # answer() chỉ ghi tên model ĐÃ GỌI, nhưng API có thể trả lời bằng bản khác (ablation 16/11: gọi 3.5-flash, chạy 3.6-flash).
    # generate.py đã đóng băng nên bọc call_llm ở đây để ghi thêm model_version mà API báo về.
    model, resp = _orig(prompt)
    _last["model_version"] = resp.model_version
    return model, resp


generate.call_llm = _call_llm  # answer() tra call_llm trong module generate lúc chạy -> dùng bản bọc này


def ask(q, config, mode):
    """Gọi answer(); gặp 429 (hết quota) thì đợi 1 phút rồi thử lại, tối đa 3 lần."""
    for attempt in range(4):
        try:
            r = answer(q["question"], k=K, mode=mode, config=config)
            return {**r, "model_version": _last.pop("model_version", None)}
        except errors.APIError as e:
            if e.code not in (429, 503) or attempt == 3:
                raise
            print(f"  lỗi {e.code}, đợi 60 giây rồi thử lại...")
            time.sleep(60)


def pct(xs):
    return round(float(np.mean(xs)), 4) if xs else None  # tỉ lệ (0..1); không có câu nào thì None


def rel(path):
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix()


def load_questions(files):
    questions = [json.loads(line) for f in files for line in f.open(encoding="utf-8") if line.strip()]
    dup = sorted(i for i, n in Counter(q["id"] for q in questions).items() if n > 1)
    if dup:  # cache, metric và phiếu chấm đều tra theo id: trùng id thì câu này lấy nhầm câu trả lời của câu kia
        raise SystemExit(f"Trùng id câu hỏi giữa các file {[rel(f) for f in files]}: {dup}")
    return questions


def grading_md(questions, table, runs, files):
    out = ["# Phiếu chấm tay câu trả lời của bot", "",
           f"Bộ eval: {', '.join(f'`{rel(f)}`' for f in files)}. Đáp án chuẩn lấy từ bộ eval (trường `review` cho biết câu nào đã được đối chiếu thủ công với PDF).", "",
           "Cách chấm: với mỗi câu, đọc câu trả lời của bot, mở nguồn bot trích (đúng văn bản, đúng trang) rồi đánh `[x]` vào ô phù hợp:",
           "- **Đúng**: đủ ý chính như đáp án chuẩn, mọi chi tiết đều có trong văn bản.",
           "- **Đúng một phần**: đúng nhưng thiếu ý quan trọng, hoặc thêm điều kiện không cần thiết.",
           "- **Sai**: nêu sai con số/điều kiện so với văn bản.",
           "- **Bịa**: nêu điều KHÔNG có trong văn bản (kể cả khi có ghi trích dẫn). Có thể đánh cùng ô khác.",
           "- **Từ chối đúng**: câu `no_answer` và bot trả lời \"Không tìm thấy trong quy chế\".",
           "- **Từ chối sai**: câu có đáp án nhưng bot từ chối.",
           "Cột tự động `cited-evidence` = có ít nhất 1 chunk được bot TRÍCH chứa câu bằng chứng của bộ eval. Chỉ là gợi ý, không thay chấm tay.", ""]
    if runs > 1:  # chấm tay N lần mỗi câu quá tốn công: chỉ chấm lần 1, tỉ lệ từ chối qua N lần đã có trong file metric
        out += [f"Mỗi câu được hỏi {runs} lần, phiếu chỉ hiện **lần 1**. Dòng ⚠️ = câu không nhất quán (lúc từ chối, lúc trả lời).", ""]
    for q in questions:
        rs = table[q["id"]]
        r, n_refused = rs[0], sum(x["refused"] for x in rs)
        out += [f"## {q['id']} ({q['type']})", "", f"**Câu hỏi:** {q['question']}", "", f"**Đáp án chuẩn:** {q.get('answer', '(không có)')}", "",
                "**Bot trả lời** (" + r["model"] + "):", ""] + [f"> {line}" for line in r["answer"].splitlines()] + [""]
        out += ["**Nguồn bot trích:**"] + [f"- [{c['n']}] {c['source']}" for c in r["citations"]] + (
            ["- (không có)"] if not r["citations"] else [])
        if r["invalid_citations"]:
            out.append(f"- Trích dẫn không hợp lệ: {r['invalid_citations']}")
        flag = "không áp dụng" if r["cited_evidence"] is None else ("có" if r["cited_evidence"] else "KHÔNG")
        out += ["", f"Tự động: cited-evidence = {flag}; bot từ chối = {'có' if r['refused'] else 'không'}", ""]
        if 0 < n_refused < runs:  # lần 1 chưa chắc đại diện: báo để người chấm biết kết luận có thể đổi chiều ở lần khác
            out += [f"⚠️ từ chối {n_refused}/{runs} lần (phiếu chỉ hiện lần 1)", ""]
        out += ["[ ] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai",
                "", "Ghi chú:", ""]
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Chấm câu trả lời của bot trên bộ eval")
    p.add_argument("config", nargs="?", default="dieu")
    p.add_argument("mode", nargs="?", default="hybrid")
    p.add_argument("--runs", type=int, default=1, help="số lần hỏi mỗi câu (flash-lite nhạy prompt: 1 lần chưa đủ tin)")
    p.add_argument("--questions", nargs="+", type=Path, default=[EVAL],
                   help="1 hay nhiều file câu hỏi, gộp lại (mặc định: questions.jsonl, chưa có thì questions_draft.jsonl)")
    p.add_argument("--only", help="chạy thử vài id, vd q11,q28: không ghi GRADING, metric ghi vào file _partial")
    a = p.parse_args()
    if a.runs < 1:
        p.error("--runs phải >= 1")
    config, mode, runs, t_start = a.config, a.mode, a.runs, time.perf_counter()
    files = [ROOT / f for f in a.questions]  # đường dẫn tương đối tính từ thư mục project
    questions = load_questions(files)
    only = [i.strip() for i in a.only.split(",")] if a.only else None
    if only:
        missing = set(only) - {q["id"] for q in questions}
        if missing:
            raise SystemExit(f"Không có id {sorted(missing)} trong bộ eval")
        questions = [q for q in questions if q["id"] in only]
    print(f"Bộ eval: {', '.join(map(rel, files))} ({len(questions)} câu), config={config}, mode={mode}, k={K}, runs={runs}")
    cache = ROOT / "results" / f"answers_{config}_{mode}.jsonl"
    # Chunk đổi (chạy lại src.chunk) hoặc prompt đổi thì câu trả lời cũ trong cache không còn đúng -> bỏ qua, hỏi lại
    version = {"chunks_sha256": file_sha256(chunks_path(config)), "prompt_sha256": hashlib.sha256(SYSTEM.encode()).hexdigest()}
    done = {}  # (id, lần chạy) -> câu trả lời đã có (cùng k, cùng phiên bản) -> không gọi lại API
    if cache.exists():  # dòng khác phiên bản chỉ bị bỏ qua, KHÔNG xoá khỏi file (cache chỉ ghi thêm)
        for r in map(json.loads, cache.open(encoding="utf-8")):
            if r["k"] == K and r.get("version") == version:
                done[r["id"], r.get("run", 1)] = r  # dòng cũ chưa có "run" = lần chạy 1; trùng khoá thì dòng ghi sau (mới hơn) thắng
    table, calls = {q["id"]: [] for q in questions}, 0
    for run in range(1, runs + 1):  # hỏi xong lần 1 cho mọi câu rồi mới tới lần 2: dừng giữa chừng vẫn đủ lần 1 cho phiếu chấm tay
        for q in questions:
            r = done.get((q["id"], run))
            if r is None or r["question_eval"] != q["question"]:
                print(f"  {q['id']} lần {run}/{runs}: đang hỏi...")
                r = {"id": q["id"], "run": run, "question_eval": q["question"], "version": version, **ask(q, config, mode)}
                with cache.open("a", encoding="utf-8") as f:  # ghi ngay từng câu: lỡ dừng giữa chừng thì lần sau làm tiếp
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
                calls += 1
                time.sleep(PAUSE)
            r["run"] = run
            cited_ids = {c["chunk_id"] for c in r["citations"]}
            r["cited_evidence"] = None if q["type"] == "no_answer" else any(  # chunk được TRÍCH có chứa bằng chứng không
                covered(c, q["evidence"]) for c in r["chunks"] if c["id"] in cited_ids)
            r["retrieved_evidence"] = None if q["type"] == "no_answer" else any(covered(c, q["evidence"]) for c in r["chunks"])
            table[q["id"]].append(r)
    kind = {q["id"]: q["type"] for q in questions}
    rows = [r for rs in table.values() for r in rs]  # mọi lần chạy của mọi câu: metric tính trên tất cả (runs=1 thì như cũ)
    ans = [r for r in rows if kind[r["id"]] != "no_answer"]
    no_ans = [r for r in rows if kind[r["id"]] == "no_answer"]
    n_refused = {i: sum(r["refused"] for r in rs) for i, rs in table.items()}
    inconsistent = [i for i, n in n_refused.items() if 0 < n < runs]  # lúc từ chối lúc trả lời: kết quả 1 lần chạy không đáng tin
    lat = lambda key, p: round(float(np.percentile([r["latency_ms"][key] for r in rows], p)), 1)
    tok = {key: round(float(np.mean([r["usage"].get(key, 0) for r in rows])), 1)
           for key in ["prompt_tokens", "output_tokens", "thoughts_tokens"]}
    cost = (tok["prompt_tokens"] * PRICE_IN + (tok["output_tokens"] + tok["thoughts_tokens"]) * PRICE_OUT) / 1e6
    metrics = {
        "refusal_accuracy": pct([r["refused"] for r in no_ans]),  # câu không có đáp án: bot có từ chối không
        "false_refusal_rate": pct([r["refused"] for r in ans]),  # câu có đáp án mà bot lại từ chối
        "inconsistent": {"count": len(inconsistent), "ids": inconsistent},
        "citation_rate": pct([len(r["citations"]) > 0 for r in rows if not r["refused"]]),  # tính trên câu bot KHÔNG từ chối
        "invalid_citation_rate": pct([len(r["invalid_citations"]) > 0 for r in rows]),
        "invalid_citations_total": sum(len(r["invalid_citations"]) for r in rows),
        "cited_evidence_rate": pct([r["cited_evidence"] for r in ans]),
        "retrieved_evidence_rate": pct([r["retrieved_evidence"] for r in ans]),  # trần trên: bằng chứng có trong k chunk đưa vào
        "latency_ms": {key: {"p50": lat(key, 50), "p95": lat(key, 95)} for key in ["retrieve", "llm", "total"]},
        "embed_api_ms_mean": round(float(np.mean([r["latency_ms"]["embed_api"] for r in rows])), 1),
        "tokens_mean": tok, "cost_usd_per_question_if_paid": round(cost, 6),
    }
    res = {"eval_files": [rel(f) for f in files], "only": only, "config": config, "mode": mode, "k": K, "runs": runs,
           "version": version, "models_used": Counter(r["model"] for r in rows),
           "model_versions": Counter(r.get("model_version") for r in rows),  # dòng cache cũ chưa ghi -> null
           "n_answerable": sum(t != "no_answer" for t in kind.values()), "n_no_answer": sum(t == "no_answer" for t in kind.values()),
           "metrics": metrics, "price_usd_per_1m_tokens": {"input": PRICE_IN, "output_incl_thinking": PRICE_OUT},
           "new_api_calls": calls, "elapsed_s": round(time.perf_counter() - t_start, 1),
           "per_question": [{"id": i, "type": kind[i], "n_refused": n_refused[i], "n_runs": len(rs),
                             "runs": [{f: r.get(f) for f in FIELDS} for r in rs]} for i, rs in table.items()],
           "timestamp": datetime.now().isoformat(timespec="seconds")}
    name = f"answers_{config}_{mode}" + (f"_runs{runs}" if runs > 1 else "") + ("_partial" if only else "")
    out = ROOT / "results" / f"{name}.json"
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(metrics, ensure_ascii=False, indent=1))
    print(f"Model: {dict(res['models_used'])}, bản thật: {dict(res['model_versions'])}. Gọi API mới: {calls}. Kết quả: {rel(out)}")
    if only:  # chạy thử vài câu: không ghi đè phiếu chấm tay đủ bộ bằng phiếu thiếu câu
        return
    grading = ROOT / "eval" / "GRADING.md"
    old = grading.read_text(encoding="utf-8").splitlines() if grading.exists() else []
    if any(l.lstrip("- ").startswith("[") and "[x]" in l.lower() for l in old):  # phiếu đã được chấm tay -> không ghi đè, ghi file mới
        grading = grading.with_name("GRADING_new.md")
    grading.write_text(grading_md(questions, table, runs, files), encoding="utf-8")
    print(f"Phiếu chấm tay: {rel(grading)}")


if __name__ == "__main__":
    main()

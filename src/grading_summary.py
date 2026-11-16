# Tổng hợp phiếu chấm tay (eval/GRADING.md, eval/GRADING_extra.md) + số tự động qua nhiều lần chạy
#   Chạy: python -X utf8 -m src.grading_summary   -> in ra màn hình và ghi results/grading_summary.json
#   Không gọi API: chỉ đọc phiếu chấm, bộ câu hỏi và file metric của src.eval_answers
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHEETS = [ROOT / "eval" / "GRADING.md", ROOT / "eval" / "GRADING_extra.md"]  # 30 câu chính + câu bẫy no_answer
QUESTIONS = [ROOT / "eval" / "questions.jsonl", ROOT / "eval" / "questions_extra.jsonl"]  # lấy type và review của từng câu
RUNS = ROOT / "results" / "answers_dieu_hybrid_runs3.json"  # cấu hình chính (dieu + hybrid), mỗi câu hỏi 3 lần
OUT = ROOT / "results" / "grading_summary.json"
LABELS = ["Đúng", "Đúng một phần", "Sai", "Bịa", "Từ chối đúng", "Từ chối sai"]
# "Đúng một phần" đặt trước "Đúng" để regex khớp nhãn dài trước; "Bịa (nói điều ...)" chỉ cần khớp chữ "Bịa"
BOX = re.compile(r"\[([ xX])\] (Đúng một phần|Đúng|Sai|Bịa|Từ chối đúng|Từ chối sai)")


def read_sheet(path):
    """{id: [các ô được tick]}. Câu chưa tick ô nào -> danh sách rỗng (để liệt kê ra, không đoán)."""
    grades, cur = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        if m := re.match(r"## (\S+) \(", line):
            cur = m.group(1)
        elif cur and [b[1] for b in BOX.findall(line)] == LABELS:  # đúng dòng có đủ 6 ô, không nhầm với dòng khác
            grades[cur] = [label for mark, label in BOX.findall(line) if mark != " "]
            cur = None
    return grades


def ratio(n, total):
    return {"n": n, "of": total, "rate": round(n / total, 4) if total else None}


def main():
    all_q = {q["id"]: q for f in QUESTIONS
             for q in map(json.loads, filter(str.strip, f.read_text(encoding="utf-8").splitlines()))}
    # review = rejected: câu bị loại khi duyệt (văn bản có thể trả lời được) -> bỏ khỏi MỌI metric, kể cả số tự động.
    # File metric của eval_answers vẫn có các câu này nếu lúc chạy chúng còn trong bộ eval, nên phải lọc ở đây.
    rejected = sorted(i for i, q in all_q.items() if q.get("review") == "rejected")
    questions = {i: q for i, q in all_q.items() if i not in rejected}
    grades = {}
    for sheet in SHEETS:
        grades |= read_sheet(sheet)
    per_q = {p["id"]: p for p in json.loads(RUNS.read_text(encoding="utf-8"))["per_question"] if p["id"] in questions}

    missing = sorted(set(questions) - set(grades))  # có trong bộ eval nhưng không có trong phiếu chấm
    not_run = sorted(set(questions) - set(per_q))  # có trong bộ eval nhưng chưa có trong file metric
    ungraded = sorted(i for i, g in grades.items() if not g and i in questions)
    graded = {i: g for i, g in grades.items() if g and i in questions}
    is_na = lambda i: questions[i]["type"] == "no_answer"
    refused1 = {i: p["runs"][0]["refused"] for i, p in per_q.items()}  # lần 1 = lần được chấm tay

    # Ô "từ chối" phải khớp với việc bot có thật sự từ chối ở lần 1 không: lệch nhau = phiếu chấm có lỗi, báo ra
    mismatch = sorted(i for i, g in graded.items()
                      if bool({"Từ chối đúng", "Từ chối sai"} & set(g)) != refused1[i])

    ans_ids = [i for i in graded if not is_na(i)]
    na_ids = [i for i in graded if is_na(i)]
    count = lambda ids, labels: {"n_graded": len(ids), **{lab: sum(lab in graded[i] for i in ids) for lab in labels}}

    # Chỉ số chính: trong các câu bot CHỊU trả lời (không từ chối ở lần 1), bao nhiêu câu sai hoặc bịa.
    # Đếm theo câu (Sai và Bịa cùng tick ở 1 câu chỉ tính 1), vì người dùng chỉ gặp 1 câu trả lời sai.
    answered = [i for i in graded if not refused1[i]]
    bad = [i for i in answered if {"Sai", "Bịa"} & set(graded[i])]

    # Số tự động trên mọi lần chạy (không cần chấm tay): chỉ biết từ chối hay không, không biết đúng hay sai
    runs_of = lambda ids: [r for i in ids for r in per_q[i]["runs"]]
    auto_ans, auto_na = runs_of([i for i in per_q if not is_na(i)]), runs_of([i for i in per_q if is_na(i)])
    all_runs = auto_ans + auto_na
    automatic = {
        "n_runs_per_question": sorted({p["n_runs"] for p in per_q.values()}),
        "correct_refusal": ratio(sum(r["refused"] for r in auto_na), len(auto_na)),
        "false_refusal": ratio(sum(r["refused"] for r in auto_ans), len(auto_ans)),
        "inconsistent": [{"id": i, "n_refused": p["n_refused"], "n_runs": p["n_runs"]}
                         for i, p in per_q.items() if 0 < p["n_refused"] < p["n_runs"]],  # lúc từ chối lúc trả lời
        "runs_with_invalid_citation": ratio(sum(bool(r["invalid_citations"]) for r in all_runs), len(all_runs)),
        # trên các lần KHÔNG từ chối của câu có đáp án: chunk được trích có chứa đoạn bằng chứng không
        "cited_evidence": ratio(sum(bool(r["cited_evidence"]) for r in auto_ans if not r["refused"]),
                                sum(not r["refused"] for r in auto_ans)),
        "models_used": sorted({r["model"] for r in all_runs}),
    }

    res = {"sheets": [s.relative_to(ROOT).as_posix() for s in SHEETS], "runs_file": RUNS.relative_to(ROOT).as_posix(),
           "n_questions": len(questions), "n_answerable": sum(not is_na(i) for i in questions),
           "n_no_answer": sum(is_na(i) for i in questions), "excluded_rejected": rejected,
           "ungraded": ungraded, "missing_from_sheets": missing, "missing_from_runs": not_run,
           "tick_vs_refusal_mismatch": mismatch,
           "hand_graded_run1": {"answerable": count(ans_ids, ["Đúng", "Đúng một phần", "Sai", "Bịa", "Từ chối sai"]),
                                "no_answer": {**count(na_ids, ["Từ chối đúng", "Bịa"]), "ids": na_ids},
                                "wrong_or_fabricated_among_answered": {**ratio(len(bad), len(answered)), "ids": bad}},
           "automatic": automatic, "timestamp": datetime.now().isoformat(timespec="seconds")}
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

    a, na, w = res["hand_graded_run1"]["answerable"], res["hand_graded_run1"]["no_answer"], \
        res["hand_graded_run1"]["wrong_or_fabricated_among_answered"]
    print(f"Bộ eval: {res['n_questions']} câu ({res['n_answerable']} có đáp án, {res['n_no_answer']} no_answer)"
          + (f", đã loại (review = rejected): {rejected}" if rejected else ""))
    print(f"Chấm tay, lần 1 ({len(graded)} câu đã chấm)")
    print(f"  Câu có đáp án ({a['n_graded']}): Đúng {a['Đúng']}, Đúng một phần {a['Đúng một phần']}, Sai {a['Sai']}, "
          f"Bịa {a['Bịa']}, Từ chối sai {a['Từ chối sai']}")
    print(f"  Câu no_answer ({na['n_graded']}): Từ chối đúng {na['Từ chối đúng']}, Bịa {na['Bịa']}")
    print(f"  CHỈ SỐ CHÍNH, sai/bịa trên số câu bot trả lời: {w['n']}/{w['of']} = {w['rate']} {w['ids'] or ''}")
    c = automatic
    print(f"Tự động, mọi lần chạy (runs = {c['n_runs_per_question']})")
    print(f"  Từ chối đúng: {c['correct_refusal']['n']}/{c['correct_refusal']['of']} lần")
    print(f"  Từ chối sai: {c['false_refusal']['n']}/{c['false_refusal']['of']} lần")
    print("  Không nhất quán: " + (", ".join(f"{x['id']} (từ chối {x['n_refused']}/{x['n_runs']})"
                                             for x in c["inconsistent"]) or "không có"))
    print(f"  Lần chạy có trích dẫn không hợp lệ: {c['runs_with_invalid_citation']['n']}/{c['runs_with_invalid_citation']['of']}; "
          f"chunk được trích chứa bằng chứng: {c['cited_evidence']['n']}/{c['cited_evidence']['of']} lần trả lời; "
          f"model: {c['models_used']}")
    print(f"Câu chưa chấm: {ungraded or 'không có'}" + (f"; không có trong phiếu: {missing}" if missing else "")
          + (f"; chưa có trong file metric: {not_run}" if not_run else ""))
    if mismatch:
        print(f"CẢNH BÁO: ô từ chối không khớp với việc bot từ chối ở lần 1: {mismatch}")
    print(f"Kết quả: {OUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()

# Bước 2: làm sạch text từng trang, rồi chia thành chunk theo 2 cấu hình để so sánh ở bước 6:
#   A "dieu":   mỗi chunk = 1 Điều (Điều dài thì tách theo khoản) hoặc 1 mục của Phụ lục
#   B "window": cửa sổ cố định WINDOW ký tự, chồng lấn OVERLAP ký tự, không quan tâm cấu trúc
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "data" / "processed" / "pages.jsonl"
OUT_DIR = ROOT / "data" / "processed"
MAX_CHARS = 2500  # Điều dài hơn mức này thì tách theo khoản
WINDOW, OVERLAP = 1500, 225  # cấu hình B: khoảng 400-500 token, chồng lấn 15%

DROP_LINE = re.compile(  # quốc hiệu, tên cơ quan, ô số/ngày để trống: lặp lại, không mang thông tin
    r"^(BỘ GIÁO DỤC VÀ ĐÀO TẠO|ĐẠI HỌC BÁCH KHOA HÀ NỘI|CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM|CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM"
    r"|Độc lập\s*[-–]\s*Tự do\s*[-–]\s*Hạnh phúc|Số:\s*/QĐ-ĐHBK|Hà Nội, ngày\s+tháng\s+năm.*|\(Kèm theo Quyết định số.*"
    r"|của Giám đốc Đại học Bách khoa Hà Nội\))$"
)
ARTICLE = re.compile(r"^Điều\s+(\d{1,3})\.\s+(\S.*?)$")
CHAPTER = re.compile(r"^CHƯƠNG\s+([IVX]+)$")
APPENDIX = re.compile(r"^Phụ lục\s+([IVX]+)$")
SECTION = re.compile(r"^(Bảng\s+\d+\.\d+|(I|II|III)\.\S*\s|\d\)\s)")  # mục con trong Phụ lục
LEVEL1 = re.compile(r"^(I|II|III)\.\S*\s")  # mục cấp 1 trong Phụ lục ("II. ..."), bên trong có các mục "1)", "2)"
NEW_PARA = re.compile(r"^(\d{1,2}\.\s|[a-zđ]\)\s|[-+•]\s|Điều\s+\d|Bảng\s|CHƯƠNG\s|Phụ lục\s)")
CLAUSE = re.compile(r"^\d{1,2}\.\s")


def clean_page(text, cfg):
    """Trả về (các dòng đã làm sạch, trang này có kết thúc phần Quyết định hay không)."""
    for old, new in cfg["replace"].items():
        text = text.replace(old, new)
    lines = [re.sub(r"\s+", " ", l).strip() for l in text.split("\n")]  # gộp khoảng trắng lạ (U+202F...)
    lines = [l for l in lines if l]
    for tail in cfg["stamp_tails"]:  # số/ngày của chữ ký số nằm cuối trang: chỉ bỏ đúng chuỗi đã biết
        if lines[-len(tail):] == tail:
            lines = lines[: -len(tail)]
    if lines and re.fullmatch(r"\d{1,3}", lines[0]):  # số trang nằm ở dòng đầu
        lines = lines[1:]
    end_of_decision = False
    for i, l in enumerate(lines):  # cắt từ "Nơi nhận:" (khối chữ ký) hoặc chú thích cuối trang trở đi
        if l.startswith("Nơi nhận:") or any(re.match(p, l) for p in cfg["cut_from"]):
            end_of_decision = l.startswith("Nơi nhận:")
            lines = lines[:i]
            break
    return [l for l in lines if not DROP_LINE.match(l)], end_of_decision


def to_paragraphs(lines):
    """Nối các dòng bị ngắt giữa câu thành đoạn; dòng mở đầu khoản/điểm/Điều thì bắt đầu đoạn mới."""
    paras = []
    for page, line in lines:
        if paras and not NEW_PARA.match(line):
            prev_page, prev = paras[-1]
            sep = "" if re.search(r"\S-$", prev) else " "  # "quốc phòng-" + "an ninh" -> không thêm dấu cách
            paras[-1] = (prev_page, prev + sep + line)
        else:
            paras.append((page, line))
    return paras


def read_docs():
    docs = {d["doc_id"]: d for d in json.loads((ROOT / "data" / "manifest.json").read_text(encoding="utf-8"))}
    lines = {d: [] for d in docs}  # doc -> [(page, part, line)]
    part = {d: "qd" for d in docs}  # "qd" = phần Quyết định ban hành, "body" = phần quy chế/quy định
    for row in map(json.loads, PAGES.open(encoding="utf-8")):
        doc = docs[row["doc"]]
        if row["page"] in doc["clean"]["skip_pages"]:
            continue
        page_lines, end_qd = clean_page(row["text"], doc["clean"])
        lines[row["doc"]] += [(row["page"], part[row["doc"]], l) for l in page_lines]
        if end_qd:
            part[row["doc"]] = "body"
    return docs, lines


def structural_units(doc, rows):
    """Đi qua từng dòng, theo dõi đang ở Chương/Điều/Phụ lục/mục nào, gom dòng thành từng đơn vị."""
    units, cur = [], None
    chapter = appendix = section = ""  # section = mục cấp 1 đang mở trong Phụ lục
    expect_title = None  # dòng ngay sau "CHƯƠNG II"/"Phụ lục I" là tiêu đề của nó
    for page, part, line in rows:
        if expect_title:
            if expect_title == "chapter":
                chapter += ". " + line
            else:
                appendix += ". " + line
                cur["heading"] = appendix
            expect_title = None
            cur["lines"].append((page, line))
            continue
        if m := CHAPTER.match(line):
            chapter, expect_title = f"Chương {m.group(1)}", "chapter"
            continue
        start = None
        if m := ARTICLE.match(line):
            start = {"dieu": int(m.group(1)), "heading": f"Điều {m.group(1)}. {m.group(2)}"}
        elif m := APPENDIX.match(line):
            appendix, chapter, section, expect_title = f"Phụ lục {m.group(1)}", "", "", "appendix"  # Phụ lục mới -> bỏ mục cấp 1 cũ
            start = {"dieu": None, "heading": appendix}
        elif appendix and SECTION.match(line):
            if LEVEL1.match(line):
                section = line[:80]
                path = [appendix, section]
            else:  # "1) Các chương trình đào tạo chuẩn" có ở cả mục I (chính quy) và mục II (vừa làm vừa học) -> giữ mục cấp 1
                path = [appendix, section, line[:80]]
            start = {"dieu": None, "heading": " > ".join(x for x in path if x)}
        if start or cur is None or cur["part"] != part:
            cur = {"doc": doc["doc_id"], "part": part, "chapter": chapter, "appendix": appendix,
                   "dieu": None, "heading": "Phần mở đầu", "lines": [], **(start or {})}
            units.append(cur)
        cur["lines"].append((page, line))
    return units


def make_chunk(doc, unit, unit_no, paras, idx):
    title = f"{doc['title']} ({doc['so_hieu']})" + (" - Quyết định ban hành" if unit["part"] == "qd" else "")
    path = " > ".join(x for x in [unit["chapter"], unit["heading"]] if x)
    note = doc.get("appendix_note", {}).get(unit["appendix"].removeprefix("Phụ lục ").split(".")[0], "")
    body = "\n".join(p for _, p in paras)
    name = f"d{unit['dieu']}" if unit["dieu"] else f"u{unit_no}"  # d5 = Điều 5, u12 = đơn vị thứ 12 (không phải Điều)
    return {
        "id": f"{doc['doc_id']}:{unit['part']}:{name}:{idx}",
        "doc": doc["doc_id"], "part": unit["part"], "dieu": unit["dieu"], "heading": unit["heading"],
        "pages": sorted({p for p, _ in paras}),
        "text": f"[{title}] {path}\n" + (note + "\n" if note else "") + body,  # tiêu đề giúp embedding hiểu ngữ cảnh
    }


def chunks_by_article(docs, lines):
    chunks = []
    for doc_id, rows in lines.items():
        for unit_no, unit in enumerate(structural_units(docs[doc_id], rows)):
            paras = to_paragraphs(unit["lines"])
            groups, cur = [], []
            for page, p in paras:  # Điều quá dài: gom các khoản liền nhau cho đến khi gần MAX_CHARS
                if cur and CLAUSE.match(p) and sum(len(x) for _, x in cur) + len(p) > MAX_CHARS:
                    groups.append(cur)
                    cur = []
                cur.append((page, p))
            groups.append(cur)
            chunks += [make_chunk(docs[doc_id], unit, unit_no, g, i) for i, g in enumerate(groups) if g]
    return chunks


def chunks_by_window(docs, lines):
    chunks = []
    for doc_id, rows in lines.items():
        paras = to_paragraphs([(p, l) for p, _, l in rows])
        text, page_at = "", []  # page_at[i] = trang của ký tự thứ i
        for page, p in paras:
            text += p + "\n"
            page_at += [page] * (len(p) + 1)
        for i, start in enumerate(range(0, len(text), WINDOW - OVERLAP)):
            piece = text[start:start + WINDOW]
            chunks.append({"id": f"{doc_id}:w:{i}", "doc": doc_id, "part": None, "dieu": None, "heading": None,
                           "pages": sorted(set(page_at[start:start + WINDOW])),
                           "text": f"[{docs[doc_id]['title']}]\n{piece}"})
            if start + WINDOW >= len(text):
                break
    return chunks


def main():
    docs, lines = read_docs()
    for name, chunks in [("dieu", chunks_by_article(docs, lines)), ("window", chunks_by_window(docs, lines))]:
        out = OUT_DIR / f"chunks_{name}.jsonl"
        out.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in chunks), encoding="utf-8")
        sizes = sorted(len(c["text"]) for c in chunks)
        print(f"{name:>6}: {len(chunks)} chunk, dài trung bình {sum(sizes) // len(sizes)} ký tự, "
              f"ngắn nhất {sizes[0]}, dài nhất {sizes[-1]} -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

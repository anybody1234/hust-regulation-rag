# Bước 1: tải 3 PDF (có cache + kiểm tra sha256) rồi tách chữ theo từng trang -> data/processed/pages.jsonl
import hashlib
import json
import unicodedata
import urllib.request
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "manifest.json"
RAW_DIR = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed" / "pages.jsonl"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def download(doc):
    path = RAW_DIR / f"{doc['doc_id']}.pdf"
    if not path.exists():  # cache: chỉ tải lần đầu, lần sau dùng lại file trong data/raw/
        print(f"Đang tải {doc['doc_id']} ...")
        path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(doc["url"], path)
    if doc["sha256"] and sha256(path) != doc["sha256"]:  # file khác bản đã kiểm tra = văn bản có thể đã bị thay
        raise ValueError(f"{doc['doc_id']}: sha256 không khớp manifest, hãy kiểm tra lại văn bản")
    return path


def extract_pages(path):
    with pymupdf.open(path) as pdf:
        for i, page in enumerate(pdf):
            text = unicodedata.normalize("NFC", page.get_text("text"))  # NFC: thống nhất 1 cách mã hoá dấu tiếng Việt
            yield i + 1, text  # đánh số trang từ 1, giống số trang khi mở PDF


def main():
    docs = json.loads(MANIFEST.read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for doc in docs:
            path = download(doc)
            n = 0
            for page, text in extract_pages(path):
                f.write(json.dumps({"doc": doc["doc_id"], "page": page, "text": text}, ensure_ascii=False) + "\n")
                n += 1
            print(f"{doc['doc_id']}: {n} trang, sha256 = {sha256(path)[:12]}...")
    print(f"Đã ghi {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

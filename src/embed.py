# Bước 4a: biến text thành vector bằng Gemini Embedding, lưu index numpy -> data/index/{config}.npy + .json
#   Chạy: python -X utf8 -m src.embed   (chunk không đổi thì dùng lại index cũ, không tốn quota)
import functools
import hashlib
import json
import os
import time
import unicodedata
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = ROOT / "data" / "index"
QUERY_CACHE = INDEX_DIR / "query_cache.json"
MODEL, DIM = "gemini-embedding-2", 768
BATCH = 50  # 1 lần gọi tối đa 100 text; free tier tối đa 100 text/phút (mỗi text tính là 1 request) -> lấy 50 cho an toàn
# Model này nhận loại tác vụ qua tiền tố trong text (tham số task_type bị bỏ qua: đã thử, vector gần như y hệt)
PREFIX = {"document": "title: none | text: ", "query": "task: search result | query: "}

load_dotenv(ROOT / ".env")  # đọc GEMINI_API_KEY từ file .env vào biến môi trường (không in key ra đâu cả)


@functools.cache  # chỉ tạo client 1 lần, và chỉ khi thật sự cần gọi API (BM25 không cần key)
def client():
    retry = types.HttpRetryOptions(attempts=8, initial_delay=2, max_delay=60)  # gặp 429/503: đợi 2, 4, 8... giây rồi thử lại
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"], http_options=types.HttpOptions(retry_options=retry))


def embed_texts(texts, kind):
    """kind = "document" hoặc "query". Trả về mảng float32 (số text, DIM), mỗi dòng là 1 vector độ dài 1."""
    vecs = []
    for i in range(0, len(texts), BATCH):
        # Mỗi text phải bọc trong 1 Content riêng; truyền list chuỗi thì API gộp tất cả thành 1 vector
        contents = [types.Content(parts=[types.Part(text=PREFIX[kind] + t)]) for t in texts[i:i + BATCH]]
        res = client().models.embed_content(model=MODEL, contents=contents,
                                            config=types.EmbedContentConfig(output_dimensionality=DIM))
        vecs += [e.values for e in res.embeddings]
    vecs = np.array(vecs, dtype=np.float32)
    assert len(vecs) == len(texts), f"gửi {len(texts)} text nhưng nhận {len(vecs)} vector"
    return vecs / np.linalg.norm(vecs, axis=1, keepdims=True)  # chuẩn hoá L2 -> cosine = tích vô hướng


def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chunks_path(config):
    return ROOT / "data" / "processed" / f"chunks_{config}.jsonl"


def build_index(config):
    """Embed mọi chunk của 1 config ("dieu" hoặc "window"). Bỏ qua nếu file chunk và model không đổi."""
    path, meta_path = chunks_path(config), INDEX_DIR / f"{config}.json"
    meta = {"model": MODEL, "dim": DIM, "sha256": file_sha256(path)}
    if meta_path.exists() and (INDEX_DIR / f"{config}.npy").exists():
        old = json.loads(meta_path.read_text(encoding="utf-8"))
        if {k: old.get(k) for k in meta} == meta:  # cache: cùng nội dung chunk + cùng model -> khỏi gọi API
            print(f"{config}: chunk không đổi, dùng lại index cũ ({len(old['ids'])} vector)")
            return
    chunks = [json.loads(line) for line in path.open(encoding="utf-8")]
    print(f"{config}: đang embed {len(chunks)} chunk (free tier 100 text/phút, có thể phải đợi khoảng 1 phút)...")
    t0 = time.perf_counter()
    vecs = embed_texts([c["text"] for c in chunks], "document")
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    np.save(INDEX_DIR / f"{config}.npy", vecs)  # ghi vector trước, ghi .json sau: lỡ dừng giữa chừng thì lần sau embed lại
    meta["ids"] = [c["id"] for c in chunks]  # dòng i của .npy là vector của chunk ids[i]
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{config}: xong {vecs.shape} trong {time.perf_counter() - t0:.1f}s -> {meta_path.relative_to(ROOT)}")


_query_cache = None


def embed_query(text):
    """Trả về (vector câu hỏi, số ms gọi API). Có cache trên đĩa: hỏi lại câu cũ thì không tốn quota."""
    global _query_cache
    if _query_cache is None:
        _query_cache = json.loads(QUERY_CACHE.read_text(encoding="utf-8")) if QUERY_CACHE.exists() else {}
    key = f"{MODEL}|{DIM}|{unicodedata.normalize('NFC', text)}"  # đổi model thì vector cũ vô nghĩa -> đưa model vào khoá
    if key not in _query_cache:
        t0 = time.perf_counter()
        vec = embed_texts([unicodedata.normalize("NFC", text)], "query")[0]
        ms = (time.perf_counter() - t0) * 1000  # lưu thời gian gọi API thật lần đầu để đo latency khi chạy lại
        _query_cache[key] = {"ms": round(ms, 1), "vec": vec.tolist()}
        INDEX_DIR.mkdir(parents=True, exist_ok=True)
        QUERY_CACHE.write_text(json.dumps(_query_cache, ensure_ascii=False), encoding="utf-8")
    hit = _query_cache[key]
    return np.array(hit["vec"], dtype=np.float32), hit["ms"]


def main():
    try:
        for config in ["dieu", "window"]:
            build_index(config)
    except errors.APIError as e:
        if e.code != 429:
            raise
        print("Lỗi 429: hết quota free tier dù đã thử lại nhiều lần. Đợi vài phút rồi chạy lại "
              "(config nào đã xong thì được giữ trong cache).")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

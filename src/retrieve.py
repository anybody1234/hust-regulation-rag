# Bước 4b: tìm các chunk liên quan tới câu hỏi bằng 3 cách:
#   dense  = so nghĩa: cosine giữa vector câu hỏi và vector chunk (Gemini Embedding)
#   bm25   = so từ khoá: BM25 tự viết
#   hybrid = gộp 2 bảng xếp hạng trên bằng Reciprocal Rank Fusion (RRF)
import functools
import json
import math
import re
import unicodedata
from collections import Counter

import numpy as np

from src.embed import INDEX_DIR, chunks_path, embed_query, file_sha256

K1, B = 1.5, 0.75  # tham số BM25: K1 = mức bão hoà tần suất từ, B = mức phạt chunk dài
RRF_K = 60  # hằng số RRF (giá trị của bài báo gốc): làm điểm giữa hạng 1 và hạng 2 không chênh quá nhiều


def tokenize(text):
    # \w+ bắt từng âm tiết tiếng Việt ("học", "phần", "14"), vì chữ có dấu cũng là ký tự \w trong Python
    return re.findall(r"\w+", unicodedata.normalize("NFC", text).lower())


class BM25:
    """BM25 = TF-IDF có thêm 2 cải tiến. Điểm của chunk d với câu hỏi q:
        score(q, d) = Σ_{từ w trong q} IDF(w) · tf·(K1+1) / (tf + K1·(1 − B + B·|d|/avgdl))
    - tf = số lần w xuất hiện trong d. Cải tiến 1, bão hoà tf: tf tăng thì điểm tăng chậm dần và không vượt
      quá IDF·(K1+1), nên một từ lặp 10 lần không được điểm gấp 10 lần (TF-IDF thường thì tăng tuyến tính).
    - |d| = độ dài chunk, avgdl = độ dài trung bình. Cải tiến 2, chuẩn hoá độ dài: chunk dài hơn trung bình
      thì mẫu số lớn hơn -> điểm giảm (chunk dài tự nhiên chứa nhiều từ hơn). B = 0 thì bỏ qua độ dài.
    - IDF(w) = log(1 + (N − df + 0.5) / (df + 0.5)), df = số chunk chứa w: từ hiếm -> IDF lớn, giống TF-IDF.
    """

    def __init__(self, texts):
        self.tfs = [Counter(tokenize(t)) for t in texts]  # mỗi chunk: {từ: số lần xuất hiện}
        self.lens = np.array([sum(tf.values()) for tf in self.tfs])  # |d| tính bằng số từ
        self.avgdl = self.lens.mean()
        df = Counter(w for tf in self.tfs for w in tf)  # duyệt từ khác nhau của từng chunk -> đếm số chunk chứa w
        n = len(texts)
        self.idf = {w: math.log(1 + (n - c + 0.5) / (c + 0.5)) for w, c in df.items()}

    def scores(self, query):
        """Trả về mảng điểm BM25, mỗi phần tử ứng với 1 chunk."""
        total = np.zeros(len(self.tfs))
        for w in set(tokenize(query)):  # mỗi từ khác nhau trong câu hỏi
            if w not in self.idf:  # từ không có trong chunk nào -> không đóng góp điểm
                continue
            tf = np.array([d[w] for d in self.tfs])  # tf của w trong từng chunk (tính cho mọi chunk cùng lúc)
            total += self.idf[w] * tf * (K1 + 1) / (tf + K1 * (1 - B + B * self.lens / self.avgdl))
        return total


@functools.cache  # mỗi config chỉ nạp chunk + vector và dựng BM25 đúng 1 lần
def load(config):
    path = chunks_path(config)
    meta = json.loads((INDEX_DIR / f"{config}.json").read_text(encoding="utf-8"))
    if meta["sha256"] != file_sha256(path):  # chunk đã đổi mà chưa embed lại -> vector lệch với text
        raise RuntimeError(f"Index {config} đã cũ, hãy chạy: python -X utf8 -m src.embed")
    chunks = [json.loads(line) for line in path.open(encoding="utf-8")]
    vecs = np.load(INDEX_DIR / f"{config}.npy")
    return chunks, vecs, BM25([c["text"] for c in chunks])


def scores_for(question, mode, config):
    """Mảng điểm của mọi chunk theo 1 mode. Điểm càng cao càng liên quan."""
    chunks, vecs, bm25 = load(config)
    if mode == "dense":
        qvec, _ = embed_query(question)
        return vecs @ qvec  # các vector đều có độ dài 1 -> tích vô hướng chính là cosine
    if mode == "bm25":
        return bm25.scores(question)
    if mode == "hybrid":
        fused = np.zeros(len(chunks))
        for m in ["dense", "bm25"]:
            order = np.argsort(-scores_for(question, m, config), kind="stable")  # order[0] = chunk hạng 1
            fused[order] += 1 / (RRF_K + np.arange(1, len(order) + 1))  # chunk hạng r được cộng 1 / (60 + r)
        return fused  # chỉ dùng thứ hạng, không dùng điểm gốc -> không cần đưa cosine và BM25 về cùng thang
    raise ValueError(f"mode phải là dense, bm25 hoặc hybrid, không phải {mode!r}")


def search(question, k=5, mode="dense", config="dieu"):
    """Trả về k cặp (chunk, điểm) liên quan nhất, điểm giảm dần."""
    question = unicodedata.normalize("NFC", question).strip()  # cùng chuẩn NFC với text đã tách từ PDF
    chunks = load(config)[0]
    scores = scores_for(question, mode, config)
    top = np.argsort(-scores, kind="stable")[:k]
    return [(chunks[i], float(scores[i])) for i in top]


if __name__ == "__main__":  # thử nhanh: python -X utf8 -m src.retrieve
    for mode in ["dense", "bm25", "hybrid"]:
        print(f"--- {mode}")
        for chunk, score in search("Điểm thành phần bao nhiêu thì bị điểm liệt?", k=3, mode=mode):
            print(f"{score:.3f}  {chunk['id']}  {chunk['heading']}")

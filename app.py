# Bước 8: giao diện web hỏi đáp quy chế. Chạy: streamlit run app.py
import streamlit as st
from google.genai import errors

from src.generate import DOCS, answer

st.set_page_config(page_title="Hỏi đáp quy chế HUST")
st.title("Hỏi đáp quy chế ĐHBK Hà Nội")
st.caption("Chỉ trả lời dựa trên: " + "; ".join(f"{d['title']} ({d['so_hieu']})" for d in DOCS.values())
           + ". Hãy mở nguồn để kiểm tra lại văn bản gốc.")

with st.sidebar:  # các lựa chọn để so sánh thí nghiệm ngay trên giao diện
    mode = st.selectbox("Cách tìm kiếm", ["hybrid", "dense", "bm25"])
    config = st.selectbox("Cách chia chunk", ["dieu", "window"])
    k = st.slider("Số chunk đưa cho LLM (k)", 1, 10, 5)


@st.cache_data(show_spinner=False)  # Streamlit chạy lại cả file sau mỗi thao tác -> cache để không tốn quota hỏi lại
def cached_answer(question, k, mode, config):
    return answer(question, k=k, mode=mode, config=config)


question = st.text_input("Câu hỏi", placeholder="VD: Bị cảnh báo học tập mức 2 thì được đăng ký tối đa bao nhiêu tín chỉ?")
if question.strip():
    try:
        with st.spinner("Đang tìm văn bản và hỏi Gemini..."):
            r = cached_answer(question.strip(), k, mode, config)
    except errors.APIError as e:
        if e.code not in (429, 503):
            raise
        st.warning("Gemini đang hết quota miễn phí hoặc quá tải. Bạn đợi khoảng 1 phút rồi hỏi lại nhé.")
        st.stop()

    if r["refused"]:
        st.info(r["answer"])  # câu từ chối hiện trong khung màu cho dễ nhận ra
    else:
        st.markdown(r["answer"])
    if r["citations"]:
        st.subheader("Nguồn")
    for c in r["citations"]:
        p = c["pages"]
        pages = f"{p[0]}-{p[-1]}" if len(p) > 1 else f"{p[0]}"
        where = c["heading"] or "đoạn trích"  # cấu hình window không có tên Điều
        # "#page=N" làm trình đọc PDF của trình duyệt mở thẳng tới trang N
        st.markdown(f"[{c['n']}] [{c['doc_title']} ({c['so_hieu']})]({c['url']}#page={p[0]}), {where}, trang {pages}")
    if r["invalid_citations"]:
        st.warning(f"Bot trích tài liệu không tồn tại: {r['invalid_citations']}. Đừng tin các câu đó.")

    with st.expander(f"{len(r['chunks'])} đoạn văn bản tìm được ({mode}, {config})"):
        for c in r["chunks"]:
            st.markdown(f"**{c['n']}.** `{c['id']}`, điểm {c['score']:.4f}")
            st.text(c["text"])

    lat, u = r["latency_ms"], r["usage"]
    st.caption(f"{r['model']} | tìm kiếm {lat['retrieve']:.0f} ms, LLM {lat['llm']:.0f} ms, tổng {lat['total']:.0f} ms | "
               f"token vào {u.get('prompt_tokens')}, ra {u.get('output_tokens')}, thinking {u.get('thoughts_tokens')}")

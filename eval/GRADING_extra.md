# Phiếu chấm tay câu trả lời của bot

Bộ eval: `eval/questions_extra.jsonl`. Đáp án chuẩn lấy từ bộ eval (trường `review` cho biết câu nào đã được đối chiếu thủ công với PDF).

Cách chấm: với mỗi câu, đọc câu trả lời của bot, mở nguồn bot trích (đúng văn bản, đúng trang) rồi đánh `[x]` vào ô phù hợp:
- **Đúng**: đủ ý chính như đáp án chuẩn, mọi chi tiết đều có trong văn bản.
- **Đúng một phần**: đúng nhưng thiếu ý quan trọng, hoặc thêm điều kiện không cần thiết.
- **Sai**: nêu sai con số/điều kiện so với văn bản.
- **Bịa**: nêu điều KHÔNG có trong văn bản (kể cả khi có ghi trích dẫn). Có thể đánh cùng ô khác.
- **Từ chối đúng**: câu `no_answer` và bot trả lời "Không tìm thấy trong quy chế".
- **Từ chối sai**: câu có đáp án nhưng bot từ chối.
Cột tự động `cited-evidence` = có ít nhất 1 chunk được bot TRÍCH chứa câu bằng chứng của bộ eval. Chỉ là gợi ý, không thay chấm tay.

Mỗi câu được hỏi 3 lần, phiếu chỉ hiện **lần 1**. Dòng ⚠️ = câu không nhất quán (lúc từ chối, lúc trả lời).

## x01 (no_answer)

**Câu hỏi:** Năm học 2025–2026, học phí một tín chỉ học phí của ngành Khoa học máy tính (chương trình chuẩn) là bao nhiêu?

**Đáp án chuẩn:** Không tìm thấy trong quy chế

**Bot trả lời** (gemini-3.5-flash-lite):

> Không tìm thấy trong quy chế.

**Nguồn bot trích:**
- (không có)

Tự động: cited-evidence = không áp dụng; bot từ chối = có

[ ] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [x] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Tự động: bot trả lời đúng câu từ chối (từ chối 3/3 lần).

## x02 (no_answer)

**Câu hỏi:** Sinh viên khóa K70 học chương trình chuẩn cần chứng chỉ tiếng Anh tối thiểu bậc mấy để đạt chuẩn ngoại ngữ đầu ra khi xét tốt nghiệp?

**Đáp án chuẩn:** Không tìm thấy trong quy chế

**Bot trả lời** (gemini-3.5-flash-lite):

> Không tìm thấy trong quy chế.

**Nguồn bot trích:**
- (không có)

Tự động: cited-evidence = không áp dụng; bot từ chối = có

[ ] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [x] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Tự động: bot trả lời đúng câu từ chối (từ chối 3/3 lần).

## x03 (no_answer)

**Câu hỏi:** e lỡ làm mất thẻ sv r, xin cap lai o dau va có mất phí ko ạ

**Đáp án chuẩn:** Không tìm thấy trong quy chế

**Bot trả lời** (gemini-3.5-flash-lite):

> Không tìm thấy trong quy chế. Thông tin này có thể được quy định tại các hướng dẫn về công tác sinh viên hoặc quy định về thu phí, lệ phí của Đại học Bách khoa Hà Nội.

**Nguồn bot trích:**
- (không có)

Tự động: cited-evidence = không áp dụng; bot từ chối = có

[ ] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [x] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Tự động: bot trả lời đúng câu từ chối (từ chối 3/3 lần).

## x04 (no_answer)

**Câu hỏi:** Sinh viên chính quy có bắt buộc phải mua bảo hiểm y tế qua trường không, và mức đóng một năm là bao nhiêu?

**Đáp án chuẩn:** Không tìm thấy trong quy chế

**Bot trả lời** (gemini-3.5-flash-lite):

> Không tìm thấy trong quy chế.

**Nguồn bot trích:**
- (không có)

Tự động: cited-evidence = không áp dụng; bot từ chối = có

[ ] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [x] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Tự động: bot trả lời đúng câu từ chối (từ chối 3/3 lần).

## x05 (no_answer)

**Câu hỏi:** Sinh viên thuộc hộ cận nghèo được giảm bao nhiêu phần trăm học phí năm học 2026–2027?

**Đáp án chuẩn:** Không tìm thấy trong quy chế

**Bot trả lời** (gemini-3.5-flash-lite):

> Không tìm thấy trong quy chế.

**Nguồn bot trích:**
- (không có)

Tự động: cited-evidence = không áp dụng; bot từ chối = có

[ ] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [x] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Tự động: bot trả lời đúng câu từ chối (từ chối 3/3 lần).

## x06 (no_answer)

**Câu hỏi:** hạn chót đóng hp kì 1 năm 2026-2027 la ngay nao vay mn, sợ bị muộn

**Đáp án chuẩn:** Không tìm thấy trong quy chế

**Bot trả lời** (gemini-3.5-flash-lite):

> Không tìm thấy trong quy chế.

**Nguồn bot trích:**
- (không có)

Tự động: cited-evidence = không áp dụng; bot từ chối = có

[ ] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [x] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Tự động: bot trả lời đúng câu từ chối (từ chối 3/3 lần).

## x07 (no_answer)

**Câu hỏi:** Thi HUST English Placement Test đầu khóa có phải nộp lệ phí không, nếu có thì bao nhiêu tiền?

**Đáp án chuẩn:** Không tìm thấy trong quy chế

**Bot trả lời** (gemini-3.5-flash-lite):

> Không tìm thấy trong quy chế.

**Nguồn bot trích:**
- (không có)

Tự động: cited-evidence = không áp dụng; bot từ chối = có

[ ] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [x] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Tự động: bot trả lời đúng câu từ chối (từ chối 3/3 lần).

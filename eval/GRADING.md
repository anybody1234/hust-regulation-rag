# Phiếu chấm tay câu trả lời của bot

Bộ eval: `eval/questions.jsonl`. Đáp án chuẩn lấy từ bộ eval (trường `review` cho biết câu nào đã được đối chiếu thủ công với PDF).

Cách chấm: với mỗi câu, đọc câu trả lời của bot, mở nguồn bot trích (đúng văn bản, đúng trang) rồi đánh `[x]` vào ô phù hợp:
- **Đúng**: đủ ý chính như đáp án chuẩn, mọi chi tiết đều có trong văn bản.
- **Đúng một phần**: đúng nhưng thiếu ý quan trọng, hoặc thêm điều kiện không cần thiết.
- **Sai**: nêu sai con số/điều kiện so với văn bản.
- **Bịa**: nêu điều KHÔNG có trong văn bản (kể cả khi có ghi trích dẫn). Có thể đánh cùng ô khác.
- **Từ chối đúng**: câu `no_answer` và bot trả lời "Không tìm thấy trong quy chế".
- **Từ chối sai**: câu có đáp án nhưng bot từ chối.
Cột tự động `cited-evidence` = có ít nhất 1 chunk được bot TRÍCH chứa câu bằng chứng của bộ eval. Chỉ là gợi ý, không thay chấm tay.

Mỗi câu được hỏi 3 lần, phiếu chỉ hiện **lần 1**. Dòng ⚠️ = câu không nhất quán (lúc từ chối, lúc trả lời).

## q01 (single)

**Câu hỏi:** Em học chương trình chuẩn, đang bị cảnh báo học tập mức 2 thì một học kỳ chính được đăng ký tối đa bao nhiêu tín chỉ?

**Đáp án chuẩn:** Tối đa 14 TC và tối thiểu 8 TC cho một học kỳ chính (sinh viên ELITECH và CTĐT hợp tác quốc tế: tối đa 18 TC, tối thiểu 8 TC).

**Bot trả lời** (gemini-3.5-flash-lite):

> Sinh viên thuộc chương trình chuẩn đang bị cảnh báo học tập từ mức 2 trở lên được đăng ký tối đa 14 tín chỉ cho một học kỳ chính [1].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 19. Cảnh báo học tập và buộc thôi học, trang 18-19

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Bot trích dẫn chính xác Điều 19 quy chế về giới hạn tín chỉ cho sinh viên chuẩn bị cảnh báo mức 2 (tối đa 14 TC).

## q02 (single)

**Câu hỏi:** Nếu em làm đơn rút một học phần trong 7 tuần đầu của học kỳ thì có phải đóng học phí học phần đó không?

**Đáp án chuẩn:** Có. Nếu đơn được chấp thuận thì chỉ phải đóng 50% học phí học phần đó; ngoại lệ: rút trong tuần đầu tiên của học kỳ thứ 2 thì không phải đóng. Quy định này không áp dụng cho học kỳ hè.

**Bot trả lời** (gemini-3.5-flash-lite):

> Người học thuộc chương trình đào tạo cử nhân, kỹ sư có đơn đề nghị rút học phần trong khoảng thời gian 7 tuần đầu của học kỳ, nếu được giải quyết theo nguyện vọng thì chỉ đóng một nửa (50%) học phí của học phần đó [1]. Trường hợp ngoại lệ là khi đề nghị rút học phần trong tuần đầu tiên của học kỳ thứ 2, nếu được giải quyết theo nguyện vọng thì không phải đóng học phí của học phần đó [1]. Quy định này không áp dụng với các học phần học ở học kỳ hè [1].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 9. Học phí, trang 11

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Đáp án chuẩn xác theo Điều 9, nêu rõ quy định đóng 50% học phí khi rút trong 7 tuần đầu và các ngoại lệ.

## q03 (single)

**Câu hỏi:** Em đã tích lũy được 70 tín chỉ thì được xếp trình độ năm thứ mấy?

**Đáp án chuẩn:** Năm thứ ba (số tín chỉ tích lũy từ 64 đến 95).

**Bot trả lời** (gemini-3.5-flash-lite):

> Sinh viên tích lũy được 70 tín chỉ sẽ được xếp trình độ năm thứ ba [1].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 12. Ý kiến phản hồi của người học, đánh giá kết quả học tập, trang 13-14

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Đúng mốc tín chỉ xếp trình độ năm thứ ba (từ 64 đến 95 TC).

## q04 (single)

**Câu hỏi:** Muốn phúc tra hoặc khiếu nại điểm học phần thì phải gửi đề nghị trong thời hạn bao lâu?

**Đáp án chuẩn:** Trong vòng 7 ngày kể từ khi điểm học phần được cập nhật vào tài khoản học tập; không áp dụng với học phần thi vấn đáp hoặc đánh giá trước hội đồng.

**Bot trả lời** (gemini-3.5-flash-lite):

> Người học có thể đề nghị phúc tra hoặc khiếu nại điểm trong thời hạn 7 ngày kể từ khi điểm học phần được cập nhật vào tài khoản học tập của người học, tuy nhiên không áp dụng với các học phần tổ chức thi theo hình thức vấn đáp hoặc đánh giá trước hội đồng [1].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 6. Hoãn thi, miễn thi, phúc tra và khiếu nại điểm, trang 10

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Chính xác thời hạn 7 ngày và điều kiện ngoại lệ không áp dụng cho thi vấn đáp/hội đồng theo Điều 6.

## q05 (single)

**Câu hỏi:** Điểm thành phần bao nhiêu thì bị coi là điểm liệt?

**Đáp án chuẩn:** Dưới 3 điểm với các học phần thông thường; dưới 5 điểm với đồ án/khóa luận tốt nghiệp cử nhân và đồ án tốt nghiệp kỹ sư. Có một điểm thành phần bị liệt thì điểm học phần là F.

**Bot trả lời** (gemini-3.5-flash-lite):

> Điểm thành phần (điểm quá trình và điểm cuối kỳ) dưới 5 đối với học phần đồ án tốt nghiệp/khóa luận tốt nghiệp cử nhân, đồ án tốt nghiệp kỹ sư được coi là điểm liệt [1]. Đối với các học phần khác, điểm thành phần dưới 3 được coi là điểm liệt [1].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 5. Điểm học phần, trang 9-10

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Phân định rõ ràng điểm liệt dưới 3 với học phần thường và dưới 5 với đồ án/khóa luận tốt nghiệp đúng như Điều 5.

## q06 (single)

**Câu hỏi:** Em muốn chuyển sang học một chương trình đào tạo khác thì cần đáp ứng những điều kiện gì?

**Đáp án chuẩn:** Phải học hết năm thứ nhất và đáp ứng đủ: đạt điều kiện trúng tuyển của CTĐT muốn chuyển sang; CPA xếp loại khá trở lên (CPA ≥ 2,5); không bị cảnh báo học tập; hiện không bị kỷ luật.

**Bot trả lời** (gemini-3.5-flash-lite):

> Sinh viên học hết năm học thứ nhất (tính cả thời gian nghỉ tạm thời nếu có) được xem xét chuyển sang học một chương trình đào tạo khác nếu đáp ứng đủ các điều kiện sau:
> - Đáp ứng điều kiện trúng tuyển của chương trình đào tạo muốn chuyển sang học [1].
> - Xếp loại học lực căn cứ theo điểm trung bình tích lũy (CPA) đạt từ loại khá trở lên (CPA ≥ 2,5) [1].
> - Không bị cảnh báo học tập [1].
> - Hiện đang không bị kỷ luật [1].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 17. Chuyển chương trình đào tạo, hình thức đào tạo, trang 17

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Liệt kê đầy đủ 4 điều kiện chuyển ngành (học hết năm 1, CPA $\ge 2.5$, không bị cảnh báo, không kỷ luật) theo Điều 17.

## q07 (single)

**Câu hỏi:** Sớm nhất là khi nào thì em được đăng ký học thêm chương trình thứ hai, và cần điều kiện gì?

**Đáp án chuẩn:** Sớm nhất khi đã được xếp trình độ năm thứ hai của chương trình thứ nhất; tại thời điểm đăng ký phải có CPA xếp loại từ trung bình trở lên và đáp ứng điều kiện trúng tuyển của chương trình thứ hai trong năm tuyển sinh.

**Bot trả lời** (gemini-3.5-flash-lite):

> Sinh viên được phép đăng ký học chương trình thứ hai sớm nhất khi đã được xếp trình độ năm thứ hai của chương trình thứ nhất [1]. Tại thời điểm đăng ký, sinh viên phải có học lực tính theo điểm trung bình tích lũy (CPA) xếp loại từ trung bình trở lên và đáp ứng điều kiện trúng tuyển của chương trình thứ hai trong năm tuyển sinh [1].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 18. Học cùng lúc hai chương trình, trang 18

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Trả lời chính xác điều kiện học cùng lúc hai chương trình theo Điều 18.

## q08 (single)

**Câu hỏi:** Em muốn xin nghỉ học tạm thời vì lý do cá nhân (không phải do ốm, thai sản, tai nạn hay nhập ngũ) thì được nghỉ tối đa bao lâu?

**Đáp án chuẩn:** Phải học ít nhất một học kỳ mới được nghỉ; thời gian nghỉ tối đa là 04 học kỳ chính và được tính vào thời gian học chậm tiến độ; nghỉ quá 04 học kỳ chính sẽ bị xét buộc thôi học.

**Bot trả lời** (gemini-3.5-flash-lite):

> Thời gian nghỉ học tạm thời tối đa cho các trường hợp vì lý do cá nhân (khác với lý do ốm đau, thai sản, tai nạn hay điều động vào lực lượng vũ trang) được quy định tùy theo hệ đào tạo như sau:
> - Đối với sinh viên đại học: Thời gian nghỉ học tối đa cho phép là 04 học kỳ chính [1].
> - Đối với học viên kỹ sư: Thời gian nghỉ học tối đa cho phép là 02 học kỳ chính [2].
> - Đối với học viên thạc sĩ: Thời gian nghỉ học tối đa là 12 tháng [3].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 16. Nghỉ học tạm thời và tự nguyện thôi học, trang 16-17
- [2] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 25. Nghỉ học tạm thời, tự nguyện thôi học và buộc thôi học, trang 21-22
- [3] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 35. Nghỉ học tạm thời và bảo lưu kết quả học tập, trang 26

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Bot đưa ra thông tin phân tách rõ ràng cho từng hệ đào tạo (đại học: 4 học kỳ chính) theo Điều 16.

## q09 (single)

**Câu hỏi:** Trong một học kỳ không đạt bao nhiêu tín chỉ thì sinh viên bị nâng mức cảnh báo học tập?

**Đáp án chuẩn:** Số TC không đạt trong học kỳ lớn hơn 8: nâng một mức; lớn hơn 16 (hoặc tự ý bỏ học, không đăng ký học tập): nâng hai mức. Ngoài ra, số TC nợ đọng từ đầu khóa lớn hơn 24 thì bị cảnh báo mức 3.

**Bot trả lời** (gemini-3.5-flash-lite):

> Sinh viên bị nâng mức cảnh báo học tập trong học kỳ khi thuộc các trường hợp sau:
> - Nâng một mức cảnh báo học tập đối với sinh viên có số tín chỉ không đạt trong học kỳ lớn hơn 8 [1].
> - Nâng hai mức cảnh báo học tập đối với sinh viên có số tín chỉ không đạt trong học kỳ lớn hơn 16 [1].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 19. Cảnh báo học tập và buộc thôi học, trang 18-19

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Chính xác các mốc số tín chỉ không đạt trong học kỳ (>8 TC và >16 TC) để nâng mức cảnh báo.

## q10 (single)

**Câu hỏi:** Học phần tiên quyết và học phần học trước khác nhau như thế nào?

**Đáp án chuẩn:** Tiên quyết: phải hoàn thành học phần A với điểm đạt mới được học học phần B. Học trước: chỉ cần đã đăng ký và học xong học phần A (có thể chưa đạt) là được học học phần B.

**Bot trả lời** (gemini-3.5-flash-lite):

> Sự khác nhau giữa học phần tiên quyết và học phần học trước được quy định như sau:
> 
> - **Học phần tiên quyết:** Học phần A là học phần tiên quyết của học phần B thì sinh viên phải hoàn thành học phần A (với mức điểm đạt) mới được dự lớp học phần B [1].
> - **Học phần học trước:** Học phần A là học phần học trước của học phần B thì sinh viên phải đăng ký và học xong (có thể chưa đạt) học phần A mới được dự lớp học phần B [1].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 4. Tín chỉ và học phần, trang 7-8

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Phân biệt cực kỳ chính xác giữa học phần tiên quyết (phải đạt) và học phần học trước (chỉ cần đăng ký, học xong).

## q11 (single)

**Câu hỏi:** Dùng chứng chỉ IELTS để xét chuẩn ngoại ngữ đầu ra thì chứng chỉ cần đáp ứng điều kiện gì?

**Đáp án chuẩn:** Chứng chỉ phải đánh giá đủ 4 kỹ năng nghe, nói, đọc, viết; được cấp trong vòng 2 năm tính đến thời điểm xét chuẩn ngoại ngữ đầu ra và còn hiệu lực tại thời điểm xét.

**Bot trả lời** (gemini-3.5-flash-lite):

> Không tìm thấy trong quy chế.

**Nguồn bot trích:**
- (không có)

Tự động: cited-evidence = KHÔNG; bot từ chối = có

⚠️ từ chối 2/3 lần (phiếu chỉ hiện lần 1)

[ ] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [x] Từ chối sai

Ghi chú: Từ chối sai. Câu hỏi hỏi điều kiện của chứng chỉ IELTS để xét chuẩn đầu ra (có trong Quy định ngoại ngữ K71, Điều 5), nhưng bot lại từ chối "Không tìm thấy trong quy chế".

## q12 (single)

**Câu hỏi:** Hạn chót nộp đơn xét miễn các học phần ngoại ngữ cơ bản là khi nào?

**Đáp án chuẩn:** Muộn nhất 2 tuần trước khi bắt đầu học kỳ theo Khung kế hoạch năm học.

**Bot trả lời** (gemini-3.5-flash-lite):

> Thời gian tiếp nhận đơn đề nghị xét miễn học phần ngoại ngữ cơ bản muộn nhất là 2 tuần trước khi bắt đầu học kỳ theo Khung kế hoạch năm học [1].

**Nguồn bot trích:**
- [1] Quy định ngoại ngữ K71 10828/QĐ-ĐHBK, Điều 3. Công nhận, xét miễn học phần ngoại ngữ cơ bản, trang 4

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Đúng mốc thời gian muộn nhất 2 tuần trước học kỳ theo Điều 3 Quy định ngoại ngữ.

## q13 (single)

**Câu hỏi:** Sinh viên chương trình ELITECH tăng cường ngoại ngữ (ngoại ngữ chính là tiếng Anh) cần chứng chỉ tiếng Anh bậc mấy để đạt chuẩn đầu ra khi xét tốt nghiệp?

**Đáp án chuẩn:** Chứng chỉ tiếng Anh quy đổi tương đương từ Bậc 4 trở lên theo Bảng 2.1, Phụ lục II (không áp dụng với CTĐT hợp tác với Đại học TROY).

**Bot trả lời** (gemini-3.5-flash-lite):

> Sinh viên chương trình ELITECH tăng cường ngoại ngữ (ngoại ngữ chính là tiếng Anh) cần có chứng chỉ tiếng Anh được quy đổi tương đương từ Bậc 4 trở lên theo Bảng 2.1, Phụ lục II để đạt chuẩn đầu ra khi xét tốt nghiệp [5].

**Nguồn bot trích:**
- [5] Quy định ngoại ngữ K71 10828/QĐ-ĐHBK, Phụ lục IV. DANH MỤC CÁC HỌC PHẦN NGOẠI NGỮ CƠ BẢN - ĐIỀU KIỆN MIỄN HỌC - CHUẨN NGOẠI NGỮ ĐẦU RA > Bảng 4.2 Yêu cầu trình độ tiếng Anh theo học kỳ và chuẩn ngoại ngữ đầu ra khi xé, trang 13

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Chuẩn đầu ra ngoại ngữ cho ELITECH tăng cường tiếng Anh là Bậc 4 trở lên theo phụ lục quy định ngoại ngữ.

## q14 (single)

**Câu hỏi:** Điểm bài thi HUST English Placement Test có được dùng để xét đạt chuẩn ngoại ngữ đầu ra không?

**Đáp án chuẩn:** Không. Kết quả HUST English Placement Test chỉ dùng để phân loại trình độ đầu vào, xếp lớp và xét miễn các học phần ngoại ngữ cơ bản.

**Bot trả lời** (gemini-3.5-flash-lite):

> Không, kết quả bài thi HUST English Placement Test không được sử dụng để xét đạt chuẩn ngoại ngữ đầu ra [1][2].

**Nguồn bot trích:**
- [1] Quy định ngoại ngữ K71 10828/QĐ-ĐHBK, Phụ lục III. DANH MỤC CÁC HỌC PHẦN NGOẠI NGỮ CƠ BẢN - ĐIỀU KIỆN MIỄN HỌC - CHUẨN NGOẠI NGỮ ĐẦU RA > Bảng 3.1 Danh mục các học phần tiếng Anh thuộc khối ngoại ngữ cơ bản và điều kiệ, trang 10
- [2] Quy định ngoại ngữ K71 10828/QĐ-ĐHBK, Phụ lục IV. DANH MỤC CÁC HỌC PHẦN NGOẠI NGỮ CƠ BẢN - ĐIỀU KIỆN MIỄN HỌC - CHUẨN NGOẠI NGỮ ĐẦU RA > Bảng 4.1 Danh mục các học phần tiếng Anh thuộc khối ngoại ngữ cơ bản và điều kiệ, trang 12

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Xác định đúng bản chất bài thi HUST English Placement Test chỉ dùng phân loại đầu vào/miễn học phần cơ bản, không dùng xét chuẩn đầu ra.

## q15 (single)

**Câu hỏi:** Học phí học kỳ hè năm học 2026–2027 được tính như thế nào?

**Đáp án chuẩn:** Bằng 1,5 lần mức học phí quy định tại mục 1, 2, 3 của Phụ lục I (mức học kỳ chính), trừ một số học phần và CTĐT kỹ sư chuyên sâu được tính bằng mức thường; việc này do Giám đốc đại học quyết định.

**Bot trả lời** (gemini-3.5-flash-lite):

> Mức học phí học kỳ hè được tính bằng 1,5 lần mức học phí quy định tại mục 1, 2, 3 của Phụ lục I, ngoại trừ một số học phần và chương trình đào tạo kỹ sư chuyên sâu được tính bằng mức học phí tại mục 1, 2, 3 của Phụ lục I do Giám đốc đại học quyết định [3].

**Nguồn bot trích:**
- [3] Quy định học phí năm học 2026-2027 12006/QĐ-ĐHBK, Phụ lục I. MỨC HỌC PHÍ CÁC CHƯƠNG TRÌNH ĐÀO TẠO ĐẠI HỌC CHÍNH QUY, KỸ SƯ > I. Các chương trình đào tạo đại học chính quy > 5) Các mức học phí khác, trang 5

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Chính xác hệ số 1,5 cho học phí học kỳ hè theo Phụ lục I của văn bản học phí.

## q16 (numeric)

**Câu hỏi:** Điểm học phần 8,0 thì quy đổi ra điểm chữ gì và được bao nhiêu điểm thang 4?

**Đáp án chuẩn:** Điểm 8,0 thuộc khoảng 8,0–8,4, quy đổi thành điểm chữ B+, tương ứng 3,5 điểm thang 4.

**Bot trả lời** (gemini-3.5-flash-lite):

> Điểm học phần 8,0 tương ứng với điểm chữ B+ và điểm số quy đổi theo thang 4 là 3,5 [1].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 5. Điểm học phần, trang 9-10

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Quy đổi chính xác 8,0 sang B+ và 3,5 điểm thang 4 theo Điều 5.

## q17 (numeric)

**Câu hỏi:** CPA bao nhiêu thì được xếp loại học lực Giỏi?

**Đáp án chuẩn:** CPA từ 3,2 đến 3,59 (thang 4).

**Bot trả lời** (gemini-3.5-flash-lite):

> Sinh viên được xếp loại học lực Giỏi khi điểm trung bình tích lũy (CPA) nằm trong khoảng từ 3,2 đến 3,59 [2].

**Nguồn bot trích:**
- [2] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 12. Ý kiến phản hồi của người học, đánh giá kết quả học tập, trang 13-14

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Khoảng điểm CPA học lực Giỏi (3,2 - 3,59) được trích đúng từ Điều 12.

## q18 (numeric)

**Câu hỏi:** Một học kỳ chính sinh viên được đăng ký tối đa và tối thiểu bao nhiêu tín chỉ? Học kỳ hè thì được đăng ký tối đa bao nhiêu?

**Đáp án chuẩn:** Sinh viên không bị cảnh báo học tập được đăng ký tối đa 24 TC và tối thiểu 12 TC mỗi học kỳ chính (không áp dụng ngưỡng tối thiểu với sinh viên trình độ năm cuối); học kỳ hè tối đa 8 TC.

**Bot trả lời** (gemini-3.5-flash-lite):

> Đối với sinh viên không thuộc diện cảnh báo học tập, số lượng tín chỉ được đăng ký tối đa là 24 TC và tối thiểu là 12 TC trong học kỳ chính, không áp dụng ngưỡng tín chỉ đăng ký tối thiểu với sinh viên trình độ năm cuối [1]. Trong học kỳ hè, sinh viên được đăng ký tối đa 8 TC [1].
> 
> Đối với sinh viên đang bị cảnh báo học tập từ mức 2 trở lên, khối lượng học tập bị hạn chế tại học kỳ 1 của năm học như sau [4]:
> - Sinh viên thuộc các chương trình đào tạo chuẩn được đăng ký tối đa 14 TC và tối thiểu 8 TC cho một học kỳ chính [4].
> - Sinh viên thuộc các chương trình ELITECH và các chương trình đào tạo hợp tác quốc tế được đăng ký tối đa 18 TC và tối thiểu 8 TC cho một học kỳ chính [4].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 10. Đăng ký học tập chương trình đại học, trang 12-13
- [4] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 19. Cảnh báo học tập và buộc thôi học, trang 18-19

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Nêu đầy đủ các hạn mức tối đa/tối thiểu cho học kỳ chính và học kỳ hè.

## q19 (numeric)

**Câu hỏi:** Năm học 2026–2027, học phí mỗi tín chỉ học phí của ngành Khoa học máy tính (chương trình chuẩn) là bao nhiêu?

**Đáp án chuẩn:** 700 nghìn đồng/tín chỉ học phí (mức cho 2 học kỳ chính).

**Bot trả lời** (gemini-3.5-flash-lite):

> Năm học 2026-2027, mức học phí của ngành Khoa học máy tính (chương trình đào tạo chuẩn đại học chính quy) là 700 nghìn đồng cho một tín chỉ học phí [1].

**Nguồn bot trích:**
- [1] Quy định học phí năm học 2026-2027 12006/QĐ-ĐHBK, Phụ lục I. MỨC HỌC PHÍ CÁC CHƯƠNG TRÌNH ĐÀO TẠO ĐẠI HỌC CHÍNH QUY, KỸ SƯ > I. Các chương trình đào tạo đại học chính quy > 1) Các chương trình đào tạo chuẩn, trang 3

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Đúng mức học phí 700k/TC cho ngành Khoa học máy tính hệ chuẩn năm học 2026-2027.

## q20 (numeric)

**Câu hỏi:** Một tín chỉ học tập của đồ án tốt nghiệp được quy đổi thành bao nhiêu tín chỉ học phí?

**Đáp án chuẩn:** Với hệ đại học chính quy, khóa luận/đồ án tốt nghiệp: 1 TCHT = 2,5 TCHP.

**Bot trả lời** (gemini-3.5-flash-lite):

> Tùy thuộc vào hệ đào tạo, một tín chỉ học tập của đồ án tốt nghiệp được quy đổi thành tín chỉ học phí như sau:
> - Hệ đại học chính quy: 1 tín chỉ học tập = 2,5 tín chỉ học phí [1].
> - Hệ đào tạo thường xuyên: 1 tín chỉ học tập = 2,5 tín chỉ học phí [2].

**Nguồn bot trích:**
- [1] Quy định học phí năm học 2026-2027 12006/QĐ-ĐHBK, Phụ lục II. QUY ĐỔI TÍN CHỈ HỌC TẬP (TCHT) SANG TÍN CHỈ HỌC PHÍ (TCHP) > I. Hệ đại học chính quy, trang 7
- [2] Quy định học phí năm học 2026-2027 12006/QĐ-ĐHBK, Phụ lục II. QUY ĐỔI TÍN CHỈ HỌC TẬP (TCHT) SANG TÍN CHỈ HỌC PHÍ (TCHP) > II. Hệ đào tạo thường xuyên, trang 7

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Quy đổi tín chỉ học tập đồ án sang tín chỉ học phí là 2,5 lần (hệ đại học chính quy) theo Phụ lục II.

## q21 (multi)

**Câu hỏi:** Sinh viên chương trình chuẩn khóa 71 cần những điều kiện gì để được xét công nhận tốt nghiệp? Chuẩn ngoại ngữ đầu ra cụ thể là bậc mấy?

**Đáp án chuẩn:** Theo QCĐT Điều 14 khoản 3: hoàn thành đủ các học phần theo yêu cầu CTĐT trong thời gian quy định (kể cả GDTC, GDQP-AN); đạt chuẩn ngoại ngữ đầu ra; CPA toàn khóa (theo các học phần đăng ký tốt nghiệp) từ 2,0 trở lên; không bị truy cứu trách nhiệm hình sự hoặc đang bị kỷ luật đình chỉ học tập. Chuẩn ngoại ngữ đầu ra với CTĐT chuẩn (trừ nhóm ngành ngôn ngữ) theo Quy định ngoại ngữ K71: chứng chỉ tiếng Anh quy đổi tương đương từ Bậc 3 trở lên.

**Bot trả lời** (gemini-3.5-flash-lite):

> Đối với chuẩn đầu ra khi xét tốt nghiệp với chương trình đào tạo chuẩn (trừ các chương trình đào tạo nhóm ngành ngôn ngữ), sinh viên cần có chứng chỉ tiếng Anh được quy đổi tương đương từ Bậc 3 trở lên theo Bảng 2.1, Phụ lục II [1]. Chứng chỉ tiếng Anh này phải đánh giá đầy đủ 4 kỹ năng nghe, nói, đọc, viết, được cấp trong vòng 2 năm tính đến thời điểm xét chuẩn ngoại ngữ đầu ra và còn hiệu lực tại thời điểm xét [5].

**Nguồn bot trích:**
- [1] Quy định ngoại ngữ K71 10828/QĐ-ĐHBK, Phụ lục III. DANH MỤC CÁC HỌC PHẦN NGOẠI NGỮ CƠ BẢN - ĐIỀU KIỆN MIỄN HỌC - CHUẨN NGOẠI NGỮ ĐẦU RA > Bảng 3.2 Yêu cầu trình độ tiếng Anh theo học kỳ và chuẩn ngoại ngữ đầu ra khi xé, trang 11
- [5] Quy định ngoại ngữ K71 10828/QĐ-ĐHBK, Điều 5. Yêu cầu về chuẩn ngoại ngữ đầu ra, trang 4

Tự động: cited-evidence = có; bot từ chối = không

[ ] Đúng  [x] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Bot tập trung trả lời đúng phần chuẩn ngoại ngữ (Bậc 3) và các điều kiện đi kèm của chứng chỉ theo phụ lục/điều khoản quy định ngoại ngữ. (Sửa khi rà soát lại 16/11: bot chỉ trả lời ý chuẩn ngoại ngữ, thiếu các điều kiện tốt nghiệp)

## q22 (multi)

**Câu hỏi:** CPA toàn khóa của em là 3,7 nhưng số tín chỉ phải học lại vượt quá 5% thì em tốt nghiệp hạng gì?

**Đáp án chuẩn:** Hạng Giỏi. CPA 3,7 thuộc loại Xuất sắc (3,6–4,0), nhưng khối lượng học lại vượt quá 5% tổng số TC dùng tính điểm trung bình toàn khóa nên hạng tốt nghiệp bị giảm một mức (không tính các học phần học cải thiện điểm).

**Bot trả lời** (gemini-3.5-flash-lite):

> Hạng tốt nghiệp của sinh viên có điểm trung bình toàn khóa (CPA) xếp loại giỏi trở lên (từ 3,2 trở lên) sẽ bị giảm một mức nếu khối lượng các học phần phải học lại vượt quá 5% tổng số tín chỉ của các học phần dùng tính điểm trung bình toàn khóa [1][2][4]. Với CPA toàn khóa là 3,7 (thuộc loại xuất sắc) và bị dính trường hợp vượt quá 5% tín chỉ học lại, hạng tốt nghiệp của bạn sẽ bị giảm từ xuất sắc xuống một mức là loại giỏi [1][2][4].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 15. Điểm trung bình toàn khóa và hạng tốt nghiệp đại học, trang 16
- [2] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 24. Điểm trung bình toàn khóa và hạng tốt nghiệp kỹ sư, trang 21
- [4] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 12. Ý kiến phản hồi của người học, đánh giá kết quả học tập, trang 13-14

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Phân tích logic chuẩn xác: CPA 3,7 (Xuất sắc) nhưng dính lỗi vượt 5% tín chỉ học lại nên bị hạ một bậc xuống Giỏi.

## q23 (multi)

**Câu hỏi:** Trường hợp nào thì sinh viên đại học bị buộc thôi học?

**Đáp án chuẩn:** (1) Bị cảnh báo học tập mức 3 lần thứ hai liên tiếp; (2) học chậm tiến độ quá thời gian cho phép hoặc không còn đủ khả năng tốt nghiệp trong thời gian cho phép – với chương trình cử nhân, thời gian chậm tiến độ không được vượt quá 5 học kỳ chính so với kế hoạch học tập chuẩn.

**Bot trả lời** (gemini-3.5-flash-lite):

> Sinh viên đại học bị buộc thôi học trong các trường hợp sau:
> 1. Sinh viên bị cảnh báo học tập mức 3 lần thứ hai liên tiếp [2].
> 2. Sinh viên học chậm tiến độ quá thời gian cho phép, hoặc không còn đủ khả năng tốt nghiệp trong thời gian cho phép theo quy định tại khoản 3 Điều 3 của Quy chế [2].

**Nguồn bot trích:**
- [2] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 19. Cảnh báo học tập và buộc thôi học, trang 18-19

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Liệt kê chuẩn xác các nguyên nhân chính dẫn đến việc bị buộc thôi học theo Điều 19.

## q24 (multi)

**Câu hỏi:** Nhóm em có 12 sinh viên muốn đề nghị mở một lớp học lại ngoài kế hoạch. Lớp có được mở không và học phí tính thế nào?

**Đáp án chuẩn:** Bình thường lớp có giờ lên lớp cần tối thiểu 20 sinh viên, nhưng lớp có từ 5 đến 19 sinh viên đăng ký theo đề nghị của sinh viên có thể được xem xét mở và áp dụng hệ số học phí. Theo quy định học phí 2026–2027, lớp học lại ngoài kế hoạch từ 10 đến dưới 20 sinh viên tính hệ số 1,5 (dưới 10 sinh viên: hệ số 2,0); việc giữ/hủy lớp do đơn vị chuyên môn quyết định.

**Bot trả lời** (gemini-3.5-flash-lite):

> - Việc quyết định giữ hoặc hủy các lớp học lại ngoài kế hoạch do các đơn vị chuyên môn phụ trách quyết định [1].
> - Mức học phí đối với lớp từ 10 đến dưới 20 sinh viên được tính với hệ số 1,5 [1].

**Nguồn bot trích:**
- [1] Quy định học phí năm học 2026-2027 12006/QĐ-ĐHBK, Phụ lục I. MỨC HỌC PHÍ CÁC CHƯƠNG TRÌNH ĐÀO TẠO ĐẠI HỌC CHÍNH QUY, KỸ SƯ > I. Các chương trình đào tạo đại học chính quy > 5) Các mức học phí khác, trang 5

Tự động: cited-evidence = có; bot từ chối = không

[ ] Đúng  [x] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Trả lời đúng mức hệ số học phí (1,5) áp dụng cho lớp học lại ngoài kế hoạch quy mô từ 10 đến dưới 20 sinh viên. (Sửa khi rà soát lại 16/11: bot không trả lời thẳng 'lớp 5–19 SV có thể được xem xét mở')

## q25 (colloquial)

**Câu hỏi:** trượt cuối kỳ thì có đc thi lại ko ạ

**Đáp án chuẩn:** Không. Mỗi học phần chỉ được thi cuối kỳ một lần (kể cả khi điểm quá trình bị liệt) và không có lần thi lại.

**Bot trả lời** (gemini-3.5-flash-lite):

> Người học được thi cuối kỳ một lần đối với mỗi học phần đã đăng ký học trong học kỳ (kể cả trường hợp có điểm quá trình là điểm liệt) và không có lần thi lại [1].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 6. Hoãn thi, miễn thi, phúc tra và khiếu nại điểm, trang 10

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Khẳng định chính xác theo quy chế: Thi cuối kỳ chỉ có 1 lần duy nhất, không có thi lại.

## q26 (colloquial)

**Câu hỏi:** hp nganh toan tin 1 tin chi bao nhieu tien vay

**Đáp án chuẩn:** 680 nghìn đồng/tín chỉ học phí (chương trình chuẩn Toán tin, năm học 2026–2027, mức cho học kỳ chính).

**Bot trả lời** (gemini-3.5-flash-lite):

> Mức học phí cho chương trình đào tạo chuẩn ngành Toán tin là 680 nghìn đồng cho một tín chỉ học phí [2].

**Nguồn bot trích:**
- [2] Quy định học phí năm học 2026-2027 12006/QĐ-ĐHBK, Phụ lục I. MỨC HỌC PHÍ CÁC CHƯƠNG TRÌNH ĐÀO TẠO ĐẠI HỌC CHÍNH QUY, KỸ SƯ > I. Các chương trình đào tạo đại học chính quy > 1) Các chương trình đào tạo chuẩn, trang 3

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Lấy đúng mức học phí 680k/TC cho ngành Toán tin (chương trình chuẩn) trong bảng phụ lục học phí.

## q27 (colloquial)

**Câu hỏi:** nghỉ học 5 buổi thì bị trừ mấy điểm quá trình vậy mn

**Đáp án chuẩn:** Nếu kết quả điểm danh được dùng để cộng/trừ: vắng từ 5 buổi trở lên bị trừ 2 điểm quá trình (vắng 3–4 buổi: −1; 1–2 buổi: 0; không vắng: +1).

**Bot trả lời** (gemini-3.5-flash-lite):

> Đối với các giờ lên lớp, nếu số lần vắng mặt từ 5 lần trở lên thì điểm quá trình bị trừ 2 điểm [1].

**Nguồn bot trích:**
- [1] Quy chế đào tạo 5445/QĐ-ĐHBK, Điều 5. Điểm học phần, trang 9-10

Tự động: cited-evidence = có; bot từ chối = không

[x] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [ ] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Chính xác quy định trừ 2 điểm quá trình khi vắng mặt từ 5 buổi trở lên theo Điều 5.

## q28 (no_answer)

**Câu hỏi:** Điểm rèn luyện bao nhiêu thì được xét học bổng khuyến khích học tập?

**Đáp án chuẩn:** Không tìm thấy trong quy chế

**Bot trả lời** (gemini-3.5-flash-lite):

> Không tìm thấy trong quy chế.

**Nguồn bot trích:**
- (không có)

Tự động: cited-evidence = không áp dụng; bot từ chối = có

[ ] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [x] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Câu hỏi dạng no_answer và bot đã từ chối đúng ("Không tìm thấy trong quy chế"). (ban đầu tick nhầm ô Đúng; ghi chú xác nhận từ chối đúng)

## q29 (no_answer)

**Câu hỏi:** Gian lận trong thi cử (thi hộ, mang tài liệu vào phòng thi) thì bị kỷ luật ở mức nào?

**Đáp án chuẩn:** Không tìm thấy trong quy chế

**Bot trả lời** (gemini-3.5-flash-lite):

> Không tìm thấy trong quy chế.

**Nguồn bot trích:**
- (không có)

Tự động: cited-evidence = không áp dụng; bot từ chối = có

[ ] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [x] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Từ chối đúng vì nội dung kỷ luật thi cử nằm ở văn bản xử lý vi phạm học vụ riêng chứ không có trong Quy chế đào tạo chính. (ban đầu tick nhầm ô Đúng; ghi chú xác nhận từ chối đúng)

## q30 (no_answer)

**Câu hỏi:** Sinh viên năm nhất muốn ở ký túc xá thì đăng ký thế nào và ai được ưu tiên?

**Đáp án chuẩn:** Không tìm thấy trong quy chế

**Bot trả lời** (gemini-3.5-flash-lite):

> Không tìm thấy trong quy chế.

**Nguồn bot trích:**
- (không có)

Tự động: cited-evidence = không áp dụng; bot từ chối = có

[ ] Đúng  [ ] Đúng một phần  [ ] Sai  [ ] Bịa (nói điều không có trong văn bản)  [x] Từ chối đúng  [ ] Từ chối sai

Ghi chú: Từ chối đúng vì quy chế đào tạo không đề cập đến quy định ký túc xá. (ban đầu tick nhầm ô Đúng; ghi chú xác nhận từ chối đúng)


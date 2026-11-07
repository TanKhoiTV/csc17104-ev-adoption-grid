# ADR-001: Chốt chủ đề nghiên cứu

## Status

Proposed

## Date

2026-11-07

## Context

- Đồ án cuối kỳ CSC17104, nhóm **2 người**, nên đề bài yêu cầu **2 × n = 4 câu hỏi**, trong đó ít nhất một câu hỏi phải trả lời bằng mô hình học máy.
- Đề bài cũng đặt ngưỡng độ sâu: mỗi câu hỏi **phi-ML** phải dùng rõ ràng **≥ 2 trong 6 tiêu chí** (D1 ghép dữ liệu, D2 tái cấu trúc & thời gian, D3 biến dẫn xuất, D4 kiểm soát biến gây nhiễu, D5 định lượng bất định, D6 kiểm tra độ vững), và cả bộ câu hỏi phải phủ **≥ 4/6**.
- Các quyết định nền đã có: dữ liệu ở **ADR-002**, mẫu 8 quốc gia và vai trò từng nước ở **ADR-004**, nhận dạng cho Q3 ở **ADR-006**, câu hỏi thứ tư ở **ADR-008**.
- Giới hạn dữ liệu đã kiểm chứng ngày 2026-11-07 trên `data/EV Data Explorer 2025.xlsx` (SHA-256 khớp ADR-002 D.2):
    - Chỉ **5 tham số** dùng được ở cấp quốc gia: `EV sales share`, `EV stock share`, `EV charging points`, `EV sales`, `EV stock` — tất cả đều đã nằm trong ADR-002/ADR-004.
    - `Battery demand` và `Oil displacement` chỉ có **6 thực thể tổng hợp** (China, Europe, India, Rest of the world, USA, World), không có Nhật/Đức/Thái Lan/New Zealand/Việt Nam.
    - `Electricity demand` **chỉ tồn tại ở `category = Projection-STEPS`**, không có quan sát lịch sử nào ⇒ không dùng được cho phân tích thực nghiệm.
- Hệ quả quan trọng: **chiều sâu của dự án phải đến từ việc ghép nguồn và biến dẫn xuất, không phải từ độ rộng của dữ liệu.** Đó cũng chính là hai tiêu chí D1 và D3 mà đề bài thưởng điểm.

## Decision

### Chủ đề

**Quá trình chuyển đổi sang xe điện ở 8 quốc gia, đặt trong tương quan với cấu trúc phát thải của chính quốc gia đó, với Việt Nam là trường hợp chính sách.**

### Bốn câu hỏi, đánh số theo thứ tự tự sự

Số thứ tự câu hỏi **trùng với thứ tự trình bày**, không trùng với thứ tự ghép nối kỹ thuật. Lý do: phần thuyết trình 15 phút và phần đọc notebook phải kể cùng một mạch; nếu đánh số theo thứ tự kỹ thuật thì người đọc phải tự sắp lại.

| # | Câu hỏi | Chủ sở hữu | Loại |
| --- | --- | --- | --- |
| **Q1** | Trọng số của ngành giao thông trong CO₂ quốc gia có dự báo được tốc độ điện khí hoá không, sau khi kiểm soát thu nhập? | Dat | Phân tích |
| **Q2** | Có thể dự báo tỉ lệ áp dụng của năm sau giữa các quốc gia không, và mô hình hỏng ở đâu? | Khoi | **ML** |
| **Q3** | Mật độ trạm sạc có làm tăng tỉ lệ áp dụng không, và panel 6 cluster thực sự nói được gì? | Dat | Phân tích |
| **Q4** | Chuyển đổi xe điện ở Việt Nam có phải là câu chuyện xe hai bánh, và quy ra CO₂ là bao nhiêu? | Khoi | Phân tích |

**Q3b** (event study thuế tín dụng xe điện Mỹ, 30/9/2025) tách khỏi Q3 và **hoãn sang future work** — xem ADR-006 D.7 và mục Consequences dưới đây.

### Vì sao bốn câu hỏi này

- **Q1 trả lời đúng câu hỏi mà ADR-001 đặt ra.** Một bảng tỉ trọng sector, tự nó, không trả lời được "giao thông có phải là đòn bẩy đúng không". Q1 biến bảng đó thành một kiểm định.
- **Q2 là câu hỏi ML duy nhất** mà đề bài bắt buộc, và khung thời gian kiểm định 2021–2024 chứa các cú đảo chiều do chính sách (Đức, New Zealand, Trung Quốc) — tức bài toán dự báo có một kiểu thất bại trung thực để phân tích.
- **Q3 giữ nguyên thiết kế đã chốt trước ở ADR-006**, kể cả nhánh "không xác định" là kết quả hợp lệ.
- **Q4 giữ trường hợp chính sách** mà dự án được tổ chức quanh nó, và dùng chuỗi dữ liệu dày nhất của Việt Nam.

### Phạm vi: "lưới điện" không phải một câu hỏi độc lập

Tên dự án có nhắc tới lưới điện, nhưng **không câu hỏi nào ước lượng cường độ carbon của lưới như một đối tượng nghiên cứu**. Lưới chỉ đi vào qua hai đường: biến kiểm soát ở Q1, và dải giả định cường độ lưới ở Q4. Ghi rõ như vậy để không ai đi tìm một kết quả về lưới trong báo cáo.

## Alternatives Considered

- **A.1. Chủ đề một quốc gia (chỉ Việt Nam).** Loại: mất khả năng so sánh, trong khi Q1–Q3 cần 6–7 quan sát chéo; và mẫu 8 quốc gia đã được chốt trước ở ADR-004 để tránh chọn mẫu theo kết quả.
- **A.2. Chủ đề một ngành (chỉ giao thông).** Loại: mất phần đối chiếu với Industry/Power, tức mất chính cái làm nên vai trò "irony" của Trung Quốc và "trường hợp tốt nhất" của New Zealand ở ADR-004.
- **A.3. Chủ đề thuần công nghệ (chỉ diffusion, không có phát thải).** Loại: bỏ mất câu hỏi chính sách, và dễ rơi vào loại câu hỏi mô tả mà đề bài coi là không đủ độ sâu.
- **A.4. Giữ cấu trúc sector như một câu hỏi mô tả độc lập (M3 cũ).** Loại: đề bài nêu rõ "một groupby, value_counts hoặc describe cộng một biểu đồ" là **không đủ độ sâu**; một bảng tỉ trọng + hai biểu đồ rơi đúng vào mô tả đó.
- **A.5. Thêm câu hỏi thứ năm về lưới điện.** Loại: đề bài yêu cầu 2 × n = 4; thêm câu hỏi làm loãng thời gian còn lại (hạn 29/11) và không câu nào được làm kỹ.
- **A.6. Dùng `Electricity demand` / `Battery demand` để dựng câu hỏi lưới điện.** Loại: `Electricity demand` chỉ có ở Projection-STEPS, `Battery demand` chỉ có 6 thực thể tổng hợp — đã kiểm chứng, xem Context.

## Consequences

- **C.1. Cỡ mẫu thay đổi theo từng câu.** Q1 = 7 (mô tả cấu trúc cho cả 8), Q2 = 6, Q3 = 6, Q4 = 1. `SPECIFICATION.md` phải ghi rõ, và mỗi notebook phải in cỡ mẫu của mình.
- **C.2. Việt Nam chỉ tham gia Q1 và Q4.** Việt Nam không vào được Q2 (không có dòng huấn luyện sau lag, xem ADR-008 D.5) và không vào được Q3 (chỉ 2 năm dữ liệu sạc, ADR-006 D.6). Đây là hệ quả của dữ liệu, không phải loại trừ tuỳ ý — phải nêu trước, không để người đọc tự phát hiện.
- **C.3. "Lưới điện" trong tên dự án không phải một kết quả độc lập**, chỉ là biến kiểm soát ở Q1 và dải giả định ở Q4.
- **C.4. Đánh số câu hỏi tách khỏi đánh số notebook.** Đề bài cố định tên file `01_collection_exploration`, `02_analysis`, `03_ml_question`, nên **Q2 nằm ở `03_ml_question.ipynb`**. Đây là quy ước đặt tên, không phải lỗi thứ tự; README phải nói rõ một dòng.
- **C.5. Q3b hoãn.** Thiết kế vẫn nằm trong ADR-006 D.7 như một phần future work, kèm lý do hoãn (phụ thuộc PDF phải số hoá tay, và không nằm trong 4 câu hỏi đăng ký).
- **C.6. Bốn câu hỏi phủ đủ 6/6 tiêu chí độ sâu**, và mỗi tiêu chí xuất hiện ở **ít nhất hai** câu hỏi. Ràng buộc này phải được kiểm lại nếu sau này có câu hỏi bị cắt.

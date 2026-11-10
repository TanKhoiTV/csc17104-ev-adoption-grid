# SPECIFICATION.md — Đăng ký trước thiết kế nghiên cứu

## Status

Proposed — **đóng băng trước khi chạy bất kỳ phân tích nào**

## Date

2026-11-07

## Phạm vi và thẩm quyền

Tài liệu này chốt **câu hỏi, mẫu, biến, đặc tả mô hình, quy tắc phán quyết và kiểm tra độ vững** cho bốn câu
hỏi của dự án, trước khi có bất kỳ kết quả nào. Mục đích là chặn việc chọn mẫu và chọn mô hình theo kết quả.

Thứ tự thẩm quyền khi có xung đột: **ADR > SPECIFICATION.md > notebook**. Các ADR đã chốt những điểm sau và
tài liệu này **kế thừa, không viết lại**:

| Nội dung | Nguồn |
| --- | --- |
| Chủ đề, bốn câu hỏi, thứ tự tự sự | ADR-001 |
| Hai bộ dữ liệu, hash, giấy phép, ánh xạ tên quốc gia | ADR-002 |
| Mẫu 8 quốc gia và vai trò từng nước | ADR-004 |
| Nhận dạng của Q3 và bảng phán quyết D.5 | ADR-006 D.1–D.5 |
| Q4: chuỗi chính, estimand dạng dải, quan hệ với Q2 | ADR-008 D.1–D.6 |

## 1. Câu hỏi và giả thuyết

Giả thuyết phải **có hướng** ở nơi có cơ sở lý thuyết, và phải **được phép sai**.

| # | Câu hỏi | Giả thuyết chốt trước | Loại |
| --- | --- | --- | --- |
| **Q1** | Trọng số ngành giao thông trong CO₂ quốc gia có dự báo được tốc độ điện khí hoá, sau khi kiểm soát thu nhập? | **H1 (có hướng):** trọng số giao thông cao hơn đi cùng tốc độ áp dụng nhanh hơn. Nếu trái dấu hoặc không phân biệt được với 0, báo cáo nguyên trạng. | Phân tích |
| **Q2** | Có thể dự báo tỉ lệ áp dụng của năm sau giữa các quốc gia không, và mô hình hỏng ở đâu? | **H2 (không hướng):** mô hình học được quy luật diffusion và **vượt baseline persistence ≥ 1,0 pp RMSE** trên tập test. Không vượt được là một kết quả hợp lệ. | **ML** |
| **Q3** | Mật độ trạm sạc công cộng có làm tăng tỉ lệ áp dụng không? | **H3 (có hướng):** hệ số của biến sạc trễ 1 năm dương và CI không chứa 0, **với điều kiện** kiểm tra lead/lag không phát hiện nhân quả ngược. | Phân tích |
| **Q4** | Chuyển đổi ở Việt Nam có phải là câu chuyện xe hai bánh, và phần CO₂ tránh được nằm trong khoảng nào? | **H4 (mô tả):** tỉ lệ áp dụng của xe hai bánh cao hơn xe hơi một bậc rõ rệt; phần CO₂ tránh được là một dải, không phải một điểm. | Phân tích |

## 2. Dữ liệu và mẫu

Dữ liệu: `data/EDGAR_2026_GHG_booklet_2026.xlsx` (SHA-256 `BB77A0DA…`) và
`data/EV Data Explorer 2025.xlsx` (SHA-256 `309C6342…`), cùng nguồn World Bank qua API. Không commit vào git;
phải tải lại và kiểm hash trước khi chạy (ADR-002 D.4).

| # | Đơn vị quan sát | Cỡ mẫu | Loại trừ, kèm lý do |
| --- | --- | --- | --- |
| **Q1** | quốc gia | **7** (mô tả cấu trúc cho 8) | Singapore: không có dòng nào trong file IEA ⇒ không có tốc độ áp dụng |
| **Q2** | quốc gia–năm, `cars` | **84** (train 60 / test 24) sau lag | Việt Nam: `cars` chỉ có 2018 trước 2021, mà lag cần 2017 ⇒ **0 dòng huấn luyện** (ADR-008 D.5); Singapore: như trên |
| **Q3** | quốc gia–năm | **70** ô, **64** sau lag 1 năm | Việt Nam: chỉ 2 năm dữ liệu sạc (ADR-006 D.6); Singapore: như trên |
| **Q4** | quốc gia–năm, Việt Nam | **11** (2014–2024), chuỗi `2 and 3 wheelers` | Không loại; `cars` chỉ dùng đối chiếu |

Cỡ mẫu thay đổi theo câu là **hệ quả của độ phủ dữ liệu**, không phải chọn mẫu theo kết quả. Mỗi notebook phải
in cỡ mẫu của mình ở mỗi bước lọc/gộp. Q3b (event study thuế tín dụng Mỹ) **không** nằm trong tài liệu này — hoãn
sang future work (ADR-001 C.5).

## 3. Biến

### Q1
- **Kết quả:** tốc độ áp dụng = `EV sales share` (`mode = Cars`, `powertrain = EV`, `category = Historical`) tại
  hai mốc **2018 và 2024**, tính bằng điểm phần trăm. Chọn `cars` cho cả 7 quốc gia để biến mục tiêu đồng nhất
  định nghĩa; Việt Nam dùng đúng hai mốc 2018 (0,0016%) và 2024 (17,0%).
- **Giải thích:** trọng số giao thông = `Transport / Σ 8 sector` từ EDGAR CO₂ năm 2025 (ADR-004). Mẫu số là
  tổng các dòng CO₂ **hiện có** cho quốc gia đó (bảng thưa: Singapore thiếu `Agriculture`, Đức và Mỹ thiếu `Waste`).
- **Kiểm soát:** log GDP bình quân đầu người (World Bank) và nhóm thu nhập.
- **Dẫn xuất:** CO₂ giao thông bình quân đầu người; tốc độ áp dụng theo năm.

### Q2
- **Mục tiêu:** `EV sales share` của năm **t+1**, `mode = Cars`.
- **Đặc trưng (chỉ dùng thông tin có tại thời điểm dự báo):** sales share trễ 1 và 2 năm; stock share trễ 1 năm;
  điểm sạc/1.000 dân trễ 1 năm; log GDP bình quân đầu người trễ 1 năm; định danh quốc gia; chỉ số năm.
- **Loại trừ để chống rò rỉ:** mọi biến cùng năm `t`; toàn bộ `category = Projection-STEPS` (IEA có dự báo tới
  2030 — đưa vào là rò rỉ đầu ra mô hình của IEA vào biến mục tiêu); mọi biến được tạo từ chính biến mục tiêu.

### Q3
- **Kết quả:** `EV sales share` (`cars`). **Giải thích:** điểm sạc công cộng trên 1.000 dân, **trễ 1 năm**
  (`mode = EV`, `powertrain ∈ {Publicly available fast, Publicly available slow}` — lưu ý dòng sạc dùng
  `mode = EV`, **khác** dòng sales/stock dùng `mode = Cars`).
- **Kiểm soát:** log GDP bình quân đầu người. **Chỉ như độ nhạy:** trọng số giao thông (nối với Q1).

### Q4
- Chuỗi chính: `2 and 3 wheelers` (sales share + stock share, 2014–2024); `cars` để đối chiếu.
- Bốn hệ số của công thức ở ADR-008 D.4, mỗi hệ số phải được ghi rõ là **dữ liệu** hay **giả định**.

## 4. Đặc tả mô hình

- **Q1 — phân tích chéo quốc gia.** Hệ số tương quan hạng **Spearman** giữa trọng số giao thông và tốc độ áp
  dụng, vì n = 7 và Spearman không bị chi phối bởi Trung Quốc (13.057 Mt). Khoảng tin cậy bằng **bootstrap
  10.000 lần**. Kiểm soát thu nhập bằng hồi quy OLS hai biến (thêm log GDP) và bằng cách chia nhóm thu nhập.
- **Q2 — pipeline scikit-learn.** `Pipeline` gồm mã hoá biến phân loại, chuẩn hoá và mô hình. So sánh **ba**
  phương án: baseline persistence (giá trị cuối cùng đã quan sát), Ridge, và HistGradientBoosting (hoặc
  RandomForest). Chia **theo thời gian**: train ≤ 2020, test 2021–2024; không trộn. Chọn siêu tham số bằng
  `TimeSeriesSplit` **chỉ trên tập train**. Đánh giá **một lần** trên test.
- **Q3 — panel FE.** `linearmodels.PanelOLS` với fixed effect **quốc gia** và **năm**; biến động nhận dạng là
  thay đổi trong nước sau khi trừ xu hướng chung. Kiểm tra lead/lag theo ADR-006 D.4. Sai lệch chuẩn bằng
  **wild cluster bootstrap** vì chỉ có **6 cluster**.
- **Q4 — dải.** Báo cáo theo ba kịch bản cường độ lưới (thấp / trung bình / cao) × ba mức tỉ trọng xe hai bánh
  trong vận tải đường bộ (50% / 65% / 80%; EDGAR chỉ có một sector `Transport` nên không tách được theo loại
  xe). Báo cáo **min – trung vị – max** của 9 tổ hợp; không báo một số duy nhất.

## 5. Quy tắc phán quyết chốt trước

Đây là phần không được sửa sau khi xem kết quả.

**Q1.** Với n = 7, giá trị tới hạn của Spearman ở α = 0,05 hai phía là **|ρ| ≈ 0,71**. Vì vậy:
- `|ρ| > 0,71` và bootstrap CI không chứa 0 ⇒ **có quan hệ**, báo cáo kèm CI.
- Ngược lại ⇒ **không phân biệt được với 0**, và phải nói rõ rằng với n = 7, một quan hệ trung bình cũng không
  phân biệt được — kết quả null ở đây **không** là bằng chứng không có quan hệ.
- Không dùng ngôn ngữ nhân quả ở Q1.

**Q2.** Thành công khi và chỉ khi **RMSE trên test nhỏ hơn RMSE của baseline persistence ít nhất 1,0 điểm phần
trăm**. Không đạt ⇒ báo cáo là thất bại, kèm phân tích lỗi theo quốc gia và theo khoảng giá trị. Không đổi
metric sau khi xem test.

**Q3.** Giữ nguyên bảng phán quyết của ADR-006 D.5:

| Kết quả | Phán quyết |
| --- | --- |
| `lead` không có ý nghĩa **và** CI của `lag` không chứa 0 | **Có đóng góp** |
| `lead` không có ý nghĩa **và** CI của `lag` chứa 0 | **Không xác định** — báo cáo null kèm CI |
| `lead` có ý nghĩa | **Không xác định** — thiết kế không tách được chiều |

Cả hai nhánh "không xác định" là kết quả hợp lệ và phải được báo cáo đầy đủ, không được hạ giọng.

**Q4.** Luôn báo cáo **dải**; nếu dải rộng đến mức không kết luận được gì thì nói thẳng như vậy. Không dùng
"tác động", chỉ dùng "nằm trong khoảng".

## 6. Kiểm tra độ vững

| # | Kiểm tra | Điều kiện đổi |
| --- | --- | --- |
| Q1 | EDGAR 2024 (bản cuối) thay cho 2025 (Fast Track) | New Zealand dịch **2,55 pp** giữa hai năm — đã kiểm chứng |
| Q1 | `2 and 3 wheelers` thay cho `cars` làm chuỗi tốc độ | tất cả 7 quốc gia đều có chuỗi này |
| Q1 | Cửa sổ 2015→2024 thay cho 2018→2024 | — |
| Q3 | Cửa sổ 2014–2024 thay cho 2010–2024 | số nước có dữ liệu sạc tăng sau 2014 |
| Q3 | Thêm/bớt kiểm soát (trọng số giao thông, giá điện) | chỉ báo cáo, không đổi kết luận chính |
| Q4 | Ba kịch bản lưới × ba mức tỉ trọng hai bánh | xem §4 |

## 7. Ràng buộc bắt buộc

1. **Không đổi câu hỏi, mẫu, biến hay quy tắc phán quyết** sau khi đã xem kết quả. Mọi thay đổi phải ghi vào §9
   **trước** khi báo cáo kết quả tương ứng.
2. Mọi bước lọc/gộp phải **in cỡ mẫu trước và sau**, và với phép gộp phải **báo khoá không khớp**.
3. **Không dùng `category = Projection-STEPS`** trong bất kỳ phân tích nào.
4. **Không đưa Singapore** vào Q1 (phần kiểm định), Q2, Q3 — không có dữ liệu IEA.
5. Q1 và Q4 **không dùng ngôn ngữ nhân quả**; Q3 chỉ dùng khi phán quyết là "có đóng góp".
6. Mọi hình phải có tiêu đề, đơn vị và chú giải (đề bài §3.4).
7. Ánh xạ tên quốc gia theo ADR-002 D.6, không dựa vào tên khớp tự động.

## 8. Thứ tự phân tích và ánh xạ notebook

| Bước | Nội dung | File |
| --- | --- | --- |
| 01 | Thu thập, mô tả nguồn, giấy phép, khám phá dữ liệu, bảng mẫu | `01_collection_exploration.ipynb` |
| 02 | **Q1**, **Q3**, **Q4** theo thứ tự tự sự | `02_analysis.ipynb` |
| 03 | **Q2** — câu hỏi ML | `03_ml_question.ipynb` |

Đánh số câu hỏi **không** trùng đánh số notebook: Q2 mang số 2 nhưng nằm ở file `03_`, vì đề bài cố định tên
file. Đã ghi ở ADR-001 C.4.

## 9. Nhật ký sai lệch

Bảng này **cố ý để trống** tại thời điểm đóng băng. Mọi sai lệch so với tài liệu này phải được thêm vào đây
kèm ngày, lý do, và ảnh hưởng lên kết luận — trước khi báo cáo kết quả bị ảnh hưởng.

| Ngày | Mục | Sai lệch | Lý do | Ảnh hưởng tới kết luận |
| --- | --- | --- | --- | --- |
| | | | | |

## 10. Tham chiếu

ADR-001 · ADR-002 · ADR-004 · ADR-006 · ADR-008. Bốn câu hỏi và chủ sở hữu: issue #23 (Q1), #21 (Q2), #22 (Q3),
#24 (Q4).

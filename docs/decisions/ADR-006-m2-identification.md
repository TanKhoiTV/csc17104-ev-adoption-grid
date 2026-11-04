# ADR-006: Nhận dạng cho M2

## Status

Proposed

## Date

2026-10-20

## Context

M2 hỏi: **mật độ trạm sạc công cộng có làm tăng tỉ lệ áp dụng xe điện không?**

Có hai vấn đề:

- **Nhân quả ngược.** Nước nhiều xe điện thường nhiều trạm sạc; tương quan dương không cho biết chiều.
- **Cỡ mẫu.** ADR-004 chốt 8 quốc gia, nhưng Singapore không có dữ liệu trong file IEA, nên M2 chỉ có **7**. Bảy quan sát chéo là quá ít; phải dùng panel để tách biến động trong nước khỏi khác biệt cấp quốc gia.

### Vì sao cú sốc thuế tín dụng 30/9/2025 không phải là nhận dạng của M2

Ngày 30/9/2025, ba khoản thuế tín dụng xe điện liên bang Mỹ (30D, 25E, 45W) ngừng áp dụng cho xe mua sau ngày đó (Public Law 119-21).

Cú sốc này **đổi cầu, không đổi cung sạc**. Một thiết kế `post × exposure` quanh nó ước lượng tác động của **thuế tín dụng**, không phải của mật độ trạm sạc. Hai câu hỏi khác nhau, không được dùng chung một hệ số.

Vì vậy cú sốc được tách thành một phân tích riêng, **M2b** (D.7), với estimand riêng.

### Vì sao M2b phải chạy theo quý

Hiệu ứng của cú sốc biến mất ở tần suất năm:

| Tần suất | Con số | Diễn giải |
| --- | --- | --- |
| Tháng | Thg 10/2025: −27%; Thg 11: −42%; Thg 12: −35% so với cùng kỳ 2024 | hiệu ứng rõ |
| Năm | Tỉ lệ bán xe điện Mỹ: 10% (2024) → 10% (2025) | không thấy gì |

Nguồn doanh số Mỹ theo tháng duy nhất là Argonne, và mọi URL trả **403** kể cả với User-Agent trình duyệt → không tự động hoá được. AFDC thì theo bang và tự động hoá được, nhưng dữ liệu sạc của AFDC có một mốc đổi cách đếm: số trạm toàn quốc 2020 → 2021 tăng **+57,8%** (31.751 → 50.097), không phải xây dựng thật. Vì vậy cửa sổ sạc của M2b phải kết thúc **trước 2021**.

M2 không dùng cú sốc nên không bị ràng buộc tần suất tháng; dữ liệu sạc theo năm của IEA là đủ.

### Dữ liệu của M2

Mật độ sạc lấy từ `EV Data Explorer 2025.xlsx` (GEVO), nhưng độ phủ không đều: Nhật/Mỹ từ 2010, Đức từ 2012, Trung Quốc từ 2014, Thái Lan/New Zealand từ 2017, **Việt Nam chỉ 2023–2024**.

## Decision

### D.1. Estimand

Tác động của **mật độ trạm sạc công cộng** lên **tỉ lệ áp dụng xe điện** (EV sales share, xe hơi), ở cấp **quốc gia–năm**.

### D.2. Panel

7 quốc gia theo ADR-004 (trừ Singapore), 2010–2024, **không cân bằng**:

| Quốc gia | Năm có dữ liệu sạc |
| --- | --- |
| Nhật, Mỹ | 2010–2024 (15) |
| Đức | 2012–2024 (13) |
| Trung Quốc | 2014–2024 (11) |
| Thái Lan, New Zealand | 2017–2024 (8) |
| Việt Nam | 2023–2024 (2) |

Tổng: **70 quan sát** (không tính Việt Nam).

### D.3. Biến

- **Kết quả:** EV sales share (cars), IEA.
- **Giải thích:** điểm sạc công cộng trên 1.000 dân, **trễ 1 năm**.
- **Kiểm soát:** GDP bình quân đầu người. Các kiểm soát khác (giá điện, transport share) chỉ báo cáo như kiểm tra độ nhạy.

### D.4. Nhận dạng

- Fixed effect **quốc gia** + **năm**.
- Biến động dùng để nhận dạng là **thay đổi trong nước** sau khi trừ xu hướng chung.
- **Kiểm tra lead/lag:** hồi quy adoption lên `lead(sạc)` và `lag(sạc)`. Nếu `lead` có ý nghĩa → có nhân quả ngược hoặc anticipation → không nhận dạng được.
- **Không dùng IV.** Không có biến công cụ nào thoả điều kiện loại trừ; lead/lag là kiểm tra chẩn đoán, không phải chiến lược nhận dạng.

### D.5. Quy tắc phán quyết (chốt trước)

| Kết quả | Phán quyết |
| --- | --- |
| `lead` không có ý nghĩa **và** CI của `lag` không chứa 0 | **Có đóng góp** |
| `lead` không có ý nghĩa **và** CI của `lag` chứa 0 | **Không xác định** — báo cáo null kèm CI |
| `lead` có ý nghĩa | **Không xác định** — thiết kế không tách được chiều |

Cả hai nhánh "không xác định" là kết quả hợp lệ, phải báo cáo đầy đủ.

### D.6. Việt Nam

Chỉ có 2 năm dữ liệu sạc nên **không đóng góp được cho M2**. Loại khỏi mô hình và **báo cáo rõ**, không loại âm thầm.

### D.7. M2b — phân tích riêng

- **Câu hỏi:** thuế tín dụng 30/9/2025 tác động thế nào đến tỉ lệ áp dụng xe điện?
- **Panel:** 51 bang + DC, **theo quý**.
- **Nhận dạng:** `post × exposure`, với `exposure` = EV share của bang năm **2019** (trước khi luật được ký).
- **Kết quả:** ưu tiên **doanh số theo quý** (Alliance for Automotive Innovation); dự phòng là **đăng ký theo năm** (AFDC — tồn kho, yếu hơn).
- **Cửa sổ sạc:** naive 2014–2025 và strict **2014–2020**.
- **Kết quả của M2b không thay thế kết luận của M2** và không được trộn vào D.5.

### D.8. Nguồn

| Vai trò | Nguồn | Truy cập |
| --- | --- | --- |
| M2: EV sales share, điểm sạc | `EV Data Explorer 2025.xlsx` (GEVO) | có sẵn trong `data/`, gitignore |
| M2: GDP bình quân | World Bank | API |
| M2b: số sạc theo bang | AFDC `historical-station-counts.xlsx` | script được |
| M2b: doanh số theo bang–quý | Alliance *Get Connected* (PDF) | tải được, số liệu nằm trong biểu đồ |
| M2b: đăng ký theo bang–năm | AFDC `vehicle-registration` | script được |

### D.9. Công cụ

`linearmodels` (panel FE) và **wild cluster bootstrap** cho sai lệch chuẩn — chỉ có 7 cluster nên cluster-robust thông thường không đáng tin. `min_ds-env.yml` hiện thiếu `statsmodels`, `linearmodels`, `pyfixest` — ADR-007 cần bổ sung.

## Alternatives Considered

- **A.1. Dùng cú sốc thuế tín dụng làm nhận dạng của M2.** Loại: cú sốc đổi cầu chứ không đổi cung sạc; hệ số là tác động của thuế, không phải của mật độ sạc.
- **A.2. Event study cấp quốc gia, tần suất tháng (Argonne).** Loại: Argonne trả 403 cho mọi URL.
- **A.3. Chỉ dùng panel quốc gia theo năm.** Đây chính là M2; nếu dùng để ước lượng cú sốc 2025 thì loại, vì ở tần suất năm hiệu ứng bằng 0 sau khi cộng.
- **A.4. IV với một biến công cụ.** Loại: không có biến nào thoả điều kiện loại trừ.
- **A.5. Dùng 51 bang Mỹ làm panel chính của M2.** Loại: đổi cấp phân tích, mâu thuẫn với ADR-004; giữ làm M2b.
- **A.6. Loại Việt Nam mà không báo cáo.** Loại: phải báo cáo rõ (D.6).

## Consequences

- **C.1. Chỉ có 7 cluster.** Sai lệch chuẩn phải dùng wild cluster bootstrap; sức mạnh thống kê của M2 thấp và ADR nói rõ điều đó.
- **C.2. Panel không cân bằng.** Việt Nam bị loại khỏi M2; n = 70.
- **C.3. M2 và M2b là hai estimand, hai phán quyết.** Không được gộp kết luận.
- **C.4. ADR-004 cần sửa một chỗ:** vai trò của Mỹ đang ghi "event study của M2", phải là **M2b**.
- **C.5. Tương quan đồng thời vẫn còn.** Fixed effect và lead/lag chỉ giảm, không loại bỏ được nhân quả ngược.
- **C.6. Môi trường thiếu gói.** `min_ds-env.yml` cần `statsmodels`, `linearmodels`, `pyfixest` (ADR-007).
- **C.7. `SPECIFICATION.md` kế thừa D.3 và D.5**, không viết lại.

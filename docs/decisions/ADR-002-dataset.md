# ADR-002: Dataset decision record

## Status

Proposed

## Date

2026-11-04

## Context

Dự án cần hai loại dữ liệu, cho ba module:

- **Phát thải theo sector và quốc gia** — cho M3 và cho cơ sở chọn mẫu của ADR-004.
- **Dữ liệu xe điện** (sales share, stock share, điểm sạc công cộng) — cho M1 (độ phủ diffusion) và M2 (mật độ sạc → áp dụng).

Ràng buộc:

- Phải phủ đủ **8 quốc gia** trong ADR-004.
- Phải là **bản phát hành chính thức, có số phiên bản**, để trích dẫn và tái lập.
- **Không được commit** vào repo: điều khoản giấy phép và kích thước file (xem D.3).

Hai file dưới đây là bộ dữ liệu chính. Chúng đã nằm trong `data/` và bị `.gitignore` che bởi `data/*`.

## Decision

### D.1. EDGAR 2026 — phát thải theo sector

| Thuộc tính | Giá trị |
| --- | --- |
| File | `data/EDGAR_2026_GHG_booklet_2026.xlsx` |
| Kích thước | 4.767.596 bytes |
| SHA-256 | `BB77A0DA5735925B3A6A64BE63DADE9E71B57174D5EC6C7EFF872274DF00F88C` |
| Sheet | `GHG_by_sector_and_country` |
| Bộ lọc | `Substance = CO2`, năm **2025** |
| Mẫu số | Tổng của **8 sector**, không gồm LULUCF |
| Gộp sector | `Industry = Industrial Combustion + Processes`; `Power = Power Industry` |

Dùng cho: cấu trúc phát thải theo sector của M3, và làm cơ sở cho vai trò từng quốc gia
trong ADR-004.

Lưu ý: năm 2025 là bản **Fast Track (sơ bộ)**; 2024 là bản cuối. Độ nhạy giữa hai năm phải
được ghi trong `SPECIFICATION.md`.

### D.2. IEA GEVO 2025 — dữ liệu xe điện

| Thuộc tính | Giá trị |
| --- | --- |
| File | `data/EV Data Explorer 2025.xlsx` |
| Kích thước | 936.334 bytes |
| SHA-256 | `309C6342BB730D1B565553B6F57F6EF7A5F436D164AF81DBCC6A2DC8AB35699D` |
| Sheet | `GEVO_EV_2025` |
| Bộ lọc | `category = Historical`, `powertrain = EV` |

Dùng cho: EV sales share, EV stock share và số điểm sạc công cộng của M1 và M2.

Giới hạn đã biết:

- Năm lịch sử mới nhất là **2024**, nên file **không có quan sát hậu điều trị** cho cú sốc
  30/9/2025. M2b dùng nguồn khác (ADR-006, D.7–D.8).
- **Singapore không tồn tại** trong file, nên M1 và M2 chỉ có 7 quốc gia.
- IEA làm tròn **hai chữ số có nghĩa**; với các giá trị rất nhỏ (ví dụ Vietnam 0,0016% năm
  2018), độ chính xác này giới hạn ý nghĩa của CI.

### D.3. Giấy phép và lưu trữ

**EDGAR 2026.** Điều khoản của bộ dữ liệu ghi: tài liệu thuộc EU được cấp phép
**CC BY 4.0**, "trừ khi có ghi chú khác". Ngoại lệ quan trọng: thành phần **IEA-EDGAR CO2**
(CO₂ từ đốt nhiên liệu hoá thạch) được cấp phép **CC BY-NC-ND 4.0**.

Vì M3 lọc `Substance = CO2` và phần CO₂ từ đốt nhiên liệu chính là thành phần IEA-EDGAR CO2,
phần dữ liệu dự án thực sự dùng **thuộc NC-ND**, không phải CC BY 4.0:

- **NC** — chỉ dùng cho mục đích học thuật, không thương mại.
- **ND** — không được phân phối lại bản đã sửa đổi.
- Bắt buộc ghi công theo hướng dẫn trích dẫn của EDGAR.

**IEA GEVO 2025.** Trang điều khoản của IEA (`iea.org/terms`) trả **403** khi truy cập bằng
script, nên điều khoản **chưa được xác nhận**. Trong lúc chờ xác nhận, file chỉ dùng nội bộ
và không được phân phối lại.

**Kết luận.** Cả hai file nằm ngoài git, che bởi `data/*` trong `.gitignore`. Đây là lý do
**giấy phép**, không chỉ vì kích thước. Bảng số liệu trong các ADR là bản ghi bền vững thay
cho file.

### D.4. Ghi nhận nguồn gốc

| File | Nguồn | Ngày tải | SHA-256 (rút gọn) |
| --- | --- | --- | --- |
| EDGAR 2026 | EDGAR / JRC, bản phát hành `EDGAR_2026_GHG` | 2026-10-19 | `BB77A0DA…` |
| GEVO 2025 | IEA, *Global EV Outlook 2025* — Global EV Data Explorer | 2026-10-19 | `309C6342…` |

Vì file không nằm trong repo, **bảng này là bản ghi nguồn gốc**. Ai clone repo phải tải lại
đúng phiên bản và kiểm tra hash trước khi chạy.

### D.5. Ghim phiên bản

- Phiên bản dùng trong dự án là **EDGAR 2026** và **GEVO 2025**. Không thay file tại chỗ.
- Bản mới hơn (ví dụ EDGAR 2027, GEVO 2026) phải có **ADR mới** thay thế ADR này.
- Mọi kết quả trong notebook phải ghi phiên bản dữ liệu đã dùng.

### D.6. Ánh xạ tên quốc gia

Hai file đặt tên khác nhau. `prepare_data.py` phải dùng bảng ánh xạ tường minh; nếu không sẽ
âm thầm bỏ mất dòng — cùng kiểu lỗi đã che giấu việc thiếu Singapore.

| Quốc gia | EDGAR name | IEA key |
| --- | --- | --- |
| Vietnam | `Viet Nam` | `Viet Nam` |
| Thailand | `Thailand` | `Thailand` |
| Singapore | `Singapore` | _không có_ |
| China | `China` | `China` |
| Japan | `Japan` | `Japan` |
| Germany | `Germany` | `Germany` |
| United States | `United States` | `USA` |
| New Zealand | `New Zealand` | `New Zealand` |

### D.7. Ngoài phạm vi

Các nguồn sau **không** thuộc ADR này:

- AFDC (sạc và đăng ký theo bang), Argonne (doanh số Mỹ theo tháng), Alliance for Automotive
  Innovation (doanh số theo bang–quý), EAFO (EU theo tháng).

Chúng phục vụ M2b và được chốt trong **ADR-006, D.7–D.8**. Quy tắc: thêm một nguồn mới phải
ghi rõ giấy phép, cách truy cập và ngày tải; nếu là nguồn chính thì cần ADR mới.

## Alternatives Considered

- **A.1. Dùng OWID GEVO 2026 thay GEVO 2025.** OWID có Singapore 2016–2025, nhưng sẽ trộn hai
  phiên bản IEA trong cùng một mẫu, làm yếu tính đồng nhất. **Loại.**
- **A.2. Dùng EDGAR 2025 thay EDGAR 2026.** Bản 2025 dừng ở 2024, thiếu năm 2025 đang dùng cho
  cấu trúc sector. **Loại.**
- **A.3. Commit hai file xlsx vào repo.** Vi phạm điều khoản **ND** của IEA-EDGAR CO2 và làm
  repo nặng thêm ~5,7 MB. **Loại.**
- **A.4. Lấy dữ liệu EV từ AFDC/EEA thay IEA.** Không phủ đủ 8 quốc gia và khác định nghĩa
  (đăng ký theo bang/nước) so với sales share của IEA. **Loại.**
- **A.5. Cào trực tiếp từ dashboard thay vì dùng file phát hành.** Không cần thiết khi đã có
  file chính thức, có phiên bản và hash. **Loại.**

## Consequences

- **C.1. Clone repo không kèm dữ liệu.** Phải có bước tải lại và kiểm tra SHA-256; ADR này là
  bản ghi nguồn gốc.
- **C.2. Giấy phép NC-ND hạn chế tái sử dụng.** Không được phân phối lại bản sửa đổi; dự án chỉ
  dùng cho mục đích học thuật.
- **C.3. Năm 2025 của EDGAR là sơ bộ.** Kết quả M3 phải kèm kiểm tra độ nhạy với bản 2024.
- **C.4. IEA làm tròn hai chữ số có nghĩa.** Các giá trị nhỏ của Vietnam bị giới hạn độ chính xác.
- **C.5. Tên quốc gia khác nhau giữa hai file.** Bắt buộc có bảng ánh xạ (D.6).
- **C.6. Singapore không có dữ liệu IEA.** M1 và M2 chạy trên 7 quốc gia; M3 trên 8.
- **C.7. Điều khoản IEA GEVO chưa xác nhận.** Cần kiểm tra trên trình duyệt trước khi công bố
  dữ liệu dẫn xuất.

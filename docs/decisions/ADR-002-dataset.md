# ADR-002: Chốt bộ dữ liệu

## Status

Đề xuất

## Date

2026-11-04

## Context

Dự án cần hai loại dữ liệu, cho ba module:

- **Phát thải theo sector và quốc gia** — cho Q1 và là cơ sở chọn mẫu (ADR-004).
- **Dữ liệu xe điện** (sales share, stock share, điểm sạc công cộng) — cho Q2 (độ phủ diffusion) và Q3 (mật độ sạc → áp dụng).

Ràng buộc:

- Phải phủ đủ **8 quốc gia** trong ADR-004.
- Phải là **bản phát hành chính thức, có số phiên bản**, để trích dẫn và tái lập.
- **Không được commit** vào repo: điều khoản giấy phép và kích thước file (xem D.3).

Hai file dưới đây là bộ dữ liệu chính. Chúng nằm trong `data/` và bị `.gitignore` che bởi `data/*`.

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

Tám nhãn sector của EDGAR, verbatim như trong sheet:

1. Agriculture
2. Buildings
3. Fuel Production
4. Industrial Combustion
5. Power Industry
6. Processes
7. Transport
8. Waste

`Industry` và `Power` trong bảng của ADR-004 là các nhóm gộp của các nhãn này; `Transport` dùng nguyên.

Dùng cho: cấu trúc sector của Q1, và cơ sở cho vai trò từng quốc gia trong ADR-004.

Lưu ý: năm 2025 là bản **Fast Track (sơ bộ)**; 2024 là bản cuối. Độ nhạy giữa hai năm phải được ghi trong `SPECIFICATION.md`.

### D.2. IEA GEVO 2025 — dữ liệu xe điện

| Thuộc tính | Giá trị |
| --- | --- |
| File | `data/EV Data Explorer 2025.xlsx` |
| Kích thước | 936.334 bytes |
| SHA-256 | `309C6342BB730D1B565553B6F57F6EF7A5F436D164AF81DBCC6A2DC8AB35699D` |
| Sheet | `GEVO_EV_2025` |
| Bộ lọc | `category = Historical`, `powertrain = EV` |

Dùng cho: EV sales share, EV stock share và số điểm sạc công cộng của Q2 và Q3.

Giới hạn đã biết:

- Năm lịch sử mới nhất là **2024**, nên file **không có quan sát hậu điều trị** cho cú sốc 30/9/2025. Q3b dùng nguồn khác (ADR-006, D.7–D.8).
- **Singapore không tồn tại** trong file, nên không thể vào Q2 hay Q3 (và chỉ đóng góp cấu trúc cho Q1).
- IEA làm tròn **hai chữ số có nghĩa**; với các giá trị rất nhỏ (ví dụ Vietnam 0.0016% năm 2018) độ chính xác này giới hạn ý nghĩa của khoảng tin cậy.
- Việc tải file bị **gated sau tài khoản IEA** ("You are either not logged in or your login session has expired… create an IEA account to download data"). Một clone mới không tải lại được nếu không có tài khoản, nên hash pin ở D.1/D.2 càng quan trọng.

### D.3. Giấy phép và lưu trữ

**EDGAR 2026.** Điều khoản của bộ dữ liệu ghi: tài liệu thuộc EU được cấp phép **CC BY 4.0**, "trừ khi có ghi chú khác". Ngoại lệ quan trọng: thành phần **IEA-EDGAR CO2** (CO₂ từ đốt nhiên liệu hoá thạch) được cấp phép **CC BY-NC-ND 4.0**.

Vì Q1 lọc `Substance = CO2`, và CO₂ từ đốt nhiên liệu chính là thành phần IEA-EDGAR CO2, phần dữ liệu dự án thực sự dùng **thuộc NC-ND**:

- **NC** — chỉ dùng cho mục đích học thuật, không thương mại.
- **ND** — không được phân phối lại bản đã sửa đổi.
- **Action item:** người dùng dữ liệu IEA-EDGAR CO2 phải liên hệ IEA tại `compliance@iea.org` để xin phép sử dụng ngoài điều khoản CC BY-NC-ND 4.0.

**IEA GEVO 2025.** Giấy phép xác nhận ngày 07/11/2026 từ trang sản phẩm `https://www.iea.org/data-and-statistics/data-product/global-ev-outlook-2025` (fetch bằng trình duyệt, lưu làm bản ghi HTML; scripted access trả về Cloudflare challenge):

- **CC BY 4.0** — được phân phối lại kèm attribution.
- Chuỗi trích dẫn IEA cung cấp: `IEA, Global EV Outlook 2025, IEA, Paris, https://www.iea.org/data-and-statistics/data-product/global-ev-outlook-2025, Licence: CC BY 4.0`
- File là "Global EV Data File", ngày 14/05/2025 trên cùng trang.

**Kết luận.** Cả hai file nằm ngoài git, che bởi `data/*` trong `.gitignore`. Lý do giờ là **khả năng tái lập** (cả hai đều tải được bằng URL và kiểm hash, nhưng không được commit), không phải giấy phép GEVO. Điều khoản NC-ND của thành phần EDGAR CO₂ là ràng buộc chính đối với **phân phối lại**: phân phối lại bản thô nguyên văn là hợp lý, nhưng phân phối lại `emissions_long.csv` (một bản dẫn xuất đã lọc) thì không.

### D.4. Ghi nhận nguồn gốc

Vì file không nằm trong repo, bảng này là bản ghi nguồn gốc bền vững.

| File | Nguồn | Ngày tải | SHA-256 (rút gọn) |
| --- | --- | --- | --- |
| EDGAR 2026 | EDGAR / JRC, bản phát hành `EDGAR_2026_GHG` | 2026-10-19 | `BB77A0DA…` |
| GEVO 2025 | IEA, *Global EV Outlook 2025* — Global EV Data Explorer | 2026-10-19 | `309C6342…` |

Ai clone repo phải tải đúng phiên bản trên và kiểm tra hash trước khi chạy `prepare_data.py`.

### D.5. Ghim phiên bản

- Phiên bản dùng trong dự án là **EDGAR 2026** và **GEVO 2025**. Không thay file tại chỗ.
- Bản mới hơn (ví dụ EDGAR 2027, GEVO 2026) phải có **ADR mới** thay thế ADR này.
- Mọi kết quả trong notebook phải ghi phiên bản dữ liệu đã dùng.

### D.6. Ánh xạ tên quốc gia

Hai file đặt tên khác nhau. `prepare_data.py` phải dùng bảng ánh xạ tường minh; nếu không sẽ âm thầm bỏ mất dòng — cùng kiểu lỗi đã che giấu việc thiếu Singapore.

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

- AFDC (sạc và đăng ký theo bang), Argonne (doanh số Mỹ theo tháng), Alliance for Automotive Innovation (doanh số theo bang–quý), EAFO (EU theo tháng).

Chúng phục vụ Q3b và được chốt trong **ADR-006, D.7–D.8**. Quy tắc: thêm một nguồn mới phải ghi rõ giấy phép, cách truy cập và ngày tải; nếu là nguồn chính thì cần ADR mới.

## Alternatives Considered

- **A.1. Dùng OWID GEVO 2026 thay GEVO 2025.** OWID có Singapore 2016–2025, nhưng sẽ trộn hai phiên bản IEA trong cùng một mẫu và làm yếu tính đồng nhất. **Loại.**
- **A.2. Dùng EDGAR 2025 thay EDGAR 2026.** Bản 2025 dừng ở 2024, thiếu năm 2025 đang dùng cho cấu trúc sector. **Loại.**
- **A.3. Commit hai file xlsx vào repo.** Vi phạm điều khoản **ND** của IEA-EDGAR CO2 và làm repo nặng thêm ~5,7 MB. **Loại.**
- **A.4. Lấy dữ liệu EV từ AFDC/EEA thay IEA.** Không phủ đủ 8 quốc gia và khác định nghĩa (đăng ký theo bang/nước) so với sales share của IEA. **Loại.**
- **A.5. Cào trực tiếp từ dashboard thay vì dùng file phát hành.** Không cần thiết khi đã có file chính thức, có phiên bản và hash. **Loại.**

## Consequences

- **C.1. Clone repo không kèm dữ liệu.** Phải có bước tải lại và kiểm tra SHA-256; ADR này là bản ghi nguồn gốc.
- **C.2. Giấy phép NC-ND hạn chế tái sử dụng.** Không được phân phối lại bản sửa đổi; dự án chỉ dùng cho mục đích học thuật.
- **C.3. EDGAR 2025 (năm dữ liệu) là Fast Track (sơ bộ); 2024 là bản cuối.** Kết quả Q1 phải kèm kiểm tra độ nhạy với năm.
- **C.4. IEA làm tròn hai chữ số có nghĩa.** Các giá trị nhỏ của Vietnam bị giới hạn độ chính xác.
- **C.5. Tên quốc gia khác nhau giữa hai file.** Bắt buộc có bảng ánh xạ (D.6).
- **C.6. Singapore không có dữ liệu IEA.** Q2 và Q3 chạy trên 6 quốc gia; Q1 chạy trên 7 (mô tả cấu trúc cho 8); Q4 chạy trên 1.
- **C.7. Điều khoản IEA GEVO chưa xác nhận tại thời điểm viết** và nay đã xác nhận CC BY 4.0; việc tải bị gated sau tài khoản vẫn là ràng buộc tái lập.

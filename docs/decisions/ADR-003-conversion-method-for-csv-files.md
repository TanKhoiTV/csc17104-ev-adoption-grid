# ADR-003: Phương pháp chuyển đổi file CSV/XLSX

## Status

Đề xuất

## Date

2026-11-08 (sửa đổi 2026-11-19)

## Context

- Hai file nguồn là `.xlsx` (gitignore, ~5.7 MB tổng), nhưng notebook và phân tích cần dữ liệu dạng bảng phẳng, có thể đọc nhanh và kiểm tra bằng `git diff`-style hash. Phải chuyển sang CSV tidy trong `data/processed/`.
- Ràng buộc:
    - **Tái lập.** Cùng input + cùng code → cùng output byte-identical. Không có bước tay.
    - **Một entry point.** Toàn bộ logic chuyển đổi nằm trong một script; notebook chỉ đọc CSV, không tự lọc sheet.
    - **Không fabricate dữ liệu thiếu.** Việt Nam thiếu năm, Singapore không có trong file IEA — phải để trống tường minh, không điền 0.
    - **Authority rule.** `ADR > SPECIFICATION.md > notebook` (SPECIFICATION.md §1): mọi thay đổi schema phải sửa ADR này trước.
- Tooling đã chốt ở `environment.yml`: Python 3.11.5, pandas 2.1.1, openpyxl 3.1.2. Không thêm dependency mới trong ADR này.
- Nguồn đã chốt ở ADR-002 (D.1/D.2): EDGAR `GHG_by_sector_and_country`, `Substance = CO2`, năm 2025; IEA `GEVO_EV_2025`, `category = Historical`. Bộ lọc `powertrain = EV` ở ADR-002 D.2 chỉ đúng cho chuỗi share — D.3 dưới đây thay bằng bộ lọc theo parameter. Ánh xạ tên quốc gia theo ADR-002 D.6.
- EDGAR là **bảng thưa**: trong 64 ô (8 quốc gia × 8 sector) chỉ có **61 dòng** — Singapore thiếu `Agriculture`, Đức và Mỹ thiếu `Waste`. Schema, row-count và kiểm tra coverage ở D.2/D.6 phải phản ánh đúng thực tế này.

## Decision

### D.1. Entry point và luồng xử lý

- Một script `src/prepare_data.py` là **entry point duy nhất**, chạy từ root repo: `python src/prepare_data.py`.
- Luồng:
    1. Đọc hash SHA-256 của hai file `.xlsx` **trong `data/raw/`**; so sánh với pin trong ADR-002 D.1/D.2. Lệch → dừng, báo lỗi.
    2. Đọc sheet với bộ lọc ở D.2/D.3.
    3. Áp dụng ánh xạ tên quốc gia (D.4).
    4. Ghi `data/processed/emissions_long.csv` và `data/processed/ev_long.csv`.
    5. In log: số dòng (tổng và theo từng parameter), số quốc gia, hash output.
- Input đọc từ `data/raw/`, output ghi vào `data/processed/`. Cả hai bị `data/*` gitignore, nên một clone phải tự tải `.xlsx` vào `data/raw/` trước khi chạy.
- Script idempotent: chạy lại cho cùng input cho cùng output byte-identical (sort + format cố định).

### D.2. EDGAR → `emissions_long.csv`

- Sheet: `GHG_by_sector_and_country`.
- Bộ lọc: `Substance = CO2`, `year = 2025`.
- Mẫu số: tổng của **8 sector** (Agriculture, Buildings, Fuel Production, Industrial Combustion, Power Industry, Processes, Transport, Waste), **không gồm LULUCF**.
- Gộp: `Industry = Industrial Combustion + Processes`; `Power = Power Industry`; `Transport` dùng nguyên.
- Schema (pin):

| Cột | Kiểu | Ý nghĩa |
| --- | --- | --- |
| `country` | str | Tên thường dùng (canonical, xem D.4) |
| `year` | int | 2025 (pinned; giữ cột để mở rộng sau) |
| `substance` | str | `CO2` |
| `sector` | str | Một trong 8 nhãn verbatim của EDGAR |
| `sector_group` | str | `Industry` / `Power` / `Transport` / `Other` |
| `emissions_mt` | float | Mt CO₂ của sector đó, năm 2025 |

- Một dòng = một (quốc gia, sector) **có mặt** trong sheet. Tổng **61 dòng**, không phải 64 — EDGAR là bảng thưa, ba ô hoàn toàn không có dòng (không phải NaN):

| Quốc gia | Sector vắng | Số dòng |
| --- | --- | --- |
| Singapore | `Agriculture` | 7 |
| Germany | `Waste` | 7 |
| United States | `Waste` | 7 |

- Ô vắng **không được điền 0** và không tạo dòng. Vì vậy mẫu số của "trọng số giao thông" (Q1) là tổng các dòng CO₂ **hiện có** của quốc gia đó, đúng như SPECIFICATION.md §3.
- `sector_group = Other` cho Agriculture, Buildings, Fuel Production, Waste.

### D.3. IEA GEVO → `ev_long.csv`

- Sheet: `GEVO_EV_2025`.
- Bộ lọc chung: `category = Historical`.
- **Bộ lọc theo parameter** (thay cho `powertrain = EV` đơn nhất; xem ghi chú điều chỉnh ADR-002 D.2 bên dưới):

| `parameter` | `mode` | `powertrain` | `unit` (verbatim) |
| --- | --- | --- | --- |
| `EV sales share` | `Cars`, `2 and 3 wheelers` | `EV` | `percent` |
| `EV stock share` | `Cars`, `2 and 3 wheelers` | `EV` | `percent` |
| `EV charging points` | `EV` | `Publicly available fast`, `Publicly available slow` | `charging points` |

- **Chỉ ba parameter trên.** `EV sales` / `EV stock` (đếm xe), `Battery demand` và `Oil displacement` **không** vào CSV: không câu hỏi nào (Q1–Q4) dùng, và giữ chúng sẽ kéo theo việc gộp BEV/PHEV/FCEV không cần thiết. Muốn thêm ⇒ sửa ADR này trước (authority rule).
- Schema (pin):

| Cột | Kiểu | Ý nghĩa |
| --- | --- | --- |
| `country` | str | Tên thường dùng (canonical, xem D.4) |
| `year` | int | Năm quan sát, 2010–2024 (mỗi nước bắt đầu ở năm có dữ liệu) |
| `parameter` | str | Ba giá trị ở bảng lọc trên |
| `mode` | str | `Cars` / `2 and 3 wheelers`; dòng sạc dùng `EV` |
| `powertrain` | str | `EV` / `Publicly available fast` / `Publicly available slow` — verbatim của IEA |
| `value` | float | Giá trị thô của IEA |
| `unit` | str | `percent` hoặc `charging points` — verbatim, không chuẩn hoá |

- **Khoá duy nhất:** (country, year, parameter, mode, powertrain). Không pivot trong bước này — pivot là việc của notebook (Q2/Q3).
- **Quy tắc gộp cho notebook** (không làm trong `prepare_data.py`, để dữ liệu giữ nguyên bản thô):
    - Điểm sạc công cộng = `fast + slow`. Nếu một năm chỉ có một loại ⇒ cộng dòng có mặt, loại vắng coi như 0 và phải ghi rõ trong notebook (có country-year chỉ có `slow`: China ×4, United States ×5; chỉ có `fast`: Japan ×4, New Zealand ×1).
    - `EV sales share` và `EV stock share` đã là tổng theo powertrain (`powertrain = EV`) ⇒ **không** cộng thêm.
- **Điều chỉnh so với ADR-002 D.2.** ADR-002 chốt `powertrain = EV`, nhưng bộ lọc đó chỉ khớp chuỗi share; dòng `EV charging points` dùng `mode = EV` và `powertrain` là fast/slow. ADR-003 thay bằng bảng lọc theo parameter ở trên; phần chọn file/hash/giấy phép của ADR-002 không đổi.
- **Singapore không có dòng nào** trong file IEA → không fabricate, không điền 0; log ghi rõ "0 dòng cho Singapore".
- **Không cắt năm.** CSV giữ toàn bộ 2010–2024; cửa sổ 2014–2024 (Q4) và 2018–2024 (Q1) là lựa chọn của notebook, ghi trong SPECIFICATION.md.

### D.4. Ánh xạ tên quốc gia

- Bảng ánh xạ theo ADR-002 D.6, canonical = tên thường dùng (cột đầu tiên):

| Canonical | EDGAR `Country` | IEA `region_country` |
| --- | --- | --- |
| Vietnam | `Viet Nam` | `Viet Nam` |
| Thailand | `Thailand` | `Thailand` |
| Singapore | `Singapore` | _không có_ |
| China | `China` | `China` |
| Japan | `Japan` | `Japan` |
| Germany | `Germany` | `Germany` |
| United States | `United States` | `USA` |
| New Zealand | `New Zealand` | `New Zealand` |

- Tên cột trong file nguồn: EDGAR dùng `Country`, IEA dùng `region_country` — không dựa vào khớp tên tự động.

- Ánh xạ theo bảng ở trên: chỉ 8 tên canonical được giữ; tên khác trong file bị loại, **không** phải lỗi. Fail-fast áp dụng ở mức nước đích: nếu một nước trong bảng vắng sau mapping ⇒ lỗi. Đây là cùng kiểu lỗi đã che giấu việc thiếu Singapore.
- Country canonical là khoá nối giữa hai CSV và với ADR-004.

### D.5. Encoding và định dạng output

- **UTF-8, không BOM**, line ending LF.
- Cột theo đúng thứ tự schema ở D.2/D.3; không có cột index.
- Sort: `country, year, sector` (emissions) và `country, year, parameter, mode, powertrain` (ev) — thứ tự này là một phần của hợp đồng byte-identical.
- Float format: Python default `repr` của pandas (`to_csv` mặc định), không làm tròn — làm tròn là việc của phân tích.
- Missing value: để trống (pandas ghi `""`), không ghi `NA`/`0`/`NaN` literal.

### D.6. Xác thực và provenance

- **Input hash.** So sánh SHA-256 của hai `.xlsx` với pin ở ADR-002 D.1/D.2; lệch → dừng.
- **Row count.** `emissions_long.csv`: **61 dòng** (= 64 ô − 3 ô vắng ở D.2). `ev_long.csv`: **496 dòng** theo bảng coverage bên dưới.
- **Country coverage.** emissions: đủ 8 nước. ev: đủ 7 nước (Singapore = 0 dòng).
- **Sector coverage.** Mỗi nước có **≥ 7 sector**, và chỉ được vắng đúng các ô trong bảng ngoại lệ ở D.2. Lệch khỏi tập đó ⇒ lỗi.
- **EV coverage (pin).** Số dòng kỳ vọng cho mỗi (country, parameter) sau bộ lọc D.3:

| Country | `EV sales share` | `EV stock share` | `EV charging points` | Tổng |
| --- | --- | --- | --- | --- |
| China | 28 | 28 | 18 | 74 |
| Germany | 28 | 28 | 26 | 82 |
| Japan | 22 | 22 | 26 | 70 |
| New Zealand | 30 | 30 | 15 | 75 |
| Thailand | 30 | 30 | 16 | 76 |
| United States | 28 | 28 | 25 | 81 |
| Vietnam | 16 | 18 | 4 | 38 |
| **Tổng** | **182** | **184** | **130** | **496** |

- **Missing-value check.** emissions không có NaN trong `emissions_mt` (đã kiểm: 0). ev: bộ lọc D.3 hiện cho 0 NaN và 0 trùng khoá; nếu bản IEA khác làm phát sinh NaN thì chỉ log số lượng — không điền, không bỏ dòng im lặng.
- **Output hash.** In SHA-256 của hai CSV vào log của script; không commit CSV (bị `data/*` gitignore).
- **Fail on any mismatch.** Không "cảnh báo rồi tiếp tục".

## Alternatives Considered

- **A.1. Convert bằng Excel macro / Power Query.** Loại: phụ thuộc GUI, không tái lập được trên máy khác, khó review trong PR.
- **A.2. Convert bằng R (`readxl`).** Loại: thêm toolchain; nhóm đang dùng Python và env đã có openpyxl.
- **A.3. Đọc `.xlsx` trực tiếp trong notebook.** Loại: chậm, bộ lọc rải rác ở nhiều cell, dễ lệch giữa các notebook; ADR-003 muốn một nguồn sự thật.
- **A.4. Output wide (mỗi sector một cột).** Loại: khó ghép hai nguồn, khó kiểm tra; long là chuẩn tidy và khớp với `groupby` của Q1/Q3.
- **A.5. Bỏ cột `year` vì EDGAR chỉ có 2025.** Loại: mất khả năng mở rộng khi có EDGAR 2027; giữ cột chi phí không đáng kể.
- **A.6. Điền 0 cho Singapore / năm thiếu của Việt Nam.** Loại: fabricate dữ liệu, vi phạm ràng buộc Context; để trống và xử lý tường minh ở notebook.
- **A.7. Gộp `fast + slow` (charging) ngay trong `prepare_data.py`.** Loại: làm mất khả năng kiểm chứng bản thô và làm mờ khác biệt fast/slow; Q3 chỉ cần tổng nên việc gộp để notebook làm theo quy tắc ghi ở D.3. Sales/stock đếm xe bị loại hẳn khỏi CSV nên không phát sinh việc gộp BEV/PHEV/FCEV.
- **A.8. Chuẩn hoá `unit` về `%` / `vehicles` / `points`.** Loại: phải đoán và dễ sai; giữ verbatim `percent` / `charging points` để `prepare_data.py` không phải diễn giải.

## Consequences

- **C.1. `data/processed/` bị gitignore** (`data/*`). ADR-003 + hash output là bản ghi bền vững; clone repo phải chạy `python src/prepare_data.py` sau khi tải `.xlsx` vào `data/raw/` và kiểm hash input.
- **C.2. Không thay đổi env.** openpyxl 3.1.2 đã có; không cần sửa `environment.yml` cho ADR này (ADR-007 sẽ thêm statsmodels v.v.).
- **C.3. Notebook chỉ đọc CSV.** Mọi thay đổi schema phải sửa ADR-003 trước, theo authority rule.
- **C.4. Singapore và các năm thiếu của Việt Nam** phải được xử lý tường minh ở Q1/Q2/Q3 (loại khỏi mô hình và báo cáo rõ), không âm thầm bỏ dòng.
- **C.5. Thêm `prepare_data.py` là bước tiếp theo** (ngoài phạm vi ADR này). Khi viết script, phải khớp schema và kiểm tra ở D.6; nếu lệch → sửa ADR-003 trước.
- **C.6. ADR-002 D.2 được điều chỉnh một phần.** `powertrain = EV` chỉ còn đúng cho chuỗi share; `EV charging points` dùng `mode = EV` với `powertrain` fast/slow. File/hash/giấy phép ở ADR-002 không đổi; lần sửa ADR-002 tới phải đồng bộ D.2 với D.3 ở đây.
- **C.7. Bảng coverage ở D.6 là hợp đồng.** Fixed effect của Q3 và mẫu số của Q2 phụ thuộc trực tiếp vào 496 dòng; mọi thay đổi coverage phải sửa ADR-003 trước.

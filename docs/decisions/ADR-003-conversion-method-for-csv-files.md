# ADR-003: Phương pháp chuyển đổi file CSV/XLSX

## Status

Đề xuất

## Date

2026-11-08

## Context

- Hai file nguồn là `.xlsx` (gitignore, ~5.7 MB tổng), nhưng notebook và phân tích cần dữ liệu dạng bảng phẳng, có thể đọc nhanh và kiểm tra bằng `git diff`-style hash. Phải chuyển sang CSV tidy trong `data/processed/`.
- Ràng buộc:
    - **Tái lập.** Cùng input + cùng code → cùng output byte-identical. Không có bước tay.
    - **Một entry point.** Toàn bộ logic chuyển đổi nằm trong một script; notebook chỉ đọc CSV, không tự lọc sheet.
    - **Không fabricate dữ liệu thiếu.** Việt Nam thiếu năm, Singapore không có trong file IEA — phải để trống tường minh, không điền 0.
    - **Authority rule.** `ADR > SPECIFICATION.md > notebook` (SPECIFICATION.md §1): mọi thay đổi schema phải sửa ADR này trước.
- Tooling đã chốt ở `min_ds-env.yml`: Python 3.11.5, pandas 2.1.1, openpyxl 3.1.2. Không thêm dependency mới trong ADR này.
- Nguồn và bộ lọc đã chốt ở ADR-002 (D.1/D.2): EDGAR `GHG_by_sector_and_country`, `Substance = CO2`, năm 2025; IEA `GEVO_EV_2025`, `category = Historical`, `powertrain = EV`. Ánh xạ tên quốc gia theo ADR-002 D.6.

## Decision

### D.1. Entry point và luồng xử lý

- Một script `prepare_data.py` ở root repo là **entry point duy nhất**.
- Luồng:
    1. Đọc hash SHA-256 của hai file `.xlsx`; so sánh với pin trong ADR-002 D.1/D.2. Lệch → dừng, báo lỗi.
    2. Đọc sheet với bộ lọc đã chốt.
    3. Áp dụng ánh xạ tên quốc gia (D.4).
    4. Ghi `data/processed/emissions_long.csv` và `data/processed/ev_long.csv`.
    5. In log: số dòng, số quốc gia, hash output.
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

- Một dòng = một (quốc gia, sector). 8 nước × 8 sector = **64 dòng**.
- `sector_group = Other` cho Agriculture, Buildings, Fuel Production, Waste.

### D.3. IEA GEVO → `ev_long.csv`

- Sheet: `GEVO_EV_2025`.
- Bộ lọc: `category = Historical`, `powertrain = EV`.
- Schema (pin):

| Cột | Kiểu | Ý nghĩa |
| --- | --- | --- |
| `country` | str | Tên thường dùng (canonical, xem D.4) |
| `year` | int | Năm quan sát |
| `parameter` | str | `EV sales share` / `EV stock share` / `EV charging points` / `EV sales` / `EV stock` |
| `powertrain` | str | `EV` |
| `value` | float | Giá trị thô của IEA |
| `unit` | str | `%` cho share; `vehicles` cho sales/stock; `points` cho charging |

- Một dòng = một (quốc gia, năm, parameter). Không pivot trong bước này — pivot là việc của notebook (Q2/Q3).
- **Singapore không có dòng nào** trong file IEA → không fabricate, không điền 0; log ghi rõ "0 dòng cho Singapore".

### D.4. Ánh xạ tên quốc gia

- Bảng ánh xạ theo ADR-002 D.6, canonical = tên thường dùng (cột đầu tiên):

| Canonical | EDGAR name | IEA key |
| --- | --- | --- |
| Vietnam | `Viet Nam` | `Viet Nam` |
| Thailand | `Thailand` | `Thailand` |
| Singapore | `Singapore` | _không có_ |
| China | `China` | `China` |
| Japan | `Japan` | `Japan` |
| Germany | `Germany` | `Germany` |
| United States | `United States` | `USA` |
| New Zealand | `New Zealand` | `New Zealand` |

- Áp dụng **fail-fast**: nếu một tên xuất hiện trong file mà không có trong bảng → raise lỗi, không âm thầm bỏ dòng. Đây là cùng kiểu lỗi đã che giấu việc thiếu Singapore.
- Country canonical là khoá nối giữa hai CSV và với ADR-004.

### D.5. Encoding và định dạng output

- **UTF-8, không BOM**, line ending LF.
- Cột theo đúng thứ tự schema ở D.2/D.3; không có cột index.
- Sort: `country, year, sector` (emissions) và `country, year, parameter` (ev).
- Float format: Python default `repr` của pandas (`to_csv` mặc định), không làm tròn — làm tròn là việc của phân tích.
- Missing value: để trống (pandas ghi `""`), không ghi `NA`/`0`/`NaN` literal.

### D.6. Xác thực và provenance

- **Input hash.** So sánh SHA-256 của hai `.xlsx` với pin ở ADR-002 D.1/D.2; lệch → dừng.
- **Row count.** `emissions_long.csv`: đúng 64 dòng (8 × 8). `ev_long.csv`: số dòng = tổng coverage IEA của 7 nước (Singapore = 0).
- **Country coverage.** emissions: đủ 8 nước. ev: đủ 7 nước (không có Singapore).
- **Sector coverage.** Mỗi nước trong emissions có đúng 8 sector, không trùng, không thiếu.
- **Missing-value check.** emissions không có NaN trong `emissions_mt`; ev được phép có NaN ở `value` (IEA làm tròn / lỗ hổng năm) nhưng phải log số lượng.
- **Output hash.** In SHA-256 của hai CSV vào log của script; không commit CSV (bị `data/*` gitignore).
- **Fail on any mismatch.** Không "cảnh báo rồi tiếp tục".

## Alternatives Considered

- **A.1. Convert bằng Excel macro / Power Query.** Loại: phụ thuộc GUI, không tái lập được trên máy khác, khó review trong PR.
- **A.2. Convert bằng R (`readxl`).** Loại: thêm toolchain; nhóm đang dùng Python và env đã có openpyxl.
- **A.3. Đọc `.xlsx` trực tiếp trong notebook.** Loại: chậm, bộ lọc rải rác ở nhiều cell, dễ lệch giữa các notebook; ADR-003 muốn một nguồn sự thật.
- **A.4. Output wide (mỗi sector một cột).** Loại: khó ghép hai nguồn, khó kiểm tra; long là chuẩn tidy và khớp với `groupby` của Q1/Q3.
- **A.5. Bỏ cột `year` vì EDGAR chỉ có 2025.** Loại: mất khả năng mở rộng khi có EDGAR 2027; giữ cột chi phí không đáng kể.
- **A.6. Điền 0 cho Singapore / năm thiếu của Việt Nam.** Loại: fabricate dữ liệu, vi phạm ràng buộc Context; để trống và xử lý tường minh ở notebook.

## Consequences

- **C.1. `data/processed/` bị gitignore** (`data/*`). ADR-003 + hash output là bản ghi bền vững; clone repo phải chạy `prepare_data.py` sau khi tải `.xlsx` và kiểm hash input.
- **C.2. Không thay đổi env.** openpyxl 3.1.2 đã có; không cần sửa `min_ds-env.yml` cho ADR này (ADR-007 sẽ thêm statsmodels v.v.).
- **C.3. Notebook chỉ đọc CSV.** Mọi thay đổi schema phải sửa ADR-003 trước, theo authority rule.
- **C.4. Singapore và các năm thiếu của Việt Nam** phải được xử lý tường minh ở Q1/Q2/Q3 (loại khỏi mô hình và báo cáo rõ), không âm thầm bỏ dòng.
- **C.5. Thêm `prepare_data.py` là bước tiếp theo** (ngoài phạm vi ADR này). Khi viết script, phải khớp schema và kiểm tra ở D.6; nếu lệch → sửa ADR-003 trước.

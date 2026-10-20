# ADR-004: Pin the countries and their analytical roles

## Status

Proposed

## Date

2026-10-19

## Context

- Vì sao lại chọn ra một số quốc gia làm mẫu: M1 khớp mô hình diffusion cho mỗi quốc gia; M2 so sánh giữa các quốc gia;
M3 so sánh quá trình chuyển đổi sang xe điện với chính lượng phát thải của quốc gia đó.
- Các mẫu cần được cố định hoàn toàn trước file `SPECIFICATION.md`, để việc chọn quốc gia không dựa trên kết quả thu được.
- Cơ sở:
    - `EDGAR_2026_GHG_booklet_2026.xlsx` cho cấu trúc sector (?)
    - `EV Data Explorer 2025.xlsx` cho chuyển đổi EV và sạc năng lượng.

## Decision

### Các quốc gia được lựa chọn

| # | Quốc gia | Vai trò | EDGAR name | IEA key |
| --- | --- | --- | --- | --- |
| 1 | Vietnam | Cơ sở | Viet Nam | Viet Nam |
| 2 | Thailand | Quốc gia ĐNA gần nhất để so sánh | Thailand | Thailand |
| 3 | Singapore | Quốc gia ĐNA giàu có | Singapore | _absent_ |
| 4 | China | Trường hợp irony | China | China |
| 5 | Japan | Quốc gia phát triển ở ĐNA | Japan | Japan |
| 6 | Germany | Đại diện EU | Germany | Germany |
| 7 | United States | Benchmark phương Tây | United States | USA |
| 8 | New Zealand | Trường hợp tốt nhất | New Zealand | New Zealand |

Cơ sở của từng vai trò, dựa trên Bảng 1 và Bảng 2:

- **Cơ sở (Vietnam)** - nước gốc của câu hỏi chính sách; `2 and 3 wheelers` có 11 năm liên tục.
- **ĐNA gần nhất để so sánh (Thailand)** - cùng khu vực, nhưng transport share 30.3% so với 13.1%
  của Việt Nam: chênh 2.3 lần, và dữ liệu đầy đủ 15 năm.
- **ĐNA giàu có (Singapore)** - transport share 10.0%, thấp thứ hai trong mẫu; tương phản với Việt Nam.
- **Trường hợp irony (China)** - transport share thấp nhất mẫu (8.3%) nhưng là nước phát thải lớn
  nhất (13,057 Mt) và áp lực chuyển đổi lớn nhất. Chỉ "irony" ở chỗ tỉ lệ so với quy mô.
- **ĐNA phát triển (Japan)** - transport share 18.4%, dữ liệu đầy đủ nhất mẫu (15 năm sạc).
- **Đại diện EU (Germany)** - nền kinh tả lớn nhất EU trong mẫu (567.8 Mt CO₂).
- **Benchmark phương Tây (United States)** - 36.4% transport share, 15 năm dữ liệu, và là nước
  duy nhất có sự kiện Clean Vehicle Credits cho event study của M2 (ADR-006).
- **Trường hợp tốt nhất (New Zealand)** - transport share cao nhất mẫu (52.7%), tức nền tảng phát
  thải lớn nhất để đo tác động của điện xe hoá.

### Cấu trúc phát thải theo sector (EDGAR)

Cách tính: chỉ lọc `Substance = CO2`, **năm 2025**; mẫu số là tổng của cả 8 sector (không gồm LULUCF); `Industry = Industrial Combustion + Processes`; `Power = Power Industry`.

Cột "Tổng CO₂" là tổng 8 sector, đơn vị Mt.

| Quốc gia | Transport % | Industry % | Power % | Tổng CO₂ 2025 (Mt) |
| --- | --- | --- | --- | --- |
| Vietnam | 13.1 | 35.6 | 46.0 | 387.0 |
| Thailand | 30.3 | 27.3 | 30.6 | 266.9 |
| Singapore | 10.0 | 41.7 | 39.5 | 57.1 |
| China | 8.3 | 30.7 | 50.3 | 13,057.1 |
| Japan | 18.4 | 21.6 | 44.9 | 977.3 |
| Germany | 24.1 | 20.4 | 31.4 | 567.8 |
| United States | 36.4 | 13.0 | 33.0 | 4,739.1 |
| New Zealand | 52.7 | 21.2 | 11.9 | 29.2 |

Nguồn: `data/EDGAR_2026_GHG_booklet_2026.xlsx`, sheet `GHG_by_sector_and_country`.

> **Lưu ý về vai trò của China và New Zealand.** Câu "New Zealand và China bracket the range
> (52.7% và 8.3%)" trong pre-registration chỉ đúng **trong phạm vi pool hợp lệ** (29 quốc gia
> ở A.1), không đúng trên toàn bộ các nước có dữ liệu: nới tiêu chí điểm sạc thì Costa Rica
> (66.8%) vượt New Zealand, còn ở ngưỡng ≥ 12 năm điểm sạc thì China rơi khỏi pool. Trên toàn
> bộ 171 nước có phát thải đáng kể, 16 nước có transport share cao hơn New Zealand. Vì vậy
> `SPECIFICATION.md` phải ghi rõ đây là khoảng bao phủ **của pool hợp lệ**, không phải toàn cầu.

### Độ phủ dữ liệu EV (IEA)

"Năm (n)" là các năm có dữ liệu liên tục; nếu có lỗ hổng thì ghi rõ.

Cột "Điểm sạc 2024" là tổng `Publicly available fast` + `Publicly available slow`.

| Quốc gia | EV sales share (cars) | EV stock share (cars) | Điểm sạc công cộng | Điểm sạc 2024 | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| Vietnam | 2018, 2021–2024 (5) | 2018–2024 (7) | 2023–2024 (2) | 6,100 | thiếu 2019–2020; sạc chỉ 2 năm |
| Thailand | 2010–2024 (15) | 2010–2024 (15) | 2017–2024 (8) | 13,400 | đầy đủ |
| Singapore | — | — | — | — | **không có trong file** |
| China | 2010–2024 (15) | 2010–2024 (15) | 2014–2024 (11) | 3,500,000 | đầy đủ |
| Japan | 2010–2024 (15) | 2010–2024 (15) | 2010–2024 (15) | 34,000 | đầy đủ |
| Germany | 2010–2024 (15) | 2010–2024 (15) | 2012–2024 (13) | 157,000 | đầy đủ |
| United States | 2010–2024 (15) | 2010–2024 (15) | 2010–2024 (15) | 193,000 | đầy đủ |
| New Zealand | 2010–2024 (15) | 2010–2024 (15) | 2017–2024 (8) | 1,440 | đầy đủ |

Nguồn: `data/EV Data Explorer 2025.xlsx`, sheet `GEVO_EV_2025`, `category = Historical`, `powertrain = EV`.

Một số điều lưu ý:

- **Singapore không tồn tại trong file IEA.** - Không có bất kỳ entry nào của Singapore xuất hiện. Do đó mà Singapore chỉ có thể được dùng cho M3, không dùng cho M1/M2.
- **Series `cars` của Vietnam mỏng hơn series `2 and 3 wheelers.`** - `cars` có 5 năm rời rạc (2018, 2021-2024), `2 and 3 wheelers` có 11 năm liên tục (2014-2024) cho cả sales share và stock share.
- **Điểm sạc của Vietnam chỉ có 2 năm (2023-2024).** - Nếu M2 sử dụng charging density làm biến hồi quy thì VN không đóng góp được gì. Thiết kế event study theo Clean Vehicle Credits của M2 không cần dữ liệu này.

## Alternatives Considered

Chỉ những phương án thay đổi mẫu nghiên cứu hoặc thay đổi kết luận mới được liệt kê.

### A.1. Ngưỡng dữ liệu và pool hợp lệ

Trong 54 quốc gia có trong file IEA, chỉ **29** thoả ba điều kiện tối thiểu: sales share và
stock share (cars) **liên tục**, và **≥ 8 năm** có điểm sạc công cộng. 25 quốc gia còn lại bị
loại vì lý do kỹ thuật, không phải vì vai trò phân tích:

| Lý do loại | Quốc gia bị loại |
| --- | --- |
| Không có stock share (cars) | Bulgaria, Croatia, Cyprus, Czech Republic, Estonia, Hungary, Ireland, Latvia, Lithuania, Luxembourg, Romania, Seychelles, Slovakia, Slovenia |
| Có lỗ hổng năm (sales share) | Indonesia, Lithuania, Russia, **Viet Nam** |
| Điểm sạc < 8 năm | Austria (6), Brazil (7), Colombia (4), Costa Rica (4), Indonesia (4), Israel (3), Jordan (4), Malaysia (4), Russia (4), Uzbekistan (0), **Viet Nam (2)** |

### A.2. Singapore — vì sao vẫn giữ trong mẫu dù không có dữ liệu IEA

Đây là phương án thay thế có ảnh hưởng lớn nhất, vì Singapore là quốc gia duy nhất trong mẫu
không thể tham gia M1/M2.

| Phương án | Đánh giá |
| --- | --- |
| **Giữ Singapore, dùng cho M3** (đã chọn) | M3 chỉ cần EDGAR — Singapore có đủ. Giữ được vai trò "ĐNA giàu có" và transport share thấp (10.0%). Đánh đổi: không đóng góp cho M1/M2. |
| Thay bằng Malaysia | Chỉ 4 năm điểm sạc (A.1); `2 and 3 wheelers` rất yếu (0.64% năm 2024), mất đối trọng với Việt Nam (9.4%). |
| Thay bằng Indonesia | `cars` bị lỗ hổng, stock share chỉ từ 2019 (A.1). |
| Bỏ Singapore, giữ 7 nước | Mất vai trò "ĐNA giàu có" và đầu dưới của dải transport share; mẫu nghiêng hẳn về nước có transport share cao. |
| Lấy từ bản IEA mới hơn | OWID (GEVO 2026) có Singapore 2016–2025, nhưng mẫu sẽ trộn hai phiên bản — làm yếu tính đồng nhất. **Không chọn.** |

### A.3. Các quốc gia trong pool hợp lệ nhưng không được chọn

Tám quốc gia được chọn không phải vì có dữ liệu tốt nhất, mà vì **vai trò phân tích**.
21 quốc gia còn lại trong pool bị loại vì lý do nội tại:

| Quốc gia (transport % CO₂) | Vì sao không chọn |
| --- | --- |
| India (11.5), South Africa (11.7) | Trùng vị trí "transport share thấp" của China. |
| South Korea (16.6) | Trùng vị trí "ĐNA phát triển" của Nhật Bản. |
| Netherlands (19.4), Poland (25.1), Belgium (27.1), France (43.6), Italy (36.2), Spain (41.3), UK (36.7), Sweden (43.4), Denmark (43.0), Finland (30.6), Greece (36.0) | Trùng vị trí "đại diện EU" của Đức. |
| Canada (28.9), Mexico (30.0), Australia (27.0), Chile (36.6) | Trùng vị trí "benchmark phương Tây" của Hoa Kỳ. |
| Norway (30.2) | 92% xe mới bán điện năm 2024 (file IEA), nhưng power chỉ chiếm **4.1%** CO₂ — điện đã sạch nên điện xe hoá ít tác động, làm M3 mất ý nghĩa. Giữ làm so sánh định tính. |
| Turkey (21.3) | Nằm giữa Đông Á và ĐNA, không khớp vai trò nào. |

### A.4. Các quy tắc chọn mẫu khác đã cân nhắc

| Quy tắc | Vì sao không dùng |
| --- | --- |
| Ngẫu nhiên từ 29 nước hợp lệ | Không bảo đảm có Việt Nam (trường hợp cơ sở) hay phủ được dải transport share. Với n = 8, mất kiểm soát tổng phân bổ. |
| Theo thứ hạng phát thải | Mẫu toàn nước lớn: trung quyền hệ số CO₂, M3 không phân biệt được "nhỏ hay lớn". Cũng loại New Zealand (29.2 Mt) — mất trường hợp transport share cao nhất. |
| Toàn bộ 29 nước hợp lệ | M1 khớp diffusion + bootstrap 10.000 lần cho 29 nước là 29 đường cong; M3 cần cấu trúc sector từng nước. n = 8 là giới hạn thực tế của phương pháp. |
| Theo mức thu nhập | 8 nước đều thu nhập trung bình-cao, mất Việt Nam — chính là lý do chính sách của dự án. |
| Toàn bộ ASEAN 10 | 5 nước (Philippines, Cambodia, Laos, Myanmar, Brunei) không có dữ liệu EV nào; Singapore không có trong file IEA. Thiếu dữ liệu quá nhiều để chọn theo nguyên tắc. |

## Consequences

- Với mỗi quá trình phân tích, kích thước về mẫu của các quốc gia sẽ bị thay đổi. M1 và M2 dựa trên 7 quốc gia và M3 sẽ dựa trên cả 8 quốc gia. Khi đó, kích thước của mẫu phải được làm rõ trong file spec hoặc notebook.
- Khối lượng dữ liệu của Vietnam bị suy giảm trong 2 đến 3 module mà nó sở hữu. Series `cars` bị trống 5 năm, khá mỏng cho M1. Dữ liệu các điểm sạc chỉ trong 2 năm, khó đóng góp cho M2. Tuy nhiên, series `2 and 3 wheelers` lại cực kỳ nhiều và khá rộng trong file với 11 năm liên tiếp - đó là mốt cho chính sách ban xe máy sử dụng nhiên liệu hóa thạch. Nếu M1 chỉ gồm xe hơi, Vietnam có thể bị loại khỏi kết quả và quyết định trên nằm trong file spec.
- Các bảng số liệu dùng EDGAR 2025, nhưng 2025 mới là bản sơ bộ (Fast Track) còn 2024 là bản cuối. Ở New Zealand, transport share dịch 2.6 điểm phần trăm giữa hai năm. Spec cần chốt rõ năm nào là năm chính và năm nào là kiểm tra độ nhạy.
- IEA làm tròn hai chữ số có ý nghĩa. Ở các giá trị nhỏ như của Vietnam (0.0016% năm 2018, 0.041% năm 2021), độ chính xác này giới hạn ý nghĩa của bootstrap CI, nên ngưỡng so sánh cho M1 phải tính đến sàn làm tròn.
- Tên quốc gia giữa hai file khác nhau: EDGAR dùng `Viet Nam` / `United States` / `South Korea` / `Türkiye`, IEA dùng `Viet Nam` / `USA` / `Korea` / `Turkiye`. `prepare_data.py` cần bảng ánh xạ tường minh, nếu không sẽ âm thầm bỏ mất dòng - cùng kiểu lỗi đã che giấu việc thiếu Singapore.
- Hai file xlsx đều bị gitignore nên không được commit. Bảng 1 và Bảng 2 trong ADR này là bản ghi bền vững của số liệu. Muốn thay đổi mẫu sau này thì phải viết ADR mới thay thế ADR này, không sửa tại chỗ.

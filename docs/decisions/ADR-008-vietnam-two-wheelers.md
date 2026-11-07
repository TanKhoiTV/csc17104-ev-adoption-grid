# ADR-008: Q4 — chuyển đổi xe hai bánh ở Việt Nam và phần CO₂ tránh được

## Status

Proposed

## Date

2026-11-07

## Context

ADR-004 đặt Việt Nam ở vai trò #1, **cơ sở** của câu hỏi chính sách. Nhưng dữ liệu của Việt Nam hẹp hơn
mọi quốc gia còn lại trong mẫu:

| Chuỗi | Số năm | Ghi chú |
| --- | --- | --- |
| `cars` — EV sales share | **5** (2018, 2021–2024) | thiếu 2019–2020 |
| `cars` — EV stock share | 7 (2018–2024) | liên tục |
| `2 and 3 wheelers` — sales & stock share | **11** (2014–2024) | liên tục |
| Điểm sạc công cộng | **2** (2023–2024) | 6.100 điểm năm 2024 |

Kiểm chứng ngày 2026-11-07 trên `data/EV Data Explorer 2025.xlsx`
(SHA-256 `309C6342…`, khớp ADR-002 D.2), `category = Historical`, `powertrain = EV`.

Bốn dữ kiện quyết định nội dung ADR này:

- **Chuỗi `2 and 3 wheelers` không phải của riêng Việt Nam.** Nó có cho cả 7 nước trong mẫu IEA:
  Thái Lan 2010–2024 (15), New Zealand 2010–2024 (15), Trung Quốc 2012–2024 (13), Đức 2012–2024 (13),
  Mỹ 2012–2024 (13), Việt Nam 2014–2024 (11), Nhật 2018–2024 (7).
- **Nhưng chất lượng tín hiệu thì khác nhau rõ rệt.** Trên `2 and 3 wheelers`, 4/7 chuỗi phẳng hoặc đảo chiều:
  Đức 0,28 → 15,0 (2022) → 3,6; New Zealand 0,098 → 8,0 (2023) → 3,9; Trung Quốc 13 → 55 (2021) → 46;
  Mỹ 0,099 → 1,7 gần như phẳng; Thái Lan 0,0004 → 1,2 gần như phẳng. Trên `cars`, 6 nước còn lại đều
  là đường S gần đơn điệu.
- **Việt Nam không vào được Q2 (ML).** Q2 chia train ≤ 2020 và dùng biến trễ 1 năm; Việt Nam trên `cars`
  chỉ có 2018 trước 2021, mà 2018 cần lag 2017 (không tồn tại) ⇒ **0 dòng huấn luyện**. Trên `2 and 3 wheelers`
  thì Việt Nam có 6 dòng huấn luyện, nhưng khi đó biến mục tiêu của mô hình gộp sẽ khác nghĩa giữa các nước.
- **Việt Nam không vào được Q3** vì chỉ có 2 năm dữ liệu sạc (ADR-006 D.6).

Vì vậy cần một chỗ đứng riêng cho Việt Nam: một câu hỏi **mô tả**, dùng đúng phần dữ liệu mà Việt Nam có
nhiều nhất, và nói rõ giới hạn của nó.

## Decision

### D.1. Câu hỏi

**Chuyển đổi xe điện ở Việt Nam có thực sự là câu chuyện xe hai bánh không, và nếu vậy thì phần CO₂
tránh được nằm trong khoảng nào?**

Đây là **Q4** trong bốn câu hỏi đã chốt ở ADR-001, giữ nguyên số thứ tự vì nó là câu cuối trong mạch tự sự:
sau khi đã biết cấu trúc phát thải (Q1), tốc độ và khả năng dự báo (Q2), và vai trò của hạ tầng sạc (Q3).

### D.2. Q4 là câu hỏi mô tả, không phải nhân quả

Không có nhóm đối chứng, không có biến công cụ, không có cú sốc ngoại sinh. Q4 **mô tả** cấu trúc chuyển đổi
và đặt ra một **cận/dải** cho phần phát thải tránh được. Mọi câu chữ trong notebook phải giữ đúng mức đó:
"nằm trong khoảng", không phải "tác động là".

### D.3. Chuỗi chính

`2 and 3 wheelers` (sales share + stock share, 2014–2024) là chuỗi chính; `cars` chỉ dùng để **đối chiếu**
(2018, 2021–2024). Khoảng trống 2019–2020 của `cars` phải được vẽ ra, không được nội suy.

### D.4. Estimand: một dải, không phải một điểm

Công thức:

```
CO₂ tránh được = CO₂ giao thông
               × tỉ trọng xe hai bánh trong vận tải đường bộ
               × mức điện khí hoá đội xe hai bánh
               × (1 − cường độ phát thải của EV hai bánh / cường độ phát thải của xe hai bánh ICE)
```

Ba quy tắc bắt buộc:

- **Báo cáo dạng dải** theo các giả định cường độ lưới (thấp / trung bình / cao), không báo một số duy nhất.
  Hệ số thứ tư là chỗ lưới điện đi vào Q4 mà không cần một câu hỏi riêng (ADR-001, phạm vi).
- **Ghi rõ đâu là dữ liệu, đâu là giả định.** Tử số thứ nhất và thứ hai đến từ EDGAR và IEA; mức điện khí hoá
  là dữ liệu IEA; tỉ lệ cường độ phát thải là **giả định có trích dẫn**, và phải nằm trong dải độ nhạy.
- **Cận trên không phải kết quả nhân hai số.** `tổng CO₂ × 13,1% × 100%` chỉ là kích thước ngành giao thông,
  không phải phát thải tránh được, vì nó bỏ qua mức điện khí hoá đã đạt và bỏ qua việc EV vẫn phát thải
  theo lưới. Phương án này bị loại ở A.4.

### D.5. Hoà giải với Q2 — điểm mâu thuẫn trước đây

Trước ADR này, issue #17 và issue #21 mâu thuẫn nhau: #21 nói "dùng `2 and 3 wheelers` cho Việt Nam"
trong câu hỏi ML, #17 lại nói M1 phải dùng chuỗi hai bánh cho Việt Nam. **Quyết định dứt điểm:**

- **Q2 giữ `cars`, 6 quốc gia, loại Việt Nam**, và báo cáo lý do loại (0 dòng huấn luyện sau lag) theo đúng
  kỷ luật của ADR-006 D.6.
- **Việt Nam vào Q1** như một quan sát trong kiểm định chéo quốc gia. Tốc độ dùng **`cars` với hai mốc 2018
  (0,0016%) và 2024 (17,0%)**, để biến mục tiêu của Q1 đồng nhất định nghĩa với 6 nước còn lại — nếu dùng
  `2 and 3 wheelers` cho riêng Việt Nam thì Q1 lặp lại đúng lỗi định nghĩa mà D.5 vừa loại bỏ ở Q2.
  `2 and 3 wheelers` chỉ dùng ở phần độ vững của Q1 và ở Q4.
- Không còn câu nào yêu cầu Việt Nam phải có chuỗi `cars` dài.

### D.6. Độ sâu

D1 (ghép IEA × EDGAR), D3 (biến dẫn xuất: tỉ trọng hai bánh, mức điện khí hoá, dải CO₂), D6 (độ nhạy theo
giả định lưới và theo cửa sổ thời gian). Q4 là câu phi-ML nên cần ≥ 2 tiêu chí; ba tiêu chí trên là đủ,
và D5 (bootstrap) là tuỳ chọn.

## Alternatives Considered

- **A.1. Dùng `2 and 3 wheelers` làm biến mục tiêu của Q2 cho cả 7 quốc gia.** Khả thi về dữ liệu — chuỗi có
  cho cả 7 nước — nhưng **loại**: 4/7 chuỗi phẳng hoặc đảo chiều, biến mục tiêu trải từ 0,0004% đến 55%,
  nên mô hình gộp sẽ học "nước nào" chứ không học "đang ở đâu trên đường cong diffusion". Đổi lại, `cars`
  cho 6 chuỗi gần đơn điệu.
- **A.2. Đưa Việt Nam vào Q2 trên `cars`.** **Loại**: 0 dòng huấn luyện sau lag (xem Context). Không phải
  lựa chọn về phương pháp mà là bất khả thi về dữ liệu.
- **A.3. Bỏ Việt Nam khỏi dự án.** **Loại**: mất trường hợp chính sách mà ADR-001 và ADR-004 tổ chức quanh nó.
- **A.4. Giữ công thức cận trên dạng một điểm: tổng CO₂ × 13,1% × 100%.** **Loại**: chỉ là phép nhân hai số
  công bố, rơi vào loại "không đủ độ sâu" của đề bài, và bỏ qua cường độ lưới — tức bỏ qua đúng phần làm
  câu hỏi này có ý nghĩa.
- **A.5. Dùng nguồn đăng ký xe máy của Việt Nam để có mẫu số thật.** **Loại (hoãn)**: cần một nguồn mới, phải
  ghi giấy phép/cách truy cập/ngày tải theo ADR-002 D.7, và thời gian còn lại (hạn 29/11) không đủ. Ghi vào
  future work — nếu có, dải sẽ hẹp lại đáng kể.

## Consequences

- **C.1. Q4 mô tả.** Kết luận là một dải, không phải một hệ số nhân quả. Câu chữ trong notebook và slide phải
  giữ đúng mức này.
- **C.2. Việt Nam không tham gia Q2 và Q3.** Hệ quả trực tiếp của dữ liệu; đã ghi ở ADR-001 C.2 và phải xuất
  hiện sớm trong báo cáo, không để người đọc tự phát hiện.
- **C.3. Giả định cường độ lưới phải hiện ra trong notebook**, kèm bảng độ nhạy. Đây là chỗ duy nhất "lưới điện"
  xuất hiện trong dự án ngoài biến kiểm soát ở Q1.
- **C.4. `SPECIFICATION.md` kế thừa D.4 và D.5**, không viết lại; nếu sau này đổi dải giả định thì phải sửa
  ADR này, không sửa tại chỗ trong notebook.
- **C.5. Dữ liệu của Việt Nam bị dùng hai lần cho hai mục đích khác nhau** (Q1: một quan sát chéo quốc gia;
  Q4: phân tích một nước). Notebook phải nói rõ để không ai coi đó là hai nguồn độc lập.

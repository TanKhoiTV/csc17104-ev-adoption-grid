# Nhật ký quyết định kiến trúc (ADR)

Mỗi quyết định lớn về dữ liệu, phương pháp hoặc quy trình được ghi thành một ADR **trước** khi code tương ứng
được viết. Thứ tự thẩm quyền của repo: **ADR > `SPECIFICATION.md` > notebook**. Nếu code mâu thuẫn với ADR,
sửa code — hoặc sửa ADR trước, kèm lý do.

Quy ước nội dung: `Context → Decision → Alternatives Considered → Consequences`, có `Status` và `Date`.
ADR viết bằng tiếng Việt (xem `CONTRIBUTING.md`).

## Danh mục

| ADR | Tiêu đề | Trạng thái | File |
| --- | --- | --- | --- |
| ADR-001 | Chốt chủ đề nghiên cứu | Đề xuất | [`ADR-001-research-topic.md`](decisions/ADR-001-research-topic.md) |
| ADR-002 | Chốt bộ dữ liệu | Đề xuất | [`ADR-002-dataset.md`](decisions/ADR-002-dataset.md) |
| ADR-003 | Phương pháp chuyển đổi file CSV/XLSX | Đề xuất | [`ADR-003-conversion-method-for-csv-files.md`](decisions/ADR-003-conversion-method-for-csv-files.md) |
| ADR-004 | Chốt các quốc gia và vai trò phân tích của chúng | Đề xuất | [`ADR-004-country-sample.md`](decisions/ADR-004-country-sample.md) |
| ADR-005 | Chốt mô hình cộng tác: branch, merge và review | Đề xuất | [`ADR-005-collaboration-model.md`](decisions/ADR-005-collaboration-model.md) |
| ADR-006 | Chiến lược nhận dạng cho Q3 | Đề xuất | [`ADR-006-m2-identification.md`](decisions/ADR-006-m2-identification.md) |
| ADR-007 | Môi trường làm việc cho repo | Đề xuất | [`ADR-007-working-env.md`](decisions/ADR-007-working-env.md) |
| ADR-008 | Q4 — chuyển đổi xe hai bánh ở Việt Nam và phần CO₂ tránh được | Đề xuất | [`ADR-008-vietnam-two-wheelers.md`](decisions/ADR-008-vietnam-two-wheelers.md) |

## Đọc theo nhu cầu

| Bạn cần biết | Đọc |
| --- | --- |
| Dữ liệu lấy từ đâu, giấy phép nào, hash nào | ADR-002 |
| Vì sao 8 quốc gia, mỗi nước giữ vai trò gì | ADR-004 |
| `.xlsx` được chuyển thành CSV theo quy tắc nào | ADR-003 |
| Q3 nhận dạng nhân quả ra sao | ADR-006 |
| Cài môi trường, pin version | ADR-007 |
| Q4 đo cái gì và dải CO₂ được dựng thế nào | ADR-008 |
| Quy trình branch/merge/review | ADR-005 |

## Ghi chú về cột Trạng thái

Cả tám ADR hiện vẫn ghi `Đề xuất`, kể cả những ADR đã được hiện thực và đang có hiệu lực
(ADR-001, ADR-002, ADR-003, ADR-004, ADR-008). Cột này phản ánh **văn bản trong từng file**, không phải
đánh giá của người viết index: chưa có lượt cập nhật trạng thái nào sau khi merge.

Nếu nhóm muốn, một PR riêng có thể chuyển các ADR đã hiện thực sang `Đã chấp nhận` — nhưng đó là thay đổi
nội dung ADR, nên phải làm sau khi cả hai thành viên đồng ý, không gộp vào PR tài liệu này.

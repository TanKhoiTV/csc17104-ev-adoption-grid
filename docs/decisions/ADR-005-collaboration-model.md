# ADR-005: Chốt mô hình cộng tác: branch, merge và review

## Context

- Nhóm gồm 2 thành viên, cùng repo, deadline 29/11. Cần quy ước branch, merge strategy, review process để tránh conflict và giữ attribution cá nhân (brief cho phép điểm cá nhân khá nhau dựa trên Git history và Q&A).
- Đã có 10 ADR/issue đang mở song song; cần thứ tự merge rõ ràng.

## Decision

- D.1. Branch naming. `khoi/<topic>` và `dat/<topic>`, tách từ `main` mới nhất. Tên topic ngắn, kebab-case, khớp issue (vd. `dat/adr-004-conversion-method`). Không commit thẳng vào `main`.
- D.2. Merge strategy: merge commits, không rebase/squash. Giữ từng commit của tác giả để Git history phản ánh đúng ai làm gì; squash làm mất granularity, rebase làm mất timestamp và attribution.
- D.3. Review gate. PR phải được thành viên còn lại review trước khi merge. Reviewer đặt `CHANGES_REQUESTED` với inline comments; tác giả fix bằng commit mới (không force-push) rồi re-request review. Không self-merge.
- D.4. Thứ tự merge. ADRs -> data layer (ADR-003 + `prepare_data.py`) -> analysis (Q1/Q3/Q4) -> ML (Q2) -> integration (notebook + slide). Lý do: downstream phụ thuộc upstream; merge ngược thứ tự gây conflict hàng loại.
- D.5. Review checklist. Trước khi approve: (1) chạy notebook end-to-end trên máy sạch; (2) in cỡ mẫu trước/sau mỗi bước lọc/gộp và đối chiếu SPECIFICATION.md §2; (3) verify plot có tiêu đề, đơn vị, chú giải; (4) verify input hash khớp ADR-002; (5) không còn M-term stray (grep M[1-3] sạch, trừ parenthetical giải thích).
- D.6. Attribution. Mỗi ADR/issue do một người sở hữu; thành viên còn lại review. Khi cần viết tay (vd. Dat bận), phải ghi rõ trong PR body và issue được reassign.

## Alternatives Considered

- A.1. Rebase merge - mất granularity commit, khó trace được ai làm gì. Loại.
- A.2. Squash merge - gộp thành 1 commit, mất lịch sử chi tiết. Loại.
- A.3. Trunk-based (commit thẳng main) - không có review gate. Loại.
- A.4. Branch theo câu hỏi (q1/, q2/) thay vì theo người thực hiện - khó attribute. Loại.

## Consequences

- C.1. History không linear nhưng attribution rõ ràng.
- C.2. PR phải đủ nhỏ để review; ADR lớn (như ADR-004) chấp nhập làm 1 PR vì là 1 quyết định.
- C.3. Trước khi branch mới phải `git pull origin main`.
- C.4. Review checklist là gate; không merge khi checklist chưa pass.
- C.5. Conflict resolution: rebase local branch onto main, không force-push vào remote.

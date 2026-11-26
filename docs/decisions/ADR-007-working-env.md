# ADR-007: Môi trường làm việc cho repo

## Status

Đề xuất

## Date

2026-11-10

## Context

- Repo cần có môi trường tái lập: cùng OS/Python/package version -> cùng kết quả.
- `environment.yml` hiện tại (Lab00 base) có Python 3.11.5, pandas 2.1.1, openpyxl 3.1.2, scikit-learn, matplotlib, seaborn, plotly, requests, selenium - nhưng thiếu **statsmodels, linearmodels, pyfixest** (ADR-006 D.9).
- Q2 (ML) cần scikit-learn (đã có) + statsmodels (kiểm định, bootstrap). Q3 (panel FE) cần linearmodels + wild cluster bootstrap (pyfixest hoặc wildboottest).
- Ràng buộc phụ thuộc: pyfixest 0.60 khai báo `seaborn >=0.13.2`, trong khi Lab00 pin `seaborn=0.13.0`. Không bump thì `conda env create/update` sẽ fail ngay khi solve. Hai gói còn lại không đụng pin hiện có: statsmodels 0.14 và linearmodels 6.1 chấp nhận numpy 1.26.0 / pandas 2.1.1 / scipy 1.11.3.

## Decision

- D.1. Kênh và Python. Giữ conda-forge + defaults, Python 3.11.5 (đã chốt). Không hạ xuống 3.10 dù một số gói cũ hơn hỗ trợ tốt hơn — 3.11.5 đủ cho tất cả gói cần.
- D.2. Bổ sung 3 gói vào `environment.yml`, pin `major.minor` theo D.4:
    - `statsmodels=0.14` (OLS, bootstrap, kiểm định)
    - `linearmodels=6.1` (PanelOLS, fixed effect)
    - `pyfixest=0.60` (wild cluster bootstrap; thay thế wildboottest vì API gọn hơn và hỗ trợ Python 3.11)
    - Kèm một thay đổi bắt buộc: `seaborn` 0.13.0 → **0.13.2**, vì pyfixest 0.60 yêu cầu `seaborn >=0.13.2`.
- D.3. Setup steps. `conda env create -f environment.yml` -> `conda activate min_ds-env` -> đăng ký Jupyter kernel (`python -m ipykernel install --user --name min_ds`). Ghi trong README (khi README được điền).
- D.4. Version pinning. Pin `major.minor` cho core (python, pandas, numpy, scikit-learn, statsmodels, linearmodels, pyfixest); patch để conda resolve. Lý do: reproducibility mà không lock quá chặt (tránh conflict khi conda solve).
- D.5. Kiểm tra môi trường. Script `check_env.py` (hoặc cell đầu notebook) in version của pandas, numpy, statsmodels, linearmodels, pyfixest; fail nếu thiếu.

## Alternatives Considered

- A.1. `requirements.txt` (pip-only). Loại. Compiled deps (numpy, scipy, openpyxl) cài pip trên Windows/WSL không ổn định; conda giải quyết binary tốt hơn.
- A.2. Docker. Loại: overkill cho đồ án 2 người, deadline 29/11; thêm overhead không cần thiết.
- A.3. Không pin version. Loại: phá vỡ tái lập; "chạy được trên máy tôi" không đủ.
- A.4. wildboottest thay pyfixest. Loại: pyfixest API gọn hơn, hỗ trợ Python 3.11 tốt hơn, và cùng tác giả với fixest - quen thuộc nếu cần cross-check.

## Consequences

- C.1. `environment.yml` tăng ~3 package; thời gian conda env create tăng ~2-3 phút.
- C.2. Sau khi pull, cả hai phải `conda env update -f environment.yml` (hoặc tạo lại env) để có gói mới.
- C.3. Wild cluster bootstrap chỉ chạy được nếu pyfixest cài đúng; nếu fail, fallback và cluster-robust thông thường với cảnh báo (sức mạnh thống kê thấp, đã ghi ở ADR-006 C.1).
- C.4. Python 3.11.5 là floor; nếu ai đó dùng 3.12+, linearmodels có thể chưa hỗ trợ - ghi rõ thêm trong setup steps.
- C.5. `seaborn` được bump 0.13.0 → 0.13.2 (bắt buộc bởi pyfixest). Đây là thay đổi duy nhất ngoài việc thêm 3 gói; sau `conda env update`, cả hai máy sẽ thấy seaborn 0.13.2.

"""slides/figures.py -- regenerate the four figures used in slides.pdf.

Two kinds of figure, and the difference is stated on purpose:

* **Recomputed** (F1, F4). Derived here from ``data/processed/``, and the script
  *asserts* the published numbers still hold. If a notebook or the pipeline
  changes, this script fails loudly instead of drawing a stale chart.
* **Rendered** (F2, F3). These redraw values the notebooks printed. They are
  pinned rather than recomputed because recomputing them needs ``scikit-learn``
  model fits and ``linearmodels.PanelOLS`` -- neither of which is a dependency
  here, and duplicating those pipelines in a figure script is exactly how a
  slide ends up disagreeing with the notebook it cites.

Run from the repository root::

    python slides/figures.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
OUT = Path(__file__).resolve().parent / "figures"

# --- published values these figures must agree with -------------------------
Q1_RHO = -0.5714                  # 02_analysis.ipynb, Q1 primary
Q4_BAND = (0.4204, 0.6245, 0.8647)  # 02_analysis.ipynb, Q4 2024 band
Q2_PERSISTENCE = 7.2423           # 03_ml_question.ipynb, test RMSE
Q2_BAR = 6.2423                   # SPECIFICATION.md section 5
Q2_TEST = {"pooled / ridge": 9.5196, "dummied / ridge": 9.2175,
           "pooled / hist_gb": 13.6825, "dummied / hist_gb": 13.6748}
Q2_CV_NOTE = "cross-validated RMSE \u2248 1.3 pp (all models)"
Q3_LAG = {"coef": 21.513, "lo": 14.323, "hi": 28.703, "boot_lo": 15.2544, "boot_hi": 27.7714}
Q3_LEAD = {"coef": 13.051, "lo": 7.1292, "hi": 18.973}
Q4_CEILING = (16.17, 33.26)       # 100% electrified two-wheeler fleet, Mt

INK, MUTED, ACCENT, WARN = "#1a1a1a", "#8a9aa5", "#0b3d5c", "#c0392b"

plt.rcParams.update({
    "font.family": "Segoe UI",
    "font.size": 11,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "axes.titlesize": 13,
    "axes.titleweight": "600",
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})


def load() -> tuple[pd.DataFrame, pd.DataFrame]:
    ev = pd.read_csv(PROCESSED / "ev_long.csv")
    em = pd.read_csv(PROCESSED / "emissions_long.csv")
    return ev, em


# ---------------------------------------------------------------- F1: Q1 ----
def f1_q1_scatter(ev: pd.DataFrame, em: pd.DataFrame) -> Path:
    total = em.groupby("country")["emissions_mt"].sum()
    transport = em[em["sector"] == "Transport"].set_index("country")["emissions_mt"]
    share = (transport / total * 100).rename("transport_share")

    sales = ev[(ev["parameter"] == "EV sales share") & (ev["mode"] == "Cars")
               & (ev["powertrain"] == "EV")]
    wide = sales.pivot(index="country", columns="year", values="value")
    pace = (wide[2024] - wide[2018]).rename("pace_pp")

    q1 = pd.concat([share, pace], axis=1).dropna()
    rho, _ = stats.spearmanr(q1["transport_share"], q1["pace_pp"])
    assert round(rho, 4) == Q1_RHO, f"Q1 rho drifted: {rho:.4f} != {Q1_RHO}"

    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    ax.scatter(q1["transport_share"], q1["pace_pp"], s=110, color=ACCENT,
               zorder=3, edgecolor="white", linewidth=1.2)
    for name, row in q1.iterrows():
        dx, dy = (1.6, 0.9)
        if name in {"Vietnam", "Thailand"}:
            dy = -2.2
        ax.annotate(name, (row["transport_share"], row["pace_pp"]),
                    xytext=(dx, dy), textcoords="offset points", fontsize=9, color=INK)

    slope, intercept = np.polyfit(q1["transport_share"], q1["pace_pp"], 1)
    xs = np.linspace(q1["transport_share"].min(), q1["transport_share"].max(), 50)
    ax.plot(xs, slope * xs + intercept, color=WARN, lw=1.6, ls="--", alpha=0.85,
            label="OLS fit (direction only)")

    ax.set_xlabel("Transport share of national CO\u2082 (%)")
    ax.set_ylabel("EV sales share, cars, 2018 \u2192 2024 (pp)")
    ax.set_title("Q1  Transport weight vs adoption pace")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25)
    ax.text(0.02, 0.96, f"Spearman \u03c1 = {rho:.4f}   n = {len(q1)}\n"
                        f"threshold |\u03c1| \u2265 0.7857  \u2192  NOT MET",
            transform=ax.transAxes, va="top", fontsize=9.5, color=INK,
            bbox={"boxstyle": "round,pad=0.45", "fc": "#f4f6f8", "ec": MUTED, "lw": 0.8})

    path = OUT / "f1_q1_scatter.png"
    fig.savefig(path)
    plt.close(fig)
    return path


# ---------------------------------------------------------------- F2: Q2 ----
def f2_q2_rmse() -> Path:
    labels = list(Q2_TEST)
    values = [Q2_TEST[k] for k in labels]

    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    y = np.arange(len(labels))
    colors = [ACCENT if v < Q2_PERSISTENCE else MUTED for v in values]
    ax.barh(y, values, color=colors, height=0.58, zorder=3)
    for yi, v in zip(y, values):
        ax.text(v + 0.18, yi, f"{v:.4f}", va="center", fontsize=9.5, color=INK)

    ax.axvline(Q2_PERSISTENCE, color=INK, lw=1.8, zorder=4)
    ax.text(Q2_PERSISTENCE, len(labels) - 0.35, f"  persistence {Q2_PERSISTENCE:.4f}",
            fontsize=9, color=INK, va="bottom")
    ax.axvline(Q2_BAR, color=WARN, lw=1.4, ls="--", zorder=4)
    ax.text(Q2_BAR, -0.75, f"bar to beat\n{Q2_BAR:.4f}", fontsize=8.5, color=WARN,
            ha="center", va="top")

    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlabel("Test RMSE, EV sales share (percentage points)")
    ax.set_title("Q2  Every model lost to persistence")
    ax.set_xlim(0, max(values) * 1.22)
    ax.grid(axis="x", alpha=0.25)
    ax.text(0.99, 0.04, f"all four test RMSE within [{min(values):.2f}, {max(values):.2f}] pp\n"
                        f"{Q2_CV_NOTE} \u2192 selecting on CV picks the worse model",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8.8, color=INK,
            bbox={"boxstyle": "round,pad=0.45", "fc": "#f4f6f8", "ec": MUTED, "lw": 0.8})

    path = OUT / "f2_q2_rmse.png"
    fig.savefig(path)
    plt.close(fig)
    return path


# ---------------------------------------------------------------- F3: Q3 ----
def f3_q3_coefficients() -> Path:
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    rows = [("lag (main model)", Q3_LAG, ACCENT), ("lead (diagnostic)", Q3_LEAD, WARN)]

    for yi, (label, d, colour) in enumerate(rows):
        xerr = [[d["coef"] - d["lo"]], [d["hi"] - d["coef"]]]
        ax.errorbar(d["coef"], yi, xerr=xerr, fmt="o", color=colour,
                    capsize=6, lw=2.2, ms=9, zorder=4)
        ax.text(d["hi"] + 0.6, yi, f"{d['coef']:.2f}  [{d['lo']:.2f}, {d['hi']:.2f}]",
                va="center", fontsize=9.5, color=INK)
        if "boot_lo" in d:
            ax.errorbar(d["coef"], yi + 0.20, xerr=[[d["coef"] - d["boot_lo"]],
                                                    [d["boot_hi"] - d["coef"]]],
                        fmt="|", color=MUTED, capsize=5, lw=1.4, ms=7, zorder=3)
            ax.text(d["hi"] + 0.6, yi + 0.26, f"wild bootstrap [{d['boot_lo']:.2f}, {d['boot_hi']:.2f}]",
                    va="center", fontsize=8.2, color=MUTED)

    ax.axvline(0, color=INK, lw=1.2, zorder=2)
    ax.set_yticks([0, 1], [r[0] for r in rows])
    ax.set_ylim(-0.6, 1.75)
    ax.set_xlabel("Coefficient on charging density (points per 1,000 pop)")
    ax.set_title("Q3  Both lead and lag are positive and precise")
    ax.grid(axis="x", alpha=0.25)
    ax.text(0.99, 0.96, "lead significant (p = 0.0001)\n\u2192 ADR-006 D.5: direction not identified",
            transform=ax.transAxes, ha="right", va="top", fontsize=9, color=INK,
            bbox={"boxstyle": "round,pad=0.45", "fc": "#f4f6f8", "ec": MUTED, "lw": 0.8})

    path = OUT / "f3_q3_coefficients.png"
    fig.savefig(path)
    plt.close(fig)
    return path


# ---------------------------------------------------------------- F4: Q4 ----
def f4_q4_band(ev: pd.DataFrame, em: pd.DataFrame) -> Path:
    vn = em[em["country"] == "Vietnam"]
    transport = vn[vn["sector"] == "Transport"]["emissions_mt"].iloc[0]
    national = vn["emissions_mt"].sum()

    stock = ev[(ev["country"] == "Vietnam") & (ev["mode"] == "2 and 3 wheelers")
               & (ev["parameter"] == "EV stock share") & (ev["year"] == 2024)]["value"].iloc[0]

    # intensity factor = 1 - EV intensity / ICE intensity, grid varies
    factors = [1 - (35 / 1e3 * g) / (2.5 / 100 * 2.31) for g in (0.30, 0.45, 0.60)]
    band = [transport * (stock / 100) * sh * f for sh in (0.50, 0.65, 0.80) for f in factors]
    got = (round(min(band), 4), round(float(np.median(band)), 4), round(max(band), 4))
    assert got == Q4_BAND, f"Q4 band drifted: {got} != {Q4_BAND}"

    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    rows = [
        ("Today's segment\n(2024, 2.6% of fleet)", min(band), max(band), ACCENT),
        ("Fully electrified\n(100% of fleet)", Q4_CEILING[0], Q4_CEILING[1], MUTED),
    ]
    for yi, (label, lo, hi, colour) in enumerate(rows):
        ax.plot([lo, hi], [yi, yi], lw=13, color=colour, solid_capstyle="butt", zorder=3)
        ax.text(hi * 1.12, yi, f"{lo:.2f} \u2013 {hi:.2f} Mt", va="center", fontsize=10, color=INK)

    ax.set_yticks([0, 1], [r[0] for r in rows])
    ax.set_xscale("log")
    ax.set_xlim(0.3, 90)
    ax.set_xlabel("Avoided CO\u2082, Vietnam (Mt, log scale)")
    ax.set_title("Q4  What the segment delivers vs what it could")
    ax.grid(axis="x", alpha=0.25, which="both")
    captured = float(np.median(band)) / np.mean(Q4_CEILING) * 100
    ax.text(0.98, 0.06, f"today \u2248 {captured:.1f}% of the potential\n"
                        f"\u2248 1/{100 / captured:.0f} of what it could ever deliver",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=9, color=INK,
            bbox={"boxstyle": "round,pad=0.45", "fc": "#f4f6f8", "ec": MUTED, "lw": 0.8})

    path = OUT / "f4_q4_band.png"
    fig.savefig(path)
    plt.close(fig)

    share_of_national = (min(band) / national * 100, max(band) / national * 100)
    return path, share_of_national


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ev, em = load()

    made = [f1_q1_scatter(ev, em), f2_q2_rmse(), f3_q3_coefficients()]
    f4_path, f4_pct = f4_q4_band(ev, em)
    made.append(f4_path)

    for p in made:
        print(f"  wrote {p.relative_to(ROOT)}  ({p.stat().st_size // 1024} KB)")
    print(f"\nQ4 band = {f4_pct[0]:.3f}-{f4_pct[1]:.3f}% of national CO2")
    print("All asserted values match the notebooks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

<!-- Regenerate the PDF (from the repo root):
       pandoc docs/proposal.md -f gfm -t html5 --standalone --css proposal.css \
              -o docs/proposal.html && weasyprint docs/proposal.html docs/proposal.pdf
     Then delete docs/proposal.html -- it is an intermediate, not a deliverable.
     Do not use pdflatex: it cannot typeset the Vietnamese names (Trần Văn Tấn Khôi). -->

# EV adoption and the shape of national CO₂

**A cross-country study of what predicts electric-vehicle uptake, and what it means for Vietnam**

CSC17104 *Programming for Data Science* — Final Project Proposal
Vietnam National University, Ho Chi Minh City · University of Science · Faculty of Information Technology
Fall 2026 · 27 November 2026

---

## 1. Team and division of work

| Member | Student ID | Questions owned | Repository work |
| --- | --- | --- | --- |
| Trần Văn Tấn Khôi | 24120010 | **Q2** (ML), **Q4** (Vietnam) | data pipeline, ML question, Vietnam analysis, README, LLM log |
| Lê Thành Đạt | 24120035 | **Q1** (cross-country), **Q3** (charging density) | cross-country correlation, EDGAR–IEA merge audit, panel specification |

Four questions, two each, at least one answered by a machine-learning model — the split
required by the course brief §3.3. Every question has exactly one owner, who is
responsible for defending it in the Q&A.

## 2. What we are studying

National electric-vehicle adoption is usually reported as a league table of shares. That
answers "who is ahead" but not "what makes a country move", and it treats a share as if it
were a cause. We test four specific claims about the *structure* behind adoption, using
only public, traceable data:

- whether the weight of transport in a country's CO₂ predicts how fast it electrifies;
- whether next year's adoption rate is predictable at all, and where a fitted model breaks;
- whether public charging density drives adoption or merely follows it;
- whether Vietnam's transition is a two-wheeler story, and how much CO₂ it avoids.

Each claim is framed as a **hypothesis fixed in writing before the analysis**, with a
decision rule fixed alongside it. Two of those rules later failed, and the failures are
reported as results rather than adjusted away.

## 3. Dataset

| Source | What we use | Size | Licence |
| --- | --- | --- | --- |
| **EDGAR 2026** (EU JRC) — `GHG_by_sector_and_country`, `Substance = CO2`, year 2025 | National CO₂ by 8 sectors, no LULUCF | 4,858 × 60 | `IEA-EDGAR CO2` component: **CC BY-NC-ND 4.0**; rest: CC BY 4.0 |
| **IEA Global EV Outlook 2025** — `GEVO_EV_2025`, `category = Historical`, `powertrain = EV` | EV sales share, stock share, public charging points | 16,436 × 9 | **CC BY 4.0** |
| **World Bank Open Data API** — `NY.GDP.PCAP.CD`, `SP.POP.TOTL`, income group | GDP per capita, population, income group | 6–7 countries, 2010–2024 | **CC BY 4.0** |

We chose this dataset because the two questions a policy audience actually asks — *does
transport structure predict adoption* and *what would electrification buy us* — both need
CO₂ and adoption measured on the same national unit. EDGAR and GEVO supply exactly that,
and both are published by the organisations that produce them, so provenance is not in
doubt.

**Two sampling facts constrain every answer.** The IEA export is wide (62 countries and
regions for EV sales share, 48 for EV stock share) but contains only **7 of our 8
countries** — Singapore has zero rows. And EDGAR's single `Transport` sector includes
aviation and shipping, so it is a coarser proxy for road transport than the questions
ideally want.

**On redistribution.** The EDGAR CO₂ series is the `IEA-EDGAR CO2` component, licensed
**NC-ND** (academic use, no redistribution of modified versions). Neither source file nor
any derived CSV is committed; the repository ships the pipeline that regenerates them, and
both inputs are hash-pinned so a fresh clone can verify it has the right files.

**Existing public analyses of this data.** Declared per brief §2, and neither asks our
questions:

- **IEA, *Global EV Outlook 2025*** — the report shipping this dataset. It reports market
  shares and scenario projections by market; it does not test a cross-country statistical
  relationship between national CO₂ structure and adoption pace (Q1), nor benchmark a
  fitted model against a persistence baseline (Q2).
- **Our World in Data, electric-vehicle pages** — descriptive charts from the same GEVO
  export. Visualisation, not hypothesis testing: no pre-registered decision rule and no
  null result to report.

<!-- AUTHOR TODO (Đạt + Khôi): add any third-party notebook or Kaggle analysis of this
     export that you know of, or delete this comment. -->

## 4. Questions and pre-registered hypotheses

| # | Question | Hypothesis fixed before analysis | Type |
| --- | --- | --- | --- |
| **Q1** | Does the weight of transport in national CO₂ predict the pace of electrification, after controlling for income? | **H1 (directional):** higher transport weight accompanies faster adoption. If the sign reverses or the estimate is indistinguishable from zero, report as found. | Analysis |
| **Q2** | Can next year's adoption rate be predicted across countries, and where does the model break? | **H2 (non-directional):** the model beats a persistence baseline by ≥ 1.0 pp of `EV sales share` on the test set. Failing to beat it is a valid result. | **ML** |
| **Q3** | Does public charging density increase adoption? | **H3 (directional):** the lagged charging coefficient is positive with a CI excluding 0, **conditional** on a lead/lag test finding no reverse causality. | Analysis |
| **Q4** | Is Vietnam's transition a two-wheeler story, and how much CO₂ does it avoid? | **H4 (descriptive):** two-wheelers adopt at a clearly higher level than cars; avoided CO₂ is a band, not a point. | Analysis |

## 5. Key findings

| # | Pre-registered test | Computed result | Verdict |
| --- | --- | --- | --- |
| **Q1** | Spearman ρ ≥ 0.7857 in magnitude **and** bootstrap 95 % CI excluding 0, n = 7 | ρ = −0.5714, exact permutation p = 0.2000, CI [−1.0000, 0.3725] | **Not met** — indistinguishable from zero, and the sign is negative, opposite to H1 |
| **Q2** | Test RMSE at least 1.0 pp below persistence (7.2423 pp → ≤ 6.2423 pp) | Pooled Ridge 9.5196 pp; country-dummy Ridge 9.2175 pp; HistGradientBoosting 13.68 pp | **Not met** — no model beat persistence |
| **Q3** | Charging coefficient positive, CI excluding 0, conditional on no reverse causality | Not yet computed — design fixed in ADR-006, implementation outstanding | **Pending** |
| **Q4** | Report a band, not a point, over a pre-declared assumption set | 2024 band 0.4204 / 0.6245 / 0.8647 Mt CO₂ avoided = 0.109 % / 0.161 % / 0.223 % of national CO₂ | **Computed** |

<!-- AUTHOR TODO (one or two sentences per question, your own words):
     Q1 (Đạt):
     Q2 (Khôi):
     Q4 (Khôi):
-->

**Q2 is also being benchmarked against IEA's own view.** The same data file publishes
IEA's modelled values (`category = Projection-STEPS`) for exactly our test country-years,
so the error analysis gains one comparison row: does a simple model add anything over
IEA's structural model? It is framed as a **hindcast**, not a forecast contest — the STEPS
series is 2025-vintage, so for 2021–2024 it is a reconstruction, not an ex-ante prediction.

## 6. What did not go to plan

We report this because it is the part of the project we can defend most confidently.

- **Two pre-registered rules failed.** Q1's correlation is not distinguishable from zero
  and points the wrong way; Q2's models all lost to a persistence baseline. Both are
  reported as failed rather than rescued by changing the threshold after seeing the data.
- **The interesting Q2 result is not the error level but its direction.** Cross-validated
  RMSE is ~1.3 pp while test RMSE is 9.5–13.7 pp, because the CV folds sit entirely in the
  low-share 2012–2020 window while the test window is the high-growth 2021–2024 regime.
  Selecting the primary model on CV alone — the honest, no-peeking way — picks the model
  that performs *worse* on test. That rank reversal is the finding.
- **Country identity adds almost nothing.** Fitting country dummies improved Ridge by
  0.30 pp and HistGradientBoosting by 0.01 pp, which indicates the missing information is
  acceleration, not country identity.
- **Q4's headline magnitude is small and we say so.** Two-wheelers are 2.6 % of Vietnam's
  EV stock, so the 2024 band is 0.11–0.22 % of national CO₂. The informative comparison is
  the ceiling: a fully electrified two-wheeler fleet would avoid 16.2–33.3 Mt, or 4.2–8.6 %
  of national CO₂. Today's segment therefore delivers roughly **a fortieth of what it could
  ever deliver** — a better sentence for a policy audience than "0.16 %".
- **The share metric and the base rates disagree.** By 2024 cars exceed two-wheelers on
  both EV sales and EV stock share, but at a roughly 22:1 motorbike-to-car fleet ratio,
  two-wheelers' 2.6 % stock share implies roughly 12× more electric two-wheelers than
  electric cars in absolute terms. GEVO publishes no absolute EV counts for Vietnam, so
  this is a measurement critique, not a settled count.

## 7. How to run

```bash
git clone <repo> && cd <repo>
conda env create -f environment.yml
conda activate min_ds-env          # Jupyter kernel is registered as `min_ds`
# download both .xlsx into data/raw/ and verify SHA-256 against ADR-002
python src/prepare_data.py         # -> data/processed/{emissions,ev}_long.csv
jupyter lab                        # run 01 -> 02 -> 03 in order
```

Both inputs are hash-pinned and the pipeline fails closed on a mismatch; output hashes are
printed for comparison. Notebook order is `01_collection_exploration` →
`02_analysis` (Q1, Q3, Q4) → `03_ml_question` (Q2) — question numbering deliberately does
not match notebook numbering, because the brief fixes the filenames.

## 8. Scope and future work

Declared out of scope rather than quietly dropped:

- **Q3b — the US tax-credit event study** is deferred to future work per ADR-001 C.5. The
  design is recorded in ADR-006 D.7; it needs a hand-digitised quarterly sales series,
  which cannot be produced with provenance in the time available.
- **Road-specific CO₂ for Q4.** EDGAR reports one `Transport` sector, so the Q4 band treats
  road transport as 100 % of transport — a stated ceiling, not a measurement. A national
  GHG inventory with a road/aviation/shipping split would turn the ceiling into a range.
- **Current Vietnamese registration counts.** The 22:1 motorbike-to-car ratio is from 2015;
  current counts by segment would replace it and settle whether two-wheelers still dominate
  the physical fleet, which GEVO's share-only data cannot answer.
- **Grid intensity from published scenarios.** Q4's three grid points are declared
  assumptions. Deriving them from IEA *World Energy Outlook 2026* annex tables
  (CPS / STEPS / NZE) would replace assumption with citation, but those tables are
  projections, so they belong in a robustness axis rather than the headline.

## 9. AI assistance

Every significant use of an LLM is logged in `LLM_USAGE.md` — tool, request, and what was
kept, changed or rejected. The brief permits LLMs as a tutor, not as a ghostwriter:
analysis, interpretation and reflection are the authors' own, and the log is written so
that any named output can be defended in the Q&A.

Two rules the repository enforces on itself:

- **Reproducibility is checked, not asserted** — inputs hash-pinned, outputs hashed, the
  pipeline fails closed.
- **Rules are frozen before results are seen** — when a pre-registered rule failed, it was
  reported as failed.

---

*Decisions and their rationale: `docs/decisions/` (ADR-001 … ADR-008, index in
`docs/README.md`). Frozen question set and decision rules: `SPECIFICATION.md`.*

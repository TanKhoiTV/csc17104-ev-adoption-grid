# EV adoption and the shape of national CO₂

What predicts how fast a country electrifies its vehicle fleet — and what does that
mean for Vietnam?

CSC17104 *Programming for Data Science*, Fall 2026
Vietnam National University, Ho Chi Minh City — University of Science
Faculty of Information Technology

## Team

| Member | Student ID | Questions owned |
| --- | --- | --- |
| Trần Văn Tấn Khôi | 24120010 | Q2 (ML), Q4 (Vietnam) |
| Lê Thành Đạt | 24120035 | Q1 (cross-country), Q3 (charging density) |

Four questions, two per member, one of them answered by a machine-learning model —
the split required by the course brief §3.3.

## Questions

| # | Question | Type | Owner |
| --- | --- | --- | --- |
| **Q1** | Does the weight of the transport sector in national CO₂ predict the pace of electrification, after controlling for income? | Analysis | Đạt |
| **Q2** | Can next year's adoption rate be predicted across countries, and where does the model break? | **ML** | Khôi |
| **Q3** | Does public charging density increase adoption? | Analysis | Đạt |
| **Q4** | Is Vietnam's transition a two-wheeler story, and how much CO₂ does it avoid? | Analysis | Khôi |

Each question carries a hypothesis fixed **before** the analysis, and each may be
falsified. The hypotheses, variables, decision rules and robustness checks are pinned in
[`SPECIFICATION.md`](SPECIFICATION.md); architectural choices are recorded as ADRs in
[`docs/decisions/`](docs/decisions/) (index: [`docs/README.md`](docs/README.md)).

## Key findings

Results only — the interpretations live in the notebooks, where the authors defend them.

| # | Pre-registered test | Computed result | Verdict |
| --- | --- | --- | --- |
| **Q1** | Spearman ρ ≥ 0.7857 in magnitude **and** bootstrap 95 % CI excluding 0, n = 7 | ρ = −0.5714, exact permutation p = 0.2000, CI [−1.0000, 0.3725] | **Not met** — indistinguishable from zero; the sign is negative, opposite to H1 |
| **Q2** | Test RMSE at least 1.0 pp below the persistence baseline (7.2423 pp → ≤ 6.2423 pp) | Pooled Ridge 9.5196 pp; country-dummy Ridge 9.2175 pp; HistGradientBoosting 13.68 pp | **Not met** — no model beat persistence |
| **Q3** | Charging coefficient positive, CI excluding 0, **conditional** on lead/lag not detecting reverse causality | Not yet computed | **Not started** (#22) |
| **Q4** | Report a band, not a point, over a pre-declared assumption set | 2024 band 0.4204 / 0.6245 / 0.8647 Mt CO₂ avoided (min/median/max) = 0.109 % / 0.161 % / 0.223 % of national CO₂; joint assumption envelope 0.3174–0.9196 Mt | **Computed** |

Two failures are reported as results rather than buried. A rule fixed in advance that
then fails is evidence; a rule chosen after seeing the data is not.

<!-- AUTHOR TODO — one sentence per question, in your own words, saying what YOU conclude.
     Leave the table above alone; it is the numbers. Write the sentence here.

     Q1 (Đạt):
     Q2 (Khôi):
     Q3 (Đạt):
     Q4 (Khôi):
-->

**Status of this table.** Q1's numbers come from PR #40, Q2's from PR #43 and Q4's from
PR #44; Q3 is unimplemented. The table will be finalised once all four are merged.

## Data

Three public sources. The two spreadsheets are pinned by SHA-256 and downloaded by hand
(the IEA one sits behind a free account, so neither is committed); the third is fetched
live.

| Source | What we use | Size | Licence |
| --- | --- | --- | --- |
| [EDGAR 2026](https://edgar.jrc.ec.europa.eu/) — EU JRC, `EDGAR_2026_GHG_booklet_2026.xlsx`, sheet `GHG_by_sector_and_country`, `Substance = CO2`, year 2025 | National CO₂ by sector, 8 sectors, no LULUCF | 4,858 × 60 | The `IEA-EDGAR CO2` component is **CC BY-NC-ND 4.0**; the rest of EDGAR is CC BY 4.0 |
| [IEA Global EV Outlook 2025](https://www.iea.org/data-and-statistics/data-product/global-ev-outlook-2025) — `EV Data Explorer 2025.xlsx`, sheet `GEVO_EV_2025`, `category = Historical`, `powertrain = EV` | EV sales share, EV stock share, public charging points | 16,436 × 9 | **CC BY 4.0** — cite as *IEA, Global EV Outlook 2025, IEA, Paris* |
| [World Bank Open Data API](https://data.worldbank.org/) — `NY.GDP.PCAP.CD`, `SP.POP.TOTL`, income group | GDP per capita, population, income group | 6–7 countries, 2010–2024 | **CC BY 4.0** |

The licence that matters most is the first one. EDGAR's CO₂ series *is* the `IEA-EDGAR CO2`
component, which is **NC-ND**: academic use only, and no redistribution of modified
versions. That is why neither source file nor any derived CSV is committed — only the
pipeline that regenerates them.

Two sampling facts shape every answer below. The IEA export is wide — 62 countries and
regions for EV sales share, 48 for EV stock share — but only **7 of our 8 countries** are
in it: **Singapore has zero rows**. And EDGAR's single `Transport` sector includes
aviation and shipping, so it is a coarser proxy for road transport than the questions
ideally want.

Data dictionaries, name-mapping and coverage pins: [ADR-002](docs/decisions/ADR-002-dataset.md)
and [ADR-004](docs/decisions/ADR-004-country-sample.md).

### Existing public analyses of this data

Declared per brief §2. Both are published by the data owners themselves, and neither asks
our questions:

- **IEA, *Global EV Outlook 2025*** — the report that ships this data file. It reports
  market shares and scenario projections by market. It does not test a cross-country
  statistical relationship between national CO₂ structure and adoption pace, which is Q1,
  and it does not benchmark a fitted model against a persistence baseline, which is Q2.
- **Our World in Data, electric-vehicle pages** — descriptive charts built from the same
  GEVO export. Visualisation, not hypothesis testing: no pre-registered decision rule, no
  null result to report.

Our contribution is therefore not new data but a *pre-registered* use of it: four
hypotheses fixed in writing before analysis, two of which fail and are reported as
failures.

<!-- AUTHOR TODO — add any third-party notebook/Kaggle analysis of this export you know of,
     or delete this comment if there is none. -->

## Repository layout

```
.
├── README.md                  this file
├── SPECIFICATION.md           frozen question set, variables, decision rules
├── environment.yml            conda environment
├── LLM_USAGE.md               per-use log of AI assistance (brief §6)
├── docs/
│   ├── README.md              ADR index
│   └── decisions/             ADR-001 … ADR-008
├── src/
│   └── prepare_data.py        the one reusable module: raw .xlsx → tidy CSV
├── data/
│   ├── raw/                   the two .xlsx sources (gitignored)
│   └── processed/             tidy CSVs (gitignored, regenerated)
├── notebooks/
│   ├── 01_collection_exploration.ipynb
│   ├── 02_analysis.ipynb      Q1, Q3, Q4
│   └── 03_ml_question.ipynb   Q2
└── slides.pdf                 presentation (in progress)
```

## How to run

Tested on Windows 11 with a conda-forge environment; it should behave the same on
Linux or WSL.

**1. Create the environment**

```bash
conda env create -f environment.yml
conda activate min_ds-env
```

The Jupyter kernel is registered as `min_ds`, which is the name the notebooks reference —
the conda environment name and the kernel name differ on purpose.

**2. Download the two raw files into `data/raw/`**

| File | Where to get it |
| --- | --- |
| `EDGAR_2026_GHG_booklet_2026.xlsx` | <https://edgar.jrc.ec.europa.eu/> — 2026 GHG booklet |
| `EV Data Explorer 2025.xlsx` | <https://www.iea.org/data-and-statistics/data-product/global-ev-outlook-2025> — requires a free IEA account |

The IEA file needs a free account, which is why the hashes are pinned rather than a URL.
Verify both before running anything:

```bash
sha256sum data/raw/*.xlsx
# or on Windows:  certutil -hashfile "data/raw/EV Data Explorer 2025.xlsx" SHA256
```

Expected:

```
BB77A0DA5735925B3A6A64BE63DADE9E71B57174D5EC6C7EFF872274DF00F88C  EDGAR_2026_GHG_booklet_2026.xlsx
309C6342BB730D1B565553B6F57F6EF7A5F436D164AF81DBCC6A2DC8AB35699D  EV Data Explorer 2025.xlsx
```

The pipeline refuses to run on a mismatch.

**3. Build the tidy CSVs** — from the repository root:

```bash
python src/prepare_data.py
```

This writes `data/processed/emissions_long.csv` (61 rows) and `data/processed/ev_long.csv`
(496 rows), and prints their hashes. Expected on the pinned inputs:

```
emissions_long.csv  D742524F6FE5F2F63D497C16F329BA14FF85088B022D22C47B4A6880159A91BD
ev_long.csv         7F8A68858032A1C541C12D62E39A9DC58CBF8382401E73BB47AB7E175F3D7A72
```

Reruns are byte-identical; outputs are written atomically, so a failed run cannot leave a
half-written CSV behind.

**4. Run the notebooks in order**

```bash
jupyter lab
```

| Order | Notebook | Contents |
| --- | --- | --- |
| 1 | `01_collection_exploration.ipynb` | sources, licences, data exploration, sample table |
| 2 | `02_analysis.ipynb` | **Q1**, **Q3**, **Q4** |
| 3 | `03_ml_question.ipynb` | **Q2** |

Question numbering does not match notebook numbering: Q2 lives in the `03_` file because
the course brief fixes the filenames ([SPECIFICATION.md](SPECIFICATION.md) §8).

Steps 2 and 3 also fetch World Bank indicators live (GDP per capita, population, income
group) and cache them to `data/processed/*.json`, so the first run of each needs network
access. Access dates are recorded in the notebooks.

## A note on AI assistance

Every significant use of an LLM is logged in [`LLM_USAGE.md`](LLM_USAGE.md) — the tool,
the request, and what was kept, changed or rejected. Analysis, interpretation and
reflection are the authors' own; the brief permits LLMs as a tutor, not as a ghostwriter,
and the log is written so that any named output can be defended in the Q&A.

Two rules the repo enforces on itself:

- **Reproducibility is checked, not asserted.** Inputs are hash-pinned, outputs are
  hashed, and the pipeline fails closed on any mismatch.
- **Rules are frozen before results are seen.** When a pre-registered rule failed, the
  rule was reported as failed (Q1, Q2) rather than adjusted to fit.

## Status

| Deliverable | State |
| --- | --- |
| Q1, Q2, Q4 code | complete, in review (#40, #43, #44) |
| Q3 code | not started (#22) |
| `LLM_USAGE.md` | in review (#30) |
| `slides.pdf` | not started (#25) |

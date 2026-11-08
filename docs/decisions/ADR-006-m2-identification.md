# ADR-006: Identification strategy for M2

## Status

Proposed

## Date

2026-10-20

## Context

M2 asks: **does public charging density increase the EV adoption rate?**

Two problems:

- **Reverse causality.** Countries with more EVs tend to have more chargers; a positive correlation does not reveal the direction.
- **Sample size.** ADR-004 fixes 8 countries, but Singapore has no IEA data, so M2 only has **6**. Six cross-sections are too few; a panel is needed to separate within-country variation from country-level differences.

### Why the 30/9/2025 tax-credit shock is not M2's identification

On 30 September 2025, three US federal EV tax credits (30D, 25E, 45W) stopped applying to vehicles purchased after that date (Public Law 119-21).

The shock changes **demand, not charging supply**. A `post × exposure` design around it estimates the effect of the **tax credit**, not of charging density. The two questions are different and must not share a coefficient.

The shock is therefore split off as a separate analysis, **M2b** (D.7), with its own estimand.

### Why M2b has to run quarterly

The shock's effect disappears at annual frequency:

| Frequency | Figure | Reading |
| --- | --- | --- |
| Monthly | Oct 2025: −27%; Nov: −42%; Dec: −35% vs same period 2024 | effect visible |
| Annual | US EV sales share: 10% (2024) → 10% (2025) | nothing visible |

The only source for US monthly sales is Argonne, which returns **403** for every URL even with a browser User-Agent — not scriptable. AFDC is scriptable at state level, but its charging counts have a measurement break: national station counts jumped **+57.8%** from 2020 to 2021 (31,751 → 50,097), not from real construction. Hence the M2b charging window must end **before 2021**.

M2 does not use the shock, so it is not bound to monthly or quarterly frequency; annual IEA charging data is sufficient.

### M2's data

Charging density comes from `EV Data Explorer 2025.xlsx` (GEVO), but coverage is uneven: Japan/US from 2010, Germany from 2012, China from 2014, Thailand/New Zealand from 2017, **Vietnam only 2023–2024**.

## Decision

### D.1. Estimand

The effect of **public charging density** on **EV adoption rate** (EV sales share, cars), at the **country–year** level.

### D.2. Panel

**6 countries** (ADR-004 minus Singapore and Vietnam), 2010–2024, **unbalanced**:

| Country | Years with charging data |
| --- | --- |
| Japan, United States | 2010–2024 (15) |
| Germany | 2012–2024 (13) |
| China | 2014–2024 (11) |
| Thailand, New Zealand | 2017–2024 (8) |
| Vietnam | 2023–2024 (2) — listed for reference only |

Total: **70 country-year cells** after the charging-coverage filter (6 countries), **64 observations** entering the regression after the one-year lag. Vietnam contributes 0 usable rows and is excluded (D.6).

### D.3. Variables

- **Outcome:** EV sales share (cars), IEA.
- **Explainer:** public charging points per 1,000 population, **lagged 1 year**.
- **Control:** log GDP per capita. Other controls (electricity price, transport share) are reported only as sensitivity checks.

### D.4. Identification

- **Country** + **year** fixed effects.
- Identifying variation is **within-country** change after removing the common trend.
- **Lead/lag test:** the diagnostic is a **separate** regression of adoption on `lead(charging)` only; the D.3 model (with `lag(charging)`) is the estimate. A significant `lead` indicates reverse causality or anticipation → not identifiable. Two designs were possible (one joint regression vs two separate ones); design (2) is chosen because D.5's verdict rule speaks of the CI of `lag` on its own.
- **No IV.** No candidate instrument satisfies the exclusion restriction; lead/lag is a diagnostic, not an identification strategy.

### D.5. Pre-committed verdict rule

| Result | Verdict |
| --- | --- |
| `lead` (diagnostic) not significant **and** CI of `lag` (D.3 model) excludes 0 | **Contributive** |
| `lead` not significant **and** CI of `lag` contains 0 | **Not identifiable** — report null with CI |
| `lead` significant | **Not identifiable** — design cannot separate the direction |

Both "not identifiable" branches are valid, reportable results and must be reported in full, not softened.

### D.6. Vietnam

Only 2 years of charging data, so Vietnam **cannot contribute to M2**. Exclude from the model and **report it explicitly** — do not drop it silently.

### D.7. M2b — separate analysis

- **Question:** what did the 30/9/2025 tax credit do to EV adoption?
- **Panel:** 51 states + DC, **quarterly**.
- **Identification:** `post × exposure`, with `exposure` = state EV share in **2019** (before the law was signed).
- **Outcome:** prefer **quarterly sales** (Alliance for Automotive Innovation); fallback is **annual registrations** (AFDC — stock, weaker).
- **Charging window:** naive 2014–2025 and strict **2014–2020**.
- **M2b's result does not replace M2's conclusion** and must not be merged into D.5.

### D.8. Sources

| Role | Source | Licence | Download date | Access |
| --- | --- | --- | --- | --- |
| M2: EV sales share, charging points | `EV Data Explorer 2025.xlsx` (GEVO) | IEA terms (unverified) | 2026-10-19 | local file, gitignored |
| M2: GDP per capita | World Bank | CC BY 4.0 | 2026-10-19 | API |
| M2b: charging ports by state | AFDC `historical-station-counts.xlsx` | US federal public data | 2026-10-19 | scriptable |
| M2b: EV sales by state-quarter | Alliance *Get Connected* (PDF) | hand-digitised from charts | 2026-10-19 | PDF, scriptable download |
| M2b: EV registrations by state-year | AFDC `vehicle-registration` | US federal public data | 2026-10-19 | scriptable |

**Provenance for hand-digitised data.** The Alliance quarterly sales will be transcribed by hand from chart images. The transcribed file (`data/raw/alliance_state_quarterly.csv`), the transcriber, the transcription date, and its hash must be recorded before M2b's outcome variable is used. Otherwise M2b's outcome has no provenance trail — the weakest position in a reproducibility review.

### D.9. Tools

`linearmodels` (panel FE) and **wild cluster bootstrap** for standard errors — with only 6 clusters, ordinary cluster-robust inference is unreliable. `min_ds-env.yml` is missing `statsmodels`, `linearmodels`, `pyfixest` — ADR-007 must add them.

## Alternatives Considered

- **A.1. Tax-credit shock as M2's identification.** Rejected: the shock changes demand, not charging supply; the coefficient would estimate the tax credit, not charging density.
- **A.2. Monthly national event study (Argonne).** Rejected: Argonne returns 403 for every URL.
- **A.3. Annual national panel only.** Rejected: blind to the 2025 shock at annual frequency.
- **A.4. IV with an undefined instrument.** Rejected: no candidate satisfies the exclusion restriction.
- **A.5. 51 US states as M2's primary panel.** Rejected: changes the level of analysis and conflicts with ADR-004; kept as M2b only.
- **A.6. Drop Vietnam without reporting it.** Rejected: must be reported (D.6).

## Consequences

- **C.1. Only 6 clusters.** Standard errors must use wild cluster bootstrap; M2's power is low and the ADR states that plainly.
- **C.2. Unbalanced panel.** Vietnam is excluded from M2; n = 70 (64 after the lag).
- **C.3. M2 and M2b are two estimands with two verdicts.** Their conclusions must not be merged.
- **C.4. ADR-004 needs one fix:** the US role currently reads "event study of M2"; it must read **M2b**.
- **C.5. Simultaneity remains.** Fixed effects and lead/lag reduce but do not remove reverse causality.
- **C.6. Environment is incomplete.** `min_ds-env.yml` needs `statsmodels`, `linearmodels`, `pyfixest` (ADR-007).
- **C.7. `SPECIFICATION.md` inherits D.3 and D.5** verbatim, without restating them.

# ADR-004: Pin the countries and their analytical roles

## Status

Proposed

## Date

2026-10-19

## Context

- Why pick a country sample at all: M1 fits a diffusion model per country; M2 compares across countries; M3 compares the EV transition against each country's own emissions structure.
- The sample must be frozen completely before `SPECIFICATION.md` is written, so country selection is never justified by results.
- Basis:
    - `EDGAR_2026_GHG_booklet_2026.xlsx` for sector structure (basis for M3 sector share and each country's role)
    - `EV Data Explorer 2025.xlsx` for EV transition and charging coverage.

## Decision

### Countries selected

| # | Country | Role | EDGAR name | IEA key |
| --- | --- | --- | --- | --- |
| 1 | Vietnam | Baseline | Viet Nam | Viet Nam |
| 2 | Thailand | Closest ASEAN comparator | Thailand | Thailand |
| 3 | Singapore | Affluent ASEAN | Singapore | _absent_ |
| 4 | China | Irony case | China | China |
| 5 | Japan | Developed East Asia | Japan | Japan |
| 6 | Germany | EU representative | Germany | Germany |
| 7 | United States | Western benchmark | United States | USA |
| 8 | New Zealand | Best case | New Zealand | New Zealand |

Rationale for each role, from the tables below:

- **Baseline (Vietnam)** — the country behind the policy question; `2 and 3 wheelers` has 11 continuous years.
- **Closest ASEAN comparator (Thailand)** — same region, but transport share 30.3% vs Vietnam's 13.1% (2.3x), with full 15-year coverage.
- **Affluent ASEAN (Singapore)** — transport share 10.0%, second lowest in the sample; contrast with Vietnam.
- **Irony case (China)** — lowest transport share in the sample (8.3%) yet the largest emitter (13,057 Mt) and the strongest transition pressure. "Irony" refers to the ratio relative to scale, not to the size of the sector.
- **Developed East Asia (Japan)** — transport share 18.4%, fullest coverage in the sample (15 years of charging).
- **EU representative (Germany)** — largest EU economy in the sample (567.8 Mt CO₂).
- **Western benchmark (United States)** — 36.4% transport share, 15 years of data, and the only country with the Clean Vehicle Credits event for M2b (ADR-006).
- **Best case (New Zealand)** — highest transport share in the sample (52.7%), i.e. the largest emissions base against which to measure the effect of electrification.

### Sector structure (EDGAR)

Method: filter `Substance = CO2`, **year 2025**; denominator is the sum of all 8 sectors (LULUCF excluded); `Industry = Industrial Combustion + Processes`; `Power = Power Industry`.

"Total CO₂" is the sum of the 8 sectors, in Mt.

| Country | Transport % | Industry % | Power % | Total CO₂ 2025 (Mt) |
| --- | --- | --- | --- | --- |
| Vietnam | 13.1 | 35.6 | 46.0 | 387.0 |
| Thailand | 30.3 | 27.3 | 30.6 | 266.9 |
| Singapore | 10.0 | 41.7 | 39.5 | 57.1 |
| China | 8.3 | 30.7 | 50.3 | 13,057.1 |
| Japan | 18.4 | 21.6 | 44.9 | 977.3 |
| Germany | 24.1 | 20.4 | 31.4 | 567.8 |
| United States | 36.4 | 13.0 | 33.0 | 4,739.1 |
| New Zealand | 52.7 | 21.2 | 11.9 | 29.2 |

Source: `data/EDGAR_2026_GHG_booklet_2026.xlsx`, sheet `GHG_by_sector_and_country`.

> **Note on China and New Zealand.** The claim that "New Zealand and China bracket the range (52.7% and 8.3%)" from the pre-registration holds only **within the eligible pool** (29 countries from A.1), not across all countries with data: widening the charging-data threshold puts Costa Rica (66.8%) above New Zealand, and at a threshold of ≥ 12 years of charging data China drops out of the pool. Across all 171 countries with substantial emissions, 16 have a transport share higher than New Zealand's. `SPECIFICATION.md` must state that this is the **eligible-pool** range, not a global one.

### EV data coverage (IEA)

"Years (n)" counts years with continuous data; gaps are stated explicitly.

"Charging 2024" is `Publicly available fast` + `Publicly available slow`.

| Country | EV sales share (cars) | EV stock share (cars) | Public charging | Charging 2024 | Note |
| --- | --- | --- | --- | --- | --- |
| Vietnam | 2018, 2021–2024 (5) | 2018–2024 (7) | 2023–2024 (2) | 6,100 | missing 2019–2020; charging only 2 years |
| Thailand | 2010–2024 (15) | 2010–2024 (15) | 2017–2024 (8) | 13,400 | complete |
| Singapore | — | — | — | — | **absent from the file** |
| China | 2010–2024 (15) | 2010–2024 (15) | 2014–2024 (11) | 3,500,000 | complete |
| Japan | 2010–2024 (15) | 2010–2024 (15) | 2010–2024 (15) | 34,000 | complete |
| Germany | 2010–2024 (15) | 2010–2024 (15) | 2012–2024 (13) | 157,000 | complete |
| United States | 2010–2024 (15) | 2010–2024 (15) | 2010–2024 (15) | 193,000 | complete |
| New Zealand | 2010–2024 (15) | 2010–2024 (15) | 2017–2024 (8) | 1,440 | complete |

Source: `data/EV Data Explorer 2025.xlsx`, sheet `GEVO_EV_2025`, `category = Historical`, `powertrain = EV`.

Notes:

- **Singapore does not exist in the IEA file.** No entry for Singapore appears anywhere in it, so Singapore can only be used for M3, not M1 or M2.
- **Vietnam's `cars` series is thinner than its `2 and 3 wheelers` series.** `cars` has 5 scattered years (2018, 2021–2024); `2 and 3 wheelers` has 11 continuous years (2014–2024) for both sales share and stock share.
- **Vietnam has only 2 years of charging data (2023–2024).** If M2 uses charging density as a regressor, Vietnam cannot contribute. The M2b event study around the Clean Vehicle Credits does not need this data.

## Alternatives Considered

Only alternatives that change the sample or its conclusion are listed.

### A.1. Data threshold and the eligible pool

Of the 54 countries in the IEA file, only **29** satisfy three minimum conditions: continuous `cars` sales share and stock share, and **≥ 8 years** of public charging data. The other 25 are excluded on technical grounds, not on analytical role:

| Exclusion reason | Countries excluded |
| --- | --- |
| No stock share (cars) | Bulgaria, Croatia, Cyprus, Czech Republic, Estonia, Hungary, Ireland, Latvia, Lithuania, Luxembourg, Romania, Seychelles, Slovakia, Slovenia |
| Year gaps (sales share) | Indonesia, Lithuania, Russia, **Viet Nam** |
| Charging < 8 years | Austria (6), Brazil (7), Colombia (4), Costa Rica (4), Indonesia (4), Israel (3), Jordan (4), Malaysia (4), Russia (4), Uzbekistan (0), **Viet Nam (2)** |

### A.2. Singapore — why it stays in the sample despite having no IEA data

Singapore is the alternative with the largest impact, since it is the only country in the sample that cannot enter M1 or M2.

| Option | Assessment |
| --- | --- |
| **Keep Singapore, use for M3 only (chosen)** | M3 only needs EDGAR, which Singapore has. Keeps the "affluent ASEAN" role and the low end of the transport-share range (10.0%). Trade-off: no contribution to M1 or M2. |
| Replace with Malaysia | Only 4 years of charging (A.1); `2 and 3 wheelers` very weak (0.64% in 2024), losing the contrast with Vietnam (9.4%). |
| Replace with Indonesia | `cars` has gaps; stock share only from 2019 (A.1). |
| Drop Singapore, keep 7 countries | Loses the "affluent ASEAN" role and the low end of the transport-share range; the sample tilts entirely toward high transport share. |
| Pull from a newer IEA release | OWID (GEVO 2026) has Singapore 2016–2025, but that mixes two versions — weakens consistency. **Not chosen.** |

### A.3. Countries in the eligible pool that were not selected

The eight countries are selected for **analytical role**, not for best data. Of the eight, only six (Thailand, China, Japan, Germany, United States, New Zealand) are members of the 29-country eligible pool; Vietnam and Singapore are chosen **outside** the pool (Vietnam as the baseline despite thin data, Singapore for its role — see A.2). Hence 29 − 6 = 23 pool countries are not selected; the table below lists the 20 most representative.

| Country (transport % of CO₂) | Why not selected |
| --- | --- |
| India (11.5), South Africa (11.7) | Duplicate the "low transport share" position of China. |
| South Korea (16.6) | Duplicate the "developed East Asia" position of Japan. |
| Netherlands (19.4), Poland (25.1), Belgium (27.1), France (43.6), Italy (36.2), Spain (41.3), UK (36.7), Sweden (43.4), Denmark (43.0), Finland (30.6), Greece (36.0) | Duplicate the "EU representative" position of Germany. |
| Canada (28.9), Mexico (30.0), Australia (27.0), Chile (36.6) | Duplicate the "Western benchmark" position of the United States. |
| Norway (30.2) | 92% of new cars sold were electric in 2024 (IEA file), but power is only **4.1%** of CO₂ — electricity is already clean, so electrification has little M3 leverage. Kept as a qualitative comparison. |
| Turkey (21.3) | Sits between East Asia and ASEAN; matches no role. |

### A.4. Other sampling rules considered

| Rule | Why not used |
| --- | --- |
| Random draw from the 29 eligible | Does not guarantee Vietnam (the baseline case) or coverage of the transport-share range. With n = 8, allocation is uncontrolled. |
| By emissions rank | Sample of large countries: dilutes the CO₂ coefficient, and M3 cannot distinguish "small vs large". Also excludes New Zealand (29.2 Mt) — losing the highest transport share. |
| All 29 eligible | Fitting diffusion + 10,000 bootstrap replicates for 29 countries is 29 curves; M3 needs per-country sector structure. n = 8 is the practical limit of the method. |
| By income level | All 8 would be middle-to-high income, excluding Vietnam — the whole point of the policy question. |
| All 10 ASEAN | 5 countries (Philippines, Cambodia, Laos, Myanmar, Brunei) have no EV data at all; Singapore is absent from the IEA file. Too much missing data to sample on principle. |

## Consequences

- **Sample size changes with every module.** M1 and M2 run on 7 countries, M3 on all 8. The sample size must be stated explicitly in the spec or notebook.
- **Vietnam's data is thin in 2–3 of its modules.** The `cars` series has 5 scattered years, which is thin for M1; charging data covers only 2 years, so Vietnam contributes little to M2. But `2 and 3 wheelers` is rich — 11 continuous years — and is the basis for the two-wheeler policy. If M1 covers only cars, Vietnam may be excluded from results; that decision belongs in the spec.
- **Tables use EDGAR 2025 data from the EDGAR 2026 release (Fast Track); 2024 is the final release.** New Zealand's transport share shifts **2.6 percentage points** between the two years. The spec must state which year is primary and which is the sensitivity check.
- **IEA rounds to two significant figures.** For small values such as Vietnam's (0.0016% in 2018, 0.041% in 2021), this limits the precision of bootstrap CIs, so M1's comparison threshold must account for the rounding floor.
- **Country names differ between files:** EDGAR uses `Viet Nam` / `United States` / `South Korea` / `Türkiye`; IEA uses `Viet Nam` / `USA` / `Korea` / `Turkiye`. `prepare_data.py` needs an explicit mapping table, otherwise rows are silently dropped — the same class of bug that hid Singapore's absence.
- **Both xlsx files are gitignored**, so they are not committed. The tables in this ADR are the durable record of the numbers. Changing the sample later requires a new ADR superseding this one, not an in-place edit.

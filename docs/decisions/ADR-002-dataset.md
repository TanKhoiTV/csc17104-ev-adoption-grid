# ADR-002: Dataset decision record

## Status

Proposed

## Date

2026-11-04

## Context

The project needs two kinds of data, for three modules:

- **Emissions by sector and country** — for Q1 and as the basis for selecting the country sample (ADR-004).
- **EV data** (sales share, stock share, public charging points) — for Q2 (diffusion coverage) and Q3 (charging density → adoption).

Constraints:

- Must cover the **8 countries** in ADR-004.
- Must be an **official release with a version number**, so it can be cited and reproduced.
- **Must not be committed** to the repository: licence terms and file size (see D.3).

The two files below are the primary dataset. They live in `data/` and are hidden by `data/*` in `.gitignore`.

## Decision

### D.1. EDGAR 2026 — emissions by sector

| Property | Value |
| --- | --- |
| File | `data/EDGAR_2026_GHG_booklet_2026.xlsx` |
| Size | 4,767,596 bytes |
| SHA-256 | `BB77A0DA5735925B3A6A64BE63DADE9E71B57174D5EC6C7EFF872274DF00F88C` |
| Sheet | `GHG_by_sector_and_country` |
| Filter | `Substance = CO2`, year **2025** |
| Denominator | Sum of **8 sectors**, LULUCF excluded |
| Sector grouping | `Industry = Industrial Combustion + Processes`; `Power = Power Industry` |

The eight EDGAR sector labels, verbatim as they appear in the sheet:

1. Agriculture
2. Buildings
3. Fuel Production
4. Industrial Combustion
5. Power Industry
6. Processes
7. Transport
8. Waste

`Industry` and `Power` in the ADR-004 tables are groupings of these labels; `Transport` is used as-is.

Used for: the sector structure of Q1, and the basis for each country's role in ADR-004.

Note: year 2025 is the **Fast Track (preliminary)** release; 2024 is the final release. The sensitivity between the two must be recorded in `SPECIFICATION.md`.

### D.2. IEA GEVO 2025 — EV data

| Property | Value |
| --- | --- |
| File | `data/EV Data Explorer 2025.xlsx` |
| Size | 936,334 bytes |
| SHA-256 | `309C6342BB730D1B565553B6F57F6EF7A5F436D164AF81DBCC6A2DC8AB35699D` |
| Sheet | `GEVO_EV_2025` |
| Filter | `category = Historical`, `powertrain = EV` |

Used for: EV sales share, EV stock share, and public charging points for Q2 and Q3.

Known limits:

- The latest historical year is **2024**, so the file has **no post-treatment observations** for the 30/9/2025 shock. Q3b uses other sources (ADR-006, D.7–D.8).
- **Singapore does not exist** in the file, so it cannot enter Q2 or Q3 (and only contributes structure to Q1).
- IEA rounds to **two significant figures**; for very small values (e.g. Vietnam 0.0016% in 2018) this limits the precision of confidence intervals.
- The download is **gated behind an IEA account** ("You are either not logged in or your login session has expired… create an IEA account to download data"). A fresh clone cannot re-fetch without an account, so the hash pin in D.1/D.2 carries more weight, not less.

### D.3. Licence and storage

**EDGAR 2026.** The dataset's conditions of use state: material owned by the European Union is licensed under **CC BY 4.0**, "unless otherwise noted". The exception: the **IEA-EDGAR CO2** component (CO₂ from fossil fuel combustion) is licensed under **CC BY-NC-ND 4.0**.

Since Q1 filters `Substance = CO2`, and the CO₂ from fossil fuel combustion *is* the IEA-EDGAR CO2 component, the part of the data the project actually uses is **NC-ND**:

- **NC** — academic use only, not commercial.
- **ND** — no redistribution of modified data.
- **Action item:** users of IEA-EDGAR CO2 data must contact the IEA at `compliance@iea.org` for permission to use it outside the CC BY-NC-ND 4.0 terms.

**IEA GEVO 2025.** Licence confirmed on 2026-11-07 from the product page `https://www.iea.org/data-and-statistics/data-product/global-ev-outlook-2025` (browser fetch, saved as a local HTML record; scripted access returns a Cloudflare challenge):

- **CC BY 4.0** — redistribution is permitted with attribution.
- IEA-supplied citation: `IEA, Global EV Outlook 2025, IEA, Paris, https://www.iea.org/data-and-statistics/data-product/global-ev-outlook-2025, Licence: CC BY 4.0`
- The file is the "Global EV Data File", dated 14/05/2025 on the same page.

**Conclusion.** Both files stay outside git, hidden by `data/*` in `.gitignore`. The reason is now **reproducibility** (both are fetchable by URL and hash-verifiable, but neither is committed), not the GEVO licence. The NC-ND terms on the EDGAR CO₂ component are the binding constraint on *redistribution*: verbatim raw redistribution is defensible, but a redistributed `emissions_long.csv` (a filtered derivative) is not.

### D.4. Provenance record

Because the files are not in the repository, this table is the durable record of the inputs.

| File | Source | Download date | SHA-256 (short) |
| --- | --- | --- | --- |
| EDGAR 2026 | EDGAR / JRC, release `EDGAR_2026_GHG` | 2026-10-19 | `BB77A0DA…` |
| GEVO 2025 | IEA, *Global EV Outlook 2025* — Global EV Data Explorer | 2026-10-19 | `309C6342…` |

Anyone cloning the repository must download the exact versions above and verify the hashes before running `prepare_data.py`.

### D.5. Version pinning

- The versions used in the project are **EDGAR 2026** and **GEVO 2025**. They are not replaced in place.
- A newer release (e.g. EDGAR 2027, GEVO 2026) requires a **new ADR** superseding this one.
- Every result in the notebooks must state which data version it used.

### D.6. Country-name mapping

The two files use different names. `prepare_data.py` must use an explicit mapping table; relying on name matching silently drops rows — the same class of bug that hid Singapore's absence.

| Country | EDGAR name | IEA key |
| --- | --- | --- |
| Vietnam | `Viet Nam` | `Viet Nam` |
| Thailand | `Thailand` | `Thailand` |
| Singapore | `Singapore` | _absent_ |
| China | `China` | `China` |
| Japan | `Japan` | `Japan` |
| Germany | `Germany` | `Germany` |
| United States | `United States` | `USA` |
| New Zealand | `New Zealand` | `New Zealand` |

### D.7. Out of scope

These sources are **not** covered by this ADR:

- AFDC (charging and registration by state), Argonne (US monthly sales), Alliance for Automotive Innovation (quarterly sales by state), EAFO (EU monthly).

They serve Q3b and are decided in **ADR-006, D.7–D.8**. Rule: adding a new source requires recording its licence, access method, and download date; if it becomes a primary source, it needs its own ADR.

## Alternatives Considered

- **A.1. Use OWID GEVO 2026 instead of GEVO 2025.** OWID has Singapore 2016–2025, but it mixes two IEA versions in one sample and weakens consistency. **Rejected.**
- **A.2. Use EDGAR 2025 instead of EDGAR 2026.** The 2025 release stops at 2024, losing the 2025 year used for sector structure. **Rejected.**
- **A.3. Commit the two xlsx files to the repository.** Violates the **ND** terms of IEA-EDGAR CO2 and adds ~5.7 MB. **Rejected.**
- **A.4. Replace IEA with AFDC/EEA for EV data.** Does not cover all 8 countries and uses different definitions (registrations by state/country) vs IEA sales share. **Rejected.**
- **A.5. Scrape the dashboards instead of using the released files.** Unnecessary when official, versioned, hashable files exist. **Rejected.**

## Consequences

- **C.1. A clone does not include the data.** A download step plus SHA-256 verification is required; this ADR is the provenance record.
- **C.2. The NC-ND terms restrict redistribution.** No redistribution of modified data; the project uses the data for academic analysis only.
- **C.3. EDGAR 2025 (data year) is Fast Track (preliminary); 2024 is final.** Q1 results must include a sensitivity check on the year.
- **C.4. IEA rounds to two significant figures.** Small values such as Vietnam's are limited in precision.
- **C.5. Country names differ between files.** An explicit mapping table is mandatory (D.6).
- **C.6. Singapore has no IEA data.** Q2 and Q3 run on 6 countries; Q1 runs on 7 (describing structure for 8); Q4 runs on 1.
- **C.7. IEA GEVO terms were unverified at write time** and are now confirmed CC BY 4.0; the account-gated download remains a reproducibility constraint.

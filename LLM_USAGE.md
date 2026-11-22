# LLM_USAGE.md

Required by the course brief (PDF §6): *"Record each significant use in `LLM_USAGE.md`: the tool, what you
asked, and how you used or changed the answer."*

This log is also the evidence for the brief's harder rule: *"You must be able to explain every line of your
submission. Work you cannot explain in the Q&A is treated as not your own."* An entry here is a promise that the
named member can defend that output — not a permission slip.

**What counts as significant.** Any use that produced text, code, a number or a decision that ended up in the
repository, in an issue, or in the analysis. Questions about syntax or error messages are not logged
individually; anything that shaped the project is.

**Reverse-chronological.** New entries at the top. Each entry names its owner so the two members' work does not
blur.

---

## Entry 004 — 2026-11-20 — review round 2: verify Dat's fixes, address Dat's review items

**Owner:** Khoi
**Tool:** Pi-Bolt (coding-agent harness) · model `glm-5.3` (provider `opencode-go` — id do harness báo qua biến
môi trường `PI_PROVIDER`; catalog id `opencode` là id upstream của cùng nguồn).

**Asked.** (a) Check updates on the 10 open PRs. (b) Verify Dat's fix commits against the source files.
(c) Apply Dat's review items on the four `khoi/` PRs.

**Produced and how it was used.**

| Output | Used as | Change / verification |
| --- | --- | --- |
| Verification of Dat's ADR-003 fix (#31) | Reviewer confidence, no further change request | Recomputed the pinned coverage table from the raw file: all 7 per-country rows match, total **496** ✓; 0 NaN, 0 duplicate keys ✓; partial fast/slow coverage (CN ×4, US ×5 slow-only; JP ×4, NZ ×1 fast-only) matches ✓. |
| Verification of Dat's ADR-007 env fix (#33) | Reviewer confidence | `statsmodels=0.14`, `linearmodels=6.1`, `pyfixest=0.60` pinned + mandatory `seaborn` 0.13.0→0.13.2 bump (pyfixest 0.60 requires ≥0.13.2) — a dependency conflict neither reviewer caught in round 1. |
| Notebook-filename verification (Dat's #28 item) | Commit `41d31d2` on PR #28 | Extracted the text of `CSC17104_2026_Final_Project.pdf` (the 5-page brief, not the 16-page slide deck): all three notebook names match the deliverable tree **verbatim**. |
| Fix commits for Dat's review items | `04b6110` (#26: PR-body ownership note, A.4 reword, C.6 criteria→question table), `0bf6172` (#27: electrification = fleet share `EV stock share`, stale `M1` reword), `41d31d2` (#28: Spearman 0.714, Q2 threshold unit, filename verification note) | AI drafted; member reviewed each diff before push. |

**Where the AI was wrong, and what caught it.**

1. **Entry 003 originally recorded this session's model as `deepseek-v4.1-flash`** — copied from the earlier
   entries instead of reading the session's own environment. The actual value was `glm-5.3` (corrected in the
   same pass as this entry). Lesson: *metadata about the current session is read from the session, not
   inherited from a template.*

---

## Entry 003 — 2026-11-19 — review pass on all 10 open PRs, fix commits on the four `khoi/` PRs

**Owner:** Khoi
**Tool:** Pi-Bolt (coding-agent harness) · model `glm-5.3` (provider `opencode-go`), reasoning effort high.
*(Model string corrected 2026-11-20 — see Entry 004.)*

**Asked.** (a) Review all 10 open PRs. (b) Verify every checkable number against the two source `.xlsx` files.
(c) Post the reviews, then apply fix commits to the four `khoi/` PRs.

**Produced and how it was used.**

| Output | Used as | Change / verification |
| --- | --- | --- |
| Formal reviews on the six `dat/` PRs (#14 APPROVE, #31/#32/#33 CHANGES_REQUESTED, #35/#36 APPROVE) | Posted as `TanKhoiTV` on GitHub | Every count re-derived from the raw files before posting: ADR-004 tables (8/8 countries, pool 29, 25 exclusions), ADR-008 values, SPECIFICATION's sparse-table claims and the NZ 2.55 pp shift. |
| Two CHANGES_REQUESTED findings on ADR-003 (#31) | Review comment | Verified in the file: the CO₂-2025 slice is **61 rows, not 64** (Singapore lacks `Agriculture`, Germany/US lack `Waste`); the pinned `powertrain = EV` filter drops all charging, sales and stock rows. |
| One CHANGES_REQUESTED finding on ADR-007 (#33) | Review comment | The PR body claims three packages were added to `min_ds-env.yml`, but the PR changes only the ADR; env file confirmed untouched on the branch. |
| Q2 sample recomputation for SPECIFICATION.md | Commit `7493e00` on PR #28 | Lag-2 feature priced in from the raw file: **78 observations (train 54 / test 24), 16 charger-NaN rows in train**. Policy chosen by the member: keep lag-2, impute NaN inside the train-only Pipeline. |
| Fix commits on ADR-001 (status wording; China reversal claim), ADR-008 (status wording; series minimums), SPECIFICATION.md (Q2 count, charger-NaN policy, World Bank source note), this file | Commits `4b58c25`, `afa3754`, `7493e00`, `87d3109` | AI drafted; member reviewed each diff before push. |
| Issue-board cleanup | Issues #1, #13, #18 edited; #5 reassigned to TanKhoiTV | #1: stale M1/M2/M2b/M3 labels replaced with Q1–Q4 (missed by the earlier renumbering pass). #13/#18: aligned with ADR-003 (root-level script path, long no-pivot schema, ADR-003 as the schema authority, ADR-003 added to the merge order) and annotated with the two PR #31 review findings that must be fixed first. #5: reassigned per ADR-005 D.6 since Khoi wrote ADR-001. Member reviewed each edit before push. |

**Where the AI was wrong, and what caught it.**

1. **The 84-observation Q2 sample survived a hand recomputation** — because the hand check reused the ADR-004 coverage table, which does not encode the lag-2 loss. Lesson: *recompute from the raw file, not from a summary table; a summary inherits its source's blind spots.*
2. **The first IEA query in this session used `United States` and briefly reported no US charging data.** The ADR-002 D.6 mapping (IEA key `USA`) caught it. Lesson: *the same name-mapping failure the ADR-003 fail-fast rule exists to prevent happens to reviewers too.*

---

## Entry 002 — 2026-11-07 — `SPECIFICATION.md`, `LLM_USAGE.md`, ADR-001, ADR-008

**Owner:** Khoi
**Tool:** Pi-Bolt (coding-agent harness) · model `deepseek-v4.1-flash` (provider `opencode-go`), reasoning effort
high.

**Asked.** Draft the pre-registration, the LLM usage log, and the two ADRs that were still empty
(`ADR-001`, `ADR-008`); fix the question numbering to narrative order.

**Produced and how it was used.**

| Output | Used as | Change / verification |
| --- | --- | --- |
| `ADR-001` (research topic, four questions in narrative order) | PR #26, `Closes #5` | AI drafted; member reviewed and accepted. The data limits it records were re-checked by re-reading the output of the coverage script. |
| `ADR-008` (Q4, avoided-emissions band) | PR #27, `Closes #17` | AI drafted. One AI statement was **wrong and corrected by the AI itself in a follow-up commit** (`829e08d`): it had let Vietnam use the `2 and 3 wheelers` series inside Q1, repeating the definitional inconsistency the same ADR rejects for Q2. |
| `SPECIFICATION.md` | PR #28, `Closes #2` | AI drafted the whole document from the ADRs. Every number in §2 and §3 (70 / 64 / 7 / 6 / 11 observations) was recomputed by hand from the ADR-004 coverage table before merging. The Q2 count was first recomputed as 84 (one lag) — **wrong, caught in review**: the two-year lag feature removes two more rows per country. Corrected to 78 (train 54 / test 24) in commit `7493e00`; see Entry 003. |
| Question renumbering (`M3→Q1`, `M1→Q2`, `M2→Q3`, `M2b→Q3b`) | Issues #17, #19, #21, #25 edited | AI performed the edit; member authorised it. Drafts for the other member's issues (#22, #23) were left unapplied, for that member to accept. |
| This file | PR for #29 | AI drafted. Member reviewed. |

**Judgement calls the member made, not the AI.** Dropping the US tax-credit event study (Q3b) to future work;
accepting that Q2 excludes Vietnam; accepting that "grid" is not a standalone question. The AI proposed each; the
member decided each.

---

## Entry 001 — 2026-11-07 — orientation, verification, licence, question redesign

**Owner:** Khoi
**Tool:** Pi-Bolt · model `deepseek-v4.1-flash` (provider `opencode-go`), reasoning effort high.

**Asked.** (a) Catch up on the project's state. (b) Review the three open ADR pull requests. (c) Verify the data
files and the tables recorded in the ADRs. (d) Determine the IEA licence. (e) Evaluate whether the four questions
and their narrative hold up against the course rubric.

**Produced and how it was used.**

| Output | Used as | Change / verification |
| --- | --- | --- |
| Board audit (state of 22 issues, 3 PRs, why they were blocked) | Discussion only | Verified by direct `gh` queries; the AI initially reported "no sub-issue links" and was **wrong** — native sub-issues existed. Corrected in conversation. |
| Review threads on PR #14 (5), #15 (3), #16 (2) | Posted as `CHANGES_REQUESTED` | Every count claim was re-derived by hand before posting: the eligible-pool arithmetic (29 pool countries − 6 in-pool selections = 23 remaining, not 21), and the Q3 panel size (70 cells = 6 countries, not 7). |
| SHA-256 verification of both data files | Accepted as fact | Reproducible: `sha256sum` against the pins in ADR-002 D.1/D.2. Both matched exactly. |
| Reproduction of ADR-004's two tables from the raw files | Used to justify accepting ADR-004 as accurate | Sector table matched 8/8 countries, charging table 7/7, NZ 2024→2025 shift +2.55 pp. Scripts re-run and output compared row by row. |
| EDGAR sector list and sparse-table structure | Requested as a change on PR #16 | Read from the file's own `info` and `Citations and references` sheets. |
| Licence finding: GEVO is **CC BY 4.0**, EDGAR's IEA-CO2 slice is **CC BY-NC-ND 4.0** | Requested as a change on PR #16 (D.3) | AI could not fetch `iea.org` (Cloudflare 403); it relied on a browser-saved copy supplied by the member. The EDGAR half was read directly from the file's citation sheet, including the instruction to contact `compliance@iea.org`. |
| GEVO parameter coverage analysis | Basis for ADR-001's Context and for rejecting three candidate questions | Reproducible from the file: `Battery demand` and `Oil displacement` exist only for 6 aggregate entities; `Electricity demand` exists only under `Projection-STEPS`. |
| Proposal to re-angle the third question and renumber the set | Accepted; applied to issues | AI proposed; member decided. |

**Where the AI was wrong, and what caught it.**

1. **Licence advice was initially wrong.** The AI advised against committing the IEA file on licence grounds,
   because it inherited the "terms unconfirmed" status recorded in ADR-002 D.3 instead of checking the primary
   source. The product page states CC BY 4.0 plainly. Lesson applied: *a summary in our own ADR is not a source.*
2. **A grid-intensity question built on GEVO would have been impossible.** The AI's first suggestion used
   `Electricity demand` as the EV electricity input. The coverage check killed it before any work was done, because
   that parameter has zero historical rows. Lesson: *check coverage before designing the question, not after.*
3. **Native sub-issue links were misreported as missing.** Lesson: *verify against the API, not against the
   absence of a text pattern.*

---

## What the AI did not do

- **No analysis was run.** None of Q1–Q4 has produced a result. Every number in the repository so far is either a
  data-file fact or a decision threshold fixed in advance.
- **No raw data was modified.** The two `.xlsx` files are byte-identical to the official releases, per hash.
- **The research direction was not invented by the tool.** The topic, the eight-country sample, and the
  identification strategy for Q3 were decided earlier by the team and are recorded in ADR-002/004/006, written
  before this session.

## Rules we apply

1. Nothing AI-drafted merges without a named member reading it. If a member cannot explain a sentence in the Q&A,
   the sentence comes out — regardless of whether it is correct.
2. Numbers produced with AI help are accepted only if reproducible by re-running a command (hash, count, table).
   Reproduction beats plausibility.
3. AI drafts structure, code and prose. **The members own the judgements**: which question to ask, which sample is
   defensible, and what a null result means.
4. Log the same day, not at the end. The log is the thing being graded alongside the work.

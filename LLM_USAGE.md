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
| `SPECIFICATION.md` | PR #28, `Closes #2` | AI drafted the whole document from the ADRs. Every number in §2 and §3 (84 / 70 / 64 / 7 / 6 / 11 observations) was recomputed by hand from the ADR-004 coverage table before merging. |
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

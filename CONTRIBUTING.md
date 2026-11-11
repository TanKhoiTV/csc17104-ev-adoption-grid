# Contributing

## Branch naming

- Branches follow `khoi/<topic>` or `dat/<topic>`, cut from the latest `main`.
- Topic is short, kebab-case, and matches the issue/ADR number (e.g. `dat/adr-003-conversion-method`).
- No direct commits to `main`.

## Commit convention

- Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, ...
- Messages in English, short, describing *what* now *how*.

## Pull request process

1. Create a branch from the latest `main` (`git pull origin main` first).
2. Write code/docs and commit with a conventional commit message.
3. Push and open a PR with a body following the template (Closes #X, What changed, Notes).
4. The other member reviews before merge. No self-merge.
5. Reviewer sets `CHANGES_REQUESTED` with inline comments; the author fixes with new commits (no force-push) and re-requests review.
6. Merge using **merge commits** (not rebase or squash) to preserve history and attribution.

## Merge order

ADRs -> data layer (ADR-003 + `prepare_data.py`) -> analysis (Q1/Q3/Q4) -> ML (Q2) -> integration (notebooks + slides).

Merging out of order causes cascading conflicts. If a PR must skip the queue (e.g. a hotfix to a merged ADR), it goes through the same review gate and the skip is noted in the PR body.

## Review checklist (before approving)

1. Run notebooks end-to-end on a clean machine.
2. Print row counts before and after every filter/join; compare against `SPECIFICATION.md`.
3. Verify plots have a title, units and legend (course brief §3.4).
4. Verify input SHA-256 hashes match ADR-002 D.1/D.2.
5. `grep M[1-3]` is clean (only explanatory parentheticals allowed).

## Environment

- `conda env create -f min_ds-env.yml` -> `conda activate min_ds`
- Python 3.11.5 (floor; 3.12+ may not support `linearmodels` yet).
- Details: ADR-007.

## Language convention

- ADRs and `SPECIFICATION.md`: Vietnamese.
- PR bodies, issues, `LLM_USAGE.md`, and this file: English.
- Chat and review discussion: Vietnamese (team convention).

## Authority rule

`ADR > SPECIFICATION.md > notebook`. Any change to schema, model, or sample must amend the relevant ADR
first; notebooks only read what the ADRs and `SPECIFICATION.md` define.

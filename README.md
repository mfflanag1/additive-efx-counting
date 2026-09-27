# Additive EFX counting

**Current program audit (27 September 2026):**
[results, corrections, review depth and next theorem](docs/EFX_PROGRAM_AUDIT_2026-09-27.md),
[pinned later research branches](docs/RESEARCH_BRANCH_INDEX.md), and
[the next goods campaign: global admission](docs/global-admission/GLOBAL_ADMISSION_CAMPAIGN.md).
The adjacent [chores paper](https://github.com/mfflanag1/counterexample-hunt/tree/main/efx2)
is a separate theorem with different certification tiers. General additive goods EFX
is **not solved**. Older optimistic campaign summaries are not current status.

This repository contains a research paper and its computational evidence on
the number of labeled EFX allocations under positive additive valuations. The
current result is deliberately narrow: it supplies six exact count-\(n\)
witnesses, a theorem explaining their parking structure, and one
computer-verified lower bound over a finite integer box. It does **not** solve
the unrestricted additive EFX existence or counting problem.

The paper is [paper/main.pdf](paper/main.pdf), with source in
[paper/main.tex](paper/main.tex). Its three claims are:

| Contribution | Status | Primary evidence |
|---|---|---|
| Positive additive instances with exactly \(n\) labeled EFX\(_0\) allocations at \((4,7),(5,8),(6,9),(4,8),(4,9),(4,10)\) | Exact exhaustive computation | [repro/counting_witnesses](repro/counting_witnesses) |
| A necessary-and-sufficient generalized parking criterion for adding one leftover good to an EFX\(_0\) base allocation | Mathematical theorem plus exact certificates | [artifacts/generalized_parking](artifacts/generalized_parking) |
| Every positive integer \(4\times7\) instance with entries in \(\{1,2,3,4\}\) has at least four labeled EFX\(_0\) allocations | Finite computer-verified result | [repro/countcegar_k4](repro/countcegar_k4) |

The six matrices establish upper bounds on the additive minimum count. They do
not establish tightness: the conjectured unrestricted additive lower bound of
\(n\) remains open. The displayed \((4,7)\) witness also lies outside the
finite box \(\{1,\ldots,4\}\), so the witness and bounded computation cannot be
combined into an unrestricted equality theorem.

## Repository map

| Path | Role |
|---|---|
| `paper/` | Current 10-page paper and its LaTeX source |
| `repro/counting_witnesses/` | Three-way exhaustive verification of the six matrices |
| `artifacts/generalized_parking/` | The parking theorem, seven fixed-witness certificates, and verifier |
| `repro/countcegar_k4/` | Protected-slot counting master, independent CNF, replay code, and DRAT evidence |
| `supplement/` | Deterministic, clean-tree release builder for the paper's 57-file evidence profile |
| `repro/countcegar_real/` | Audited exact-real CEGAR checkpoint; research prototype, not a theorem |
| `artifacts/efx_chambers/` | Audited chamber-radius extension; not currently in the paper |
| `artifacts/multifloater_parking/` | Audited multi-floater extension; not currently in the paper |
| `tracks/parkability/` | Exact \((4,8)\) parkable-deletion evaluator and sound bounded CEGAR workbench; no \(K=4\) result yet |
| `results/`, `tracks/`, root research scripts | Campaign archive and discovery work; presence is not a claim of correctness |
| `docs/` | Accomplishments, audit history, archive guide, and [thesis research program](docs/THESIS_RESEARCH_PROGRAM.md) |

Canonical program status is recorded in the dated audit above; the counting
claims remain recorded here and in [ACCOMPLISHMENTS.md](ACCOMPLISHMENTS.md).
Older reports and campaign notes are
preserved as research history; see
[docs/CAMPAIGN_ARCHIVE.md](docs/CAMPAIGN_ARCHIVE.md) before citing them.

The later general-existence campaign, including the internally certified
\((4,8)\) package and a proof-checked \((4,9)\) theorem for the strict-common-
favorite/universal-owner-threshold-failure branch, is tracked separately in
[results/GENERAL_EFX_GOAL_20260730.md](results/GENERAL_EFX_GOAL_20260730.md).
It postdates this frozen counting manuscript. Results from the two tracks
must be cited with their own scope and provenance; the counting paper does
not claim the unrestricted \((4,9)\) cell or general existence theorem.

## Quick verification

Python 3.10 was used for the audited runs. From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
make verify-paper
```

`make verify-paper` reruns the six exact counts, generalized-parking
certificates, encoding regressions, fixed-instance slot boundary, and archived
DRAT integrity check without modifying tracked evidence. `make verify-audit`
also checks the exact-real checkpoint and the two scratch extensions. Full
commands and trust boundaries are in
[REPRODUCIBILITY.md](REPRODUCIBILITY.md).

## Current calibration

This is research-grade, PhD-level work suitable for a focused paper or a
substantial thesis chapter. Its strongest contribution is the combination of
explicit exact witnesses, a structural theorem, and archived solver evidence.
It is not by itself a full thesis and should not be presented as a resolution
of additive EFX existence.

The LaTeX source still contains an author-metadata placeholder. No public
license or citation metadata has been chosen; the repository is therefore
intended to remain private until those publication decisions are made.

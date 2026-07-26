# Additive EFX counting

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
| `results/`, `tracks/`, root research scripts | Campaign archive and discovery work; presence is not a claim of correctness |
| `docs/` | Accomplishments, audit history, archive guide, and [thesis research program](docs/THESIS_RESEARCH_PROGRAM.md) |

Canonical status is recorded here and in
[ACCOMPLISHMENTS.md](ACCOMPLISHMENTS.md). Older reports and campaign notes are
preserved as research history; see
[docs/CAMPAIGN_ARCHIVE.md](docs/CAMPAIGN_ARCHIVE.md) before citing them.

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

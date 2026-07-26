# Campaign archive guide

The repository preserves discovery programs, intermediate results, failed
conjectures, and referee-era reports so the route to the current paper remains
inspectable. These files are not all current and should not be read as one
consistent specification.

## Current claim-bearing material

| Claim family | Authoritative entry point |
|---|---|
| Six exact count-\(n\) witnesses | `repro/counting_witnesses/README.md` |
| Generalized single-floater theorem | `artifacts/generalized_parking/README.md` |
| Bounded \((4,7)\), \(K=4\) theorem | `repro/countcegar_k4/README.md` |
| Paper release profile | `supplement/README.md` |

Only files selected by those packages and their manifests belong to the
current paper evidence. A file's presence in `results/` alone does not make it
a theorem or verified result.

## Audited but out of paper

| Work | Status |
|---|---|
| `repro/countcegar_real/` | Reproducible `CHECKPOINT`; no UNSAT theorem |
| `artifacts/efx_chambers/` | Audited scratch theorem and exact certificates |
| `artifacts/multifloater_parking/` | Audited scratch theorem and exhaustive regression |

These packages are useful starting points for follow-on work but are
intentionally absent from the paper supplement.

## Historical records

- `LEDGER.md` is the literature and hypothesis ledger from the search campaign.
- `PLAN.md` is a dated research plan, not the current roadmap.
- `results/CAMPAIGN_LOG.md` is chronological and intentionally preserves
  mistakes and reversals.
- `results/REPORT.md` and `results/REVIEW.html` are superseded campaign-report
  revisions. They contain stale running/pending states.
- theory notes under `results/` may carry supersession banners and should be
  cited only after checking the current paper and audit history.
- root Python programs and `tracks/` are discovery code. They were valuable for
  finding witnesses and mechanisms but are not automatically part of the
  verification chain.

The archive was left at its original relative paths because moving hundreds of
programs and evidence files would create unnecessary provenance risk. This
guide supplies the organizational boundary instead.

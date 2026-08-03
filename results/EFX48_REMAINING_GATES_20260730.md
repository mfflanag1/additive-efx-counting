# Remaining Gates: Nonnegative Additive EFX at \(4\times8\)

**Snapshot:** 2026-07-30 EDT  
**Claim:** every nonnegative additive four-agent, eight-good instance
admits a complete EFX allocation.

This ledger separates work the repository can close internally from work
that requires an independent person or machine.

| Gate | Status | Evidence or next action |
|---|---|---|
| Lean structural reduction | Closed | Pinned build and `AxiomAudit.lean` pass |
| Eight terminal UNSAT certificates | Closed | 8/8 cvc5 CPC proofs accepted by Ethos |
| Lean-to-SMT semantic binding | Closed | 8/8 cells and all 1,701 partitions audited |
| Independent direct encoding | Closed | 8/8 cells UNSAT over 40,824 labeled onto allocations |
| Published-input variants | Closed internally | Exact paper versions and Lean interfaces audited; paper proofs remain trusted |
| Frozen end-to-end release | Closed internally | Consolidated manifest verifies |
| Fresh-source same-host replay | Closed internally | New temporary project extraction, build, audits, and manifest pass |
| Full Ethos replay from fresh-source workflow | Closed internally | 8/8 `correct` |
| Independent-machine reproduction | Open, external | Repeat on another macOS ARM host or pin rebuilt Linux tools |
| Nonnegative closure | Closed | Uniform positive perturbation is Lean-checked; the main theorem now covers zero-valued goods |
| 130-core deletion witnesses | Active | 54/130 exact witnesses |
| Short analytic replacement | Sharpened | A 191-partition invariant anchored lemma is isolated in Lean; direct Hall-mask compression is empirically rejected |
| Technical exposition | Closed internally | Revised 14-page submission built and visually inspected |
| Submission-ready paper | Closed internally | Nonnegative theorem, calibrated related work, trust boundary, and analytic target included |
| Fair-division expert sign-off | Open, external | Use `EFX48_REVIEWER_HANDOFF.md` |
| Formal/certificate expert sign-off | Open, external | Rebuild, inspect bridge, and rerun Ethos |
| Novelty confirmation | Internally refreshed | Current literature still calls general four-agent additive EFX open; active researchers must confirm |

## What can be claimed now

The correct label is:

> **Internally verified bounded hybrid computer-assisted theorem.**

It is stronger than a conjecture, numerical experiment, or unchecked solver
result. It is not yet independently reproduced, externally reviewed, or
peer reviewed.

## Remaining executable sequence

Completed in this gate-closing pass:

- rebuilt the deterministic source archive and end-to-end manifest;
- replayed the fresh-source workflow with all eight Ethos checks enabled; and
- verified every final manifest hash.

Remaining:

1. Resume deletion witnesses:

   ```sh
   python3.10 tracks/parkability/analyze_core_deletion_witnesses.py \
     --checkpoint /absolute/path/favorite-211.shrunk.json \
     --output /absolute/path/favorite-211.deletion-witnesses.json \
     --per-check-limit 600
   ```

2. Give the manuscript and reviewer handoff to one fair-division expert and
   one formal/computational-proof expert.

The first remaining step is further proof compression. The second is the
genuinely external release gate.

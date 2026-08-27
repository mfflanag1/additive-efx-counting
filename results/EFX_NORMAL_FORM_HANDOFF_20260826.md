# Handoff — fixed-U normal-form session (2026-08-26)

Branch `fable/efx-fixed-u-normal-form` from `codex/efx-fixed-u-resume-20260820` @ `69c1dcd`.
Read first: `FIXED_U_NORMAL_FORM_THEOREM_20260826.md`, then `FIXED_U_NORMAL_FORM_PREMISE_LEDGER_20260826.md`.

## What was established
1. **Chart theorems.**  Under the rank-three master (nonself responses) exactly 316 exact response
   relations are realizable (twelve-atom) and exactly 679 under the physical-minimum (cap-free)
   master; the twelve-atom chart is precisely the physical cells containing `d->r`.  `d->q` is
   universal, charity is never a response target, named forms 1 and 3 are unrealizable, forms 0 and
   2 occur exactly once each.  Both charts have solver-free independent verifiers at every witness.
2. **The inserted step.**  "The exact support relation has five edges" (premise ledger item 4) is
   not derived anywhere; it is what reduces 316/679 cells to the two named forms.  The
   classification lemma is correct relative to that premise and is verified.
3. **Four-edge objective refuted on the twelve-atom master.**  The global four-edge CEGAR found two
   exact residual valuations (all premises verified solver-free, cells outside the named forms) with
   no four-edge complete EFX allocation; both close with five edges (two encodings + 4^12 brute
   force).  See `fixed_u_twelve_atom_four_edge_residuals_20260826.json`.
3′. **Immediate EFX.**  Every twelve-atom chart witness closes by a complete EFX allocation within
   four support edges (min edges 1/2/3/4 in 1/12/180/123 cells).  The universal version (global
   CEGAR over `M`, edge cap 4) and the cap-free whole-role five-edge CEGAR over the physical
   master are the two long-running certificates; see the theorem document's status lines.
4. **Cap-free four-edge whole-role closure is false** (obstruction after 8 cuts, relation
   `{d>q,q>r,q>s,r>s,s>q,s>r}`), closing at five edges or with one split at four edges.

## Resume commands (repo root)
```bash
# twelve-atom global FIVE-edge closure (the surviving universal statement; four edges is refuted):
python -m tracks.parkability.run_fixed_u_master_complete_efx_cegar --edge-cap 5 \
  --resume-cuts results/fixed_u_master_complete_efx_edge4_cuts_20260826.jsonl \
  --output results/g4_resume.json --cut-ledger results/g4_resume_cuts.jsonl
# cap-free five-edge whole-role closure (physical master, no form restriction):
python -m tracks.parkability.run_fixed_u_physical_master_whole_role_cegar --edge-cap 5 \
  --resume-cuts results/fixed_u_physical_whole_role_edge5_cuts_20260826.jsonl \
  --output results/p5_resume.json --cut-ledger results/p5_resume_cuts.jsonl
pytest -q tracks/parkability/test_fixed_u_normal_form_chart.py
```
Seeded parallel bursts (`--z3-seed`, `--max-rounds 15`, merge/dedupe ledgers by allocation, re-run
with `--resume-cuts`) multiply throughput; master checks slow from ~1 s to ~45 s as cuts accumulate.

## Laws
- Names are not charts: enumerate the exact relation by CEGAR to UNSAT, then re-verify every
  witness without a solver.
- Keep the twelve-atom and physical (T,M) objects apart: `d->r` is forced for atoms only.
- A single role's physical tail is `T-M`, never 0 (this bug cost one verifier round).
- Whole-role EFX conditions are linear in (T,M): closing allocations are exact master cuts;
  split allocations are cell-specific and are not cuts.
- Do not run z3 campaigns under machine load >100: UNKNOWN is a timeout, not a verdict.

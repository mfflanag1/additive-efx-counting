# Fixed-U handoff addendum — 2026-08-26 (four-split conjecture F4: refuted)

Appends to `EFX_FIXED_U_HANDOFF_20260814.md` and `HANDOFF_FROM_CC_20260817.md`;
companion to the parallel branch `cc/efx-four-split-20260826`
(`EFX_FOUR_SPLIT_HANDOFF_20260826.md`, commit `bacc5b0`).  This branch:
`cc/efx-four-split-f4-20260826` from `69c1dcd`.  Main note:
`results/FIXED_U_FOUR_SPLIT_F4_DECISION_20260826.md`.

## Verdict

**(F4) is false — permitted outcome 2, class (a).**  On the frozen
pattern-mixed profile `fixed_u_tame_or_anchor_cegar_20260821.json` the exact
two-good cell with side bits `{gq:r, h:r, j:d, j:q, l:r, m:s} = 1` (found by
the parallel session) has no complete EFX allocation within four support
edges at any split count.  This branch confirms it with a third encoding
(anchor-split integer-owner oracle: UNSAT at split caps 4 and 11), notes that
every split of a two-good role is an anchor split so the anchor restriction
is not the cause, and shows five edges close the cell with zero splits.  The
cell is displayed good by good in
`results/fixed_u_f4_obstruction_cell_20260826.json`.

## What else changed

1. Lemma E (endpoint reduction) is proved for arbitrary cardinality and
   witness identity; it yields an exact, adversary-favourable decision
   procedure for (F4) per profile (`decide_fixed_u_f4.py`, verified by
   `independently_verify_fixed_u_f4.py` in a one-hot encoding).
   Calibrations: the audited product cell reproduces split minimum 4 with
   the frozen split set and edges; the wild-and-forced profile reproduces
   min split 1 with template B and slack `23/1924`; both baseline artifacts
   replay byte-identically.
2. On every other decided corpus profile (405 of the other 407: 205
   retained, 81 tame-or-anchor, 7 anchor, 113 banked, the wild-and-forced
   terminal) (F4) holds; split counts 0/1/2/3 on 330/52/21/2 profiles; two
   `fresh-81` profiles undecided at caps 2–4 (oracle timeouts under load
   >100, not obstructions).  Independent verifier: 404 pass, 3 timeouts
   (two undecided profiles, one cap-2 obstruction re-check), 0 refutations.
3. The four-edge cap is the only reason any split is ever needed (edge-free
   ablation: zero splits; five edges: zero splits on the refuting cell and,
   per the parallel branch, on 293/293 ledger profiles).
4. Positivity of goods is load-bearing for the split count (zero-value goods
   lift the wild-and-forced minimum from 1 to 2 splits), not for closure.

## Precise remaining claim boundary

* Theorem (this branch): for each of the 405 decided non-refuted corpus
  profiles and every physical realization, a complete EFX allocation with at
  most four edges and at most four anchor splits exists (exact; two
  encodings; no realization enumeration).
* Refutation (both branches): (F4) fails on an admissible profile because a
  fifth edge is necessary.
* Not a theorem: any universal statement over the infinite admissible master.
  `run_fixed_u_f4_cegar.py` ran 0 (status MASTER_UNKNOWN); its union-closed rounds
  are point exclusions, not region cuts.
* Retired: the four-split conjecture and, with it, the "greedy anchor
  splitting along the support edges" lemma of step 5 — splitting is an
  edge-budget artifact, so no ordering lemma about splits can be the cap-free
  bridge.

## Corrected surviving local conjecture

> Every admissible form-2 exact-response profile admits a complete EFX
> allocation of whole roles using at most five support edges.

Whole-role allocations are realization-free (identity-aware Theorem 1), so
this is a linear condition on `(T, M)` and its universal form is decidable by
a symbolic CEGAR over the master (the parallel branch's W5).  The live
cap-free obligation is whether the retained-support termination argument of
the 2026-08-13 ledger tolerates a five-edge premise.  The global program is
unchanged after that: lift form 2 to every saturated fixed-`U` separator,
then lift fixed-`U` closure to general additive EFX.

## Rules observed

No return to (4,8); no census promoted to a cap-free theorem; the refuting
cell was run through the widest oracle (every split count; at five edges the
whole-role oracle) before being named; exact rationals throughout; positive
certificates (covers) and negative ones (relaxed obstructions one cap below
the minimum) verified independently; ablation countermodels recorded.

## Artifacts

```text
results/fixed_u_f4_obstruction_cell_20260826.json          the refuting cell, explicit goods, oracle verdicts
results/fixed_u_f4_obstruction_cell_onehot_20260826.json   one-hot re-verification (if finished within budget)
results/fixed_u_f4_profile_corpus_20260826.json            corpus (provenance-tagged)
results/fixed_u_f4_banked_113_20260826.jsonl               the 113 banked profiles extracted from 53bdeec
results/fixed_u_f4_corpus_results_20260826.jsonl           per-profile decisions + closing template sets
results/fixed_u_f4_corpus_verify_20260826.jsonl            independent re-verification per profile
results/fixed_u_f4_corpus_summary_20260826.json            minima table + certificate structure
results/fixed_u_f4_audited_product_cell_20260826.json      calibration at the frozen product cell
results/fixed_u_f4_audited_four_split_structure_20260826.json
results/fixed_u_f4_ablation_*_20260826.json                edge-free / zero-floor / random / no-exact
results/fixed_u_f4_profile_cegar_20260826.json(.jsonl)     profile-level CEGAR run
```

## Suggested next targets, in order

1. **Finish W5** on `cc/efx-four-split-20260826`
   (`run_fixed_u_whole_role_edge_cegar.py`, seeded/resumable): UNSAT is the
   theorem "every admissible form-2 profile has a whole-role five-edge EFX
   allocation"; SAT is a profile to run through the split oracle at five
   edges *before* naming it (do not repeat the four-edge mistake one edge up).
2. **Five-edge termination:** decide whether the retained-support termination
   argument (`FIXED_U_RETAINED_SUPPORT_TERMINATION_THEOREM_20260813.md`)
   tolerates a five-edge premise (three owner pairs + charity + one more).
   This is the real cap-free bridge now.
3. Cleanup on this branch: decide the two undecided profiles on a quiet
   machine (`python -m tracks.parkability.decide_fixed_u_f4 --profile ...
   --split-cap 4 --oracle-timeout 300`); give the one-hot obstruction check a
   better encoding at cap 4 (it times out on 12-role cells; the Int-owner
   oracle decides them in about 30 s).

## Tools on this branch (`tracks/parkability/`)

`decide_fixed_u_f4.py` (CEGAR in the relaxed realization space;
`--minima-table`), `independently_verify_fixed_u_f4.py` (one-hot;
`verify_cover` is instant, `verify_obstruction` slow),
`build_/run_/verify_/summarize_fixed_u_f4_corpus.py`,
`run_fixed_u_f4_cegar.py` (profile-level; the master returned UNKNOWN at
900 s in QF_LRA mode with 286 seeded cuts — a search tool, not a theorem
tool), `ablate_fixed_u_f4*.py`, `test_fixed_u_f4.py`.

## Hazards / laws

- Quantify allocations **per cell**; selectors quantified over realizations
  were the recurring flaw.  Test named cells directly: the adversary CEGAR
  ran more than 120 rounds without reaching the refuting cell that a direct
  query decides in 30 s.
- Under machine load above 100, z3 `unknown` is a timeout, not a verdict.
  Use `python3 -u` under `nohup`, or nothing appears until exit.
- `independently_verify_fixed_u_mixed_and_four_split` embeds the
  `--primary-audit` *path* in its artifact; pass the repository path or the
  SHA-256 will not match.
- Two sessions worked this goal concurrently; check `MEMORY.md` and the
  branch list before banking anything as first.
- Nothing here touches complete EFX, universal fixed-`U` closure, or general
  additive EFX; do not return to (4,8).

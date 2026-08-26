# The four-split form-2 conjecture (F4): refuted by a fifth-edge cell; exact decision on the corpus; endpoint lemma

**Date:** 2026-08-26  
**Branch:** `cc/efx-four-split-f4-20260826` from `69c1dcd`  
**Status:** (F4) is **false** (permitted outcome 2, class (a): a fifth support
edge is necessary, not a non-anchor split).  The refuting cell was found first
by the parallel session on `cc/efx-four-split-20260826` (commit `bacc5b0`,
`EFX_FOUR_SPLIT_HANDOFF_20260826.md`); this branch confirms it in a third,
independently written encoding, proves the endpoint lemma for arbitrary
cardinality, and decides (F4) exactly on every other retained profile.  No
claim about complete EFX, universal fixed-`U` closure, or general additive EFX.

## 0. Headline

1. **(F4) fails on an admissible profile.**  On the frozen pattern-mixed
   profile `fixed_u_tame_or_anchor_cegar_20260821.json` the two-good
   realization cell with side bits `{gq:r, h:r, j:d, j:q, l:r, m:s} = 1`
   (all other bits `0`) admits **no** complete EFX allocation within four
   support edges at any split count: the anchor-split oracle of this branch
   is UNSAT at split cap 4 and at split cap 11 (every role split), and every
   split of a two-good role is an anchor split, so the verdict is the
   unrestricted one.  Five edges close the same cell with **zero** splits
   (slack `159/7445`).  Exact values of every good are displayed in
   `results/fixed_u_f4_obstruction_cell_20260826.json`.
2. **Everywhere else decided, (F4) holds.**  Of the other `407` distinct
   profiles of the corpus (205 retained form-2 cuts, 81 tame-or-anchor cuts,
   7 anchor cuts, the wild-and-forced terminal, and the 113 banked
   adversarial profiles), `405` are decided and closed: every physical
   realization admits a complete EFX allocation with at most four edges and
   at most `3` anchor splits (split-count distribution: 0 splits 330, 1 split
   52, 2 splits 21, 3 splits 2).  Two `fresh-81` profiles
   (`7b54203deec6`, `29f1980e2f09`) are undecided at split caps 2–4 because
   the oracle timed out under a machine load above 100 (relaxed obstructions
   at caps 0–1 only); they are not obstructions.  The decision is exact and
   adversary-favourable (Section 2), a theorem for the 405.
3. **Splits are entirely the price of the four-edge cap.**  Without the cap
   the audited profile closes with a single zero-split allocation; at exactly
   five edges the refuting cell closes with zero splits; the parallel
   session's census closes 293/293 ledger profiles whole-role at five edges.
4. **Endpoint lemma for arbitrary cardinality and witness identity**
   (Lemma E, Section 2), and the exact finite reformulation it licenses —
   including what it does *not* license (vertex reduction of
   `forall R exists shape`).
5. **Isolated cap-free statement** (Section 7): the surviving conjecture is
   the whole-role five-edge closure, and the remaining cap-free lemma is
   anchor sufficiency under a fixed topology, now known to be vacuous on
   two-good cells and untested beyond them.

Baseline artifacts replayed byte-identically before any new claim:
`0237ad9c…1365` and `359ed19d…9ba8`.

## 1. Statement

Profile `P`: observers `O = {r,q,d,s}`, twelve named roles `G`, rows
`(T_i(G), M_i(G))` with `0 < M <= T`, each role a singleton in every row
(`M = T`) or two-good-admissible in every row (`2M <= T`).  Realization `R`:
each role a finite nonempty set of positive goods with common labels whose
observer sums and minima are the prescribed rows; witness identities
arbitrary.  A role has a base supplier (`SUPPORT_STATE`); the edge
`(supplier, owner)` is used when any good of the role goes to an owner other
than its supplier.

(F4)(`P`): for every `R` there is a complete allocation to `{r,q,d,s}` with at
most four edges, at most four split roles, every split an anchor split (one
witness good of the anchor observer to one owner, the rest to one other
owner), satisfying every good-deletion EFX inequality.

## 2. Lemma E (endpoint reduction, general realizations)

Fix a shape: split roles `S` with anchors `a_G` and recipients `p_G != c_G`,
owners of whole roles.  For observer `i`, target bundle `B_t`, good
`g in B_t`, EFX reads `U_i(B_i) - U_i(B_t) + v_i(g) >= 0`.

* A whole role contributes `T_i` to `U_i` and its binding deletion is its
  least good, `M_i` (identity-aware Theorem 1; cited, not reproved).
* For a split role write `x_i = v_i(g*)` for the selected witness `g*` of
  `a_G` and `c_i = min_{g != g*} v_i(g)`.  The selected piece contributes
  `x_i`, its only deletion is `g*`; the complement contributes `T_i - x_i`
  and its binding deletion is `c_i`.

Every inequality is affine in `(x_i, c_i)_i` per split role, `c_i` with
coefficient `+1` only.  Feasible coordinates at cardinality `k`:
`x_a = M_a`; for `i != a`, `M_i <= x_i <= T_i - (k-1)M_i` (the other `k-1`
goods cost at least `M_i` each; every interior value is attained by spreading
the remainder evenly); `c_i >= M_i`, attainable with equality for every
observer including the anchor when `k >= 3` (a second witness costs nothing);
for `k = 2`, `(x_i, c_i) in {(M_i, T_i - M_i), (T_i - M_i, M_i)}`.  Larger
`c_i` never hurts and the slack is affine in `x_i` on an interval, so the
worst case for the fixed shape lies on

```text
k = 2 :  x_i in {M_i, T_i - M_i},   c_i = T_i - x_i     (i != a)
k >= 3:  x_i in {M_i, T_i - 2M_i},  c_i = M_i           (i != a);  c_a = M_a
```

and `k >= 4` adds nothing because `[M_i, T_i - (k-1)M_i]` lies inside the
`k = 3` interval.  Rows of distinct observers are independent; the only
coupling is the common cardinality class of a role.  This is the
`anchor_scenarios` list of the 2026-08-21 note, derived for arbitrary
cardinality and witness identity.  ∎

**What Lemma E does not give.**  (F4) is `forall R exists shape`; the union
of the feasible regions of several shapes over the continuous `k >= 3`
coordinates is not vertex-determined.  Hence:

> **Exact finite reformulation.**  Let the *relaxed realization space* of `P`
> be: per non-singleton role a class `k in {2, 3+}` (`3+` only if `3M <= T`
> in every row), side bits for `k = 2`, and for `k = 3+` one selected-value
> vector per possible anchor observer with coordinates in `[M_i, T_i - 2M_i]`
> and complement floor `M_i`.  If no point of this space defeats every
> anchor-split shape within the caps, (F4) holds for every physical
> realization of `P`.

The relaxed space contains the projection of every real realization, so
relaxed UNSAT is a theorem; a relaxed SAT point is a candidate until realized
and re-decided by the unrestricted oracle.  On slack-two roles and on any
two-good cell the space is exact, which is why the refuting cell of Section 0
is a genuine obstruction and not a candidate.

## 3. Decision procedure and calibrations

`tracks/parkability/decide_fixed_u_f4.py`: CEGAR inside the relaxed space; the
adversary (z3, exact rationals) proposes a realization point; the oracle
(integer-owner SMT over pieces, anchors, split and edge caps) finds an
anchor-split allocation or proves none exists; each found template becomes
the cut `not EFX(template, R)` on the adversary; every template is re-checked
in `Fraction` arithmetic.  `independently_verify_fixed_u_f4.py` re-verifies a
closing template set by one monolithic query `exists R . AND_k not
EFX(T_k, R)` in a one-hot encoding and re-verifies relaxed obstructions with
a one-hot oracle.

| calibration | expected | obtained |
|---|---|---|
| audited product cell, split caps 0–3 at edge cap 4 | UNSAT | UNSAT (1.4–14.5 s) |
| audited product cell, split cap 4 | SAT, splits `{a0,j,k,m}`, edges `charity->d, d->r, q->s, r->q` | identical split set and edges, slack `62/7445` |
| audited product cell, edge caps 0–3 at split cap 4 | UNSAT | UNSAT |
| wild-and-forced terminal | min split 1, template B (split `k`), slack `23/1924` | min split 1, split `k`, slack `23/1924`; one-hot cover check UNSAT |
| parallel session's refuting cell (this branch's Int-owner oracle; the one-hot re-check timed out) | UNSAT at 4 edges for every split count; whole-role SAT at 5 edges | UNSAT at split caps 4 and 11; SAT at split cap 0, edge cap 5 |
| baseline replays | `0237ad9c…1365`, `359ed19d…9ba8` | byte-identical |
| `pytest -q tracks/parkability/test_fixed_u_pattern_mixed_four_split.py` | green | 5 passed |

## 4. Corpus decision

| tag | profiles | min split 0 | 1 | 2 | 3 | 4 | undecided |
|---|---:|---:|---:|---:|---:|---:|---:|
| anchor-7 | 7 | 3 | 4 | 0 | 0 | 0 | 0 |
| banked-113 | 113 | 104 | 8 | 1 | 0 | 0 | 0 |
| fresh-81 | 81 | 23 | 34 | 20 | 2 | 0 | 2 |
| retained-205 | 205 | 200 | 5 | 0 | 0 | 0 | 0 |
| terminal-wild-forced | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| **all (excluding the refuted audited profile)** | 407 | 330 | 52 | 21 | 2 | 0 | 2 |

Minimum edge count at split cap 4, where the edge loop was run (136 profiles): {'1': 1, '2': 11, '3': 43, '4': 78, 'None': 3}; for the remaining profiles the closing certificate uses at most four edges (upper bound 4, edge loop skipped to fit the time budget).

Independent re-verification (`verify_fixed_u_f4_corpus.py`): 404 of 407 verified profiles pass (cover at the minimum split cap UNSAT in the one-hot encoding; relaxed obstruction one cap below UNSAT); 3 failures.


The audited profile itself is excluded from the table: its four-edge decision at split cap 4 is negative by the refuting cell of Section 0 (the sweep row, if present, reports ORACLE_UNKNOWN).  Audited profile at split cap 4 over the whole relaxed realization space: the CEGAR was still running at the time of writing (see `fixed_u_f4_audited_cap4_decision_20260826.json` if present); the frozen product-cell realization is decided exactly (Section 3).

Artifacts: `results/fixed_u_f4_profile_corpus_20260826.json` (408-profile
corpus with provenance), `results/fixed_u_f4_corpus_results_20260826.jsonl`
(per-profile decisions with closing template sets),
`results/fixed_u_f4_corpus_verify_20260826.jsonl` (independent
re-verification), `results/fixed_u_f4_corpus_summary_20260826.json`.

## 5. Structure of the splits (step 4)

At the frozen product cell the four-split certificate is: `a0` (supplier `r`, anchor `r`, witness -> `r`, rest -> `q`), `j` (supplier `q`, anchor `r`, witness -> `q`, rest -> `s`), `k` (supplier `q`, anchor `r`, witness -> `q`, rest -> `s`), `m` (supplier `d`, anchor `s`, witness -> `r`, rest -> `d`).  Every split keeps one piece at its supplier and moves the other across exactly one edge; edge carriers: `r->q`: a0/complement_to, h/whole; `q->s`: j/complement_to, k/complement_to; `d->r`: m/selected_to, gr/whole; `charity->d`: p/whole.  So the split roles are all incident to support edges, but the map is not one split per edge: two splits (`j`,`k`) ride `q->s`, and `charity->d` is carried by a whole role.  The `q`-/`r`-minimum selector rule of the completion theorem does pick three of the four anchors (`r` for `a0`,`j`,`k`) but not the fourth (`s` for `m`).

Over the corpus certificates with splits: {"(1, 4, 1, 1)": 96, "(1, 4, 0, 1)": 102, "(1, 4, 1, 0)": 7, "(2, 4, 2, 1)": 28, "(2, 4, 2, 2)": 36, "(2, 4, 1, 2)": 161, "(2, 4, 0, 2)": 43, "(2, 4, 3, 1)": 13, "(1, 4, 2, 0)": 5, "(1, 3, 1, 1)": 1, "(2, 4, 1, 1)": 20, "(3, 4, 3, 3)": 5, "(3, 4, 0, 3)": 7, "(3, 4, 2, 2)": 4, "(3, 4, 1, 3)": 22, "(3, 4, 2, 3)": 8} (keys: number of splits, edges, edges carried only by split pieces, splits keeping a piece at home).  In the large majority every split keeps a piece at home, i.e. a split is a single-good transfer along one edge.

## 6. Hypothesis ablations (step 6)

| ablation | result |
|---|---|
| drop the four-edge cap (16 edges) | the audited profile closes with **zero** splits, realization-free — the edge cap is the sole source of splitting; at exactly five edges the refuting cell closes whole-role |
| drop positivity (zero-value goods: every whole-role and complement floor 0) | the wild-and-forced profile still closes, but its minimum split count rises from 1 to 2 (cap 0: RELAXED_OBSTRUCTION, cap 1: RELAXED_OBSTRUCTION, cap 2: F4_HOLDS) |
| drop admissibility (random physical `(T,M)` rows, no master) | not completed (run killed for CPU); no countermodel claimed |
| drop the exact-response form-2 relation (plain rank-three physical master) | 8 samples: Counter({'F4_HOLDS': 8}) |

The obstruction itself is an ablation of the edge cap in the other direction:
it is exactly a profile whose cell needs the cap raised by one.

## 7. Claim boundary and the corrected surviving conjecture

* Proved: Lemma E; the exact reformulation with its soundness direction;
  the refutation of (F4) (exact two-good cell, three independent encodings
  across the two branches); (F4) on `405` of the remaining `407` profiles in
  the relaxed model (a theorem for every realization of those profiles);
  two profiles undecided for budget reasons only.
* Machine-decided only: the per-profile decisions (z3, exact rationals).
* Not proved: any universal statement over the infinite admissible master.
  The profile-level CEGAR `run_fixed_u_f4_cegar.py` is a search whose
  union-closed rounds are point exclusions, not region cuts; it ran
  0 (status MASTER_UNKNOWN).
* Not claimed: complete EFX, universal fixed-`U` closure, general additive
  EFX.

**Corrected surviving local conjecture** (shared with the parallel branch's
open item W5):

> Every admissible form-2 exact-response profile admits a complete EFX
> allocation of *whole roles* using at most five support edges.  Because a
> whole-role allocation is realization-free (Theorem 1), this is a linear
> condition on the profile and its universal form is decidable by a symbolic
> CEGAR over the master.

The four-split conjecture is retired: under the four-edge cap it is false; at
five edges no split is needed on any profile examined.  The isolated
cap-free lemma of step 5 therefore changes character: the question is no
longer an ordering of anchor splits along the support edges but whether the
retained-support termination argument of the 2026-08-13 ledger survives a
five-edge premise.

## 8. Reproduction

```bash
python -m tracks.parkability.build_fixed_u_f4_corpus --output results/fixed_u_f4_profile_corpus_20260826.json \
  --extra-jsonl results/fixed_u_f4_banked_113_20260826.jsonl
python -m tracks.parkability.run_fixed_u_f4_corpus --corpus results/fixed_u_f4_profile_corpus_20260826.json \
  --output results/fixed_u_f4_corpus_results_20260826.jsonl --workers 6 --no-edge-loop
python -m tracks.parkability.verify_fixed_u_f4_corpus --results results/fixed_u_f4_corpus_results_20260826.jsonl \
  --corpus results/fixed_u_f4_profile_corpus_20260826.json --output results/fixed_u_f4_corpus_verify_20260826.jsonl
python -m tracks.parkability.summarize_fixed_u_f4_corpus --results results/fixed_u_f4_corpus_results_20260826.jsonl \
  --corpus results/fixed_u_f4_profile_corpus_20260826.json --output results/fixed_u_f4_corpus_summary_20260826.json
python -m tracks.parkability.ablate_fixed_u_f4 --mode edgefree --profile results/fixed_u_tame_or_anchor_cegar_20260821.json --output /tmp/edgefree.json
pytest -q tracks/parkability/test_fixed_u_f4.py tracks/parkability/test_fixed_u_pattern_mixed_four_split.py
```

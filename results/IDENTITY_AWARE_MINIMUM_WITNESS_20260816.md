# Identity-aware minimum-witness abstraction (2026-08-16)

**Branch:** `cc/efx-idwitness-20260816` (from `codex/efx-fixed-u-termination-20260813`)

**Predecessor:** `results/PHYSICAL_MINIMUM_ROLE_UNION_CHECKPOINT_20260814.md`,
`results/R2_RESPONSE_ROLE_CRITICAL_COMPRESSION_LEMMA_20260814.md`, and the
session-1 artifacts salvaged on `cc/efx-fixed-u-salvage-20260814`.

## Outcome

This note does **not** prove or refute the active fixed-`U` theorem, and it
produces **no** EFX counterexample.

It does three things.

1. It gives the identity-aware minimum-witness abstraction a formal
   definition, and settles exactly when that abstraction is complete: it is
   complete precisely on the *slack-two stratum*, where every named role has
   `T[i,g] < 3 M[i,g]` for some observer.
2. It **refutes the proposed witness-coincidence dichotomy** as stated.
   Realizability of a coincidence partition does not split into "two
   observers coincide" versus "all four are distinct".  It is a four-level
   ladder controlled by one numeric statistic per role, and the *shape* of a
   partition is provably irrelevant.
3. It **removes the banked one-minimum-split selector obstruction** as a real
   obstruction.  For that profile the identity-aware state machine is exactly
   complete, and an exhaustive terminating search shows every physical
   realization admits a complete EFX allocation within four support edges.
   The banked obstruction was an artifact of identity-blind conservatism.

The net effect on the program is negative for the countermodel hunt and
positive for the theorem: identity-awareness was the recommended next attack
surface, and on all `113` banked adversarial profiles it closes rather than
opens.

## 1. The abstraction

Fix the four observers `N = {r,q,d,s}` and the twelve named base/current
provenance roles `a0,a1,h,j,k,q0,l,e,m,gq,gr,p` of the exact-response chart.
A physical instance assigns each role `g` a nonempty finite set of goods and
each observer a positive additive valuation.

For a role `g` and observer `i` write

```text
T[i,g] = v_i(g),            M[i,g] = min_{x in g} v_i(x),
W_i(g) = argmin_{x in g} v_i(x).
```

The banked whole-role abstraction is the pair `(T, M)` together with the
common size-class disjunction: a role is a singleton for every observer
(`M = T`), or a multi-good packet for every observer (`2M <= T`).

> **Definition (identity-aware minimum-witness state).**
> A *witness selection* for role `g` is a map `w : N -> g` with
> `w(i) in W_i(g)`.  Its *coincidence partition* is `ker(w)`, an element of
> the set partitions of `N`.  Role `g` *admits* a partition `pi` when some
> witness selection induces it; write `Adm(g)` for the admitted set.
> The identity-aware state is `(T, M, {Adm(g)}_{g})`, and a *design* fixes
> one admitted `pi_g` per role.

`N` has four elements, so there are `B_4 = 15` candidate partitions.  These
are the fifteen coincidence partitions named in the session-1 synthesis.

Selection semantics matter.  The naive relation "`i ~ i'` when
`W_i(g) ∩ W_{i'}(g)` is nonempty" is **not** transitive — take
`W_1 = {a,b}`, `W_2 = {b,c}`, `W_3 = {c}` — so it induces no partition.
Quantifying over selections is what makes the state well defined under ties.

### 1.1 What identity is needed for

Whole-role moves never need it.  For a bundle `B` that is a union of whole
roles, `v_i(B) = sum_g T[i,g]` and `min_B v_i = min_g M[i,g]`, both
independent of which good realizes each minimum.  This is exactly why the
whole-role CEGAR of the 2026-08-14 checkpoint is a faithful abstraction, and
it is the content of Lemma C below.

Identity becomes load-bearing at the first *split*.  If role `g` is divided
into `P` (moved to owner `u`) and `Q` (retained by `w`), then for each
observer `i` exactly one side contains an `i`-witness; that side has minimum
`M[i,g]`, and the other side has minimum strictly greater.  Which side that
is, is precisely the identity datum, and it is constant across observers that
share a witness.

So the state that decides every EFX comparison for the four-edge / at-most-one
split-per-role move family is:

```text
(a) T[i,g], M[i,g]                        for every observer and role;
(b) for each split role, v_i(P)           the moved piece's value;
(c) for each split role, sigma : N -> {P,Q}   which side holds i's witness;
(d) for each split role and each observer whose witness lies off a side,
    that side's own minimum.
```

Item (c) is the identity-aware coordinate.  Item (d) is a residual that the
partition alone does not pin down — and Proposition 4 below identifies exactly
when it vanishes.

## 2. Lemma A — block-count realizability (proved)

> **Lemma A.** Let role `g` carry totals `T[i,g]` and minima `M[i,g] > 0`, and
> let `pi` be a partition of `N` with `b = |pi|` blocks.  Then `g` can be
> realized as a physical role with these totals and minima and with
> `pi in Adm(g)` **if and only if**
>
> ```text
> T[i,g] >= b * M[i,g]   for every observer i.
> ```
>
> In particular admission depends on `pi` only through `b`: every partition
> with the same number of blocks is admitted or refused together, and the
> shape of the partition is irrelevant.

*Proof.*

(⇐) Give each block `j = 1..b` a distinct good `x_j`.  For observer `i` in
block `j` set `v_i(x_j) = M[i,g]` and spread the remainder
`T[i,g] - M[i,g]` evenly over the other `b - 1` goods, giving each the value
`M[i,g] + (T[i,g] - b M[i,g])/(b-1)`.  The column sums to `T[i,g]`, every
value is at least `M[i,g]`, and `x_j` attains it, so the minimum is `M[i,g]`
and `w(i) = x_{block(i)}` is a witness selection with `ker(w) = pi`.  All
values are positive.  For `b = 1` and a multi-good role, use the two goods
`M[i,g]` and `T[i,g] - M[i,g]` instead.

(⇒) Let `w` be a witness selection with `ker(w) = pi`, and let
`x_1,...,x_b` be its `b` distinct image goods.  Fix an observer `i`, in block
`j`.  Then `v_i(x_j) = M[i,g]`, and `v_i(x_l) >= M[i,g]` for every other `l`
because `M[i,g]` is the minimum over all of `g`.  Since the `x_l` are distinct
goods of `g` and every value is positive,

```text
T[i,g] >= sum_{l=1..b} v_i(x_l) >= M[i,g] + (b-1) M[i,g] = b M[i,g].
```

∎

The corresponding statistic is the **role slack**

```text
rho(g) = min_{i in N} floor( T[i,g] / M[i,g] ),
```

and Lemma A says `pi in Adm(g)` iff `|pi| <= rho(g)` (with `rho = 1` forced
for a singleton role).  This replaces the fifteen-row partition table by a
four-level ladder.

**This refutes the proposed dichotomy.**  The brief's candidate structure was
"either two observers share a witness, collapsing the case count, or the
witnesses are distinct and a rotation argument applies."  There is no such
two-case split.  Admission is monotone in a single integer, and the seven
two-block partitions behave identically to one another, as do the six
three-block partitions.  No rotation or exchange argument is needed or
available at this level, because the shape carries no information.

## 3. Lemma B — cardinality bound and exhaustiveness (proved)

> **Lemma B.** A physical role `g` with `k` goods satisfies
> `T[i,g] >= k * M[i,g]` for every observer, hence `k <= rho(g)`.
> Consequently, if `rho(g) <= 2` then `g` has at most two goods, and when it
> has exactly two its value column is forced to be `{M[i,g], T[i,g]-M[i,g]}`
> for every observer `i`.

*Proof.* Every good of `g` is worth at least `M[i,g]` to observer `i`, and
there are `k` of them, so `T[i,g] >= k M[i,g]`; minimise over `i`.  For the
second part, a two-good column `(a, T-a)` with minimum `M` forces
`{a, T-a} = {M, T-M}`. ∎

> **Corollary B1 (exhaustive family at slack two).** If `rho(g) <= 2` for
> every role, then every physical instance realizing `(T, M)` is obtained,
> up to relabelling the two goods of each multi-good role, by choosing one
> side pattern `s[g,.] : N -> {0,1}` per multi-good role.  The number of such
> instances is `2^(3 m)` for `m` multi-good roles after the relabelling
> symmetry is quotiented out, and the induced coincidence partition of role
> `g` is `ker(s[g,.])`, ranging over the eight partitions of `N` into at most
> two blocks.

This is what converts the identity-aware search below from a heuristic sample
into an exact decision for the profiles that satisfy its hypothesis.

## 4. Lemma C and Proposition 4 — where identity is visible (proved)

> **Lemma C (split-locality).** In a two-good realization, the multiset
> `{v_i(g:0), v_i(g:1)}` equals `{M[i,g], T[i,g]-M[i,g]}` for every observer
> and every side pattern.  Hence for any allocation that does **not** split
> role `g` between two distinct recipients, neither any bundle total nor any
> bundle minimum depends on `s[g,.]`.

*Proof.* Immediate from Lemma B: totals and minima of the pair are pattern
independent, and if both goods sit in one bundle the bundle's total and its
contribution to the bundle minimum are determined by that multiset. ∎

> **Proposition 4 (exact completeness boundary).** On the slack-two stratum
> the identity-aware state `(T, M, {pi_g})` determines the physical instance
> up to isomorphism, hence decides every EFX comparison of every allocation.
> Above that stratum it does not: when `rho(g) >= 3` the residual datum (d) of
> §1.1 is genuinely free, and `(T, M, {pi_g})` has realizations with different
> off-witness side minima.

*Proof.* The first half is Corollary B1.  For the second, take `rho(g) = 3`
and compare the three-good column `(M, M + t, T - 2M - t)` for different
admissible `t > 0`: all share `T`, `M` and the same witness selection kernel,
but the minimum of the two-good side `{x_2, x_3}` differs with `t`. ∎

So the identity-aware abstraction is **exactly complete at slack two and
strictly incomplete above it**.  That is the sharpest available statement of
what this enrichment buys, and it is the honest limit of the present note.

## 5. Partition realizability tables

### 5.1 Premise level — all fifteen partitions are admitted at every role

`run_identity_aware_partition_admission_sweep.py` pushes the Lemma A
condition `T[i,g] >= b M[i,g]` into the exact-response form-2 physical master
(the same `build_physical_master` used by the banked checkpoint) and asks for
each role and each `b in {2,3,4}` whether the fixed-`U` premises admit it.

Result: **`sat` in all 36 cells**, each with an exact rational admission
witness recorded in the output.

| block count `b` | partitions of that width | roles admitting (of 12) | verdict |
|---|---|---|---|
| 1 | 1 | 12 | realizable (trivially) |
| 2 | 7 | 12 | realizable, exact witness |
| 3 | 6 | 12 | realizable, exact witness |
| 4 | 1 | 12 | realizable, exact witness |

So all `15` coincidence partitions are realizable at every one of the twelve
roles under the fixed-`U` premises: **15 proved realizable, 0 refuted, 0
open**.  No partition can be discarded by a premise argument.  The
`120` per-(role, partition) verdicts follow from the `36` block-count cells by
Lemma A's shape-independence.

Claim tier: exact-computational (z3 `sat` with recorded rational witnesses,
each re-checked in exact arithmetic by the script).

### 5.2 Profile level — the slack ladder bites hard

Admission at a *fixed* banked profile is far more restrictive.
`audit_identity_aware_witness_realizability.py` constructs and re-verifies all
`15 x 12` cells per profile in closed form, with no solver.

Form-2 whole-role obstruction profile
(`exact_response_form2_physical_minimum_cegar_checkpoint_20260814.json`):

| role | slack `rho` | admitted widths | partitions admitted (of 15) |
|---|---|---|---|
| `a0` | 3 | 1,2,3 | 14 |
| `a1`, `e`, `gq`, `gr`, `h`, `j`, `l` | 2 | 1,2 | 8 |
| `m` | 99 | 1,2,3,4 | 15 |
| `p` | 236 | 1,2,3,4 | 15 |
| `k`, `q0` | 1 (singleton) | 1 | 1 |

Form-2 one-minimum-split obstruction profile
(`exact_response_form2_one_minimum_split_cegar_20260814.json`):

| role | slack `rho` | admitted widths | partitions admitted (of 15) |
|---|---|---|---|
| `a0`, `a1`, `e`, `gq`, `l`, `p`, `q0` | 2 | 1,2 | 8 |
| `gr`, `h`, `j`, `k`, `m` | 1 (singleton) | 1 | 1 |

The second profile has `rho(g) <= 2` for **every** role.  By Corollary B1 its
two-good side-pattern family is therefore the *complete* set of physical
realizations of its totals and minima.

The audit also certifies mechanically, on both profiles, that admission
depends only on block count and that the admitted widths are exactly those at
most the slack — Lemma A's two conclusions, checked cell by cell.

Claim tier: exact-computational, closed form, solver free.

## 6. The identity-aware decision — result and countermodel search

`run_identity_aware_witness_side_cegar.py` alternates

- a **side-pattern master** over Booleans `s[g,i]` (with `s[g,r]` pinned to
  break the good-relabelling symmetry), seeking a pattern that defeats every
  allocation found so far, against
- the **exact concrete four-support-edge EFX decision** for the pattern it
  proposes, reusing the banked
  `decide_physical_minimum_countermodel_four_edge.build_decision` encoding
  with unrestricted splits.

Every side pattern realizes the same `T` and `M`, so a concrete `unsat` next
to a satisfiable canonical baseline would have proved that totals and minima
do not determine the four-edge gate.  That was the target theorem.

**It does not happen.**  Both runs terminate with the master `unsat`:

| profile | multi-good roles | side patterns covered | CEGAR rounds | verdict |
|---|---|---|---|---|
| one-minimum-split obstruction | 7 | `2^21 = 2,097,152` | 11 | every pattern admits a four-edge EFX allocation |
| whole-role obstruction | 10 | `2^30 = 1,073,741,824` | 19 | every pattern admits a four-edge EFX allocation |

An `11`-allocation menu covers all two million realizations of the first
profile; a `19`-allocation menu covers all billion realizations of the second.
The canonical baseline on the first profile uses support edges
`charity->d, d->s, r->q, s->r` and splits roles `gq` and `l`.

Batch replay over the banked adversarial population
(`run_identity_aware_witness_side_batch.py`, all four form-2 physical CEGAR
traces) reproduces this on every profile; see §7.

### 6.1 Consequence — the one-minimum-split obstruction dissolves

The banked `exact_response_form2_one_minimum_split_cegar_20260814.json`
records status `SAT_ONE_MINIMUM_SPLIT_SELECTOR_OBSTRUCTION`.  Reading its
driver explains why.  Its docstring states that when a role is split into a
least good and its complement, "both pieces are conservatively assigned least
good value `M`".  That is sound — the true minimum of either piece is at least
`M`, so demanding EFX with deletion floor `M` is a strengthening — but it is
strictly weaker than asking the real question, because no actual realization
has both pieces at minimum `M` while the totals stay at `M` and `T-M`.  The
selector is identity-blind by construction: it behaves as if every observer's
witness could be on whichever side hurts most, independently per constraint.

Combining §5.2 and §6:

> **Result (exact, for this profile).** Every role of the form-2
> one-minimum-split obstruction profile has slack at most two.  Hence every
> physical instance realizing its totals and minima lies in the two-good
> side-pattern family, and all `2^21` of them admit a complete EFX allocation
> using at most four support-supplier/recipient pairs.  The banked
> one-minimum-split selector obstruction is therefore an artifact of the
> selector's conservatism, not an obstruction to the four-edge conclusion.

This is the sharpest concrete finding of the session.  It retires a live
terminal rather than adding one.

Claim tier: exact-computational, and exhaustive for this profile by
Corollary B1.  It does **not** extend to the whole-role obstruction profile,
whose roles `a0`, `m`, `p` have slack `3`, `99`, `236`; there the same
`unsat` covers only the two-good realizations, and realizations with three or
more goods per role remain unexamined.

## 7. Test against the banked adversarial population

`run_identity_aware_witness_side_batch.py` replays the identity-aware CEGAR on
every distinct totals/minima profile appearing in the four banked form-2
physical CEGAR traces.

**Population correction.** The task brief cites `173` exact adversarial
profiles.  That figure is not reproducible from the banked artifacts.  The
traces contain `100 + 101 + 7 + 3 = 211` rounds, which reduce to **`111`
distinct `(totals, minima)` profiles** — the stage-2 canonical run resumed
from stage 1 and replayed its cuts, so the two overlap almost completely.
Adding the traces' terminal countermodel profiles gives **`113` distinct
profiles** in total, which is the population the batch examines.  The
qualitative claim attached to the figure is correct: every round does carry a
four-edge EFX allocation.  The count should be corrected wherever `173` is
cited.

**Batch verdict.**

| quantity | value |
|---|---|
| distinct profiles examined | `113` |
| `UNSAT_EVERY_SIDE_PATTERN_ADMITS_A_BANKED_ALLOCATION` | `113` |
| identity-sensitive countermodels found | `0` |
| `UNKNOWN` or round-limited | `0` |
| canonical baselines satisfiable | `113` |
| profiles where the two-good family is exhaustive (`rho <= 2` everywhere) | `68` |
| CEGAR rounds per profile | min `1`, max `28`, total `607` |

The maximum role slack across the population is `2` on `68` profiles, `3` on
`11`, `4` on `12`, and `5` or more on the remaining `22`.  The identity-aware
state machine therefore decides all `113` banked profiles without a single
unknown, and for the `68` exhaustive ones the decision is complete for every
physical realization, not merely for the two-good family.

Per-profile detail is in `results/identity_aware_witness_side_batch_form2.json`.

## 8. Verification

```bash
pytest -q tracks/parkability/test_identity_aware_witness.py
```

Recorded result: `9 passed in 0.12s`.  The tests check that four observers
give fifteen partitions with widths `1,7,7,...`; that the Lemma A threshold is
exactly `T >= b M` across a sweep of ratios; that admission is blind to
partition shape; that role cardinality is bounded by the slack; that a
singleton role admits only the one-block partition; and that every side
pattern preserves totals and minima.

Replay commands (inputs are read from the salvage branch):

```bash
mkdir -p /tmp/efx-idw-inputs
for f in exact_response_form2_one_minimum_split_cegar_20260814.json \
         exact_response_form2_physical_minimum_cegar_checkpoint_20260814.json \
         exact_response_form2_canonical_physical_cegar_20260814.json \
         exact_response_form2_canonical_physical_cegar_stage2_20260814.json; do
  git show cc/efx-fixed-u-salvage-20260814:results/$f > /tmp/efx-idw-inputs/$f
done

python -m tracks.parkability.audit_identity_aware_witness_realizability \
  --profile /tmp/efx-idw-inputs/exact_response_form2_physical_minimum_cegar_checkpoint_20260814.json \
  --profile /tmp/efx-idw-inputs/exact_response_form2_one_minimum_split_cegar_20260814.json \
  --output results/identity_aware_witness_realizability_audit.json

python -m tracks.parkability.run_identity_aware_partition_admission_sweep \
  --output results/identity_aware_partition_admission_sweep_form2.json \
  --form-index 2 --timeout-seconds 45

python -m tracks.parkability.run_identity_aware_witness_side_cegar \
  --profile /tmp/efx-idw-inputs/exact_response_form2_one_minimum_split_cegar_20260814.json \
  --output results/identity_aware_witness_side_cegar_one_minimum_split.json \
  --maximum-rounds 60 --timeout-seconds 60

python -m tracks.parkability.run_identity_aware_witness_side_cegar \
  --profile /tmp/efx-idw-inputs/exact_response_form2_physical_minimum_cegar_checkpoint_20260814.json \
  --output results/identity_aware_witness_side_cegar_whole_role_obstruction.json \
  --maximum-rounds 80 --timeout-seconds 90

python -m tracks.parkability.run_identity_aware_witness_side_batch \
  --trace /tmp/efx-idw-inputs/exact_response_form2_one_minimum_split_cegar_20260814.json \
  --trace /tmp/efx-idw-inputs/exact_response_form2_physical_minimum_cegar_checkpoint_20260814.json \
  --trace /tmp/efx-idw-inputs/exact_response_form2_canonical_physical_cegar_20260814.json \
  --trace /tmp/efx-idw-inputs/exact_response_form2_canonical_physical_cegar_stage2_20260814.json \
  --output results/identity_aware_witness_side_batch_form2.json \
  --maximum-rounds 40 --timeout-seconds 45
```

Imported session-1 inputs, verified against the sha256 values recorded inside
the banked JSONs themselves:

```text
466f8350ce854a39f9aa6520f7f7a3ed6f0861ee6692a08450adc2713768ccec  tracks/parkability/decide_physical_minimum_countermodel_four_edge.py
452d58bea46009136d6f79162be76f3a79640bd0d3c5ace009403983706feb18  tracks/parkability/run_exact_response_one_minimum_split_cegar.py
24872d6bf5e5b75ae2dc0de8faa453346806c2bc97f2cd38d975e935d130896b  exact_response_form2_one_minimum_split_cegar_20260814.json
e396f24dfb60f0ea796e6dea46962a3ac4eb3794ee6e6e87932f9fa94eff6963  exact_response_form2_physical_minimum_cegar_checkpoint_20260814.json
8762ceec28c9c4d6fac06f05aa8b5df7446c851dd644b84a3470577839ab032c  exact_response_form2_one_minimum_obstruction_physical_decision_20260814.json
```

New script and output sha256 values are recorded in §10.

## 9. Claim ledger

**Proved (hand proof in this note).**

- Lemma A: a `b`-block coincidence partition is realizable at a role iff
  `T[i,g] >= b M[i,g]` for every observer; admission is blind to partition
  shape.
- Lemma B and Corollary B1: a physical role has at most `rho(g)` goods; at
  slack two the two-good side-pattern family is every realization.
- Lemma C: in a two-good realization, witness identity is invisible to any
  allocation that does not split the role.
- Proposition 4: the identity-aware state is exactly complete on the
  slack-two stratum and strictly incomplete above it.
- Refutation of the proposed witness-coincidence dichotomy as a two-case
  structure.

**Exact-computational.**

- All `15` partitions are premise-realizable at all `12` roles of the
  exact-response form-2 physical master, with rational witnesses.
- Both banked form-2 adversarial profiles: every two-good realization admits a
  complete EFX allocation within four support edges (`2^21` and `2^30`
  realizations, covered by `11` and `19` allocations).
- The one-minimum-split obstruction profile is exhaustively resolved: its
  selector obstruction is not a four-edge obstruction.

**Evidence.**

- The same verdict across all `113` distinct banked adversarial profiles, with
  zero unknowns and zero countermodels; `68` of the `113` are exhaustive and
  so are exact-computational rather than evidence.  The remaining `45` are
  discovery evidence for a general theorem, not a proof of one.

**Open.**

- Realizations with three or more goods per role, for profiles whose slack
  exceeds two. The whole-role obstruction profile has roles at slack `3`,
  `99`, `236`; the present search does not touch them.
- Whether the fixed-`U` premises force some role to slack two — §5.1 says they
  do not force it globally, but a *joint* condition over roles is untested.
- A general theorem behind the batch evidence: does every fixed-`U`-admissible
  slack-two profile admit a four-edge EFX allocation for every side pattern?
- Everything the predecessor checkpoint left open: chart coverage, observer
  safety after splits, and closure of the decorated-response recurrence.

Nothing here resolves four-agent or general additive EFX.

## 10. Next steps, in priority order

1. **Symbolic-value identity CEGAR.** Replace the two-good side pattern by a
   z3-symbolic role realization with up to `min(rho(g), c)` goods, values
   constrained to sum to `T` with minimum `M`. This makes the `unsat` verdicts
   exhaustive above slack two and is the direct continuation of §6.
2. **Prove the slack-two theorem.** The verdict is uniform over all `113`
   profiles and exact on the `68` slack-two ones.  Lemma C says only split
   roles matter and the canonical baselines split at most three roles, so the
   target is a bounded statement: for a slack-two profile, a four-edge EFX
   allocation exists that is robust to the side pattern of its split roles.
   This looks reachable by hand.
3. **Re-audit the one-minimum-split driver.** Since its obstruction is an
   artifact, `run_exact_response_one_minimum_split_cegar.py` should either be
   re-run with the identity-aware deletion floor (floor `M` only on the side
   carrying the witness, `T-M` on the other) or retired in favour of the
   side-pattern encoding.
4. **Correct the `173` figure** wherever it is cited downstream: the banked
   traces hold `111` distinct round profiles, `113` counting their terminal
   countermodels.
5. **External review**, per the predecessor's standing list: rebuild the
   form-2 premise ledger without importing the master builder, and
   independently enumerate the four-edge menu.

## 11. Artifact sha256

Recorded at freeze.  Each output JSON also carries its driver's
`script_sha256` self-recorded inside it.

```text
594a9e4890f46400fca6357a2ac9b1f517f42dfe01a36b318f3e0daa454aa06a  tracks/parkability/audit_identity_aware_witness_realizability.py
1b33ee9f54eccfc4f862da73f148cdb3e73e2b19c47c2c41be40891d9e8dfd2c  tracks/parkability/run_identity_aware_partition_admission_sweep.py
4f584558d4c638b371062298445270b8ec959073f9250fc38991478099b6ffee  tracks/parkability/run_identity_aware_witness_side_cegar.py
cbf568189655a099db08d6519adbb9f8cddb4c706623e66712e5543aea2e7748  tracks/parkability/run_identity_aware_witness_side_batch.py
2bc0e51a5c9eb444814669db872ff8bbed7eb371a3a5e454140cf953ec126ebb  tracks/parkability/test_identity_aware_witness.py
2e5c9d13b7167e790619333d58427b21fce76a2d00d1b56b562afa26841b8314  results/identity_aware_witness_realizability_audit.json
e7ce8125dc70e62d4c2d77129c5002fc6e5490e00adef9fb95d94ffaf2d19dc4  results/identity_aware_partition_admission_sweep_form2.json
e67935f76c0fe35fbf722d4741c05aaf1732c8e62a67ddbeb73a59d5b20fb159  results/identity_aware_witness_side_cegar_one_minimum_split.json
22dc50c17982b4fa46859c92a17aa39bbe84e9ca0dc21ca62e64ab7f372255fb  results/identity_aware_witness_side_cegar_whole_role_obstruction.json
a9819bd56688895cd8066bb715d1e55930cbff0e74e57be16c977e93db758947  results/identity_aware_witness_side_batch_form2.json
```

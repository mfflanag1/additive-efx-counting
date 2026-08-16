# Realization-free reduction and the slack-two theorem (2026-08-16)

**Branch:** `cc/efx-idwitness-20260816`

**Predecessor:** `results/IDENTITY_AWARE_MINIMUM_WITNESS_20260816.md`, whose
open items 1-3 this note executes.

## Outcome

The headline is that the slack-two theorem is **true and provable, and the
slack hypothesis is not needed**.

1. **No countermodel appeared above slack two.** All `113` banked adversarial
   profiles are closed, and the verdict is exhaustive over *every* physical
   realization — every role cardinality, every witness identity — not merely
   over realizations with two or three goods per role.  Identity-necessity
   above slack two is not resurrected; it is closed off.
2. **Theorem 1 (realization-free reduction) is proved by hand** and replaces
   the intended slack-two theorem with a strictly stronger statement that
   carries no slack hypothesis.  The slack-two theorem is Corollary 2.
3. **The banked `SAT_ONE_MINIMUM_SPLIT_SELECTOR_OBSTRUCTION` is superseded.**
   Its profile is closed realization-free by an eight-allocation menu that
   splits role `e`, and the chart-level rerun with the repaired oracle passes
   the iteration at which the old driver stopped.

The mechanism behind all three is one observation the predecessor note had
already isolated but not exploited: **witness identity is invisible except at a
split, and a role that no allocation splits is exactly modelled by its total
and its minimum whatever its cardinality.**  Making the search prefer
allocations that never split a wide role converts the whole question into the
slack-two calculus, where Lemma B forces the value column outright.

Nothing here resolves four-agent or general additive EFX.

## 1. The theorem

### 1.1 Notation

As in the predecessor note: four observers `N = {r,q,d,s}`, the twelve named
roles of the exact-response chart, and for role `g` and observer `i`

```text
T[i,g] = v_i(g),   M[i,g] = min_{x in g} v_i(x),   rho(g) = min_i floor(T[i,g]/M[i,g]).
```

A *realization* `R` of a profile `(T, M)` assigns each role a finite nonempty
set of goods and each observer a positive additive valuation reproducing `T`
and `M`.  Call a multi-good role **tame** when `rho(g) <= 2` and **wild** when
`rho(g) >= 3`.  A menu of allocations is **tame** when no allocation in it
splits a wild role between two owners.

**Marking convention.** The corpus has no `C2`/`C3` licensing labels — a
repository-wide search finds only equation tags of that shape — so each step
below is marked either *(abstraction)*, meaning it follows from Lemmas A/B/C of
the predecessor note and needs nothing further, or *(additive)*, meaning it
uses additivity of the valuations and must be revisited for any wider
valuation class.

### 1.2 The cardinality-free form of split-locality

Lemma C of the predecessor note is stated for two-good realizations.  It holds
at every width, and that is what does the work here.

> **Lemma C′ (cardinality-free split-locality).** Let `g` be a role of any
> cardinality `k >= 1` in a realization `R`, and let `A` be an allocation
> giving all of `g` to a single owner `u`.  Then for every observer `i`:
>
> 1. `g` contributes exactly `T[i,g]` to `v_i(B_u)`;
> 2. `min_{x in g} v_i(x) = M[i,g]`, and every other good of `g` is worth at
>    least `M[i,g]` to `i`.
>
> Consequently the EFX constraints that `g` contributes inside `B_u` are
> exactly those contributed by the two-good stand-in `{M[i,g], T[i,g]-M[i,g]}`
> — or by the singleton `{M[i,g]}` when `T[i,g] = M[i,g]` — independently of
> `k` and of every witness identity.

*Proof.* (1) is additivity of `v_i` over the goods of `g` *(additive)*.  (2) is
the definition of `M[i,g]` as the minimum of the column *(abstraction)*.

For the constraint claim, EFX for observer `i` against bundle `B_u` is the
family `v_i(B_i) >= v_i(B_u) - v_i(x)` over `x in B_u` *(additive: deleting one
good subtracts its value)*.  Among the `x` lying in `g` the tightest member is
the one minimising `v_i(x)`, that is any `i`-witness, and it reads
`v_i(B_i) >= v_i(B_u) - M[i,g]`; by (2) every other `x in g` yields a strictly
weaker inequality, so the family restricted to `g` is equivalent to that single
constraint.  The two-good stand-in has total `T[i,g]` by construction and
offers `M[i,g]` as its smallest good, so it generates the same bundle total by
(1) and the same tightest constraint. ∎

The point to record for the class map is that **both** uses of additivity are
in the same place: the bundle value is a sum, and a deletion subtracts a value.
A submodular or XOS class breaks (1) and breaks the reduction of the deletion
family to its minimiser, so Lemma C′ is additive-scoped as stated.

### 1.3 Recalled from the predecessor

> **Lemma B.** A role with `k` goods satisfies `T[i,g] >= k M[i,g]` for every
> observer, so `k <= rho(g)`.  Hence a tame multi-good role has exactly two
> goods and the forced column `{M[i,g], T[i,g]-M[i,g]}` for every `i`.

*(abstraction; its own proof is additive.)*  For a tame role the only remaining
freedom is therefore the **side pattern** `s[g,·] : N -> {0,1}` naming the good
that carries each observer's minimum.  Swapping the two goods is a relabelling,
so patterns are taken modulo the global flip and `s[g,r]` may be pinned to `0`,
leaving exactly `8` classes per tame role.

### 1.4 The reduction theorem

> **Theorem 1 (realization-free reduction).** Let `(T, M)` be a profile and let
> `A_1, ..., A_n` be a *tame* menu of complete allocations, each within the
> support-edge budget.  Suppose that for every side pattern `s` of the tame
> roles, some `A_j` is EFX in the canonical two-good model under `s`.
>
> Then for **every** physical realization `R` of `(T, M)` — every cardinality
> of every role, every witness identity — some `A_j` induces a complete
> allocation of `R` that is within the support-edge budget and EFX.

*Proof.* Fix a realization `R`.

*The tame roles.*  By Lemma B each tame multi-good role of `R` has exactly two
goods with the forced column; let `s_R[g,i]` be the index of the good carrying
observer `i`'s minimum, normalised by the relabelling so `s_R[g,r] = 0`.  So
`R` restricted to the tame roles **is** the canonical two-good model under the
pattern `s_R` — not merely equivalent to it *(abstraction)*.

*The choice.*  By hypothesis some `A_j` is EFX in the two-good model under
`s_R`.  Fix that `A_j`.

*Transport to `R`.*  `A_j` splits no wild role, so each wild role sits entirely
in one bundle, and Lemma C′ applies to it: its contribution to that bundle's
total is `T[i,·]` and the tightest deletion constraint it contributes is at
`M[i,·]`, exactly as for the two-good stand-in used by the model.  Each tame
role is realised identically in `R` and in the model, split or not.  Hence for
every observer `i` and every owner `u`,

```text
v_i^R(B_u) = v_i^model(B_u)      and      min_{x in B_u} v_i^R(x) = min_{x in B_u} v_i^model(x),
```

the first by additivity over roles *(additive)* and the second because the
minimum over a bundle is the minimum over its roles of the per-role minima,
which agree role by role *(abstraction, via Lemma C′(2))*.  EFX for `i` against
`B_u` is equivalent to `v_i(B_i) >= v_i(B_u) - min_{x in B_u} v_i(x)`
*(additive)*, so `A_j` is EFX in `R` exactly because it is EFX in the model.

*Completeness and budget.*  `A_j` assigns every wild role wholly to one owner
and every tame role to one or two owners; transporting it to `R` places every
good of `R`, and the set of support-supplier/recipient pairs it uses is
determined by which owners receive goods of which role, which is unchanged.
∎

> **Corollary 2 (slack-two theorem).** On the slack-two stratum every
> multi-good role is tame, so every menu is tame.  Hence if for each of the
> eight side patterns per role some complete four-support-edge EFX allocation
> exists in the two-good model, then **every** realization of the profile
> admits a complete four-support-edge EFX allocation.  The two-good
> eight-pattern family is a complete decision procedure on that stratum.

This is the statement the brief asked for, and Theorem 1 shows the slack-two
hypothesis was never the load-bearing one: what matters is that the *split*
roles be tame, not that all roles be.

> **Corollary 3 (whole-role universality).** A profile admitting a single
> complete four-support-edge EFX allocation that splits **no** role is closed
> at every cardinality and every witness identity, whatever its slack — the
> menu `{A}` is tame and the pattern hypothesis is vacuous.

> **Remark 4 (observer factorization).** Every EFX constraint indexed by
> observer `i` involves only `v_i`, and `s[g,i]` perturbs only `v_i`.  So the
> pattern space factorizes over observers: a *single* allocation `A` is EFX in
> every realization iff, for each observer separately and each of the
> `2^|S(A)|` side choices of that observer alone, its own constraints hold.
> Deciding universality of one allocation is `4 · 2^|S(A)|` checks, not
> `2^(4|S(A)|)`.  This is why the menus below stay small.

### 1.5 What is *not* proved

Theorem 1 is a reduction, not an existence statement.  It says that *if* a tame
menu covering the patterns exists then the profile is closed for every
realization; it does not prove that a fixed-`U`-admissible profile always
admits one.  That is the chart-level question, and §3 attacks it directly.

## 2. Exact-computational results

### 2.1 Whole-role census — Corollary 3 does most of the work

`census_whole_role_universality.py` finds, for each distinct banked profile,
the least number of roles that any complete four-support-edge EFX allocation
must split, in the canonical realization.

| least split count | profiles |
|---|---|
| `0` | `104` |
| `1` | `9` |
| `>= 2` | `0` |

So `104` of the `113` profiles are closed outright by Corollary 3, **at every
cardinality**, with no slack hypothesis and no solver quantification over
identities.  `40` of those `104` are above slack two, where the predecessor
note recorded the question as open.  Zero-split allocations are re-audited
directly in the `(T, M)` abstraction — bundle totals as sums of `T`, bundle
deletion floors as minima of `M` — so the audit is itself realization-free.

The `9` profiles that need a split need exactly one, and in every case the role
it splits is tame:

| profile index | max role slack | split role | wild roles | split role tame |
|---|---|---|---|---|
| `5` | `3` | `gq` | `l` | yes |
| `6`, `7` | `2` | `gq` | — | yes |
| `11` | `236` | `l` | `a0`, `m`, `p` | yes |
| `14` | `7` | `a0` | `gq` | yes |
| `102` | `2` | `m` | — | yes |
| `103` | `89` | `m` | `a1` | yes |
| `104` | `30` | `m` | `a1` | yes |
| `107` | `2` | `a1` | — | yes |

Claim tier: exact-computational, with every accepted allocation re-audited
outside z3 in exact rational arithmetic.

### 2.2 Realization-free universality — the full verdict

`run_realization_free_universality_cegar.py` runs the side-pattern CEGAR with
one added constraint: **no wild role may be split**.  By Theorem 1 a master
`unsat` is then exhaustive over all realizations.

| quantity | value |
|---|---|
| distinct profiles examined | `113` |
| `UNSAT_EVERY_REALIZATION_ADMITS_A_BANKED_ALLOCATION` | `113` |
| realization-free (all cardinalities, all identities) | `113` |
| countermodels above slack two | `0` |
| `UNKNOWN` or round-limited | `0` |
| profiles carrying at least one wild role | `45` |
| maximum wild roles on one profile | `5` |
| CEGAR rounds per profile | min `1`, max `18`, total `430` |

`46` profiles need a single allocation; the rest need a menu, never more than
`18`.  Every allocation is re-audited in exact rational arithmetic, and a
separate audit confirms directly that no accepted allocation splits a wild
role — the hypothesis Theorem 1 rests on is checked, not assumed.

**This is the answer to open item 1, by a stronger route than the item
proposed.**  The item asked for symbolic values at up to `min(rho(g), 3)` goods
per role, which would have been exhaustive only for roles of slack exactly
three — `11` of the `45`, since by Lemma B a role of slack `>= 4` can carry
four or more goods.  Restricting the *allocation* instead of enumerating the
*realization* removes the cap entirely: the verdict below holds at every
cardinality, including the roles at slack `99`, `133` and `236`.

Per-profile verdicts are in `results/realization_free_universality_form2.json`.
Every one of the `45` slack-`> 2` profiles reads EXHAUSTIVE-UNSAT.

### 2.3 Why no countermodel is available above slack two

Worth recording, because it explains the negative result rather than merely
reporting it.  A wild role is exactly where the identity-blind conservatism of
the old selector becomes *realizable*: with `rho(g) >= 3` the column
`(M, M, T-2M)` exists, so a role can be split into two pieces **both** of which
carry a given observer's minimum, which is what the blind floor assumed.  That
is the mechanism by which identity-necessity could have returned.

It does not return, because on this population the allocator never has to split
a wild role: some allocation always avoids it.  A countermodel above slack two
therefore requires a profile on which *every* four-edge complete EFX allocation
splits a role of slack at least three.  No banked profile has that shape.  That
is a sharp, falsifiable target for the next hunt, and a better one than
"realizations with three or more goods".

## 3. Open item 3 — the one-minimum-split driver, repaired

`run_identity_aware_one_minimum_split_cegar.py` is a new driver; the old
`run_exact_response_one_minimum_split_cegar.py` and its JSON are untouched.

For a candidate profile it tries, in order:

* **Branch W** — an allocation splitting no role.  Realization-free by
  Corollary 3.
* **Branch S** — one tame split role `C`, with a *separate* allocation for each
  of the eight side patterns of `C`.  A piece is then a single good, so its
  deletion floor is its own value: `M` on the witness side and `T-M` off it.
  This is the identity-aware floor the open item asked for.

The old driver's two errors are both fixed here.  It assumed a single least
good common to all four observers, and it demanded one allocation valid for
every realization at once; the correct quantifier lets the allocation depend on
the realization, which is what "every realization admits an allocation" means.

### 3.1 The banked profile

Running the new driver on the banked countermodel profile of
`exact_response_form2_one_minimum_split_cegar_20260814.json`
(sha256 `24872d…3ccec`):

```text
status              CLOSED_REALIZATION_FREE
superseded status   SAT_ONE_MINIMUM_SPLIT_SELECTOR_OBSTRUCTION
branch              S   (split role `e`, menu of 8 allocations)
```

Every role of that profile has slack at most `2`, so Corollary 2 applies and
the verdict is exhaustive.  Branch W fails on it — the profile genuinely needs
a split — so the identity-aware floor is exactly what retires the obstruction,
not an incidental improvement.  Banked in
`results/identity_aware_one_minimum_split_profile.json`.

> **Supersession note (2026-08-16).** The status
> `SAT_ONE_MINIMUM_SPLIT_SELECTOR_OBSTRUCTION` recorded in
> `results/exact_response_form2_one_minimum_split_cegar_20260814.json` on
> branch `cc/efx-fixed-u-salvage-20260814` is **superseded**.  It is an
> artifact of an identity-blind deletion floor and of demanding one allocation
> for all realizations at once.  Its profile is closed realization-free, and
> the obstruction is not an obstruction to the four-support-edge conclusion.
> The old JSON and its driver are left exactly as banked; this note is the
> correction of record.

### 3.2 The chart-level rerun

The new driver also runs the full premise CEGAR against `build_physical_master`
for form 2, so the repair is tested on the chart rather than only on the banked
profile.  Every cut it adds is realization-free: branch W sees only `T` and
`M`, and branch S is guarded by `rho(C) = 2` on the split role, where Lemma B
forces the column and the eight patterns exhaust the realizations.

| quantity | value |
|---|---|
| rounds completed | `120` (the declared iteration limit) |
| closed by branch W (no split) | `111` |
| closed by branch S (one tame split, 8-allocation menu) | `9` |
| obstructions found | `0` |
| first round needing branch S | iteration `1` |
| roles carrying a branch-S split | `m`, `e`, `k` (twice each), `a1`, `j`, `h` |

The old driver stopped at **iteration 7** and banked
`SAT_ONE_MINIMUM_SPLIT_SELECTOR_OBSTRUCTION`.  The repaired driver runs through
iteration `119` without an obstruction, so it passes the old stopping point by
a wide margin.

Two things must be said plainly about the tier of this run.  First, it ended at
the **iteration limit, not at `unsat`**, so it is *not* a chart theorem: it is
strong evidence that the identity-aware selector has no obstruction, not proof
that it has none.  Second, branch S was already needed at iteration `1`, so the
identity-aware floor is load-bearing from the very start of the run rather than
a refinement that only matters in exotic corners — which is precisely why the
identity-blind driver failed early.

Banked in `results/identity_aware_one_minimum_split_chart.json`.

## 4. Claim ledger

**Proved (hand proof in this note).**

- Lemma C′: split-locality at every cardinality; an unsplit role of any width
  is exactly its two-good stand-in.  Additive-marked at both uses.
- Theorem 1: a tame menu covering the tame side patterns closes a profile for
  every realization, at every cardinality and every witness identity.
- Corollary 2: the slack-two theorem, as the case where every role is tame.
- Corollary 3: a zero-split allocation is realization-free at any slack.
- Remark 4: the pattern space factorizes over observers.

**Exact-computational.**

- `104` of `113` banked profiles admit a zero-split four-edge EFX allocation,
  hence are closed at every cardinality; the other `9` need exactly one split,
  always of a tame role.
- All `113` banked profiles are realization-free closed, `0` countermodels,
  `0` unknowns — including all `45` with a role above slack two.
- The banked one-minimum-split obstruction profile is closed realization-free
  by an eight-allocation menu splitting role `e`.

**Evidence.**

- The chart-level identity-aware one-minimum-split CEGAR runs `120` rounds
  with `0` obstructions, `111` closed by branch W and `9` by branch S.  It
  ended at the iteration limit, not at `unsat`, so it is evidence for the
  identity-aware selector on the form-2 chart, not a theorem.
- Independent corroboration from a different method: the symbolic-realization
  CEGAR banked in commit `62c40e8`
  (`results/identity_aware_symbolic_realization_*.json`) enumerates
  realizations symbolically up to three goods per role and also reports
  `UNSAT_EVERY_REALIZATION_ADMITS_A_BANKED_ALLOCATION` on both flagship
  profiles, with no countermodel.  Its verdict is exhaustive on the
  one-minimum-split profile (`cap_covers_every_role` true) and *not* exhaustive
  on the whole-role obstruction profile (roles `m` and `p` at slack `99` and
  `236`), which the reduction above closes exhaustively.  Two independent
  routes, same verdict.

**Open.**

- The chart-level existence statement: whether *every* fixed-`U`-admissible
  profile admits a tame covering menu.  Theorem 1 reduces the universal
  question to this one; it does not answer it.
- The sharp countermodel target of §2.3: a profile on which every complete
  four-edge EFX allocation must split a role of slack at least three.  None
  exists in the banked population; whether the premises admit one is open.
- Everything the predecessor left open: chart coverage, observer safety after
  splits, and closure of the decorated-response recurrence.

## 5. Verification

```bash
pytest -q tracks/parkability/test_realization_free_universality.py
```

Recorded result: `19 passed in 0.16s`.  The tests check that a column of any
width keeps its total and its minimum; that an unsplit role of width `2..7`
matches its two-good stand-in in total, in minimum, and in which deletion
constraint binds; that the two-good column is *forced* at slack two, a
three-good column being arithmetically impossible there; that tame/wild
classification agrees with the slack statistic at the boundary; that the eight
side patterns are exactly the relabelling classes of the sixteen assignments;
that a split piece deletes at its own value while a whole role deletes at the
role minimum; and that the move family covers every role exactly once.

Replay commands (session-1 inputs are read from the salvage branch, as in the
predecessor note's §8):

```bash
python -m tracks.parkability.census_whole_role_universality \
  --trace /tmp/efx-idw-inputs/exact_response_form2_one_minimum_split_cegar_20260814.json \
  --trace /tmp/efx-idw-inputs/exact_response_form2_physical_minimum_cegar_checkpoint_20260814.json \
  --trace /tmp/efx-idw-inputs/exact_response_form2_canonical_physical_cegar_20260814.json \
  --trace /tmp/efx-idw-inputs/exact_response_form2_canonical_physical_cegar_stage2_20260814.json \
  --output results/whole_role_universality_census_form2.json --timeout-seconds 60

python -m tracks.parkability.run_realization_free_universality_cegar \
  --trace /tmp/efx-idw-inputs/exact_response_form2_one_minimum_split_cegar_20260814.json \
  --trace /tmp/efx-idw-inputs/exact_response_form2_physical_minimum_cegar_checkpoint_20260814.json \
  --trace /tmp/efx-idw-inputs/exact_response_form2_canonical_physical_cegar_20260814.json \
  --trace /tmp/efx-idw-inputs/exact_response_form2_canonical_physical_cegar_stage2_20260814.json \
  --output results/realization_free_universality_form2.json \
  --maximum-rounds 80 --timeout-seconds 60

python -m tracks.parkability.run_identity_aware_one_minimum_split_cegar \
  --profile /tmp/efx-idw-inputs/exact_response_form2_one_minimum_split_cegar_20260814.json \
  --output results/identity_aware_one_minimum_split_profile.json

python -m tracks.parkability.run_identity_aware_one_minimum_split_cegar \
  --form-index 2 --output results/identity_aware_one_minimum_split_chart.json \
  --maximum-rounds 120 --timeout-seconds 90
```

## 6. Artifact sha256

Recorded at freeze.  Each output JSON also carries its driver's `script_sha256`
self-recorded inside it.

```text
8dfe27a6f74d6cd95814dc1b5d161267219883213ecffab6a8459f5b18efaaf8  tracks/parkability/census_whole_role_universality.py
63d86bb9ce0294da5ef4e216ec9f6d9a6c899811139da8fb38120b145af1fdb8  tracks/parkability/run_realization_free_universality_cegar.py
e4cdcba198b1a264b8836ee7fc0fb62f6b1e2d4bd24dae134e42e5f53d1e578c  tracks/parkability/run_identity_aware_one_minimum_split_cegar.py
152696f9512dc9107bc9fc3ff92d332ae1c4a2d93700bfea2a2e24b4350ca06e  tracks/parkability/test_realization_free_universality.py
1df6fe98ae4136642bb50bc6abe070f0669d957d08e1f0758d4bf88bea6da996  results/whole_role_universality_census_form2.json
94c061a0420a804c8a2f35f185b8cc125f89ff54f80539bcc04da50345526755  results/realization_free_universality_form2.json
8f641757b4cef8f665e4e97b78e762ce933229014d29a77955f2a34a7275c0b3  results/identity_aware_one_minimum_split_profile.json
f086b168a47bcc91d8808b393bc8e25e424c530252d574d96a5d6afd9d858120  results/identity_aware_one_minimum_split_chart.json
```

Session-1 inputs, re-extracted from `cc/efx-fixed-u-salvage-20260814` for this
session.  The first two match the sha256 values recorded in §8 of the
predecessor note exactly, so the input provenance is unbroken:

```text
24872d6bf5e5b75ae2dc0de8faa453346806c2bc97f2cd38d975e935d130896b  exact_response_form2_one_minimum_split_cegar_20260814.json
e396f24dfb60f0ea796e6dea46962a3ac4eb3794ee6e6e87932f9fa94eff6963  exact_response_form2_physical_minimum_cegar_checkpoint_20260814.json
4e4e1919680fdf480b5257bfe8111cf6b794838a7728c52a58bb93db0a0f0c17  exact_response_form2_canonical_physical_cegar_20260814.json
201149865ee0e39b6e0635bd66c9ae50522e7ddca0cb7793d04e9df20df0653e  exact_response_form2_canonical_physical_cegar_stage2_20260814.json
```

The banked JSONs record the input paths under this session's scratch
directory; the sha256 values above, not those paths, are the provenance of
record.

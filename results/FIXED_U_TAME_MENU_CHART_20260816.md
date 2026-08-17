# The chart-level tame-covering-menu question (2026-08-16)

**Branch:** `cc/efx-idwitness-20260816`

**Predecessor:** `results/IDENTITY_AWARE_SLACK_TWO_20260816.md`, whose Theorem 1
reduces the universal statement to the chart-level question attacked here.

## Outcome

Theorem 1 says: a *tame covering menu* — a family of complete within-budget
allocations, none splitting a role of slack at least three, covering the side
patterns of the tame roles — closes a profile for every physical realization.
The remaining question is whether the fixed-`U` premises always supply one.

**That theorem is not proved here, and I do not think it is close.**  What this
note contributes is a sharp account of why, which is more useful than another
confirmation run:

1. **Open item (a) is done.**  §1 formalises "fixed-`U`-admissible" for form 2
   as an explicit constraint list over `96` rational unknowns.
2. **A necessary structural lemma is proved from the premises** (§2.1, Lemma
   D).  Every EFX allocation must either give observer `d` a role outside the
   packet `W`, or place `a0` and `a1` in different bundles.  It is verified to
   hold with no exceptions across all `83` banked whole-role allocations.
3. **The two natural constructive routes are refuted outright** (§2.2), each on
   all `113` banked profiles, with the mechanism identified.  This is why the
   positive theorem resists: the obvious candidate menus are not merely
   insufficient, they fail everywhere.
4. **The failure shape is characterised** (§3) and turns out to be a genuine
   near-miss, which sharpens the countermodel hunt considerably.
5. The chart-level run remains **evidence, not theorem** — and its terminal
   `SAT` verdict turned out to be an **artifact of its own move family**, which
   §7 documents.  The obstruction it reported is closed, realization-free, by a
   menu splitting three tame roles at once.  This is the second time an
   obstruction on this chart has dissolved on inspection; §7.2 draws the
   lesson.

## 1. Open item (a) — what "fixed-`U`-admissible" means

`build_physical_master(form_index=2)` is the definition of record.  Unfolding
it through `build_rank_three_master` and `build_master`, an admissible profile
is a pair `(v, m)` of rational tables — `v[g,i]` the role total, `m[g,i]` the
role minimum, over `12` roles and `4` observers, so `96` unknowns — satisfying:

**Normalisation and range.**
```text
0 < v[g,i] < 16                        every role, every observer
0 < m[g,i] <= v[g,i]                   every role, every observer
sum_{g in BASE[i]} v[g,i] = 1          every owner i          (own base is the unit)
sum_{g in BASE[charity]} v[g,i] <= 1   every owner i
tail_i(BASE[t]) <= 1                   every owner i, every owner t != i
```
where `tail_i(S) = sum_{g in S} v[g,i] - min_{g in S} m[g,i]` is the *physical*
tail, the bundle value after deleting one least good.  This is the tail
substitution that `physical_tail` installs, and it is the only place the
minima enter the base premises.

**Size class.**  Each role is one common physical packet, so for every role `g`
```text
( m[g,i] = v[g,i] for all i )   or   ( 2 m[g,i] <= v[g,i] for all i ),
```
singleton or multi-good uniformly across observers.  This disjunction is the
cap-free totals/minima abstraction, exact by Lemma A of the predecessor.

**Desire.**  `v_r(A) > 1`, `v_q(Q) > 1`, `v_s(E) > 1`, `v_d(Q) > 1`, with the
named packets `A = {a0,a1}`, `Q = {j,k,q0}`, `E = {l,e}`, `W = {m,gq,gr}`,
`K = {j,k}`, `P = {p}`.

**Inclusion-minimal restoration.**  `v_d({j,k,h}) > 1`, `v_d({j,h}) <= 1`,
`v_d({k,h}) <= 1`, plus the `mu/theta/nu/kappa/B` inequalities of
`build_master` and a full residual-selector failure sweep over the subsets of
`W`.

**The rank-three wall.**  With `d_floor = v_d(W)`,
```text
d_floor <  tail_d(A)          (*)
d_floor >= tail_d(Q)
d_floor >= tail_d(E)
d_floor >= v_d(P)
```

**Response-relation saturation.**  For form index `2`, the nonself response
edges of the support state are *exactly*
`r->q, q->s, s->r, d->q`, together with `d->r`, and every other nonself edge is
negated.  In addition no rank-four ordinary SDR exists in the support, split or
reassembly states.

Line `(*)` is the one that does the work below.

## 2. Open item (b) — the positive theorem, and why it resists

### 2.1 A necessary condition, proved

First a monotonicity fact worth isolating, since it is used twice.

> **Lemma T (tail monotonicity).** For a bundle `S` of whole roles and a role
> `g` not in `S`, `tail_i(S ∪ {g}) >= tail_i(S) + v[g,i] > tail_i(S)`.

*Proof.* `tail_i(S ∪ {g}) = v_i(S) + v[g,i] - min(min_i(S), m[g,i])`
*(additive: the bundle value is a sum; and the bundle's least good is the least
of the per-role minima, by Lemma C′ of the predecessor)*.  Since
`min(min_i(S), m[g,i]) <= min_i(S)`, this is at least
`v_i(S) - min_i(S) + v[g,i] = tail_i(S) + v[g,i]`, and `v[g,i] > 0`. ∎

> **Lemma D (`A`-envy).** Let `(v, m)` be fixed-`U`-admissible at form 2, and
> let `A` be any complete allocation of the roles.  If observer `d`'s bundle
> satisfies `B_d ⊆ W` and both `a0` and `a1` lie in one bundle `B_u` with
> `u ≠ d`, then EFX fails for `d` against `u`.
>
> Equivalently: **every** EFX allocation gives `d` a role outside `W`, or
> separates `a0` from `a1`.

*Proof.* `B_d ⊆ W` gives `v_d(B_d) <= v_d(W) = d_floor`, by additivity and
positivity *(additive)*.  `B_u ⊇ A`, so by Lemma T applied repeatedly,
`tail_d(B_u) >= tail_d(A)`.  Premise `(*)` gives `tail_d(A) > d_floor`.  Chain
them:
```text
v_d(B_d) <= d_floor < tail_d(A) <= tail_d(B_u) = v_d(B_u) - min_{x in B_u} v_d(x),
```
which is exactly the negation of `d`'s EFX constraint against `u` *(additive:
deletion subtracts a value, so EFX for `d` against `u` is
`v_d(B_d) >= tail_d(B_u)`)*. ∎

Lemma D is a hard constraint on the shape of every menu the chart could
possibly supply, and it is premise-derived rather than observed.  Premise `(*)`
itself holds on all `113` banked profiles, as it must.

The banked data confirms Lemma D and then says something sharper than the
lemma requires.  Of the `83` distinct whole-role allocations recovered from the
census, `83` satisfy the disjunction and `0` violate it — but the disjunction
is never actually needed, because **all `83` take the first alternative**:

| | count of `83` |
|---|---|
| gives `d` a role outside `W` | `83` |
| of which give `d` a role of `A` itself | `59` |
| additionally separate `a0` from `a1` | `55` |

So on this population the second alternative never has to carry a case alone.
Every closing allocation the chart produced escapes Lemma D by giving `d`
something outside its own support home, and in `59` of the `83` that something
is a role of the very packet `d` envies.  That is a stronger regularity than
the lemma proves, and I have not been able to promote it: nothing in §1's
premises forces `B_d ⊄ W`, so it is recorded as an exact-computational
observation about the banked menu, not as a lemma.

### 2.2 Both natural constructions are refuted

The two canonical candidate menus are the ones the chart hands you for free.
Both fail, and not marginally.

> **Refutation 1 (base blocks).** Give each owner its own base block
> `BASE[i]`, and charity's block `{j,l,gr}` to one owner.  This is EFX on
> **`0` of the `113`** banked profiles, for every choice of host, and needs `6`
> or `7` support edges against a budget of `4`.

The valuation half of this looks like it should work and does not, which is
worth recording.  The premises give `v_i(BASE[i]) = 1` and
`tail_i(BASE[t]) <= 1` for `t ≠ i`, so if every bundle were exactly one base
block the allocation would be EFX by construction.  But charity is not an
owner, so its block must be absorbed, and the premises bound
`v_i(BASE[charity]) <= 1` *separately* — they say nothing about
`tail_i(BASE[u] ∪ BASE[charity])`, which Lemma T shows can reach `2`.  The host
bundle is therefore unprotected, and empirically always breaks.

> **Refutation 2 (supplier homes).** Give every role to its own support
> supplier, and `p` to one owner.  This costs only `1` edge, comfortably inside
> the budget, and is EFX on **`0` of the `113`** profiles.

Here the failing constraint is identifiable and is Lemma D: `d`'s support home
is exactly `W`, and `A` sits whole with `r`.  The pair `(d, r)` fails on
`113` of `113` profiles for three of the four hosts.  So the cheapest
allocation in the chart is precisely the one Lemma D forbids.

### 2.3 The exact gap

Putting the two together explains the difficulty.  The edge budget pushes
toward supplier homes; Lemma D forbids the supplier-home allocation outright;
and the valuation-friendly base-block allocation is both over budget and broken
by charity's block.  Every admissible profile must therefore be closed by an
allocation that is a *compromise* between the two structures, and the banked
evidence says the compromise is genuinely profile-dependent: `83` distinct
whole-role allocations across `104` profiles, using `47` distinct edge sets,
with `80` of the `83` at exactly the budget of `4` edges.

That is the gap, stated precisely:

> **Gap.** No single allocation, and no small profile-independent family,
> closes the chart.  A positive proof must exhibit a *selection rule* that maps
> an admissible profile to a closing allocation, and the rule must be sensitive
> to the profile, not merely to the chart's combinatorics.  Nothing in §1's
> premise list obviously determines such a rule, and the two natural candidates
> are refuted above.

I do not have that rule, and I do not want to overstate how close it is.  A
menu of `83` allocations with `47` edge sets is not a structure that reads off
easily, and the honest reading of the evidence is that the chart-level theorem
needs an idea that is not yet present.

## 3. Open item (c) — the minimal failure shape

By Theorem 1, a profile defeats the whole approach exactly when **every**
complete four-edge EFX allocation splits a role of slack at least three.  §2
sharpens what such a profile must look like.

> **Failure shape.** An admissible profile `P` defeats the tame menu only if
>
> 1. no whole-role four-edge EFX allocation exists for `P` — so `P` is already
>    outside the `104 / 113` majority; and
> 2. every four-edge EFX allocation of `P` splits some role `C` with
>    `rho(C) >= 3`; and
> 3. by Lemma D, each such allocation still gives `d` a role outside `W` or
>    separates `a0` from `a1`.

**The banked population is a near-miss, and that is the useful part.**  Of the
`113` profiles, `9` need a split, and in every one of the `9` the role that
must be split has slack exactly `2` — tame, every time:

| profile | split role | slack of that role | max role slack |
|---|---|---|---|
| `5`, `6`, `7` | `gq` | `2` | `3`, `2`, `2` |
| `11` | `l` | `2` | `236` |
| `14` | `a0` | `2` | `7` |
| `102`, `103`, `104` | `m` | `2` | `2`, `89`, `30` |
| `107` | `a1` | `2` | `2` |

Now compare against which roles are *ever* wild across the population:

```text
m: 15    l: 13    gq: 13    p: 8    a1: 6    a0: 4    j: 2    e: 2
h: 1     k: 1     q0: 1     gr: 1
```

The roles that are forced to split — `gq`, `m`, `l`, `a0`, `a1` — are exactly
the roles that are most often wild.  `m` is wild on `15` profiles and is the
forced split role on `3`; `gq` is wild on `13` and forced on `3`; `l` is wild
on `13` and forced on `1`.  The two conditions simply never coincide in the
banked population.

> **Sharpened countermodel target.** Search the fixed-`U` premises for a
> profile on which a role in `{gq, m, l, a0, a1}` is simultaneously
>
> - **wild**, `rho >= 3`, and
> - **forced**, in the sense that every complete four-edge EFX allocation
>   splits it.
>
> This is a coincidence of two conditions each of which is common in the
> banked population, and which the population never realises together.  It is a
> far narrower target than "realizations with three or more goods per role".

`run_realization_free_universality_cegar.py` already emits
`UNSAT_NO_TAME_SPLIT_ALLOCATION` on exactly this shape, so it is a cheap screen
for driving a premise-side search.  It never fired on the banked population.

## 4. The chart-level run — still evidence

`run_fixed_u_tame_menu_chart_theorem.py` runs the premise CEGAR with the menu
**seeded** by the `83` banked whole-role allocations, so the master starts from
a far stronger position than the unseeded driver of the predecessor note.  The
cut algebra is what makes a terminating run a theorem:

```text
Not( OR_c closes(c) )  ==  AND_c Not( closes(c) ),
```

so the accumulated cuts state exactly "no certificate of the menu closes this
profile", and `unsat` would say every admissible profile has a tame covering
menu.  A seed certificate is sound for any complete allocation inside the edge
budget whether or not it is EFX anywhere — the cut only excludes profiles on
which that allocation *is* EFX, and there it is a witness — so completeness and
the edge budget are verified for each seed and nothing else is assumed.

**Seeding costs runtime, though less than it first appears.**  Each of the `83`
seed cuts is a disjunction of linear constraints over the `96` unknowns, and
the master pays for them.  Measured: the first `9` rounds are very slow while
the master digests the seed, after which the run settles to about `2.7`
rounds per minute against roughly `4.8` for the unseeded driver — so
steady-state is about half speed, not the two orders of magnitude the opening
phase suggests.  An early impression of the slowdown taken from the first few
rounds would have been badly wrong, which is why the rate is quoted from a
timed interval in steady state rather than from the start of the run.

The run terminated at iteration `43` with `SAT`, not `unsat`, and that verdict
turned out to be an artifact of the driver's own move family — §7 documents the
re-test that dissolves it.  So the chart-level claim stands where the
predecessor left it: evidence, not theorem, and now with a known defect in the
search driver rather than merely an inconclusive run.

For the record, the unseeded run of the predecessor note reached `120` rounds,
`111` closed whole-role and `9` by a tame split, with `0` obstructions, and the
old identity-blind driver it replaced stopped at iteration `7`.

**A caveat on the move family that matters for interpreting any future SAT.**
The chart driver's oracle (`close_profile`) tries a whole-role allocation and
then a single tame split.  Theorem 1's hypothesis is weaker: it allows a menu
splitting *several* tame roles at once.  So a `SAT` verdict from this driver is
**not** by itself a failure of the tame-menu hypothesis — it would first have
to be re-tested against multi-tame-split menus, which
`run_realization_free_universality_cegar.py` does and which closed all `113`
banked profiles.  Any future obstruction from the chart driver must be run
through that wider family before being called a failure shape.

## 5. Claim ledger

**Proved (hand proof in this note).**

- Lemma T: the physical tail is strictly monotone under adding a role.
  Additive-marked.
- Lemma D: under the fixed-`U` premises at form 2, every EFX allocation gives
  `d` a role outside `W` or separates `a0` from `a1`.  Additive-marked.

**Exact-computational.**

- The premise inequality `d_floor < tail_d(A)` holds on all `113` banked
  profiles; Lemma D's disjunction is satisfied by all `83` banked whole-role
  allocations, with `0` violations.
- The base-block allocation is EFX on `0` of `113` profiles and needs `6`-`7`
  edges against a budget of `4`, for every choice of host.
- The supplier-home allocation is EFX on `0` of `113` profiles at `1` edge, and
  the failing constraint is the `(d, ·)` pair Lemma D predicts, on `113` of
  `113` for three of four hosts.
- Every one of the `9` split-needing profiles splits a role of slack exactly
  `2`; the wildness distribution over roles is as tabulated in §3.

**Exact-computational (continued).**

- The seeded chart CEGAR's terminal `SAT` at iteration `43` is superseded: its
  reported obstruction is closed realization-free, in `8` rounds, by a menu
  splitting the three tame roles `gq`, `k`, `q0` at once.  The verdict was an
  artifact of a one-split oracle.

**Evidence.**

- The seeded chart CEGAR reached `43` rounds and the unseeded run `120`, both
  with `0` surviving obstructions.  Neither reached `unsat`, so the chart-level
  statement is not a theorem.

**Open.**

- The chart-level positive theorem itself, and specifically the selection rule
  named in §2.3's Gap.  This is the live obstacle.
- The sharpened countermodel target of §3.  Note that the one profile which
  looked like a hit — `a0` wild at slack `6` — was not one, so the target is
  still unmet rather than met.
- The chart driver whose oracle matches Theorem 1's hypothesis is now built
  (§7.4) and its run is in flight (§7.5) rather than terminal, so the chart
  question is open on the evidence, not on the instrument.
- The exponential barrier §7.4 quantifies: covering menus on this chart split
  as many as six tame roles, a `8^6 = 262144` pattern product for one
  certificate.  Deciding the chart by search needs a cut that avoids the full
  product without losing soundness, and I do not have one.  Remark 4 collapses
  a *single* allocation's universality to `4 · 2^k` checks but does not collapse
  the menu-covering statement, which is where the product actually lives.

## 6. Verification

```bash
pytest -q tracks/parkability/test_fixed_u_tame_menu_chart.py \
         tracks/parkability/test_fixed_u_multi_split_chart.py
```

Recorded result: `19 passed` and `26 passed`; `73 passed` across all four test
files of this line of work.

The first file checks Lemma T on explicit rationals, including the tie case
where the added role carries the new minimum; Lemma D's disjunction on the
banked whole-role menu; that a seed certificate is rejected unless it is
complete and inside the edge budget; and that the two refuted constructions are
reproduced exactly as reported.

The second file is the instrument's own guard rail, and its tests are written
against the three defects of §7.3 and §7.4 rather than against the happy path:
that the side-pattern product is exactly `8^k` and factorises per role; that
narrowing a certificate to "visited" patterns is rejected, as is dropping a
single vector, claiming a larger split set than the certificate carries, or
padding to the right count with wrong keys; and that no search limit -- an
exhausted budget, an inconclusive wide-family run -- may be mapped to an
obstruction verdict.

Replay:

```bash
python -m tracks.parkability.run_fixed_u_tame_menu_chart_theorem \
  --form-index 2 --seed-menu results/seed_whole_role_menu_form2.json \
  --output results/fixed_u_tame_menu_chart_theorem.json \
  --maximum-rounds 600 --timeout-seconds 120

# the re-test of §7 that supersedes that run's SAT verdict; the driver reads
# countermodel_totals / countermodel_minima straight out of the chart output
python -m tracks.parkability.run_realization_free_universality_cegar \
  --profile results/fixed_u_tame_menu_chart_theorem.json \
  --output results/fixed_u_chart_countermodel_wide_family_retest.json \
  --maximum-rounds 200 --timeout-seconds 120
```

## 7. The chart run terminated — and its verdict is an artifact

### 7.1 What happened

The seeded run terminated at iteration `43`:

```text
status              SAT_NO_TAME_COVERING_MENU_FOR_THIS_PROFILE
seed certificates   83   (all verified complete and within the edge budget)
rounds completed    43   (39 whole-role, 4 tame-split on roles k and gr)
menu size at exit   126
countermodel slacks a0: 6, p: 6, and gq, gr, k, q0 at 2, the rest singletons
```

At face value this is the shape §3 predicted: `a0` is a role of the forced set
`{gq, m, l, a0, a1}` and it is **wild**, at slack `6`.

**It is not a countermodel.**  §4's caveat required re-testing any `SAT`
against the multi-tame-split family before reading it as a failure shape, and
that test dissolves it:

```text
run_realization_free_universality_cegar --profile <the countermodel>
  -> UNSAT_EVERY_REALIZATION_ADMITS_A_BANKED_ALLOCATION   in 8 rounds
     tame roles k, q0, gq, gr | wild roles a0, p
     the closing baseline splits gq, k and q0 simultaneously
```

The profile is closed realization-free — every cardinality, every witness
identity — by a menu that splits **three** tame roles at once.  The chart
driver's oracle tries a whole-role allocation and then at most **one** tame
split, so it could not express the closing menu and reported an obstruction
that does not exist.  The `SAT` verdict is therefore superseded by this
re-test, and the chart-level question stays **open**, not answered negatively.

### 7.2 The lesson, because this is the second time

The banked `SAT_ONE_MINIMUM_SPLIT_SELECTOR_OBSTRUCTION` that the predecessor
note retired was an artifact of an identity-blind deletion floor and of
demanding one allocation for all realizations.  This obstruction is an artifact
of a move family too narrow to express the closing allocation.  Different
defect, same shape:

> **On this chart, an obstruction verdict has never yet survived contact with a
> wider move family.**  Every `SAT` reported so far has been a statement about
> the selector, not about the chart.  A future obstruction should be assumed to
> be a selector artifact until it has been re-tested against the widest
> available family, and the re-test should be run *before* the verdict is
> banked, not after.

I built the caveat into §4 before this run finished and it caught the error, so
the discipline works; but the driver should not have been able to emit a
verdict its own oracle was too narrow to justify.

### 7.3 The fix, and its soundness requirement

The repair is to widen `close_profile` to a branch that splits a *set* of tame
roles, taking its menu from the realization-free CEGAR.  The symbolic cut must
then be

```text
guard( every split role is tame )  AND  AND_{pattern vectors s}  OR_{A in menu} EFX(A, s),
```

quantified over the full product of side patterns of the split roles — `8^k`
vectors for `k` split roles, so `64` at `k = 2` and `512` at `k = 3`.  That
product is the soundness requirement and is where a widened driver would most
easily go wrong: dropping to a single allocation per split role, or covering
only the patterns the CEGAR happened to visit, would produce an unsound cut and
hence a false chart theorem.  Remark 4 of the predecessor note (the pattern
space factorizes over observers) is the lever that keeps this tractable, since
it decides one allocation's universality in `4 · 2^k` checks rather than
`2^(4k)`.

I have not built that driver, and I would rather leave the chart question open
than bank a theorem resting on a cut I had not verified covers every pattern.

### 7.4 The widened oracle, built

`run_fixed_u_multi_split_chart_theorem.py` is that driver.  A certificate fixes
a set `S` of tame split roles and carries one allocation for **every** vector
of the full `8^|S|` product; branch W is the case `S` empty, so whole-role and
split certificates are one object.  Every certificate passes an exact rational
re-audit of each allocation *and* a coverage audit before its cut is added.

Building it surfaced two further defects of the same family, neither
hypothetical.  Recording them matters more than the driver does.

> **Defect 2 — a search cap reported as an obstruction.**  With the split set
> capped at three roles the driver reported `SAT` on a profile whose closing
> menu needs **four** tame roles split.  A limit of the instrument had been
> dressed up as a fact about the chart, which is precisely the error §7.2 warns
> about, committed while fixing it.

> **Defect 3 — the split set proposed from the baseline alone.**  The wide
> CEGAR reports its *baseline* allocation's split roles, which is a strict
> understatement: later menu allocations routinely split others.  On one
> profile the baseline proposed `{h, k}` while the covering menu actually
> splits `{gq, gr}`, so the driver gave up at a pattern product of `64` against
> a budget of `4096` — failing well inside its own limits and mislabelling the
> result a budget bound.

Both are now closed structurally rather than by care:

* `close_profile` returns a *status*, and `HALT_VERDICT` maps an exhausted
  budget and an inconclusive wide-family run to `HALTED_…` names.  Only a
  genuine `UNSAT_NO_TAME_SPLIT_ALLOCATION` from the widest family may be called
  an obstruction, and `OBSTRUCTION_STATUSES` is a single-element set the tests
  pin down.
* `wide_menu_split_union` recomputes the split set as the union over the whole
  covering menu.  With `S` that union a certificate *must* exist — every menu
  allocation splits inside `S`, and by Lemma C its EFX status depends only on
  the pattern over the roles it splits — so the code asserts that rather than
  assuming it, and tries subsets first only to keep the product small.

Both profiles that produced false obstructions now close: the one-split
driver's countermodel on the split set `{gq, gr, k}`, and the cap-bound profile
on `{gq}`.

The self-tests are the point of the exercise.
`test_narrowing_a_certificate_to_visited_patterns_is_rejected` narrows a
complete certificate to the patterns a search "visited" and asserts the audit
refuses it; companions cover dropping a single vector, a certificate claiming a
larger split set than it carries, and padding to the right count with wrong
keys.  A separate test pins the rule that no search limit may be reported as an
obstruction.  The instrument can no longer repeat any of the three defects
silently.

**What the widened run shows.**  The chart-level question is still open, and
the driver now says why in a quantified way rather than by failing.  On this
chart the covering menus are wide: one admissible profile's menu splits **six**
tame roles, a pattern product of `8^6 = 262144` for a single certificate.  That
is the real barrier to deciding the chart by search — not solver speed, but the
exponential cost of certifying a profile whose closing menu splits many roles.
The `4096`-vector budget that seemed generous is exceeded by a single profile
needing four.

### 7.5 The widened run

Three configurations were run, and the first two are worth recording because
each halted for a different instrument reason, both now fixed:

| run | budget | outcome |
|---|---|---|
| seeded, one-split cap | — | `UNKNOWN` at round `67`, master timed out; `0` obstructions |
| unseeded, split cap `3` | — | `SAT` at round `5` — **defect 2**, a cap reported as an obstruction |
| unseeded, budget `4096`, baseline proposal | `4096` | halted at round `1` — **defect 3**, gave up at a product of `64` |
| unseeded, budget `20000`, union proposal | `20000` | in flight; see below |

The corrected run, with the union proposal and a `20000`-vector work budget:

```text
status              RUNNING at freeze
rounds completed    191
branch W            188   (whole-role, 1 pattern each)
branch M              3   (split sets {a1}, {h}, {gq}, 8 patterns each)
obstructions          0
```

It has passed every point at which an earlier configuration stopped — round
`67`, round `5`, round `1` — and has found no obstruction.  The round rate
decays as cuts accumulate, from roughly `6` per minute early to about `0.5` per
minute at round `190`, so the `400`-round budget is hours away and the master
is the bottleneck, not the oracle.

**Tier: evidence, not theorem.**  The run has not reached `unsat`, so nothing
here upgrades §4.  What the widened oracle does establish is that the two
obstructions this line of work produced were both artifacts, and that no
obstruction survives an oracle matching Theorem 1's hypothesis on any profile
examined so far.

The terminal verdict supersedes this snapshot when the run lands.  `unsat`
would be the chart theorem; a `SAT_NO_TAME_COVERING_MENU_FOR_THIS_PROFILE` from
*this* driver would, for the first time, be a genuine failure shape rather than
a selector artifact, since only a real failure of the widest family can now
produce that status.

## 8. Artifact sha256

Recorded at freeze, including the one-split chart run's terminal output and the
re-test that supersedes its verdict.  `results/fixed_u_multi_split_chart_theorem.json`
is deliberately absent: it is the widened run's in-flight snapshot per §7.5, so
its hash is not stable until the run lands.

```text
fc9f2e8aab0b100b4a51addb5a5f50856d6d65d7b85bffcf1b0bd5d94930d906  results/fixed_u_tame_menu_chart_theorem.json
01c27852cbe0210716c6b1191a86ccb432c9d3272e54be69542307a576800f6c  results/fixed_u_chart_countermodel_wide_family_retest.json
0892a2a26b520d5c5ddc5254f981bfa8800e2240591a5f1d9b25d88dbe917eb0  tracks/parkability/run_fixed_u_multi_split_chart_theorem.py
458066f7070e870cb48cb6607493ce7b12227acefeb51b30495ad45612fc4857  tracks/parkability/test_fixed_u_multi_split_chart.py
58435d30bb97e8df279b5f49c9dcc4a28066ff9d348b05100fa3108a0d4b1d74  results/fixed_u_multi_split_chart_capbound_defect.json
6ba597f499084ca41e2697d209133513d741b187309ed8b2b5ab24c705ecc97d  tracks/parkability/run_fixed_u_tame_menu_chart_theorem.py
a2b24ff0a7e3cb7bea0087f5bbc83fb89f6ff515819ce9c24699505229bf8064  tracks/parkability/audit_fixed_u_chart_structure.py
3871aa3f90974b904dea04871943bba01fe746b5c00bfd8b73677330382a7cde  tracks/parkability/test_fixed_u_tame_menu_chart.py
d33c33c2146c2d335539055284439fd01c193b73a353a014297e78e58d654259  results/seed_whole_role_menu_form2.json
54d7bb4818fca5daeb3688cc613203b857780babd94da0c9bf8da6aa2261edf6  results/fixed_u_chart_structure_audit.json
```

The seed menu is derived from `results/whole_role_universality_census_form2.json`
of the predecessor note (sha256 `1df6fe98…a996`) by taking the distinct
role-to-owner maps of its zero-split allocations.  The trace inputs are the four
session-1 artifacts whose sha256 values are recorded in §6 of that note.

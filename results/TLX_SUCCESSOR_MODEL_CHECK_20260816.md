# `T_{L,times}` successor-state model check — referee repair item 5

**Date:** 2026-08-16

**Status:** completed machine check of the contested content of the retracted
`T_{L,times}` closure. Every verdict below is computed from an exhaustive
scan; there are no hardcoded verdict fields.

Executes repair item 5 of `results/TLX_CLOSURE_REFEREE_REPORT_20260816.md:300-304`
— "a small exhaustive model checker over 4 agents / 5-6 goods / integer weights
instantiating an actual `T_{L,times}^*`-shaped state, applying the star,
computing the real minimal response, and comparing the successor's packet
coordinate against the predecessor's."

- Checker: `tracks/parkability/model_check_tlx_successor_20260816.py`
- Data: `results/tlx_successor_model_check_20260816.json`

Scale: **233,030 instances**, 493,333 lex-maximal bases, 3,673,242 star states,
35,876,208 successor configurations, 11,958,736 cancellation configurations,
530.7 s. Self-test battery: 14/14 pass.

## 1. Verdicts

| # | Claim tested | Verdict | Evidence |
|---|---|---|---|
| G2a | the response extracted at the star is always a singleton | **CONFIRMED** | 3,673,242 / 3,673,242 star states have `|D|=1`; none has `|D|>1` |
| G2b | the star allocation is never EFX, so the lexicographic endpoint is vacuous | **CONFIRMED** | 0 of 3,673,242 star states are EFX |
| G2c | the closure's equation (5) fails under the reset theorem's own quantifier | **CONFIRMED (refutes eq. 5)** | `D={k}` is an admissible globally minimum response in all 35,876,208 configurations |
| G3a | the successor packet coordinate can fail to decrease (adversarial choice, steelman reading) | **CONFIRMED** | 34,072,500 / 35,876,208 configurations stall |
| G3b | *no* legal response decreases it (favourable choice, maximal steelman) | **CONFIRMED** | 21,294 configurations, all with `L_alpha` strictly over `K` |
| G3c | the star strictly increases the collision hitting multiplicity | **CONFIRMED** | 34,072,500 configurations |
| G3d | progress holds **exactly** on the `L_alpha = K` slice | **CONFIRMED** | decreases on 1,803,708 / 1,803,708 of that slice and on 0 / 34,072,500 of its complement |
| G7 | canonical cancellation `Z^-` destroys root-strictness | **CONFIRMED** | 1,992,396 contract-reading failures (all exactly at `v_r(Y^-_r)=x`), 6,544,116 referee-reading failures |
| — | equation (3), `v_r(G-k)>x`, the part nobody disputes | **SOUND** | 601,236 checks, 0 failures |
| — | the successor packet can return to the root | **NOT OBSERVED** | 0 cases; the star always hands the packet to a nonroot owner |

### G2 — the response is manufactured, and the closure's own bound fails

The star allocation is never EFX anywhere in the searched space, so the branch
that would contradict global lexicographic maximality never fires: everything
runs through the non-EFX branch, exactly as the referee report predicted. The
minimum desired response is a singleton in every single case, because the star
empties two owners and any single good beats an empty bundle.

The sharper result is G2c. The floor-reset theorem minimises "among every
source and every desired subset of every target"
(`STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMISSION_THEOREM_20260814.md:60-63`). The
singleton target `{k}` is *desired* by any emptied owner (`v_i({k}) > 0 =
F_i^Y`) even though it is never *strongly envied*. So `D = {k}` is a globally
minimum desired response, and then

    D cap K = {k},   which is not contained in K - k.

Equation (5) of the closure is false as stated under the quantifier the
closure imports. The closure's justification — "every EFX wall is against
`G-k`", `ROOT_SINGLETON_...:96-98` — establishes only that the *strongly
envied* target is `G-k`; it does not restrict the minimisation, which ranges
over desired subsets of every target. Repairing this needs an explicit extra
hypothesis (`D <= G-k`), not the wall argument. Under that repaired reading
the violation count is 0, so the rest of this report scores the repaired
(steelman) reading.

Separately, in the wide-root probe the root itself is a source at the star in
735 cases (`v_r({k}) > v_r(G-k)`), so the emptied-owner route is not the only
one producing `D = {k}`.

### G3 — no descent in either declared coordinate once `L_alpha` exceeds `K`

Taking the steelman reading (`D <= G-k`), the packet behaviour splits exactly
along one line:

| slice | configurations | packet decreases for every legal response |
|---|---|---|
| `L_alpha = K` | 1,803,708 | 1,803,708 (all) |
| `L_alpha` strictly over `K` | 34,072,500 | 0 (none) |

The mechanism is the one the referee report named: with `|K| = 1`, every good
of `L_alpha - K` sitting in the root's star bundle is itself a legal globally
minimum response, and adopting it gives `K' = D cap L_alpha` of size 1 again.
The star's claimed progress therefore depends entirely on a hypothesis the
closure never states and the referee report flagged as unargued — that
`L_alpha = K` in the root-holder branch.

Two refinements:

- **Choice-dependence (G3b).** If the selector is additionally allowed to pick
  *favourably* among equally minimal responses — avoiding the ledger when
  possible — the packet does decrease in 35,854,914 configurations. It still
  cannot decrease in 21,294 of them, all with `L_alpha` strictly over `K`,
  namely those where `L_alpha` covers `G - {k}` so no ledger-free response
  exists. That is a genuinely irreparable slice, but a small one: the honest
  statement is that the star's progress is **choice-dependent**, and no such
  selection rule appears in either theorem.
- **The other declared coordinate moves the wrong way (G3c).** The frozen
  contract permits progress by "strict reduction of `K`, its collision hitting
  multiplicity, or the response-rank deficiency"
  (`RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md:98-99`). The
  star moves every good to the root, so it moves every off-root retired good
  off its holder: its collision hitting multiplicity is `|W| + 1` against the
  original candidate's `|K|`. In all 34,072,500 configurations with
  `L_alpha` strictly over `K` this is a strict **increase**.

The stalling successor can host another round (root still protected at `>= x`,
packet size unchanged) in 34,031,181 of the 34,072,500 stalling
configurations. It is not a literal star-only cycle: the successor packet is
never root-held (0 cases), so the next round routes to the nonroot branch. But
no declared coordinate has decreased.

### G7 — the canonical cancellation kills root-strictness

The composition theorem mandates that a colliding candidate first be tested in
its cancelled form `Z^-`, "cancelling every transfer of a good in `K`: leave
that good with its current holder and perform every other transfer"
(`GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPOSITION_THEOREM_20260813.md:85-88`),
and that the lexicographic contradiction at `Z^-` rest on the *preserved
strict-priority floor* (same file, `:96-98`). The star declines to form `Z^-`.

Applying it: the star's collision set is `W u {k}` where `W = L_alpha - Y_r`,
so `Z^-` gives `Y^-_r = G - W`, and

    1,992,396 of 11,958,736 configurations have v_r(Y^-_r) = x, not > x.

The failure is always exactly at equality, never below (0 cases below `x`) —
a structural fact the checker discovers rather than assumes, and one with a
one-line explanation: `Y_r` is disjoint from `W`, so `Y_r <= Y^-_r` and
`v_r(Y^-_r) >= v_r(Y_r) >= x`. Equality is reached precisely when the
protected root floor sits at the base certificate, which is the generic
`T_{L,times}^*` situation. Equality is fatal here: `> x` is what makes `Z^-`
a lexicographic contradiction, and `= x` gives none.

Under the referee report's own reading of the scenario (the deliberate
sacrifice of `k` to `u` is kept and only the off-root retired goods are
withheld) the failure is strict: 6,544,116 configurations with
`v_r(Y^-_r) < x`.

A further 1,987,376 configurations were rejected before the cancellation test
because no root-protected pre-state exists for that withheld set at all.

## 2. What was instantiated

For each valuation matrix the checker builds a state of the frozen format
`S=(Y,P,r,alpha,F,Sigma,M,h,R,L,C)`
(`GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md:14`), restricted to
the coordinates the star's own proof reads:

- **base certificate `(X,r,x)`.** `r` is agent 0, the first owner of the fixed
  priority order. `X` is *computed*, not posited: the checker enumerates all
  `5^m` assignments of each good to one of four owners or to charity, keeps the
  partial-EFX-with-charity ones under the repo's own predicate
  (`tracks/parkability/audit_fixed_u_global_lex_premise.py:49-59`:
  `v_o(A_o) >= v_o(A_t) - min_{g in A_t} v_o(g)` for every owner/target pair,
  and `v_o(A_o) >= v_o(P)`), and takes the lexicographic maximum of
  `(v_0(A_0),...,v_3(A_3))`. This is the rival family the branch itself
  declares (`ALTERNATING_GLOBAL_LEX_ATOMIC_THEOREM.md:48-51`). Ties are
  enumerated up to the per-space cap; every tied base shares the same first
  coordinate, so `x = v_r(X_r)` is a function of the instance. `O = G - X_r`.
- **anchor label `alpha`.** Instantiated by its load-bearing content, the old
  common-safe desired root core of closure equation (1): `A_anchor <= O`,
  `|A_anchor| >= 2`, `v_r(A_anchor) > x`. Instances admitting no such core are
  counted and skipped — the star's hypothesis is unsatisfiable there.
- **ledger `L`.** `L_alpha <= G`, nonempty, enumerated.
- **named packet.** `K = A cap L_alpha` nonempty with the **root** as current
  holder, `K <= Y_r` — the root-holder branch, the only branch the star exists
  for. The candidate cell `A = K u B` is completed by the witness certifier.
- **current allocation `Y` and floors `F`.** `F_i = v_i(Y_i)`, with the
  protected root floor `F_r >= x`. In the sweep, `Y` is represented by its only
  load-bearing coordinate — the set `W = L_alpha - Y_r` of retired goods parked
  off the root — with the root-maximal completion `Y_r = G - W`. Each reported
  witness is then re-certified against an **exhaustive** scan of all `5^m`
  feasible `Y`, selecting one with no empty owner where one exists.
- **collision history `C`.** Carried as the derived collision sets, computed by
  diffing the pre-state and star holder maps rather than by a closed formula.

## 3. Documented simplifications, and why they do not lose G2/G3/G7

**S1 — the `T*` recurrence condition is not enforced.** The `T_{L,times}^*`
type requires an exact generic `T*` recurrence of the complete augmented
record (`GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md:137-153`).
Verifying that needs the whole `G0--G10` selector machinery and is out of
scope here. The checker enforces the sub-conditions the star's proof consumes,
plus requirement 4 of the type (failure of the canonical ledger-free
realization — see S3). *Effect on the verdicts:* the searched space is a
**superset** of the genuine `T_{L,times}^*` states. A CONFIRMED verdict is
therefore reported as a refutation *of the star's argument as stated* — it
needs the witness state to be reachable before it refutes the theorem's
statement — while a REFUTED verdict (no counterexample anywhere in the space)
is **stronger** than it would be on the exact space.

**S2 — the anchor core is instantiated by its two used properties.** The
closure writes `A = T_q + f` with flower/charity provenance
(`LENGTH_THREE_GLOBAL_LEX_TARGET.md:36-70`), but its proof of equation (3)
uses only `A <= O`, `|A| >= 2`, `v_r(A) > x`. Extra structure only shrinks the
space, so S1 applies.

**S3 — the candidate cell's non-retired part `B` is not swept.** The star's
argument uses no recipient margin ("No criticality, current-root minimality,
recipient margin, or historical return premise is needed below",
`ROOT_SINGLETON_...:39-40`). Instead the witness certifier searches for a `B`
and a recipient `s != r` giving an explicit strict-capture collision
certificate: `v_s(K u B) > F_s` with `v_s(B) <= F_s`. That is the frozen
contract's "strict capture" row, and it simultaneously makes the canonical
ledger-free candidate `A^- = B` fail its recipient floor, which is
requirement 4 of the `T_{L,times}^*` type.

**S4 — the successor's next candidate cell is the adopted response.** The
frozen record inserts a collision "only together with adoption of its actual
extracted/tested response"
(`GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPOSITION_THEOREM_20260813.md:158-161`),
so the adopted response `D` is taken as the successor's candidate cell `A'`
and `K' = A' cap L_alpha = D cap L_alpha`. Any other reading makes `K'` depend
on an unspecified downstream selector; this is the most favourable
well-defined choice available, since `D` is the smallest packet the transition
touches.

**S5 — two readings of the response quantifier are scored separately.** The
floor-reset theorem minimises "among every source and every desired subset of
every target" (`STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMISSION_THEOREM:60-63`) —
the *strict* reading. The closure then restricts to `D <= G-k` on the ground
that "every EFX wall is against `G-k`" (`ROOT_SINGLETON_...:96-98`) — the
*wall* reading. Both are computed; the wall reading is the steelman.

**S6 — three readings of the response *choice* are scored separately.** `D` is
chosen, not determined. The checker reports whether *every* globally minimum
response decreases the packet (adversarial), whether *some* does (favourable),
and the full option list.

**S7 — priority.** `r` is taken to be globally first-priority, as the closure
assumes. Finding G8 of the referee report (that this is not established
upstream) is inherited, not tested here.

## 4. Searched space

Goods are unlabelled, so the exhaustive spaces enumerate one canonical
(column-sorted) valuation matrix per good-relabelling orbit; that is a
complete enumeration of the space, not a sample of it. Agents are **not**
interchangeable (the priority order is fixed), so no agent symmetry is used.

| space | goods | root weights | other weights | mode | matrices | seconds |
|---|---|---|---|---|---|---|
| A | 5 | {1,2} | {1,2} | exhaustive | 15,504 | 28.8 |
| B | 5 | {1,2,3} | {1,2} | exhaustive | 98,280 | 168.4 |
| C | 6 | {1,2} | {1,2} | exhaustive | 54,264 | 234.0 |
| D | 5 | {1,2,3} | {1,2,3} | sampled (seed 20260816) | 29,982 | 40.7 |
| E | 6 | {1,2,3} | {1,2,3} | sampled (seed 816) | 5,000 | 19.9 |
| F | 5 | {1..8} | {1,2,3} | sampled (seed 5) | 30,000 | 38.9 |

Within each matrix the sweep is exhaustive over: every lex-maximal base (up to
the per-space cap of 4, or 2 for 6 goods), every sacrificed atom `k`, every
sacrifice row `u` in {1,2,3}, and every set `W` of retired goods parked
off-root. Because every tied base shares the first coordinate `x`, and because
the swept quantities depend on the base only through `x`, capping the tied-base
list does not restrict the sweep.

Coverage note: 240,685 of 493,333 bases (49%) admit **no** anchor core
satisfying `A <= O`, `|A| >= 2`, `v_r(A) > x`, and are skipped — on those
instances the star's own hypothesis (1) is unsatisfiable. The results above are
over the 252,648 bases where it is satisfiable.

The full weight range {1,2,3} at 5 and 6 goods is sampled, not exhausted
(`3^20` and `3^24` matrices). Every phenomenon reported above appears in the
fully exhaustive spaces A, B and C as well as in the sampled ones, and no
phenomenon appears only in a sampled space, except the root-is-a-source case,
which needs root weights above 3 and is therefore confined to probe F.

## 5. Self-test

`--self-test` runs 14 checks that flip one input at a time and require the
verdict to move. All 14 pass:

- the EFX detector returns true on a hand-built EFX allocation and false after
  one valuation entry is raised;
- the minimum-response cardinality is 1 at the star, exceeds 1 on an
  allocation with no empty-handed owner, and returns to 1 when one owner is
  emptied again — so the ubiquitous `|D|=1` is computed, not assumed;
- the cancellation test fails at the boundary instance and passes after one
  root weight is raised;
- the lex-max detector's output is EFX, undominated by any other EFX
  allocation, and a deliberately worse EFX allocation is not reported;
- the successor accounting decreases the packet when `L_alpha = K` and stalls
  when `L_alpha` strictly contains `K`, and the strict and wall readings of the
  response quantifier give different answers on the same input — so the two
  readings are genuinely distinct code paths.

The third self-test was itself written with the wrong expectation first: it
asserted that the packet decreases when `L_alpha = K`, and the checker
disagreed, which is how the equation-(5) violation of G2c was found.

## 6. Minimal witnesses

All data exact; goods `g0..g4`, priority `agent0 (= r) < agent1 < agent2 < agent3`.

### W1 — G3, the packet stalls (steelman reading)

```
v_r = v_1 = v_2 = v_3 = (1,1,1,1,1)          five goods, all unit
X   = ({g0,g1}, {g2}, {g3}, {g4}),  P = {}   verified globally lex-maximal
x   = v_r(X_r) = 2
O   = {g2,g3,g4},  anchor A = O,  v_r(A) = 3 > 2
Y   = ({g0,g1}, {g2}, {g3}, {g4}),  P = {}   floors (2,1,1,1), F_r = x
L_alpha = {g0,g4},  K = {g0} <= Y_r          root is the current holder
collision certificate: recipient s = agent1, A_cell = {g0,g1}, B = {g1},
                       mu_s = 1 > 0, v_s(B) = 1 <= F_s = 1
```

Star with `k = g0`, `u = agent1`: `Y* = ({g1,g2,g3,g4}, {g0}, {}, {})`,
`v_r(Y*_r) = 4 > 2` (eq. (3) holds). Floors reset to `(4,1,0,0)`. Agents 2 and
3 hold nothing, so every singleton of `Y*_r` is a globally minimum desired
response. Choosing `D = {g4}` — a legal globally minimum response under the
closure's own restriction `D <= G-k` — gives

    K' = D cap L_alpha = {g4},   |K'| = 1 = |K|.

No decrease. `D cap K` is empty, so the closure's equation (5) is satisfied and
still yields nothing: the coordinate that (5) bounds is not the coordinate that
has to descend.

### W2 — G7, canonical cancellation loses root-strictness

```
v_r = (1,1,1,2,2),  v_1 = v_2 = (1,1,1,1,1),  v_3 = (1,1,1,1,2)
X   = ({g0,g3}, {g1}, {g2}, {g4}),  P = {}   verified globally lex-maximal
x   = 3
O   = {g1,g2,g4},  anchor A = O,  v_r(A) = 4 > 3
Y   = ({g0,g1,g2}, {g3}, {g4}, {}),  P = {}  floors (3,1,1,0), F_r = x
L_alpha = {g0,g3,g4},  K = {g0} <= Y_r
W   = L_alpha - Y_r = {g3,g4}                 parked on agents 1 and 2
collision certificate: recipient s = agent1, A_cell = {g0,g1}, B = {g1},
                       mu_s = 1 > 0, v_s(B) = 1 <= F_s = 1
```

Star with `k = g0`: `Y*_r = {g1,g2,g3,g4}`, `v_r = 6 > 3`. Canonical
cancellation leaves `g3` with agent 1, `g4` with agent 2 and `g0` with the
root:

    Y^-_r = {g0,g1,g2},   v_r(Y^-_r) = 3 = x,   NOT > x.

The strict-priority floor that `Z^-` needs for its lexicographic contradiction
is gone. Under the referee report's reading (keep the sacrifice of `g0` to
agent 1) it is worse: `Y^-_r = {g1,g2}`, `v_r = 2 < 3`. This is the concrete
instance the referee report predicted would exist when `L_alpha` strictly
contains `K`.

### W3 — G3b, no legal response decreases the packet at all

```
v_r = (1,1,1,1,2),  v_1 = v_2 = (1,1,1,1,1),  v_3 = (1,1,1,1,2)
X   = ({g4}, {g0,g1}, {g2}, {g3}),  x = 2
O   = {g0,g1,g2,g3},  anchor A = O,  v_r(A) = 4 > 2
L_alpha = {g0,g1,g2,g3,g4} = G,  K = {g4},  W = {g0,g1,g2,g3},  k = g4
```

Every good of `Y*_r = G - {g4}` is retired, so every legal globally minimum
response meets `L_alpha` and `|K'| = 1 = |K|` no matter which is chosen. Even
a ledger-avoiding selection rule cannot produce progress here.

### W4 — the two readings of `Z^-` are not equivalent

Same instance as W2 with `K = {g3}`, `L_alpha = {g3,g4}`, `W = {g4}`,
`Y = ({g0,g3}, {g1}, {g2}, {g4})`: the contract reading survives
(`Y^-_r = {g0,g1,g2,g3}`, `v_r = 5 > 3`) while the referee reading fails
(`Y^-_r = {g0,g1,g2}`, `v_r = 3 = x`). Both are reported separately throughout.

## 7. What this does not decide

- Whether states with `L_alpha` strictly containing `K` and a root-held `K` are
  **reachable** in the real GG pipeline. If some upstream invariant forces
  `L_alpha = K` in the root-holder branch, the star's progress survives — that
  is exactly repair item 4 of the referee report, and it remains open.
- Anything about the nonroot-holder branch
  (`NONROOT_SAFE_WHOLE_HIT_ENVELOPE_DESCENT_THEOREM_20260814.md`), which the
  referee report already found sound. Note that theorem's own claim boundary
  already disclaims "that normalization of other retired support closes" and
  routes "a different retired packet exposed by normalization" out of scope —
  which is the same gap this check measures from the root side.
- S3 registry admissibility (which of `G0--G10` consumes the star's successor
  state) and S4 well-foundedness across *all* admitted operations. This check
  bounds one operation's effect on two coordinates; it does not supply the
  missing global order.
- Findings G1, G4, G5, G6, G8 of the referee report.
- Whether a literal closed cycle exists. The stalling successor's packet is
  held by a nonroot owner, so the next round is routed to the nonroot branch
  rather than back to the star; no star-only recurrence was constructed.

## 8. Recommendation: retire the floor-reset route

The question this check was built to decide — is there a real monotone
coordinate in the small space, or does the operation loop? — has a sharp
answer: **the star advances a declared coordinate if and only if
`L_alpha = K`.** On that slice it works, in all 1,803,708 configurations. Off
it, in all 34,072,500, the packet coordinate does not decrease for the
adversarial response choice, and the collision hitting multiplicity — the
contract's own alternative — strictly increases.

So the route is not repairable by finding a better coordinate; the two
coordinates the contract declares both fail on the same slice. It is
repairable only by discharging repair item 4, i.e. proving `L_alpha = K` in
the root-holder branch. Three reasons to judge that unpromising:

1. `L_alpha` is monotone and never deleted by construction
   (`GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md:50-52`), while `K`
   is one candidate's intersection with it. `L_alpha = K` says no earlier
   retirement under the same physical label survives outside the current
   candidate's cell — an invariant that the ledger's own monotonicity works
   against, and that no document in the corpus asserts.
2. The nonroot-holder branch, which the referee report found sound, already
   disclaims precisely this case: its claim boundary says it does not "prove
   that normalization of other retired support closes", and it routes "a
   different retired packet exposed by normalization" out of scope
   (`NONROOT_SAFE_WHOLE_HIT_ENVELOPE_DESCENT_THEOREM_20260814.md:80-94`). Both
   halves of the holder split therefore stop at the same wall, from opposite
   sides. `L_alpha` strictly containing `K` is not a corner case of the
   argument; it is the case neither half handles.
3. Even granting `L_alpha = K`, three further obligations remain untouched by
   this check: S3 (which `G0--G10` selector consumes the star's successor),
   S4 (a well-founded order no *other* admitted operation increases), and
   findings G1, G6 and G8 of the referee report. The star would still be an
   operation available at essentially every state of the branch that closes
   exactly one of three structurally parallel terminals.

Recommendation: **retire the controlled-floor-reset route** and let `T_0^*`
and `T_{L,perp}^*` absorb the effort. If it is kept alive instead, the minimum
honest statement is "closed on the `L_alpha = K` slice, open otherwise", and
`ROOT_SINGLETON_SUPPLIER_STAR_FLOOR_RESET_CLOSURE_THEOREM_20260814.md` needs
two amendments regardless: the explicit hypothesis `D <= G-k` (its equation (5)
is false without it, section 1/G2c), and either a response-selection rule or
the `L_alpha = K` hypothesis.

## 9. Reproduction

```
/private/tmp/efx-charity-py/bin/python \
  tracks/parkability/model_check_tlx_successor_20260816.py --self-test
/private/tmp/efx-charity-py/bin/python \
  tracks/parkability/model_check_tlx_successor_20260816.py \
  --output results/tlx_successor_model_check_20260816.json
```

The checker is deterministic (sampled spaces use fixed seeds) and imports no
audit module of the branch. `--self-test` runs the input-flip battery
described in section 5.

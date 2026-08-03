# Core-token exchange gate

## Exact status

Four-agent additive EFX remains open.  The fixed-core five-token orbit is now
an exact, adversarially tested gate rather than only a corpus observation.

For the canonical positive (4\times9) pair base

\[
01\mid23\mid45\mid67;\qquad f=8,
\]

the exact CEGAR imposes eligibility, unique owner minima (1,3,5,7), failure
of every discovered EFX completion in the 120-state token orbit, and an
expanding set of global normalized-threshold maximality inequalities.

After 141 cumulative adversarial rounds it has accumulated:

- 137 exact orbit-completion blockers; and
- 42 exact global-maximality witnesses.

It has found many positive valuations whose entire eligible fixed-core token
orbit is blocked.  Every such valuation found so far fails global threshold
maximality.  No globally maximal blocked orbit has been found, and no UNSAT
proof has been obtained.

The last aligned blocked seed has two eligible orbit states and zero completing
states.  Its best exact Hall margin is (-1/3718).  Its fixed base is not a
global threshold maximum; among 120 maximizing bases, 112 are Hall
insertable.  This refutes the token-orbit statement without global maximality,
not the globally maximal theorem.

## Maximality-gap attack

An independent integer annealer preserves all of the following exactly after
every accepted move:

1. positivity and fixed row totals;
2. eligibility of the canonical base;
3. strict owner-minimum identities (1,3,5,7); and
4. failure of every eligible state in the complete 120-state token orbit.

It then maximizes the exact ratio between the fixed base's normalized owner-
threshold score and the globally maximal score.  The ratio improved from
(0.8482932262) to (0.9613170458), but did not reach one.  At the best exact
endpoint,

\[
\Theta(X)=\frac{95851}{55584},\qquad
\Theta^*=\frac{8309}{4632}=\frac{99708}{55584},
\]

so the remaining gap is (3857/55584).  The best orbit Hall margin is only
(-1/55584), but the threshold gap is still strictly positive.

One maximizing competitor has floater 1 and masks

\[
(264,129,80,36),
\]

that is, bundles (\{3,8\},\{0,7\},\{4,6\},\{2,5\}).  Relative to the fixed
pair base, its four normalized-threshold gains, expressed over denominator
55584, are (45,3808,0,4).  Thus almost the entire residual advantage is a
core reassignment for owner 1, outside the five-token orbit.

This is the strategic correction: a proof confined to frozen cores is likely
too narrow at the obstruction boundary.  Global maximality must be used to
force a completing token permutation or a profitable core-token exchange.

## Nearest-exchange refinement

The maximality oracle was strengthened to choose, among all 589,824 labeled
one-floater states, an eligible strictly higher-threshold state with minimum
owner-assignment distance from the blocked base.  In 74 adversarial rounds it
needed only 15 distinct maximality witnesses before the bounded solver timed
out: 13 have distance two and two have distance three.  Thus the previously
heterogeneous global-winner menu collapses locally to swaps and three-slot
cycles.

The complete balanced local menu has 144 states:

- 32 two-slot exchanges, including exchanges with the floater slot; and
- 112 three-slot cycles, including cycles through the floater slot.

The swap-only alternative is exactly false.  The boundary audit exhibits an
orbit-blocked positive valuation with no eligible positive-threshold distance-
two exchange.  Of all 144 local states, only two are eligible: one neutral
floater swap and the three-owner cycle with masks

\[
(3,68,24,160),
\]

which has exact threshold gain \(41/1260\).  The cycle sends goods \(3,5,6\)
through owners \(2,3,1\), respectively, and leaves floater 8 fixed.  Hence a
three-cycle is genuinely necessary; this is not merely solver preference.

## Radius-three falsification

The stronger swap-or-three-cycle alternative is also false away from global
maximality.  A compact Hall-state CEGAR ran for 120 cumulative rounds with 21
whole-orbit Hall cuts and 108 nearest-higher-state cuts.  The witness distances
were 18 at distance two, 56 at distance three, 30 at distance four, and four
at distances five through seven.  It found neither a globally maximal blocked
orbit nor an UNSAT proof.

The final aligned blocked model has exactly one eligible token-orbit state and
no completing orbit state.  None of the 144 balanced radius-three states is
even eligible.  Its nearest eligible higher-threshold state has masks

\[
(8,69,48,130),
\]

shape \(1+3+2+2\), owner distance four, and exact threshold gain
\(403/8220\).  Thus the balanced radius-three menu is not a cover.  The proof
must allow bundle-shape changes and unions of transfer components.

## Connected-completion evidence

Despite the unbounded owner distance, every one of the 108 stored nearest
higher-state witnesses has exactly one nontrivial transfer component.  This
includes the four witnesses at distances five through seven.  Across four
aligned blocked-orbit landmarks, the nearest higher state that is also Hall
insertable is always connected; their distances are two, two, three, and
four, and all have strictly positive exact Hall margin.

The final radius-three boundary has an especially rigid completion
obstruction.  For hosts \(0,1,2,3\), respectively, its unique inclusion-
minimal Hall witnesses are

\[
\{0,3\},\quad\{0,1\},\quad\{1,2\},\quad\{2,3\},
\]

and each pair sees only its corresponding host bundle.  These four deficient
pairs form a cycle.  The nearest higher connected allocation is already Hall
insertable, with exact Hall margin \(19/13152\).

These Hall-completable states are discovery witnesses at the valuations that
generated them.  A stored global-maximality cut remains valid throughout the
cell because it excludes every eligible strict threshold improvement, whether
or not that same allocation remains Hall-completable after the valuation
changes.  The cut pool therefore supports the global-improvement theorem
below, not a universal completing-restart theorem for any fixed allocation.

## Closed four-host edge subcell

Fixing all four host-completion edge graphs to those of the final boundary
profile makes the formula UNSAT.  The exact certificate closed after 86
cumulative CEGAR iterations with 73 global-maximality cuts and 26 whole-state
Hall blockers.  Consequently, inside that exact edge subcell, a globally
threshold-maximal canonical base cannot have its entire eligible token orbit
blocked.

Every one of the 73 global cuts is a connected transfer from the canonical
base: 18 have owner distance two, 30 distance three, and 25 distance four.
All were Hall-completable at their discovery valuations, but only eligibility
and threshold non-improvement occur in the final cut formulas.

This is a new bounded theorem, recorded in
`PARTIAL_THRESHOLD_FOUR_HOST_EDGE_CELL_THEOREM.md`.  It fixes all 64 edge
truth values, rather than only the four cyclic pair-Hall witnesses.  The next
exact gate is to remove the 32 truth values not specified by those four pair
obstructions.

## Diagonal-switch coarsening

The first coarsening pass fixes the source's 24 off-host edge values while
allowing the eight remaining host-edge switches to vary.  Local exact tests
show that all 24 Hamming-one off-host flips are impossible under simultaneous
token-orbit blockage, while five diagonal flips have exact blocked models and
three diagonal flips remain bounded UNKNOWN.  This is local rigidity only;
multiple off-host bits may still change together.

The named-swap lemma and the complete 32-state distance-two exchange menu are
both exactly false in diagonal pattern 1.  The latter countermodel remains
nonmaximal, and its nearest higher Hall-completable allocation is a connected
distance-three transfer.  A fine-grained dynamic CEGAR nevertheless closes
the complete pattern-1 edge cell: 65 global cuts and 116 individual matching
blockers are UNSAT after 50 cumulative iterations.  A fresh staged replay
reproduces the same ordered pools and UNSAT verdict.  All 65 global witnesses
are connected and have owner distance at most four.  Cyclic invariance of the
fixed off-host profile transfers the theorem to patterns 1, 4, 32, and 64;
together with pattern 0, five exact diagonal profiles are closed.  Pattern 2,
representing the other single-bit orbit, initially stalled after
58 global cuts and 70 matching blockers.  A larger merged pool with 69 global
cuts and 149 blockers still times out under both default and QF_LRA-specialized
Z3 after the direct pairwise-inequality rewrite.

The later literal/topology attack closes pattern 2 with a fresh-replayed
63-cut core: 41 connected global moves and 22 completion blockers.  Its cyclic
orbit is \(\{2,8,16,128\}\), so all nine diagonal profiles of Hamming weight
at most one are now closed in the fixed off-host subcell.  The exact theorem
and remaining boundary are recorded in
`PARTIAL_THRESHOLD_DIAGONAL_PATTERN2_THEOREM.md`.

The pattern-1 proof has also been compressed to a fresh-replayed,
solver-minimized UNSAT core with 27 global cuts and 25 matching blockers.  Its
global side consists only of 12 connected swaps and 15 connected four-owner
cycles.  Across the cyclic pattern orbit the full core has eight exchange
templates and 15 completion templates, making it the current analytic
extraction target.  Default Z3, QF_LRA Z3, and independent cvc5 1.3.4 all
return UNSAT on the extracted core.

The theorem, exact map, claim boundaries, and replay commands are recorded in
`PARTIAL_THRESHOLD_DIAGONAL_PATTERN1_THEOREM.md` and
`PARTIAL_THRESHOLD_DIAGONAL_SWITCH_GATE.md`.

## Live analytic lemma

The canonical-pair target is now:

> **Hall-cycle global-improvement alternative.**  If the four host completions of a
> blocked canonical pair base have the cyclic pair-Hall normal form above,
> then either a token-orbit state completes or there is an eligible allocation
> with larger normalized owner-threshold potential.

The arbitrary-core target remains:

> **Augmenting-component-cycle alternative.**  At a globally threshold-
> maximal blocked state, the Hall-wall dependencies generated by failed
> minimum-slot moves contain a directed cycle whose full union is eligible
> and has positive normalized owner-threshold gain, unless an orbit state
> already admits an EFX completion.

Global maximality would exclude the positive-gain outcome.  Unlike the false
fixed-radius statements, the component union may change bundle shapes and may
use every owner in the dependency cycle.

The theorem needed for four-agent EFX is the corresponding statement for
arbitrary frozen cores (R_i), not only this (4\times9) pair cell.  The
canonical lemma is valuable because it isolates the smallest fully populated
core-token exchange pattern; proving it alone would not resolve the
four-agent problem.

The immediate proof work is to sum the four cyclic pair-Hall inequalities and
extract a positive eligible transfer union.  Connected Hall-completable
discovery witnesses identify promising unions but are not themselves a
uniform certificate over the cell.  For the arbitrary-core lift, the
exact transfer-component decomposition already makes threshold gain additive;
the remaining step is cancellation of incoming-target and owner-shortfall
walls around the dependency cycle.

## Claim boundary

Closing the generalized arbitrary-core lemma for all critical-cut sizes would
resolve the four-agent one-charity-good reduction.  Closing only the canonical
pair lemma would settle this stress-test cell.  Neither result by itself would
resolve general additive EFX, which additionally needs a multi-good charity
absorption theorem.

## Reproducible artifacts

- `minimum_slot_orbit_global_threshold_cegar_orbit_first_session4.json`,
  SHA-256
  `c9877c6efb6e3d85fecf0a7b912b9f91247db67a19d16c0efd14d218d1700acf`;
- `minimum_slot_orbit_global_threshold_cegar_orbit_first_session4_orbit_blocked_seed.json`,
  SHA-256
  `ac107ca123a94e541997c23ce3000812cbff5ee7b882bc38b4bf24f4bed65be6`;
- `minimum_slot_orbit_threshold_maximality_anneal_seed29_session2.json`,
  SHA-256
  `12d93161ea955aaef14c772ff38f378069044d52eccd38098face2f6b202628d`;
- `minimum_slot_orbit_swap_only_boundary_audit.json`, SHA-256
  `3e66500a46ec649546aaaa010cdb2a8a9348e7ccfffee38ed1eba3b5f77e400c`;
- `minimum_slot_orbit_nearest_exchange_cegar_session1.json`, SHA-256
  `53123f7bff5709965e1f1e0f752c7d95d811374ed1daef9d8c816b7be746ff0c`;
- `minimum_slot_orbit_local_exchange_radius2_cegar_session1.json`, SHA-256
  `3ad4f2bbbe18a5aa6cbc01a4f2726bba8cf9f06d0a14ee7cf08002c41087bd48`;
- `minimum_slot_orbit_local_exchange_radius2_cegar_session1_orbit_blocked_seed.json`,
  SHA-256
  `86478b7da5df12e80d604a13293c0c08aa615e9198d6165e52aa19feb8d8a66f`;
- `minimum_slot_orbit_hall_state_nearest_cegar_session2.json`, SHA-256
  `3b6146441d44686b4ef6e15f533d6e3cf5160243c93cb219639eaf05134299d7`;
- `minimum_slot_orbit_hall_state_nearest_cegar_session2_orbit_blocked_seed.json`,
  SHA-256
  `d673550b47f7c0d7b7b57bc8ffbda847ef3ac97dd38eaae516967e35e0e73d2b`;
- `minimum_slot_orbit_radius3_boundary_audit.json`, SHA-256
  `513fa95d99e9260350b9f9bd62057e6db7e9cb637d843a00cfcf79bcd60a9afb`;
- `minimum_slot_orbit_four_host_cycle_cegar_session2.json`, SHA-256
  `910d8d0188db22cce81b44fe8593ec102b42e5cefef6896a7dffe69c7d54e034`;
- `minimum_slot_orbit_four_host_cycle_replay_audit.json`, SHA-256
  `86f586b8db909ba2c2452e7b69bb9ad50d370540197a6b87167000116965edb7`;
- `minimum_slot_orbit_four_host_cycle_component_audit.json`, SHA-256
  `31aead6081bb18717254b40008657bdec8c1c500e84b34271a8f027d4bfdb419`;
- `minimum_slot_orbit_hall_encoding_audit.json`, SHA-256
  `db5c5ef0b58a6f142f54c73fce9f3cdd974c695015491a57383d00db5f441f2f`;
- `audit_minimum_slot_exchange_radius.py`;
- `audit_minimum_slot_orbit.py`;
- `run_minimum_slot_orbit_cegar.py`; and
- `anneal_minimum_slot_orbit_maximality.py`.

Shortest exact replay of the aligned blocked orbit:

```sh
python tracks/parkability/audit_minimum_slot_orbit.py \
  --values results/minimum_slot_orbit_global_threshold_cegar_orbit_first_session4_orbit_blocked_seed.json \
  --floater 8 --masks 3,12,48,192 --minima 1,3,5,7 \
  --output /tmp/minimum-slot-orbit-replay.json
```

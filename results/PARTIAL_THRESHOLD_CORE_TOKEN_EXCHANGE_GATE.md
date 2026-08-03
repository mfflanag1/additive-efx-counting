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

## Live analytic lemma

The sharpened exact stress-test lemma is:

> **Swap-or-three-cycle alternative.**  Let the canonical pair base be
> eligible with unique owner minima.  If every eligible state in its
> five-token orbit is Hall-blocked, then either one orbit state admits an EFX
> completion or an eligible balanced state at owner-assignment distance at
> most three has strictly larger normalized owner-threshold potential.

Global maximality would exclude the second outcome.  The 144-state local menu
is a concrete finite target, but it is not yet a proved cover.  Distance two
alone cannot suffice by the exact boundary model.

The theorem needed for four-agent EFX is the corresponding statement for
arbitrary frozen cores (R_i), not only this (4\times9) pair cell.  The
canonical lemma is valuable because it isolates the smallest fully populated
core-token exchange pattern; proving it alone would not resolve the
four-agent problem.

The immediate proof work is now to write the 32 swap and 112 three-cycle gains
owner by owner and combine failure of the eligible token permutations into a
strict cycle inequality.  If that finite menu does not close, the exact solver
should export an incremental proof state rather than reconstructing all cuts:
reconstruction of the earlier 179-cut checkpoint timed out after 180 seconds
before a new model was obtained.

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
  `a14dfa73fe0a6a7162b1599793541498480716d594a5927d0a0f1200be2312d1`;
- `minimum_slot_orbit_nearest_exchange_cegar_session1.json`, SHA-256
  `53123f7bff5709965e1f1e0f752c7d95d811374ed1daef9d8c816b7be746ff0c`;
- `minimum_slot_orbit_local_exchange_radius2_cegar_session1.json`, SHA-256
  `3ad4f2bbbe18a5aa6cbc01a4f2726bba8cf9f06d0a14ee7cf08002c41087bd48`;
- `minimum_slot_orbit_local_exchange_radius2_cegar_session1_orbit_blocked_seed.json`,
  SHA-256
  `86478b7da5df12e80d604a13293c0c08aa615e9198d6165e52aa19feb8d8a66f`;
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

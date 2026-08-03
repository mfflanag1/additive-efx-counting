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

## Live analytic lemma

The exact stress-test lemma is:

> **Core-token exchange alternative.**  Let the canonical pair base be
> eligible with unique owner minima.  If every eligible state in its
> five-token orbit is Hall-blocked, then either the base is not globally
> normalized-threshold maximal or one of the orbit states admits an EFX
> completion.

Equivalently, under orbit blockage, the Hall-wall inequalities should imply
an eligible positive-threshold core-token exchange.  The 42 CEGAR witnesses
are a finite candidate menu for discovering that implication; they are not
yet a proved cover.

The theorem needed for four-agent EFX is the corresponding statement for
arbitrary frozen cores (R_i), not only this (4\times9) pair cell.  The
canonical lemma is valuable because it isolates the smallest fully populated
core-token exchange pattern; proving it alone would not resolve the
four-agent problem.

The immediate proof work is to quotient those witnesses by exchange topology,
write the threshold gain owner by owner, and combine failure of the eligible
token permutations into a strict cycle inequality.  If the quotient does not
close, the exact solver should export an incremental proof state rather than
reconstructing all cuts: reconstruction of the 179-cut checkpoint timed out
after 180 seconds before a new model was obtained.

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

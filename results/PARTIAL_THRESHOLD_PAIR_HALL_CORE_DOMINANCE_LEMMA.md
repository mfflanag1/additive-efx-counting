# Pair-Hall core-dominance lemma

## Result

Four-agent additive EFX and general additive EFX remain open. This checkpoint
removes a real degree of freedom from the canonical full cyclic pair-Hall cell.

Let the partial allocation be

\[
01\mid23\mid45\mid67;\qquad f=8,
\]

with positive additive valuations, unique owner minima
\(v_i(2i+1)<v_i(2i)\), and the cyclic pair-Hall completion obstructions

\[
(0,3),\ (0,1),\ (1,2),\ (2,3)
\]

at hosts \(0,1,2,3\), respectively. Suppose the base is globally maximal
for normalized owner-threshold potential and every eligible state in the
fixed five-token orbit is EFX-completion blocked. Then

\[
v_i(2i)\ge
\max\!\left\{v_i(8),v_i\bigl((2i-1)\bmod 8\bigr)\right\}
\qquad\text{for every }i\in\{0,1,2,3\}.
\]

The first direct certificate proves \(v_1(2)\ge v_1(8)\). Conditional on its
four cyclic images, a second direct certificate proves
\(v_2(4)\ge v_2(3)\). The full antecedent and the pair-Hall cycle are invariant
under simultaneous cyclic relabeling of owners and their paired goods, so
each direct wall lifts to all four owners.

This is a structural lemma inside the canonical pair-Hall cell. It does not
close that cell, lift from canonical pairs to arbitrary four-agent partial
EFX allocations, or prove four-agent or general additive EFX.

## Why the finite certificate proves the implication

The refutation formula uses only consequences of the stated antecedent:

- 159 global-maximality inequalities, including every pair-preserving exchange
  of owner distance at most three;
- 78 individual matching-failure consequences; and
- 30 whole-token-state EFX-completion obstructions.

Any valuation satisfying the full antecedent satisfies this finite subset.
Adding \(v_1(2)<v_1(8)\) makes the finite formula UNSAT. Therefore the full
antecedent also excludes that strict inequality.

Three Z3 profiles reproduce UNSAT:

- QF_LRA: 0.11 seconds;
- default: 1.84 seconds; and
- arithmetic solver 2: 72.79 seconds.

After a syntax-only normalization and bijective valuation-symbol rename,
cvc5 1.3.3 independently returns UNSAT in 0.61 seconds. Exact formula and
artifact hashes are recorded in
minimum_slot_orbit_pair_hall_core_dominance_replay_audit.json.

For the second wall, adding all four core--floater inequalities and then
adding \(v_2(3)>v_2(4)\) makes the same finite consequence pool UNSAT. A
tracked extraction from the earlier 36-leaf cover retains only this one cube
literal. Default, QF_LRA, and arithmetic-solver-2 Z3 replays return UNSAT in
40.13, 77.59, and 62.46 seconds. cvc5 remains UNKNOWN at 180 seconds, so this
second wall is triple-Z3 confirmed but not independently solver-confirmed.
See minimum_slot_orbit_pair_hall_predecessor_token_wall_audit.json.

## Residual gate

Adding both four-row walls does not yet close the pair-Hall master. Default,
QF_LRA, and arithmetic-solver-2 all remain UNKNOWN at 300 seconds.

The earlier one-wall depth-six cover had 36 leaves and initially left 29
UNKNOWN. Assumption-core extraction proves that its entire
\(v_2(3)>v_2(4)\) side is impossible, superseding the raw timeout map. A fresh
exact depth-six cover inside both walls has 58 leaves, four with immediate
UNSAT hints; the cover has not yet been fully decided. No SAT valuation has
been found.

The next proof target is to decide or extract another shared assumption core
from those 58 two-wall leaves. Monolithic timeout extension is not evidence.

## Reproduction

Direct QF_LRA replay:

~~~sh
python tracks/parkability/run_minimum_slot_orbit_cegar.py \
  --timeout-seconds 300 --max-iterations 1 \
  --seed results/minimum_slot_orbit_pair_hall_distance3_pool.json \
  --relabeling-mode cyclic --completion-batch-size 8 \
  --completion-cut-mode orbit_matching --solver-profile qf_lra \
  --global-witness-mode hall_insertable --base-host-pair-hall-cycle \
  --preload-local-exchange-distance 3 \
  --refute-base-owner-core-below-floater 1 \
  --output /tmp/pair-hall-core-dominance-wall.json
~~~

Expected status: BASE_OWNER_CORE_DOMINANCE_FORCED.

Second-wall default replay:

~~~sh
python tracks/parkability/run_minimum_slot_orbit_cegar.py \
  --timeout-seconds 300 --max-iterations 1 \
  --seed results/minimum_slot_orbit_pair_hall_distance3_pool.json \
  --relabeling-mode cyclic --completion-batch-size 8 \
  --completion-cut-mode orbit_matching --solver-profile default \
  --global-witness-mode hall_insertable --base-host-pair-hall-cycle \
  --preload-local-exchange-distance 3 \
  --base-owner-cores-dominate-floater \
  --refute-base-owner-predecessor-token-above-core 2 \
  --output /tmp/pair-hall-predecessor-token-wall.json
~~~

Expected status: BASE_OWNER_PREDECESSOR_TOKEN_DOMINANCE_FORCED.

Focused tests:

~~~sh
pytest -q --disable-warnings \
  tracks/parkability/test_minimum_slot_orbit_cegar.py
~~~

Primary artifacts:

- minimum_slot_orbit_pair_hall_distance3_pool.json;
- minimum_slot_orbit_pair_hall_core_dominance_wall_qflra.json;
- minimum_slot_orbit_pair_hall_core_dominance_replay_audit.json;
- minimum_slot_orbit_pair_hall_core_dominance_cubes_d6.json;
- minimum_slot_orbit_pair_hall_core_dominance_cubes_d6_qflra120.json; and
- minimum_slot_orbit_pair_hall_core_dominance_cubes_d6_default120.json;
- minimum_slot_orbit_pair_hall_predecessor_token_wall_default.json;
- minimum_slot_orbit_pair_hall_predecessor_token_assumption_core.json;
- minimum_slot_orbit_pair_hall_predecessor_token_wall_audit.json; and
- minimum_slot_orbit_pair_hall_two_walls_cubes_d6.json.

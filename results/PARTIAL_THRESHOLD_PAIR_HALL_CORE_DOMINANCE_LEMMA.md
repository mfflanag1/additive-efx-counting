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
v_i(2i)\ge v_i(8)\qquad\text{for every }i\in\{0,1,2,3\}.
\]

The direct certificate proves \(v_1(2)\ge v_1(8)\). The full antecedent and
the pair-Hall cycle are invariant under simultaneous cyclic relabeling of
owners and their paired goods, so the other three inequalities follow.

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

## Residual gate

Adding all four proved inequalities does not yet close the pair-Hall master.
Default and arithmetic-solver-2 both remain UNKNOWN at 300 seconds.

An exact depth-six cube cover has 36 leaves. QF_LRA closes six leaves and
default Z3 closes five; their union closes seven distinct leaves, leaving 29
UNKNOWN. No SAT leaf was found. The tempting additional wall
\(v_2(3)\le v_2(4)\) is not proved: three leaves on its opposite side remain
UNKNOWN.

The next proof target is therefore precise: close or extract witnesses from
those 29 residual polyhedral cells, preferably by deriving another
owner-local ordering wall. Monolithic timeout extension is not evidence.

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
- minimum_slot_orbit_pair_hall_core_dominance_cubes_d6_default120.json.

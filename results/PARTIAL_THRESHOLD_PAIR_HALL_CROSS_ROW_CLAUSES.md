# Pair-Hall cross-row clauses

## Exact result

Work in the canonical cyclic pair-Hall cell with base pairs

\[
01\mid 23\mid 45\mid 67
\]

and floater 8. Assume the archived 159 global-maximality cuts, 78 matching
cuts, 30 whole-orbit blockers, and both previously proved cyclic owner walls.
Then the antecedent forces

\[
v_0(0)\ge v_0(3)
\quad\text{or}\quad
v_2(2)\le v_2(3)+v_2(4),
\tag{A0}
\]

and

\[
v_3(1)\le v_3(3)+v_3(6)
\quad\text{or}\quad
v_0(1)+v_0(4)\ge v_0(3)+v_0(8).
\tag{B0}
\]

Simultaneously rotating owners by one and paired goods by two preserves the
full antecedent. Therefore A0 and B0 each yield four cyclic images, for eight
cross-row clauses in total.

These disjunctions are the first consequences in this route that couple
different valuation rows. They do not close the pair-Hall cell.

A minimized eight-fact structural core now gives a direct human exchange
proof of A0, independently replayed by Z3 and cvc5 in under 0.08 seconds. See
`PARTIAL_THRESHOLD_ROTATING_TOKEN_LEMMA.md`.

## Verification boundary

A0 is directly refuted under its negation by default, QF_LRA, and
arithmetic-solver-2 Z3 in 183.27, 202.09, and 195.88 seconds. B0 is directly
refuted by QF_LRA and arithmetic-solver-2 in 170.80 and 101.03 seconds;
default Z3 remains UNKNOWN after 300 seconds. cvc5 has not confirmed either
clause family.

The clauses were first extracted by tracked deletion from exact cover leaves
18 and 53. The direct runner replays remove dependence on the warmed solver
state used during that extraction. Exact artifact hashes are recorded in
`minimum_slot_orbit_pair_hall_cross_row_clause_audit.json`.

## Residual experiment

Adding all eight clauses to the two-wall master does not solve it
monolithically: default and arithmetic-solver-2 both time out at 300 seconds.
A fresh depth-six exact cover again has 58 leaves. A 60-second-per-leaf
QF_LRA pass proves four UNSAT and leaves 54 UNKNOWN, with no SAT leaf.

Thus the clauses are real structural progress but not a computational closure
by themselves. The next target is an analytic case composition: combine
cyclic images of A0 and B0 with the two owner walls to force either an EFX
completion or a third shared inequality.

## Direct replay

For A0, replace `default` by `qf_lra` or `arith2` to reproduce the other
profiles:

~~~sh
python tracks/parkability/run_minimum_slot_orbit_cegar.py \
  --timeout-seconds 300 --max-iterations 1 \
  --seed results/minimum_slot_orbit_pair_hall_distance3_pool.json \
  --relabeling-mode cyclic --completion-batch-size 8 \
  --completion-cut-mode orbit_matching --solver-profile default \
  --global-witness-mode hall_insertable --base-host-pair-hall-cycle \
  --preload-local-exchange-distance 3 \
  --base-owner-cores-dominate-floater \
  --base-owner-cores-dominate-predecessor-tokens \
  --refute-base-pair-hall-cross-row-core-clause a0 \
  --output /tmp/pair-hall-cross-row-a0.json
~~~

Expected status: `BASE_PAIR_HALL_CROSS_ROW_CORE_CLAUSE_FORCED`.

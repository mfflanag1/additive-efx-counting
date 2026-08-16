# Exact threshold--Hall gradient gate

## Fixed-cell statement

The first symbolic attack fixes four agents, nine goods, base bundles

\[
01\mid23\mid45\mid67,
\qquad f=8.
\]

It asks whether positive row-normalized additive valuations can satisfy all
of the following:

1. the labeled one-floater base is EFX and the floater is unenvied;
2. its exact direct-completion margin \(H\) is negative;
3. whenever either good in an owner pair is owner-minimum and swapping it
   with the floater is eligible, the swap does not raise the owner's threshold
   term; and
4. no such eligible owner-minimum swap has direct-completion margin greater
   than the base margin.

A SAT model would refute this fixed-cell local-gradient statement.  It would
refute the global threshold selector only if exhaustive enumeration
additionally showed that the fixed base is a global threshold maximizer.
UNSAT would prove the local gradient only in the four-pair cell, not arbitrary
bundle shapes.

The generator is
`tracks/parkability/decide_threshold_hall_local_gradient.py`.

## Current exact verdict

Three 60-second Z3 formulations are all `UNKNOWN (TIMEOUT)`:

- nested successor maxima, 516,368-byte SMT-LIB, SHA-256
  `cdac47d167655cb46d316f085302bb3ee44e2708085c6226707be2e5428c1f88`;
- 96 direct successor-margin inequalities per swap, 26,713,610 bytes,
  SHA-256
  `d156efbd47692ce4c8da6879dba5bb290032503c078351925622ff12b970a61b`;
- the direct-inequality encoding with base best-witness index fixed to zero,
  4,048,309 bytes, SHA-256
  `87563d87171107030ffe3a52e274a43f6c350f0803ebbb009b3814030bde363f`.

These are not theorem or counterexample verdicts.  The witness-fixed formula
shows that eliminating the outer maximum is insufficient by itself.

## Next analytic decomposition

The
`PARTIAL_THRESHOLD_MINIMUM_SWAP_OBSTRUCTION_LEMMA.md` removes floater-nonenvy
from every nonsingleton-source swap.  The remaining implication should be
split by its two exact wall types rather than by another long solver run:

1. incoming-target wall, forcing an external observer to rank the old
   floater above the released owner-minimum good; or
2. owner-shortfall wall, forcing the source owner to rank the old floater
   below that good.

The cap-free
`PARTIAL_THRESHOLD_HALL_COMPLETION_MOVE_REDUCTION_LEMMA.md` gives the useful
case split on the *completed* partitions: every strict improving swap becomes
either a one-good transfer, a two-bundle swap, or a three-bundle augmenting
path.  Reinserting the new floater into its source can never be a strict
improvement because it reconstructs an old completion candidate exactly.

For the four-pair cell, selecting one wall for each of the four sources gives
a directed dependency graph on four owners.  The next proof target is a
weighted contradiction for each of the three completed-partition move types,
with the Hall-margin witness fixed only after the move type is known.  This
avoids the 768 guarded matching-margin comparisons that caused the exact
master to stall.

No further runtime on the monolithic formulas is currently justified.

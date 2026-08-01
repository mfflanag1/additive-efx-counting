# Single-Wall Pivot Gate

**Status:** the one-transfer pivot is refuted in all three realizable Hall
sizes; the two-transfer pivot is refuted in Hall sizes two and three; one
seven-good Hall-size-four cell is dual-solver UNSAT at radius two  
**Scope:** four positive-additive agents at one generic subset-sum wall  
**Not claimed:** an EFX counterexample, a proof of row-merge continuation, or
a general radius bound

## Question tested

At a generic wall, an EFX allocation can fail because exactly one feasibility
edge of the moving agent disappears. If that edge is essential to every
perfect matching of the current four bundles, deleting it creates a minimal
Hall witness of size two, three, or four. The first natural pivot conjecture
was:

> After the wall, an EFX-supporting partition can always be reached by moving
> one good, or perhaps two goods, between the four current bundles.

Here distance means the minimum number of goods whose bundle membership must
change, after optimally relabeling the four bundles. A distance-one state is
exactly a legal one-good transfer from a non-singleton bundle.

## Exact refutations

The exact-real driver
[decide_row_merge_single_wall_radius.py](../tracks/parkability/decide_row_merge_single_wall_radius.py)
constructs a wall valuation and a post-wall valuation subject to all of the
following conditions:

1. all item values are strictly positive and additive;
2. the wall equality is \(v_0(U)=v_0(W)\), where the envied bundle is
   \(W\cup\{g\}\);
3. every other disjoint subset-sum comparison is strict and keeps the same
   sign after the perturbation, so this is one generic wall rather than a
   multiple-wall degeneracy;
4. the displayed allocation is EFX at the wall;
5. post-wall, its feasibility graph changes in exactly one place: edge
   \((0,U)\) is deleted; and
6. the resulting minimal Hall witness has the prescribed size.

For the seven-good wall partition

\[
\{0,1\}\mid\{2,3\}\mid\{4,5\}\mid\{6\},
\]

the exact results are:

| Hall size | Radius excluded | Post-wall EFX partitions | EFX allocations | Nearest EFX distance |
|---:|---:|---:|---:|---:|
| 2 | 2 | 9 | 16 | 3 |
| 3 | 2 | 11 | 40 | 3 |
| 4 | 1 | 18 | 57 | 2 |

Thus a one-good pivot fails in all three cases. More strongly, every
partition obtainable by moving at most two goods fails in the size-two and
size-three examples. These are not EFX counterexamples: the last two columns
give the complete, independently enumerated EFX census farther from the
failed partition.

The durable sources are the
[size-two result](row_merge_single_wall_q2_radius2_refutation.json),
[size-three result](row_merge_single_wall_q3_radius2_refutation.json), and
[size-four result](row_merge_single_wall_q4_radius1_refutation.json). The
solver-free
[aggregate audit](row_merge_single_wall_radius_refutation_audit.json)
rechecks positivity, the unique wall crossing, the single changed edge, the
minimal Hall witnesses, all 127 or 19 obstructed nearby partitions, and every
complete allocation of the post-wall instances.

## Positive radius-two boundary in the size-four cell

For the same seven-good bundle shape and a size-four Hall witness, the formula
asserting failure of every radius-two partition is UNSAT. Z3 and cvc5 1.3.3
independently return UNSAT on the archived formula. See the
[Z3 result](row_merge_single_wall_q4_radius2_m7_unsat.json),
[normalized cvc5 formula metadata](row_merge_single_wall_q4_radius2_m7_unsat.cvc5.normalization.json),
and [cvc5 replay](row_merge_single_wall_q4_radius2_m7_unsat.cvc5.json).

This proves only the exact encoded cell: seven goods, bundle sizes
\((2,2,2,1)\), a generic wall, and a minimal Hall witness of size four. It is
not yet a human analytic lemma and does not cover other bundle shapes. At
eight goods, 300-second exact-real attempts for shapes \((2,2,2,2)\) and
\((2,2,3,1)\) returned UNKNOWN rather than a model or proof, so no extension
is recorded.

### Seven-partition core

Assumption-core extraction shrinks the 127 radius-two candidates to a
deletion-minimal menu of seven. Z3 and cvc5 independently prove that these
seven alone cannot all fail:

\[
\begin{aligned}
&013\mid2\mid45\mid6,\\
&014\mid23\mid5\mid6,\qquad
015\mid23\mid4\mid6,\\
&02\mid13\mid45\mid6,\qquad
03\mid12\mid45\mid6,\\
&04\mid15\mid23\mid6,\qquad
05\mid14\mid23\mid6.
\end{aligned}
\]

The first three add one of goods 3, 4, or 5 to the critical bundle
\(\{0,1\}\). The other four exchange one good of \(\{0,1\}\) with one of
the two nonsingleton resident bundles. This is a much more compact analytic
target than the full radius-two ball. Every one of the seven states is
necessary for this solver core: deleting any one makes the formula SAT.

See the [core record](row_merge_single_wall_q4_radius2_m7_core.json), its
[cvc5 normalization](row_merge_single_wall_q4_radius2_m7_core.cvc5.normalization.json),
and the [independent cvc5 replay](row_merge_single_wall_q4_radius2_m7_core.cvc5.json).
This remains a fixed-shape computer-assisted lemma until its seven cases are
converted into a human inequality argument.

## Consequence for the proof program

The Hall classification remains the right cap-free normal form, but a proof
cannot simply repair the broken allocation by transferring the critical good
or by checking a universal menu of one- and two-good moves. In the smallest
Hall cases, the nearest valid state may require a three-bundle exchange cycle.

The next analytic target is therefore a **global Hall exchange lemma**: use
the deficient agent set and the tight comparison to construct an improving
exchange chain, with no fixed bound of two moved goods. A second target is to
prove the seven-state size-four core analytically, then determine which part
of its exchange menu survives arbitrary bundle sizes.

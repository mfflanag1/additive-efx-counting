# Single-Wall Pivot Gate

**Status:** the one-transfer pivot is refuted in all three realizable Hall
sizes; the two-transfer pivot is refuted in Hall sizes two and three; one
seven-good Hall-size-four cell has a two-comparison seven-pivot core; the
balanced eight-good Hall-size-four cell has a dual-solver 11-pivot theorem  
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
not yet a human analytic lemma. The core below sharpens the genericity
hypotheses, and the following section extends the pair-complete construction
to the balanced eight-good shape.

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

### Two-comparison genericity core

The seven partitions do not follow from the post-wall Hall graph alone: if
the perturbation is allowed to cross unrelated subset comparisons, an exact
positive-additive model blocks all 127 radius-two partitions. Tracking all
965 noncritical disjoint subset comparisons and shrinking the resulting
assumption core leaves exactly two:

\[
v_0(014)>v_0(2)\quad\text{and}\quad v_0(015)>v_0(2)
\]

after the perturbation. Because the wall equality is \(v_0(01)=v_0(2)\),
these are precisely

\[
0<\delta<v_0(4),\qquad 0<\delta<v_0(5).
\]

Both bounds together are sufficient and deletion-minimal; either bound alone
admits a SAT model. Thus the full generic-wall machinery is unnecessary for
this cell. Any sufficiently small positive continuation step satisfies the
only two preserved comparisons used by the exact proof.

The durable chain is the
[genericity-core record](row_merge_single_wall_q4_radius2_m7_genericity_core.json),
[raw formula](row_merge_single_wall_q4_radius2_m7_genericity_core.smt2),
[normalization metadata](row_merge_single_wall_q4_radius2_m7_genericity_core.cvc5.normalization.json),
and [cvc5 replay](row_merge_single_wall_q4_radius2_m7_genericity_core.cvc5.json).
Z3 and cvc5 independently return UNSAT.

## Balanced eight-good pair-pivot theorem

Consider the balanced wall partition

\[
01\mid23\mid45\mid67,
\]

with critical equality \(v_0(01)=v_0(2)\), the edge from agent zero to
\(01\) essential, and a minimal post-wall Hall witness containing all four
agents. For

\[
0<\delta<\min\{v_0(4),v_0(5),v_0(6),v_0(7)\},
\]

at least one partition in an explicit 11-state menu supports complete EFX.
The menu consists of:

1. moving critical good 3 into \(01\);
2. the two cross-pairings of \(01\) with \(23\); and
3. for each of \(45\) and \(67\), two transfers into \(01\) and the two
   cross-pairings with \(01\).

The negation is exact QF_LRA UNSAT. Z3 proves the frozen formula in about 125
seconds; pinned cvc5 1.3.3 independently proves its syntax-normalized image
in about 234 seconds. See the
[result](row_merge_q4_small_step_pair_m8.json),
[raw formula](row_merge_q4_small_step_pair_m8.smt2),
[normalization metadata](row_merge_q4_small_step_pair_m8.cvc5.normalization.json),
and [cvc5 replay](row_merge_q4_small_step_pair_m8.cvc5.json).

This is the first positive eight-good wall-pivot cell in the continuation
program. It covers only shape \(2+2+2+2\) and Hall size four. It does not
cover Hall sizes two or three, unbalanced wall shapes, or prove that a row
path can always be continued.

## First unbalanced failure at nine goods

The balanced theorem does not extend to a cap-free radius-two statement.
For wall shape

\[
01\mid23\mid45\mid678,
\]

the 16-state menu containing every transfer and every nontrivial split of
the pair and triple is SAT. Radius-two CEGAR then learned all nearby repairs
from successive models, growing the pool \(16\to27\to32\to37\). The terminal
positive-additive model blocks all 319 partitions within transfer radius two.
Its post-wall feasibility graph still changes only at edge \((0,01)\), and
its unique minimal Hall witness is the full four-agent set with neighborhood
the other three bundles.

This is not an EFX counterexample. Exact enumeration finds 123 supporting
partitions and 206 complete EFX allocations, beginning at distance three.
The nearest supporting partition is

\[
0136\mid27\mid45\mid8.
\]

The durable chain is the
[16-to-27 seed trace](row_merge_q4_small_step_radius2_m9_cegar_seed16.json),
[cvc5 SAT replay of the 27-cut formula](row_merge_q4_small_step_radius2_m9_cegar_seed16.cvc5.json),
[terminal 37-cut trace](row_merge_q4_small_step_radius2_m9_cegar_terminal37.json),
and
[solver-free complete audit](row_merge_q4_small_step_radius2_m9_boundary_audit.json).
This establishes that even Hall size four needs a genuine three-transfer
exchange once a resident bundle has three goods.

Exact motif extraction reduces the full radius-three ball to 515 partitions
formed by simple one-good transfer paths and cycles of length at most three.
The terminal profile has eight EFX-supporting partitions in this menu. The
resulting universal candidate remains open: a 24-cut exact master is SAT with
48 repairs, a fixed-graph 32-cut master is SAT with nine repairs, and the
strengthened 56-cut cell times out under matching-clause and Hall-selector
encodings. See
[ROW_MERGE_EXCHANGE_CHAIN_GATE.md](ROW_MERGE_EXCHANGE_CHAIN_GATE.md).

## Consequence for the proof program

The Hall classification remains the right cap-free normal form, but a proof
cannot simply repair the broken allocation by transferring the critical good
or by checking a universal menu of one- and two-good moves. In the smallest
Hall cases, the nearest valid state may require a three-bundle exchange cycle.

The next analytic target is therefore a **global Hall exchange lemma**: use
the deficient agent set and the tight comparison to construct an improving
exchange chain whose length can grow with bundle size. The compact positive
targets are the seven-state \(2+2+2+1\) lemma and the symmetric 11-state
\(2+2+2+2\) lemma; the nine-repair fixed-graph boundary now isolates the first
required three-transfer case split. A human proof should expose the
resident-matching Hall witnesses shared by these positive cores and explain
how that motif propagates.

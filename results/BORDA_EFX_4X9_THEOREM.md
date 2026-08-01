# Borda-Additive EFX at \(4\times 9\)

**Status:** computer-assisted theorem candidate, dual-encoding audit passed  
**Scope:** four agents, nine goods, Borda-additive valuations  
**Not claimed:** arbitrary additive valuations or the general EFX conjecture

## Result

Call an additive instance **Borda-additive** when, for each agent, the nine
item values are a permutation of

\[
1,2,\ldots,9.
\]

Independent positive scaling of an agent's row is immaterial. Adding a
constant to every item is not included, because bundles have unequal sizes.

The certified computational statement is:

> **Borda \(4\times9\) shape theorem candidate.** Every four-agent,
> nine-good Borda-additive instance has a complete EFX allocation whose
> bundle-size multiset is \((3,2,2,2)\).

The result is stronger than merely finding some complete EFX allocation in
this subclass: it fixes the allocation shape.

## Basic explanation

Each agent ranks all nine goods strictly and assigns Borda scores from 1 to
9. The search considers ways to split the goods into one triple and three
pairs. For each split, it asks which agents could receive which bundle while
satisfying every EFX comparison. This gives a four-by-four bipartite graph.
The split supports EFX exactly when that graph has a perfect matching.

The proof is by contradiction. A finite-domain solver was asked to construct
four Borda rows for which every pooled triple-plus-three-pairs split has no
perfect matching. It proved that no such rows exist in each of the five
possible favorite-good collision patterns.

## Exact reduction

For a partition \(P=(B_1,\ldots,B_4)\), agent \(i\) is adjacent to bundle
\(B_b\) when

\[
\sum_{g\in B_b}v_i(g)
\;\ge\;
\sum_{g\in B_c\setminus\{h\}}v_i(g)
\]

for every \(c\ne b\) and every \(h\in B_c\). A perfect matching assigns one
distinct bundle to each agent and is exactly a complete EFX allocation.

The integer master uses variables \(x_{ig}\in\{1,\ldots,9\}\) and an
all-different constraint in every row. Thus every row is exactly a
permutation of \(1,\ldots,9\); there is no discretization approximation.
Strict EFX violation is encoded as

\[
\sum_{g\in B_b}x_{ig}+1
\;\le\;
\sum_{g\in B_c\setminus\{h\}}x_{ig}.
\]

Every comparison Boolean is reified in both directions. The two obstruction
encodings are:

1. **Matching clauses.** For each of the \(4!=24\) bundle assignments, at
   least one EFX comparison must fail.
2. **Hall selectors.** Some nonempty agent set \(S\) must have its feasible
   neighborhood contained in a bundle set \(T\) with \(|T|<|S|\).

These encodings are logically equivalent but structurally different.

## Favorite-orbit coverage

Every Borda row has a unique favorite good. Up to permuting agents and goods,
the multiplicities of the four favorite goods have exactly five forms:

| Multiplicity | Representative favorite map |
|---|---|
| \(4\) | \((0,0,0,0)\) |
| \(3+1\) | \((0,0,0,1)\) |
| \(2+2\) | \((0,0,1,1)\) |
| \(2+1+1\) | \((0,0,1,2)\) |
| \(1+1+1+1\) | \((0,1,2,3)\) |

All five cells were solved without lexicographic stabilizers, row-distinctness
cuts, universal-minimum cuts, or peelability cuts. Relabeling an arbitrary
profile into its representative cell and then undoing the relabeling
therefore covers every Borda profile.

## Frozen evidence

All ten cells use the same 417-partition pool. Every pooled partition has
shape \((3,2,2,2)\). There are 1,260 unlabeled partitions of that shape in
total; the 417 pooled obstructions suffice.

| Favorite type | Matching clauses | Hall selectors |
|---|---:|---:|
| \(4\) | 127.20 s | 265.13 s |
| \(3+1\) | 50.21 s | 92.84 s |
| \(2+2\) | 34.37 s | 74.43 s |
| \(2+1+1\) | 14.44 s | 38.87 s |
| \(1+1+1+1\) | 7.45 s | 19.55 s |

The machine-readable entry point is
[`efx49_borda_shape3222_dual_encoding_audit.json`](efx49_borda_shape3222_dual_encoding_audit.json).
It rehashes every result, exported CP-SAT model, and pool; checks every scope
flag; verifies the common pool; and confirms all ten infeasibility verdicts.

Re-run the audit and differential tests with:

```bash
make verify-parkability PYTHON=/Users/maxf/miniforge3/bin/python3.10
```

The core implementation is:

- [`integer_partition_master.py`](../tracks/parkability/integer_partition_master.py);
- [`run_integer_partition_cegar.py`](../tracks/parkability/run_integer_partition_cegar.py); and
- [`audit_borda_shape_theorem.py`](../tracks/parkability/audit_borda_shape_theorem.py).

The comparison and Hall encodings agree exhaustively on all 192
two-agent/three-good matrices with values in \(\{1,2\}\), across all three
nonempty bundle partitions.

## Trust boundary

The evidence is exact finite-domain reasoning, not floating-point
optimization. Two independent obstruction encodings agree in all five
favorite cells, and their exported models are hash-pinned.

The ten full cells were nevertheless solved by OR-Tools CP-SAT. A
non-stabilized ten-minute Z3 QF_LIA/Hall replay on the full 790-partition
\(2+1+1\) cell returned `unknown`.

The reduced \(2+1+1\) cell is substantially more hardened:

- both CP-SAT encodings close its 17-partition core in under 0.5 seconds;
- Z3 proves the QF_LIA/Hall formula UNSAT in 16.4 seconds;
- pinned cvc5 1.3.3 independently returns UNSAT in 31.6 seconds; and
- cvc5 emitted a 52.3 MB CPC proof with 555,808 proof steps, which the
  separate Ethos 0.2.3 checker accepted as `correct`.

The certificate record is
[`efx49_borda_shape3222_favorites211_core17_cpc_ethos.json`](efx49_borda_shape3222_favorites211_core17_cpc_ethos.json).
The other four full favorite-orbit cells do not yet have external proof logs,
so the conservative label for the combined theorem remains
**computer-assisted theorem candidate**.

## Relation to the general additive-EFX goal

This does not resolve arbitrary additive \(4\times9\), let alone arbitrary
numbers of goods. General item values can have unequal gaps and near-zero
goods; Borda rows have the rigid spectrum \(1,\ldots,9\). The full
small-integer counterexample bound for nine goods is 19,683, and the same
hard \(2+1+1\) residual cell remains solver-unknown at that cap.

The analytic value is the shape and core structure:

- all ten Borda cells close using only \(3+2+2+2\) partitions;
- in the stabilized \(2+1+1\) cell, deletion shrinking gives a
  17-partition minimal core; and
- those 17 partitions form a small family centered on repeated pair
  exchanges.

The rank-cap experiment now locates the first sharp boundary. The same
\(3+2+2+2\) conclusion is solver-closed when every row uses nine distinct
integers from \(\{1,\ldots,10\}\) or \(\{1,\ldots,11\}\), but it fails at
cap 12. The cap-12 witness still has 838 complete EFX allocations, all with
a singleton bundle that isolates the common favorite. See
[`RANK_GAP_EFX_4X9.md`](RANK_GAP_EFX_4X9.md).
Adding those singleton repairs gives a dual-encoded complete-EFX theorem
candidate for the entire rank-distinct cap-12 domain.
At cap 13, all five matching cells and all five Hall-selector cells still
close under the broader alternative “balanced or designated-favorite
singleton.”

The next breakthrough-conversion target is therefore a two-branch lemma:
balanced Hall completion when the common favorite is moderate, and
singleton completion when it is dominant.

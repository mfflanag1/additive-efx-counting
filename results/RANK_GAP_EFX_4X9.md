# Rank-Gap Boundary for Additive EFX at \(4\times9\)

**Status:** dual-encoded theorem candidate through cap 13  
**Scope:** four agents, nine goods, nine distinct positive integer values per
agent  
**Not claimed:** arbitrary additive valuations or an externally proof-checked
cap-13 theorem

## The rank-cap ladder

Let \(\mathcal D_K\) be the class of additive \(4\times9\) instances in which
each agent assigns the nine goods distinct integer values from
\(\{1,\ldots,K\}\). The score set and its assignment to goods may differ
between agents.

The matching-clause master closes every favorite-multiplicity orbit over
\(\mathcal D_{10}\) and \(\mathcal D_{11}\): every such instance has a
complete EFX allocation of bundle shape

\[
(3,2,2,2).
\]

This strictly extends the Borda case \(K=9\). The five orbit representatives
are \(0000,0001,0011,0012,0123\). The runs use the same 417-partition pool as
the Borda theorem and only sound relabeling stabilizers: agents sharing a
favorite are lex-ordered, as are goods that are nobody's designated
favorite.

| Cap | \(4\) | \(3+1\) | \(2+2\) | \(2+1+1\) | \(1+1+1+1\) |
|---:|---:|---:|---:|---:|---:|
| 10 | 92.98 s | 10.76 s | 13.35 s | 7.38 s | 15.76 s |
| 11 | 156.84 s | 22.26 s | 26.72 s | 16.45 s | 6.42 s |

These cap-10/11 runs are exact finite-domain CP-SAT infeasibility verdicts.
The stronger cap-12 statement below has now received dual-encoding coverage,
so it subsumes their complete-EFX conclusion.

## The fixed shape breaks at cap 12

The cap-11 result is sharp in this ladder. At \(K=12\), the four
non-common-favorite orbits still close against the 417 partitions, but the
common-favorite orbit contains the following profile:

\[
\begin{pmatrix}
12&8&7&6&5&4&3&2&1\\
12&8&7&6&5&4&1&3&2\\
12&8&7&5&6&4&2&3&1\\
12&8&7&5&6&4&1&3&2
\end{pmatrix}.
\]

Every row has nine distinct positive values and good \(0\) is every agent's
unique favorite. Literal enumeration of all \(4^9=262{,}144\) labeled
allocations gives:

| Bundle shape | Complete EFX allocations |
|---|---:|
| \(3+2+2+2\) | 0 |
| \(3+3+2+1\) | 636 |
| \(4+2+2+1\) | 202 |
| **Total** | **838** |

Equivalently, among all 7,770 unlabeled nonempty four-bundle partitions,
exactly 48 support an EFX matching: 37 have shape \(3+3+2+1\), 11 have
shape \(4+2+2+1\), and all 48 isolate the common favorite as the singleton
\(\{0\}\).

The frozen independent census is
[`efx49_rankgap12_shape_boundary_audit.json`](efx49_rankgap12_shape_boundary_audit.json).
It re-enumerates every labeled allocation with the literal EFX definition
and separately reconstructs every feasible agent--bundle graph.

## What the boundary says analytically

The equal-gap argument is not robust under arbitrary widening: at cap 12 a
top gap of four appears, and the balanced \(3+2+2+2\) shape can fail.
Complete EFX does not become scarce; it changes shape and isolates the
dominant common favorite.

This points to a two-branch proof architecture for the common-favorite cell:

1. **balanced branch:** when the common favorite is not too dominant, find a
   \(3+2+2+2\) allocation by the Hall/matching argument;
2. **singleton branch:** give the common favorite alone to one agent and use
   a three-agent EFX allocation of the remaining eight goods, while choosing
   the singleton owner/allocation so that the owner does not strongly envy a
   remaining bundle.

The second branch is the precise missing lemma. Other agents can never
strongly envy the singleton bundle, because removing its only good leaves
the empty set. Only the singleton owner's comparisons remain to be
controlled.

## Dual-encoded complete EFX at cap 12

Feeding all 48 singleton repairs into the complete-partition master grows the
pool from 424 to 472 partitions. A one-worker 300-second run on that frozen
pool returned `unknown`, but an eight-worker portfolio replay proved the
common-favorite cell infeasible in 88.88 seconds. Rebuilding the certificate
one singleton repair at a time then reduced the repair family from 48 to two
canonical partitions:

\[
\{0\}\mid\{1,2\}\mid\{3,4\}\mid\{5,6,7,8\},
\qquad
\{0\}\mid\{1,2\}\mid\{3,4,6\}\mid\{5,7,8\}.
\]

Together with the 424 balanced partitions, this 426-partition pool is
infeasible under both encodings. The good labels are canonical under the
sound unused-good lexicographic stabilizer. The other four favorite orbits
were already closed by balanced allocations. Therefore the current exact
discovery statement is:

> Every instance in \(\mathcal D_{12}\) has a complete EFX allocation.

The same frozen pools were independently rebuilt with explicit Hall
deficiency selectors. All five Hall cells are infeasible as well. The
machine-readable ten-cell audit is
[`efx49_rankgap12_dual_encoding_audit.json`](efx49_rankgap12_dual_encoding_audit.json).
It verifies every scope flag, pool and exported-model hash.

More strongly, the hard common-favorite proof uses only 424 balanced
partitions and two partitions that isolate the common favorite. Thus:

- the \(3+2+2+2\) extension is **disproved** at cap 12;
- complete EFX at cap 12 is **dual-encoding solver-closed** across all
  favorite orbits;
- the hard cell has an exact sparse 426-partition
  **balanced-or-singleton** certificate; and
- the active human gate is the common-favorite singleton-completion lemma
  proved as an exact reduction in
  [`COMMON_FAVORITE_SINGLETON_REDUCTION.md`](COMMON_FAVORITE_SINGLETON_REDUCTION.md).

The sparse machine-readable audit is
[`efx49_rankgap12_sparse_common_audit.json`](efx49_rankgap12_sparse_common_audit.json).
Both encodings still use OR-Tools CP-SAT, and the cap-12 cells do not yet
have external proof logs. The conservative status is therefore
**computer-assisted theorem candidate**. This boundary is substantially
closer to a reusable proof idea than the original 17-partition Borda core:
it identifies both the failure mode and the repair shape.

## Cap 13: balanced or isolate a designated favorite

At cap 13, the balanced shape also fails in the \(3+1\) and \(2+2\)
favorite orbits. Independent literal audits give:

| Favorite orbit | Labeled complete EFX | Supporting partitions | Repair |
|---|---:|---:|---|
| \(3+1\) | 467 | 106 | every partition isolates favorite good 0 or 1 |
| \(2+2\) | 350 | 101 | every partition isolates favorite good 0 or 1 |

Neither profile has a \(3+2+2+2\) EFX allocation. Their EFX allocations
have shapes \(3+3+2+1\), \(4+2+2+1\), or \(4+3+1+1\). The frozen matrices
and complete censuses are in
[`efx49_rankgap13_shape_boundaries_audit.json`](efx49_rankgap13_shape_boundaries_audit.json).

Adding those repairs yields the following cap-13 structural pools:

| Favorite orbit | Pool | Structural family |
|---|---:|---|
| \(4\) | 446 | balanced or singleton favorite 0 |
| \(3+1\) | 560 | balanced or singleton favorite 0 or 1 |
| \(2+2\) | 535 | balanced or singleton favorite 0 or 1 |
| \(2+1+1\) | 417 | balanced |
| \(1+1+1+1\) | 417 | balanced |

All five matching-clause masters are infeasible. Therefore:

> **Rank-cap-13 theorem candidate.** Every instance in \(\mathcal D_{13}\)
> has an EFX allocation that is either of shape \(3+2+2+2\), or isolates
> one of the designated favorite goods as a singleton.

Hall-selector masters independently close all five cells. For the hard
common-favorite orbit, a sparse rebuild reduces the pool from 536 to 446
partitions: 427 balanced partitions, 14 of shape \(3+3+2+1\), and five of
shape \(4+2+2+1\). Both the matching-clause and Hall-selector masters are
infeasible on exactly that hash-identical pool. Thus cap 13 is fully
dual-encoded. The machine-readable trust ledger is
[`efx49_rankgap13_theorem_audit.json`](efx49_rankgap13_theorem_audit.json).

Cap 13 is now the fully dual-encoded frontier. It remains far from the
sufficient arbitrary-value cap
\(19{,}683\), but the stable structural alternative is now clearer:

\[
\text{balanced EFX}\quad\text{or}\quad
\text{favorite-singleton EFX}.
\]

## Cap 14: the balanced-only ladder breaks again

The balanced branch does not extend by itself through cap 14. In the
favorite-\(2+1+1\) orbit, the matching-clause CEGAR produced the exact
profile

\[
\begin{pmatrix}
14&7&8&6&5&4&3&2&1\\
14&7&8&6&5&4&1&3&2\\
7&14&12&13&6&1&3&2&4\\
12&13&14&9&2&6&3&4&1
\end{pmatrix}.
\]

It has no balanced EFX allocation. Exhaustive replay over all \(4^9\)
labeled allocations nevertheless finds 298 complete EFX allocations on 85
unlabeled partitions: 183 labeled allocations have shape \(3+3+2+1\) and
115 have shape \(4+2+2+1\). Every repair isolates one of goods \(0,1,2\),
the three goods designated as a strict favorite by at least one agent.

Thus this is not an EFX counterexample. It refutes only the cap-14
balanced-shape extension and supplies a new sharpness witness for the
broader alternative

\[
\text{balanced EFX}\quad\text{or}\quad
\text{designated-favorite-singleton EFX}.
\]

The independent literal and partition census is
[`efx49_rankgap14_favorites211_boundary_audit.json`](efx49_rankgap14_favorites211_boundary_audit.json).
Adding all 85 repairs to the learned balanced pool gives a 624-partition
structural master. Its matching-clause encoding is infeasible, proving the
bounded \(2+1+1\) cell under that encoding. The hash-identical Hall-selector
replay returned unknown after 1,200 seconds, so this cell is not yet
dual-closed. The all-distinct-favorites cell is dual-closed on its 417
balanced partitions. The common-favorite, \(3+1\), and \(2+2\) cells remain
open at cap 14; no cap-14 theorem is claimed. Because cap 13 is already
closed, an exact cap-14 countermodel must use the value 14. Adding this
sound upper-used cut did not close the remaining gates: the common-favorite
matching run learned 16 repairs, growing its pool from 482 to 498, then
timed out; the \(3+1\) and \(2+2\) matching runs timed out on pools 560 and
535; and the upper-used Hall replay of the 624-partition \(2+1+1\) cell also
timed out. These are `MASTER_UNKNOWN` results, not counterexamples.

## Beyond the cap: exact-real stress tests

The finite 446-partition common-favorite pool is not a cap-free certificate.
An exact positive-real model with nine distinct values in every row avoids
every partition in that pool. Exhaustive literal replay nevertheless finds
104 complete EFX allocations supported by 39 new partitions, and every one
isolates the common favorite. This is a counterexample to the fixed repair
pool, not to the structural alternative or to EFX existence. See
[`efx49_common_favorite_real_frontier_audit.json`](efx49_common_favorite_real_frontier_audit.json).

The converse boundary also occurs: another strict common-favorite profile
has 2,231 complete EFX allocations, all balanced, and no singleton EFX
allocation. Hence neither branch can replace the other. See
[`efx49_common_favorite_real_balanced_boundary_audit.json`](efx49_common_favorite_real_balanced_boundary_audit.json).

A targeted anneal found a common-favorite profile with only 18 complete EFX
allocations on two partitions; all 18 isolate the favorite. Three
independent 60,000-step continuations and all 841 positive one-row transfers
preserving the common-favorite cell failed to improve it. This is
local-search evidence, not a minimality theorem. The frozen exhaustive audit
is [`efx49_common_favorite_boundaries_audit.json`](efx49_common_favorite_boundaries_audit.json).

One extreme \(6+1+1+1\) repair has the exact Hall characterization in
[`RESIDUAL_THRESHOLD_MATCHING_LEMMA.md`](RESIDUAL_THRESHOLD_MATCHING_LEMMA.md).
However, the stronger “balanced or \(6+1+1+1\)” cover is false already at
cap 13; favorite-singleton repairs of intermediate shapes are essential.

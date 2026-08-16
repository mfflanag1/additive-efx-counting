# Generalization Map After Additive EFX at \((4,8)\)

**Snapshot:** 2026-07-30 EDT  
**Status:** research-program design based on formally proved structural
lemmas and exact state-space counts; no existence claims are made for the
next cells

## What already generalizes

Two results developed for the \((4,8)\) proof are not specific to four agents.

### Favorite matching at \(m=2n\)

The Lean theorem
`EFX48.favorite_matching_allocation` is stated for arbitrary finite agent and
good types. If the \(2n\) goods can be written as one distinct favorite plus
one extra good for every agent, then the resulting pairs form a complete EFX
allocation.

The new generic theorems `EFX48.favorite_small_bundles_efx` and
`EFX48.admitsEFX_of_favorite_small_bundles` isolate the actual fairness
argument: any valid allocation is EFX when every agent owns a favorite good
and every bundle has size at most two. This is the reusable lemma needed to
extend the construction from \(m=2n\) to \(n\le m\le2n\).

That allocation step is now also formalized. Given an injective favorite map
and an embedding from the nonfavorite goods into the agents,
`EFX48.favoriteFiberAllocation_valid` assigns every good exactly once and
`EFX48.favoriteFiberAllocation_card_le_two` proves that each bundle has at
most two goods. The theorem
`EFX48.admitsEFX_of_injective_favorites_and_extra_embedding` composes this
construction with the fairness lemma. Finally,
`EFX48.admitsEFX_of_injective_favorites_of_card_le_twice` derives the
extra-good embedding automatically from \(m\le2n\). Thus the entire
injective-favorite case is now formal for arbitrary finite
\(n\le m\le2n\).

Equivalently, when the agent--favorite-good graph has a matching saturating
all agents, EFX follows immediately. Therefore every counterexample at
\(m=2n\) must already be Hall-deficient in its favorite graph.

With strict rankings, the first canonical split is governed by the integer
partitions of \(n\): all favorite multiplicity patterns except
\(1+\cdots+1\). If only the all-common-favorite cell is refined by
second-favorite multiplicity, the first two ranking levels produce

\[
2p(n)-2
\]

candidate cells, where \(p(n)\) is the integer-partition function. This gives
8 cells for \(n=4\), 12 for \(n=5\), and 20 for \(n=6\). Further refinements
may still be needed for effective terminal solving.

### Threshold-cycle normal form

The Lean theorem `EFX48.threshold_cycle_normal_form` is also generic over
finite agent and good types. For nonnegative additive valuations, any valid
EFX allocation with nonempty bundles can be permuted along maximal-threshold
cycles until some owned good is removable.

The separate theorem
`allocation_nonempty_of_positive_efx_of_card_lt` shows that strict positivity
forces nonempty bundles whenever there are more goods than agents. Hence the
parking normal form applies throughout the positive near-diagonal program,
not just at \((4,8)\).

These two pieces are reusable mathematics. The eight-cell enumeration and
terminal certificate are the parameter-specific parts.

## The next-cell dependency ladder

The two residual cuts have a useful recursive structure:

- a **universal-minimum** good reduces \((n,m)\) to \((n,m-1)\); and
- a **peelable** agent--good pair reduces \((n,m)\) to
  \((n-1,m-1)\).

The new \((4,8)\) theorem therefore unlocks two immediate targets:

```text
published: three agents, any number of goods
published: m <= n + 3
                    │
                    ▼
             proved here: (4,8)
                ┌───┴───┐
                ▼       ▼
              (4,9)   (5,9)
                └───┬───┘
                    ▼
                  (5,10)
```

- At \((4,9)\), deleting a universal minimum invokes the new \((4,8)\)
  theorem; deleting a peelable pair invokes the published three-agent
  theorem.
- At \((5,9)\), deleting a universal minimum invokes the published
  \(m=n+3\) theorem at \((5,8)\); deleting a peelable pair invokes the new
  \((4,8)\) theorem.
- If both \((4,9)\) and \((5,9)\) are later proved, they supply the two
  residual inputs for \((5,10)\), the next \(m=2n\) cell.

This does not prove any arrow's target. It says that the same residual
architecture would remove two large, structurally easy regions from each
next search.

## Exact computational growth

For \(m\) goods and \(n\) agents, the partition/matching encoding uses
\(S(m,n)\) unlabeled nonempty partitions and excludes \(n!\) matchings per
partition.

| Cell | Unlabeled partitions \(S(m,n)\) | Labeled onto allocations \(n!S(m,n)\) | Favorite-cell consequence |
|---|---:|---:|---:|
| \((4,8)\) | 1,701 | 40,824 | 8 cells after the common-favorite refinement |
| \((4,9)\) | 7,770 | 186,480 | Distinct favorites no longer close the cell |
| \((5,9)\) | 6,951 | 834,120 | Provisionally 12 after extending the size-\(\le2\) construction |
| \((5,10)\) | 42,525 | 5,103,000 | 12 under the \(m=2n\) construction |
| \((6,12)\) | 1,323,652 | 953,029,440 | 20 under the \(m=2n\) construction |

This table gives a practical conclusion:

- \((4,9)\) is the closest direct extension in raw partition count, but it
  loses the favorite-matching closure because nine goods cannot all be put
  into four bundles of size at most two;
- \((5,9)\) has a comparable number of partitions but five times as many
  bundle matchings per partition; unlike \((4,9)\), its four unmatched goods
  can be placed one per agent, so distinct favorites should still give EFX;
- \((5,10)\) probably needs stronger analytic reductions or learned small
  cores before full proof production; and
- brute-force replication of the current terminal formulas is not a viable
  route to \((6,12)\).

## Recommended next experiments

### 1. Reuse the proof architecture at \((4,9)\)

Generalize only the parameterized definitions needed for nine goods:
positivity, normalization, strict perturbation, favorite cells, stabilizers,
and partition matching. Use the established \((4,8)\) theorem for the
universal-minimum residual cut. Unlike at eight goods, the injective-favorite
cell must be retained or replaced by a new construction controlling the
inevitable three-good bundle. Before full CPC production, probe all top-level
favorite multiplicities and refine only the hard cells.

### 2. Attack \((5,9)\) as the next \(n+4\) frontier

The residual inputs are already available once \((4,8)\) is accepted. The
full allocation construction is formalized as
`admitsEFX_of_injective_favorites_of_card_le_twice`. The main new burden is
then five-agent canonical coverage and the larger
\(5\times5\) matching obstruction. Hall-selector encodings may be
substantially smaller than enumerating all 120 perfect matchings.

### 3. Learn reductions common to both cells

The current 200-core suggests an “anchored favorite goods” family of
partitions. Test whether every terminal cell can be closed using only
partitions in which distinct favorite representatives lie in separate
bundles. If true, this would replace much of the Stirling-number growth with
a targeted partition family.

### 4. Feed existence back into counting

The \((4,8)\) existence theorem supplies only a lower bound of one complete
EFX allocation. The additive counting conjecture asks for at least four.
Analyze whether threshold-cycle rotations from one EFX allocation necessarily
generate multiple distinct allocations, and whether the terminal proof can
be strengthened from “some perfect matching exists” to “at least four
labeled EFX allocations exist.”

### 5. Separate reusable mathematics from parameter certificates

Refactor future formal work around generic interfaces for:

- favorite-matching constructions with bundles of size at most two;
- threshold-cycle normal form;
- universal-minimum and peelable reductions;
- canonical ranking-cell coverage; and
- fixed-partition Hall obstructions.

The \((4,8)\) proof can then serve as the first instantiated certificate in a
larger family rather than as a one-off development.

## Current priority order

1. Freeze and reproduce the \((4,8)\) end-to-end package.
2. Shrink and explain the `favorite-211` core.
3. Prototype \((4,9)\) terminal generation and compare matching clauses with
   Hall selectors.
4. Formalize the parameter-generic parts exposed by that prototype.
5. Attempt \((5,9)\), then use both results to assess \((5,10)\).

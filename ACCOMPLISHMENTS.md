# Accomplishments and claim status

## 1. Six exact count-\(n\) witnesses

The project gives six positive additive valuation matrices whose complete set
of labeled EFX\(_0\) allocations has size exactly \(n\):

| Cell | Allocation space | Exact count | Instance |
|---:|---:|---:|---|
| \((4,7)\) | \(4^7=16{,}384\) | 4 | `results/t47.json` |
| \((5,8)\) | \(5^8=390{,}625\) | 5 | `results/ch5_A.json` |
| \((6,9)\) | \(6^9=10{,}077{,}696\) | 6 | `results/tight69_witness.json` |
| \((4,8)\) | \(4^8=65{,}536\) | 4 | `results/tb4.json` |
| \((4,9)\) | \(4^9=262{,}144\) | 4 | `results/tight49_witness.json` |
| \((4,10)\) | \(4^{10}=1{,}048{,}576\) | 4 | `results/tight410_witness.json` |

Across the six cells, each of three implementations checks all 11,860,961
labeled allocations. Two pure-Python verifiers use independent enumeration
and bundle-checking strategies; a NumPy implementation supplies a third path.
All entries are positive, so the EFX\(_0\) and positive-good EFX conventions
coincide on these instances.

What this proves: the additive minimum count is at most \(n\) at these six
cells.

What it does not prove: that the minimum is \(n\), or even that every
unrestricted additive instance has an EFX allocation.

## 2. Generalized single-floater parking theorem

For an EFX\(_0\) allocation \(B\) of all goods except \(f\), the project proves
an exact observer-host inequality characterizing when adding \(f\) to a chosen
host preserves EFX\(_0\). This strictly generalizes the universal-minimum
parking argument: only the \((6,9)\) witness uses a universal-minimum floater.

Seven machine-checkable certificates cover the six paper witnesses plus a
second \((4,8)\) basin. They record the base allocation, floater, complete
observer-by-host slack matrix, source hashes, and exact EFX\(_0\) count.

## 3. Bounded \((4,7)\), \(K=4\) counting result

The archived result is:

> Every positive integer \(4\times7\) additive valuation matrix with entries
> in \(\{1,2,3,4\}\) has at least four labeled EFX\(_0\) allocations.

The final alternative terminal pool contains 1,240 distinct allocations. The
slot-protected CP-SAT master is infeasible, and an independently built
literal-slot CNF is UNSAT. The frozen CNF has 282,029 variables and 600,624
clauses. Its compressed binary DRAT proof is archived and was checked with the
pinned `drat-trim` revision.

The original historical terminal pool was not retained: only a periodic
checkpoint survived. The current package therefore presents an alternative
complete terminal pool, not a reconstruction of the missing historical cuts.
The Z3 replay timed out with `UNKNOWN` and is explicitly not evidence.

This theorem is finite. It does not cover values above 4, zero-valued goods, or
arbitrary positive reals, and there is no known magnitude-reduction theorem
that extends it.

## 4. Reproducibility and audit engineering

The project now includes:

- hash-pinned instance, verifier, pool, formula, CNF, and proof artifacts;
- differential tests for the threshold CNF translation and slot boundary;
- semantic replay of all retained exact-real CEGAR refinements;
- an independent standard-library verifier for the chamber certificates;
- a deterministic 57-file paper-supplement builder with clean-index,
  inventory, path-safety, metadata, and snapshot-binding checks; and
- a provenance record separating current claims from withdrawn or exploratory
  campaign material.

The paper package distinguishes ordinary proof, exhaustive computation, solver
evidence, and exploratory search. That distinction is part of the result.

## 5. Audited extensions outside the paper

Two additional developments are preserved but not claimed as paper
contributions:

- `artifacts/efx_chambers/` proves that all six displayed matrices lie in
  full-dimensional positive-valuation regions with the same exact EFX\(_0\)
  allocation sets and supplies rational radius certificates.
- `artifacts/multifloater_parking/` gives an exact criterion for injectively
  parking multiple leftover goods, a safe-matching sufficient theorem, and an
  exhaustive small-instance regression.

`repro/countcegar_real/` is a well-archived checkpoint for the unrestricted
positive-real search. It is not an UNSAT result, counterexample, or theorem.

## 6. Internally verified positive additive EFX at \((4,8)\)

A new proof program, not yet incorporated into the counting paper, establishes
the following hybrid theorem:

> Every strictly positive additive valuation instance with four agents and
> eight goods admits a complete EFX allocation.

Lean checks the structural reduction from a hypothetical counterexample to
eight exact terminal ranking cells, including normalization, generic strict
perturbation, favorite-pattern coverage, residual reductions, stabilizer
symmetries, all 1,701 nonempty bundle partitions, and the perfect-matching
obstruction equivalence. The final composed theorem has no `sorryAx` or
native-computation axiom dependency.

For every terminal cell, an independently generated QF_LRA formula has a cvc5
CPC proof accepted as `correct` by the separate Ethos checker. The eight
proofs total 1,668,457,899 bytes and 13,812,082 proof steps. A separate parser
audit binds every formula assertion to the exact Lean terminal semantics, and
an executable literature audit pins the two published smaller-case inputs.

The authoritative entry point is
[`results/EFX48_PROOF_GUIDE.md`](results/EFX48_PROOF_GUIDE.md). Current
limitations are explicit: the 73-entry end-to-end release manifest passes
locally, and the frozen source archive builds and passes its audits in a new
temporary project directory on the original host. A second-machine or
cross-platform replay has not yet been performed. The two published proofs
are trusted inputs rather than re-formalized proofs, and no external
fair-division or formal-certification expert has yet signed off. The proper
present label is therefore **internally verified hybrid theorem**, not
peer-reviewed theorem.

## 7. Universal owner-threshold failure at \((4,9)\)

The later existence campaign now proves a cap-free conditional theorem:

> Four positive-additive agents and nine goods admit complete EFX whenever
> they have a strict common favorite and every possible favorite-singleton
> owner fails the exact residual owner-threshold test.

The proof chooses one residual bottom pair per agent. A pair shared by at
least three agents is handled by a separate conversion theorem; otherwise an
exhaustive multigraph census leaves exactly 20 canonical patterns. All 20
are closed by favorite-triple Hall cells or favorite-pair conversion
families. The eleven all-distinct cases pass two Z3 encodings, fresh-process
Z3 replay, pinned cvc5, and CPC/Ethos. The full class aggregate covers
723,786,758 checked proof bytes and 8,552,082 proof steps.

The authoritative entry point is
[`results/COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_THEOREM.md`](results/COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_THEOREM.md).
This is a genuine new \((4,9)\) subclass theorem, not the full \((4,9)\)
cell and not a resolution of general additive EFX. The next common-favorite
gate is threshold-passing but resident-Hall-deficient.

## Bottom-line assessment

The existing counting paper remains a focused package of six exact witnesses,
one parking theorem, and one carefully bounded computer-assisted result. That
package is substantial PhD-thesis work.

The separate \((4,8)\) existence proof is a larger professor/frontier-level
development in both mathematics and certification engineering. If external
review confirms its proof and novelty, its significance is breakthrough-level
for the additive EFX parameter frontier. The immediate work is to freeze and
replay the end-to-end package on an independent machine, complete the
small-core Hall analysis, and obtain adversarial expert review.

The \((4,9)\) universal-threshold theorem is a substantial follow-on result:
broader in value range but narrower in instance class than the \((4,8)\)
theorem. It materially advances the common-favorite program while leaving
the famous general conjecture open.

The remaining mixed threshold/Hall branch has also been made exact. Two
positive cap-20 profiles prove that threshold passage alone does not force a
favorite-singleton allocation: they have 114 and 273 threshold-passing
owner--partition pairs, no Hall-valid favorite-singleton partition, and
only balanced EFX support. A third profile blocks the six obvious
one-transfer repairs. These are rigorous no-go results that focus the next
lemma on a rank-maximal, owner-changing alternating exchange; they are not
additional existence theorems.

The rank-selection precursor is now exactly refuted. After symmetry-reduced
cap-20 CEGAR grew the rank-two and zero-neighbor motif pools to 119 and 69, a
smaller cap-4 search found a two-type profile with exactly three threshold
passes, all of rank one, and no favorite-singleton EFX partition. Independent
enumeration finds 195 balanced supporting partitions and 3,690 complete
allocations. This retires both unconditional selectors without threatening
EFX existence; the exact repair restricts to four pairwise nonproportional
valuation rows, since all smaller type counts are already known safe.
The first two repaired cap-4 sessions find 12 exact four-type trace profiles
and grow the cumulative rank-two obstruction pool from 29 to 77 motifs.
Independent replay checks every row-type condition, seed and proto hash,
motif census, and learned-count transition. A third session then exactly
refutes the repaired selector: four pairwise bundle-order-inequivalent rows,
exactly three threshold passes all of rank one, no favorite-singleton EFX
partition, 599 balanced supporting partitions, and 3,878 complete
allocations. Thus rank maximization cannot remove the rank-one branch even
in the genuinely open four-preference-type stratum.

A separate cap-free formulation now interpolates one valuation row away from
a safe three-type boundary. Each fixed allocation is feasible on an exact
rational interval, so a first failure has a tight-breakpoint certificate. A
proved resident-extension lemma sharpens this to a fixed bundle partition:
only the moving agent's at most four extendable-bundle intervals matter, and
the merged endpoint supplies at least two of them. An ordinal-chamber
corollary closes every instance with at most three bundle-order types, a
strictly larger safe class than identical cardinal rows. Across four tight
count-four witnesses and the two mixed-Hall boundaries, all 72 ordered row
paths have a stable partition; 63 need one assignment and nine need two
assignments of the same bundles. This is a new proof target with exact finite
evidence, not yet a theorem.
The remaining chamber crossing has a proved essential-edge reduction: if the
single changing feasibility edge is avoidable by a perfect matching, no
bundle pivot is needed. Otherwise a minimal Hall witness has size 1, 2, 3,
or 4 and is deficient by exactly one. An exhaustive audit checks all 4,929
labeled essential-edge graphs and 213 symmetry orbits. Additive
maximum-bundle feasibility rules out witness size 1 at a genuine single-wall
crossing, leaving only sizes 2, 3, and 4.
Exact generic-wall constructions now settle the first proposed pivot menu.
All three Hall sizes can defeat every one-good transfer. Sizes 2 and 3 can
defeat all 127 partitions within transfer radius two, with their nearest EFX
support at distance three; the post-wall profiles still have 16 and 40
complete allocations. The size-4 profile has 57 allocations at minimum
distance two. Conversely, the size-4 radius-two obstruction is dual-solver
UNSAT in the fixed seven-good (2+2+2+1) shape. This gives a verified local
no-go and one bounded positive boundary, redirecting the cap-free proof
toward longer Hall exchange chains or a global potential.

Inside the previously opaque rank-one Hall case, a new analytic normal form
shows that all residents must accept only one common bundle and satisfy one
strict density inequality. This yields an exact owner-switch reduction.
The associated audits also prevent overclaiming: all six one-good transfers,
the 21-state contested-partner family, and the 30-state bridge successor are
false even with the global no-singleton hypothesis. The final cap-6
refutation has three identical resident rows, blocks all 966 singleton
partitions and all 30 proposed repairs, yet retains 264 supporting partitions
and 2,790 complete EFX allocations. Every failed singleton is explained by
one of two elementary Hall obstructions. Its 15 nearest repairs identify two
more origin orbits, producing a 45-state successor. The first exact campaign
blocks all 45 states and reaches a six-singleton Hamming-two local minimum;
the global floor remains open. The identical-resident cap-6 subcell containing
all current extremal profiles now closes under both matching-clause and
Hall-selector encodings with a shared 392-partition pool. This is a bounded
theorem candidate, not the unequal-resident rank-one theorem. A second
dual-encoded result weakens full identity to any repeated resident row
through cap 5: the two symmetry-reduced equality cases close independently under
12-matching and seven-case Hall quotient encodings. The Hall reduction was
also exhaustively checked on all 4,096 possible neighborhood graphs. Cap 6
remains the first unresolved rung for this wider repeated-row stratum.
This is a bounded statement about the particular local repair family, not a
new EFX-existence class: four agents with any repeated valuation row have at
most three valuation types and are already covered by the known three-types
existence theorem (Ghosal et al., EC 2025).

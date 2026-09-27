# Accomplishments and claim status

For the later goods campaign, superseded claims, chores work and current review
depth, use the [27 September 2026 consolidated audit](docs/EFX_PROGRAM_AUDIT_2026-09-27.md).
This file records the narrower counting publication; it is not a general EFX proof.

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

The rank-selection precursor is now independently frozen as an open gate.
All three exact mixed profiles have a rank-two threshold pass with a
zero-neighbor bundle. Two bounded cap-20 CEGAR searches produced neither a
counterexample nor a certificate, sharply separating this plausible lemma
from the already proved results.

Inside the previously opaque rank-one Hall case, a new analytic normal form
shows that all residents must accept only one common bundle and satisfy one
strict density inequality. This yields an exact owner-switch reduction.
The associated audit also prevents overclaiming: a natural three-conversion
rule is false even with the global no-singleton hypothesis. The exact
boundary blocks all six one-good transfers, retains 366 balanced repairs and
1,259 allocations, and raises the smallest surviving exchange radius to two.
The 63 radius-two states are now reduced to nine origin signatures and a
21-state contested-partner proof target, frozen at a 302-cut open boundary.

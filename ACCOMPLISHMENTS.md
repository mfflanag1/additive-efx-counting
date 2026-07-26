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

## Bottom-line assessment

The viable paper is narrower than the original campaign, but stronger in
credibility: six exact witnesses, one structural theorem, and one carefully
bounded computer-assisted result. That is a defensible focused research paper
and a substantial PhD-thesis chapter. The next research step is an independent
proof-producing master or a genuine structural reduction beyond the finite
box.

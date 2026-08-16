# Independent Review 2: Formal and Computational Certification

**Date:** 2026-07-30 EDT  
**Reviewer:** independent subagent, formal/computational track  
**Repository access:** read-only  
**Verdict:** **conditional acceptance; no concrete formula or certificate
mismatch found**

This review was conducted independently of the fair-division review. Its
central question was whether an incorrect theorem, stale formula, or unrelated
proof object could pass the current pipeline.

## Checks performed

- Built the pinned Lean 4.32.1/mathlib project: passed.
- Ran `AxiomAudit.lean`: only `propext`, `Classical.choice`, and `Quot.sound`.
- Searched Lean sources for `sorry`, `admit`, local `axiom`, `opaque`,
  `unsafe`, `extern`, `implemented_by`, and related gaps.
- Inspected final theorem composition, perturbation, residual predicates,
  terminal definitions, stabilizers, and partition matching.
- Manually compared every SMT semantic category with the Lean definitions.
- Reran the parser-based semantic audit over eight formulas and all 1,701
  partitions: passed.
- Inspected both universes: 1,701 unlabeled partitions and 40,824 labeled
  onto allocations.
- Verified all 73 final manifest hashes.
- Confirmed all 66 archived source members match the current repository.
- Confirmed nine dependency repositories are at the revisions in
  `lake-manifest.json` with clean Git status.
- Reran Ethos on `top4-second211`: `correct`.
- Independently expanded the term DAG in every CPC proof and compared every
  proof assumption with every SMT assertion.

The new all-eight comparison produced:

| Cell | SMT assertions | CPC assumptions | Mismatches |
|---|---:|---:|---:|
| `favorite-211` | 68,150 | 68,150 | 0 |
| `favorite-31` | 68,157 | 68,157 | 0 |
| `favorite-22` | 68,157 | 68,157 | 0 |
| `top4-second1111` | 68,176 | 68,176 | 0 |
| `top4-second4` | 68,182 | 68,182 | 0 |
| `top4-second31` | 68,180 | 68,180 | 0 |
| `top4-second22` | 68,180 | 68,180 | 0 |
| `top4-second211` | 68,178 | 68,178 | 0 |

In total, **545,360 proof assumptions matched 545,360 formula assertions
with zero mismatches**. This materially strengthens the current certificate
evidence.

## Findings

### High: the complete theorem is not closed inside Lean

The exported theorem takes `EightTerminalCellsUnsat` as an argument:

- [`PublishedLifting.lean`](../formal/efx48/EFX48/PublishedLifting.lean);
- [`TerminalCells.lean`](../formal/efx48/EFX48/TerminalCells.lean).

The axiom audit therefore establishes that the conditional structural theorem
is kernel-clean. The terminal CPC results become part of the complete theorem
through an external semantic bridge and Ethos, not through a Lean theorem.

This is a legitimate hybrid proof, but public descriptions must not imply
that the whole result is kernel-closed.

### High release blocker: CPC proof includes are not relocatable

[`run_cvc5_cpc_proof.py`](../tracks/parkability/run_cvc5_cpc_proof.py)
writes absolute CPC signature paths. The frozen CPC files include paths under
the original `/Users/maxf/.../certification-20260729` directory.

Moving the package to another user, directory, or machine will make Ethos
fail unless the original path is recreated or the proofs undergo an audited
relocation transformation. This does not weaken the current same-host
verdict, but it blocks straightforward independent-machine reproduction.

### Medium: the Lean semantic binding is narrower than its name suggests

[`audit_independent_formula_semantics.py`](../tracks/parkability/audit_independent_formula_semantics.py)
thoroughly parses the SMT formulas and validates a hand-written Python
specification. Its direct Lean inspection checks canonical constants but does
not mechanically prove equivalence to Lean's residual predicates,
stabilizers, feasible-edge definition, or matching obstruction.

The reviewer manually checked those correspondences and found no mismatch.
The finding concerns assurance architecture, not a discovered formula error.

### Medium: formula-to-CPC binding was not automated

The current finalizers validate formula hashes, proof hashes, recorded return
codes, and Ethos verdicts. They do not compare the assumptions used by a CPC
proof with the assertions in its target SMT formula.

In principle, fabricated metadata could pair an unrelated valid proof with a
formula. The reviewer's new all-eight comparison rules that attack out for
the current artifacts, but the check should become permanent and
manifest-bound.

### Medium: same-host replay reuses tool and dependency state

[`replay_efx48_clean_source.py`](../tracks/parkability/replay_efx48_clean_source.py)
symlinks the original dependency checkout and uses binaries under the
original certification root. The manifest hashes cvc5 and Ethos but not the
Lean executable or complete dependency trees, and the replay reuses compiled
dependency caches.

The reviewer independently checked that current dependency repositories are
clean and at pinned revisions. The replay record accurately limits its claim
to the same host.

### Low: published-input variant judgments are declarations

[`audit_published_inputs.py`](../tracks/parkability/audit_published_inputs.py)
checks paper hashes and theorem fragments, but its variant judgments are
hard-coded booleans. They are documented human judgments, not formal
verification of the papers.

### Low: direct-allocation checks are corroborative

Six direct formulas rely on Z3 `UNSAT_CANDIDATE` records without proof
objects. The main CPC proof chain does not depend on these records, so this is
not a correctness issue; the direct encoding should continue to be presented
as an independent cross-check.

### No issue: `native_decide`

Although `RestrictedGrowth.lean` uses `native_decide`, the final theorem's
dependency audit contains neither `native_decide` nor `ofReduceBool`.

## Strongest attempted falsification

The reviewer attempted to pair the current formulas with stale or unrelated
CPC proofs. The published pipeline did not directly test the relation between
formula assertions and proof assumptions.

The independent term-DAG expansion and all-eight exact comparison found zero
mismatches. The stale-proof attack is therefore ruled out for the current
frozen artifacts.

The reviewer also sought sign reversals, missing target bundles, omitted
removal cases, incomplete matching enumeration, missing partitions, and
labeled/unlabeled coverage errors. None was found.

## Trusted or unchecked components

- Lean kernel and the official Lean distribution.
- Mathlib and pinned dependencies.
- Ethos and the CPC signatures.
- The two published paper proofs.
- Human correspondence between the Python semantic specification and Lean.
- No full source audit or rebuild of Ethos/cvc5.
- One direct Ethos rerun in this review; the prior frozen record covers all
  eight.
- No independent-machine or cross-platform replay.
- No independent rerun of the six large Z3 corroborative solves.

## Reproducibility assessment

- Integrity on the present host: **strong**.
- Fresh project-source build on the present host: **passed**.
- Independent machine with the current package: **blocked by path and
  provisioning issues**.
- Cross-platform reproduction: **absent**.

## Mandatory next actions

1. Add a permanent `audit_cpc_formula_assumptions.py` implementing the
   all-eight exact comparison and bind its source and output into the final
   manifest.
2. Replace absolute CPC signature includes with relocatable paths, or provide
   a narrowly audited relocation transformation.
3. Produce a standalone artifact with formulas, proofs, signatures, tools or
   acquisition hashes, Lean sources, and replay code.
4. Hash or independently acquire Lean; verify every dependency revision and
   clean status inside the replay; avoid shared compiled caches in the
   independent run.
5. Strengthen the Lean-to-SMT bridge with generated Lean reflection or a
   checker that parses the relevant Lean definitions.
6. Reproduce the package on another machine and preserve its transcript.
7. State prominently that the complete theorem is hybrid and the Lean theorem
   is conditional on terminal UNSAT.

## Confidence

- Eight formula UNSAT claims, conditional on Ethos correctness: **about
  0.97**.
- SMT formulas matching the intended Lean predicates: **about 0.90**.
- Overall hybrid theorem, conditional on the published inputs: **about
  0.88--0.92**.
- Independent-release reproducibility as packaged: **about 0.50**.


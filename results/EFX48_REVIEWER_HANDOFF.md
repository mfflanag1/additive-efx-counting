# External Reviewer Handoff: Nonnegative Additive EFX at 4x8

**Review target:** Every nonnegative additive instance with four agents
and eight indivisible goods admits a complete EFX allocation.

**Current status:** internally verified hybrid proof package. This document
requests adversarial review; it does not represent reviewer approval.

## What a reviewer is being asked to decide

Please return one of:

1. **No material issue found**, with the layers actually checked listed;
2. **Conditional acceptance**, with unchecked dependencies stated;
3. **Material issue**, with a minimal counterexample, failing command, or
   precise proof step; or
4. **Unable to assess**, with the blocking artifact or expertise identified.

Silence or a successful build alone is not mathematical sign-off.

## Five-minute orientation

There are four people and eight goods. Each person assigns a nonnegative value
to each good, and values bundles by summing. An allocation is EFX when, after
removing any one good from someone else's bundle, no observer prefers what
remains to their own bundle.

The proof assumes a counterexample, first perturbs it to strictly positive
weights, then normalizes and generically perturbs it,
uses published smaller-case theorems to remove two residual regions, and
reduces the remaining rankings to eight canonical cells. For each of the
1,701 unlabeled nonempty partitions, a 4x4 feasibility graph records which
agent could own which bundle while satisfying EFX. A partition works exactly
when this graph has a perfect matching. The eight resulting rational
linear-arithmetic systems are all inconsistent.

Lean checks the mathematical reduction. A separate parser checks that the
exact SMT assertions have the Lean-specified semantics. cvc5 produces a CPC
proof for each terminal formula, and Ethos accepts all eight proofs.

## Recommended review tracks

### Fair-division mathematics

Start with:

- [submission manuscript](../output/pdf/efx48-submission.pdf);
- [proof guide](EFX48_PROOF_GUIDE.md);
- [Lean definitions](../formal/efx48/EFX48/Definitions.lean);
- [nonnegative closure](../formal/efx48/EFX48/Perturbation.lean);
- [strict perturbation](../formal/efx48/EFX48/StrictPerturbation.lean);
- [residual cuts](../formal/efx48/EFX48/UniversalMinimum.lean) and
  [corrected peelable reduction](../formal/efx48/EFX48/Peelable.lean);
- [canonical coverage](../formal/efx48/EFX48/CanonicalCoverage.lean); and
- [terminal reduction](../formal/efx48/EFX48/TerminalCells.lean).

Highest-value questions:

1. Does the uniform perturbation correctly reduce nonnegative weights to
   positive weights?
2. Does the generic perturbation preserve no-EFX while obtaining all strict ranking
   and row-distinctness conditions?
3. Do the two smaller published theorem variants exactly supply the deleted
   instances used by Lean?
4. Are the stabilizers restricted to genuine symmetries of each fixed cell?
5. Does the corrected deleted-agent observer scope retain every comparison
   required for reinsertion?

### Formal and computational certification

Start with:

- [final theorem](../formal/efx48/EFX48/PublishedLifting.lean);
- [axiom audit](../formal/efx48/AxiomAudit.lean);
- [semantic-binding audit](../tracks/parkability/audit_independent_formula_semantics.py);
- [end-to-end finalizer](../tracks/parkability/finalize_efx48_end_to_end.py);
- [clean-source replay](../tracks/parkability/replay_efx48_clean_source.py);
- [full expert checklist](EXPERT_REVIEW_CHECKLIST.md).

Highest-value questions:

1. Is the parser audit semantically independent enough to catch an encoder
   error rather than merely reproducing counts?
2. Can every load-bearing formula and proof hash be followed from the final
   certificate?
3. Does any Lean theorem depend on `sorryAx`, native computation, or an
   unimported local module?
4. Does Ethos interpret the CPC proof under the intended signatures?

## Current hardened release candidate (2026-08-01)

The coherent current snapshot is

```text
game-theory/experimental-runs/additive-efx-counting-runs/
parkability/certification-20260801-v2
```

It contains a 124-entry end-to-end manifest, a 96-entry terminal-certificate
manifest, and a 72-file deterministic source archive. The terminal manifest
now binds the exact 545,360-assertion/545,360-assumption audit, the official
cvc5 1.3.3 source archive, and all 51 transitive CPC signature files. The
current Lean snapshot includes and builds the final nonnegative theorem.

The full eight-cell moved-root Ethos replay has passed with every proof-body
byte preserved; a clean Linux/ARM container replay has also passed on the same
physical Mac.  Physically independent-host and independent-person replays
remain release gates. See
[`EFX48_RELEASE_HARDENING_20260801.md`](EFX48_RELEASE_HARDENING_20260801.md).

Snapshot boundary: v2 remains internally coherent, but the working
`paper/efx48/submission.tex` and generated PDF were updated after v2 to report
the completed all-eight moved-root replay.  They are not manifest-bound v2
artifacts.  Cut and verify a new coherent snapshot before distributing the
updated manuscript as the certified release package.

## Historical frozen package

Certification root:

```text
game-theory/experimental-runs/additive-efx-counting-runs/
parkability/certification-20260729
```

Primary files:

- `EFX48_END_TO_END_CERTIFICATE.json`;
- `EFX48_END_TO_END_MANIFEST.sha256`;
- `EIGHT_CELL_CPC_CERTIFICATES.json`;
- `EIGHT_CELL_CPC_MANIFEST.sha256`;
- `independent-generator-audit/semantic-binding.json`;
- `literature/PUBLISHED_INPUT_AUDIT.json`;
- `direct-allocation-crosscheck/DIRECT_ALLOCATION_CROSSCHECK.json`; and
- `EFX48_CLEAN_SOURCE_REPLAY.json`; and
- `EFX48_CLEAN_SOURCE_FULL_ETHOS_REPLAY.json`.

This historical end-to-end manifest contains 73 entries and the source archive
contains 66 files. The eight CPC proofs total 1,668,457,899 bytes and
13,812,082 proof-step lines.

## Reproduction commands

From the certification root:

```sh
shasum -a 256 -c EFX48_END_TO_END_MANIFEST.sha256
```

From the source repository:

```sh
python3.10 tracks/parkability/finalize_efx48_end_to_end.py \
  --root /absolute/path/to/certification-20260729 \
  --project-root .
```

Fresh extraction and project-build replay on macOS:

```sh
python3.10 tracks/parkability/replay_efx48_clean_source.py \
  --root /absolute/path/to/certification-20260729 \
  --shared-packages /absolute/path/to/formal/efx48/.lake/packages \
  --output /absolute/path/to/EFX48_CLEAN_SOURCE_REPLAY.json \
  --recheck-ethos
```

The full clean-source/Ethos record reports 8/8 proofs as `correct`. It reuses
the pinned dependency checkout by path on the original macOS host. A genuinely
independent reproduction should repeat the build and Ethos checks on another
macOS ARM machine, or rebuild and pin Linux versions of the toolchain and
checker in a container.

## Known limitations, not review surprises

- Mahara's and Chaudhury--Garg--Mehlhorn's paper proofs are trusted published
  inputs, not re-formalized in Lean.
- The Lean-to-SMT connection is checked by an independent parser, not a
  kernel-reflected translation.
- Lean, mathlib, cvc5 proof emission, and Ethos remain trusted software
  components at their stated boundaries.
- The novelty search is current through July 30, 2026 but has not been
  confirmed by active EFX researchers.
- The 130-partition core is deletion minimal, not proved minimum cardinality.

## Suggested response template

```text
Reviewer:
Expertise:
Date:
Commit/source archive hash:
Certificate manifest hash:

Layers checked:
[ ] fair-division reduction
[ ] published theorem variants
[ ] Lean build and axiom boundary
[ ] Lean-to-SMT semantic audit
[ ] CPC/Ethos proof checking
[ ] direct-allocation cross-encoding
[ ] novelty position

Material issues:
Unchecked dependencies:
Verdict:
```

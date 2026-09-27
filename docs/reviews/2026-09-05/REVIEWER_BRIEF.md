# Specialist review brief: additive EFX counting

5 September 2026. Request: assess correctness, novelty and publishability; this is not a claim of external acceptance.

Read `paper/main.pdf` first. The source is an editorially revised copy of `additive-efx-counting` commit `76c1c781fec61a48d114ac4dd4e74d00fb55965a`. `SOURCE_INVENTORY.json` records the original blobs; `EDITORIAL_DIFF.patch` shows every manuscript change; `REVIEW_MANIFEST.json` binds the distributed review files. Historical supplement documentation describes the original release, not this derivative package.

## Exact contribution to review

| Claim | Scope | Not claimed |
|---|---|---|
| Six explicit count-n examples | Positive additive valuations; complete labeled EFX allocations; cells (4,7), (5,8), (6,9), (4,8), (4,9), (4,10); counts 4,5,6,4,4,4 | No infinite family, universal lower bound, or global tightness |
| Generalized parking criterion | A necessary and sufficient observer-host inequality for adding the single leftover good to a selected host in an EFX0 base | No universal successful host; the criterion is direct EFX algebra |
| Bounded counting result | Every 4-by-7 integer valuation matrix in {1,2,3,4} has at least four complete labeled EFX allocations | No unbounded-value theorem or formalized mathematical encoding |

All computational valuations are strictly positive, so the zero-tolerant EFX0 and positive-good-only conventions coincide. The parking criterion allows nonnegative valuations and explicitly uses EFX0. Agent and item identities are not silently quotiented out when reporting the six counts.

The displayed (4,7) witness is outside the bounded box. Its upper bound and the finite-box lower bound therefore do not prove unrestricted equality. The conjecture is stated for at least one good, excluding the trivial empty-good degeneracy.

## Requested referee decisions

1. Does the six-cell upper-bound improvement add something publishable to Neoh and Teh's counting program? Is a matching construction already known? Please distinguish conjectural additive tightness from the actual finite examples.
2. Audit the protected-slot encoding end to end: distinct allocation identifiers, reuse/duplicates in the terminal pool, integer thresholds, exact EFX negation, symmetry restrictions, and the implication from a terminal UNSAT pool to the full finite valuation box.
3. Is the reconstructed 1,240-allocation terminal pool a valid replacement for the missing historical checkpoint? The claim rests on the new terminal master and proof, not on an assertion that the old trajectory was recovered.
4. Does the CNF construction encode the same mathematical property as the CP-SAT construction? A DRAT proof certifies the supplied CNF, not this translation.
5. Check the parking equivalence at empty bundles, zero values and zero-valued removed goods. Please assess it as supporting exposition, not as the main novelty claim.
6. Recommend acceptance, revision or withdrawal for each claim separately, with any load-bearing gap stated explicitly.

## Evidence and remaining trust boundary

The six instances are enumerated by three implementations, including two independently written exact counters. The seven archived parking certificates have an exact checker. The finite-box theorem has CP-SAT and independent CNF encodings and an archived compressed binary DRAT proof. These are internal computational audits; no independent human referee acceptance is claimed, and no Lean theorem formalizes this counting result.

Fresh September 5 commands and results are in `review-checks/` and summarized in `VERIFICATION_STATUS.md`. That record distinguishes full logical proof replay from hash verification. Reviewer effort should concentrate on mathematical encoding and exhaustive coverage, not merely another solver verdict.

## Literature boundary

- [Neoh and Teh, Understanding EFX Allocations: Counting and Variants, AAAI 2025](https://ojs.aaai.org/index.php/AAAI/article/view/33536): the minimum-count baseline and Conjecture 6.1.
- [Akrami et al., arXiv:2604.18216](https://arxiv.org/abs/2604.18216): counterexamples for submodular valuations; the unrestricted monotone counting conjecture does not survive, but that does not refute its additive restriction.
- [Alkassar, Fouz and Mehlhorn, arXiv:2608.08590](https://arxiv.org/abs/2608.08590): four-agent complete EFX0 existence through nine goods. This review copy removes the outdated claim that (4,8) is the current existence frontier. Existence and counting are distinct.

The September 5 targeted check found no matching publication for the six-cell package. This is provisional novelty evidence, not an exhaustive priority determination.

## Reading and reproduction

Start with the abstract, Sections 2-4 and the finite-box soundness argument, then the encoding and reconstruction notes in `repro/countcegar_k4/README.md`. See `REPRODUCE.md` for commands. Large historical exploratory solver files are outside this selected artifact. No research process needs to be resumed to review the paper.

Author names and affiliations are intentionally omitted from the PDF pending the author's publication choices. AI assistance is disclosed; do not infer anonymous human authorship or external review from the phrase "independent verifier."

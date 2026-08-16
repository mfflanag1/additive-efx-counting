# Synthesis of Two Independent Reviews

**Date:** 2026-07-30 EDT  
**Method:** two parallel, read-only subagent reviews with separate scopes and
no inter-reviewer communication  
**Overall verdict:** **conditional acceptance; no material proof error found**

## Independent verdicts

| Review | Verdict | Principal condition |
|---|---|---|
| [Fair-division mathematics](INDEPENDENT_REVIEW_FAIR_DIVISION_20260730.md) | Conditional acceptance | Terminal UNSAT and the hand-audited semantic bridge |
| [Formal/computational certification](INDEPENDENT_REVIEW_FORMAL_CERTIFICATION_20260730.md) | Conditional acceptance | External Lean-to-SMT/CPC bridge and release reproducibility |

Both reviewers independently selected the Lean-to-SMT boundary as the
highest-risk layer. Neither found a concrete mismatch there after manual
comparison.

## Agreements

The reviewers agree that:

1. no reversed inequality, missing EFX comparison, invalid stabilizer,
   residual-reinsertion error, or uncovered ranking cell was found;
2. the final Lean theorem is a kernel-clean **conditional reduction**, not a
   kernel proof of the CPC terminal results;
3. the Python semantic audit is strong but does not mechanically derive its
   full specification from Lean;
4. the published paper proofs remain external trusted inputs;
5. same-host integrity is strong, while independent-machine reproduction has
   not passed; and
6. the present evidence supports a serious hybrid theorem, not an
   unconditional formal-verification claim.

## New evidence contributed by the reviews

The formal/computational reviewer expanded all eight CPC term DAGs and
compared every proof assumption with every SMT assertion:

> **545,360 assertions, 545,360 proof assumptions, zero mismatches.**

This closes the most plausible stale-or-unrelated-proof attack for the
current artifacts. The check is not yet part of the permanent pipeline.

## Issues requiring correction

### Release blockers

1. **CPC files contain absolute signature paths.** The frozen package is not
   relocatable without recreating the original path or transforming the
   includes.
2. **No permanent formula-to-CPC assumption audit.** The reviewer's new exact
   check must become executable, source-controlled, and manifest-bound.
3. **No independent-machine reproduction.** The same-host replay reuses
   binaries, dependency checkout, and compiled caches.

### Assurance improvements

4. Strengthen the Lean-to-SMT bridge so that correspondence with residual
   predicates, stabilizers, feasible edges, and matching obstruction is
   mechanically checked rather than only manually reviewed.
5. Print the complete conditional Lean signature and hybrid trust boundary
   prominently.
6. Verify Lean and dependency identities as part of replay.

### Minor corrections

7. Change the manuscript's stale source-archive count from 60 to 66.
8. Add an explicit finite-type transport wrapper for the three-agent
   published input.
9. Continue to label the direct-allocation encoding as corroboration rather
   than certified proof.

## Updated assessment

The reviews increase confidence in the current frozen proof artifacts because
they independently failed to find a mathematical mismatch and added an exact
all-eight formula/proof comparison.

They simultaneously lower the release-readiness assessment: the absolute CPC
paths mean that the package, as currently frozen, is not yet independently
relocatable despite its strong same-host replay.

The responsible present label is:

> **Independently reviewed by two internal adversarial agents with conditional
> acceptance and no material proof error found; strong same-host hybrid proof;
> external human review and independently relocatable reproduction still
> required.**

These are independent internal reviews, not external peer review.

## Ordered next actions

1. Make CPC proofs relocatable.
2. Productize and manifest-bind the all-eight CPC-assumption audit.
3. Correct the manuscript and print the conditional Lean signature.
4. Strengthen or more precisely describe the Lean-to-SMT bridge.
5. Build a standalone clean-room reproduction bundle.
6. Run it on another machine.
7. Obtain one active fair-division expert and one formal-certification expert
   as external human reviewers.


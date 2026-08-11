# Source-margin root-budget frontier lemma

**Date:** 2026-08-11

**Status:** cap-free canonical compensation selector for every captured-source
packet; the terminal pointwise blockade still requires packet splitting or a
third-owner connected fork

## Setting

Let `A` be a common-safe desired core for source `a`, with strict margin

\[
 \mu=v_a(A)-v_a(X_a)>0.
\]

Let `P` be the current root pool and suppose it has deficit

\[
 \Delta=v_r(X_r)-v_r(P)>0.
\]

A minimal dual-pool extraction supplies `C subseteq A` such that

\[
 v_r(C)\ge\Delta,
 \qquad v_a(C)\ge\mu.                              \tag{1}
\]

The second inequality is precisely the source-margin capture branch.  Put

\[
 \beta=v_r(C)-\Delta\ge0.                           \tag{2}
\]

This is the exact amount of root value that may be returned from `P` while
the root remains weakly paid.

## Canonical compensation frontier

Among all packets `B subseteq P` satisfying

\[
 v_r(B)\le\beta,                                    \tag{3}
\]

choose one maximizing `v_a(B)`.  The family is nonempty because it contains
the empty packet.  Define

\[
 P'=P-B+C,
 \qquad A'=A-C+B.                                   \tag{4}
\]

Exactly one of the following holds.

1. **Source restored.** If
   \[
   v_a(B)>v_a(C)-\mu,                               \tag{5}
   \]
   then `v_a(A')>v_a(X_a)`, while (2)--(3) give
   `v_r(P')>=v_r(X_r)`.  If `A'` is common-safe, the root-paid selector
   reapplies.  If it is unsafe, a minimal unsafe deletion supplies the
   existing response augmentation.
2. **Root-budget blockade.** If (5) fails, then
   \[
   v_a(C)-v_a(B)\ge\mu.                             \tag{6}
   \]
   Moreover every unused good `g in P-B` satisfies
   \[
   v_r(g)>\beta-v_r(B).                             \tag{7}
   \]

To prove (7), suppose instead that an unused `g` fits the remaining budget.
Then `B+g` satisfies (3) and, by positivity,
`v_a(B+g)>v_a(B)`, contradicting maximality of `B`.

Thus a captured-source packet cannot remain an unnamed two-row inequality.
It either has a best root-affordable compensation that restores its source,
or every unselected pool good is individually root-critical at the exact
remaining budget.

## Terminal forms

If `B=P`, equation (6) is the full-pool exhaustion certificate

\[
 v_a(C)-v_a(P)\ge\mu.                               \tag{8}
\]

If `B` is proper, equation (7) is stronger than aggregate underpayment: no
single unused good can be appended without making the root fall below base.
The next operation must therefore do at least one of the following:

1. split or replace part of `C`, changing the root budget itself;
2. transfer an unused pool good through a third owner who receives a
   compensating packet elsewhere; or
3. assemble the resulting packets into the surplus-budgeted connected fork.

Merely enlarging `B`, changing the missing-owner label, or maximizing another
raw cross-owner residual cannot cross the frontier.

## Scale and support compatibility

All comparisons in the root budget use row `r`; all compensation comparisons
use row `a`.  Independent positive scaling of either row preserves (1)--(8).
The exchange (4) conserves physical support and connects the old source core
to the root pool.  Hence any third-owner continuation automatically attaches
to the same connected transfer component.

## Verification and boundary

[`source_margin_root_budget_frontier_audit.json`](source_margin_root_budget_frontier_audit.json)
checks the two payment identities, the exact root budget, the source-restored
dichotomy, and the maximality implication (7) symbolically.

This lemma supplies the smallest deterministic operation missing after dual
minimal extraction: maximize same-source compensation under the exact root
return budget.  It does not contradict the pointwise blockade, select the
third-owner fork in every case, close unsafe/hitting-set recurrence, close
`GG`, or prove four-agent/general additive EFX.

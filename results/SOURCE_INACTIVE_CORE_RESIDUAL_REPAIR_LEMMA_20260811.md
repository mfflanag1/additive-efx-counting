# Source-inactive core/residual repair lemma

**Date:** 2026-08-11

**Status:** cap-free finite repair theorem; the unanimous core-dominance
exhaustion branch remains open

## Setting

Use a compressed state with missing owner `d`, residual `W`, and a
common-safe desired core `A` held by its source `j`.  Suppose `d` strongly
envies `A` but is source-inactive there:

\[
 v_d(W)<\tau_d(A)<v_d(A)<v_d(X_d).                    \tag{1}
\]

The first two inequalities imply in particular

\[
 v_d(A)>v_d(W).                                      \tag{2}
\]

For packets `H subseteq A` and `K subseteq W`, exchange `H` and `K`:

\[
 A(H,K)=(A\setminus H)+K,
 \qquad
 W(H,K)=(W\setminus K)+H.                            \tag{3}
\]

The two bundles still partition `A+W`.

## Adaptive repair chain

Maintain the source-payment condition

\[
 v_j(A(H,K))>v_j(X_j),                               \tag{J}
\]

the repaired missing-owner comparison

\[
 v_d(W(H,K))\ge \tau_d(A(H,K)),                      \tag{D}
\]

and the monotone-residual condition

\[
 v_d(H)\ge v_d(K).                                   \tag{M}
\]

Start with `H=K=empty`.  Condition (J) holds and (D) fails by (1).
Repeat:

1. If (D) or (M) fails, enlarge `H` by an inclusion-minimal packet from
   `A-H` restoring both conditions.
2. If (J) then fails, enlarge `K` by an inclusion-minimal packet from
   `W-K` restoring it.  If even `K=W` does not restore (J), stop at
   **J-exhaustion**.
3. If all three conditions hold, stop successfully.

Both selected packets grow monotonically.  Hence every branch terminates
after at most `|A|+|W|` strict additions.

## The d-repair can never exhaust

For fixed `K`, the choice `H=A` satisfies both (D) and (M).  Indeed,
`A(H,K)=K` and `W(H,K)=A+(W-K)`.  From (2) and `K subseteq W`,

\[
 v_d(A+W-K)>v_d(K)\ge\tau_d(K),                      \tag{4}
\]

while `v_d(A)>v_d(K)`.  Thus a finite inclusion-minimal `H`-repair always
exists.  J-exhaustion is the only terminal failure.

## Successful repair

At a successful leaf, `j` still strictly improves and `d` no longer envies
the repaired core.  Moreover `H` is nonempty.  Under the nondegenerate
normal form, (M) is strict because the disjoint packets `H,K` are distinct:

\[
 v_d(W(H,K))=v_d(W)+v_d(H)-v_d(K)>v_d(W).             \tag{5}

If `A(H,K)` is common-safe at the base, it is again a valid desired core
for `j`.  Replacing `A,W` by (3) strictly advances the missing-owner
residual potential.  No old core wall for `d` can be created by this move,
and the wall against `A` is removed.  New failures, if any, are residual
walls from represented sources and remain inside the response-compression
architecture.

If `A(H,K)` is not common-safe, take an inclusion-minimal desired subset of
an unsafe deletion.  Its most-envious source is a named response
augmentation.  Thus unsafe success does not disappear into an unnamed EFX
failure; it returns to the response/Hall branch.

## Exact exhaustion polarity

At J-exhaustion, even transferring the entire residual to `j` cannot pay
for the returned core packet:

\[
 v_j((A\setminus H)+W)\le v_j(X_j)<v_j(A).
\]

Subtracting gives the strict margin

\[
 v_j(H)-v_j(W)
 \ge v_j(A)-v_j(X_j)>0.                              \tag{6}

Hence

\[
 v_j(H)>v_j(W).                                      \tag{7}

Together with (2), the only survivor has a two-row unanimous orientation:
the missing owner ranks the full core above the residual, while the core
source ranks the payment-critical returned packet above the entire
residual.  The packet `H` and the exact source margin in (6) are retained
for the next root/hub operation.

## Composition consequence

Combine this lemma with aligned recapture and the base-response hole pivot.
Every two-sided compression star now has one of four outcomes:

1. an EFX flexible/lex endpoint;
2. an internal response/Hall augmentation;
3. a strict increase of the missing-owner residual potential; or
4. the explicit J-exhausted unanimous core-dominance state (6)--(7), or a
   priority-invalid root-facing pivot.

Thus arbitrary source-inactive core walls are no longer terminal.  The
remaining analytic target is to use the critical packet `H` in a root flip
or owner-rooted hub split, and to show that a revisit creates a
release-compatible PI cycle.

## Verification and claim boundary

[`source_inactive_core_residual_repair_audit.json`](source_inactive_core_residual_repair_audit.json)
checks the exchange partition, nonexhaustion of the d-repair, strict
residual-potential increase, preservation of old d-core safety, and the
J-exhaustion margin under Z3 5.0.0 and 4.15.3.

The lemma does not eliminate J-exhaustion, prove that every unsafe repaired
core closes its new Hall boundary, eliminate a root-facing pivot, close the
`GG` flower class, or prove four-agent additive EFX.

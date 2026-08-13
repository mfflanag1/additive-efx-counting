# Closing-source deletion-return residual-completion lemma

**Date:** 2026-08-11

**Status:** **referee correction (2026-08-12): payment reduction proved, but
termination refuted under the stated local premises.**  An unsafe candidate
may return an already recorded rank-one decorated response; PI or permanent
support progress does not follow without a rank-completing transition.

See
[`CLOSING_SOURCE_DELETION_RETURN_REFEREE_REPORT_20260812.md`](CLOSING_SOURCE_DELETION_RETURN_REFEREE_REPORT_20260812.md).

## Universal nonself pivot

Let

\[
 t=h_0\longrightarrow h_1\longrightarrow h_2
 \longrightarrow h_3\longrightarrow c             \tag{1}
\]

be any rank-four PI-free Hamiltonian owner-to-charity response path.  Let
`s=h_k`, with `k in {1,2,3}`, have an old decorated current-safe response

\[
 D\subseteq Y_t                                    \tag{2}
\]

into the owner hole.  The self case `s=t` is impossible: positivity prevents
a proper subset of t's current target from being strictly preferred by t to
the whole target.

For each source `i`, let `A_i` be its old assigned path core.  For every
nonhole target `i`, let `C_i` be its incoming path core and

\[
 R_i=Y_i\setminus C_i.                             \tag{3}
\]

All `A_i,C_i` are base-common-safe desired cores, and the old path matching
makes `A_{h_{j-1}}=C_{h_j}`.  The last assigned core lies in charity.

## Already closed nonowners

For every observer `h notin {t,s}`, the mixed-margin nonowner lemma gives
one of two outcomes.

1. `A_h+R_h` pays h's debt against `D`; an unsafe enlarged target gives a
   new decorated response/progress event.
2. Residual failure forces `C_h>A_h`, giving a self-response, PI, support
   growth, or augmentation.

Thus only target owner `t` and closing source `s` need be treated below.

## Delete one good and return the target

The exact target-owner separator is

\[
 v_t(A_t+R_t)<\tau_t(D),
 \qquad R_t=Y_t\setminus D.                        \tag{4}
\]

Choose a least-t good `g in D` and put `P=D-g`.  Then

\[
 v_t(P)=\tau_t(D)>v_t(A_t+R_t)>v_t(X_t).          \tag{5}
\]

Assign `P` to the hole owner instead of assigning `D` to `s`.  Deletion
monotonicity gives

\[
 \tau_h(P)\le\tau_h(D)\qquad(h\in N),             \tag{6}
\]

so every nonowner compensation already paying `D` also pays `P`.

## Reassign the former source

Keep `s` on its old path core `A_s` and give it the residual `R_s` released
by the incoming edge into target `s`.

### Source residual pays

If

\[
 v_s(A_s+R_s)\ge\tau_s(P),                         \tag{7}
\]

all four rows are paid.  The candidate bundles are physically disjoint:

- `P` lies in the unmatched hole target;
- every `A_i` lies in its distinct matched target; and
- every `R_i` excludes the incoming core selected from target `i`.

Every owner is strictly above the globally maximal base.  If the enlarged
targets are safe, this is a partial EFX Pareto—and hence lexicographic—
improvement.  If an enlarged target is unsafe, globally minimal current
extraction gives a decorated response.  The deleted good `g` occurs in no
allocated target, so this cannot be the same physical core `D`.  A new full
record is permanent response/support augmentation; an old exact record
invokes the already proved full-state reconstruction and hole-pivot cycle,
yielding PI or physical support progress.  Arbitrary leftover charity is
handled by the charity-packet blocker collapse when that invariant is
required.

### Source residual fails

Otherwise current safety of `D`, deletion monotonicity, and (3) imply

\[
 v_s(A_s)+v_s(R_s)
 <\tau_s(P)
 \le\tau_s(D)
 \le v_s(C_s)+v_s(R_s).
\]

Hence

\[
 v_s(C_s)>v_s(A_s)>v_s(X_s).                      \tag{8}
\]

The incoming core `C_s` is base-common-safe, so (8) is an exact self-response
by the former closing source into its own target.  A new label augments; an
old internally supplied self-edge is PI; and an outside supplier or changed
release strictly grows the physical support record.  Thus source residual
failure cannot remain a mixed-payment separator.

## Corrected theorem

For every nonself decorated response into the owner hole of a PI-free
rank-four Hamiltonian charity path, all underfunded rows yield at least one
of:

1. a partial EFX lexicographic improvement;
2. a release-compatible PI/self-response component;
3. strict physical support/component growth; or
4. a current-safe decorated response at the deletion-return candidate.

The fourth outcome is new augmentation only when its complete physical record
was not already present.  If it was present, the proof reaches the named
**rank-completing paid-response splice terminal**.  A single repeated response
does not supply the rank-four matching or strict finite state-order increase
needed for PI/support termination.

## Verification and claim boundary

[`closing_source_deletion_return_residual_completion_audit.json`](closing_source_deletion_return_residual_completion_audit.json)
exhausts all 24 Hamiltonian owner paths and all 72 nonself pivots, with 24
cycles of each length two, three, and four.  It verifies path-core/residual
support disjointness, target-owner payment, threshold monotonicity under
deletion, and the source self-response cancellation in exact arithmetic.

The audit re-proves the scalar and support implications but does not prove the
last termination sentence in the original version.  The exact rational
referee witness has a strictly improving non-EFX candidate, an already
recorded failed-target response, response-source rank one, and no forced PI
cycle or support change.  Therefore this theorem does not close mixed-margin
recurrence, GG, four-agent additive EFX, or general additive EFX.

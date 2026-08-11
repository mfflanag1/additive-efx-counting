# Retained-q Bq floater-substitution handoff lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of simultaneous root/q floater criticality
and root monopoly; q-source role collision and rank-two termination remain
open

## Canonical reservoir substitute

Let

\[
 A_r=T_q+f,
 \qquad
 D(U)=(T_r\setminus U)+f                           \tag{1}
\]

be the permanent root anchor and protected q core, with

\[
 v_q(D(U))>v_q(X_q).                               \tag{2}
\]

The live GG bottom polarity gives

\[
 v_q(B_q)\ge v_q(f),                               \tag{3}
\]

with strict inequality in the positive full-capture branch.  Replace the
floater in the protected q target by the complete bottom reservoir:

\[
 Z_q=(T_r\setminus U)+B_q.                         \tag{4}
\]

Equations (2)--(3) imply

\[
 v_q(Z_q)>v_q(X_q).                                \tag{5}
\]

Moreover

\[
 Z_q\cap A_r=\varnothing.                          \tag{6}
\]

As an edge into the q target, `A_r` releases all of `B_q`; hence (4) is not
an unsupported cross-bundle target.  Its substitute packet is internally
available on the anchored component.

## Minimal response extraction

Among every pair `(i,E)` with `E subseteq Z_q` and

\[
 v_i(E)>v_i(X_i),                                  \tag{7}
\]

choose globally inclusion-minimal support.  The family is nonempty by (5).
Global minimality makes `E` base-common-safe: deleting any good cannot be
desired by any owner.

If its source `i` is nonroot, `E` and `A_r` are disjoint common-safe desired
cores with distinct sources.  They restore the root-anchored rank-two
matching.  In particular, source `i=q` gives a physically disjoint
floater-free q core for the third-owner fork; source `i in {c,s}` gives the
existing external owner-growth/two-hole boundary.

## Root-source anchor return

Suppose the selected common-safe desired response inside `Z_q` has source
`r`, and write it as

\[
 E_r=K_T+K_B,
 \qquad
 K_T\subseteq T_r\setminus U,
 \quad K_B\subseteq B_q.                           \tag{8}
\]

Then

\[
 K_B\ne\varnothing.                                \tag{9}
\]

Indeed, a core contained in `T_r-U` is worth strictly less to the root than
`X_r=T_r+B_r`, by positivity.  More precisely, root desire in (7) gives

\[
 v_r(K_B)>
 v_r(T_r\setminus K_T)+v_r(B_r).                  \tag{10}
\]

Thus the root response captures a named packet from the reservoir that was
supposed to replace `f`.  This capture is nevertheless not terminal.  Put

\[
 O=Z_q\setminus E_r
\]

and perform the complete anchor return

\[
 Y_r=E_r,
 \qquad
 Y_q=A_r+O,
 \qquad
 Y_c=X_c,
 \qquad
 Y_s=X_s.                                          \tag{11}
\]

Every good of `A_r+Z_q` is conserved.  The root is strictly above base, and
the exact q gain is

\[
 v_q(Y_q)-v_q(X_q)
 =v_q(D(U))-v_q(E_r).                               \tag{12}
\]

If `v_q(E_r)<=v_q(D(U))`, both mutual owners are paid.  The root target is
common-safe and the external targets are unchanged, so the only possible
owner-target wall is against `Y_q`.  If it is safe, (11), followed by the
arbitrary-charity collapse for the unused packet, is an EFX lexicographic
improvement.  If it is unsafe, globally minimal extraction gives the named
current-response augmentation/progress continuation.

If instead

\[
 v_q(E_r)>v_q(D(U))>v_q(X_q),                      \tag{13}
\]

then the same physical common-safe core `E_r` is desired by `q`.  Select
`q -> E_r` beside `r -> A_r`; the sources and targets are distinct, so the
root-anchored rank-two matching is restored.  Hence a root-only response
relation inside `Z_q` is impossible as a terminal: anchor return pays q, or
the captured core itself makes q a nonroot response source.

## Consequence

The simultaneous criticality of `f` for `r` and `q` is never by itself a
terminal.  The released `B_q` reservoir replaces the floater in q's target
and gives exactly one of:

1. a floater-free q donor core;
2. an external nonroot response/rank-two boundary; or
3. a paid root-source anchor return or a q-sourced response on that same
   captured core.

For q-donor-role-available anchored pivots, only the ordinary fork outcomes
and the named rank-two continuation remain.  For q-source-collision pivots,
the physical floater conflict is likewise removed, but q still cannot
simultaneously serve as closing source and distinct donor; the two-core q
rerouting remains necessary.

## Verification and boundary

[`retained_q_bq_floater_substitution_handoff_audit.json`](retained_q_bq_floater_substitution_handoff_audit.json)
checks substituted q payment, support disjointness and internal `B_q`
release, forced nonempty bottom capture, the exact anchor-return payment
identity, and the paid-return/q-response dichotomy in exact linear
arithmetic.

This lemma does not discharge every rank-two source-inactive boundary,
resolve the q-source role collision, produce a globally maximal countermodel,
close GG, or prove four-agent/general additive EFX.

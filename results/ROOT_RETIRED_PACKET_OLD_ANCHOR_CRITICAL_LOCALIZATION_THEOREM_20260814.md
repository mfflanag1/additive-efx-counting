# Root retired packet old-anchor critical-localization theorem

**Date:** 2026-08-14

**Status:** cap-free, floor-preserving reduction of every root-held retired
packet to critical atoms of the permanent old root anchor

## Exact fixed-label input

Let `r` be the first-priority root, put `x=v_r(X_r)`, and let the exact
root-held `T_{L,times}^*` state have current root target `Z_r`.  The frozen
anchored interface retains a permanent old root core

\[
 A=D_r=T_q+f\subseteq Z_r,
 \qquad v_r(A)>x,                                \tag{1}
\]

which is common-safe and base-desired by `r`.  Let
`empty != K subseteq Z_r` be the named retired collision packet.  Every
retired atom `g` has a recorded nonroot retirement source `s(g)` and is
currently held by `r`.

The protected root floor in this branch is the globally maximal base value
`x`; the current root may have a larger transient value.  Every nonroot
source keeps her current target throughout the operation below.

## One-atom recorded return

Choose `g in K`.  Return `g` to its recorded retirement source and change no
other physical assignment:

\[
 Z'_r=Z_r-g,
 \qquad
 Z'_{s(g)}=Z_{s(g)}+g.                           \tag{2}
\]

All other owner bundles and charity are unchanged.  The current holder `r`
supplies `g`, the recipient is exactly its recorded retirement source, and
no inferred historical reversal is used.  Positivity gives

\[
 v_{s(g)}(Z'_{s(g)})>v_{s(g)}(Z_{s(g)}),          \tag{3}
\]

so every nonroot declared floor is preserved.

Two floor-valid root cases are available.

1. If `g notin A`, then `A subseteq Z'_r`, so (1) keeps the same physical
   root anchor strictly above `x`.
2. If `g in A` and `v_r(A-g)>x`, then `A-g` is common-safe by deletion
   monotonicity and remains strictly desired over `X_r`.  Record it as the
   new root anchor.  This is a controlled anchor release, not an unlabeled
   restoration.

In either case the candidate conserves goods, preserves all declared
floors, is supplier-closed, and has an exact physical response/anchor record.

## Packet progress and EFX audit

If (2) is EFX, the root remains strictly above the globally maximal base and
the result is a lexicographic contradiction.  Otherwise recompute every EFX
comparison and extract a globally minimum current response.  Independently
of where that response lies, the physical collision packet held by the root
has changed from `K` to `K-g`.  Thus the named packet coordinate strictly
shrinks before any exact fixed-label recurrence can occur.  A response that
mentions `g` belongs to the separately recorded returned-source label and
cannot restore the old root-held packet silently.

The argument does not waive the colliding recipient's floor, the retirement
source's floor, or an unrelated observer floor.  It therefore applies to
strict capture, equality-critical capture, source-inactive/base-floor debt,
and normalization-bypass entries alike.

## Exact recurrent survivor

Define the critical part of the old anchor by

\[
 C_r(A)=\{g\in A:v_r(A-g)\le x\}.                \tag{4}
\]

Every exact root-held recurrence in which all permitted outcomes fail must
satisfy

\[
 \varnothing\ne K\subseteq C_r(A)\subseteq A.   \tag{5}
\]

Under bundle nondegeneracy, `A-g` and `X_r` are distinct bundles, so (4)
is strict:

\[
 v_r(A-g)<x,
 \qquad
 v_r(g)>v_r(A)-x.                                \tag{6}
\]

Thus the root floor-admission gap is no longer a generic supplier-star
problem.  It is localized to a retired packet made entirely of critical
atoms of the already-minimal old root anchor.

## Claim boundary

This theorem closes every root-held collision containing an off-anchor or
noncritical anchor atom.  It does not pay for returning a critical atom,
prove that `C_r(A)` is empty, close the remaining critical-anchor packet,
close `T_{L,times}^*`, GG, four-agent EFX, or general additive EFX.

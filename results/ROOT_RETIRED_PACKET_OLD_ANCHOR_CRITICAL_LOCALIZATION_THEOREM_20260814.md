# Root retired packet old-anchor critical-localization theorem

**Date:** 2026-08-14

**Status:** cap-free controlled-priority reduction of every root-held retired
packet to critical atoms of the permanent old root anchor

**Admission correction (2026-08-14).** Retirement provenance does not
authorize adding an atom to its historical recipient's current bundle. The
operation below is instead the singleton, empty-exterior specialization of
`ROOT_STRICT_CLEAN_SUBPACKET_RELEASE_ADMISSION_THEOREM_20260814.md`: the
chosen atom is given alone to the named sacrificed nonroot owner and her
displaced bundle is released to charity. Her explicitly auxiliary later
floor is waived; every nonsacrificed protected floor is unchanged. No
historical reversal is used.

## Exact fixed-label input

Let `r` be the first-priority root, put `x=v_r(X_r)`, and let the exact
root-held `T_{L,times}^*` state have current root target `Z_r`.  The frozen
anchored interface retains a permanent old root core

\[
 A=D_r=T_q+f\subseteq Z_r,
 \qquad v_r(A)>x,                                \tag{1}
\]

which is common-safe and base-desired by `r`.  Let
`empty != K subseteq Z_r` be the named retired collision packet. Every
retired atom `g` has a recorded nonroot historical recipient `u(g)` and is
currently held by `r`. In the clean-release operation `u(g)` is the named
later sacrifice row; this is an operation premise, not a right inferred from
the retirement record.

The protected root floor in this branch is the globally maximal base value
`x`; the current root may have a larger transient value. Every
nonsacrificed owner keeps her current target throughout the operation below.

## One-atom clean controlled release

Choose `g in K`. Specialize the admitted clean-release theorem to `T={g}`
and the empty compatible exterior packet. Form

\[
 Z'_r=Z_r-g,
 \qquad Z'_{u(g)}=\{g\}.                         \tag{2}
\]

Move the displaced old target `Z_{u(g)}` to charity. Every other owner target
is unchanged. The current holder `r` supplies `g`; `u(g)` supplies her
displaced target to charity. The construction deliberately waives only the
named later owner's auxiliary floor. It preserves the protected root floor
and every nonsacrificed protected floor, and it makes no historical
reversibility inference.

The exact root-strict test is

\[
 v_r(Z_r-g)>x.                                    \tag{3}
\]

Two useful support certificates imply (3).

1. If `g notin A`, then `A subseteq Z'_r`, so (1) keeps the same physical
   root anchor strictly above `x`.
2. If `g in A` and `v_r(A-g)>x`, then `A-g` is common-safe by deletion
   monotonicity and remains strictly desired over `X_r`. Record it as the
   new root anchor. This is a controlled anchor release, not an unlabeled
   restoration.

More generally, (3) admits the same clean release even when `A-g` itself is
not strict: retain the strict current target `Z_r-g` and its existing current
anchor label. Thus recurrence tests criticality against all of `Z_r`, not
only against the displayed old subanchor.

In either case the root is strict, so this is exactly the admitted branch of
the clean-release theorem: the candidate conserves goods, preserves every
nonsacrificed protected floor, is supplier-closed, and has an exact physical
response/anchor record. The named sacrifice is part of that record.

## Packet progress and EFX audit

If (2) is EFX, the root remains strictly above the globally maximal base and
the result is a lexicographic contradiction.  Otherwise recompute every EFX
comparison and extract a globally minimum current response.  Independently
of where that response lies, the physical collision packet held by the root
has changed from `K` to `K-g`.  Thus the named packet coordinate strictly
shrinks before any exact fixed-label recurrence can occur. The only target
containing `g` is the singleton `{g}`, which cannot be strongly envied under
positive valuations. Hence every extracted response has intersection
contained in `K-g`; the old root-held packet cannot recur.

The argument waives exactly the named sacrifice row's auxiliary floor. It
does not waive the protected root floor or any nonsacrificed protected floor.
Because the root remains strict, it applies independently of whether the
incoming collision was typed as strict capture, equality-critical capture,
source-inactive/base-floor debt, or normalization bypass.

## Exact recurrent survivor

Define the deletion-critical sets

\[
 C_r(Z_r)=\{g\in Z_r:v_r(Z_r-g)\le x\},
 \qquad
 C_r(A)=\{g\in A:v_r(A-g)\le x\}.                \tag{4}
\]

Every exact root-held recurrence in which all permitted outcomes fail must
satisfy

\[
 \varnothing\ne K\subseteq C_r(Z_r)
 \subseteq C_r(A)\subseteq A.                    \tag{5}
\]

Indeed, every `g in K` failing membership in `C_r(Z_r)` is removed by the
strict clean release. Also `g notin A` is impossible because then
`A subseteq Z_r-g` and `v_r(A)>x`. Finally, for `g in A`, the containment
`A-g subseteq Z_r-g` proves `C_r(Z_r) subseteq C_r(A)`.

Under bundle nondegeneracy, both `Z_r-g` and `A-g` are distinct from `X_r`,
so the survivor inequalities are strict. Writing
`delta_Z=v_r(Z_r)-x>0` and `delta_A=v_r(A)-x>0`, every `g in K` satisfies

\[
 v_r(Z_r-g)<x,
 \qquad v_r(g)>\delta_Z\ge\delta_A,
 \qquad v_r(A-g)<x.                              \tag{6}
\]

Thus the root floor-admission gap is no longer a generic supplier-star
problem. It is localized to a retired packet made entirely of atoms critical
for the full current root target and, consequently, for the old root anchor.

## Claim boundary

This theorem closes every root-held collision containing an off-anchor or
noncritical anchor atom through the admitted clean controlled release. It
does not pay for releasing a current-target-critical atom, prove that
`C_r(Z_r)` is empty, close the remaining critical-anchor packet,
close `T_{L,times}^*`, GG, four-agent EFX, or general additive EFX.

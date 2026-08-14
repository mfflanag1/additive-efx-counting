# Base-contained signed reset to one-good root normal form

**Date:** 2026-08-14

**Status:** cap-free root-preserving signed reset; exact repeats have a
one-good enlarged base root and an on-good loss band or off-good base-root
response

## Input

Let the first-priority root be strict at current bundle `Y_r`, and write

\[
 S^+=Y_r\setminus X_r,
 \qquad S^-=X_r\setminus Y_r.
\]

Then `S^+` is nonempty and

\[
 v_r(S^+)-v_r(S^-)=\delta>0.                   \tag{1}
\]

Assume the named retired packet is base-contained,

\[
 K\subseteq Y_r\cap X_r,                       \tag{2}
\]

and the signed missing-base packet `S^-` is an admitted supplier/release
mode.  The blocked `S^-` branch is already the multi-label charge side of the
signed-support theorem.

## Root-preserving signed reset

Choose `g in S^+`.  Give `S^-` to the root, leave `g` at the root, and
release `S^+-g` through an explicit later-owner sacrifice target.  Every
current holder of `S^-` and the root supplier of `S^+-g` is recorded; other
retired labels moved by the signed return remain explicit.  The new root
target is exactly

\[
 (Y_r-(S^+-g))+S^-=X_r+g.                      \tag{3}
\]

It is strictly above the base by `v_r(g)>0`.  If the tested allocation is
EFX, it contradicts global lexicographic maximality.  Otherwise adopt its
globally minimum response and the physical root/anchor label `X_r+g`.

If this label/state is new, (3) is a valid root-preserving anchor transition.
At an exact repeat, the signed root decoration is the normal form

\[
 S^-_{\rm new}=\varnothing,
 \qquad S^+_{\rm new}=\{g\}.                   \tag{4}
\]

No scalar floor change is counted as a new label.

## Whole-packet response at the normal form

Every target outside `X_r+g` is disjoint from `K`.  Suppose the globally
minimum response `D` lies in the root target and contains the whole packet.
The target is unsafe, so minimum-cardinality extraction makes `D` proper.
The response is safe at the tested allocation. Put

\[
 L=X_r\setminus D.
\]

Because `K subseteq D`, always `L subseteq X_r-K`. There are two exact
support branches.

### On-good response

If `g in D`, properness forces `L` nonempty and

\[
 \varnothing\ne L\subseteq X_r\setminus K,
 \qquad D=(X_r\setminus L)+g.                  \tag{5}
\]

Bundle nondegeneracy gives exactly one of:

1. `v_r(D)>x`, in which case `D` is a safe root-anchor reselection; or
2. `v_r(D)<x`, which by (5) is equivalent to the strict loss band

\[
 v_r(L)>v_r(g).                                  \tag{6}
\]

### Off-good response

If `g notin D`, then

\[
 L\subseteq X_r\setminus K,
 \qquad D=X_r\setminus L.                       \tag{7}
\]

For nonempty `L`, the root values `D` strictly below `x`. For `L=empty`, the
response is exactly the base root bundle `X_r`; this is the source-inactive
base-root response and is not excluded by bundle nondegeneracy because the
physical bundles are identical.

Every response outside the root target has zero `K`-intersection, and every
root response not containing all of `K` gives proper packet reduction.

## Composed normal form

Combining the signed reset, exterior dominance, and source-topology theorem,
the base-contained recurrent face has all of the following:

\[
 Y_r=X_r+g,
 \qquad K\subseteq X_r,
 \qquad v_r(G-X_r)<v_r(k)\ (k\in K),            \tag{7}
\]

an exact safe whole-packet response in the on/off-good forms (5)--(7), and nonroot
source set `{c}`, `{c,q}`, or `{c,s}`, with root-threshold debt in the
two-source cases.

## Claim boundary

This theorem proves the signed reset, the exact-repeat root normal form, and
the two whole-packet support branches. It does not eliminate the on-good loss
band or the off-good base-root/source-inactive branch,
route its response source through the retirement supplier/debt owner, prove
multi-label charge well-foundedness, close `T_{L,times}^*`, GG, four-agent
EFX, or general additive EFX.

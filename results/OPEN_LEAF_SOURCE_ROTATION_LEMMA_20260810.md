# Open-leaf source-rotation lemma

**Date:** 2026-08-10

**Status:** cap-free analytic component-growth step; terminal capture/Hall
branches remain open

## Setting

Let root `q` perform an improving charity replacement

\[
Z_q=X_q\setminus E+f,
\qquad
v_q(f)>v_q(E), \tag{1}
\]

and let a leaf owner `a` receive the released packet:

\[
Z_a=X_a+E. \tag{2}

\]

Suppose a most-envious source `b notin {q,a}` responds to the leaf target
with a common-safe desired subset

\[
B\subseteq X_a+E,
\qquad
v_b(B)>v_b(X_b). \tag{3}

\]

Write

\[
S=B\cap X_a,
\qquad
J=B\cap E. \tag{4}

\]

## Source rotation

Replace the one-leaf endpoint by

\[
Y_q=X_q\setminus E+f,
\]

\[
Y_b=B=S+J,
\]

\[
Y_a=X_b+(X_a\setminus S)+(E\setminus J), \tag{5}

\]

fixing every other owner.  The allocation is complete.  Root `q` strictly
improves by (1), and the newly represented owner `b` strictly improves by
(3).  The old leaf `a` also strictly improves exactly when

\[
v_a(X_b)+v_a(E\setminus J)>v_a(S). \tag{6}

\]

If (6) holds, (5) is an owner-improving component on the strictly larger owner set
`{q,a,b}`.

If it fails, nondegeneracy gives the strict capture wall

\[
v_a(S)>v_a(X_b)+v_a(E\setminus J). \tag{7}

\]

Thus an open leaf source cannot remain an unnamed dependency: it either
grows the improving component or forces the old leaf to rank the portion of
its own bundle captured by the source above both the new source's entire
bundle and every unused root good.

## Release compatibility

Relative to the base allocation, the three targets have labels

| target | incoming | release |
|---|---|---|
| `q` | `f` | `E` |
| `b` | `S+J` | `X_b` |
| `a` | `X_b+(E\J)` | `S` |

The incoming sets are pairwise disjoint.  They are internally supplied:
`f` is initially unallocated, `J` and `E\J` are released by `q`, `S` is
released by `a`, and `X_b` is released by `b`.  Hence every internal
response SDR is a release-compatible PI edge set.  Without an SDR, another
source outside `{q,a,b}` grows the component or Hall's theorem supplies a
minimal deficient target set.

## Hardened-profile check

For the hardened Q-exhausted profile, `a=s`, `b=c`, and the open response is
the ordinary desired subset `B=X_s={z}`.  Inequality (6) holds exactly, so
the rotation represents `q,c,s`.  Its response relation then exposes the
previously fixed owner `r` on the enlarged `s` target.  This is the desired
strict growth of represented owners; it is not yet a universal proof that
the four-owner response relation closes.

The scalar capture implication and packet support replay in
[`open_leaf_source_rotation_audit.json`](open_leaf_source_rotation_audit.json).

## Claim boundary

This lemma proves the cap-free open-source rotation and its exact failure
wall.  It does not eliminate (7), prove that every enlarged component is
EFX, eliminate its final Hall defect after all four owners are represented,
close the R-exhausted branch, close the `GG` flower, or prove four-agent
additive EFX.

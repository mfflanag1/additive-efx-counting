# R3 singleton-source root-compensated direct-return lemma

**Date:** 2026-08-14

**Status:** cap-free second selector for the two-target favorable path;
residual is exact edge overflow or root-margin-plus-charity capture

## Direct return

Use the two-target state and notation

\[
 B_x=X\mathbin{\dot\cup}U\mathbin{\dot\cup}V,
 \qquad B_y=Y\mathbin{\dot\cup}W,
\]

where `x=r` is the strict root, `z` holds singleton `p`, and the signed owner
pairs are `y -> x`, `z -> x`, and `z -> y`.  Let

\[
 D_z=A_x\mathbin{\dot\cup}A_y\mathbin{\dot\cup}A_z
       \subseteq B_x,
 \qquad v_z(D_z)>v_z(p)                          \tag{1}
\]

be an inclusion-minimal response of the singleton holder into the root.

Do not use the root's separate response into `B_y`.  Return `D_z` to `z`,
give `p` to the root, and leave `y,d` unchanged:

\[
 Z_x=(B_x\setminus D_z)\mathbin{\dot\cup}\{p\},
 \quad Z_y=B_y,\quad Z_z=D_z,\quad Z_d=B_d.      \tag{2}
\]

This is complete, and `z` strictly improves because `D_z` is desired above
its former singleton.

## Exact payment alternative

Put

\[
 \delta_x=v_x(B_x)-v_x(X_x)>0.                  \tag{3}
\]

The first-priority root remains strict exactly when

\[
                         v_x(D_z)<\delta_x+v_x(p).\tag{4}
\]

If (4) fails, the response core satisfies the sharp capture alternative

\[
                         v_x(D_z)\ge\delta_x+v_x(p).\tag{5}
\]

Thus direct return never leaves an untyped root-payment failure: the same
core desired by the singleton holder captures the root's entire current
strict margin plus the singleton compensation.

## Exact edge criterion

Besides `charity -> x` and the always-present `z -> y` cell `W`, the only
possible pairs are

\[
\begin{array}{c|c}
x\to z&A_x\ne\varnothing,\\
y\to x&(U\setminus A_y)\ne\varnothing,\\
y\to z&A_y\ne\varnothing,\\
z\to x&(V\setminus A_z)\ne\varnothing.
\end{array}                                      \tag{6}
\]

Hence (2) uses at most four edges exactly when at most two of the four
conditions in (6) hold.  With all three root supplier cells nonempty, the
none/proper/all census has 26 nonempty response signatures.  Ten satisfy
this criterion: two use three edges and eight use four.  When combined with
the earlier full root-path selector, direct return rescues 33 of the 139
full-path-incompatible five-cell signatures, raising the exact union from
69 to 102 of 208 before valuation conditions are applied.

## Consequence

Whenever (4) and the edge criterion both hold, (2) is a priority-valid
complete candidate through at most four edges.  If it is EFX, it is the
required lexicographic endpoint.  Otherwise globally minimal extraction
gives the exact decorated-response continuation at (2).

After testing both favorable-path selectors, the surviving branch has at
least one of:

1. edge overflow for both selectors;
2. the root capture inequality (5); or
3. an exact repeated decorated response at a tested four-edge candidate.

This lemma does not contradict (5), close the observer/repeat continuation,
handle the backward path or singleton star, close the later-source anchor
separator, prove fixed-`U`, or prove general EFX.

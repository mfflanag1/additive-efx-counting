# Canonical-path base-response prefix or terminal-split lemma

**Date:** 2026-08-14

**Status:** cap-free all-owner payment closure when the missing source's
ordinary base-response target is internal on the canonical path; terminal
target reduces to one exact bicriteria packet

## Input

Use the canonical path from
`IMAGE_THREE_UNIQUE_HAMILTONIAN_OMISSION_AND_HOLE_LEMMA_20260814.md`:

\[
       t_0=m\longrightarrow t_1\longrightarrow t_2
       \longrightarrow t_3,                       \tag{1}
\]

with common-safe desired cores

\[
 D_k\subseteq B_{t_k},\qquad
 v_{t_{k+1}}(D_k)>v_{t_{k+1}}(B_{t_{k+1}})
 \quad(k=0,1,2).                                  \tag{2}
\]

The missing source `m` has an ordinary base-desired core

\[
                         C\subseteq B_b,qquad v_m(C)>v_m(X_m), \tag{3}
\]

where `b` is represented and therefore equals one of `t_1,t_2,t_3`.
Assume every represented current bundle is weakly base-paid:

\[
                         v_i(B_i)\ge v_i(X_i)\quad(i\ne m).    \tag{4}
\]

Charity is the positive singleton `p`.

## Internal-target prefix construction

Suppose `b=t_j` with `j in {1,2}`.  Send `C` to `m`, reverse exactly the
path-prefix cores `D_0,...,D_{j-1}`, leave every other current bundle and
path core in place, and give `p` to `m`.

Owner `m` is strictly base-paid by `C` alone.  For `1<=k<=j`, owner `t_k`
receives `D_{k-1}`, whose value exceeds its entire old current bundle by
(2), so it remains strictly paid despite releasing its own next core or `C`.
Every later path owner is unchanged and paid by (4).

The current-holder transfer pairs are

\[
 t_0\to t_1,\ldots,t_{j-1}\to t_j,qquad
 b\to m:C,qquad charity\to m:p.                 \tag{5}
\]

Thus there are `j+2<=4` current-holder pairs.  No packet-size assumption is
used.

At a later mixed-support probe, one displayed packet may contain several
frozen-`Y` suppliers.  Equation (5) is therefore not automatically the
objective's frozen-supplier edge bound; all supplier labels must be retained.

## Terminal-target bicriteria split

Suppose `b=t_3`.  Put

\[
 \Delta_i=v_i(B_i)-v_i(X_i)\ge0\qquad(i\ne m),
 \qquad
 \theta=v_b(C)-\Delta_b.                         \tag{6}
\]

Because `C subseteq B_b`, `theta<=v_b(X_b)`, while (2) gives
`v_b(D_2)>v_b(B_b)>=v_b(X_b)`.  Hence some packet `P subseteq D_2` satisfies

\[
                         v_b(P)\ge\theta.         \tag{7}

\]

Choose an inclusion-minimal such `P`.  Send `C` to `m`, send `P` from
`t_2` to `b`, leave every other ordinary good in place, and give `p` to `m`.
The missing owner and `b` are paid.  Owner `t_2` remains paid exactly when

\[
                         v_{t_2}(P)\le\Delta_{t_2}.              \tag{8}

\]

When (8) holds, the construction uses only the three current-holder pairs

\[
                 t_2\to b:P,qquad b\to m:C,qquad charity\to m:p. \tag{9}

\]

If (8) fails, minimality gives the exact terminal separator

\[
\begin{aligned}
 v_b(P)&\ge\theta,\\
 v_b(P-g)&<\theta &&(g\in P),\\
 v_{t_2}(P)&>\Delta_{t_2}.                       \tag{10}
\end{aligned}

\]

Thus `P` is simultaneously indispensable for compensating the terminal
owner after its response core is removed and too expensive for its physical
predecessor to release while staying base-paid.

## Exact role census

Fix the missing source and the ordinary base-response target, as in the
fixed-`U` roles `m=d`, `b=q`.  Among the twelve compatible image-three maps,
`b` occupies each path position `1,2,3` exactly four times.  Therefore eight
maps have the immediate at-most-four current-holder prefix payment closure;
the other four reduce to (10).

## Claim boundary

Proved: conservation, all-owner payment, exact current-holder edge counts,
the `4+4+4` role census, existence of the terminal compensator, and its
minimal bicriteria failure certificate.  Not proved: frozen-supplier edge
compression for mixed packets, observer EFX safety, elimination of (10)
from signed saturation/PI premises, terminal admission, or the fixed-`U`
theorem.

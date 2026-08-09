# Alternating root-flip lemma

**Date:** 2026-08-09
**Status:** cap-free analytic theorem
**Scope:** normalized monotone valuations; arbitrary packet sizes

## Setup

Let a partial EFX allocation have

\[
X_p=\{x\},\qquad X_s=\{y\},\qquad X_r,\qquad X_q,
\]

with one unallocated good `f`.  Assume the ordinary envy edges

\[
r\longrightarrow s,
\qquad
q\longrightarrow p,
\tag{1}
\]

so

\[
v_r(y)>v_r(X_r),
\qquad
v_q(x)>v_q(X_q).
\tag{2}
\]

Let \(D\subseteq X_r\cup\{f\}\) be a selected desired set for `p`.  Thus

\[
v_p(D)>v_p(x)
\tag{3}
\]

and no agent strongly envies `D` relative to the base allocation:

\[
v_i(D\setminus\{g\})\le v_i(X_i)
\qquad(i\in\{p,r,s,q\},\ g\in D).
\tag{4}
\]

No assumption about the internal size of `D`, `X_r`, or `X_q` is made.

## Theorem

> **Root-flip lemma.** At least one of the following partial allocations is
> EFX:
>
> \[
> A=(\{x\},\{y\},D,X_q)
> \quad\text{for owners }(p,r,s,q),
> \tag{5}
> \]
>
> or
>
> \[
> B=(D,\{y\},X_q,\{x\})
> \quad\text{for owners }(p,r,s,q).
> \tag{6}
> \]
>
> Goods not displayed in (5)--(6) remain unallocated.

Consequently, the base allocation is not lexicographically maximal for the
priority order `(p,q,r,s)`.  Allocation `A`, when EFX, preserves `p` and `q`
and strictly improves `r`.  Allocation `B`, when EFX, strictly improves `p`.

## Proof

Write \(u_i=v_i(X_i)\).  Base EFX gives

\[
v_i(X_q\setminus\{h\})\le u_i
\qquad(i\in N,\ h\in X_q),
\tag{7}
\]

and desired-set safety gives (4).

In allocation `A`, agents `p` and `q` retain utilities \(u_p,u_q\), while
`r` has utility \(v_r(y)>u_r\).  Hence (4) and (7) verify every EFX
comparison made by `p`, `q`, or `r`.  The other bundles visible to `s`, apart
from `D` and `X_q`, are singletons.  Therefore `A` can fail EFX only if

\[
v_s(X_q\setminus\{h\})>v_s(D)
\tag{8}
\]

for some \(h\in X_q\).

In allocation `B`, (2)--(3) show that `p`, `r`, and `q` all strictly improve
over their base utilities.  Equations (4) and (7) therefore verify all of
their EFX comparisons.  Again the other visible bundles are singletons, so
`B` can fail EFX only if

\[
v_s(D\setminus\{g\})>v_s(X_q)
\tag{9}

for some \(g\in D\).

If both allocations failed, nonnegativity and (8) would give

\[
v_s(X_q)>v_s(D),
\]

while nonnegativity and (9) would give

\[
v_s(D)>v_s(X_q),
\]

a contradiction.  Thus at least one allocation is EFX.  Its stated
lexicographic improvement follows from (2)--(3). \(\square\)

## Alternating-cycle consequence

In the alternating champion cycle

\[
p\xrightarrow f r\longrightarrow s
\xrightarrow f q\longrightarrow p,
\]

take `D` to be `p`'s selected desired set on the edge entering `r`.  The
lemma closes the hard priority order `(p,q,r,s)` for arbitrary bundle sizes.
Rotating the cycle by two vertices closes `(s,r,q,p)` as well.

Together with the easy-priority lemma, 18 of the 24 priority-role orders in
the alternating two-large topology are now closed cap-free.  The remaining
six are

\[
(p,s,r,q),\ (p,s,q,r),\ (p,q,s,r),
(s,p,r,q),\ (s,p,q,r),\ (s,r,p,q).
\]

The proof uses only monotonicity, base EFX, desired-set safety, and the two
strict envy relations; additivity and absence of compatible cross-bottom
families are not needed.  It does not by itself close the alternating
topology, the complete two-large case, or complete four-agent EFX.

## Exact discovery certificate

The lemma was extracted from a deletion-minimal two-rival QF_LRA core in the
eleven-good split-packet cell.  See
[`alternating_root_flip_split_core_audit.json`](alternating_root_flip_split_core_audit.json)
and its independent replay script.

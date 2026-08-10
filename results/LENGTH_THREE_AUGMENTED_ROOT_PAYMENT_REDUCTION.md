# Augmented-root payment reduction

**Date:** 2026-08-09

**Status:** valid cap-free analytic reduction, superseded as a completion
gate by the reservoir-order escape theorem

## Setup

Let `P` be an externally safe augmented `p`-root produced by the
parallel-root pivot lemma.  Thus

\[
v_p(P)>b_p,\qquad
\tau_i(P)\le b_i\quad(i=r,q,s).
\tag{1}
\]

In the external-`q` cell, both `x` and `y` are desired singletons for `q`.
Give `s` her preferred singleton `w` and give `q` the other singleton `z`,
breaking an `s`-tie in favor of `w=y`.  Then

\[
v_s(w)\ge b_s,\qquad v_q(z)>b_q.
\tag{2}
\]

We work in the live external-`q`-only branch.  If `p` also envies `y`, the
external-`p` theorem closes the state.  Hence throughout the live branch

\[
v_p(x)=b_p,\qquad v_p(y)\le b_p.
\tag{2a}
\]

Let `U` be the residual after reserving `P,z,w`, put
`theta=tau_r(P)`, and suppose `v_r(U)>=theta`.  Choose an inclusion-minimal
`R subseteq U` with `v_r(R)>=theta`.  Test deletion remainders of `R` at

\[
c_p=\tau_p(P),\qquad c_q=v_q(z),\qquad c_s=v_s(w).
\tag{3}
\]

The first ceiling is strictly above `b_p`: the augmented root contains the
new desired root as a deletion remainder.

If every remainder satisfies (3), then `(P,R,{z},{w})` is EFX and improves
`p`.

Otherwise choose an inclusion-minimal crossing set `F` inside a violating
deletion.  Every deletion of `F` is below all ceilings in (3), and

\[
v_r(F)<\theta.
\tag{4}
\]

## Boundary sources

If `F` is `p`-sourced, choose a least-`r` good `h in P`.  Then

\[
(F,P-h,\{z\},\{w\})
\tag{5}
\]

is EFX.  Agent `p` values `F` above `tau_p(P)>b_p`; agent `r` receives
value `theta` and (4) settles her comparison to `F`.  External safety of
`P` and the deletion bounds for `F` settle `q` and `s`.

Suppose `F` is `q`-sourced.  If `v_r(z)>=theta`, then

\[
(P,\{z\},F,\{w\})
\tag{6}
\]

is EFX.  Otherwise choose a least-`p` good `k in P`, so

\[
v_p(P-k)=\tau_p(P)>b_p.
\tag{7}

\]

If

\[
v_r(z+k)\ge
\max\{\tau_r(P-k),\tau_r(F)\},
\tag{8}
\]

then

\[
(P-k,\{z,k\},F,\{w\})
\tag{9}
\]

is EFX.  Agent `q` values `F` above `z`; external safety of `P` gives
`v_q(k)<=tau_q(P)<=v_q(z)`, so she can also compare to `z+k`.  Agent `p`
owns her maximum deletion remainder (7), which dominates the `p`-tail of
`F`, both singleton values in the live external-`q` branch, and the tail of
`P-k`.  Agent `s` is protected by her preferred singleton and (1)--(3).
Condition (8) is exactly the two comparisons made by `r`.

Finally suppose `F` is `s`-sourced.  Let `a` be `q`'s less-preferred
singleton and `b` her more-preferred singleton.  If `v_r(a)>=theta`, then

\[
(P,\{a\},\{b\},F)
\tag{10}

\]

is EFX.  Otherwise, with the same least-`p` good `k`, the allocation

\[
(P-k,\{a,k\},\{b\},F)
\tag{11}

\]

is EFX whenever

\[
v_r(a+k)\ge
\max\{\tau_r(P-k),\tau_r(F)\}.
\tag{12}

\]

Here `q` prefers `b` to `a`, while `s` values `F` above her preferred
singleton and therefore above both singleton goods.  The remaining checks
are identical to (9).

## Exact remaining output

Once total residual capacity exists, every unsafe payment closes except a
failure of (8) or (12).  Both have the same form:

> the singleton assigned to `r`, augmented by the least-`p` good of `P`,
> is worth less to `r` than a deletion tail of `P-k` or of the minimal
> boundary `F`.

This is a one-good compensation deficit, not a packet-wide Hall wall.  It
must be routed together with the capacity certificate
`v_r(g)>v_r(B_q)` from the parallel-root lemma when total capacity itself
fails.

All five displayed candidate-allocation implications replay as exact
QF_LRA-UNSAT when their EFX conclusion is negated in
[`length_three_augmented_root_payment_audit.json`](length_three_augmented_root_payment_audit.json).
That audit checks the aggregate additive inequalities; the BCFF derivation
of the augmented root, residual, and minimal boundary remains analytic.

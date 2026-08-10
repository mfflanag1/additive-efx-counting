# Adaptive-singleton reduction for the external-`q` rows

**Date:** 2026-08-09

**Status:** valid cap-free analytic reduction, superseded as a completion
gate by the reservoir-order escape theorem

**Rows:** `(p,r,q,s)`, `(p,r,s,q)`, `(p,s,r,q)`, `(s,p,r,q)`

## Setup

Let the external singleton edge be `q -> s`, and retain the selected edge
`q -> p`.  Thus both singleton goods satisfy

\[
v_q(x)>b_q,\qquad v_q(y)>b_q.
\tag{1}
\]

Put `E=T_r+f`, choose a least-`r` good `h in E`, and write

\[
\theta=\tau_r(E)=v_r(E-h).
\tag{2}
\]

Let `w` be `s`'s preferred member of `{x,y}` and let `z` be the other,
breaking a tie in favor of `w=y`.  Provisionally give `q` the singleton
`z` and `s` the singleton `w`.  This does not lower `s`, because
`v_s(w)>=v_s(y)=b_s`, and (1) makes either singleton an improvement for
`q`.

Choose an inclusion-minimal `R subseteq B_r+X_q` with
`v_r(R)>=theta`, and test its deletion remainders at

\[
v_p(E),\qquad v_q(z),\qquad v_s(w).
\tag{3}
\]

If every remainder satisfies (3), then

\[
(E,R,\{z\},\{w\})
\tag{4}
\]

is EFX and improves `p`.  Otherwise extract an inclusion-minimal crossing
set `F` inside a violating deletion.  Every deletion of `F` is below all
three ceilings in (3), and

\[
v_r(F)<\theta.
\tag{5}
\]

## Source routing

If `F` is `p`-sourced, `(F,E,{z},{w})` is EFX and improves `p`.

Suppose `F` is `q`-sourced.  If `v_r(z)>=theta`, then

\[
(E,\{z\},F,\{w\})
\tag{6}
\]

is EFX.  If `v_r(z)<theta` but

\[
v_p(z)\ge v_p(E-h),
\tag{7}
\]

then

\[
(\{z,h\},E-h,F,\{w\})
\tag{8}

\]

is EFX.  Agent `s` is safe against `z+h` because `w` is her preferred
singleton and `h` lies in a deletion remainder of the common-safe set `E`.
The remaining comparisons are the canonical least-pivot calculation.

Finally suppose `F` is `s`-sourced.  Let `a` be `q`'s less-preferred
singleton and `b` her more-preferred singleton, breaking a tie with `a=x`.
Because `w` is `s`'s preferred singleton, `v_s(F)>v_s(w)` dominates both
singleton values for `s`.  If `v_r(a)>=theta`, then

\[
(E,\{a\},\{b\},F)
\tag{9}
\]

is EFX.  If `v_r(a)<theta` but

\[
v_p(a)\ge v_p(E-h),
\tag{10}
\]

then

\[
(\{a,h\},E-h,\{b\},F)
\tag{11}
\]

is EFX.  Agent `q` prefers `b` to `a`, and agent `s` values `F` above both
singletons, so the two possible external-observer walls are absent.

Every allocation (4), (6), (8), (9), and (11) improves `p`, except that an
`s`-sourced boundary also improves `s`.  Hence each closes all four stated
orders.

## Exact surviving walls

The base singleton `x` always satisfies

\[
v_p(x)=b_p\ge v_p(E-h)
\tag{12}
\]

by common safety of `E`.  Therefore failure of (7) or (10) forces the
anchor to be `y`.  The entire external-`q` row is reduced to exactly these
two scalar certificates:

1. **`q`-boundary wall**
   \[
   v_s(x)>v_s(y),\qquad
   v_r(y)<\theta,\qquad
   v_p(y)<v_p(E-h);
   \tag{13}
   \]
2. **`s`-boundary wall**
   \[
   v_q(x)>v_q(y),\qquad
   v_r(y)<\theta,\qquad
   v_p(y)<v_p(E-h).
   \tag{14}
   \]

The strict preference in (13) follows from the tie rule defining `w`; the
one in (14) follows from the tie rule defining `a`.  No packet-size or
fixed-value assumption occurs.  Proving that (13)--(14) force a root flip,
cross-reservoir escape, or a shorter/adjacent cycle is the remaining
external-`q` task.

All eight direct/suffix calculations, for both singleton orientations,
replay as QF_LRA-UNSAT in
[`length_three_canonical_packet_audit.json`](length_three_canonical_packet_audit.json).
The audit verifies the local algebra, not the structural derivation or the
final exclusion of (13)--(14).

## Charity-swap routing of the two walls

Both walls have the same first fallback.  The selected-cycle inequalities
give `v_r(T_q)>v_r(T_r)`.  In wall (13), where `s` prefers `x`, test

\[
(E,T_q,\{y\},\{x\});
\tag{15}
\]

in wall (14), test

\[
(E,T_q,\{x\},\{y\}).
\tag{16}

\]

Either allocation is EFX whenever

\[
v_r(T_q)\ge\theta.
\tag{17}

\]

The singleton recipients strictly improve in the applicable wall, `p`
gets the desired set `E`, and (17) is `r`'s only nonautomatic comparison.

Suppose (17) fails.  Since `v_r(T_q)>v_r(T_r)`, a deletion attaining
`theta=tau_r(T_r+f)` cannot remove `f`.  It removes a good `g in T_r`, and

\[
v_r(f)>v_r(g).
\tag{18}

\]

Replace `g` in `X_r` by `f`.  If the resulting allocation is EFX, it
Pareto-improves `r`.  Otherwise the charity-swap transition produces a new
genuine edge `k -f-> r`, with a desired set omitting `g` and one additional
deletion witness.  Its source routes as follows.

1. `k=r` is a forbidden self-champion.
2. `k=q` enters the two-genuine-edge length-two residual.
3. `k=p` is a parallel root into `r`; it is the only branch that stays in
   the same rooted wall.
4. `k=s` closes after changing the selected length-three cycle.  In wall
   (13), the new cycle is `s -f-> r -f-> q -> s`, with old `p` external;
   the edge `s -> p` from (13) makes its external source the new `p`, so the
   cap-free external-`p` theorem applies.  In wall (14), the same new cycle
   has external source `q`.  Swapping the singleton roles reverses the
   strict `q` preference in (14), while old `p` does not prefer `y` to its
   own `x` unless the already-closed external-`p` source is also present.
   Hence neither scalar wall survives in the renamed cell, and the adaptive-
   singleton reduction closes it.

Consequently the external-`q` obstruction is no longer an arbitrary
singleton wall.  It is exactly a finite-family parallel-`p` root recurrence,
with a possible handoff to the length-two topology.  A global potential on
parallel `p -f-> r` decompositions, or an independently composed length-two
escape, is the remaining operation.

The parallel branch itself admits a strict refinement.  If a failed
charity swap exposes a new `p`-root `E'` after removing pivot `g`, then
`E'+g` is strictly better for `p` than the old root.  Every external failure
of this augmentation either creates an ordinary PI cycle or a non-`p`
champion and routes out.  Thus the root recurrence closes at the safety
level; only the residual payment for the augmented root remains.  See
[`LENGTH_THREE_PARALLEL_ROOT_PIVOT_REDUCTION.md`](LENGTH_THREE_PARALLEL_ROOT_PIVOT_REDUCTION.md).

# Canonical escape for the external-`p` length-three row

**Date:** 2026-08-09

**Status:** cap-free analytic theorem

**Priority order:** `(s,p,r,q)`

## Setup

Use the length-three normal form

\[
X_p=\{x\},\qquad X_r=T_r\mathbin{\dot\cup}B_r,\qquad
X_q=T_q\mathbin{\dot\cup}B_q,\qquad X_s=\{y\},
\]

with charity good `f`, selected desired set

\[
E=T_r+f
\]

for `p`, and external envy edge `p -> s`.  Put

\[
b_i=v_i(X_i),\qquad \theta=\tau_r(E).
\]

The selected-cycle inequalities give

\[
v_r(B_r+X_q)>b_r\ge\theta.
\tag{1}
\]

Choose an inclusion-minimal `R subseteq B_r+X_q` with
`v_r(R)>=theta`.  Set

\[
c_p=\min\{v_p(E),v_p(y)\},\qquad c_q=v_q(x),\qquad c_s=b_s.
\tag{2}
\]

## Theorem

> At least one explicit partial allocation below is EFX and
> lexicographically improves the base in order `(s,p,r,q)`.  No packet-size
> bound is required.

If every deletion of `R` is below the three ceilings in (2), then

\[
(Y_p,Y_r,Y_q,Y_s)=(E,R,\{x\},\{y\})
\tag{3}
\]

is EFX and improves `p` while fixing `s`.

Otherwise, inside a violating deletion of `R`, choose an inclusion-minimal
set `F` crossing one of the ceilings in (2).  Every deletion of `F` is at
or below all three ceilings, and minimality of `R` gives

\[
v_r(F)<\theta.
\tag{4}
\]

The source of `F` determines the escape.

### Source `p`

Use

\[
(F,E,\{x\},\{y\}).
\tag{5}
\]

Agent `p` values `F` above `c_p>b_p`.  Agent `r` can hold `E`, since
`v_r(E)>=theta>v_r(F)`.  The deletion bounds for `F`, common safety of
`E`, and the singleton bundles verify every other comparison.  Thus (5) is
EFX, fixes `s`, and improves `p`.

### Source `s`

Use

\[
(\{y\},E,\{x\},F).
\tag{6}
\]

Here `s` strictly improves.  Agent `p` can hold `y`: deletion remainders of
`F` are at most `c_p<=v_p(y)`, while common safety of `E` and the singleton
`x` settle her other comparisons.  Equation (4) lets `r` hold `E`, and
the `q`-ceiling settles `q`'s comparison to `F`.  Hence (6) is EFX.

### Source `q`

Now

\[
v_q(F)>v_q(x)>b_q.
\tag{7}
\]

If `v_r(x)>=theta`, use

\[
(E,\{x\},F,\{y\}).
\tag{8}
\]

Agent `r` can compare to `E` by the assumed inequality and to `F` by (4).
All other comparisons follow from (2), common safety of `E`, and (7).

Suppose instead `v_r(x)<theta`.  Choose a least-`r` good `h in E`.  Since
`E` has at least two goods,

\[
v_r(E-h)=\theta,\qquad v_r(h)\le\theta.
\tag{9}
\]

Use the suffix rotation

\[
(\{x,h\},E-h,F,\{y\}).
\tag{10}
\]

The desired-set safety of `E` gives
`v_p(E-h)<=b_p=v_p(x)`, and therefore

\[
v_p(x+h)\ge v_p(E)>b_p.
\tag{11}
\]

Agent `r` safely compares to `x+h`: deleting `h` leaves `x`, whose value is
below `theta`, while deleting `x` leaves `h`, whose value is at most
`theta`.  Equation (4) settles her comparison to `F`.

Agent `q` owns `F` and, by (7), can compare to `x`; she can compare to `h`
and `E-h` because they lie in deletion remainders of the common-safe set
`E`.  Agent `s` has the same safety for `h` and `E-h`.  Finally,
`v_s(x)<=b_s`: otherwise `s -> p`, together with the external envy edge
`p -> s`, is an ordinary-envy PI 2-cycle at the base.  The deletion bounds
for `F` settle the remaining comparisons.  Thus (10) is EFX, fixes `s`,
and improves `p`.

The four constructions exhaust the minimal boundary source and the scalar
comparison of `x` with `theta`.  This proves the theorem. \(\square\)

## Consequence and trust boundary

The sole residual priority type with external singleton source `a=p` is
closed for arbitrary packets.  The former maximizing-`Q`, anchor-safety,
and scalar-deficit branches are unnecessary for this row.

The proof is analytic.  Its eight aggregate packet calculations replay as
QF_LRA-UNSAT in
[`length_three_canonical_packet_audit.json`](length_three_canonical_packet_audit.json).
That audit checks the displayed inequalities but does not replace their
BCFF derivation.  The remaining
length-three work concerns the external-source types `a=q` and `a=r` and
the final BCFF composition.

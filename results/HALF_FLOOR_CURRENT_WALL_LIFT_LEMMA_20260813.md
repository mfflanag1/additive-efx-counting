# Half-floor current-wall lift lemma

**Date:** 2026-08-13

**Status:** cap-free conversion of the nonsingleton `d->r` current wall into
a base-paying unrestricted packet; final enlarged-target observer safety
remains

## Setting

Normalize the sacrificed owner's base floor to `F_d>0`.  In the saturated
root-facing fixed-`U` state write

\[
 W=Y_d,
 \qquad v_d(W)\ge \tau_d(Q),
 \qquad v_d(W)<\tau_d(A),                         \tag{1}
\]

where `Q` is the ordinary base-desired `d->q` core and `A` is the root core.
Thus

\[
 v_d(Q)>F_d.                                      \tag{2}
\]

Assume first that `Q` contains at least two positive-value goods.  No upper
bound on its cardinality is imposed.

## The half-floor inequality

Let `q` be a least-`d` good of `Q`.  Since `Q` has at least two goods,

\[
 v_d(q)\le \frac12v_d(Q),
\]

and hence

\[
 \tau_d(Q)=v_d(Q-q)\ge \frac12v_d(Q)>\frac12F_d.
                                                               \tag{3}
\]

It follows from (1) that

\[
 v_d(W)>\frac12F_d.                              \tag{4}
\]

Choose a least-`d` good `g` of `A` and put

\[
                         T=A-g.                  \tag{5}
\]

Then `v_d(T)=tau_d(A)>v_d(W)>F_d/2`. Choose an
inclusion-minimal nonempty packet `D subseteq T` such that

\[
                         v_d(D)>v_d(W).           \tag{6}
\]

It exists because `T` itself has this property. Minimality gives
`tau_d(D)<=v_d(W)`. For every other observer, the full-value estimate below
gives `v_i(D)<=F_i`, hence also current safety at a paid represented state.
Thus `D` is an exact current-safe desired core, and

\[
                  v_d(W+D)>F_d.                 \tag{7}
\]

Thus the strong-wall core `D` need not itself be base-desired. Whenever
`d` retains `W`, receiving the unrestricted packet `D` strictly pays `d`
above the base floor.  Charity, if also assigned to `d`, is pure additional
slack.

## Safety of the lifted packet

The root core `A` is base-common-safe:

\[
 \tau_i(A)\le F_i\qquad(i\in N).                 \tag{7}
\]

Although `g` was chosen using `d`'s row, for every observer `i` its value is
at least the least `i`-value in `A`.  Therefore

\[
 v_i(T)=v_i(A)-v_i(g)
       \le v_i(A)-\min_{a\in A}v_i(a)
       =\tau_i(A)\le F_i.                         \tag{8}
\]

Since `D subseteq T`, `v_i(D)<=F_i` as well. For observers other than its
source, `D` is stronger than merely current-common-safe: its **full value**
is at most the base floor. It may be moved as one packet regardless of how
many goods it contains.

## Singleton alternative

If `Q` is a singleton, (2) says that `Q` itself is already a base-paying
one-packet response for `d`.  Consequently every state has the exact
payment dichotomy

1. `Q` is a singleton and the ordinary `d->q` packet alone pays `d`; or
2. `Q` is nonsingleton and retaining `W` while importing the minimal current
   core `D subseteq A-g` pays `d` by (7).

This removes **owner payment** as a reason to treat `d->r` as an unusable
current-only response.  In the R3 near-perfect matching, where `d` is the
target hole and retains `W`, the second branch supplies the previously
missing base-payment implication without converting `A-g` into a
base-desired core.

## Exact remaining boundary

The final bundle is `W+D` (and possibly charity), not `D` alone.  Equation
(8) therefore does not prove that the enlarged target `W+D` is safe for all
other observers.  Nor does the singleton branch by itself prove that the
`d->q` packet can be chosen disjointly from every other reversed core.

The mixed current/base gate is consequently reduced to one issue:
**observer-safe integration or saturated decorated-response extraction for
the enlarged `d` target**.  A countermodel to the universal four-edge theorem
must defeat both the singleton base packet and the nonsingleton half-floor
lift while satisfying the full response/saturation premises.  This lemma
does not by itself prove complete EFX or the universal four-edge theorem.

[`audit_half_floor_current_wall_lift.py`](../tracks/parkability/audit_half_floor_current_wall_lift.py)
independently verifies the half-floor implication, base payment, and the
cross-observer deletion inequality in exact QF-LRA, with no item cap.

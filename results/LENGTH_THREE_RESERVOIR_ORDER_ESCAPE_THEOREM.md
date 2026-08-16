# Reservoir-order escape for the length-three topology

**Date:** 2026-08-09

**Status:** cap-free analytic theorem covering every priority and external
source type

## Normal form

Let

\[
X_p=\{x\},\qquad X_r=T_r\mathbin{\dot\cup}B_r,\qquad
X_q=T_q\mathbin{\dot\cup}B_q,\qquad X_s=\{y\},
\]

with one charity good `f` and selected length-three basic cycle

\[
p\xrightarrow f r\xrightarrow f q\longrightarrow p.
\tag{1}
\]

Thus `D_p=T_r+f` is desired by `p`, `D_r=T_q+f` is desired by
`r`, and `q` envies `{x}`. Let `a in {p,r,q}` be the source of the
external envy edge `a -> s`, so `a` envies `{y}`. All desired bundles are
common-safe at the base.

## Minimal-threshold extraction

The following elementary operation is used in both order orientations.
Let `D` be common-safe, let `P` be a disjoint pool containing a desired
set, and put `t=tau_j(D)`. Then either:

1. there is a common-safe `Q subseteq P` with `v_j(Q)>=t`; or
2. there is a desired `A subseteq P` with `v_j(A)<t`.

If `v_j(P)<t`, take a minimal desired subset of `P`. Otherwise take an
inclusion-minimal `Q subseteq P` crossing `t`. If `Q` is unsafe, a minimal
desired subset of an unsafe deletion `Q-h` has `j`-value below `t`.
This extraction is cap-free.

## The `q`-before-`r` orientation

Put

\[
W=X_q+B_r,\qquad t_r=\tau_r(D_p).
\tag{2}
\]

The pool contains a desired set because
`v_q(W)>v_q(X_q)=b_q` (*cancelable-class repair 2026-08-16*, R2: `B_r` is
nonempty and disjoint from `X_q`, so `W` and `X_q` are different bundles;
monotonicity gives `>=` and non-degeneracy upgrades it to `>`. The former
additive form `b_q+v_q(B_r)` was decorative). Apply extraction to
`(D_p,W,r)`.

If it returns a common-safe `Q` with `v_r(Q)>=t_r`, then

\[
(Y_p,Y_r,Y_q,Y_s)=(D_p,Q,\{x\},\{y\})
\tag{3}
\]

is EFX. Agent `p` and agent `q` strictly improve, while `s` is fixed.

Otherwise it returns a desired `A subseteq W` with
`v_r(A)<t_r`. According to the source of `A`, use:

| source of `A` | `(Y_p,Y_r,Y_q,Y_s)` |
|---|---|
| `p` | `(A,D_p,{x},{y})` |
| `r` | `(D_p,A,{x},{y})` |
| `q` | `({x},D_p,A,{y})` |
| `s`, `a=p` | `({y},D_p,{x},A)` |
| `s`, `a=r` | `(D_p,{y},{x},A)` |
| `s`, `a=q` | `({x},D_p,{y},A)` |

Every displayed bundle is common-safe or a singleton. The only recipient
who may not receive a base-improving bundle is `r` holding `D_p`; the strict
inequality

\[
v_r(D_p)>\tau_r(D_p)>v_r(A)\ge\tau_r(A)
\tag{4}
\]

settles her sole comparison between nonsingletons. In every displayed
allocation, `p` and `s` are fixed or improved, `q` strictly improves, and
only `r` may lose utility. Hence `q` preceding `r` makes each allocation a
lexicographic improvement, independently of the positions of `p,s`.

## The `r`-before-`q` orientation

Put

\[
U=X_r+B_q,\qquad t_q=\tau_q(D_r).
\tag{5}
\]

Here `v_r(U)>v_r(X_r)=b_r` (*cancelable-class repair 2026-08-16*, R2; `B_q`
nonempty, same monotone-plus-non-degenerate argument as for `W`), so `U`
contains a desired set. Apply extraction to `(D_r,U,q)`.

If it returns a common-safe `Q` with `v_q(Q)>=t_q`, then

\[
(Y_p,Y_r,Y_q,Y_s)=(\{x\},D_r,Q,\{y\})
\tag{6}
\]

is EFX, fixes `p,s`, and strictly improves `r`.

Suppose extraction instead returns a desired `A subseteq U` with
`v_q(A)<t_q`. Only `r` and `s` can source `A`. To see this, put
\(H=A\cap B_q\). If `H` is empty, a `p`- or `q`-source would envy
`X_r`, contrary to the large-bundle no-envy lemma. If `H` is nonempty,
put `S=X_r\setminus A`. Then

\[
A=(X_r\setminus S)\mathbin{\dot\cup}H.
\]

Because `A` is desired by its source and common-safe, that source is most
envious of the displayed set. Hence `A` gives a generalized
`(H|S)`-champion edge into `r`. A `q`-source closes

\[
q\xrightarrow{H\mid S}r\xrightarrow f q,
\]

and a `p`-source closes

\[
p\xrightarrow{H\mid S}r\xrightarrow f q\longrightarrow p.
\]

The edge `r -f-> q` releases the whole bottom `B_q`, hence the incoming
set `H subseteq B_q`; the remaining incoming set `{f}` is unallocated.
The incoming sets are disjoint, so both displayed cycles satisfy BCFF
Definition 3.4 and contradict global maximality. No chordless-graph
assumption is used.

If `A` is desired by `r`, use

\[
(Y_p,Y_r,Y_q,Y_s)=(\{x\},A,D_r,\{y\}).
\tag{7}
\]

This is EFX because

\[
v_q(D_r)>\tau_q(D_r)>v_q(A)\ge\tau_q(A).
\tag{8}
\]

It fixes `p,s` and strictly improves `r`.

If `A` is desired by `s`, use the external source `a`:

| external source `a` | `(Y_p,Y_r,Y_q,Y_s)` |
|---|---|
| `p` | `({y},D_r,{x},A)` |
| `r` | `({x},{y},D_r,A)` |
| `q` | `({x},D_r,{y},A)` |

For `a=p` and `a=q`, every changed recipient receives a desired bundle.
For `a=r`, agents `r,s` receive desired bundles and (8) settles `q`'s
comparison between `D_r` and `A`. Thus all three allocations are EFX.
In every displayed allocation, `p` and `s` are fixed or improved, `r`
strictly improves, and only `q` may lose utility. Together with (6)--(7),
this contradicts every priority order with `r` before `q`.

## Global length-three conclusion

Every priority order has exactly one of `q` before `r` or `r` before `q`.
The two reservoir orientations above therefore cover all 24 orders for
each of the three possible external sources. Consequently:

> **Length-three global-lex escape theorem.** A positive, PI-free,
> one-charity partial EFX allocation in the length-three normal form (1),
> with arbitrary nonempty packets, is not globally lexicographically
> maximal.

No fixed-size cell, bounded value domain, extremal pair assumption, or
absence of nonselected champion edges is used. \(\square\)

## Composition with the BCFF reduction

The theorem applies directly to the length-three branch of the BCFF
exactly-two-nonsingleton reduction.

Start with a globally lexicographically maximal one-charity partial EFX
allocation in the positive nondegenerate profile used by BCFF. It is
PI-free, since BCFF Lemma 3.5 converts a PI cycle into a Pareto-improving
EFX allocation. Select one incoming basic champion edge for every allocated
bundle. A selected edge whose desired set discards `f` can be replaced by
the parallel envy edge. Call the remaining edges genuine.

A selected simple cycle has at least two genuine edges: a cycle with zero
or one is already PI. No genuine edge enters a singleton. Indeed, for a
singleton `{z}`, the only subsets of `{z,f}` containing `f` are `{f}` and
`{z,f}`; the first is not envied by charity dominance, while the second is
not common-safe after deleting `f` because every singleton is envied at
global maximality. With exactly two nonsingleton bundles, a simple selected
cycle therefore contains exactly two genuine edges, entering the two large
owners.

In the length-three branch the two genuine edges are consecutive and the
third edge is an envy return. Relabeling its vertices gives exactly (1),
with the remaining singleton owner `s` external. That singleton is envied:
otherwise its owner could absorb `f` while preserving EFX. Its envier is
some `a in {p,r,q}`, giving the three source cases used above.

The top/bottom packets in (1) are nonempty. An empty top would make `{f}`
desired, contradicting charity dominance. An empty bottom, together with
BCFF Observation 2.10 and positivity, would force a self-`f`-champion and
hence a PI cycle. The selected desired tops are common-safe by definition.
Finally, every nonowner's envy of either large bundle closes a PI cycle
through (1) and the external envy edge, proving the large-bundle no-envy
premise used in the low-source exclusion.

Thus every hypothesis of the reservoir-order theorem is derived from the
BCFF state. Extra envy or champion edges do not invalidate the argument:
an edge used by the low-source wall is explicitly routed as a PI cycle,
and all other extra edges are harmless additional structure. This proves
the length-three branch without an exact-graph, chordless, fixed-packet,
or uniqueness assumption.

For nonnegative valuations and ties, apply BCFF Lemma A.1, run the argument
in its respecting positive nondegenerate perturbation, and return the EFX
allocation to the original profile. Any strict original EFX violation would
remain strict in the perturbation. No additional continuity premise is
needed.

This composition proves only the length-three branch. It does not silently
assume or claim the length-two or either length-four branch, nor the cases
with more than two nonsingleton bundles.

## Trust boundary

The twenty-four aggregate allocation implications replay as exact
QF_LRA-UNSAT in
[`length_three_reservoir_order_packet_audit.json`](length_three_reservoir_order_packet_audit.json).
That audit checks the aggregate threshold inequalities; its encoding uses
only bundle totals and deletion maxima, so it is valid for cancelable
valuations. The source exclusion in the `r`-before-`q` low branch and the
derivation of the normal form from BCFF remain analytic parts of the theorem.

*Cancelable-class repair 2026-08-16* (R5 of
[`CANCELABLE_CLASS_SWEEP_20260816.md`](CANCELABLE_CLASS_SWEEP_20260816.md)).
This sentence previously read "That audit checks the additive inequalities",
which understated it.  `decide_length_three_reservoir_order.py` represents
each bundle by two scalars — a total and a tail (`= tau`) — constrained only
by `total > 0`, `0 <= tail < total`, `tail <= base`, plus the base
envy/desire signs.  There is no per-good decomposition and no sum anywhere in
the encoding, so those constraints are exactly the monotone, non-degenerate
and common-safety facts and the replay certifies the aggregate argument at
the cancelable level.  Re-replayed on this branch: `status: ALL_FORCED,
cases: 24` (z3 5.0.0).

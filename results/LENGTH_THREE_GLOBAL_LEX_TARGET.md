# Length-three global-lex target

**Date:** 2026-08-09

**Status:** BCFF normal form reconstructed; easy priority types closed
cap-free; packet-safety gate open

## Source-valid starting point

Fix a lexicographic priority order and choose a globally maximal partial EFX
allocation `X`.  Berger--Cohen--Feldman--Fiat (BCFF), Lemma 2.4, permits the
one-charity contradiction setup and proves that no agent envies the set of
unallocated goods.  In the present residual there is one unallocated good
`f`, so

\[
v_i(f)\le v_i(X_i)\qquad(i\in N).
\tag{1}
\]

BCFF Definition 2.6 supplies an incoming `f`-champion for every allocated
bundle; Definitions 3.1--3.4 and Lemma 3.5 convert every PI cycle into a
Pareto-improving EFX allocation.  Such a cycle is impossible at a globally
lexicographically maximal state.

The earlier restart memo cited three local reduction files that do not exist
in the repository history.  Consequently this note does not treat their
claimed one-large and length-two conclusions as established inputs.  The
present theorem is conditional only on the explicit length-three normal form
below until a separate composition proof derives that form from BCFF.

## Length-three normal form

Use agents `(p,r,q,s)` and write

\[
X_p=\{x\},\qquad
X_r=T_r\mathbin{\dot\cup}B_r,\qquad
X_q=T_q\mathbin{\dot\cup}B_q,\qquad
X_s=\{y\}.
\]

The length-three mixed basic cycle is

\[
p\xrightarrow f r\xrightarrow f q\longrightarrow p,
\tag{2}
\]

where the first two edges are genuine champion edges and the last is the
envy edge `q -> p`.  Select the desired bundles

\[
D_p=T_r+f,\qquad D_r=T_q+f.
\tag{3}
\]

Both are common-safe at the base.  In particular each of `T_r,T_q` is
common-safe in total.  Since the base is EFX and the complementary packets
are nonempty, each of `B_r,B_q` is also common-safe in total.

Global maximality also excludes every self-`f`-champion.  Applying BCFF
Observation 2.10 to the selected decompositions gives

\[
v_r(T_r+f)<b_r,\qquad v_q(T_q+f)<b_q.
\]

Since `D_r=T_q+f` is desired by `r`, the first inequality implies

\[
v_r(f)<v_r(B_r),\qquad v_r(T_q)>v_r(T_r).
\]

Thus the mixed pool `B_r+T_q` strictly improves `r` over `X_r`.  Likewise,
absence of the internal chord `p -> q` and BCFF Observation 2.10 give
`v_p(T_q+f)<b_p<v_p(T_r+f)`, hence `v_p(T_r)>v_p(T_q)`.  These inequalities
are cap-free and are part of the real normal form; the atomic cores use them
implicitly.

The singleton owner `s` is external to (2), but its incoming basic edge
cannot be omitted.

> **Singleton-absorption lemma.** Every singleton bundle in a globally
> maximal one-charity partial EFX allocation is envied.

Indeed, suppose `X_j={z}` is unenvied.  Give `f` to `j`.  After deleting
`f`, every observer sees `{z}`, which is below her base by assumption.  After
deleting `z`, every observer sees `{f}`, which is below her base by (1).
Thus the new allocation is EFX and Pareto improves `j`, a contradiction.

Hence some `a in {p,r,q}` envies `y`.  The length-three residual has three
external-source types:

\[
a=p,\qquad a=r,\qquad a=q.
\tag{4}
\]

This correction is essential.  Modeling `s` as unenvied makes the structural
cell inconsistent, because `s` is then a self-`f`-champion and can absorb
the charity good.

## Cap-free easy-priority lemma

Every allocation giving each agent at most one good is EFX.  Therefore the
following priority types cannot be globally maximal:

1. the first-priority agent is `q`: give `q` the envied singleton `x`;
2. the first-priority agent is `a`: give `a` the envied singleton `y`;
3. the order begins `(p,a)` with `a != p`: keep `p={x}` and give `a={y}`;
4. the order begins `(s,q)`: keep `s={y}` and give `q={x}`;
5. if `a=p`, every order beginning with `p` is closed by giving `p={y}`.

Give the remaining agents distinct goods chosen from `f` and the two large
bundles, and leave all other goods unallocated.  Earlier priority utilities
are fixed where required, and the displayed envier strictly improves.

The orders not covered by this lemma are:

| source of `a -> s` | remaining priority orders |
|---|---|
| `a=p` | the six `r`-first orders; `(s,p,r,q)`, `(s,p,q,r)`, `(s,r,p,q)`, `(s,r,q,p)` |
| `a=r` | `(p,q,r,s)`, `(p,q,s,r)`, `(p,s,r,q)`, `(p,s,q,r)`, `(s,p,r,q)`, `(s,p,q,r)`, `(s,r,p,q)`, `(s,r,q,p)` |
| `a=q` | the six `r`-first orders; `(p,r,q,s)`, `(p,r,s,q)`, `(p,s,r,q)`, `(p,s,q,r)`, `(s,p,r,q)`, `(s,p,q,r)`, `(s,r,p,q)`, `(s,r,q,p)` |

Repeated appearances are intentional: the topology source changes which
singleton transfer is available.

## Reservoir structure already inherited analytically

Put

\[
W=X_q+B_r.
\]

The sets `D_p` and `W` are disjoint, `q` values `W` strictly above her base,
and `q` envies `x`.  Therefore the minimal-threshold proof of the alternating
dual-reservoir trichotomy applies verbatim whenever no subset of `W` is
desired by `r` or `s`.  It yields one of:

1. a same-offer promotion of `p` paid from `W`;
2. an anchored desired `q`-handoff paid by `D_p`; or
3. an opposite-reservoir desired promotion of `p`.

No alternating second champion edge is used in that proof.  The only new
source wall is therefore a desired set in `W` sourced by the external
singleton `s`.  A desired `r`-set in `W`, disjoint from `D_p,x,y`, combines
with `(D_p,A,x,y)` to give an EFX Pareto improvement and is impossible at
global maximality.

The remaining analytic task is to reroute an `s`-desired set in `W`, or to
use its failure inequalities to construct a coupled cross-reservoir escape.
This is the cap-free packet-safety gate; proving more fixed-size cells would
not close it.

## A cap-free three-promotion/payment lemma

The external-source type `a=p` admits a further packet-safe reduction.  Put

\[
t=\tau_s(D_r)=\tau_s(T_q+f).
\]

Exactly one of the following constructions applies.

1. If `v_s(X_r)>=t`, choose an inclusion-minimal `C subseteq X_r` with
   `v_s(C)>=t` and set

   \[
   (Y_p,Y_r,Y_q,Y_s)=(\{y\},D_r,\{x\},C).
   \tag{5}
   \]

2. If `v_s(X_r)<t`, set

   \[
   (Y_p,Y_r,Y_q,Y_s)=(\{y\},X_r,\{x\},D_r).
   \tag{6}
   \]

Both allocations are EFX for arbitrary packet sizes.  For (5), minimality
gives `tau_s(C)<t`, while `p` and `q` do not envy `X_r` and `r` values
`X_r` at her base.  Hence `C` lies below the new utilities of `p,r,q`, and
`s(C)>=tau_s(D_r)` is the only nontrivial comparison made by `s`.  The
bundles `D_r`, `x`, and `y` are common-safe or singletons.  For (6), agents
`p,q` improve and `r` keeps her base bundle.  The only agent below base can
be `s`, and

\[
v_s(D_r)\ge\tau_s(D_r)>v_s(X_r)\ge\tau_s(X_r),
\]

so her only nonsingleton comparison is safe.

In (5), `p,r,q` all strictly improve, so every order not beginning with `s`
is closed.  In (6), `p,q` improve and `r` is fixed.  It closes every order
in which `p` or `q` occurs before `s` after an optional initial `r`.
Combined with the easy-priority lemma, source type `a=p` is therefore reduced
to the six orders beginning with `s` or with `(r,s)`.  The residual failure
has a concrete meaning: `s` must be preserved before either singleton
transfer can be used, or must be paid from the mixed remainder `X_r+B_q`
rather than from `X_r` alone.

The same argument, with a different desired block, closes most of source
type `a=r`.  Put `u=tau_s(D_p)`.  If `v_s(X_q)>=u`, take a minimal
`C subseteq X_q` at the `s` threshold and use

\[
(Y_p,Y_r,Y_q,Y_s)=(D_p,\{y\},\{x\},C).
\tag{7}
\]

If `v_s(X_q)<u`, use

\[
(Y_p,Y_r,Y_q,Y_s)=(\{x\},\{y\},X_q,D_p).
\tag{8}
\]

For (7), `p,r,q` improve and `C subseteq X_q` lies below each of their new
utilities: `p,r` do not envy `X_q`, while `q(x)>b_q`.  For (8), `p,q` are
fixed, `r` improves, and the low inequality gives
`v_s(D_p)>tau_s(X_q)`.  Thus both are EFX cap-free.  In the low branch an
order is closed whenever `r` occurs before `s` after an optional prefix of
the fixed agents `p,q`; together with the easy lemma only the seven hard
`a=r` orders in which `s` precedes `r` remain.

## Exact atomic motif audit

For discovery only, the proper-decomposition atom has goods
`(tr,br,tq,bq,x,y,f)`.  The exact structural encoding includes (2), the
external envy source (4), strict EFX, charity dominance, and absence of all
other basic champion chords.  Every one of the `3*24=72` source/order cells
is QF_LRA-UNSAT after exact enumeration of all `5^7=78,125` partial
allocations.  Deletion-minimal rival menus have size at most three.

The recurring coupled motifs assign `x` to `q`, use `D_p` or transfer `y`
to its envier, and repartition `T_r,B_r,T_q` between the two remaining
agents.  Their atomic EFX safety relies on singleton packets and is not a
packet theorem.

## Completion requirements

The target is complete only after all of the following are proved:

1. cap-free closure of the external `s`-source wall for every remaining
   priority order;
2. treatment of empty top/bottom packets rather than assuming proper
   decompositions silently;
3. derivation of the exact length-three normal form from the BCFF
   globally-maximal state, including disposal of extra envy/champion edges;
4. a nonnegative/tie wrapper replacing the temporary positive,
   nondegenerate convention; and
5. an explicit statement of what the result proves inside the
   exactly-two-nonsingleton reduction and what cases remain outside it.

Until these items are discharged, neither the exactly-two-nonsingleton
closure nor complete four-agent additive EFX is claimed.

## Primary source

Berger, Cohen, Feldman, and Fiat, *Almost Full EFX Exists for Four Agents
(and Beyond)*, Definitions 2.3 and 2.6--2.7, Definitions 3.1--3.4, and
Lemma 3.5, [arXiv:2102.10654](https://arxiv.org/abs/2102.10654).

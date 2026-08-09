# Adjacent-large global-lex target

**Date:** 2026-08-09  
**Status:** every `q`-, `s`-, and `r`-first order closed cap-free; `p`-first
residual contracted to a contested-`T_r` quota wall

## Structural normal form

Up to relabeling, let

\[
X_p=\{x\},\qquad X_r=T_r\mathbin{\dot\cup}B_r,\qquad
X_s=\{y\},\qquad X_q=T_q\mathbin{\dot\cup}B_q
\]

and let `f` be the one charity good.  The adjacent-large basic cycle is

\[
p\xrightarrow f r\xrightarrow f q\longrightarrow s\longrightarrow p.
\tag{1}
\]

Write `b_i=v_i(X_i)`,

\[
D_p=T_r+f,\qquad D_r=T_q+f,
\]

and

\[
\tau_i(Z)=\max_{g\in Z}v_i(Z-g).
\]

The selected desired sets are `D_p` for `p`, `D_r` for `r`, `{y}` for
`q`, and `{x}` for `s`.  Thus all four sets are common-safe at the base,
and their respective sources strictly prefer them to their base bundles.

The target is unrestricted.  A rival may cross either reservoir, change
the root, repartition packets, or use a bundle whose safety is visible only
at the new allocation.

## Easy first priorities

If `s` is first, give `s` the singleton `{x}` and discard every other good.
If `q` is first, give `q` `{y}` and discard every other good.  A singleton-
only allocation is EFX, and the corresponding envy edge makes it a strict
lexicographic improvement.  Hence all twelve orders beginning in `q` or `s`
are closed cap-free.

## Mirrored reservoir extraction

Put

\[
W=B_r+X_q,\qquad U=X_r+B_q.
\]

The following minimal-crossing argument is used twice.

> **Reservoir extraction lemma.** Let `D` be common-safe and let `t=tau_j(D)`.
> Suppose a pool `P`, disjoint from `D`, contains a desired set.  Then either
> there is a common-safe `R subseteq P` with `v_j(R)>=t`, or there is a
> desired `A subseteq P` with `v_j(A)<t`.

If `v_j(P)<t`, take an inclusion-minimal desired subset of `P`.  Otherwise
take an inclusion-minimal `R subseteq P` with `v_j(R)>=t`.  If `R` is not
common-safe, some deletion `R-h` crosses an observer's base utility.  A
minimal crossing subset `A subseteq R-h` is desired and, by minimality of
`R`, satisfies `v_j(A)<t`.  This proof uses no packet-size bound.

The premise holds for both reservoirs: positivity gives

\[
v_q(W)>b_q,\qquad v_r(U)>b_r,
\]

and a minimal subset on which any observer crosses is desired.

## Cap-free closure of every `r`-first order

Apply reservoir extraction to `D_r`, recipient `p`, and pool `U`.

If a common-safe `P subseteq U` satisfies

\[
v_p(P)\ge\tau_p(D_r),
\tag{2}
\]

then

\[
(Y_p,Y_r,Y_s,Y_q)=(P,D_r,\{x\},\{y\})
\tag{3}
\]

is EFX.  Agent `r` strictly improves, so (3) improves every order beginning
with `r`.

Otherwise extraction gives a desired `B subseteq U` with

\[
v_p(B)<\tau_p(D_r).
\tag{4}
\]

The basic edge `r -f-> q` releases `B_q`.  A generalized edge into `r`
using any incoming subset of `B_q` is PI-compatible when its source is
`q`, `s`, or `p`:

\[
r\xrightarrow f q\xrightarrow{B_q}r,qquad
r\xrightarrow f q\longrightarrow s\xrightarrow{B_q}r,qquad
r\xrightarrow f q\longrightarrow s\longrightarrow p
 \xrightarrow{B_q}r.
\tag{5}
\]

The incoming set in (5) is released by the first edge, and is disjoint from
`f`; hence each displayed cycle is PI in the sense of BCFF Definition 3.4.
At a PI-free globally maximal state, no desired subset of `U` can therefore
be sourced by `p`, `q`, or `s`.  The extracted `B` is sourced by `r`.

Now use

\[
(Y_p,Y_r,Y_s,Y_q)=(D_r,B,\{x\},\{y\}).
\tag{6}
\]

The sets `D_r` and `B` are disjoint and common-safe.  Agent `r` improves on
`B`; agents `s,q` improve on their envied singletons.  Agent `p` may be
below base, but (4) and positivity give

\[
v_p(D_r)>\tau_p(D_r)>v_p(B)\ge\tau_p(B),
\]

which is its only comparison between nonsingleton new bundles.  Thus (6) is
EFX and improves the first coordinate `r`.  This proves:

> **Theorem 1 (adjacent `r`-first escape).** No PI-free adjacent-large state
> is globally lexicographically maximal in an order beginning with `r`, for
> arbitrary packet sizes.

Together with the easy singleton cases, eighteen of the twenty-four orders
are closed analytically.

## `p`-first source wall

Apply reservoir extraction to `D_p`, recipient `r`, and pool `W`.  If a
common-safe `R subseteq W` satisfies

\[
v_r(R)\ge\tau_r(D_p),
\tag{7}
\]

then

\[
(Y_p,Y_r,Y_s,Y_q)=(D_p,R,\{x\},\{y\})
\tag{8}
\]

is EFX and improves `p`, closing every `p`-first order.

If (7) fails, extraction gives a desired `A subseteq W` with

\[
v_r(A)<\tau_r(D_p)\le b_r.
\tag{9}
\]

Thus `A` cannot be sourced by `r`.  If it is sourced by `p`, then

\[
(A,D_p,\{x\},\{y\})
\tag{10}
\]

is EFX: positivity and (9) give
`v_r(D_p)>tau_r(D_p)>v_r(A)>=tau_r(A)`.  Allocation (10) improves `p`.
Consequently every unresolved `p`-first state has `A` sourced by `q` or
`s`.

This distinction also closes several orders.  If `A` is sourced by `q`,

\[
(Y_p,Y_r,Y_s,Y_q)=(\{x\},D_p,\{y\},A)
\tag{11}
\]

is EFX and closes every `p`-first order in which `q` precedes `r`.  If `A`
is sourced by `s`,

\[
(Y_p,Y_r,Y_s,Y_q)=(\{x\},D_p,A,\{y\})
\tag{12}
\]

is EFX and closes every order in which either `s` or `q` precedes `r`.
The same inequality (9) checks `r` against `A`; all other nonsingleton
comparisons follow from common safety.

Hence the remaining priority/source types are:

| source of `A` | orders not closed by (8)--(12) |
|---|---|
| `q` | `(p,r,s,q)`, `(p,r,q,s)`, `(p,s,r,q)` |
| `s` | `(p,r,s,q)`, `(p,r,q,s)` |

## Contested-top contraction

Independently choose an inclusion-minimal desired set `B subseteq U`.
The compatible cycles (5) force its source to be `r`.  Since `D_p` is
desired by `p`, disjointness of `B` and `D_p` would make

\[
(D_p,B,\{x\},\{y\})
\]

an EFX Pareto improvement.  Therefore every unresolved globally maximal
state satisfies

\[
H=B\cap D_p=B\cap T_r\ne\varnothing.
\tag{13}
\]

Put

\[
\delta_p=b_p-v_p(D_p\setminus H),\qquad
\delta_r=b_r-v_r(B\setminus H).
\]

If `H` had a partition `H=H_p dotcup H_r` with

\[
v_p(H_p)>\delta_p,\qquad v_r(H_r)>\delta_r,
\tag{14}
\]

then the disjoint sets

\[
D'_p=(D_p\setminus H)+H_p,qquad
B'=(B\setminus H)+H_r
\]

would remain common-safe by downward closure and would be desired by `p`
and `r`, respectively.  Together with `{x}` for `s` and `{y}` for `q`,
they would give an EFX Pareto improvement.  Thus every unresolved state
obeys the exact two-demand quota obstruction

\[
\boxed{\quad
\text{for every }J\subseteq H,\quad
v_p(J)\le\delta_p\ \text{or}\
v_r(H\setminus J)\le\delta_r.
\quad}
\tag{15}
\]

Equations (9), (13), and (15) are the promised cap-free contraction.  The
adjacent-large problem is no longer an unrestricted allocation enumeration:
it is a contested subset of `T_r`, coupled to a low `q`- or `s`-sourced
payment wall in `B_r+X_q`.  This is the same two-demand quota/payment object
that remains in the length-three residue, with the source roles rotated.

> **Theorem 2 (adjacent source-wall contraction).** Any PI-free adjacent-
> large state globally maximal in one of the five displayed `p`-first
> source/order types induces the quota witness (15) and the low wall (9).
> Conversely, failure to induce either object gives one of the explicit EFX
> lexicographic improvements (8)--(12).

Theorem 2 is a reduction, not yet a proof that the five types cannot occur.
Closing (15) against (9), or producing an exact unrestricted profile in one
of those types, remains the final adjacent-large gate.

## Corrected exact diagnostics

The strict structural encoding must not treat the identity candidate
`X_source` as a degeneracy tie.  It is skipped when excluding absent desired
relations.  After that correction:

- all 24 seven-good atomic orders remain exact QF_LRA-UNSAT;
- 22 orders have one-rival cores, the maximum core size is three, and the
  total order-specific menu has 27 rivals;
- for the hard atomic order `(s,r,p,q)`, splitting any one of
  `T_r,B_r,T_q,B_q` still gives exact UNSAT, with deletion-minimal core sizes
  `1,7,11,1`, respectively;
- the full binary selected-`p` completion statement is false in a strict,
  subset-nondegenerate profile, while the opposite selected `r` root and all
  24 unrestricted priority orders still escape;
- the mirrored direct-payment dichotomy is false in another strict binary
  profile, while all 24 unrestricted orders again escape with minimum
  repairs changing two to four goods.

The last counterprofile has only `s`-sourced minimal desired sets in `U`.
It therefore contains the compatible middle cycle
`r -f-> q -> s -(B_q)-> r` from (5) and is correctly excluded from the
PI-free branch of Theorem 1.  The finite refutation does not refute the
analytic theorem.

The 162- and 174-escape profiles remain essential move-completeness tests.
They show that a final proof cannot require the promoted bundle to lie in
the original champion offer, cannot insist on an anchored root, and cannot
test safety only against old base utilities.  The constructions above use
only those restrictions when deriving a contradiction; Theorem 2's final
gate explicitly permits cross-face and endogenous reallocations.

## Trust boundary and next gate

Theorem 1 and the contraction in Theorem 2 are analytic and independent of
packet sizes.  The exact computations corroborate them but are not premises
of their proofs.  Neither theorem proves complete four-agent EFX.

Completion of the active target requires one of:

1. an uncrossing argument showing that (9) and (15) force a cross-face,
   root-flip, endogenous, or length-three-contraction escape in all five
   remaining types; or
2. a strict exact profile with no unrestricted EFX lexicographic improvement
   in one of those types.

Primary source: Berger, Cohen, Feldman, and Fiat, *Almost Full EFX Exists
for Four Agents (and Beyond)*, Definitions 3.1--3.4 and Lemma 3.5,
[arXiv:2102.10654](https://arxiv.org/abs/2102.10654).

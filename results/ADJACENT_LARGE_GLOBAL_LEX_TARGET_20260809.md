# Adjacent-large global-lex target

**Date:** 2026-08-09  
**Status:** all 24 priority orders closed analytically for arbitrary packet
sizes; adjacent-large global-lex escape lemma proved

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

## Standing hypotheses

*Referee repair 2026-08-16* (gap G1 of the referee report
`TWO_NONSINGLETON_COMPOSITION_REFEREE_REPORT_20260816.md`, currently on
`codex/efx-breakthrough-next-20260802`).  Theorems 1--3 below are stated for
a PI-free adjacent-large state satisfying, in addition to the normal form
above:

- **strictly positive valuations**, and
- **nonempty packets `T_r`, `B_r`, `T_q`, `B_q`** (top-packet nonemptiness
  is discharged by part (b) of the composition's Packet nondegeneracy
  section, via charity dominance; it does not follow from `B_r,B_q` being
  nonempty).

These were used silently and are load-bearing: `v_r(U)=b_r+v_r(B_q)>b_r` in
Theorem 1 and in the second extraction branch of Theorem 3 needs `B_q`
nonempty and positive, and `v_q(W)=b_q+v_q(B_r)>b_q` behind the `p`-first
escapes (11)--(12) needs `B_r` nonempty and positive.  Both are supplied by
the reservoir-extraction premise "the pool contains a desired set", which
fails outright for an empty bottom packet.

In the two-nonsingleton composition neither hypothesis is assumed: positivity
comes from the nondegeneracy of the BCFF Lemma A.1 respecting witness
together with the paper's standing monotonicity — *not* from A.1 alone, see
"Nonnegative values and ties" below — and the nonempty packets are discharged
once for all four cycle
classes by the "Packet nondegeneracy" section of
[`TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md`](TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md)
— an empty bottom makes the owner a self-`f`-champion whose `f`-absorption is
an EFX lexicographic improvement in every order, and an empty top makes the
selected desired set `{f}`, excluded by charity dominance.  The premise
bookkeeping is tabulated in
[`ADJACENT_BCFF_COMPOSITION_AUDIT.md`](ADJACENT_BCFF_COMPOSITION_AUDIT.md).

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
> satisfying the standing hypotheses (positive valuations, `B_r,B_q`
> nonempty) is globally lexicographically maximal in an order beginning with
> `r`, for arbitrary packet sizes.

*Referee repair 2026-08-16:* the standing hypotheses are discharged by the
composition, not assumed by it.

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

Theorem 2 was the intermediate contraction that isolated the five hard
types.  The next theorem closes them without having to solve the quota wall
directly.

## Endogenous safe-repartition closure

The minimum escapes from the binary payment counterprofiles reveal a useful
cap-free family that is broader than an anchored handoff or a one-way packet
transfer.  Put

\[
P=X_r+X_q+f.
\]

> **Safe-repartition lemma.** Suppose disjoint sets `R,Q subseteq P` satisfy
>
> 1. `R` is desired by `r`;
> 2. `Q` is common-safe at the base; and
> 3. `v_q(Q)>=tau_q(R)`.
>
> Then
> \[
> (Y_p,Y_r,Y_s,Y_q)=(\{x\},R,\{y\},Q)
> \tag{16}
> \]
> is EFX.  It closes all five remaining priority/source types.

Indeed, common safety of `R` checks every observer other than possibly `q`,
whose comparison is exactly condition 3.  Common safety of `Q` checks
`p,r,s`, while `q`'s comparison with its own bundle is automatic.  The two
singleton bundles impose no nonzero deletion comparison.  Agents `p,s`
keep their base utilities and `r` strictly improves, so (16) is a strict
lexicographic improvement whether `r` is second or follows the fixed `s`.
This proof permits arbitrary repartition and discard inside `P`; neither
bundle must be an old offer or be safe only by reference to the old
recipient.

> **Theorem 3 (adjacent `p`-first escape).** No PI-free adjacent-large state
> satisfying the standing hypotheses (positive valuations, `B_r,B_q`
> nonempty) is globally lexicographically maximal in any of the five
> remaining `p`-first priority/source types, for arbitrary packet sizes.

*Referee repair 2026-08-16:* the standing hypotheses are discharged by the
composition, not assumed by it.

Apply the reservoir extraction lemma to the common-safe set `D_r`, recipient
`q`, and pool

\[
U=X_r+B_q.
\]

The sets `D_r=T_q+f` and `U` are disjoint.  Moreover `U` contains a desired
set: positivity gives `v_r(U)>b_r`, so an inclusion-minimal subset of `U`
that crosses some agent's base is desired.

In the first extraction branch there is a common-safe `Q subseteq U` with

\[
v_q(Q)\ge\tau_q(D_r).
\tag{17}
\]

Take `R=D_r` in (16).  It is desired by `r`, and (17) is exactly the payment
condition, so the safe-repartition lemma gives the required escape.

In the second extraction branch there is a desired `A subseteq U` with

\[
v_q(A)<\tau_q(D_r).
\tag{18}
\]

The three compatible cycles in (5) exclude `p`, `q`, and `s` as sources of
any desired subset of `U`; hence `A` is desired by `r`.  Now take `R=A` and
`Q=D_r` in (16).  Positivity and (18) give

\[
v_q(D_r)>\tau_q(D_r)>v_q(A)>\tau_q(A),
\tag{19}
\]

so `D_r` pays `q`'s EFX threshold for `A`.  The safe-repartition lemma again
gives an EFX allocation fixing `p,s` and strictly improving `r`.  The two
extraction branches are exhaustive, proving the theorem.

This is the same minimal-threshold mechanism as the independently audited
[`ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md`](ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md),
but the adjacent cycle has the stronger source wall (5): its low reversal
must be sourced by `r`, exactly the recipient needed in (16).

Combining Theorem 3 with the twelve singleton-first escapes and Theorem 1
closes all twenty-four priority orders.  Thus the adjacent-large length-four
residual cannot occur at a PI-free globally lexicographically maximal
one-charity state.

The argument does not assume that an unrestricted escape is anchored or
uses an original offer.  It searches the full logical space and proves that
one of the two displayed safe repartitions exists; in the second branch the
promoted `r` bundle is an arbitrary extracted desired subset of `U`.  The
common safety of the constructed bundles is a conclusion of extraction,
not a restriction placed on possible rival allocations.

## Nonnegative values and ties

The structural proof is run in a nondegenerate positive profile respecting
every strict comparison of the original instance.  Positivity is used only
for `v_r(U)>b_r` and for the strict total-versus-deletion inequalities in
(19); nondegeneracy makes the selected envy/champion relations strict.

*BCFF-audit repair 2026-08-16* (the single drift found by
[`BCFF_IMPORT_AUDIT_20260816.md`](BCFF_IMPORT_AUDIT_20260816.md); provenance,
not mathematics).  This paragraph previously read "BCFF Lemma A.1 supplies an
additive perturbation".  It does not.  What A.1 supplies is a **nondegenerate
cancelable** respecting witness `v'` together with the one-directional
transfer `EFX(v') => EFX(v)`.  Three corrections follow.

1. The *additive* respecting nondegenerate perturbation this proof is run in
   does exist and is standard, but it is folklore (Chaudhury et al.), **not**
   BCFF Lemma A.1.
2. A.1 says nothing about **positivity**.  The positivity used above is A.1's
   nondegeneracy together with the paper's standing monotonicity assumption,
   and should be cited that way.
3. The transfer is one-directional and carries back **only the final EFX
   allocation** — not global lexicographic maximality, not the one-charity
   normal form, not the selected champion graph.  Those are defined inside
   the perturbed profile, which is exactly what makes the argument sound; the
   correct in-corpus statement is `ONE_LARGE_CHAMPION_CLOSURE_REDUCTION.md`,
   lines 276--281 (that file is on `codex/efx-breakthrough-next-20260802`).
   Extending this normal form verbatim to tied nonnegative profiles would
   need an explicit state-preserving tie wrapper, which is not claimed here.

If the surrounding composition produces a complete EFX allocation in the
perturbed instance, it is EFX for the original valuations: an original
strict EFX violation would remain strict under a respecting perturbation.
That one-directional transfer is exactly what A.1 licenses.  Thus zero item
values and ties do not create an additional adjacent-large packet case.  This
wrapper does not upgrade the present cycle-class theorem to complete
four-agent EFX; that still requires the composition described below.

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
- the broad safe-repartition gate is exact UNSAT in the atom, every
  one-packet split, and the full binary cell.  The pure binary solver core
  uses 28 repartition rivals and no direct-payment premise.  The repartition
  ranges over all disjoint `R,Q` in
  `X_r+X_q+f`, permits discards, requires `R` desired by `r`, and requires
  only endogenous common safety plus `v_q(Q)>=tau_q(R)`.  These fixed-cell
  results are diagnostics; Theorem 3 supplies the independent arbitrary-
  packet proof.  A larger `(3,2,2,2)` pure-gate replay was deliberately
  retired without a decision; no cap-free claim depends on scaling the
  encoding.

The mirrored-payment counterprofile has only `s`-sourced minimal desired
sets in `U`.  It therefore contains the compatible middle cycle
`r -f-> q -> s -(B_q)-> r` from (5) and is correctly excluded from the
PI-free branch of Theorem 1.  The finite refutation does not refute the
analytic theorem.

The 162- and 174-escape profiles remain essential move-completeness tests.
They belong to the alternating topology, not the adjacent normal form, and
therefore do not contradict Theorem 3.  Their lesson is nevertheless built
into its formulation: the safe-repartition family permits cross-face,
opposite-reservoir, discarded, and endogenous bundles, and the second
extraction branch promotes an arbitrary desired subset rather than a subset
of the original champion offer.  The theorem concludes that a particularly
simple witness exists from the adjacent PI-cycle structure; it does not
assume that narrower witness as a premise.

Concretely, the 162 profile is frozen in
[`alternating_variable_extension_1121_refutation_audit.json`](alternating_variable_extension_1121_refutation_audit.json),
and the 174 profiles in
[`alternating_psqr_unrestricted_refutation_audit.json`](alternating_psqr_unrestricted_refutation_audit.json).
The first refutes “anchored or original-offer promotion”; the second refutes
“anchored or any base-desired root.”  Theorem 3 asserts neither dichotomy.
Its extraction ranges over every desired subset of `U`, and its validity
comes from the three adjacent PI-compatible source exclusions in (5), which
those alternating profiles do not satisfy in the adjacent labeling.

## Trust boundary and composition gate

Theorems 1--3 are analytic and independent of packet sizes.  The exact
computations corroborate them but are not premises of their proofs.  The
result proves the cap-free global-lex escape lemma for the adjacent-large
length-four residual topology.  It does **not** by itself prove complete
four-agent EFX.

The next program-level gate is composition: combine this adjacent theorem
with independently verified length-two, length-three, and alternating
cycle-class theorems, and verify that the exactly-two-nonsingleton BCFF
reduction reaches one of those classes without an unstated graph or
decomposition assumption.

Shortest exact replay from the repository root (with `z3-solver` installed):

```bash
PYTHONPATH=tracks/parkability python3 tracks/parkability/audit_adjacent_large_safe_repartition_cells.py --output /tmp/adjacent-safe-repartition-audit.json
```

Primary source: Berger, Cohen, Feldman, and Fiat, *Almost Full EFX Exists
for Four Agents (and Beyond)*, Definitions 3.1--3.4 and Lemma 3.5,
[arXiv:2102.10654](https://arxiv.org/abs/2102.10654).

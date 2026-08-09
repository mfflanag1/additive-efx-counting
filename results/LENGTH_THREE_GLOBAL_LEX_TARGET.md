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

No alternating second champion edge is used in that proof.  Unlike the
alternating application, however, the length-three topology need not assume
that `r`- and `s`-sourced desired subsets of `W` are absent.  The next lemma
closes both sources explicitly.

## All-source reservoir return lemma

Put `t=tau_r(D_p)`.  The threshold extraction in `W=X_q+B_r` has the
following cap-free outputs.

1. If `v_r(W)>=t`, choose an inclusion-minimal `Q subseteq W` at the
   `r` threshold.  If `Q` is common-safe, then

   \[
   (Y_p,Y_r,Y_q,Y_s)=(D_p,Q,\{x\},\{y\})
   \tag{5}
   \]

   is EFX.
2. Otherwise—either `v_r(W)<t`, or a deletion of the minimal `Q` is
   unsafe—there is a desired `A subseteq W` satisfying

   \[
   \tau_r(A)<t\le v_r(D_p).
   \tag{6}
   \]

   The source of `A` determines an EFX allocation:

   | source of `A` | `(Y_p,Y_r,Y_q,Y_s)` |
   |---|---|
   | `r` | `(D_p,A,{x},{y})` |
   | `p` | `(A,D_p,{x},{y})` |
   | `q` | `({x},D_p,A,{y})` |
   | `s`, with `a=p` | `({y},D_p,{x},A)` |
   | `s`, with `a=r` | `(D_p,{y},{x},A)` |
   | `s`, with `a=q` | `({x},D_p,{y},A)` |

For the first three rows this is the dual-reservoir proof without excluding
sources.  In the `s` rows, assign the envied singleton `y` to its source `a`.
If `a=p` or `a=q`, `r` receives `D_p` and inequality (6) is exactly her sole
nontrivial comparison.  If `a=r`, every recipient receives a desired or
base bundle and strictly improves except possibly none.  All displayed
bundles are disjoint and common-safe at the base, apart from the recipient
payment whose comparison is supplied by (6).

Thus the former external-`s` source wall is closed.  The only output that
can move `r` downward while fixing `p,s` is the `q`-source handoff
`({x},D_p,A,{y})`.  It lexicographically closes every priority type in which
`q` precedes `r` after the fixed agents, but requires a second operation when
`r` has earlier priority.  This is the exact remaining reservoir-order wall.

## Rotated all-source reservoir lemma: all `r`-first orders

Every priority order beginning with `r` is also closed cap-free.  If `a=r`,
this is already the easy singleton transfer `r <- y`.  Assume therefore
`a in {p,q}` and put

\[
U=X_r+B_q,qquad t'=\tau_p(D_r).
\]

The sets `U` and `D_r` are disjoint, and
`v_r(U)=b_r+v_r(B_q)>b_r`, so `U` contains a desired set.  Repeat the
threshold extraction, now at the `p` threshold.

If `v_p(U)>=t'`, choose an inclusion-minimal `Q subseteq U` at that
threshold.  When `Q` is common-safe,

\[
(Y_p,Y_r,Y_q,Y_s)=(Q,D_r,\{x\},\{y\})
\tag{7}
\]

is EFX and strictly improves `r`.  Otherwise—also covering
`v_p(U)<t'`—extract a desired `A subseteq U` with

\[
\tau_p(A)<t'\le v_p(D_r).
\tag{8}
\]

Use the following allocation according to the source of `A`:

| source of `A` | `(Y_p,Y_r,Y_q,Y_s)` |
|---|---|
| `p` | `(A,D_r,{x},{y})` |
| `r` | `(D_r,A,{x},{y})` |
| `q` | `({x},D_r,A,{y})` |
| `s`, with `a=p` | `({y},D_r,{x},A)` |
| `s`, with `a=q` | `({x},D_r,{y},A)` |

In the `r` row, `p` is the sole possibly sub-base recipient and (8) is
exactly her comparison to `A`.  Every other row gives each non-base
recipient a desired bundle, with (8) available whenever `D_r` is used as
the `p` payment.  In all rows `r` receives a desired set and strictly
improves.  Therefore every `r`-first priority order is contradicted,
independently of all later priorities and without a packet-size bound.

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
   \tag{9}
   \]

2. If `v_s(X_r)<t`, set

   \[
   (Y_p,Y_r,Y_q,Y_s)=(\{y\},X_r,\{x\},D_r).
   \tag{10}
   \]

Both allocations are EFX for arbitrary packet sizes.  For (9), minimality
gives `tau_s(C)<t`, while `p` and `q` do not envy `X_r` and `r` values
`X_r` at her base.  Hence `C` lies below the new utilities of `p,r,q`, and
`s(C)>=tau_s(D_r)` is the only nontrivial comparison made by `s`.  The
bundles `D_r`, `x`, and `y` are common-safe or singletons.  For (10), agents
`p,q` improve and `r` keeps her base bundle.  The only agent below base can
be `s`, and

\[
v_s(D_r)\ge\tau_s(D_r)>v_s(X_r)\ge\tau_s(X_r),
\]

so her only nonsingleton comparison is safe.

In (9), `p,r,q` all strictly improve, so every order not beginning with `s`
is closed.  In (10), `p,q` improve and `r` is fixed.  It closes every order
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
\tag{11}
\]

If `v_s(X_q)<u`, use

\[
(Y_p,Y_r,Y_q,Y_s)=(\{x\},\{y\},X_q,D_p).
\tag{12}
\]

For (11), `p,r,q` improve and `C subseteq X_q` lies below each of their new
utilities: `p,r` do not envy `X_q`, while `q(x)>b_q`.  For (12), `p,q` are
fixed, `r` improves, and the low inequality gives
`v_s(D_p)>tau_s(X_q)`.  Thus both are EFX cap-free.  In the low branch an
order is closed whenever `r` occurs before `s` after an optional prefix of
the fixed agents `p,q`; together with the easy lemma only the seven hard
`a=r` orders in which `s` precedes `r` remain.

## Critical mixed-pool reduction

The hardest `p`-promotion motifs admit a sharper two-wall formulation.  Put

\[
R=B_r+T_q.
\]

The no-self and no-chord inequalities above imply

\[
v_r(R)>b_r,
\qquad
v_p(R)<v_p(D_p).
\tag{13}
\]

For the first inequality, `v_r(T_q)>v_r(T_r)`.  For the second, the selected
`p` edge and absence of `p -> q` give `v_p(T_r)>v_p(T_q)`, while
`p` not envying `X_r` together with `p(D_p)>b_p` gives
`v_p(f)>v_p(B_r)`.

Choose an inclusion-minimal `C subseteq R` with `v_r(C)>b_r`.  Then every
deletion of `C` is below `b_r`, and (13) gives

\[
\tau_p(C)<v_p(D_p).
\]

Consequently

\[
(Y_p,Y_r,Y_q,Y_s)=(D_p,C,\{x\},\{y\})
\tag{14}
\]

is EFX—and strictly improves `p,r,q`—if and only if the following two
moving-ceiling conditions hold:

\[
\tau_q(C)\le v_q(x),
\qquad
\tau_s(C)\le b_s.
\tag{15}
\]

All other comparisons follow from desired-set safety, minimality, (13), or
the singleton bundles.  Thus a failed `p` promotion has only two possible
packet walls:

1. a `q`-heavy deletion `C-h` with `v_q(C-h)>v_q(x)>b_q`; or
2. an external-`s`-heavy deletion `C-h` with `v_s(C-h)>b_s`.

Both walls lie strictly below `b_r` by minimality of `C`.  This asymmetry is
the prospective uncrossing currency: every obstruction is high for `q` or
`s` but low for the intended recipient `r`.  The atomic three-rival menus
are precisely the singleton-packet realizations of choosing which side of
this separation to return to `r`.

The reduction is cap-free, but it does not yet prove that either wall can
always be rerouted.  A valid completion must use the remaining goods
`T_r+B_q+f` and may use the coupled/off-offer promotions already permitted
by the alternating theorem.

## Exact remaining source/order table

Combining the easy-priority lemma, the all-source `W` return, and the rotated
`U` return leaves only nine source/order types:

| source of `a -> s` | priority orders not yet closed |
|---|---|
| `a=p` | `(s,p,r,q)` |
| `a=r` | `(p,s,r,q)`, `(s,p,r,q)`, `(s,r,p,q)`, `(s,r,q,p)` |
| `a=q` | `(p,r,q,s)`, `(p,r,s,q)`, `(p,s,r,q)`, `(s,p,r,q)` |

For `a=p` or `a=q`, the rotated theorem closes every order beginning with
`r` and every `(s,r,...)` order.  The `W` theorem closes every order in
which `q` precedes `r`.  For `a=r`, direct transfer of `y` closes `r`-first
and `(p,r,...)` orders, while the `W` theorem again closes `q` before `r`.

In every row above, a hypothetical failure forces the `W` extraction onto
its `q`-source handoff while `r` precedes `q`.  In the `(s,p,r,q)` column it
also forces the rotated `U` extraction away from its `p`, `q`, and `s`
desired-source outputs.  This paired `q`-source/`r`-source wall—not the
external singleton by itself—is the final cap-free uncrossing target.

## Desired-set transversal and quota uncrossing

The final wall has a forced intersection geometry.  Let `A subseteq W` be
desired by `q`.  Since `D_r=T_q+f` is desired by `r`, disjointness would make

\[
(Y_p,Y_r,Y_q,Y_s)=(\{x\},D_r,A,\{y\})
\]

an EFX Pareto improvement.  Hence global maximality forces

\[
A\cap D_r=A\cap T_q\ne\varnothing.
\tag{16}
\]

Symmetrically, every `r`-desired `B subseteq U=X_r+B_q` must meet
`D_p`, and therefore $B\cap T_r$ is nonempty.  Thus the two reservoir
source walls are trapped on the corresponding top packets, not on arbitrary
goods.

There is a sharper exact uncrossing criterion.  Let `A` be desired by `q`
and `B` desired by `r`, put $H=A\cap B$, and define the strict additive
deficits

\[
\delta_q=b_q-v_q(A\setminus H),
\qquad
\delta_r=b_r-v_r(B\setminus H).
\]

If `H` has a partition $H=H_q\mathbin{\dot\cup}H_r$ satisfying

\[
v_q(H_q)>\delta_q,
\qquad
v_r(H_r)>\delta_r,
\tag{17}
\]

then

\[
A'=(A\setminus H)+H_q,qquad
B'=(B\setminus H)+H_r
\]

are disjoint desired bundles for `q` and `r`.  They remain common-safe by
downward closure, and `({x},B',A',{y})` is an EFX Pareto improvement.  Hence
every obstruction must violate the two-demand partition condition (17).
Equivalently, for every `J subseteq H`, at least one of

\[
v_q(J)\le\delta_q,qquad
v_r(H\setminus J)\le\delta_r
\]

holds.  This is the precise contested-good Hall witness left by the paired
source wall.

For `B=D_r`, equation (16) puts `H subseteq T_q`.  Giving the whole top
packet to `r` and returning `q` to the envied singleton produces the atomic
fallback

\[
(D_p,T_q,\{x\},\{y\}),
\tag{18}
\]

which is EFX exactly when

\[
v_r(T_q)\ge\tau_r(D_p).
\tag{19}
\]

The atomic cell makes (19) automatic because `T_r` is a singleton and the
no-self inequalities give `v_r(T_q)>max(v_r(T_r),v_r(f))`.  For a genuine
packet, a deletion `T_r-g+f` can exceed `v_r(T_q)`.  Therefore the remaining
analytic step is precisely to use the contested-top quota witness to pay
that deletion threshold through a coupled return; treating `T_q` as one
supergood would be unsound.

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

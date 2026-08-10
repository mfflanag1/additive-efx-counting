# Length-three global-lex target

**Date:** 2026-08-09

**Status:** BCFF basic-cycle classification reconstructed; the external-`p`
row and the two external-`r`, `p`-before-`r` rows are closed cap-free; the
four external-`q` rows reduce to two scalar singleton-preference walls; two
external-`r` dual-base rows remain; final source-sensitive routing is open

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

The four packets are necessarily nonempty; this is not an additional
genericity assumption.  If `T_r` were empty, the selected desired set
`D_p={f}` would make `p` envy the charity good, contradicting (1).  The same
argument excludes empty `T_q`.  If `B_r` were empty, then `X_r=T_r` and
BCFF Observation 2.10 would make the negation of the self-edge `r -> r`
imply `v_r(X_r)>v_r(X_r+f)`, contradicting positivity.  Hence `r` is a
self-`f`-champion, which is a PI cycle.  The same argument excludes empty
`B_q`.  Thus every proper-decomposition fact used below is forced at a
globally maximal state.

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

The selected cycle also forces ordinary nonenvy of both large bundles:

> **Large-bundle no-envy lemma.** Every agent other than the owner weakly
> prefers her own bundle to `X_r` and to `X_q`.

Each contrary edge closes a basic PI cycle.  For `X_r`, edges from `p` or
`q` close respectively through `r -f-> q -> p` or directly through
`r -f-> q`; an edge from `s` closes through the external envy edge in each
of the three source cases.  For `X_q`, an edge from `p` closes the envy
2-cycle with `q -> p`, one from `r` closes through
`q -> p -f-> r`, and one from `s` again closes using the external envy
edge.  Every resulting cycle has at most one genuine `f`-edge.  Hence, at
global maximality,

\[
v_i(X_r)\le b_i\quad(i\ne r),
\qquad
v_i(X_q)\le b_i\quad(i\ne q).
\tag{4a}
\]

## BCFF basic-cycle classification

The normal form above follows from BCFF without a chordless-graph
assumption.  Select one incoming basic `f`-champion edge for every allocated
bundle.  Since every vertex has an incoming selected edge, the finite
directed graph contains a simple directed cycle.  If a selected champion
edge discards `f`, its desired set lies inside the target's old bundle, so
the source envies the target; replace that edge by the parallel envy edge.
Call the remaining selected `f`-edges genuine.

A cycle with zero or one genuine `f`-edge is a basic PI cycle and is
impossible at global maximality.  Thus the selected cycle has at least two
genuine edges.

No genuine edge can enter a singleton bundle `{z}`.  The
singleton-absorption lemma says `{z}` is envied.  The only subsets of
`{z,f}` containing `f` are `{f}` and `{z,f}`.  The former cannot be envied
by (1); the latter is not common-safe because deleting `f` leaves the envied
singleton `{z}`.  Hence every incoming champion of a singleton is
nongenuine and can be represented by an envy edge.

With exactly two nonsingleton bundles, a simple cycle therefore contains at
most two genuine edges.  It contains exactly two, and they enter the two
nonsingleton owners.  A simple cycle on four agents has only the following
possibilities:

1. length two: the two large owners exchange genuine edges;
2. length three: two consecutive genuine edges followed by one envy return,
   which is exactly (2), with the other singleton external;
3. length four: the two genuine edges have adjacent or alternating target
   positions.

These are the four residual classes in the exactly-two-nonsingleton
reduction.  Extra basic edges do not invalidate the selected length-three
cycle.  A self-edge or an extra edge closing a cycle with at most one `f`
edge is already PI; any remaining edge is simply additional input to the
all-source reservoir lemmas.  Thus the length-three theorem, once its nine
quota cases are closed, applies to the BCFF state without an unstated exact
envy/champion-graph premise.

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
U=X_r+B_q,\qquad t'=\tau_p(D_r).
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
| `a=p` | closed by the canonical escape lemma below |
| `a=r` | `(s,r,p,q)`, `(s,r,q,p)`; the two `p`-before-`r` rows are now closed |
| `a=q` | `(p,r,q,s)`, `(p,r,s,q)`, `(p,s,r,q)`, `(s,p,r,q)` |

For `a=p` or `a=q`, the rotated theorem closes every order beginning with
`r` and every `(s,r,...)` order.  The `W` theorem closes every order in
which `q` precedes `r`.  For `a=r`, direct transfer of `y` closes `r`-first
and `(p,r,...)` orders, while the `W` theorem again closes `q` before `r`.

In every still-open row above, a hypothetical failure forces the `W` extraction onto
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

There is also a universal exclusion that holds for every valid parallel
decomposition `D_p=T_r+f`.  Put `P=B_r+B_q`.

> **Bottom-pool exclusion lemma.** No subset of `P` is desired by any
> agent.  Consequently `v_i(P)<=b_i` for every agent `i`, and `P` and all
> its subsets are common-safe.

Suppose `A subseteq P` is desired.  Route it according to its source:

| source of `A` | Pareto-EFX allocation `(p,r,q,s)` |
|---|---|
| `p` | `(A,D_r,{x},{y})` |
| `r` | `(D_p,A,{x},{y})` |
| `q` | `({x},D_r,A,{y})` |
| `s`, with `a=p` | `({y},D_r,{x},A)` |
| `s`, with `a=r` | `(D_p,{y},{x},A)` |
| `s`, with `a=q` | `({x},D_r,{y},A)` |

All displayed bundles are pairwise disjoint and common-safe, and every
non-base recipient receives a desired bundle.  Each row contradicts global
maximality.  If some agent valued `P` above her base, an inclusion-minimal
subset of `P` envied by any agent would be desired, giving the same
contradiction.

Thus the bottoms may change the numerical deficits, but they are disjoint
universal safe currency.  Every irreducible desired-set collision is forced
onto `T_q` (and, in the rotated argument, onto `T_r`).

The exclusion also removes the easy half of the moving `q` ceiling.  Let
`C subseteq B_r+T_q` be any critical-pool bundle.  If
`v_q(B_r)<=v_q(B_q)`, then

\[
v_q(C)\le v_q(B_r)+v_q(T_q)
\le v_q(B_q)+v_q(T_q)=b_q<v_q(x).
\]

Thus `tau_q(C)<v_q(x)` automatically.  Every genuine `q`-wall must
therefore satisfy

\[
v_q(T_q)\ge v_q(B_r)>v_q(B_q)>v_q(f).
\]

The first weak inequality follows from the bottom-pool bound
`v_q(B_r+B_q)<=b_q=v_q(T_q+B_q)`; the last strict inequality is the
no-self-`q` consequence.  Hence the final cell is not an arbitrary Hall
obstruction: `q` strictly prefers the foreign bottom to her own bottom,
but not to her own top.

There is a still smaller witness inside the hard `q` reversal.  In the
critical-pool proof, a genuine `q` wall yields a `q`-desired set

\[
A\subseteq T_q+B_r
\]

inside a deletion of the minimal `r`-threshold bundle.  Put
`K=A\cap B_r`.  The transversal property gives `A\cap T_q != empty`, while
`K` is also nonempty: a subset of `T_q` alone is worth strictly less than
`b_q=v_q(T_q+B_q)`.  More sharply,

\[
v_q(K)>v_q(B_q)+v_q(T_q\setminus A)>v_q(B_q).
\tag{16a}
\]

Indeed, expand `v_q(A)>b_q` and move the missing part of `T_q` to the other
side.

Now replace the contested subset `K` in `r`'s base bundle by `B_q` and put

\[
L=(X_r\setminus K)+B_q.
\]

The pools `L` and `A` are disjoint.  If `v_r(B_q)>v_r(K)`, then
`v_r(L)>b_r`, so `L` contains a desired set `E` disjoint from `A`.  Every
possible source is impossible:

1. source `r` gives the Pareto-EFX allocation `({x},E,A,{y})`;
2. source `p` gives the PI cycle
   `p -(B_q|K)-> r -f-> q -> p`;
3. source `q` gives the PI cycle
   `q -(B_q|K)-> r -f-> q`;
4. source `s` gives the analogous PI cycle through the external envy edge
   when `a=p` or `a=q`; when `a=r`, the direct allocation
   `({x},{y},A,E)` is Pareto-EFX.

Here `E` is exactly the desired bundle of the generalized edge into `r`
with incoming set `B_q` and release set `K` (possibly with additional
discard).  The existing basic edge `r -f-> q` releases `B_q`, so every
listed generalized cycle satisfies the PI release condition; its incoming
sets `B_q` and `{f}` are disjoint.

Therefore global maximality forces the **joint bottleneck**

\[
K\subseteq B_r,\qquad
v_q(K)>v_q(B_q),\qquad
v_r(K)\ge v_r(B_q).
\tag{16b}
\]

The selected `p -> r` edge and absence of the parallel envy edge also give
`v_p(B_r)<v_p(f)`, hence

\[
v_p(K)<v_p(f),\qquad
v_q(K)>v_q(B_q)>v_q(f),\qquad
v_r(K)\ge v_r(B_q).
\tag{16c}
\]

This is the smallest currently known missing operation.  The three rows
want the resource chain `f -> p`, `K -> q`, and `B_q -> r`, but `B_q`
alone does not compensate `r` for releasing `K`.  A completion must either
augment `B_q` by a subset of the released part `T_q\setminus A`, give `f`
to `r` while promoting `p` through a different desired set, or turn the
failure of one of those payments into a compatible generalized champion
cycle.  This is strictly sharper than an arbitrary packet Hall failure.

The joint bottleneck has an exact one-sided threshold form.  Write
`A_q=A\cap T_q` and

\[
d_q=v_q(B_q)+v_q(T_q\setminus A_q).
\]

For every `J subseteq K` satisfying `v_q(J)>d_q`, global maximality forces

\[
v_r(J)\ge v_r(B_q).
\tag{16d}
\]

Otherwise `A_J=A_q+J` is a `q`-desired subset of `A`, while
`L_J=(X_r\setminus J)+B_q` is disjoint from `A_J` and is worth more than
`b_r` to `r`.  Extract a desired set `E subseteq L_J`.  Source `r` pairs
directly with `A_J`.  Sources `p` and `q` create respectively the PI cycles
`p -(B_q|J)-> r -f-> q -> p` and
`q -(B_q|J)-> r -f-> q`.  Source `s` uses the analogous external-envy
cycle for `a=p,q`, while for `a=r` the allocation
`({x},{y},A_J,E)` is Pareto-EFX.  These are the same release checks as in
the proof of (16b).

Thus the surviving wall is the pure knapsack statement

\[
\min\{v_r(J):J\subseteq K,\ v_q(J)>d_q\}\ge v_r(B_q).
\tag{16e}
\]

Its fractional relaxation either has a scalar `q/r` ratio price separating
the two thresholds, or has a greedy optimum with one fractional boundary
good.  The final analytic operation therefore needs to defeat one price or
compensate one indivisible pivot; it no longer needs to reason about an
arbitrary family of overlapping desired sets.

There is a complementary residual-payment formulation.  For a
`q`-sufficient `J subseteq K`, put

\[
S_J=(T_q\setminus A_q)+B_q,
\qquad
G_J=(B_r\setminus J)+S_J.
\]

Then `D_p`, `A_J`, and `G_J` are pairwise disjoint, and

\[
v_q(G_J)=v_q(B_r)-v_q(J)+d_q
<v_q(B_r)\le v_q(T_q)<b_q.
\tag{16f}
\]

Let `theta=tau_r(D_p)` for seven of the nine residual source/order types,
and let `theta=b_r` for the two `a=r` orders beginning `(s,r)`.  If
`v_r(G_J)>=theta`, choose an inclusion-minimal `R subseteq G_J` at that
threshold.  A common-safe `R` makes `(D_p,R,A_J,{y})` EFX; it either
promotes `p`, or in the two `theta=b_r` orders preserves `r` before the
later promotion.

If `R` is unsafe, reverse a violating deletion to a desired set
`E subseteq R-h`.  Minimality gives `v_r(E)<theta`, while (16f) rules out
source `q`.  The all-source payment allocations close sources `p,r,s`
except in exactly two symmetry pairs:

1. `a=r`, order `(s,r,p,q)` or `(s,r,q,p)`, with source `p`; and
2. `a=q`, order `(p,r,q,s)` or `(p,r,s,q)`, with source `s`.

In the first pair, paying `r` by `D_p` would lower `r` before the
`p`-promotion.  In the second, transferring `y` to `q` would lower `r`
before either later improvement.  These are source/order mismatches, not a
new packing wall.

If no `J` reaches the threshold, every `q`-sufficient subset satisfies the
additional scalar inequality

\[
v_r(J)>v_r(B_r)+v_r(S_J)-\theta.
\tag{16g}
\]

Together, (16d) and (16g) reduce the non-mismatch branch to one knapsack
cost bound with lower threshold

\[
v_r(J)\ge
\max\{v_r(B_q),\ v_r(B_r)+v_r(S_J)-\theta\}.
\tag{16h}
\]

The remaining work is now exact: defeat this price/pivot bound using `f`,
or show that the two mismatch sources create a root-flipped or adjacent
cycle whose established escape preserves the earlier-priority agent.

### Charity-compensated split flip

There is one operation that bypasses every source/order distinction.  Let
`J subseteq X_r` satisfy

\[
\begin{aligned}
v_r(J)&\le \min\{v_r(f),v_r(T_q)\},\\
v_q(J)&>v_q(T_q),\qquad v_q(J)\ge v_q(f),\\
v_i(f)&\le v_i(J)\le v_i(T_q)\qquad(i=p,s).
\end{aligned}
\tag{16i}
\]

Then the allocation

\[
(Y_p,Y_r,Y_q,Y_s)
=\bigl(\{x\},(X_r\setminus J)+f,J+B_q,\{y\}\bigr)
\tag{16j}
\]

is EFX, weakly improves `r`, and strictly improves `q`.  Hence it
lexicographically improves every order in the nine-row residual table,
because all those orders place `r` before `q` and keep `p,s` fixed.

For the proof, `r`'s utility changes by `v_r(f)-v_r(J)`, while `q` replaces
`T_q` by the strictly preferred `J`.  To check the new `r` bundle, deleting
`f` leaves a subset of `X_r`; after deleting an old good `h`, every observer
`i=p,q,s` sees at most `X_r-h`, because `v_i(f)<=v_i(J)`.  These remainders
are safe by base EFX.  To check `J+B_q`, observers `i=p,r,s` may replace
`J` by `T_q` using `v_i(J)<=v_i(T_q)`; the resulting set is a subset of
`X_q` or one of its deletion remainders, and (4a) plus base EFX makes it
safe.  Recipient self-comparisons are automatic.  Thus (16j) is EFX.

This identifies the most economical possible pivot repair: transfer one
subpacket `J` from `r` to `q`, compensate `r` with the charity good, and
release `T_q`.  The final selector theorem may therefore be stated as:

> either a subset satisfying the four-row sandwich (16i) exists, or the
> scalar separator for this subset-sum system forces a compatible desired
> family/root-flipped cycle.

The strict two-split adversarial profile that survived 928 earlier rival
allocations was escaped exactly by (16j), with a two-good `J`; this is motif
evidence only, not a premise of the lemma.

At a hypothetical globally maximal state, the split flip collapses to its
charity-transition face.  BCFF's respecting nondegenerate perturbation
ensures `v_r(J)!=v_r(f)` for distinct bundles.  Hence the recipient
condition `v_r(J)<=v_r(f)` is strict.  If `R_J` were common-safe, replacing
`X_r` by `R_J` while leaving `J` unallocated would already be an EFX Pareto
improvement of `r`, without using `Q_J` at all.  Therefore global maximality
forces `R_J` to be unsafe for every recipient-feasible `J`.

Accordingly the `Q_J` analysis below is a useful exact diagnosis of why a
root-only repair cannot rescue a tied or nonmaximal split profile, but it is
not the live maximal-state branch.  At a nondegenerate global maximum, the
live branch is always the genuine
`f`-champion exposed by the unsafe `R_J` deletion and routed by the
single-pivot lemma (16n)--(16o).

The same construction gives an exact six-face failure certificate even
without the sufficient sandwich bounds.  Suppose only that

\[
v_r(J)\le v_r(f),\qquad v_q(J)>v_q(T_q).
\tag{16k}
\]

Then the two recipients in (16j) weakly/strictly improve.  If (16j) is not
EFX, one of only the following faces fails:

1. an observer in `{p,q,s}` blocks a deletion of
   `R_J=(X_r\setminus J)+f`; or
2. an observer in `{p,r,s}` blocks a deletion of `Q_J=J+B_q`.

Deleting `f` from `R_J` is always safe.  A blocker on its other deletion
therefore yields, by minimal crossing, a desired set containing `f` inside
`X_r\setminus(J\cup\{h\})+f`.  This is exactly the charity-swap transition: a
new genuine `f`-champion into `r`, omitting `J` and one further good.

A blocker on `Q_J` yields a desired subset of the generalized offer that
replaces `T_q` by `J`, hence an explicit edge

\[
k\mathrel{\mathop{\longrightarrow}^{J\mid T_q}}q
\tag{16l}
\]

for some source `k` (with possible additional discard).  Moreover `J`
cannot lie wholly in `B_r`: the bottom-pool exclusion gives
`v_q(B_r)<=v_q(T_q)`, contradicting (16k).  Thus
`J\cap T_r` is nonempty.  The part `J\cap B_r` is already released by the
selected `p -f-> r` edge; the sole compatibility defect of (16l) is the
explicit top subpacket `J\cap T_r`.

This converts the adaptive-root problem into a precise finite choice:
select a parallel `p -f-> r` decomposition that places the top defect of a
recipient-feasible `J` in its released bottom, or route the source of
(16l) directly.  No fixed packet-size statement is hidden in this
certificate.

The source routing in the second face is in fact complete whenever
`R_J=(X_r\setminus J)+f` is common-safe.  Let `E subseteq Q_J-h` be the
desired set exposed by an unsafe deletion of `Q_J=J+B_q`.

| source of `E` | EFX escape `(p,r,q,s)` |
|---|---|
| `p` | `(E,R_J,{x},{y})` |
| `q` | `({x},R_J,E,{y})` |
| `s`, `a=p` | `({y},R_J,{x},E)` |
| `s`, `a=q` | `({x},R_J,{y},E)` |

Every row is disjoint; `R_J` weakly improves `r`, and every other changed
recipient gets a desired bundle.  Thus each row is EFX and improves every
residual priority order.

Only source `r`, and source `s` with `a=r`, remain.  Suppose there is a
parallel selected decomposition `D'_p=T'_r+f` with `T'_r\cap J=empty`.
Its bottom `B'_r=X_r\setminus T'_r` releases all of `J`.  Source `r` then
gives the PI cycle

\[
r\mathrel{\mathop{\longrightarrow}^{J\mid T_q}}q
\longrightarrow p\xrightarrow f r,
\]

and source `s` with `a=r` gives

\[
s\mathrel{\mathop{\longrightarrow}^{J\mid T_q}}q
\longrightarrow p\xrightarrow f r\longrightarrow s.
\]

The incoming sets are `J` and `{f}`, which are disjoint; `J` is released by
the `p -f-> r` edge under the alternative decomposition.  Both are valid PI
cycles.

Consequently an unresolved `Q_J` face forces the exact
**root-transversal obstruction**

\[
T'_r\cap J\ne empty
\quad\text{for every valid parallel }p -f-> r\text{ decomposition }T'_r+f.
\tag{16m}
\]

In fact (16m) is forced automatically whenever `R_J` is common-safe and
`v_r(J)<=v_r(f)`.  Suppose a valid parallel decomposition
`D'_p=T'_r+f` had `T'_r\cap J=empty`, and put
`B'_r=X_r\setminus T'_r`.  The no-self inequality for this decomposition
gives

\[
v_r(B'_r)>v_r(f)\ge v_r(J),
\]

so `B'_r\setminus J` contains a good `h`.  But then the deletion remainder
`R_J-h` contains the entire desired set `T'_r+f`, which `p` values above
`b_p`.  This contradicts common safety of `R_J`.

Therefore a root change cannot resolve the two hard `Q_J` sources while
preserving the safe compensated bundle: every admissible root necessarily
meets `J`.  This exactly refutes the narrower **root-only completion** of
the split-flip bridge.  The missing operation must change the allocation
itself—remove an additional top blocker, repartition the suffix, or pay the
single budget-crossing pivot—rather than merely select a different parallel
decomposition.

The two hard sources nevertheless have one exact common reduction.  Let
`E subseteq Q_J-h` be the desired bundle exposed by the `Q_J` face.  If its
source is `r`, or if its source is `s` and `a=r`, then any common-safe set
`Z` disjoint from `E,x,y` satisfying

\[
v_q(Z)\ge\tau_q(E)
\tag{16m.1}
\]

gives an EFX escape:

\[
({x},E,Z,{y})
\quad\text{or}\quad
({x},{y},Z,E),
\]

respectively.  In the second allocation `r` receives the singleton she
envies.  This is exactly the already-proved two-safe-bundle reduction, with
`E` as its desired bundle and `Z` as the `q` payment.

Thus the root-only bridge is false for a structural reason, but the full
adaptive bridge now has a precise final obligation: extract the payment
`Z` from the residual goods, or reverse an unsafe threshold extraction into
a compatible desired family.  No additional four-agent EFX verification is
needed once (16m.1) holds.

There is a canonical first payment.  Since `E subseteq J+B_q`, put

\[
E_q=E\cap B_q,
\qquad
Z_0=X_q\setminus E_q=T_q+(B_q\setminus E_q).
\]

The sets `E` and `Z_0` are disjoint.  Moreover `Z_0` is common-safe by
downward closure from the base bundle `X_q`.  Hence (16m.1) holds, and the
hard face closes, whenever

\[
v_q(E_q)+\tau_q(E)\le b_q.
\tag{16m.2}
\]

Consequently every surviving hard blocker must use a nonempty part of
`B_q` and satisfy the strict overlap inequality

\[
v_q(E\cap B_q)+\tau_q(E)>b_q.
\tag{16m.3}
\]

The safe-payment problem is therefore no longer spread across the residual
goods: its irreducible overlap lies entirely in `B_q`.  Goods of
`J\setminus E` may be added only to repair the strict deficit in (16m.3),
with an unsafe addition again exposing a desired-family edge.

There is a monotone cap-free potential on the other face.  For any
`J subseteq X_r` with `v_r(J)<v_r(f)`, put

\[
R_J=(X_r\setminus J)+f.
\]

If `R_J` is common-safe, replacing `X_r` by `R_J` and leaving `J`
unallocated is EFX and strictly Pareto improves `r`.  Moreover common
safety is monotone in `J`: enlarging `J` only lowers every deletion
remainder of `R_J`.

Choose an inclusion-maximal `r`-affordable set `J`, so

\[
v_r(J)<v_r(f),\qquad
v_r(J+h)\ge v_r(f)\quad(h\in X_r\setminus J).
\tag{16n}
\]

Global maximality says `R_J` is unsafe.  Deleting `f` is safe, so some old
good `h` and observer expose a desired set

\[
E\subseteq (X_r\setminus(J\cup\{h\}))+f
\tag{16o}
\]

that contains `f`.  Thus one of the following occurs:

1. a self-`f`-champion of `r`, which is PI;
2. a `q -f-> r` edge, which redirects to the length-two class;
3. an `s -f-> r` edge, routed by the shortest-cycle cases above; or
4. a parallel `p -f-> r` decomposition whose top avoids both `J` and the
   single pivot `h`.

Hence arbitrary packet growth never produces an irreducible multi-good
swap wall.  It produces one budget-crossing pivot `h`, while every cheaper
good in `J` is released by the alternative root in case 4.  This is the
integral counterpart of the fractional price-or-pivot lemma.

### Parallel-root residual-payment lemma

The alternative root in case 4 couples directly to the persistent `q` wall.
Write its desired bundle as

\[
E=T+f,
\qquad B=X_r\setminus T,
\]

so `E` is desired by `p`.  Let `A subseteq T_q+B` be the `q`-desired set
forced by failure of the all-source return, and put

\[
A_q=A\cap T_q,
\qquad K=A\cap B,
\qquad
Z_0=(B\setminus K)+(T_q\setminus A_q)+B_q.
\tag{16p}
\]

Then `E`, `A`, `Z_0`, and `{y}` are pairwise disjoint.  More importantly,

\[
v_q(Z_0)<v_q(B)\le v_q(T_q)<b_q.
\tag{16q}
\]

Indeed, `A` being desired by `q` gives

\[
v_q(K)>v_q(B_q)+v_q(T_q\setminus A_q).
\]

Substitution in (16p) gives the strict first inequality in (16q).  The
bottom-pool exclusion, reapplied to the valid parallel root `E=T+f`, gives
`v_q(B+B_q)<=b_q`, and hence `v_q(B)<=v_q(T_q)`.  Finally positivity gives
`v_q(T_q)<b_q=v_q(T_q+B_q)`.

For the seven residual priority/source types in which `p` precedes `r`
after any fixed initial `s`, define

\[
\theta=\max\{\tau_r(E),\tau_r(A)\}.
\]

For the two types with `a=r` and priority `(s,r,p,q)` or `(s,r,q,p)`, put
`theta=b_r`.  In every case, if there is a common-safe `Z subseteq Z_0`
with

\[
v_r(Z)\ge\theta,
\tag{16r}
\]

then

\[
(Y_p,Y_r,Y_q,Y_s)=(E,Z,A,\{y\})
\tag{16s}
\]

is EFX and lexicographically improves the base.  The desired bundles `E`
and `A` protect their recipients, `{y}` is unchanged, and (16r) is exactly
the only nonautomatic pair of comparisons made by `r`.  In the seven easy
orders `p` is the first changed priority agent and strictly improves.  In
the two hard orders `s` is unchanged, `r` weakly improves, and if `r` is
unchanged then the later agent `p` strictly improves.

This payment test has an exact source reduction.  If `v_r(Z_0)>=theta`,
choose an inclusion-minimal `Z subseteq Z_0` satisfying (16r).  If `Z` is
unsafe, reverse a violating deletion to a desired set `F subseteq Z-g`.
Minimality and (16q) give

\[
v_r(F)<\theta\le b_r,
\qquad
v_q(F)<b_q.
\tag{16t}
\]

Therefore the source of `F` is in `{p,s}`; neither large owner can be the
source.  In the two hard `a=r` orders, source `s` closes immediately via

\[
(E,\{y\},A,F),
\tag{16u}
\]

because `r` strictly envies `{y}` and all four displayed recipient bundles
are desired or singleton-safe.  Consequently a surviving hard-order state
has exactly one of the following two certificates:

1. the scalar payment deficit `v_r(Z_0)<b_r`; or
2. a `p`-desired `F subseteq Z-g`, disjoint from both the parallel-root
   bundle `E` and the `q`-desired bundle `A`.

The second certificate is a duplicate-source Hall obstruction: two
pairwise-disjoint bundles `E` and `F` are both desired by `p`, while `A` is
desired by `q`.  It is strictly smaller than the former arbitrary
external-observer wall.  A final augmenting argument must either turn this
second `p` demand into a compatible generalized cycle or use the scalar
deficit to pay the unique budget-crossing pivot.  No fixed cardinality or
bounded-value premise occurs in the reduction.

The duplicate-source wall admits a global-potential reduction that does not
freeze either desired bundle.  Call a disjoint ordered pair `(P,Q)`
**`r`-residual-feasible** when `y` belongs to neither member,

\[
v_p(P)>b_p,\qquad v_q(Q)>b_q,
\tag{16v}
\]

the two bundles are mutually safe at their proposed owners,

\[
\begin{array}{ll}
\tau_p(Q)\le v_p(P),&\tau_q(P)\le v_q(Q),\\
\tau_s(P),\tau_s(Q)\le b_s,&
\tau_r(P),\tau_r(Q)\le b_r,
\end{array}
\tag{16w}
\]

and the residual pool

\[
U(P,Q)=M\setminus(P\cup Q\cup\{y\})
\]

satisfies `v_r(U(P,Q))>=b_r`.

This family is nonempty.  Take `P=E=T+f` from any valid parallel
`p -f-> r` root and `Q={x}`.  The desired set `E` is common-safe, while
`q` strictly envies `{x}`.  The residual pool is `B+X_q`, and

\[
v_r(B+X_q)>v_r(B)+v_r(T)=b_r
\tag{16x}
\]

because the no-chord inequality for the parallel root gives
`v_r(T_q)>v_r(T)`.

Choose an `r`-residual-feasible pair `(P,Q)` lexicographically maximizing
`(v_p(P),v_q(Q))`.  Inside its residual pool choose an inclusion-minimal
`R` with `v_r(R)>=b_r`.  If `(P,R,Q,{y})` is EFX, it improves both hard
orders: `s` is fixed, `r` is weakly improved, and `p` strictly improves if
`r` ties.

Otherwise only an external comparison to `R` can fail.  Choose inside a
violating deletion `R-g` an inclusion-minimal set `F` whose value exceeds
one of the four current thresholds

\[
c_p=v_p(P),\qquad c_q=v_q(Q),\qquad c_r=b_r,
\qquad c_s=b_s.
\]

Then for every agent `i` and every `h in F`,

\[
v_i(F-h)\le c_i.
\tag{16y}
\]

The source cannot be `r`, since inclusion-minimality of `R` gives
`v_r(F)<=v_r(R-g)<b_r`.  If the source is `s`, (16y) makes

\[
(P,\{y\},Q,F)
\tag{16z}
\]

EFX: `r` strictly improves to the singleton she envies, `s` strictly
improves to `F`, and (16w)--(16y) protect `p` and `q`.

If the source is `p`, the pair `(F,Q)` satisfies all compatibility
inequalities in (16v)--(16w) and strictly raises the first extremal
coordinate.  Its residual `r`-value is

\[
v_r(U(F,Q))=v_r(U(P,Q))-v_r(F)+v_r(P).
\]

Maximality therefore forces `v_r(F)>v_r(P)`; otherwise `(F,Q)` would remain
`r`-residual-feasible and contradict the choice of `(P,Q)`.  Similarly, a
`q`-source forces

\[
v_r(F)>v_r(Q).
\tag{16aa}
\]

Writing `sigma=v_r(U(P,Q))-b_r` for the residual slack sharpens these to

\[
v_r(F)-v_r(P)>\sigma
\quad\hbox{or}\quad
v_r(F)-v_r(Q)>\sigma,
\tag{16ab}
\]

respectively: otherwise the replacement pair would still leave residual
`r`-value at least `b_r`.  This is the exact budget-crossing inequality,
not merely a qualitative failure of an exchange.

There is also an immediate top-up escape.  In the `p`-source case, if
`v_s(P)>=b_s`, then

\[
(F,\{y\},Q,P)
\tag{16ac}
\]

is EFX.  Agent `p` prefers `F` to `P`; `q` retains `Q`; `r` receives the
envied singleton; and (16w)--(16y) give every deletion comparison.  Thus a
surviving `p` blocker additionally forces `v_s(P)<b_s`.  Symmetrically, a
surviving `q` blocker forces `v_s(Q)<b_s`, since otherwise
`(P,{y},F,Q)` is EFX.  The missing compensation may therefore be stated as
one externally safe top-up of the replaced low-`s` bundle, after which `y`
can pay `r` and the boundary blocker can pay its own source.

Thus the adaptive-pair potential eliminates every nonnumeric observer
wall in the two hard orders.  A surviving state supplies a single
inclusion-minimal blocker that improves `p` or `q` but crosses the residual
`r` budget by being strictly more expensive to `r` than the bundle it
would replace.  Proving that the charity good or a released suffix pays
this strict cost, or routing the boundary blocker to a shorter/adjacent
cycle, is the remaining hard-order operation.

The same potential has a symmetric formulation that absorbs the remaining
source/order mismatch.  Call a triple `(P,Q,S)`, provisionally assigned to
`p,q,s`, **`r`-budget-feasible** if its members are pairwise disjoint,
`y` belongs to neither `P` nor `Q`,

\[
v_p(P)>b_p,\qquad v_q(Q)>b_q,\qquad v_s(S)\ge b_s,
\tag{16ad}
\]

each provisional owner is EFX-safe against the other two bundles,

\[
\tau_i(B_j)\le v_i(B_i)
\quad(i,j\in\{p,q,s\},\ i\ne j),
\tag{16ae}
\]

agent `r` is base-safe against all three, and the residual pool has enough
total `r`-value:

\[
\tau_r(P),\tau_r(Q),\tau_r(S)\le b_r,
\qquad
v_r\bigl(M\setminus(P\cup Q\cup S)\bigr)\ge b_r.
\tag{16af}
\]

This family is nonempty: `(E,{x},{y})` satisfies (16ad)--(16af), and its
residual is again `B+X_q`, whose `r`-value is strictly above `b_r` by
(16x).

Choose a coordinatewise Pareto-maximal `r`-budget-feasible triple and let
`U` be its residual pool.  Choose an inclusion-minimal `R subseteq U` with
`v_r(R)>=b_r`.  If `(P,R,Q,S)` is EFX, it is already a Pareto improvement
of the base: `p,q` strictly improve and `r,s` weakly improve.

Otherwise an agent `k in {p,q,s}` blocks a deletion of `R`.  Inside that
deletion choose an inclusion-minimal set `F` exceeding one of the current
owner thresholds

\[
c_i=v_i(B_i)\quad(i\in\{p,q,s\}),
\qquad c_r=b_r.
\]

As in (16y), every deletion of `F` is below every corresponding threshold,
and `r` cannot be its source because `v_r(F)<b_r`.  If `k` is the source,
replace `B_k` by `F`.  All inequalities (16ad)--(16ae) and the first part
of (16af) remain true, while agent `k` strictly improves and nobody else's
provisional utility changes.  Therefore Pareto maximality forces the new
residual to violate the last inequality in (16af).  With

\[
\sigma=v_r(U)-b_r,
\]

this is exactly

\[
v_r(F)-v_r(B_k)>\sigma.
\tag{16ag}
\]

Hence the length-three source table no longer leaves different `p`, `q`,
and external-singleton safety walls.  After the global triple is selected,
every one of them is an instance of the same strict `r`-budget crossing
(16ag).  The only remaining information carried by the source is which
provisional bundle `B_k` becomes available for compensating `r` or topping
up the owner of the envied singleton.

In fact the `s` source disappears in the hard `a=r` branch.  If `y` is not
in `S`, it lies in the residual pool, and

\[
(P,\{y\},Q,S)
\]

is EFX by (16ae)--(16af); `r` strictly improves to the envied singleton.
Thus an obstruction forces `y in S`.  But `tau_r(S)<=b_r` while
`v_r(y)>b_r`.  Positivity then forces `S={y}`: if `S` contained another
good, deleting that good would leave a set containing `y` and violate
`r`-safety.  A putative `s`-source replacement releases `{y}` into the
residual and has `r`-value below `b_r`, so it cannot satisfy the strict
budget crossing (16ag).  Therefore only `p`- and `q`-sourced boundary
blockers survive, and the selected triple has the exact form `(P,Q,{y})`.

### Dual-mode adaptive-root potential

The root choice can be included in the extremal potential.  Call a
disjoint pair `(P,Q)`, with `y` in neither bundle, **compatible** when

\[
v_p(P)>b_p,\qquad v_q(Q)>b_q,
\tag{16ah}
\]

\[
\tau_p(Q)\le v_p(P),\qquad
\tau_q(P)\le v_q(Q),
\tag{16ai}
\]

and both bundles are base-safe for `r` and `s`.  Put

\[
U(P,Q)=M\setminus(P\cup Q\cup\{y\}).
\]

The pair is feasible in **`r` mode** if `v_r(U(P,Q))>=b_r`, and feasible
in **`s` mode** if `v_s(U(P,Q))>=b_s`.  In `r` mode the intended allocation
keeps `s={y}` and pays `r` from `U`; in `s` mode it gives `r={y}` and pays
`s` from `U`.

The union of the two mode families is nonempty.  The structural pair
`(E,{x})` is compatible and is `r`-mode feasible by (16x).  Choose over the
union a pair `(P,Q)` whose utility vector `(v_p(P),v_q(Q))` is
coordinatewise Pareto-maximal, and fix a mode in which it is feasible.
Let `d` be that mode's payment agent and choose an inclusion-minimal
`d`-threshold set `R subseteq U(P,Q)`.

If the corresponding allocation `(P,R,Q,{y})` in `r` mode, or
`(P,{y},Q,R)` in `s` mode, is EFX, it Pareto improves the base.  Otherwise
choose in a violating deletion of `R` an inclusion-minimal set `F`
exceeding one of the thresholds

\[
c_p=v_p(P),\qquad c_q=v_q(Q),\qquad c_r=b_r,
\qquad c_s=b_s.
\tag{16aj}
\]

Every deletion of `F` is below all four thresholds.  The payment agent
cannot be the source by minimality of `R`.  If the other member of
`{r,s}` is the source, switch the ownership of `y`: in `r` mode an
`s`-source gives `(P,{y},Q,F)`, while in `s` mode an `r`-source gives
`(P,F,Q,{y})`.  Both are EFX Pareto improvements.

It remains to consider source `k in {p,q}`.  Replace `k`'s provisional
bundle `B_k` by `F`.  The new pair is compatible and strictly improves one
coordinate.  Hence it can belong to neither mode, or it would contradict
the global choice of `(P,Q)`.  Writing

\[
U'=\bigl(U(P,Q)\setminus F\bigr)+B_k,
\]

every surviving blocker therefore satisfies the simultaneous deficit

\[
v_r(U')<b_r,
\qquad
v_s(U')<b_s.
\tag{16ak}
\]

Equivalently, it crosses both additive budgets:

\[
v_i(F)-v_i(B_k)>v_i(U(P,Q))-b_i
\qquad(i=r,s).
\tag{16al}
\]

The right side need not be nonnegative for the mode not originally
selected, but (16ak) is unconditional.  This is an exact adaptive-root
certificate.  A one-bundle replacement cannot preserve either possible
owner of the contested singleton `y`; the smallest remaining operation
must change both provisional bundles jointly, or expose a shorter/adjacent
cycle while repartitioning `U'`.  The six fixed-order countermodels do not
invalidate this statement because they optimize within one mode only.

The boundary set itself is indivisible in a stronger sense.  Let `t` be
the nonpayment member of `{r,s}`: `t=s` in `r` mode and `t=r` in `s` mode.
If

\[
\tau_t(F)\ge b_t,
\tag{16am}
\]

choose a deletion remainder `H=F-g` attaining `tau_t(F)`.  By the minimal
choice of `F`, its total value is below every other current owner threshold.
In `r` mode,

\[
(P,\{y\},Q,H)
\]

is therefore EFX: the original compatible pair stays assigned, `r`
strictly improves to `{y}`, and `s` weakly improves to `H`.  In `s` mode
the symmetric allocation `(P,H,Q,{y})` is EFX.  Consequently every
surviving boundary blocker satisfies

\[
\tau_t(F)<b_t.
\tag{16an}
\]

Thus no proper part of `F` can compensate the owner displaced from `y`,
while the whole of `F` is required to cross the `p`- or `q`-source
threshold.  The remaining integral obstruction is one contested minimal
bundle, not an arbitrary family of observer failures.

### Exact falsification boundary for fixed roots

The dual-mode potential must optimize over arbitrary compatible pairs.
Freezing it at the structural pair `(E,{x})` is false for genuine packets,
even in the exact chordless length-three cell.

In the seven-good atom, the fixed pair has opposite behavior in two exact
formulas.  Under only the selected edges it is SAT-refuted; the model has
many additional envy/champion chords and unrestricted escapes.  Under the
exact atomic envy/champion graph, blocking all fourteen `r`- and `s`-mode
payments is QF_LRA-UNSAT.  This explains the atomic cores but proves no
packet statement.

In the `(2,2,2,2)` split cell, the exact chordless formula is SAT after all
126 fixed-root payments are blocked.  The frozen positive-integer model is
recorded in
[`length_three_dual_mode_split_refutation.json`](length_three_dual_mode_split_refutation.json).
Its minimum escape in the unrestricted dual-mode family changes three goods:

\[
\begin{aligned}
Y_p&=\{x,tr_1\},\\
Y_r&=\{tr_0,br_0,tq_0\},\\
Y_q&=\{br_1,tq_1,bq_0,bq_1\},\\
Y_s&=\{y\},
\end{aligned}
\tag{16ao}
\]

with `f` still unallocated.  Relative to the base, `tr_1` moves from `r`
to `p`, `tq_0` from `q` to `r`, and `br_1` from `r` to `q`.  Every moving
recipient strictly improves and the allocation is EFX.  Thus the smallest
missing fixed-root operation is an anchored three-agent suffix cycle, not a
larger payment bundle.

The broader compatible-pair quantifier in (16ah)--(16al) already contains
this suffix cycle and its charity-paid variants.  The countermodel therefore
rules out further fixed-root casework without weakening the global
dual-mode target.

The adversarial replay in
[`length_three_dual_mode_adversarial_audit.json`](length_three_dual_mode_adversarial_audit.json)
tests the unrestricted dual-mode family on 26 frozen profiles: the six
strict hard-order countermodels, the eighteen eleven-good profiles, the
augmented-`q`-face countermodel, and the Pareto-maximal profile `V*`.  It
finds an exact dual-mode Pareto escape in all 25 profiles having a feasible
mode.  `V*` is the sole failure, and has no mode-feasible compatible pair;
in particular it lacks the length-three residual-capacity consequence
(16x).  No tested profile realizes the simultaneous deficit (16ak).  This
is adversarial evidence for the global potential, not a proof of its final
uncrossing step.

### Lexicographic tail-mode extremal reduction

#### Canonical closure of the external-`p` row

The sole `a=p` order `(s,p,r,q)` is now closed without an extremal pair.
Take the structural pair `(E,{x})`, choose a minimal `r`-payment at
`theta=tau_r(E)`, and reverse an unsafe deletion at the simultaneous
ceilings

\[
\min\{v_p(E),v_p(y)\},\qquad v_q(x),\qquad b_s.
\]

A `p`- or `s`-sourced boundary gives the direct allocations in (16ak.0c).
For a `q`-sourced boundary `F`, if `v_r(x)>=theta`, the allocation
`(E,{x},F,{y})` is EFX.  Otherwise, for a least-`r` good `h in E`,

\[
(p,r,q,s)=(\{x,h\},E-h,F,\{y\})
\]

is EFX and improves `p` while fixing `s`.  The full packet-safe proof is
[`LENGTH_THREE_AP_CANONICAL_ESCAPE_LEMMA.md`](LENGTH_THREE_AP_CANONICAL_ESCAPE_LEMMA.md).

This dichotomy supersedes the maximizing-`Q` anchor analysis below for the
`a=p` row.  That analysis is retained as proof-mining history and remains
potentially relevant to the external-`q` row; it is no longer a completion
gate for `a=p`.

#### Canonical closure of the external-`r` tail rows

The same minimal-payment dichotomy closes `(p,s,r,q)` and `(s,p,r,q)` when
`a=r`.  A boundary sourced by `p` reverses to `(F,E,{x},{y})`; one sourced
by `s` gives `(E,{y},{x},F)`; and a `q` boundary uses the same direct-
singleton/least-pivot split as above.  The external edge `r -> s` excludes
the sole suffix observer wall `s -> p` by a one-charity-edge PI cycle.
See
[`LENGTH_THREE_AR_TAIL_ESCAPE_LEMMA.md`](LENGTH_THREE_AR_TAIL_ESCAPE_LEMMA.md).

Consequently the asymmetric hybrid potential below is no longer needed for
the two `p`-before-`r` rows.  Its exact models remain useful adversarial
evidence for the still-open dual-base operation.

#### Adaptive-singleton reduction of the external-`q` rows

Assign `s` her preferred singleton from `{x,y}` and `q` the other before
performing the same canonical payment extraction.  A `q`-sourced boundary
uses its assigned singleton as the direct payment or suffix anchor.  An
`s`-sourced boundary instead assigns `q` her preferred singleton and uses
the other as the payment/anchor.  All branches close unless `y` is the
forced anchor and simultaneously

\[
v_r(y)<\tau_r(E),\qquad v_p(y)<v_p(E-h),
\]

where `h` is least for `r` in `E`; the forcing preference is either
`v_s(x)>v_s(y)` for a `q` boundary or `v_q(x)>v_q(y)` for an `s` boundary.
See
[`LENGTH_THREE_AQ_ADAPTIVE_SINGLETON_REDUCTION.md`](LENGTH_THREE_AQ_ADAPTIVE_SINGLETON_REDUCTION.md).

Thus the former four-row external-`q` table is now one two-scalar anchor
deficit with two possible witnesses, not an unrestricted tail-payment wall.
If the atomic fallback `(E,T_q, singleton, singleton)` fails, the charity-
swap transition routes every new source except a parallel `p -> r` root or
the length-two topology: a new `s -> r` root either enters the now-closed
external-`p` row or reverses the singleton preference and closes on the
next adaptive-singleton pass.  The live external-`q` object is therefore a
parallel-root recurrence, not a free observer failure.

For the seven residual priority/source types in which `p` or `q` precedes
`r` after any unchanged initial `s`, the `r`-mode feasibility threshold can
be lowered analytically.  Retain the compatible-pair definition
(16ah)--(16ai), and define

\[
\vartheta_r(P,Q)=\max\{\tau_r(P),\tau_r(Q)\}.
\tag{16ak.1}
\]

Call `(P,Q)` **`r`-tail-feasible** when its residual pool satisfies

\[
v_r(U(P,Q))\ge\vartheta_r(P,Q).
\tag{16ak.2}
\]

This family is nonempty: the structural pair `(E,{x})` is compatible,
`vartheta_r(E,{x})<=b_r`, and (16x) gives residual `r`-value strictly above
`b_r`.  Choose an `r`-tail-feasible pair Pareto-maximal in
`(v_p(P),v_q(Q))`, and inside its residual choose an inclusion-minimal
`R` with

\[
v_r(R)\ge\vartheta_r(P,Q).
\tag{16ak.3}
\]

If `(P,R,Q,{y})` is EFX, it lexicographically improves every such type:
`p,q` strictly improve, while `s` keeps `{y}`.  This conclusion does not
require `v_r(R)>=b_r`.  It does not apply to the two `a=r` types
`(s,r,p,q)` and `(s,r,q,p)`, where `r` is earlier than both improving pair
owners.

The sole `a=p` residual type has a sharper source-valid canonical form.
Its priority order is `(s,p,r,q)`.  Take

\[
P=E=T_r+f,\qquad Q=\{x\},\qquad
\vartheta_r(P,Q)=\tau_r(E).
\tag{16ak.0a}
\]

The residual `B_r+X_q` has `r`-value above `b_r` by (16x), so choose an
inclusion-minimal payment `R` at `tau_r(E)`.  If `(E,R,{x},{y})` is unsafe,
reverse a violating deletion to an inclusion-minimal base-desired set
`F`.  It is common-safe and

\[
v_r(F)<\tau_r(E).
\tag{16ak.0b}
\]

Two sources close immediately:

\[
\begin{array}{c|c}
\text{source of }F & (p,r,q,s)\\ \hline
p & (F,E,\{x\},\{y\})\\
s & (\{y\},E,\{x\},F).
\end{array}
\tag{16ak.0c}
\]

Both rows are EFX.  In the first, `p` receives her desired `F`; in the
second, `p` receives the singleton she envies and `s` receives her desired
`F`.  Agent `r` can hold `E` because (16ak.0b) pays her only nontrivial
comparison; `q={x}` and common safety settle the rest.  Each allocation
lexicographically improves `(s,p,r,q)`.  Consequently the `a=p` row has
only a `q`-sourced tail boundary left; arbitrary `p`- and `s`-observer walls
are analytically eliminated without changing roots or bounding packets.

For `a=q`, use the same canonical payment and boundary `F`.  A `p`-source
again closes all four residual orders through `(F,E,{x},{y})`.  If `F` is
`s`-desired, then

\[
(p,r,q,s)=(\{x\},E,\{y\},F)
\tag{16ak.0d}
\]

is EFX: `q` receives the singleton she envies, `s` receives her desired
set, and (16ak.0b) lets `r` hold `E`.  It closes `(p,s,r,q)` and
`(s,p,r,q)`, where the improving `s` precedes any possible loss of `r`.
It need not close `(p,r,q,s)` or `(p,r,s,q)`, because `p` is fixed and `r`
may be below base.  Thus the four `a=q` types reduce source-validly to:

- a `q`-sourced tail boundary in all four orders; and
- an additional `s`-sourced boundary only in the two orders where `r`
  precedes `s` after the fixed `p`.

This priority distinction is why ownership of `{y}` cannot be treated as a
source-independent mode switch.

The persistent `q` wall admits a root-preserving one-coordinate potential.
Fix `P=E` and consider compatible bundles `Q` with

\[
x\in Q,\qquad v_q(Q)>b_q,\qquad
\tau_p(Q)\le v_p(y),\qquad
\tau_r(Q)\le v_r(E),\qquad
v_r(U(E,Q))\ge\max\{\tau_r(E),\tau_r(Q)\}.
\tag{16ak.0e}
\]

The family is nonempty at `Q={x}`.  Choose a member maximizing `v_q(Q)` and
take a minimal exact-tail payment.  A `p`-source boundary closes through
`(F,E,Q,{y})`; for `a=p`, an `s`-source closes through
`({y},E,Q,F)`.  The direct EFX checks use both extra ceilings in
(16ak.0e): `r` can hold `E`, and `p={y}` can compare safely to `Q`.

For a surviving `q`-source boundary `F`, the only anchor-preserving
replacement is

\[
Q'=F+\{x\}.
\tag{16ak.0f}
\]

If `Q'` is compatible and its residual is tail-feasible, it contradicts
the maximal choice of `Q`.  Otherwise there are exactly two outputs:

1. a safety failure of `F+x`.  Deleting `x` is safe after excluding a
   simultaneous second source; deleting `z in F` can fail only through a
   desired set
   \[
   x\in A\subseteq(F\setminus\{z\})+x;
   \tag{16ak.0g}
   \]
2. the anchored scalar deficit
   \[
   v_r\bigl((U(E,Q)\setminus F)+(Q\setminus\{x\})\bigr)
   <\max\{\tau_r(E),\tau_r(F+x)\}.
   \tag{16ak.0h}
   \]

Thus the `a=p` row is reduced cap-free to one envied-singleton anchor wall
or one exact `r`-tail deficit.  For `a=q`, the same reduction handles the
`q`-source part of all four orders; the two earlier-`r` `s`-source walls
remain source-specific outputs.  This anchored one-coordinate gate retains
the original `p -f-> r` root and is strictly narrower than the unrestricted
hybrid return lemma.

The exact extremal audit also tests this fixed-`P` potential directly.  Its
structural family is nonempty on 24 of the 28 loaded profiles; the four
exceptions are precisely profiles missing one of the canonical capacity or
compatibility premises.  Each of the 24 has a unique maximizing `Q`, and
all 24 admit a direct exact `R`-tail payment.  This is targeted evidence for
(16ak.0e)--(16ak.0h), not a proof of the anchored scalar gate.

There is a structural suffix operation on the scalar side of the
`q`-source wall.  Before forcing the anchor `x` into the replacement, test
the compatible unanchored pair `(E,F)`.  Its residual is

\[
V=(U(E,Q)\setminus F)+Q,
\qquad
\theta_0=\max\{\tau_r(E),\tau_r(F)\}.
\tag{16ak.0i}
\]

If `v_r(V)>=theta_0`, an exact-tail payment either gives an EFX escape or
reverses to another explicit minimal desired boundary.  Suppose instead

\[
v_r(V)<\theta_0.
\tag{16ak.0j}
\]

The original minimal payment gives `v_r(F)<theta`, where
`theta=max{tau_r(E),tau_r(Q)}`, while the old residual has value at least
`theta`.  Comparing it with (16ak.0j) yields

\[
v_r(Q)<v_r(F)<\theta.
\tag{16ak.0k}
\]

Consequently `theta` cannot equal `tau_r(Q)`, since
`v_r(Q)>=tau_r(Q)`.  Hence

\[
\theta=\tau_r(E)>\tau_r(Q).
\tag{16ak.0l}
\]

Choose a least-`r` good `h in E`.  Then `v_r(E-h)=theta`, and the forced
suffix rotation is

\[
(p,r,q,s)=(\{x,h\},\ E-h,\ F,\ \{y\}).
\tag{16ak.0m}
\]

This allocation is EFX for arbitrary packets.  Its `p` bundle strictly
improves: if `h=f`, positivity gives `v_p(x+f)>b_p`; if
`h in T_r`, (16ar) gives `v_p(x+h)>=v_p(E)>b_p`.

For agent `r`, (16ak.0k) gives
`v_r(x)<=v_r(Q)<theta`, while leastness of `h` gives
`v_r(h)<=theta=v_r(E-h)`; also `v_r(F)<theta`.  Thus all of
`r`'s comparisons are safe.  Agent `q` values `F` above `Q`, so she
can compare to `x`; she can compare to `h` because `h` lies in a deletion
remainder of the common-safe desired set `E`, and hence
`v_q(h)<=b_q<v_q(F)`.

Finally `s` can compare to `h` by the same common-safety argument.  She
also satisfies `v_s(x)<=b_s`: otherwise the ordinary envy edge
`s -> p`, together with the external edge `p -> s` of the `a=p`
cell, would be a zero-charity PI 2-cycle, contradicting global maximality.
Comparisons to `F` and `E-h` follow from common safety.  Therefore
(16ak.0m) closes the scalar `q`-source branch completely; no
anchor-observer or recipient wall remains.

The 14 atomic boundary/pivot cases, including tied least-`r` pivots, replay
as exact QF_LRA-UNSAT in
[`length_three_ap_suffix_atom_exact.json`](length_three_ap_suffix_atom_exact.json).
This is a local audit of the displayed packet proof, not its justification.

Otherwise the only possible failure is an external comparison to a
deletion of `R`.  Within such a deletion perform the same simultaneous
minimal-threshold extraction at

\[
v_p(P),\qquad v_q(Q),\qquad b_s.
\tag{16ak.4}
\]

Agent `r` cannot be the source because every deletion of the minimal
payment has `r`-value below (16ak.3).  If the source is `s` in the hard
`a=r` orbit, `(P,{y},Q,F)` is EFX and Pareto improving: `r` receives the
singleton she envies and `s` receives her desired set.  If the source is
`k in {p,q}`, replace `k`'s provisional bundle `B_k` by `F`.  Minimality
at (16ak.4), together with `v_r(F)<vartheta_r(P,Q)<=b_r`, makes the new pair
compatible and strictly improves one extremal coordinate.  Hence its
residual

\[
U'=(U(P,Q)\setminus F)+B_k
\]

cannot be `r`-tail-feasible.  Every surviving obstruction therefore has
the single exact certificate

\[
v_r(U')<
\max\{\tau_r(F),\tau_r(B_{\{p,q\}\setminus\{k\}})\}.
\tag{16ak.5}
\]

This is the cap-free tail-budget crossing.  It subsumes the `r` half of
(16ak), but with the exact EFX threshold in place of `b_r`; it also bypasses
the canonical overlap split entirely.  A completion now has two equivalent
routes: contradict (16ak.5) for a globally extremal compatible pair, or use
the released bundle `B_k` and a minimal-payment deletion to form a
shorter or adjacent basic cycle.  What is not yet proved is that one of
those routes must always succeed.

The exact replay
[`length_three_lex_tail_adversarial_audit.json`](length_three_lex_tail_adversarial_audit.json)
searches the unrestricted compatible-pair/payment family exactly on the
same 26 frozen adversarial profiles.  Both surviving lexicographic orders
have an EFX escape on every profile, including `V*`; the replay is
byte-identical.
This validates the strict weakening from base mode to tail mode on the
adversarial corpus, but it is not a proof that (16ak.5) is impossible.

The scalar crossing already determines which side must move.  Let `k` be
the source of `F`, let `B_k` be the replaced provisional bundle, and let
`B_l` be the other member of `(P,Q)`.  Since `F subseteq R-g` and `R` is
minimal at (16ak.3),

\[
v_r(F)<\vartheta_r(P,Q).
\tag{16ak.6}
\]

For the replacement pair, put
`vartheta'_r=max{tau_r(F),tau_r(B_l)}`.  Compatibility gives
`vartheta'_r<=vartheta_r(P,Q)`.  Combining (16ak.2), (16ak.5), and
additivity of `U'=U-F+B_k` yields

\[
v_r(B_k)<v_r(F)<\vartheta_r(P,Q),
\qquad
\vartheta_r(P,Q)=\tau_r(B_l)>\tau_r(B_k).
\tag{16ak.7}
\]

Indeed, the residual inequality gives
`v_r(B_k)-v_r(F)<vartheta'_r-v_r(U)<=0`.  If the binding tail belonged to
`B_k`, then `v_r(B_k)>=tau_r(B_k)=vartheta_r(P,Q)`, contradicting
(16ak.6)--(16ak.7).  Thus every tail-budget crossing replaces the
nonbinding bundle and is paid against the other bundle's binding tail.
There is no unordered two-budget wall left.

This identifies the smallest missing operation.  Choose a least-`r` good
`h in B_l`, so

\[
v_r(B_l-h)=\tau_r(B_l)=\vartheta_r(P,Q).
\tag{16ak.8}
\]

The forced three-way pivot rotation is

\[
B_k\longmapsto B_l\text{'s owner},\qquad
B_l-h\longmapsto r,\qquad
F\longmapsto k,
\tag{16ak.9}
\]

with `h` appended to the released bundle `B_k` and `{y}` left at `s`.
If `k=p`, the candidate is

\[
(F,B_l-h,B_k+h,\{y\});
\tag{16ak.10}
\]

if `k=q`, it is

\[
(B_k+h,B_l-h,F,\{y\}),
\tag{16ak.11}
\]

where the displayed order is `(p,r,q,s)`.  Equations (16ak.6)--(16ak.8)
settle `r`'s comparison to `F`, and compatibility/minimality settle every
comparison between `F` and the unaugmented old bundles.  The only new EFX
walls involve the single augmented bundle `B_k+h`; in the `q`-source case
it must also keep the first changed pair owner above base.
There are two orientations to check: the displayed rotation assigns
`B_l-h` to `r` and `B_k+h` to the other provisional owner, while the
reverse matching exchanges those two recipients.  The displayed
orientation can fail either because an external observer sees a deletion of
`B_k+h`, or because its recipient values `B_k+h` below a deletion remainder
of `F` or `B_l-h`.  The latter **recipient-deficit wall** is not implied by
an observer of the augmented bundle and must be retained in the matching
problem.

Thus (16ak.9), not another root choice or a larger fixed menu, is the
smallest operation still missing from the analytic bridge.  It is the
cap-free analogue of the anchored three-good suffix cycle in (16ao).  The
external-observer half of its augmented-bundle wall localizes exactly to the
pivot.  Write

\[
C=B_k+h.
\tag{16ak.12}
\]

If deleting `h` from `C` causes an EFX failure, the only possible observer
is `s`.  The source `k` prefers `F` to `B_k`; agent `r` has
`v_r(B_k)<vartheta_r(P,Q)` by (16ak.7); and the other provisional owner is
the recipient of `C`.  If `s` desires `B_k`, assign `F` to `k`, the original
`B_l` to its owner, `{y}` to `r`, and `B_k` to `s`.  This is EFX: the
replacement pair `(F,B_l)` is compatible, the old pair protects every
comparison to `B_k`, and `r` strictly improves to the singleton she envies.

Now delete a good `z in B_k`.  Any desired set exposed inside
`C-z=(B_k-z)+h` must contain `h`.  Indeed, a subset of `B_k-z` is below the
current bundle of source `k`, below `r`'s value in (16ak.8), and base-safe
for `s`; the recipient of `C` cannot envy her own deletion.  Therefore every
unresolved pivot-rotation failure supplies

\[
h\in A\subseteq (B_k-z)+h
\tag{16ak.13}
\]

for an explicit desired set `A`.

This leaves an exact two-bundle matching gate.  With `F` fixed at its source
and `{y}` fixed at `s`, match

\[
B_l-h,\qquad B_k+h
\tag{16ak.14}
\]

to `r` and the other provisional owner.  A failure of the displayed
matching is either the one-pivot desired edge (16ak.13), the closing
`s`-wall above, or a recipient deficit.  A failure of the reverse matching
has the symmetric recipient/observer form.  The remaining proof obligation
is to prove that one matching works, reverse either failure into the
cap-free two-safe-bundle theorem, or produce an exact state in which both
matchings fail while (16ak.5) holds.  The earlier one-pivot statement alone
does not close the recipient-deficit wall.

### Exact refutation of the one-mode bridge and hybrid repair

The `r`-tail extremal pair by itself is not a universal selector.  The exact
audit
[`length_three_tail_extremal_adversarial_audit.json`](length_three_tail_extremal_adversarial_audit.json)
contains 57 Pareto-maximal `r`-tail pairs across the 26 frozen adversarial
profiles and two exact length-three models.
Nine have no direct `r`-payment EFX allocation.  Seven reverse through an
`s`-source as above, but two have genuine `p/q` boundary blockers and no
recorded pivot orientation succeeds.  These profiles are adversarial tests
of the abstract compatible-pair argument; they are not asserted to satisfy
the length-three topology.

One of the two is the strict atomic profile `fixed_hard_order_3`.  Its unique
Pareto-maximal `r`-tail pair is

\[
P=\{tr,f\},\qquad Q=\{br,tq\},\qquad U=\{bq,x\},
\qquad v_r(U)=\vartheta_r(P,Q)=12.
\tag{16ak.15}
\]

No subset of `U` yields EFX in `r` mode.  The exact reversal exposes
`F={x}` sourced by `q`; the binding-side pivot is `h=f`.  Both orientations
in (16ak.14) fail, and neither gives `p` more than her base.  This is an
exact counterexample to deriving the **one-mode/pivot bridge** from the
compatible-pair inequalities alone, not to a possible length-three
structural strengthening and not to the full escape theorem: the same
profile has an `s`-payment escape.
Thus the smallest missing operation is ownership reversal of `{y}` together
with a base-level payment to `s`.

For the `a=r`, `p/q`-before-`r` sub-tier, the correct global family is
consequently asymmetric.  A compatible pair is feasible in

\[
\begin{array}{ll}
R\text{-mode} & v_r(U(P,Q))\ge
  \vartheta_r(P,Q)=\max\{\tau_r(P),\tau_r(Q)\},\\[2mm]
S\text{-mode} & v_s(U(P,Q))\ge b_s.
\end{array}
\tag{16ak.16}

In `R`-mode keep `s={y}` and pay `r` only at her exact EFX tail threshold.
In `S`-mode give `r={y}` and pay `s` at base.  A completed `R`-mode
allocation closes every `p/q`-before-`r` type because `p,q` improve before
any possible loss of `r`.  The `S`-mode repair is justified here when
`a=r`: `r` improves to `{y}`, while `s` weakly improves and `p,q` improve.
For `a=p` or `a=q`, ownership reversal of `{y}` must instead use the
source-specific all-source rows above; it is not supplied by (16ak.16).
The family is nonempty because `(E,{x})` is `R`-feasible by (16x).

For the two `r`-before-`p,q` types, `R`-mode must instead require
`v_r(U)>=b_r`; `S`-mode still requires `v_s(U)>=b_s` and uses `a=r`, so
`r` improves to `{y}`.  That is the dual-base potential (16ah)--(16al), not
the asymmetric tail potential.  None of the tail-mode audits is evidence
that this earlier-priority requirement can be dropped.

Choose a Pareto-maximal compatible pair over the union of the two modes and
test an inclusion-minimal payment in each mode in which it is feasible.  If
any resulting allocation is EFX, it closes the applicable `a=r` sub-tier.
Otherwise fix a
failing feasible mode and perform simultaneous minimal-threshold reversal at

\[
v_p(P),\qquad v_q(Q),\qquad b_r,\qquad b_s.
\tag{16ak.17}

The payment agent cannot be the source.  The other member of `{r,s}` closes
by exchanging `{y}` with the desired boundary set: in `R`-mode an
`s`-source gives `(P,{y},Q,F)`; in `S`-mode an `r`-source gives
`(P,F,Q,{y})`.  For source `k in {p,q}`, replacement by `F` preserves
compatibility and strictly raises one extremal coordinate.  Maximality then
forces the replacement residual `U'=U-F+B_k` to fail both modes:

\[
v_r(U')<\max\{\tau_r(F),\tau_r(B_l)\},
\qquad
v_s(U')<b_s.
\tag{16ak.18}

This is the exact cap-free **hybrid crossing certificate for the `a=r`,
`p/q`-before-`r` sub-tier**.  It supersedes the one-mode claim there.  The exact audit
[`length_three_hybrid_extremal_adversarial_audit.json`](length_three_hybrid_extremal_adversarial_audit.json)
tests all 54 Pareto-maximal hybrid pairs on the expanded 28-profile corpus.
Every one has a direct EFX payment: the strict countermodel (16ak.15) closes
in `S`-mode, while `V*` closes in `R`-mode.  The zero-failure census is
evidence for (16ak.16), not a packet proof that (16ak.18) is impossible.
In the exact seven-good length-three atom, the source-valid family is forced
for all three singleton sources.  The exact decisions block 4,096 `R`-tail
forms for `a=p`, 8,192 `R`-tail/`S`-base forms for `a=r`, and 4,096
`R`-tail forms for `a=q`; all three formulas are QF_LRA-UNSAT.  See
[`length_three_hybrid_atom_exact.json`](length_three_hybrid_atom_exact.json).
That decision is a discovery/falsification check on the motif only and is
not used as a packet theorem.

#### Canonically anchored hybrid potential

The global pair need not discard the BCFF root data.  Restrict (16ak.16) to

\[
f\in P,\qquad x\in Q.
\tag{16ak.18a}
\]

This anchored family is nonempty because its structural member is
`(E,{x})`.  Choose a Pareto-maximal anchored hybrid-feasible pair and test
both payments exactly as above.  The expanded exact audit contains 52 such
anchored Pareto-maximal pairs and no direct-payment failure.  Thus the
restriction loses none of the observed escapes while preserving the two
distinguished root goods.  This remains corpus evidence, not a theorem.

Analytically, let a failed payment expose `F` sourced by `k in {p,q}` and
write

\[
a_k=\begin{cases}f,&k=p,\\x,&k=q,\end{cases}
\qquad
B_k^-=B_k\setminus\{a_k\}.
\tag{16ak.18b}
\]

The anchor-preserving replacement is

\[
B'_k=F+a_k.
\tag{16ak.18c}
\]

It strictly improves source `k`, remains disjoint from the other anchored
bundle, and has residual

\[
U^a=(U\setminus F)+B_k^-.
\tag{16ak.18d}
\]

If `(B'_k,B_l)` is compatible and either hybrid mode is feasible on `U^a`,
it contradicts anchored maximality.  Hence every surviving anchored
boundary has one of only two forms:

1. **anchor-safety wall:** a deletion of `F+a_k` is unsafe.  Deleting the
   anchor leaves `F`; after excluding a simultaneous second source and the
   already-closing `r/s` source, this is safe.  Deleting `z in F` can fail
   only through a desired set
   \[
   a_k\in A\subseteq(F\setminus\{z\})+a_k;
   \tag{16ak.18e}
   \]
2. **anchored hybrid deficit:** the augmented pair is compatible, but
   \[
   v_r(U^a)<\max\{\tau_r(F+a_k),\tau_r(B_l)\},
   \qquad v_s(U^a)<b_s.
   \tag{16ak.18f}
   \]

Unlike the arbitrary pivot `h`, the sole contested good in (16ak.18e) is
now the actual charity good or envied singleton.  This is the correct input
for the established root-flip, cross-reservoir, and alternating-cycle
operations.  The remaining composition task is to show that each
anchor-containing desired family triggers one of those operations, and
that (16ak.18f) forces such a family when direct compatibility survives.

The scalar return test below applies verbatim to (16ak.18f) after replacing
`F` by the anchored boundary `F+a_k` and replacing `A` in (16ak.23) by
`U^a`.  In particular, put

\[
t_l^a=\max\{b_l,\tau_l(F+a_k)\}.
\tag{16ak.18g}
\]

Because compatibility in the deficit branch makes `B_l` an admissible
endpoint, every inclusion-minimal subset `C subseteq B_l` crossing `t_l^a`
is a valid anchored return.  If neither hybrid budget survives, every such
return is simultaneously above the corresponding `r`-cost cap and
`s`-cost cap.  Thus the live anchored deficit is again one additive demand
against two scalar prices, but its boundary set contains the actual root
good.  This is the precise form to which the parallel-root and alternating
reservoir lemmas must be applied.

The unrestricted hybrid crossing also has a pure packing formulation.  In
(16ak.18), let `l`
be the other provisional owner and put

\[
W=B_k+B_l,
\qquad
t_l=\max\{b_l,\tau_l(F)\}.
\tag{16ak.19}
\]

Call `C subseteq W` an admissible return to `l` when

\[
v_l(C)>b_l,quad v_l(C)\ge\tau_l(F),quad
\tau_k(C)\le v_k(F),quad
\tau_r(C)le b_r,quad
\tau_s(C)le b_s.
\tag{16ak.20}
\]

The admissible family is nonempty: `C=B_l` satisfies (16ak.20) by
compatibility of the old pair and simultaneous minimality of `F`.  For any
admissible `C`, `(F,C)` is a compatible pair that strictly improves source
`k` while preserving the other provisional owner's improvement.  Its
residual is

\[
U_C=U-F+(W\setminus C).
\tag{16ak.21}
\]

Thus maximality says every admissible return simultaneously violates

\[
v_r(U_C)\ge\max\{\tau_r(F),\tau_r(C)\}
\quad\hbox{and}\quad
v_s(U_C)\ge b_s.
\tag{16ak.22}

Conversely, one admissible `C` satisfying either inequality in (16ak.22)
contradicts the extremal choice and completes the hybrid augment.  The live
analytic statement is therefore the following cap-free packing lemma:

> **Hybrid return lemma.** For the boundary set `F` generated by a minimal
> failed payment at a hybrid-extremal pair, the pool `B_k+B_l` contains an
> admissible return `C` for which at least one mode in (16ak.22) survives,
> or an unsafe minimal return reverses to a shorter/adjacent basic cycle.

This is narrower than arbitrary two-bundle matching: one bundle is fixed at
the minimal boundary source, `B_l` is a certified endpoint, and the only
budgets are the exact `r` tail and the `s` base.  It is also the precise
place where the already-proved alternating reservoir exchange may compose
after a root/half-turn transition.  Proving that composition, rather than
another fixed cell, is the remaining global-potential task.

The return lemma has an exact two-row scalar sufficient condition.  It is
enough to search inside the certified endpoint `B_l`.  Put

\[
A=U-F+B_k,\qquad
T_r=v_r(A+B_l),\qquad T_s=v_s(A+B_l),
\tag{16ak.23}
\]

and

\[
\alpha=\min\{T_r/2,\ T_r-\tau_r(F)\},
\qquad
\beta=T_s-b_s.
\tag{16ak.24}
\]

Every `C subseteq B_l` with `v_l(C)>b_l` and
`v_l(C)>=tau_l(F)` is automatically admissible: all four safety conditions
are downward closed from `B_l`, and the source `k` now owns the strictly
better bundle `F`.  If such a `C` satisfies

\[
v_r(C)\le\alpha,
\tag{16ak.25}
\]

then

\[
v_r(U_C)=T_r-v_r(C)
 \ge\max\{\tau_r(F),v_r(C)\}
 \ge\max\{\tau_r(F),\tau_r(C)\},
\]

so `R`-mode survives.  If instead

\[
v_s(C)\le\beta,
\tag{16ak.26}
\]

then `v_s(U_C)=T_s-v_s(C)>=b_s`, so `S`-mode survives.

Therefore a hybrid crossing can remain only if **every** `l`-sufficient
subset of `B_l` is simultaneously expensive in both rows:

\[
v_r(C)>\alpha,\qquad v_s(C)>\beta.
\tag{16ak.27}
\]

This is a one-demand/two-cost threshold obstruction.  Minimizing either
cost subject to the additive `l` threshold is a fractional knapsack with at
most one boundary good.  Hence the only remaining outputs are two scalar
price separators or one critical good in each cost row; an arbitrary Hall
family or a growing solver pool is no longer needed.  The analytic task is
to use the parallel-root/bottom-pool inequalities to rule out the joint
price certificate, or to route either critical good through the alternating
reservoir theorem.

### Joint-split completion of a canonical `q` blocker

The three-good suffix cycle has a cap-free formulation.  Return to the
structural compatible pair `(E,{x})`, where `E=T+f` is inclusion-minimal
for `p`, and put `U=B+X_q`.  Suppose a failed `r`-payment exposes an
inclusion-minimal relative blocker `F subseteq U` sourced by `q`, with

\[
v_q(F)>v_q(x),
\tag{16ap}
\]

and every deletion of `F` below the four moving thresholds

\[
v_p(E),\qquad b_r,\qquad v_q(x),\qquad b_s.
\tag{16aq}
\]

For every `j in T`, minimality of `E` gives

\[
v_p(E-j)\le b_p=v_p(x),
\qquad
v_p(x+j)\ge v_p(E).
\tag{16ar}
\]

Moreover `q`'s base EFX comparison to `X_r` gives
`v_q(j)<b_q<v_q(x)<v_q(F)`.  Hence the two provisional bundles

\[
P_j=\{x,j\},\qquad Q=F
\]

are mutually EFX-safe, strictly improve `p` and `q`, and are base-safe for
`r,s`.  They are disjoint because `F subseteq U` and `T` is disjoint from
`U`.

The exact joint-split payment pool is

\[
H_j=(E\setminus\{j\})+(U\setminus F).
\tag{16as}
\]

If it contains a bundle `Z` satisfying

\[
\begin{aligned}
v_r(Z)&\ge b_r,\\
\tau_p(Z)&\le v_p(P_j),\\
\tau_q(Z)&\le v_q(F),\\
\tau_s(Z)&\le b_s,
\end{aligned}
\tag{16at}
\]

then

\[
(P_j,Z,F,\{y\})
\tag{16au}
\]

is EFX and Pareto improves the base.  Conditions (16ap)--(16ar) check the
comparisons between `P_j` and `F`; (16at) checks every comparison to `Z`;
and both moving bundles are safe for `s={y}`.  This proves the claim without
any packet-size restriction.

Thus a canonical `q` blocker cannot merely be declared incompatible with
the original root.  The correct operation gives one top subgood to `p`,
gives the blocker to `q`, and releases the rest of the old champion bundle
to pay `r`.  Failure has only two exact forms:

1. the total scalar deficit `v_r(H_j)<b_r` for every `j in T`; or
2. every minimal `r`-threshold subset of some adequate `H_j` violates one
   of the three moving ceilings in (16at).

In the second form, minimal reversal again excludes source `r`.  Source
`s` closes by assigning `{y}` to `r`; sources `p,q` strictly improve one
coordinate of the compatible pair and return to the dual-mode extremal
potential.  Hence (16as)--(16at), rather than a fixed placement of `f`, is
the remaining packet-safe joint operation.

The scalar branch has an exact closed form.  Since
`E+U=X_r+X_q+f`,

\[
v_r(H_j)=b_r+v_r(X_q)+v_r(f)-v_r(F)-v_r(j).
\]

Consequently failure for every top good is equivalent to

\[
v_r(F)+v_r(j)>v_r(X_q)+v_r(f)
\qquad(j\in T).
\tag{16av}
\]

It also forces the transversal

\[
F\cap T_q\ne\varnothing.
\tag{16aw}
\]

Indeed, if `F` were disjoint from `T_q`, then

\[
(\{x,j\},T_q+f,F,\{y\})
\]

would be EFX for any `j in T`: the first and third bundles are mutually
safe by (16ap)--(16ar), `T_q+f` is desired by `r` and common-safe, and all
four recipients weakly improve.  Thus the final scalar obstruction is
confined to the overlap of the relative `q` blocker with `r`'s desired top,
not spread through the residual pool.

Put $H=F\cap T_q$ and define the moving deficits

\[
\delta_q^x=v_q(x)-v_q(F\setminus H),
\qquad
\delta_r^f=b_r-v_r((T_q\setminus H)+f).
\tag{16ax}
\]

If $H$ has a partition $H=H_q\mathbin{\dot\cup}H_r$ with

\[
v_q(H_q)>\delta_q^x,
\qquad
v_r(H_r)>\delta_r^f,
\tag{16ay}
\]

then, for every `j in T`,

\[
\bigl(\{x,j\},
      (T_q\setminus H)+H_r+f,
      (F\setminus H)+H_q,
      \{y\}\bigr)
\tag{16az}
\]

is EFX and Pareto improves the base.  The `q` bundle is a subset of `F`
and exceeds `v_q(x)`; the `r` bundle is a subset of the desired common-safe
set `T_q+f` and exceeds `b_r`; and (16ar) protects the `p` bundle.  Therefore
failure of (16ay) is the sole contested-top partition wall for the canonical
`q` blocker.  Its fractional relaxation has one boundary good by the same
price-or-pivot argument below.

When the fractional relaxation is feasible, its boundary-good case
collapses further.  Such a solution supplies a partition

\[
H=H_q\mathbin{\dot\cup}H_r\mathbin{\dot\cup}\{h\}
\]

such that, with

\[
Q_0=(F\setminus H)+H_q,
\qquad
R_0=(T_q\setminus H)+H_r+f,
\]

\[
v_q(Q_0)\le v_q(x)<v_q(Q_0+h),
\qquad
v_r(R_0)\le b_r<v_r(R_0+h).
\tag{16ba}
\]

In fact

\[
H_q=H_r=\varnothing,
\qquad H=\{h\}.
\tag{16ba.1}
\]

To see this, `F` was chosen inclusion-minimal above the `q` threshold
`v_q(x)`.  Thus every proper subset of `F` has `q`-value at most
`v_q(x)`.  Since `Q_0+h` is a subset of `F` and exceeds that threshold in
(16ba), it equals `F`, forcing `H_r=empty`.  Likewise `T_q+f` is a desired
set for `r`, hence every proper subset has `r`-value at most `b_r`.
Because `R_0+h subseteq T_q+f` exceeds `b_r`, it equals `T_q+f`, forcing
`H_q=empty`.  Therefore, in the fractionally feasible branch, the relative
blocker and the selected desired set meet in exactly one good.  Equivalently,
a multi-good overlap can survive only in the fractionally infeasible
ratio-separation branch.  This does not yet eliminate that branch; it
separates it cleanly from the integral rounding obstruction.

There is then a sharper order-valid two-rounding form for the seven
tail-priority types.  In each, `s={y}` may be kept fixed and `p` precedes
both `r` and `q`, so a strict improvement of `p` is lexicographically
decisive; the later agents need not weakly retain their base utilities.  Put

\[
L^r_j=((T_q\setminus\{h\})+f)+G_j,
\qquad
L^q_j=(F\setminus\{h\})+G_j,
\tag{16ba.2}
\]

and define the exact EFX payment thresholds

\[
\theta^r_j=\max\{\tau_r(P_j),\tau_r(F)\},
\qquad
\theta^q_j=\max\{\tau_q(P_j),\tau_q(T_q+f)\}.
\tag{16ba.3}
\]

If a set `Z_r subseteq L^r_j` has `v_r(Z_r)>=theta^r_j` and

\[
\tau_p(Z_r)\le v_p(P_j),\quad
\tau_q(Z_r)\le v_q(F),\quad
\tau_s(Z_r)\le b_s,
\tag{16ba.4}
\]

then `(P_j,Z_r,F,{y})` is EFX and lexicographically improves either
surviving order.  If a set `Z_q subseteq L^q_j` has
`v_q(Z_q)>=theta^q_j` and

\[
\tau_p(Z_q)\le v_p(P_j),\quad
\tau_r(Z_q)\le v_r(T_q+f),\quad
\tau_s(Z_q)\le b_s,
\tag{16ba.5}
\]

then `(P_j,T_q+f,Z_q,{y})` does the same.  These statements are direct EFX
checks.  The first gives the pivot to `q` as part of `F`; the second gives
it to `r` as part of `T_q+f`.  The recipient thresholds in (16ba.3) are
exactly their comparisons to the other displayed bundles.  All comparisons
made by `p` and `s` are (16ba.4) or (16ba.5), while (16ap)--(16ar) protect
the remaining comparisons.  No individual-rationality or Pareto premise is
needed after the first changed lexicographic coordinate.

Consequently, if total value alone defeats both lexicographic roundings,
the exact residual certificate is

\[
v_r(L^r_j)<\theta^r_j,
\qquad
v_q(L^q_j)<\theta^q_j.
\tag{16ba.6}
\]

This strictly sharpens (16be): `theta^r_j<=b_r` and
`theta^q_j<=b_q`, and the two losing-pivot pools include all goods that can
be transferred without disturbing `P_j`, the winning desired set, or
`{y}`.  If a total threshold is met but a minimal payment violates one of
the displayed ceilings, reversing the violating deletion again supplies an
explicit desired set.  Thus the remaining analytic gate inside the
fractionally feasible branch is the two-row tail deficit (16ba.6) plus
those minimal-payment reversals, not base-utility compensation.

For comparison with the earlier Pareto-strength formulation, the residual
currency disjoint from `P_j`, `F`, and `T_q+f` is

\[
G_j=(T\setminus\{j\})+\bigl((B+B_q)\setminus F\bigr).
\tag{16bb}
\]

There are two sufficient compensations.

1. Give `h` to `r`.  If some `C_q subseteq G_j` makes
   `Q_0+C_q` exceed `v_q(x)` and

   \[
   \tau_p(Q_0+C_q)\le v_p(P_j),\quad
   \tau_r(Q_0+C_q)\le v_r(R_0+h),\quad
   \tau_s(Q_0+C_q)\le b_s,
   \tag{16bc}
   \]

   then `(P_j,R_0+h,Q_0+C_q,{y})` is EFX and Pareto improving.
2. Give `h` to `q`.  If some `C_r subseteq G_j` makes
   `R_0+C_r` exceed `b_r` and

   \[
   \tau_p(R_0+C_r)\le v_p(P_j),\quad
   \tau_q(R_0+C_r)\le v_q(Q_0+h),\quad
   \tau_s(R_0+C_r)\le b_s,
   \tag{16bd}
   \]

   then `(P_j,R_0+C_r,Q_0+h,{y})` is EFX and Pareto improving.

All comparisons not displayed in (16bc)--(16bd) follow from
(16ap)--(16ar), because `Q_0+h subseteq F` and
`R_0+h subseteq T_q+f`.  Thus the same pool `G_j` pays either rounding.
If its total value fails both recipient thresholds, the surviving scalar
certificate is

\[
v_q(G_j)\le v_q(x)-v_q(Q_0),
\qquad
v_r(G_j)\le b_r-v_r(R_0).
\tag{16be}
\]

If a total threshold is met but every minimal payment violates a moving
ceiling, minimal reversal produces an explicit relative desired bundle.  On
the `r`-compensation side its source is in `{p,q,s}`; on the
`q`-compensation side it is in `{p,r,s}`.  Source `s` switches `y` to `r`,
sources `p,q` feed the strictly increasing dual-mode pair potential, and
the remaining `r` source returns to the two-demand overlap uncrossing.
Consequently the Pareto-strength outputs (16be) and the `r`-source reversal
are subsumed, for the seven tail-priority types in the fractionally feasible
branch, by the sharper tail deficit (16ba.6) and its minimal-payment
reversals.  The fractionally infeasible ratio-separation output remains
separate.

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
A'=(A\setminus H)+H_q,\qquad
B'=(B\setminus H)+H_r
\]

are disjoint desired bundles for `q` and `r`.  They remain common-safe by
downward closure, and `({x},B',A',{y})` is an EFX Pareto improvement.  Hence
every obstruction must violate the two-demand partition condition (17).
Equivalently, for every `J subseteq H`, at least one of

\[
v_q(J)\le\delta_q,\qquad
v_r(H\setminus J)\le\delta_r
\]

holds.  This is the precise contested-good Hall witness left by the paired
source wall.

### Fractional price-or-pivot lemma

The obstruction in (17) has a cap-free one-dimensional relaxation.  Write
`a_g=v_q(g)`, `c_g=v_r(g)`, and

\[
C=v_r(H)-\delta_r.
\]

Giving a fraction `z_g` of good `g` to `q` and the remaining fraction to
`r` meets the two deficits precisely when

\[
\sum_{g\in H}a_gz_g>\delta_q,
\qquad
\sum_{g\in H}c_gz_g<C.
\tag{18}
\]

Minimize the second sum subject to the first reaching `delta_q`, with
`0<=z_g<=1`.  The fractional-knapsack rule orders goods by decreasing
ratio `a_g/c_g`; an optimum is a prefix with at most one fractional
boundary good.  Consequently exactly one of the following holds (with the
strict thresholds obtained by an arbitrarily small respecting
perturbation):

1. the minimum `r`-cost is at least `C`; equivalently a scalar ratio price
   separates the two demands, so even fractional sharing cannot satisfy
   (17); or
2. a fractional split satisfies (17) and splits at most one good.  If no
   integral partition satisfies (17), all remaining integrality failure is
   therefore localized at that one boundary good.

This is just fractional knapsack, but it materially sharpens the Hall wall:
an arbitrary contested packet is never the irreducible object.  The final
operation must either contradict the scalar price obstruction using the
off-face goods `B_r+B_q+f`, or compensate one recipient for one indivisible
pivot good.  It is not sound merely to round the pivot; either rounding can
violate one of the strict deficits.

For `B=D_r`, equation (16) puts `H subseteq T_q`.  Giving the whole top
packet to `r` and returning `q` to the envied singleton produces the atomic
fallback

\[
(D_p,T_q,\{x\},\{y\}),
\tag{19}
\]

which is EFX exactly when

\[
v_r(T_q)\ge\tau_r(D_p).
\tag{20}
\]

The no-self inequalities imply `v_r(T_q)>v_r(T_r)` and
`v_r(B_r)>v_r(f)`, but they do **not** imply `v_r(T_q)>v_r(f)`.  Thus (20)
is not automatic even when `T_r` is a singleton under the selected-edge
premises.  At the globally maximal atom, however, failure swaps the unique
good of `T_r` with `f`; the new `r` bundle has two goods, so all of its
deletion remainders are singletons and the swap is EFX.  It Pareto improves
`r`, a contradiction.  This—not the two displayed inequalities—is why the
atomic fallback succeeds.  For a genuine packet, a deletion `T_r-g+f` can
likewise exceed `v_r(T_q)`, while the corresponding charity swap can fail
through a second retained good.  Therefore the remaining analytic step is
precisely to use the contested-top quota witness or the extra desired family
exposed by that failure to pay the deletion threshold through a coupled
return; treating `T_q` as one supergood would be unsound.

### Charity-swap transition lemma

The failed fallback has an additional structural consequence.  In any
one-charity partial EFX allocation, suppose `g in X_j` and
`v_j(f)>v_j(g)`.  Replace `g` in `X_j` by `f` and leave `g` unallocated.  If
the resulting allocation is EFX, it Pareto improves `j`.  Otherwise there
are an observer `i != j` and a good `h in X_j-{g}` such that

\[
v_i(X_j-\{g,h\}+f)>b_i.
\tag{21}
\]

Indeed, every bundle other than `j`'s is unchanged.  Deleting `f` from the
new bundle leaves a subset of the old bundle and is base-safe.  Therefore a
violating deletion must remove an old good `h`; self-comparison cannot be
the violation because `j` strictly improves.  Now choose an
inclusion-minimal subset `E` of the left side of (21) that is envied by
*some* agent, and let `k` be such an agent.  Minimality makes `E`
common-safe, so `E` is desired by `k`.  It must contain `f`: without `f`,
it is a proper subset of `X_j` and hence lies inside an old EFX deletion
remainder.  Thus `k` is a genuine `f`-champion of `j`, with a desired set
that omits both `g` and `h`.  The extracted champion `k` need not equal the
original violating observer `i`.

If (20) fails, its maximizing deletion cannot remove `f`, because
`v_r(T_q)>v_r(T_r)`.  Hence it removes some `g in T_r` and gives

\[
v_r(f)>v_r(g).
\tag{22}
\]

Apply the transition lemma to owner `r`.  Global maximality rules out the
EFX-swap branch, so a new genuine edge `k -> r` is forced.  Its source
classifies the remaining obstruction:

1. `k=r` is impossible at global maximality because it is a self-`f`-
   champion and hence a PI cycle;
2. `k=q` creates the two-genuine-edge length-two topology with the selected
   edge `r -> q`;
3. `k=s`, together with the incoming envy edge to `s`, either creates a PI
   shortcut or redirects to a length-three/length-four two-large topology;
4. only `k=p` remains in the same rooted topology, and supplies a second
   `p -> r` desired set omitting the offending good and one deletion
   witness.

In case 4, write `E=T'_r+f` and `B'_r=X_r-T'_r`.  The extracted set is a
valid alternative decomposition of the same `p -> r` edge.  The structural
inequalities and the critical-pool construction reapply with
`B'_r+T_q`: this pool improves `r`, while `p` values it below `E`.
Consequently `p`-, `r`-, and `s`-sourced unsafe reversals are again handled
by the all-source constructions.  The branch is not a separate obstruction;
it enlarges the finite family of admissible `p -> r` decompositions over
which the persistent `q`-source wall may be optimized.  A completion may
select a decomposition by an extremal potential and prove that its
`q`-wall uncrosses.  The transition does not by itself supply that
potential.

### Shortest-cycle routing of the transition

For the residual classification, choose a shortest simple basic cycle
containing at least two genuine `f`-edges.  The length-three cell means that
this shortest length is three.  The sources in the charity-swap transition
then route more sharply than the raw four-way list above.

- A new `q -> r` edge, together with the selected `r -> q` edge, creates a
  length-two two-genuine-edge cycle.  It therefore leaves the length-three
  residual immediately.
- If the new source is `s` and the external envy source is `a=r`, the cycle
  `r -> s -> r` contains only one genuine edge and is PI.
- If the new source is `s` and `a=p`, the edges
  `p -> s -> r -> q -> p` form the adjacent-genuine length-four topology.
- If the new source is `s` and `a=q`, the edges
  `s -> r -> q -> s` form another length-three cycle, now with `p` external.
  In the new normal-form names this swaps the singleton roles `p` and `s`
  while keeping `r,q` fixed.

The last swap changes the four hard `a=q` orders as follows:

| old order | order in the swapped normal form | status |
|---|---|---|
| `(p,r,q,s)` | `(s,r,q,p)` | already closed |
| `(p,r,s,q)` | `(s,r,p,q)` | already closed |
| `(p,s,r,q)` | `(s,p,r,q)` | remains in the hard table |
| `(s,p,r,q)` | `(p,s,r,q)` | remains in the hard table |

Thus a shortest-cycle choice disposes of the `q`-source transition, and the
singleton flip disposes of half of the `s`-source transition orders.  The
irreducible transition orbit consists of the two swapped orders in the last
two rows, the `a=p` adjacent-cycle branch, and a `q`-source contested wall
that persists across the finite family of parallel `p -> r`
decompositions.

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

The nine residual types were also replayed in a strictly weaker structural
cell that requires only the two selected genuine edges, `q -> p`, `a -> s`,
base EFX, charity dominance, and the two genuine-edge nonenvy comparisons.
Every additional envy or champion chord is permitted.  All nine cells remain
exact UNSAT; their minimal menus have size at most six.  See
[`length_three_selected_residual_atomic_cores.json`](length_three_selected_residual_atomic_cores.json)
and its independent exact replay
[`length_three_selected_residual_atomic_cores_audit.json`](length_three_selected_residual_atomic_cores_audit.json).

This proves no packet theorem, but it verifies that the atomic exclusion is
not an artifact of silently imposing the chordless normalization.  In the
analytic BCFF composition, self-champions and edges closing a cycle with at
most one `f` edge are already PI certificates; other extra edges must either
be routed by the all-source lemmas above or assigned to a different residual
topology in the final graph classification.

## Completion requirements

The target is complete only after all of the following are proved:

1. closure of the remaining external-`q` and external-`r` source/order
   types at the correct priority threshold: defeat the two adaptive-
   singleton walls (13)--(14) for the external-`q` types and prove the
   dual-base certificate (16ak) for
   `(s,r,p,q)` and `(s,r,q,p)`.  Equivalently, the canonical tail fallback
   must defeat the fractionally infeasible ratio-separation branch and the
   two-row tail deficit (16ba.6), while the earlier-`r` fallback must retain
   the base threshold;
2. composition of the other charity-swap sources with independently proved
   length-two and adjacent/alternate length-four cycle lemmas;
3. an explicit statement of what the result proves inside the
   exactly-two-nonsingleton reduction and what cases remain outside it.

Until these items are discharged, neither the exactly-two-nonsingleton
closure nor complete four-agent additive EFX is claimed.

## Nonnegative and tie wrapper

Empty packets are handled above.  Zero item values and valuation ties do not
require a separate limiting argument inside the packet proof.  Apply BCFF
Lemma A.1 to replace the original nice additive profile by a nondegenerate
additive profile that respects every strict comparison of the original.
Run the lexicographic-maximality argument entirely in the perturbed profile.
If it yields a complete EFX allocation, that allocation is EFX for the
original valuations: any original strict EFX violation would remain strict
under the respecting perturbation, contradicting perturbed EFX.

Consequently positivity and nondegeneracy may be used for the structural
argument without changing the final existence claim.  What remains is the
mathematical closure of the contested-top cases and the explicit placement
of the resulting length-three lemma inside the other three basic-cycle
classes, not a continuity assumption.

## Primary source

Berger, Cohen, Feldman, and Fiat, *Almost Full EFX Exists for Four Agents
(and Beyond)*, Definitions 2.3 and 2.6--2.7, Definitions 3.1--3.4, and
Lemma 3.5, [arXiv:2102.10654](https://arxiv.org/abs/2102.10654).

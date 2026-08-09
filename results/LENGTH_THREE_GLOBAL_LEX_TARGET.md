# Length-three global-lex target

**Date:** 2026-08-09

**Status:** BCFF basic-cycle classification reconstructed; easy priority
types closed cap-free; contested-top packet-safety gate open

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
v_p(K)<v_p(f),qquad
v_q(K)>v_q(B_q)>v_q(f),qquad
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
v_r(J)<v_r(f),qquad
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

1. a cap-free extremal choice among parallel `p -> r` decompositions that
   closes the scalar-price/pivot `q`-wall in the nine contested
   source/order types;
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

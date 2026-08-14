# Self-core to charity-collision cycle lemma

**Date:** 2026-08-14

**Status:** cap-free analytic reduction; collision conversion remains open

## Theorem

Let `X=(X_1,...,X_n;C)` be a finite partial allocation under positive
additive valuations, normalized so that `v_i(X_i)=1`.  For every target owner
`t`, consider all pairs `(i,B)` satisfying

\[
B\subseteq X_t\cup C,\qquad v_i(B)>1.             \tag{1}
\]

The family is nonempty because positivity gives
`v_t(X_t union C)>1` whenever charity is nonempty.  Choose an
inclusion-minimal support `B_t` among all pairs in (1), and let `sigma(t)` be
one source that desires it.

Then:

1. `B_t` is a physical common-safe desired core for `sigma(t)`;
2. if `sigma(t)=t` for some `t`, `B_t` is a closed one-owner generalized PI;
3. if the source map `sigma` has no fixed point, it contains a directed cycle

   \[
   t_1\mapsto t_2\mapsto\cdots\mapsto t_k\mapsto t_1,
   \qquad 2\le k\le n;                            \tag{2}
   \]

4. the noncharity parts of the cycle cores `B_{t_j}` are pairwise disjoint;
   hence every overlap between two cycle cores is contained in `C`;
5. if the cycle cores are pairwise disjoint, they form a closed physical
   generalized PI; and
6. otherwise, every good of every selected minimal core is pivotal for its
   source:

   \[
   v_{\sigma(t)}(g)\ge v_{\sigma(t)}(B_t)-1>0
   \qquad(g\in B_t).                              \tag{3}
   \]

Consequently, after generalized PI is excluded, the complete obstruction to
these base-plus-charity replacement cores is a directed owner cycle whose
only resource collisions are shared pivotal charity goods.  The statement is
independent of the number of goods in `C` or in any base bundle.

## Proof

For item 1, suppose some observer `h` and good `g in B_t` satisfy
`v_h(B_t-g)>1`.  Then `(h,B_t-g)` is a pair satisfying (1) with strictly
smaller support, contradicting the choice of `B_t`.  Thus every one-good
deletion is worth at most one to every observer, while `sigma(t)` desires the
whole bundle.  This is exactly physical common safety and desire.

If `sigma(t)=t`, every noncharity good of `B_t` is base-owned by the only
source `t`; charity goods are permitted.  Hence the singleton family
`{B_t}` is a closed generalized PI, proving item 2.

If there is no fixed point, the finite functional digraph of `sigma` contains
a directed cycle of length at least two, proving item 3.  The noncharity part
of `B_t` lies in `X_t`, and the base bundles are pairwise disjoint.  This
proves item 4.  Along a cycle, the set of sources equals the set of targets.
If its cores are pairwise disjoint, all their noncharity goods are owned by a
cycle source and their remaining goods are charity goods.  They therefore
satisfy the closed disjoint-core characterization of generalized PI, proving
item 5.

Finally, inclusion minimality says

\[
v_{\sigma(t)}(B_t-g)\le1
\]

for every `g in B_t`.  Subtracting from strict desire gives (3).  Thus any
failure of disjointness is exactly a collision over pivotal charity goods,
not an untyped packet-cardinality obstruction.

## Endpoint-6 interface

In the physically realizable endpoint-6 search, all 135 learned one-owner
cores have precisely the form

\[
B_i=(X_i-R)+C_i,qquad C_i\subseteq G_r,
\qquad v_i(C_i)>v_i(R).                           \tag{4}

There are 11 `r`, 38 `q`, 75 `d`, and 11 `s` witnesses.  The theorem replaces
this finite list by one cap-free object: a fixed-point-free source cycle with
overlap confined to pivotal subgoods of `G_r`.  Once those self cores were
separated computationally, the next model exposed physical PI families on
`{q,r}` or `{d,q,r}`, exactly the collision-free cycle outcome above.

## Exact audit

`audit_self_core_charity_collision_cycle.py` exhausts all fixed-point-free
functions on two, three, and four owners; verifies a directed cycle in every
case; exhausts abstract private-support/three-charity-token intersections and
checks that every cross-core overlap is in charity; and independently proves
the pivotal inequalities (3) by QF_LRA UNSAT checks for core arities one
through eight.

## Claim boundary

Proved: cap-free global-minimum extraction, common safety, self-PI closure,
functional-cycle existence, charity-only collision localization, disjoint
cycle closure, and pivotality.

Not proved: that a pivotal charity collision can always be uncrossed while
preserving all owner payments and the fixed-`U` ledger; that the collision
forces the observed `{q,r}` or `{d,q,r}` physical PI; the universal saturated
rank-three fixed-`U` four-edge theorem; or general additive EFX.

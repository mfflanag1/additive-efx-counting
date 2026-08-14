# Closed disjoint desired-core PI/capture lemma

**Date:** 2026-08-13

**Status:** cap-free generalized-PI construction and exact rank-three
full-capture corollary

## Closed disjoint-core characterization

Let `X` be a partial EFX allocation with charity `U`.  Let `V` be a nonempty
set of owners.  For every `i in V`, let `D_i` be an inclusion-minimal bundle
that is strictly desired by `i` and common-safe at the base floors.  Assume:

1. the bundles `D_i` are pairwise disjoint; and
2. every allocated good in their union has base owner in `V`:

\[
 D_i\cap D_j=\varnothing\quad(i\ne j),
 \qquad
 \bigcup_{i\in V}D_i\subseteq
 U\mathbin{\dot\cup}\bigcup_{j\in V}X_j.        \tag{1}
\]

Then the generalized champion graph of `X` contains a PI cycle on `V`.

Choose any directed Hamiltonian cycle `sigma` on `V` (a self-cycle when
`|V|=1`).  Relabel `D_i` as the generalized edge from `i` to `sigma(i)` by

\[
 H_i=D_i\setminus X_{\sigma(i)},\qquad
 S_i=X_{\sigma(i)}\setminus D_i.                 \tag{2}
\]

The offered bundle `(X_{sigma(i)}-S_i)+H_i` is exactly `D_i`, so minimality
and common safety make this a valid generalized champion edge.  The incoming
packets `H_i` are pairwise disjoint because the `D_i` are.

Take `g in H_i`.  If `g in U`, it is immediately available. Otherwise let
`k in V` be its base owner. The edge entering target `k` is indexed by
`pred(k)`. It cannot be the same edge `i`: if `sigma(i)=k`, then
`g in X_k`, contrary to `g in H_i`. Hence pairwise disjointness gives
`g notin D_pred(k)`, and therefore

\[
                       g\in X_k\setminus D_{pred(k)}=S_{pred(k)}. \tag{3}
\]

Thus every incoming allocated good is released by another cycle edge. All
PI conditions hold. No bound on goods, values, or packet sizes is used.

The converse also holds after canonicalizing each generalized edge to its
actual desired core. In a PI cycle, those cores are pairwise disjoint:
their base-target parts lie in distinct base bundles, their incoming parts
are pairwise disjoint, and an incoming good cannot also remain in another
core because the unique edge targeting its base owner would then fail to
release it. Every noncharity incoming good is released from the base bundle
of a cycle target. Hence every core good has base owner on the cycle or is
in charity, establishing (1).

Therefore generalized PI-cycle existence is **equivalent** to the closed
set-packing condition (1), with one minimal common-safe desired core per
participating source. The cyclic order is arbitrary once that core family
exists; different orders do not define different valuation constraints.

## Rank-three full-capture corollary

Suppose three represented sources `R={r,q,s}` have pairwise-disjoint selected
minimal desired cores `A_i`, as supplied by a rank-three response matching.
Let the unmatched owner `d` have any common-safe desired core `C`. Put

\[
 A=\bigcup_{i\in R}A_i,qquad C_0=C\setminus A.  \tag{4}
\]

If `C_0` is still desired by `d`, choose a minimal desired
`D_d subseteq C_0`.  Then the four cores `(A_r,A_q,A_s,D_d)` are pairwise
disjoint, and their base-owner closure is automatically contained in all
four owners plus charity.  The theorem with `V=N` yields a generalized PI
cycle. Consequently, in a generalized-PI-free state,

\[
                         v_d(C\setminus A)\le F_d,              \tag{5}
\]

where `F_d` is the strict response floor of `C`. If

\[
                         \mu_d=v_d(C)-F_d>0,                    \tag{6}
\]

then additivity gives the exact global capture inequality

\[
                         v_d(C\cap A)\ge\mu_d.                 \tag{7}

\]

Thus the disjoint-response branch of the rank-three gate is not merely a
four-edge allocation candidate: it is impossible under full generalized
PI-freeness. Every survivor has **full response-margin capture by the union
of the three selected cores**.

There is also a three-source provenance consequence. Applying the theorem
to `(A_i)_{i in R}`, PI-freeness forces at least one selected core to contain
a good whose base owner is `d`. Hence the captured-own-support polarity is
structural, not an artifact of the residual-split atomization.

## Verification and remaining boundary

`audit_closed_disjoint_desired_core_pi_capture.py` exhausts every nonempty
owner subset, every cyclic order, and every assignment of labeled goods to
pairwise-disjoint cores under the closure premise. It independently verifies
incoming disjointness and exact release coverage. QF_LRA separately checks
the full-margin implication (5)--(7).

The lemma does not reverse the capture inequality. The remaining universal
gate is now exact: return captured `d` support while compensating the selected
core sources, or prove that repeated compensation creates another disjoint
closed desired-core family, response/support growth, or a four-edge EFX
endpoint.

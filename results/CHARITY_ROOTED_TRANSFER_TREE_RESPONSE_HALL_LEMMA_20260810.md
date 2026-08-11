# Charity-rooted transfer-tree response-Hall lemma

**Date:** 2026-08-10

**Status:** cap-free analytic component theorem; flower-specific tree
selection and terminal Hall deficiency remain open

## Transfer tree

Let `(X,{f})` be a partial EFX allocation for positive additive agents.
Choose a nonempty owner set `T` and a rooted directed tree on `T`, oriented
away from root `h`.  For every arc `u -> v`, choose a nonempty packet

\[
R_{uv}\subseteq X_u,
\]

with packets on distinct arcs pairwise disjoint.  Give `f` to the root and
transfer every arc packet from its parent to its child.  Thus

\[
Y_h=X_h\setminus O_h+f,
\]

and, for every nonroot `v`,

\[
Y_v=X_v\setminus O_v+R_{p(v),v}, \tag{1}
\]

where

\[
O_u=\mathbin{\dot\bigcup}_{u\to w}R_{uw}.
\]

Owners outside `T` are fixed.  Since every removed packet is assigned to
its child and `f` is assigned to the root, (1) is a complete allocation.
Assume every owner in `T` strictly prefers `Y_u` to `X_u`.

Stars, paths, and a hub followed by a donating leaf are all special cases.
No bound is imposed on any packet cardinality.

## Exact release support

View each `Y_u` as a response target relative to the base allocation `X`.
Its incoming and prescribed-release sets are

\[
I_h=\{f\},
\qquad
I_v=R_{p(v),v}\quad(v\ne h), \tag{2}
\]

\[
O_u=\mathbin{\dot\bigcup}_{u\to w}R_{uw}. \tag{3}
\]

The incoming sets in (2) are pairwise disjoint.  The root incoming good is
initially unallocated.  Every other incoming packet is contained in the
release set of its unique parent target.  Consequently

\[
\bigcup_{u\in T}I_u
\subseteq
\{f\}\cup\bigcup_{u\in T}O_u. \tag{4}
\]

This remains valid if a most-envious desired subset discards additional
goods: additional discard only enlarges the available release set.

## Response-Hall theorem

For each target `Y_u`, let `C_u` be its set of most-envious response sources
relative to `X`.  These sets are nonempty because the intended owner
strictly desires the target.  Restrict them to internal sources in `T`.

1. If the internal response relation has a system of distinct
   representatives, select one distinct source for every target.  The
   resulting directed response graph is a permutation of `T`, hence a
   disjoint union of cycles.  By (2)--(4), its incoming sets are disjoint
   and internally supplied, so the cycles form a BCFF Pareto-improvable
   edge set.
2. If there is no internal SDR, a target with no internal source exposes an
   owner outside `T` and strictly grows the component.  Otherwise Hall's
   theorem supplies an inclusion-minimal deficient target set.
3. If `Y` itself is EFX, it is a complete Pareto improvement of `X` and is
   already the required contradiction to global lexicographic maximality.

Thus a selected improving transfer tree has exactly three outcomes: an EFX
improvement, a release-compatible PI edge set, or a named open/Hall-
deficient response boundary.

## Flower specialization

The two hardened flexible-flower profiles escape through depth-two transfer
trees, not through a bounded-radius accident.

- One has root `r`, arcs `r -> q`, `r -> c`, and `c -> s`.
- After genuine-self and one-genuine-edge PI cycles are excluded, the
  hardened profile has root `q`, two goods on `q -> c`, and one good on
  `c -> s`, while `r` is fixed.

The latter is exactly the topology suggested by a Q-exhausted compensation
leaf: `q` values the charity above the terminal external bundle, replaces a
low packet by `f`, and routes that packet through the other external owner
to the singleton.  Its frozen allocation is EFX even though its response
relation has no internal SDR.  Hence the analytic continuation must test
the EFX endpoint before interpreting Hall deficiency as failure.

The finite support audit
[`charity_rooted_transfer_tree_release_audit.json`](charity_rooted_transfer_tree_release_audit.json)
checks every labeled rooted tree and every internal response permutation for
one through four owners: 405 tree/permutation pairs in total.

## Claim boundary

This lemma proves release compatibility and finite response classification
for every selected charity-rooted transfer tree.  It does not prove that a
Q- or R-exhausted flower leaf always supplies owner-improving arc packets,
that one selected tree is EFX, that every response relation has an internal
SDR, eliminate a terminal Hall defect, close the `GG` flower, or prove
four-agent additive EFX.

# Genuine mixed-edge Hamiltonian interface

**Date:** 2026-08-13

**Status:** cap-free reconstruction from the BCFF response definitions and
the paid-state matching endpoint; the previous one-decorated shorthand was
not universal

## Base and paid state

Let `X` be the globally lexicographically maximal partial EFX base.  Let
`Y` be one exact paid splice state:

\[
 v_i(Y_i)\ge v_i(X_i),
 \qquad
 \Delta_i=v_i(Y_i)-v_i(X_i)\ge0.                 \tag{1}
\]

The five current physical targets are the four pairwise-disjoint owner
bundles `Y_i` and current charity `Y_c`.

There are two kinds of response cores at this fixed state.

1. An **old core** `A` is desired relative to `X` and base-common-safe:

   \[
   v_s(A)>v_s(X_s),\qquad
   \tau_h(A)\le v_h(X_h)\quad(h\in N).            \tag{2}
   \]
2. A **decorated core** `D` is desired and safe only relative to `Y`:

   \[
   v_s(D)>v_s(Y_s),\qquad
   \tau_h(D)\le v_h(Y_h).                         \tag{3}
   \]

Its exact positive base-debt rows are

\[
 B(D)=\{h:\beta_h(D)>0\},\qquad
 \beta_h(D)=(\tau_h(D)-v_h(X_h))_+.               \tag{4}
\]

Equation (3) gives, for every `h`,

\[
 0\le\beta_h(D)\le\Delta_h,                      \tag{5}
\]

and a row is positive only if `Delta_h>0`.  The complete signed decoration
of `Y` fixes these rows and the physical gains that pay them.  Their
identities are valuation data; graph position alone does not determine
them.

## How many decorated matching edges?

Select a rank-four matching of response sources to four distinct current
targets.  Let `kappa` be the minimum number of decorated edges among such
matchings.

- `kappa=0` is impossible at global maximality: the four disjoint old cores
  form a partial EFX allocation strictly improving all four sources.
- `kappa=4` closes by the current-safe matching endpoint: all four sources
  receive cores strictly above `Y`, and every core is safe against `Y`.
- A genuine mixed survivor therefore has

  \[
  \kappa\in\{1,2,3\}.                             \tag{6}
  \]

Nothing in the BCFF definition, full-state reconstruction lemma, or
five-target matching lemma forces `kappa=1`.  Multiple decorated responses
may have accumulated at the same exact signed state.  The old manuscript's
four-old-core path was impossible, while replacing it silently by exactly
three old cores would still omit the `kappa=2,3` branches.

The audit gives the smallest graph countermodel to the singular claim: the
Hamiltonian edges at positions zero and two are decorated, those at one and
three are old, and no other response edges exist.  The old rank is two, the
full rank is four, and every rank-four matching uses both decorated edges.
This is an abstract response-interface countermodel, not a globally maximal
GG valuation profile.  It proves that a separate provenance lemma—such as a
rank-three old Hall defect augmented for the first time by its missing
source—is required to force `kappa=1`.

## The requested one-decorated branch

When `kappa=1`, the matching contains exactly three simultaneously physical
old cores and one decorated core.  In the PI-free graph-level branch it is a
Hamiltonian path

\[
 h_0\longrightarrow h_1\longrightarrow h_2
 \longrightarrow h_3\longrightarrow c.           \tag{7}

There is a unique position `p in {0,1,2,3}` whose selected edge is
decorated:

\[
 h_p\longrightarrow
 \begin{cases}
 h_{p+1},&p<3,\\
 c,&p=3.
 \end{cases}                                      \tag{8}

Call its core `D` and its source `d=h_p`.  Every other selected edge has an
old core `A_i`.  The mixed observer-payment separator is exactly a row
`h != d` with

\[
 m_h<\beta_h(D)\le\Delta_h,
 \qquad m_h=v_h(A_h)-v_h(X_h).                    \tag{9}

Thus (8), (4), and (9)—not a generic phrase such as “the mixed edge”—are
the complete scalar interface.

In the anchored GG branch, the permanent edge `r -> q` is old.  Hence it
cannot be (8).  Across the six anchored paths there are exactly eighteen
possible locations for the unique decorated edge: three nonanchor positions
per path.  The identities are not reduced further by graph structure.

## A distinct closing edge into the hole

The matching hole is the owner target `Y_{h_0}`.  A later old exact response

\[
 E\subseteq Y_{h_0}
 \quad\text{from source }s=h_k,quad k\in\{1,2,3\}, \tag{10}

may be decorated/current-safe at the same paid state.  It is not the
selected `D` in (8): `D` lies in a matched target, whereas `E` lies in the
unmatched hole target, so

\[
 D\cap E=\varnothing.                             \tag{11}

Pivoting (10) closes the prefix cycle.  That cycle contains selected `D`
exactly when `p<k`.  When `p>=k`, the selected mixed edge lies outside the
prefix; the closing edge `E` is itself the only decorated edge on that
cycle.  The old manuscript used one letter for these two logically distinct
objects and then treated every selected path core as old.

## Physical incoming and release table

Let `K_i=D` for `i=d` and `K_i=A_i` otherwise.  For every nonhole owner
target `h_j`, `j=1,2,3`, its incoming selected core and released residual are

\[
 C_{h_j}=K_{h_{j-1}},\qquad
 R_{h_j}=Y_{h_j}\setminus C_{h_j}.                \tag{12}

The last selected core `K_{h_3}` lies in charity; its charity complement is
released.  The hole target decomposes independently as

\[
 Y_{h_0}=E\mathbin{\dot\cup}H.                    \tag{13}

Consequently:

1. all four selected cores are pairwise disjoint;
2. `E`, `H`, and every selected core/residual are pairwise disjoint across
   their parent targets;
3. `K_i` is disjoint from the residual `R_i` of source `i`'s own target,
   because (7) has no self edge;
4. the unique incoming mixed target is the head of (8), when `p<3`; if
   `p=3`, the mixed core is supplied by charity;
5. the signed base provenance is not erased: for every owner target `j`,
   `Y_j=(X_j\setminus O_j) dotunion I_j`, so every core and residual has the
   exact retained/incoming split obtained by intersecting it with
   `X_j\setminus O_j` and `I_j`.

Item 5 is the physical release label needed for PI.  Target disjointness
proves allocation feasibility; internal supply additionally requires the
cycle's incoming intersections with the signed `I_j` packets to be released
by another selected edge or charity.

## Correct interface boundary

The paid-response program must now branch before deletion return:

1. `kappa=1`: use the three old cores, selected decorated `D`, distinct hole
   response `E`, both debt vectors, and the release table (12)--(13);
2. `kappa=2,3`: retain one debt vector for every decorated matching edge and
   solve the corresponding multi-decorated budget matching; and
3. any claimed PI cycle must check the signed incoming/release intersections,
   not merely core disjointness.

This reconstructs the genuine interface.  It does not prove that every
fixed state has `kappa=1`, solve the multi-decorated branches, pay the two
decorated cores in the one-decorated deletion-return branch, close GG, or
prove four-agent/general additive EFX.

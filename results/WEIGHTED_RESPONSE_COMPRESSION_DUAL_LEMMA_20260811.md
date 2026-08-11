# Weighted response-compression dual lemma

**Date:** 2026-08-11

**Status:** cap-free analytic selector and exact obstruction certificate;
elimination of the weighted certificate remains open

## Minimum-cost compression

Use a minimal all-owner Hall defect and its three-source neighborhood `S`
from the response-compression lemma. Let `d` be the unique missing source.
For every response edge `i -> j`, let `D_ij` be the finite nonempty family
of common-safe desired response cores carried by that edge, and define its
cost in the missing source's row by

\[
w_{ij}=\min_{A\in D_{ij}}v_d(A). \tag{1}
\]

Adjoin a dummy source `delta` with a zero-cost edge to every target. A
perfect matching of the augmented four-by-four graph selects three distinct
real response edges and uses the dummy edge on the omitted target. Such a
matching always exists, and every prescribed real response edge can be
forced into one, by the deficiency-one response-compression lemma.

Put

\[
B_d=v_d(f)+\sum_{k\ne d}v_d(X_k). \tag{2}
\]

For a matching `M`, choose a minimum-cost core on each of its three real
edges and give every residual good to `d`. The residual has exact value

\[
v_d(W_M)=v_d(X_d)+B_d-
\sum_{(i,j)\in M,\ i\ne\delta}w_{ij}. \tag{3}
\]

Consequently `d` is weakly nonworse exactly when the matching cost is at
most `B_d`. Choosing a minimum-cost augmented perfect matching is therefore
the canonical global packet selector. It is cap-free: item cardinality
enters only through the finite minimum in (1).

When the minimum cost is at most `B_d`, the three real sources strictly
improve and `d` is weakly nonworse. Every selected core is common-safe, so
the compressed allocation has at most one EFX wall: the residual target
`W_M`. An EFX endpoint is the required lexicographic improvement, while a
response SDR is a release-compatible generalized PI edge set.

## Exact weighted obstruction

If no response compression pays the missing source, then every augmented
perfect matching has cost strictly above `B_d`. By integrality and strong
duality of the bipartite assignment polytope, this is equivalent to dual
potentials `alpha_i` on the three real sources and the dummy source, and
`beta_j` on the four targets, satisfying

\[
\alpha_i+\beta_j\le w_{ij}
\quad\text{on every real response edge}, \tag{4}
\]

\[
\alpha_\delta+\beta_j\le0
\quad(j\in N), \tag{5}
\]

and

\[
\sum_i\alpha_i+\sum_j\beta_j>B_d. \tag{6}
\]

Thus a terminal all-owner Hall obstruction is not an unstructured family of
packet failures. It has an exact weighted assignment certificate in one
valuation row. To close the flower bridge it is enough to contradict (4)--
(6) using the flower inequalities, or to use those potentials to select a
new root.

The same statement holds with one prescribed response edge by restricting
the primal to augmented matchings containing it. This is the anchored form
needed to retain a particular sink-capturing response.

## One-wall recapture

Assume a paid compression has selected cores `A_i`, residual `W`, and
missing-source margin

\[
\gamma_d=v_d(W)-v_d(X_d)\ge0.
\]

If source `i in S` responds to the sole wall target `W` with common-safe
desired core `D subseteq W`, replace

\[
Z_i=A_i,\quad Z_d=W
\]

by

\[
Z'_i=D,\quad Z'_d=A_i+(W\setminus D). \tag{7}
\]

All other cores remain fixed. This is complete, source `i` still strictly
improves, and the missing source remains weakly nonworse exactly when

\[
v_d(D)-v_d(A_i)\le\gamma_d. \tag{8}
\]

When (8) holds, the new state again consists of three common-safe desired
cores and one residual target, so it preserves the one-wall normal form.
Failure is the strict recapture wall

\[
v_d(D)>v_d(A_i)+\gamma_d. \tag{9}
\]

Take the finite closure of the initial paid compressions under recaptures
(7) that preserve weak payment, and choose a state maximizing `v_d(W)` in
that closure. Every response core `D` with `v_d(D)<v_d(A_i)` is then
excluded, because (7) would strictly increase the residual. Nondegeneracy
turns the remaining comparison strict. Hence a maximal terminal state has a
fully oriented dependency: every recapturing core is more valuable to the
missing source than the source-owned core it would replace, and (9)
identifies those that also exhaust the entire residual margin.

The scalar identities, one-wall implication, recapture threshold, and weak
assignment-dual inequality replay in
[`weighted_response_compression_dual_audit.json`](weighted_response_compression_dual_audit.json).

## Claim boundary

This lemma gives the cap-free minimum-cost selector, exact weighted dual,
and a one-wall-preserving recapture operation. It does not contradict the
dual certificate, prove that every recapture satisfies (8), orient a root
change when (9) holds, prevent a sequence of margin-decreasing recaptures,
close the `GG` flower, or prove four-agent additive EFX.

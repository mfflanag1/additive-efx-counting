# Alternating two-head root-covered compression lemma

**Date:** 2026-08-13

**Status:** cap-free reduction of every alternating two-head protected Hall
cut to the existing one- or two-residual compression normal forms

## Anchored alternating topology

Let the supplier-saturated mixed cycle contain the permanent old edge

\[
 r\longrightarrow q.
\]

The only topology with two decorated heads is the alternating edge word
`D,O,D,O`.  Since the edge leaving `r` is old, the edge entering `r` is
decorated.  Therefore `r` is itself one of the two heads.  Write

\[
 H=\{r,h\}.                                      \tag{1}
\]

Let `Z` be the paid residual-completed candidate, let `X` be the globally
maximal base, and define the protected thresholds

\[
 \lambda_i=\max\{v_i(X_i),\max_j\tau_i(Z_j)\}.   \tag{2}

Every nonhead has its identity acceptance edge.  Each head has a nonempty
nonidentity acceptance row, and every accepted edge `i -> j` admits an
inclusion-minimal packet `A_i subseteq Z_j` satisfying

\[
 v_i(A_i)\ge\lambda_i,
 \qquad \tau_k(A_i)\le\lambda_k\quad(k\in N).     \tag{3}

For a nonhead edge the whole accepted target may be used.  Thus every
matching in the protected graph lifts to pairwise-disjoint protected
response cores.

## A maximum matching can cover the root

Suppose the protected graph has no perfect matching.  Its maximum matching
rank is at least two because the two nonheads have distinct identity edges,
and at most three.  Since the root row is nonempty, some maximum matching
covers `r`: if a maximum matching leaves `r` unmatched, take any edge
`r -> t`.  Target `t` must be matched, or the matching was not maximum;
replacing its matched edge by `r -> t` preserves the rank and covers `r`.

Choose such a root-covered maximum matching and lift it using (3).  The root
receives at least `lambda_r`.  Because `r` is a blocking head,

\[
 \lambda_r>v_r(Z_r)>v_r(X_r),                    \tag{4}

so every EFX endpoint below is a strict fixed-priority lexicographic
improvement even if every unmatched later owner loses.

## Rank-three branch

If the matching rank is three, give the three protected cores to their
sources and give their exact complement `W` to the unique unmatched owner
`d`.  The root is represented, hence `d != r`.  Every represented source
pays every selected core, and `d` is automatically safe against her own
residual.  Therefore an EFX failure is exactly either

1. `d` against a selected core; or
2. a represented source against `W`.

This is the priority-valid two-sided three-core/one-residual compression
star.  No payment premise for `d` is needed.

## Rank-two branch

If the matching rank is two, retain its two protected cores and pool every
remaining good for the two unmatched owners.  Apply the finite maximin
cut-and-choose partition to that pool.  The two holes are mutually EFX.
Every represented source pays both selected cores, so every remaining wall
is exactly either

1. a hole against a selected core; or
2. a represented source against a residual cell.

This is the two-core/two-residual response-Hall normal form.  Its two
opposite `2 x 2` response blocks either match, yield a release-compatible
cross-block PI cycle, or expose the already-named empty-target/source-
inactive or lower-dimensional recurrence.  Supplier saturation supplies
the physical owner union; it is not used as an observer-payment inequality.

## Consequence

The alternating two-head protected Hall cut is not an independent packet
gate.  Every such graph has exactly one of three outcomes:

1. a perfect protected matching, hence an EFX lexicographic contradiction;
2. a root-covered rank-three compression star; or
3. a root-covered rank-two cut-and-choose Hall boundary.

Together with the one-head nonroot handoff, all non-root-facing decorated-
head Hall failures enter the existing compressed response/star recurrence.
The only direct one-head exception remains `N(h)={r}` for `h != r`.

## Claim boundary

This lemma proves the anchored head identity, root-covered maximum matching,
rank-two/rank-three exhaustion, lexicographic validity, and wall
localization without an item or value cap.  It does not terminate the
compressed star or empty-target recurrence, eliminate the one-head
root-facing row, eliminate root-sourced complete-residual-pool capture,
close GG, or prove four-agent/general additive EFX.


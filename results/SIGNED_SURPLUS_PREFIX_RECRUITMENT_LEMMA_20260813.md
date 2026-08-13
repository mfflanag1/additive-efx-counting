# Signed-surplus predecessor-prefix recruitment lemma

**Date:** 2026-08-13

**Status:** cap-free recruitment of every underfunded old matching source;
the terminal is a full-prefix recurrent current-response/rank interface, not
the previously claimed selected-pool separator

## State and correction

Let `X` be the globally lexicographically maximal partial EFX base and let
`Y` be one exact paid state, so

\[
 v_i(Y_i)\ge v_i(X_i)\qquad(i\in N).              \tag{1}
\]

Fix the genuine PI-free mixed Hamiltonian matching

\[
 h_0\longrightarrow h_1\longrightarrow h_2
 \longrightarrow h_3\longrightarrow c.           \tag{2}
\]

The selected core of source `h_i` is `K_i`; it lies in target `Y_{h_{i+1}}`
for `i<3` and in current charity for `i=3`.  Each `K_i` is either old
base-common-safe and desired above `X_{h_i}`, or decorated current-safe and
desired above `Y_{h_i}`.

The former complete-pool local obstruction is not in the post-residual
terminal.  In its exact valuation table the alleged fixed old observer has
utility `11` but sees the original decorated three-good core at threshold
`12`, and the alleged hole owner has utility `12` while that core's threshold
is only `8`.  Thus the old observer should already have entered the residual/
incoming-core branch, while the required hole-row inequality is false.  The
262,144 null partitions are a correct census of that local table but do not
certify the stated separator.

## Predecessor-closed recruitment

For `j in {0,1,2,3}`, define the prefix-retention candidate `Z^(j)` by

\[
 Z^{(j)}_{h_i}=\begin{cases}
   Y_{h_i},&i\le j,\\
   K_i,&i>j.
 \end{cases}                                      \tag{3}
\]

Every good not appearing in (3) remains unallocated.  This is the correct
physical operation for recruiting the realized signed surplus of source
`h_j`: retain not a scalar credit but the entire current target that realizes
it, and retain every predecessor target needed to avoid collision with its
incoming selected core.

### Feasibility and floors

The bundles in (3) are pairwise disjoint.  Retained targets have indices at
most `j`; every allocated selected core has source index greater than `j` and
therefore lies in a target of index greater than `j` or in charity.  Equation
(1) pays every retained owner weakly above base, while every suffix source is
strictly above base on its desired selected core.  Hence `Z^(j)` is
priority-valid, and is a strict lexicographic improvement whenever `j<3`.
For `j=3`, strictness is exactly the strictness already present in the paid
state `Y`.

The operation preserves the full signed provenance of every retained target:

\[
 Y_i=(X_i\setminus O_i)\mathbin{\dot\cup}I_i.     \tag{4}
\]

It also preserves the permanent root-to-q anchor as a physical labeled core.
If `Y_q` is retained, the anchor remains inside its unchanged target.  If it
is not retained, the core remains in the unretained q target (allocated only
when its source is still in the suffix).  No prefix operation cuts or
duplicates the anchor core.

### Exact failure types

Consider an EFX failure in `Z^(j)`.

1. An old suffix core is base-common-safe, so no base-paid observer can fail
   against it.
2. Every retained-prefix owner receives `Y_i` and therefore pays every
   decorated suffix core by current safety.
3. Every decorated suffix owner receives a core worth strictly more than her
   own `Y_i`, and likewise pays every decorated suffix core.

Consequently a failure against a selected suffix core can only be made by an
**old suffix source** against a decorated suffix core.  Recruiting that
source replaces `j` by its strictly larger path position.  Thus this failure
causes a strict increase of the finite prefix coordinate.

Every other failure is against a retained current target `Y_{h_l}`, `l<=j`.
If the failing source is retained or is a decorated suffix source, its own
bundle is worth at least its current target, so a globally minimal desired
subcore of `Y_{h_l}` is a genuine current response with its complete signed
target/release label.  If the failing source is an old suffix source, recruit
it first; this again strictly increases the prefix coordinate.

## Recruitment theorem

Starting from any `j`, repeat the following operation:

1. if an old suffix source is underfunded, extend the retained prefix through
   that source;
2. otherwise, if `Z^(j)` is EFX, stop at an EFX lexicographic improvement;
3. otherwise extract the labeled current response into the retained prefix.

The first operation can occur at most three times.  It preserves physical
disjointness, every base floor, the signed target provenance, and the
permanent anchor.  Therefore every genuine mixed Hamiltonian state reaches
one of:

1. an EFX lexicographic improvement;
2. a new current-response/core/target/release record, which is strict finite
   augmentation;
3. an old current response into the retained prefix; or
4. full prefix `j=3`, namely the exact paid state `Y`, together with a
   recurrent current response.

For an old response from path position `k` into retained target position
`l`, `k>l` closes the selected path segment `[l,k]`.  Its cores are physically
disjoint.  The cycle is release-compatible exactly when every incoming
intersection from (4) is supplied by charity or released by another edge of
that segment.  Failure names an outside supplier and strictly grows the
signed owner component until all four owners are represented.  A response
with `k<l` is a forward chord; it does not by itself form a cycle and must be
handled by an anchored matching/root-order change.

Thus component recruitment itself is cap-free and well-founded.  The exact
survivor is narrower than the former pool separator:

> a full-prefix, full-owner exact signed state with an old recurrent current
> response whose backward segment is already supplier-saturated but not
> observer-paid, or whose edge is a forward chord not yet converted into an
> anchor-preserving strict matching transition.

## Claim boundary

This lemma proves the recruitment, disjointness, floor, provenance, anchor,
and finite-prefix assertions.  It does not prove observer payment of a
supplier-saturated mixed cycle, convert every old forward chord into a strict
anchored transition, derive the final root/q inequality, close GG, or prove
four-agent/general additive EFX.

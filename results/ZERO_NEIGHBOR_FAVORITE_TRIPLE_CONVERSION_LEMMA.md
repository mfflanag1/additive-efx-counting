# Zero-Neighbor Favorite-Triple Conversion Lemma

**Status:** cap-free analytic lemma; the global motif-selection step remains open  
**Scope:** four additive agents and nine goods with a strict common favorite  
**Role:** converts a universally rejected Hall edge into a favorite-pair EFX
allocation

## Statement

Let (f) be a strict favorite of every agent and write (F_i=v_i(f)).
Partition the other eight goods as two low goods (h,\ell) and three pairs
(E=\{x,y\},P,Q). Assume that every agent (i) satisfies

\[
v_i(h)\ge v_i(\ell),
\qquad
v_i(E)<F_i+v_i(h),                                      \tag{1}
\]

\[
v_i(E)+v_i(\ell)\ge F_i,                               \tag{2}
\]

and, for (R=P,Q),

\[
v_i(R)\ge
M_i:=\max\!\left\{
F_i,
v_i(E),
v_i(\ell)+\max\{v_i(x),v_i(y)\}
\right\}.                                               \tag{3}
\]

Then the partition

\[
\{f,h\}\mid E\cup\{\ell\}\mid P\mid Q               \tag{4}
\]

is EFX under every assignment of its four bundles to the four agents. In
particular, it supports a complete EFX allocation.

Condition (1) says that (E) is a zero-neighbor edge in the
favorite-triple Hall graph for lows (h,\ell), with a common orientation of
those lows. The lemma complements the one-defect conversion lemma: here
(E) may be rejected by all four agents rather than by only one.

## Proof

Fix an observer (i). The largest value left after removing one good from
each target bundle in (4) is at most (M_i):

- removing one good from ({f,h}) leaves at most (F_i), because (f)
  is the strict favorite;
- the three two-good remainders of (E\cup\{\ell\}) have values
  (v_i(E)), (v_i(\ell)+v_i(x)), and (v_i(\ell)+v_i(y)); and
- removing one good from (P) or (Q) leaves a residual singleton worth
  strictly less than (F_i).

The bundles (P,Q) have value at least (M_i) by (3). The triple
(E\cup\{\ell\}) dominates its own three two-good remainders and has value
at least (F_i) by (2), so it also has value at least (M_i).

Finally, ({f,h}) has value (F_i+v_i(h)). It dominates (F_i); it
strictly dominates (v_i(E)) by (1); and it strictly dominates
(v_i(\ell)+\max\{v_i(x),v_i(y)\}), because
(v_i(h)\ge v_i(\ell)) and every residual good is worth strictly less than
(F_i). Thus it too has value at least (M_i).

Every bundle is therefore EFX-feasible for every agent. Any bijection of
agents to bundles is EFX. \(\square\)

## Why this is the live conversion motif

Two independently found hard-branch profiles have exactly 15
EFX-supporting unlabeled partitions in total. All 15 are balanced and every
one has a complete agent--bundle feasibility graph. In each profile:

- the single cell with lows ({7,8}) has 12 Hall-valid perfect pairings
  and three failed pairings;
- the three failed pairings all contain one common zero-neighbor edge;
- the low pair has a common strict orientation across all four agents;
- conditions (2)--(3) hold for each failed pairing; and
- the three converted partitions from (4) are exactly the profile's three
  favorite-pair EFX partitions.

The first profile uses (h=8,\ell=7,E=\{5,6\}); the second uses
(h=7,\ell=8,E=\{1,6\}). Both have no full Hall cell, no EFX partition in
the six-orbit family, exactly 15 unlabeled EFX partitions, and 360 labeled
complete EFX allocations.

This explains the previously opaque three-repair floor: the repairs are not
three unrelated states. They are the conversions of the three missing
perfect matchings in an almost-full Hall cell.

## Remaining selection target

The cap-free global statement still needed must be conditioned on the
absence of every favorite-pair EFX allocation:

> **Conditional zero-neighbor selection target.** In the
> distinct-representative universal-threshold branch, assume no
> favorite-pair balanced partition supports EFX. If no favorite-triple
> Hall cell is full, then some failed pairing satisfies (1)--(3).

The conclusion would contradict the conditioning through (4), while a full
cell already supplies favorite-triple EFX. Thus a proof would close the
exact favorite-pair/full-cell dichotomy for the four-agent, nine-good hard
branch. The conditioning is essential: two earlier positive boundary
profiles have no full cell and no zero-neighbor conversion of this form,
but retain 27 favorite-pair EFX partitions. The lemma does not by itself
prove the conditional selection step or general additive EFX.

## Artifact

The deterministic audit
[efx49_zero_neighbor_favorite_triple_conversion_audit.json](efx49_zero_neighbor_favorite_triple_conversion_audit.json)
recomputes the (12+3) Hall split, the common zero-neighbor edge, every
inequality in the lemma, the converted EFX graphs, all 15 balanced
partitions, and the literal (4^9) allocation count for both profiles. It also
pins a cap-100 CP-SAT boundary that hard-blocks the other 777 eight-orbit
states and optimizes only the three converted states. That run retained all
three, but its bound still permits zero and therefore proves no floor.

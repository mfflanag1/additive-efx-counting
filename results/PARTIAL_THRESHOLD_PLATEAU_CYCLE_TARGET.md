# Threshold-plateau cycle target

## Current headline

For an eligible one-floater EFX state \((X,f)\), write

\[
\Theta(X,f)=\sum_i\frac{\tau_i(X_i)}{v_i(M)},
\qquad
\tau_i(B)=v_i(B)-\min_{g\in B}v_i(g).
\]

Across all 237 distinct stored positive four-agent profiles with 7--10 goods,
at least one global \(\Theta\)-maximizer admits direct insertion of its
floater followed by an EFX Hall matching.  This is exact corpus evidence, not
a theorem.

No fixed elementary tie-break identifies the completing maximizer.  In
particular, minimizing normalized owner utility inside the maximum plateau is
false on 46 profiles.  Those failures expose the plateau geometry rather
than refuting the existential selector.

## Exact plateau-transition census

For every blocked minimum-utility tie-break winner in those 46 profiles,
`partial_hall_threshold_plateau_completion_analysis.json` finds the nearest
Hall-completing state on the same global threshold plateau.  The exact census
covers 4,847 blocked selected states:

- 4,823 are one-good swaps between the floater position and one owner;
- 23 are same-floater, two-owner swaps;
- one is a three-edge rotation through the floater and two owners; and
- every transition has owner distance at most three.

Every one of the 4,847 transitions preserves each affected owner's threshold
term individually.  Of these, 4,843 are literal **minimum-slot cycles**: each
affected owner releases one owner-minimum good and receives a good that is
owner-minimum in the new bundle.  The four exceptions occur in one tied
integer profile and swap an outgoing top good for an equal-valued incoming
top good; they are still ownerwise threshold-neutral.  Thus under generic
item values the observed transition family is exactly minimum-slot cycles.

## Analytic lemma that would close four agents

Select a global \(\Theta\)-maximizer and, within its plateau, maximize a finite
Hall-defect order: first the largest matching cardinality over all four
floater hosts, then the corresponding edge data under a fixed lexicographic
order.

The required lemma is:

> **Plateau-cycle conversion lemma.** If the selected state has no direct
> Hall completion, the owner-minimum Hall-pair extraction theorem produces
> either (i) an eligible state with strictly larger \(\Theta\), or (ii) an
> eligible ownerwise-threshold-neutral slot cycle through at most two owners
> and the floater position whose endpoint strictly improves the Hall-defect
> order.

Alternative (i) contradicts global threshold maximality.  Alternative (ii)
contradicts the secondary finite maximum.  Therefore the selected plateau
state must have a direct Hall completion.  Combining this with the known
four-agent one-unallocated-good theorem proves complete additive EFX for four
agents.

The key unresolved implication is local: turn the two-agent/one-neighbor Hall
trap into the threshold-neutral cycle while preserving all cross-agent EFX
and floater-nonenvy inequalities.  The exact distance-three example shows
that a floater swap alone is insufficient; two owners plus the floater are
the smallest plausible universal family.

## General-EFX extension boundary

For arbitrary \(n\), a corresponding result would need:

1. a Hall-deficient-set extraction theorem replacing the four-agent pair
   trap;
2. a threshold-neutral slot cycle through that deficient set and one charity
   position; and
3. an invariant ensuring the other charity goods remain collectively
   unenvied while one good is absorbed.

If the cycle reduces the charity set by one while preserving those
conditions, it can be iterated from the known partial EFX theorem to a
complete allocation.  None of these arbitrary-\(n\) statements is currently
proved.

## Claim boundary

Neither four-agent EFX nor general additive EFX is resolved.  The durable new
content is the 237-profile existential plateau census, the exact refutation
of the minimum-utility tie-break, the 4,847-transition ownerwise-neutral
census, and the precise plateau-cycle lemma above.

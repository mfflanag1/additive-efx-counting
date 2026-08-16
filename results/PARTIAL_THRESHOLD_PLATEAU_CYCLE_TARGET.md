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

The subsequent exact-rational audit strengthens this substantially.  Across
the same 46 profiles there are 15,557 global threshold-maximal states, of
which 7,655 have no direct Hall completion.  Every one of those 7,655 blocked
maxima has a strictly direct-completion-margin-increasing path, through
eligible owner-minimum floater swaps on the same plateau, to a completion;
the maximum path length is two.  Thus the phenomenon is not an artifact of
the minimum-utility tie-break or of floating-point comparisons.  See
`PARTIAL_THRESHOLD_MAXIMUM_SWAP_REDUCTION_LEMMA.md` and
`partial_hall_threshold_plateau_exact_path_audit.json`.

## Analytic lemma that would close four agents

Select a global \(\Theta\)-maximizer and, within its plateau, maximize the
exact direct-completion margin \(H\) defined in
`PARTIAL_THRESHOLD_MAXIMUM_SWAP_REDUCTION_LEMMA.md`.

The required lemma is:

> **Exact Hall-gradient lemma.** If the selected state has no direct Hall
> completion, some eligible owner-minimum floater swap stays on the global
> threshold plateau and strictly increases \(H\).

The proved threshold-maximum swap lemma makes plateau preservation automatic;
the strict increase contradicts secondary maximality.  Therefore the
selected plateau state must have a direct Hall completion.  Combining this
with the known four-agent one-unallocated-good theorem proves complete
additive EFX for four agents.

The key unresolved implication is local: prove the exact Hall-gradient lemma
while preserving all cross-agent EFX and floater-nonenvy inequalities.  One
of the 7,655 exact corpus paths needs two successive floater swaps, so a proof
may need to show that every blocked state has an increasing first step rather
than a one-step completion.  The swapped owner is not always in a designated
minimum Hall-deficient set, ruling out that simplest role-fixed proof.

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
of the minimum-utility tie-break, the proved cap-free threshold-maximum swap
lemma, and the exact-rational 15,557-state/7,655-blocked-state Hall-gradient
census.

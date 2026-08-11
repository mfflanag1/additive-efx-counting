# Paid-anchor least-good consumption lemma

**Date:** 2026-08-11

**Status:** cap-free conversion of every anchor-driven residual wall into
strict current-source improvement plus nonempty paid-anchor consumption, or
unsafe augmentation; restoration of already consumed anchor support remains
open

## Anchor-driven wall

Use the paid-anchor state

\[
 W=Y_d\mathbin{\dot\cup}R                         \tag{1}
\]

with represented source `i` holding common-safe desired core `A_i`. Suppose

\[
 v_i(A_i)<\tau_i(W)                                \tag{2}
\]

and the outside-anchor residual does not improve `i`:

\[
 v_i(R)\le v_i(A_i).                               \tag{3}

Let `g` be a least-`i` good of `W`, and put

\[
 B=W-g.                                            \tag{4}

Equation (2) is exactly

\[
 v_i(B)>v_i(A_i)>v_i(X_i),                         \tag{5}

\]

so `B` is a strict current-source improvement.

## Nonempty anchor consumption

The packet `B` must meet the paid anchor:

\[
 C=B\cap Y_d\ne\varnothing.                        \tag{6}

Indeed, if `C` were empty, then `Y_d subseteq {g}`. The paid target is
nonempty, so `Y_d={g}`, and (1), (4) give `B=R`. This contradicts (3) and
(5).

Thus every least-good response witnessing an anchor-driven wall consumes a
nonempty physical packet of the paid pre-compression target.

## Exact continuation

1. If `B` is common-safe, perform the complete recapture
   \[
   Z'_i=B,
   \qquad Z'_d=A_i+g.                              \tag{7}
   \]
   Source `i` strictly improves relative to the current compression, and
   every other represented source is unchanged. Record
   \[
   T'=T\cup C\subseteq Y_d                         \tag{8}
   \]
   as consumed paid-anchor support. On the first such event for the current
   anchor, `T` grows strictly. If (7) pays `d`, it remains in the paid
   current-wall family; if not, the nonroot unconditional-recapture theorem
   enters the priority-valid sacrificed-owner machinery with the same
   nonempty physical packet `C` recorded.
2. If `B` is unsafe, it is already a desired current-improving target.
   Globally minimal desired-subset extraction supplies an unsafe response
   augmentation. The proof does not perform an unrecorded recapture.

At fixed physical anchor `Y_d`, only finitely many strict updates (8) are
possible. A later state that restores a good of `T` to the residual reverses
an explicit earlier transfer and must be treated as a connected return
component, not as a fresh reset.

## Consequence

Combining this lemma with the paid-anchor current-wall theorem removes every
fixed-hole residual wall:

1. a common-safe outside-anchor residual strictly raises the represented-
   source utility vector;
2. an unsafe residual augments; or
3. an anchor-driven wall strictly consumes paid-anchor support.

There is no fourth scalar recapture case. The only live recurrence is now a
hole/source change or explicit restoration of already consumed anchor
support, both of which expose the connected return geometry required by the
outer rank-reset theorem.

## Verification and boundary

[`paid_anchor_least_good_consumption_audit.json`](paid_anchor_least_good_consumption_audit.json)
checks current-source improvement, the contradiction proving (6), recapture
support conservation, and strict support-set growth.

This lemma does not prove that restoration of `T` is release-compatible,
terminate the sacrificed-owner machinery after an unpaid recapture, close
all unsafe augmentations, close GG, or prove four-agent/general additive EFX.

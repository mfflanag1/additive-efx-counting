# Permanent-anchor retire-on-backup exchange theorem

**Date:** 2026-08-13

**Status:** conditional diagnostic only; post-handoff safety of `E` is not
supplied by the actual sacrifice-handoff premises, so this theorem is not the
recurrence resolution

## The exact state

Let `Y` be a post-recruitment allocation with first-priority root `r`.  The
root owns

\[
 Y_r=K\mathbin{\dot\cup}E,                       \tag{1}
\]

where `K` is the old permanent anchor, originally supplied by owner `q`, and
`E` is the recruited backup response.  Require the premises already carried
by the post-recruitment record:

1. `E` is current-safe relative to `Y`;
2. `E` is strictly desired by the root over the pre-recruitment root bundle;
3. the root value of `E` pays every unchanged target threshold;
4. `K` and `E` are physically disjoint; and
5. the full signed provenance of `K` identifies `q` as its original supplier.

Write `Q=Y_q`.  No assumption about the values of a mixed response to
`K+E` is used below.

## Retire-on-backup operation

Return the old anchor to its supplier and retain the backup at the root:

\[
 Z_r=E,
 \qquad Z_q=Q\mathbin{\dot\cup}K,
 \qquad Z_i=Y_i\quad(i\notin\{r,q\}).             \tag{2}
\]

Retire the label `K` from the set of admissible permanent anchors.  The
retirement is part of the full signed state record; a later use of the same
physical packet as a permanent anchor is not an unrecorded reset.

This is a root-preserving anchor exchange in the precise current-phase
sense.  The old base anchor is released with exact provenance, while `E`
becomes the current root anchor.  The theorem does not relabel `E` as an old
base anchor: its certified safety floor is the current post-recruitment
floor.

## Proof of validity

Feasibility is immediate from disjointness.  The root remains strictly above
the base because `E` was recruited as a strict root response.  It pays every
unchanged target by premise 3.  Owner `q` strictly improves in her own row by
positivity:

\[
 v_q(Q+K)>v_q(Q).                                 \tag{3}
\]

Every other owner keeps the same assigned bundle.  The old root target
`K+E` shrinks to `E`.  Current safety of `E`, together with the fact that no
nonroot assigned value decreases, proves that no observer has an EFX wall
against the new root target.  The only enlarged target is `Q+K`.

For any unchanged target `T`, the root pays `T` by premise 3; owner `q` has
strictly more value than before; and every other observer has the same
assigned value and the same threshold.  Therefore a wall against an
unchanged target after (2) was already a wall before (2).  In particular,

> every genuinely new EFX failure created by the exchange is against the
> single enlarged return target `Q+K`.

Pre-existing sacrificed-owner or residual walls are not falsely declared
absent; they retain their old labels.  A wall against `Q+K` has an exact
globally minimum current-safe response inside that one physical target and
enters the existing one-target response/recapture interface.

The full signed decoration changes transparently.  The transfer of `K` from
its original supplier to the root is cancelled; no item is duplicated and no
historical packet is inferred from a scalar balance.  Since the retirement
label is monotone and `K` is nonempty, the old complete permanent-anchor
state cannot recur exactly after (2).

## Resolution of the requested recurrence

Suppose now that an exact recurrent response `D` intersects both `K` and
`E`.  Apply (2) before executing another fixed-anchor response.  The root is
preserved on a certified current-safe, strictly desired core, the old anchor
is physically returned to its supplier, and its signed provenance is
cancelled.  This is outcome 4 of the frozen recurrence contract.  The values,
source, and critical goods of `D` are irrelevant to validity of the
exchange.

The same operation eliminates the associated source-inactive loss band.  If
a sacrificed owner has a desired core inside `K`, returning all of `K` to
`q` removes `K` from the root target and hence removes that anchor-side wall.
Any unrelated old wall remains labeled, and any new wall is confined to
`Q+K`.  Thus the loss band cannot recur with the same permanent anchor.

This also explains why the earlier fixed-anchor analysis stalled: retaining
`K` after a disjoint paid backup `E` has been recruited is an unnecessary
restriction.  Controlled release/reselection is not merely sufficient; it
is the smallest operation needed to leave the fixed-anchor state class.

## Relationship to the proper-response reduction

Independently, global minimum-cardinality extraction from an unsafe target
implies every selected mixed response is a proper subset of `K+E`.  That
removes the apparent whole-target recurrence and remains useful if anchor
release is forbidden.  It is not needed for the retire-on-backup proof.

## Claim boundary

Under the additional post-handoff-safety premise, this theorem resolves the
permanent-anchor recurrence via outcome 4.  That premise is stronger than
the actual sacrifice-handoff interface: the displaced owner's utility may
fall, so a core safe when recruited need not remain safe after the handoff.
Accordingly this file is a diagnostic conditional theorem, not the campaign
resolution.  It does not prove `E` is post-handoff safe or an old
base-common-safe anchor, erase pre-existing residual walls, terminate every
subsequent response to `Q+K`, close GG, or prove four-agent/general additive
EFX.

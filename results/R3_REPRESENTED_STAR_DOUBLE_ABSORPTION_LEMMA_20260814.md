# R3 represented-star double-absorption lemma

**Date:** 2026-08-14

**Status:** cap-free elimination of a persistent sole-source represented
star; a different represented response source remains to be converted

## Residual star

After full-owner recruitment is applied, the only external Hall defect not
yet in the full-owner charity-exchange terminal has form `R3`.  Its selected
matching is

\[
 r\to q,\qquad q\to s,\qquad s\to r,             \tag{1}
\]

and one represented owner `x` has universally safe current-desired response
cores in both of the other represented targets.  Write these targets as
`u,v`.  In the matching rotation,

\[
 B_t=R_t\mathbin{\dot\cup}C_t\qquad(t=u,v),      \tag{2}
\]

where `C_t` is the incoming matching packet.  Exactly one of `C_u,C_v` was
originally supplied by `x`; the other was supplied by the remaining
represented owner.

Choose a singleton placement away from `x`, so both star cores are desired
simultaneously.  Enlarge each core inside its own physical target by adding
the rest of that target's incoming packet.  Positivity preserves desire.

## Double absorption and edge identity

Move both enlarged cores to `x`, retain every unselected residual at its
target, and give the charity singleton to either depleted target.  Completing
the incoming packets is the important operation: the two old cycle edges
entering `u,v` disappear.  Relative to the saturated support allocation, the
only owner-transfer pairs left are

\[
                         u\to x,\qquad v\to x.   \tag{3}
\]

The pair in (3) absorbs both redirected incoming packets and every selected
retained-residual part because each such part has supplier `u` or `v`.
Adding `charity -> u` or `charity -> v` gives exactly three transfer edges.
No packet-size bound is used.

The identity remains true if either original star core used no retained
support, a proper retained subpacket, or the whole retained residual.  It
also remains true when its incoming part was empty or proper: completing
that part deletes the old cycle destination before the new destination is
counted.

## Monotone continuation

The enlarged recipient bundle at `x` need not be observer-safe, and a
depleted target need not be EFX-paid.  Recompute a globally minimal response.

If the response is again sourced by `x` into `u` or `v`, move that nonempty
core to `x`.  It uses one of the already present pairs in (3), strictly
shrinks the residual union `B_u union B_v`, and strictly enlarges `x`'s
bundle.  Because the ground set is finite, this branch terminates after at
most `|B_u|+|B_v|` transfers without adding an edge.

At termination exactly one of the following holds:

1. the complete allocation is EFX through at most three edges;
2. the next response is sourced by an owner other than `x`; or
3. `x` responds into the remaining owner target `d`.

Outcome 3 recruits the full owner component.  A new response source/core in
outcome 2 is a saturated response augmentation unless it is already present
in the exact signed record.  If it is old, it is the precise remaining
multi-source represented-component gate; the sole-source `2x1` star cannot
recur.

## What this removes

The generic `2x1` frontier allowed a fifth-edge obstruction when a response
mixed retained support with a proper incoming packet.  In the represented
`R3` star, handling both targets simultaneously eliminates that obstruction:
both incoming packets are completed and two old cycle edges cancel.  Thus
none of the three owner-label stars in
`EXTERNAL_HALL_FULL_OWNER_RECRUITMENT_LEMMA_20260814.md` remains a terminal
sole-source edge-overflow pattern.

## Claim boundary

Proved: exact conservation, the two-owner-edge identity, and finite
termination of every repeated common-source response into the two star
targets.

Not proved: that a different old represented response source immediately
forms release-compatible PI, that every resulting full-owner response meets
the full base-margin separator, the complete fixed-U theorem, or general
additive EFX.

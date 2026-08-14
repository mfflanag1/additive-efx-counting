# Endpoint-6 one-packet repair no-go

**Date:** 2026-08-14

**Status:** exact PI-free bounded countermodel; direct fourth-edge donation is
not the missing universal operation

## Tested strengthening

Start from the root-retained endpoint-6 allocation

\[
(A+H,\ (Q-J)+P+M,\ J+(W-M),\ E).               \tag{1}
\]

The first three supplier edges are `q->d`, `d->q`, and `charity->q`.  For
each nonroot target other than `q`, enumerate every nonempty packet contained
in that target and move the packet to `q`, leaving every other good fixed.
Each such move uses at most one additional supplier edge; a packet from the
`d` target reuses or removes an existing edge.  There are exactly seventeen
distinct repairs:

- seven packets from `A+H`;
- seven packets from `J+(W-M)`; and
- three packets from `E`.

The proposed strengthening was that, whenever endpoint `Z6` is EFX and pays
`q,s` but (1) leaves `q` below base, some one-packet repair is complete EFX.

## Countermodel

The exact CEGAR starts with 46,683 valid generalized-PI exclusions.  It finds
and excludes 71 additional hidden generalized-PI families and terminates at
a positive-rational profile satisfying:

1. the complete allocated-`E` form-2 master;
2. no generalized PI under the exact complete oracle;
3. endpoint `Z6` is complete EFX and pays `q,s`;
4. the root-retained `q` bundle is below base; and
5. all seventeen one-target-to-`q` packet repairs are non-EFX.

The producer is `allocated_e_form2_endpoint6_one_packet_repair_cegar.json`.
`audit_allocated_e_endpoint6_one_packet_repair_countermodel.py` independently
reconstructs the exact rational master, reruns the complete generalized-PI
oracle, and checks every repair with direct Fraction EFX inequalities.  Its
record is `allocated_e_form2_endpoint6_one_packet_repair_cegar_audit.json`.

## Interpretation

The spare fourth edge is real but cannot be used as an isolated donation to
`q`.  The final universal operation must change at least two target roles,
use a GG response/anchor transition, or exploit the signed `q<->d` cycle.
Moving a larger packet from the same single target does not evade this
countermodel because every nonempty subset was tested.

## Claim boundary

Refuted: the bounded one-target-to-`q` direct-EFX repair selector.

Not refuted: response-mediated progress, a coordinated multi-target exchange
whose final support relation still compresses to four edges, the full GG
supplier theorem, the universal fixed-`U` theorem, or general EFX.

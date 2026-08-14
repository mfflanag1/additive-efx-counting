# Two-survivor named-topology selector refutation

**Date:** 2026-08-13

**Status:** exact bounded refutation of the response-derived topology menu;
the unrestricted four-edge theorem survives

## Selector tested

After the corrected exact response classification leaves only the two-cycle
form `R2` and the three-cycle form `R3`, the cap-free construction lemmas
produce three types of complete four-edge candidate:

1. reverse a Hamiltonian response path and give charity to its endpoint;
2. omit one response, insert a `d` response, and give charity to the omitted
   source; or
3. rotate the whole paid response cycle and give charity to `d`.

For each form, take the union of every topology of those three types and
allow **arbitrary packets** along every permitted edge.  Edges may even be
empty, so the tested family is larger than the literal response-core
construction.

## Exact result

The direct QF-LRA decisions are SAT for both exact response forms:

| Form | topologies | distinct complete allocations blocked | result |
|---|---:|---:|---|
| `R2` | 5 | 1,826 | SAT counterprofile |
| `R3` | 9 | 1,211 | SAT counterprofile |

In each rational counterprofile:

- the full encoded twelve-atom necessary-premise master replays SAT at the
  exact values;
- the complete nonself response relation is exactly the declared five-edge
  `R2` or `R3` relation;
- no allocation supported by any named response-derived topology is EFX;
  but
- unrestricted complete EFX allocations using at most four support edges do
  exist (105 for the `R2` profile and 47 for the `R3` profile).

Both profiles even have a three-edge complete EFX allocation.  Hence failure
is not evidence against the theorem's four-edge conclusion.  It is evidence
that response arrows alone do not determine the correct transfer topology.

## Structural consequence

The response-path route is retired as a universal selector.  This is not
merely an endpoint-margin gap: even allowing every packet choice within its
topologies cannot close the two exact forms.

A separate topology census of all 25 profiles in the frozen corrected
exact-response CEGAR snapshot finds:

- 215 distinct feasible topologies;
- no cover by the 24 charity-rooted Hamiltonian paths; and
- a minimum four-topology **functional** cover of the observed profiles.

Thus the next live route is a flexible functional transfer selector driven
by signed packet margins, not by reversal of the response graph.

## Verification and boundary

[`audit_two_survivor_named_topology_refutation.py`](../tracks/parkability/audit_two_survivor_named_topology_refutation.py)
independently re-enumerates the named families, rechecks EFX in exact
rational arithmetic, fixes every value in the exact-response master, checks
the complete response relation, and exhaustively finds unrestricted
four-edge witnesses.  Its manifest is
[`two_survivor_named_topology_refutation_audit.json`](two_survivor_named_topology_refutation_audit.json).

The exact topology census is
[`fixed_u_exact_owner_cycle_relation_topology_cover_round24.json`](fixed_u_exact_owner_cycle_relation_topology_cover_round24.json).

These are bounded twelve-atom results.  They refute a sufficient selector,
not the cap-free four-edge theorem and not the existence of complete EFX at
the saturated terminal.

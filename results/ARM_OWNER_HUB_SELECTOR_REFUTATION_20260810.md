# Arm-owner hub selector refutation

**Date:** 2026-08-10

**Status:** exact bounded refutation of the canonical one-star selector;
component-growing selector remains open

## Refuted selector

In the full-`X_q` three-packet flower, the first hub-split escape found by
exact optimization uses the external large arm owner `c`: `c` receives `f`
and sends one top good and one bottom good to two distinct recipients.  This
suggested the cap-free shortcut that some improving two-leaf split from `c`
must be EFX or immediately yield a release-compatible PI cycle.

The direct EFX part is false even after all earlier local gates are imposed.
The strengthened full-capture solver blocks:

1. every EFX insertion of `f`, owner-improving one-item charity swap, and
   priority-directed one-good transfer;
2. every priority-directed two-good exchange;
3. every simple three-good owner path;
4. every improving one-recipient packet-for-charity replacement; and
5. every improving complete two-leaf hub split whose hub is `c`.

The cell remains SAT under Z3 5.0.0 and 4.15.3.  The exact profile is
[`three_nonsingleton_flower_full_capture_arm_hub_gate.json`](three_nonsingleton_flower_full_capture_arm_hub_gate.json).

## Exact hub census

The strengthened profile has six improving two-leaf splits from `c`.  All
six fail EFX: two expose an external wall at a target with no internal wall,
and four have a target with no internal wall and no external wall.  None is
a leaf-mutual trap or a PI cycle through `c`.

Across all possible hubs, the exact census is:

| classification | count |
|---|---:|
| eligible improving splits | 5,436 |
| PI wall cycle through the hub | 351 |
| external/open target | 3,416 |
| internally terminal target | 1,605 |
| leaf-mutual trap | 64 |
| complete EFX | 0 |

The frozen replay is
[`three_nonsingleton_flower_arm_hub_gate_split_census.json`](three_nonsingleton_flower_arm_hub_gate_split_census.json).
The 351 PI classifications also make the claim boundary important: this
bounded profile is not globally PI-free and therefore does not refute a
broader selector whose outcome is “EFX or PI.”

## Smallest escapes

The nearest partial EFX-with-charity improvement moves two goods in two
components: one `c`-good moves to `r`, and one `q`-good joins `f` in charity.
The nearest complete improvement moves five goods in one component spanning
`q,c,s,charity`: `q` sends one good each to `s,c`, `c` sends a top good to
`q`, `s` sends `z` to `c`, and charity sends `f` to `s`.  See
[`three_nonsingleton_flower_full_capture_arm_hub_gate_improvement.json`](three_nonsingleton_flower_full_capture_arm_hub_gate_improvement.json).

Thus the arm-owner star is a valid *starting component*, not a universal
endpoint.  Its wall-free/open targets must be spliced to another flower
component, and the final endpoint may contain a cycle plus a charity edge
rather than retain star topology.

## Corrected analytic target

Prove an arm-rooted **component-growing selector**.  Begin with the finite
family of packet partitions induced by `T_c,B_c`.  For each failed split:

- a hub-containing wall cycle is immediately PI;
- an external wall grows through the fourth owner;
- an internally wall-free target is frozen as a safe endpoint; and
- the leaf-mutual family triggers an alternate hub or repartition.

Show that with four owners this growth either closes a release-compatible PI
edge set or joins safe endpoints into a lex-improving EFX allocation.  The
five-good `q,c,s,charity` escape above is the smallest new topology that the
statement must permit.

## Claim boundary

This is a bounded countermodel to one proof mechanism, not to EFX.  It does
not show that all hub choices avoid PI closure, and the modeled base state is
not asserted globally maximal.  General additive EFX and the
three-nonsingleton flower remain open.

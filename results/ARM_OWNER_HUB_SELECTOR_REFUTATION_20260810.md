# Arm-owner direct-EFX selector refutation

**Date:** 2026-08-10

**Status:** exact bounded refutation of the direct-EFX endpoint; the corrected
response-Hall selector survives

## Refuted selector

In the full-`X_q` three-packet flower, the first hub-split escape found by
exact optimization uses the external large arm owner `c`: `c` receives `f`
and sends one top good and one bottom good to two distinct recipients.  This
suggested the cap-free shortcut that some improving two-leaf split from `c`
must itself be EFX.

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

The strengthened profile has six improving two-leaf splits from `c`, and all
six fail EFX. Exact enumeration of common-safe desired subsets relative to
the base allocation gives a different and more useful response picture: two
splits already have a full internal response matching and hence a PI edge
set, two have an external champion source, and two are internally Hall
deficient.

Across all possible hubs, the exact census is:

| classification | count |
|---|---:|
| eligible improving splits | 5,436 |
| PI response matching | 3,542 |
| external/open champion source | 1,892 |
| response-Hall deficient | 2 |
| complete EFX | 0 |

The frozen replay is
[`three_nonsingleton_flower_arm_hub_gate_split_census.json`](three_nonsingleton_flower_arm_hub_gate_split_census.json).
The 3,542 PI classifications make the positive boundary important: this
bounded profile is not globally PI-free and therefore supports rather than
refutes the corrected selector whose outcome is “EFX or response-Hall PI.”
In particular, two of the six arm-owner splits already close by response
matching.

## Smallest escapes

The nearest partial EFX-with-charity improvement moves two goods in two
components: one `c`-good moves to `r`, and one `q`-good joins `f` in charity.
The nearest complete improvement moves five goods in one component spanning
`q,c,s,charity`: `q` sends one good each to `s,c`, `c` sends a top good to
`q`, `s` sends `z` to `c`, and charity sends `f` to `s`.  See
[`three_nonsingleton_flower_full_capture_arm_hub_gate_improvement.json`](three_nonsingleton_flower_full_capture_arm_hub_gate_improvement.json).

Thus the arm-owner star is a valid *starting component*, not necessarily an
EFX endpoint. Its actual generalized champion sources—not merely the strong-
envy observers—must be matched first. Only response-Hall-deficient or open
cases need to be spliced to another flower component.

## Corrected analytic target

Prove an arm-rooted **response-Hall selector**. Begin with the finite
family of packet partitions induced by `T_c,B_c`.  For each failed split:

- enumerate the most-envious source sets of the three proposed targets;
- a full internal matching is immediately PI;
- an external champion source grows through the fourth owner; and
- an internal Hall witness triggers an alternate hub or repartition.

Show that with four owners this growth either closes a release-compatible PI
edge set or joins safe endpoints into a lex-improving EFX allocation.  The
five-good `q,c,s,charity` escape above is the smallest new topology that the
statement must permit.

## Claim boundary

This is a bounded countermodel only to requiring the arm-owner star itself to
be EFX. It does not refute EFX-or-PI response matching; the frozen profile
contains thousands of such PI matchings and is not globally maximal. General
additive EFX and the three-nonsingleton flower remain open.

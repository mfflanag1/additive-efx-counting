# Arm-response selector gate refutation

**Date:** 2026-08-10

**Status:** exact bounded refutation of guaranteed arm-hub eligibility; the
all-hub response selector remains open

## Strengthened gate

The corrected arm-rooted selector asks for an improving two-leaf split from
the external arm owner `c` that is either EFX or whose exact most-envious
response sets admit an internal matching.  The strengthened full-capture
solver forbids both outcomes for every arm-owner split, on top of all earlier
exchange, path, and one-recipient packet gates.

The cell remains SAT.  It evades the selector at its premise: `c` has no
improving two-leaf split at all.  Thus flower championship does not by itself
force the arm owner to satisfy `v_c(f)>v_c(R)` for a packet with two nonempty
leaf cells.

The exact profile is
[`three_nonsingleton_flower_full_capture_arm_response_gate.json`](three_nonsingleton_flower_full_capture_arm_response_gate.json).
Z3 5.0.0 returns SAT. A bounded replay under Z3 4.15.3 was stopped after ten
minutes with `unknown`; dual-solver confirmation of the full symbolic gate is
therefore still pending. The frozen rational profile and its hub census are
independently replayable.

## Alternate-hub escape

The model does not evade hub splitting globally.  Exact enumeration finds
six eligible two-good splits from mutual-cycle owner `q`:

| response outcome | count |
|---|---:|
| complete EFX | 1 |
| external champion source | 4 |
| internal Hall deficiency | 1 |

The EFX split replaces two `q`-goods by `f`, sends one released good to `c`
and one to singleton owner `s`, and leaves `r` fixed.  The complete census is
[`three_nonsingleton_flower_arm_response_gate_split_census.json`](three_nonsingleton_flower_arm_response_gate_split_census.json).

## Corrected selector target

The next theorem cannot privilege the external arm owner.  It must prove an
**alternate-hub response dichotomy**:

1. some nonsingleton owner has an improving packet partition whose endpoint
   is EFX or whose internal response sets match; or
2. every nonsingleton owner's floater value is below every admissible
   two-cell packet, and those simultaneous owner-row inequalities force a
   common-safe cover, a generalized PI cycle, or a larger-packet endpoint.

The frozen model demonstrates the first branch with hub `q`.  The highest-
leverage analytic work is now to derive this cross-owner eligibility
dichotomy from the three flower decompositions instead of fixing `c`.

## Claim boundary

This refutes only guaranteed eligibility of the arm owner.  It does not
refute the all-hub EFX-or-response-Hall selector; the same model contains an
EFX alternate-hub split.  It is not an EFX counterexample and is not asserted
globally maximal.

# Two-cycle branching charity-completion lemma

**Date:** 2026-08-13

**Status:** cap-free support and payment closure of the two-cycle form unless
both d-response cores suffer full-margin overlap capture

**Boundary update:** this is a conditional construction, not an exhaustive
selector. Its topology is included in the exact refuted family documented in
`TWO_SURVIVOR_NAMED_TOPOLOGY_SELECTOR_REFUTATION_20260813.md`.

## Branching completion

In the two-cycle survivor, choose disjoint response cores

\[
 D_r\subseteq Y_q,\qquad D_q\subseteq Y_r         \tag{1}
\]

for `r -> q` and `q -> r`. The sacrificed owner has responses into both
targets. If there is a d-response core

\[
 C_d\subseteq Y_t\setminus D_{\operatorname{pred}(t)},
 \qquad t\in\{r,q\},                               \tag{2}
\]

rotate the two cycle cores, give `C_d` to `d`, and give singleton charity
`p` to `s`. Owner `s` keeps its whole paid current bundle.

The active support edges are

\[
 q\to r,qquad r\to q,qquad t\to d,qquad
 \text{charity}\to s.                             \tag{3}

Thus the allocation is complete and uses exactly four edges, even when
`t` sends two distinct packets. Every packet may have arbitrary size.

Owners `r,q,d` are strictly paid by their desired cores. Owner `s` retains
its paid bundle and receives a positive good, so it is strictly paid as
well. At a saturated state, any unsafe enlarged target must give a new
response/support/progress exit; otherwise (3) is EFX.

## Dual-overlap survivor

Apply the shared-target disjoint-or-capture lemma separately at `r` and `q`.
If neither target admits a disjoint d-core, the intersection with the cycle
core captures d's entire response margin at both targets. Therefore this
branching construction has one exact remaining separator:

> simultaneous full-margin capture of both d-responses by the two paid cycle
> cores.

A proof using this construction must turn dual capture into retained-support growth,
a response replacement, or a release-compatible component. A countermodel
must realize both capture inequalities at one complete saturated signed
record while defeating all other four-edge graphs.

## Verification and boundary

[`audit_two_cycle_branching_charity_completion.py`](../tracks/parkability/audit_two_cycle_branching_charity_completion.py)
independently constructs both target choices and proves conservation, the
four-edge count, empty charity, and all owner-payment implications.

This lemma does not reverse simultaneous overlap capture or independently
prove observer safety of every final target.

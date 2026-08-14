# Paid functional four-edge selector reduction

**Date:** 2026-08-13

**Status:** cap-free reduction to one repeated decorated-component extraction
gate; universal existence of the selector remains open

## Functional selector family

Let `Y` be the physical support allocation with singleton charity `{p}`.
For each supplier

\[
 x\in\{r,q,d,s,\mathrm{charity}\},
\]

choose at most one recipient `phi(x)` different from `x` and an arbitrary
packet `P_x subseteq Y_x`.  The charity packet is necessarily `P_c={p}`.
Move each nonempty `P_x` to `phi(x)` and retain every other good at its
current supplier.  Require at most four nonempty supplier-recipient pairs.

This is exactly the family of complete allocations whose support-transfer
graph is **functional on suppliers** and has at most four edges.  Packet
sizes are unrestricted, recipients may receive from several suppliers, and
the graph may contain cycles or disconnected components.

## Why this family remains live

The corrected exact-response census contains 25 rational profiles.  Every
one has a functional complete EFX allocation on at most four edges; every
one also has such an allocation that weakly pays every owner relative to the
base.  The minimum paid-functional edge histogram is `2:4, 3:13, 4:8`, so
eight profiles require four edges.  The exact replay is
[`paid_functional_four_edge_census_audit.json`](paid_functional_four_edge_census_audit.json).
In contrast:

- the union of all response-derived path, branching, and cycle topologies is
  exactly refuted in both surviving response forms; and
- a fixed four-topology functional menu is exactly refuted in `R3`.

Thus functionality survives the adversarial profiles, while every fixed
small topology menu tested so far fails.  This motivates a *dynamic*
functional selector rather than another response-graph normal form.

## Cap-free failure reduction

Suppose a member `Z` of the functional family weakly pays all four owners:

\[
 v_i(Z_i)\ge v_i(X_i)\qquad(i\in N).              \tag{1}
\]

If `Z` is not EFX, the paid-splice observer-failure lemma applies without
any packet cap.  A globally inclusion-minimal failed target subset `D`
satisfies

\[
 v_h(D)>v_h(Z_h)\ge v_h(X_h)                      \tag{2}
\]

for its responding source `h`, and is current-safe for every observer.  Its
base safety debts are bounded exactly by the signed gains retained in `Z`.
Consequently failure yields a complete decorated response record consisting
of the source, physical target, core `D`, released residual, and all signed
incoming/outgoing compensation packets.

At a saturated fixed-`U` state, that record must do one of the following:

1. augment the response record or represented support;
2. strictly improve the same-record source utility;
3. expose a PI/self-response component; or
4. repeat with the identical signed physical state.

The first three are explicit saturated exits.  Hence only exact repetition
survives.

## Exact remaining implication

The cap-free theorem is reduced to:

> From an exactly repeated paid functional candidate and its complete
> decorated response record, extract either another weakly paid functional
> candidate with strict finite-state progress, or a release-compatible
> complete EFX allocation on at most four supplier edges.

This is narrower than arbitrary observer safety and broader than reversing a
fixed response path.  The extraction must be allowed to change `phi`
dynamically.  The bounded counterprofiles prove that keeping `phi` inside
any of the presently named response-derived menus is insufficient.

## Computational gate and boundary

The exact direct decisions now separately negate all 76,692 nonempty-owner
functional allocations in each of the two corrected twelve-atom response
forms.  UNSAT would prove only the bounded functional theorem.  SAT would
refute the bounded functional selector, but not the unrestricted four-edge
theorem unless its profile also defeats nonfunctional allocations.

This reduction does not prove that a weakly paid functional candidate always
exists, close exact decorated repetition, prove the cap-free four-edge
theorem, or prove general additive EFX.

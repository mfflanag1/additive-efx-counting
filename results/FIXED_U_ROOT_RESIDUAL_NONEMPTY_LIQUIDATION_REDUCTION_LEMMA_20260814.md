# Fixed-U root-residual nonemptiness and liquidation reduction

**Date:** 2026-08-14

**Status:** cap-free universal reduction for the frozen target predicate;
the post-probe response recurrence remains open

## Frozen-record implication

Let `(Y,{p})` satisfy items 1--12 of
`FIXED_U_RANK_THREE_FOUR_EDGE_PREMISE_LEDGER_20260813.md`.  Item 4 contains
the mandatory nonself response `d -> r`, and item 5 records for that response
a nonempty desired core `E_{dr}` inside its physical target support.  Since
the target of `d -> r` is `Y_r`,

\[
                     \varnothing\ne E_{dr}\subseteq Y_r.
\]

Consequently every state in the frozen target has `Y_r` nonempty.  This
uses the literal target-support field of the decorated response record; it
does not identify the permanent anchor core with `E_{dr}`.

## Universal liquidation probe

Let `q` be the target of the permanent anchor response and let

\[
 A\subseteq Y_q,\qquad v_r(A)>v_r(X_r).
\]

For any nonroot owner `i`, form the complete allocation

\[
 Z_r=A,qquad
 Z_i=(Y_i\setminus A)\mathbin{\dot\cup}Y_r\mathbin{\dot\cup}\{p\},
\]

where `Y_i\setminus A` matters only when `i=q`; every other nonroot owner
keeps its current bundle, with `A` removed from `q` when `i!=q`.

Relative to the original current suppliers, the only possible nonself
pairs are

\[
 q\to r:A,\qquad r\to i:Y_r,\qquad charity\to i:p.
\]

Thus `Z` is complete and uses at most three packet-transfer edges, without
any restriction on packet sizes.  Moreover

\[
 v_r(Z_r)=v_r(A)>v_r(X_r),
\]

and owner `i` strictly improves relative to the anchor-moved state because
`Y_r` is nonempty and valuations are positive.

Equivalently, with `B_r=Y_r dotunion A` and
`delta_r=v_r(B_r)-v_r(X_r)`, strictness of `A` gives

\[
 v_r(Y_r)=v_r(B_r)-v_r(A)<\delta_r<\delta_r+v_r(p).
\]

Therefore the universal empty-compensator bilateral-failure separator is
inconsistent with the frozen target premises.

## Exact remaining gate

If `Z` is EFX, it is the requested complete strict-priority endpoint.  If
`Z` is not EFX, a globally minimum common-safe desired response exists at
the actual floors of `Z`.  Nothing above proves that this response is new,
hits the retired support, closes generalized PI, or satisfies the
represented-component extraction interface.

The universal fixed-`U` theorem has consequently been reduced past the
physical residual/payment question.  Its live implication is:

> Every non-EFX liquidation probe generated above has a response whose full
> decorated record forces a saturated exit (new record, strict progress,
> release-compatible generalized PI, or represented-component extraction).

The reset-admission theorem cited by the separate two-edge charity-relay
route exists at commit `34709c9ce22dbde23a5fa381a2ccea7898dfe1ca` but is
not in this branch's ancestry.  In any event, that theorem explicitly
requires a separate physical progress argument, so it cannot by itself
discharge the displayed live implication.

## Claim boundary

Proved: `Y_r` is nonempty in every frozen target state, and every such state
has the displayed cap-free, complete, at-most-three-edge strict-priority
probe.  Not proved: that the probe is EFX, closure of its failed response,
the saturated rank-three fixed-`U` theorem, four-agent additive EFX, or
general additive EFX.

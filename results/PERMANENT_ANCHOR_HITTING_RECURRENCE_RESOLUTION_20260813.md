# Permanent-anchor hitting recurrence: resolution

**Date:** 2026-08-13

**Verdict:** **proved under the exact post-recruitment GG contract.**  Every
globally minimum response to the enlarged root target yields either a valid
current-phase root-anchor reselection or strict permanent retired-support
progress.  The same dichotomy removes the associated source-inactive
loss-band recurrence.

## One-line mechanism

Let `B=K+E`, let `x=v_r(X_r)`, and let `p` be the pre-recruitment root floor.
The permanent anchor and recruited response give

\[
 v_r(K)>x,
 \qquad v_r(E)>p\ge x.                            \tag{1}
\]

Extract a globally minimum desired response `D subsetneq B` at the complete
handoff state.  Minimality makes `D` safe there.  Then:

- if `v_r(D)>x`, use the safe `D` as a new current-phase root anchor;
- if `v_r(D)<=x`, give `D` to its source and keep `B-D` at the root, because
  \[
  v_r(B-D)>x+p-x=p.                               \tag{2}
  \]
  Permanently retire `D` from the old labeled root support.

The first branch is outcome 4; the second is outcome 3.  No third scalar
case exists.

## Requirement audit

| Requested requirement | Resolution |
|---|---|
| Globally maximal post-recruitment GG state | inherited from the frozen contract; only the base root floor is used |
| Response intersects both `K` and `E` | covered; the proof is actually independent of how `D` splits across them |
| EFX lexicographic improvement | retained as a possible endpoint, but not needed for the dichotomy |
| Release-compatible PI cycle | not needed |
| Strict retained-support or finite signed-state progress | root-low branch strictly enlarges a globally monotone retired-support ledger |
| Root-preserving anchor exchange/reselection | root-high branch reselects the exact current-safe response `D` |
| Recapture/hole-pivot/two-hole termination | not invoked |
| Source-inactive loss band | the same root-value dichotomy applies to a globally minimum anchor-side response; otherwise another minimum response changes the state first |
| Exact arithmetic | symbolic rational-linear proof plus independent positive-integer replay |
| Premise audit | post-handoff safety of recruited `E` is explicitly **not** assumed |

## The key correction caught during review

An initially attractive proof returned the old anchor to its supplier and
kept `E` at the root.  That operation is valid if `E` remains safe after the
sacrifice handoff, but the actual interface does not guarantee this: the
displaced owner's assigned value can fall.  The conditional theorem and
audit are retained as diagnostics, with a non-resolution status.  The final
proof instead uses `D`, whose safety follows at the exact handoff state from
global minimum cardinality.

## Exact artifacts

- [`PERMANENT_ANCHOR_HITTING_RECURRENCE_CONTRACT_20260813.md`](PERMANENT_ANCHOR_HITTING_RECURRENCE_CONTRACT_20260813.md)
- [`PERMANENT_ANCHOR_MINIMAL_RESPONSE_PEEL_OR_RESELECT_THEOREM_20260813.md`](PERMANENT_ANCHOR_MINIMAL_RESPONSE_PEEL_OR_RESELECT_THEOREM_20260813.md)
- [`permanent_anchor_minimal_response_peel_or_reselect_audit.json`](permanent_anchor_minimal_response_peel_or_reselect_audit.json)
- [`permanent_anchor_minimal_response_peel_or_reselect_independent_audit.json`](permanent_anchor_minimal_response_peel_or_reselect_independent_audit.json)

The primary audit proves the scalar dichotomy in QF_LRA, checks the physical
partition, and checks strict ledger growth.  The independent implementation
does not import the primary audit; it enumerates 824 exact positive-integer
scalar cases and all 14 nonempty proper supports of a four-atom target.

## Referee claim boundary

This is a real cap-free closure of the named permanent-anchor recurrence, not
a proof of four-agent additive EFX.  It leaves other pre-existing residual
walls and other GG state classes to the larger composition.  The new global
obligation is mechanical but essential: every later composition theorem
must carry the retired-support ledger and must not silently rebuild an old
labeled root target from retired goods.


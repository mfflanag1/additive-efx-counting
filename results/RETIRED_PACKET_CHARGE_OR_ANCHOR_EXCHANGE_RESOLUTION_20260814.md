# Retired-packet charge-or-anchor-exchange theorem: resolution

**Date:** 2026-08-14

**Correction verdict:** **not yet proved under the frozen exact
`T_{L,times}^*` contract.**

The nonroot branch is closed and the root scalar contradiction is exact
conditional on its premise.  The final audit found that the proposed root
supplier-star move empties positive-floor later owners, contrary to the
frozen candidate-admissibility rule.  Until a controlled floor reset or
floor-paying supplier star is proved, the root-held branch remains open. See
`ROOT_GLOBAL_SUPPLIER_STAR_FLOOR_ADMISSIBILITY_GAP_20260814.md`.

Conditional on that missing admission operation, every named retired-packet collision yields an EFX lexicographic
improvement, a release-compatible PI cycle, a valid root/anchor transition,
strict packet/hitting/rank progress, or a contradiction to the typed floors
or global maximality.  This conditional conclusion is not presently a
theorem of the frozen contract.

## Input and exhaustive holder split

Use the complete signed state, typed floors, retirement supplier, current
holder, colliding recipient, response record, and physical anchor label from
the frozen charge-or-anchor contract.  The current holder of the allocated
retired packet is either the protected first-priority root or a nonroot
owner.  These cases are exhaustive.

The split is also exhaustive over the collision certificate.  A repeated
whole hit supplies the named current response directly.  A
normalization-bypass repeat supplies the ledger-free response extracted from
the actual normalized allocation while retaining the failed original
collision, packet provenance, typed floors, and holder.  Protected-floor
extraction therefore enters the same holder split below; the bypass is not a
third terminal and does not reset the physical label.

## Nonroot holder

Protected-floor extraction supplies an actual common-safe core `D`
containing the named packet `K` and its named protected source or colliding
recipient.  The desire-free envelope-descent theorem assigns `D` through
that typed handoff while preserving the earlier strict root.

Only the sacrificed old holder can create a new wall against `D`.  A
globally minimum response is a proper subset, so every repeated whole hit
forms a strict chain

\[
 D=D_0\supsetneq D_1\supsetneq\cdots\supseteq K.
\]

The chain terminates with a proper or empty `K`-intersection; a singleton
terminal is universally safe.  This is strict reduction of the packet or
its hitting coordinate.  The argument covers strict capture,
equality-critical assignment, and source-inactive/base-floor debt because
it uses current safety rather than current desire.  Every moved bundle has
its actual current supplier.

## Root holder

Write

\[
 Z_r=K\mathbin{\dot\cup}H,
 \qquad v_r(Z_r)=x+\delta,
 \qquad E=G\setminus Z_r.
\]

For every nonempty `T subseteq K`, the admitted global supplier-star
sacrifice gives the root `G-T` and gives `T` to the named nonroot sacrifice
target.  A strict or equality-paying test gives an EFX contradiction or a
proper/empty packet response.  Therefore an exact recurrence would have to
satisfy

\[
 v_r(k)>\delta+v_r(E)\qquad(k\in K).             \tag{1}
\]

Exact support accounting turns the right side into the value of the entire
base exterior:

\[
 \delta+v_r(E)=v_r(G\setminus X_r).              \tag{2}
\]

It also forces `K subseteq X_r`.  But the frozen anchored `GG` edge supplies
an old root-desired core

\[
 D_r=T_q+f\subseteq G\setminus X_r,
 \qquad v_r(D_r)>v_r(X_r).                       \tag{3}
\]

For any `k in K`, (1)--(3) imply the impossible chain

\[
 v_r(k)>v_r(G\setminus X_r)
 \ge v_r(D_r)>v_r(X_r)\ge v_r(k).               \tag{4}
\]

Thus the root-held terminal is empty.  If the proof root or physical anchor
label changes before (3) is retained, that executed change is already the
contracted root/anchor-exchange outcome and cannot be counted as the same
fixed-label recurrence.

## Requirement audit

| Required branch or outcome | Resolution |
|---|---|
| strict capture | nonroot envelope descent or admitted root supplier-star packet reduction |
| equality-critical payment | nonroot safety descent; root equality packet spread |
| base-floor/source-inactive debt | desire-free nonroot handoff; root proof uses no nonroot floor |
| release compatibility | actual protected handoff on the nonroot side; all-holder supplier star on the root side |
| EFX lexicographic improvement | retained as an immediate endpoint of every tested strict-root allocation |
| release-compatible PI | retained from the contracted path/Hall and supplier-cycle exits; not needed for the final scalar contradiction |
| root/anchor exchange | an executed new root/physical-anchor label is an allowed outcome; fixed-label root recurrence is contradicted by (4) |
| strict packet/hitting/rank progress | proper/empty packet responses in both holder branches |
| exact recurrence | impossible after the exhaustive holder split |

## Superseded conditional frontier

The second Aug-14 checkpoint continued the hypothetical exterior-dominant
root face through a charity reset, a two-source threshold debt, and a forced
nonroot `GGS` cycle.  Those conditional statements need not be false, but
they are no longer live under the complete anchored `GG` premises: equation
(4) eliminates their input.  In particular, no `GG -> GGS` conversion is
needed to prove the present collision theorem.

## Exact replay

From the repository root:

```bash
python -m tracks.parkability.audit_gg_old_root_core_exterior_dominance \
  --output results/gg_old_root_core_exterior_dominance_audit.json
python -m tracks.parkability.audit_gg_old_root_core_exterior_dominance_independent \
  --output results/gg_old_root_core_exterior_dominance_independent_audit.json
python -m tracks.parkability.audit_retired_packet_charge_anchor_resolution_20260814 \
  --output results/retired_packet_charge_anchor_resolution_20260814_audit.json
pytest -q \
  tracks/parkability/test_nonroot_safe_whole_hit_envelope_descent.py \
  tracks/parkability/test_root_global_exterior_subpacket_sacrifice.py \
  tracks/parkability/test_gg_old_root_core_exterior_dominance.py \
  tracks/parkability/test_gg_old_root_core_exterior_dominance_independent.py \
  tracks/parkability/test_retired_packet_charge_anchor_resolution_20260814.py
```

The independent root replay imports neither Z3 nor the primary root audit.
The finite audits check the scalar and support implications and the exact
artifact composition; the cap-free semantic GG argument remains a
conventional proof requiring external expert review.

## Claim boundary

This does not yet resolve the certified collision subtype
`T_{L,times}^*`.  It also does not close `T_{L,perp}^*`, `T_0^*`, the full `GG` class, the other
selected-cycle classes, four-agent EFX, or general additive EFX.  Promotion
to any larger theorem requires a fresh composition audit showing how those
other terminals are eliminated.

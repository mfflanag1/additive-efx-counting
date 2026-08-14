# Retired-packet charge-or-anchor-exchange theorem: resolution

**Date:** 2026-08-14

**Verdict:** **proved for the complete collision subtype
`T_{L,times}^*`, subject to independent semantic review of the new strict
first-priority floor-reset operation.**

The proof closes the exhaustive current-holder split. A nonroot holder is
eliminated by the desire-free safe-envelope descent. A root holder is
eliminated by the singleton supplier-star allocation together with an
explicit controlled reset of every later auxiliary floor. The reset repairs
the floor-admission gap in the earlier conditional global supplier-star
argument; it does not pretend that the old floors were preserved.

## Exact input

Use the complete signed `T_{L,times}^*` state: the allocation and charity,
globally maximal EFX base, first-priority root, physical anchor label, typed
floors, suppliers and releases, named nonempty retired packet `K`, retirement
supplier, current holder, colliding recipient, protected-floor capture
inequality, and repeated whole-hit or normalization-bypass response.

The current holder is either the protected root or a nonroot owner. These
cases are exhaustive. The four typed failure branches—strict capture,
equality-critical payment, base-floor/source-inactive debt, and release
failure—enter the same holder split after their exact response or protected
safe core has been extracted.

## Nonroot current holder

The protected-floor extraction supplies an actual common-safe core `D`
containing the named packet and its named source or colliding recipient. The
desire-free nonroot safe-envelope theorem assigns `D` through its current
supplier while retaining the earlier strict root.

Only the sacrificed old holder can create a new wall against `D`. A globally
minimum response is proper, so every repeated whole hit forms a strict chain

\[
 D=D_0\supsetneq D_1\supsetneq\cdots\supseteq K.
\]

The chain terminates with a proper or empty `K`-intersection; a singleton
terminal cannot be strongly envied. This is strict packet or hitting
progress. Supplier and normalization failures keep their exact labels and
enter the already recorded recapture, hole-pivot, or normalization-bypass
interfaces rather than silently restoring the old packet.

## Root current holder: controlled floor reset

Put `x=v_r(X_r)` and `O=G-X_r`. The fixed physical anchor label retains the
old root core

\[
 A=T_q+f\subseteq O,
 \qquad v_r(A)>x,                                \tag{1}
\]

where `T_q` is nonempty. Choose any `k in K`. Then

\[
 v_r(G-k)>x.                                     \tag{2}
\]

Indeed, if `k in X_r`, then
`v_r(O)>=v_r(A)>x>=v_r(k)`. If `k in O`, the packet `O-k` is nonempty: it
contains `A` when `k notin A`, and contains the nonempty `A-k` when `k in A`.
Positivity proves (2).

Form the complete current-holder supplier star

\[
 Y_r=G-k,
 \qquad Y_u=\{k\},
 \qquad Y_j=\varnothing\quad(j\notin\{r,u\}),   \tag{3}
\]

where `u` is the named later sacrifice row. Every moved good has its actual
current holder as supplier and one displayed destination. Record every
other retirement collision and the new physical root support; infer no PI
edge and no historical reversal.

The old proof stopped here because (3) can put a later owner below a positive
declared floor. The strict first-priority floor-reset theorem supplies the
missing operation. At the actual allocation (3), set

\[
 F_i^Y=v_i(Y_i)qquad(i\in N),                   \tag{4}
\]

retain the immutable base/root certificate and every physical label, and
recompute all EFX comparisons. Every owner pays the new current floor, and
(2) preserves the only coordinate needed for a lexicographic contradiction:
the first-priority root is strictly above the base. Lowering later auxiliary
floors is explicit and is not counted as progress.

If (3) is EFX, (2) contradicts global maximality. Otherwise empty targets
cannot be strongly envied and the singleton `{k}` cannot be strongly envied.
Every wall is therefore against `G-k`. A globally minimum desired response
`D subseteq G-k` is safe at the actual reset allocation and satisfies

\[
 D\cap K\subseteq K-k\subsetneq K.              \tag{5}
\]

Equation (5), not the numerical floor reset, is the required strict packet
or hitting progress. A later restoration of the old whole packet requires a
new signed collision record and cannot be an exact recurrence of this state.

## Typed-branch and release audit

| Required branch | Resolution |
|---|---|
| strict capture | nonroot envelope descent or root singleton-star reduction; no recipient surplus is used as root payment |
| equality-critical payment | nonroot descent is desire-free; the root star is physically strict, so no root-equality face remains |
| base-floor/source-inactive debt | nonroot currentization/descent preserves its protected root; the root case explicitly resets every later auxiliary floor while retaining the strict first coordinate |
| release compatibility | nonroot edges use their current supplier; the root star names every current holder and destination and makes no PI claim |
| repeated whole hit | strict nested-envelope descent for a nonroot holder; equation (5) for a root holder |
| normalization bypass | the actual bypass response and packet enter the same exhaustive holder split; no historical return is assumed |
| EFX endpoint | strictly improves the first-priority root over the globally maximal base |
| PI/anchor alternatives | retained when independently produced, but neither is required for the final root singleton-star reduction |

## Verification

The root closure has two independent executable replays. The primary audit
uses QF_LRA for both root-support cases and exhausts the packet/target
geometry. The independent replay imports neither the primary audit nor Z3
and checks the same inequalities over bounded integers plus an independent
support enumeration. The floor-reset audit separately checks exact payment
of the recomputed floors and the minimal-response deletion implication.

From the repository root:

```bash
python -m tracks.parkability.audit_strict_first_priority_floor_reset_admission \
  --output results/strict_first_priority_floor_reset_admission_audit.json
python -m tracks.parkability.audit_root_singleton_supplier_star_floor_reset_closure \
  --output results/root_singleton_supplier_star_floor_reset_closure_audit.json
python -m tracks.parkability.audit_root_singleton_supplier_star_floor_reset_closure_independent \
  --output results/root_singleton_supplier_star_floor_reset_closure_independent_audit.json
python -m tracks.parkability.audit_retired_packet_charge_anchor_resolution_20260814 \
  --output results/retired_packet_charge_anchor_resolution_20260814_audit.json
pytest -q \
  tracks/parkability/test_nonroot_safe_whole_hit_envelope_descent.py \
  tracks/parkability/test_strict_first_priority_floor_reset_admission.py \
  tracks/parkability/test_root_singleton_supplier_star_floor_reset_closure.py \
  tracks/parkability/test_root_singleton_supplier_star_floor_reset_closure_independent.py \
  tracks/parkability/test_retired_packet_charge_anchor_resolution_20260814.py
```

## Claim boundary

This proves the retired-packet charge-or-anchor-exchange theorem for
`T_{L,times}^*` inside the frozen anchored `GG` interface. It does not close
`T_{L,perp}^*`, `T_0^*`, the full `GG` class, the other selected-cycle
classes, four-agent EFX, or general additive EFX. The floor-reset operation
is a new load-bearing conventional proof step. It has exact machine replays,
but still requires independent mathematical and external expert review.

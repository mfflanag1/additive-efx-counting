# Retired-packet charge-or-anchor-exchange checkpoint

**Date:** 2026-08-13

**Status:** theorem not yet proved or refuted; cap-free reduction to two
explicit coupled-payment separator families

## Headline boundary

For an exact collision state `T_{L,times}^*`, the recipient-row capture
identity does not by itself pay the current holder.  Direct compensation,
priority-valid sacrifice, protected matching/compression, root reselection,
proper-packet reduction, and normalization reversal now reduce the goal to:

1. a **holder-price separator**, appearing either as an atomwise-critical
   whole retired packet or as its bounded root-facing specialization; or
2. a **safe-center three-offer star**, after protected target-envelope
   payment sends every other normalization pattern to PI or the existing
   two-core/two-hole machinery.

This is not a proof of `T_{L,times}^*`, GG, four-agent EFX, or general EFX,
and it is not a complete-contract counterexample.

## Exact results established at this checkpoint

### Packet accounting and invalid route

For `A=B dot-union K`, strict/equality margin `mu` and deficit `d` satisfy

\[
v_s(K)=\mu+d.
\]

The holder price is independently

\[
p_h(K)=\max\{0,v_h(K)-\sigma_h\}.
\]

Exact positive rational cross-row models satisfy recipient capture while
every named return packet underpays the holder.  These refute only the
capture-implies-payment proof route; they do not refute the GG theorem.

### Strict whole-packet charge

If some `g in K` has `v_s(g)<mu`, deleting `g` leaves a strict safe candidate
with a proper collision packet.  Hence a recurrent whole-packet survivor is
atomwise critical and obeys

\[
v_s(g)\ge\mu\ (g\in K),
\qquad
(|K|-1)\mu\le d.
\]

In particular `mu>d` forces `K` to be a singleton.  Equality capture
(`mu=0`) remains separately typed.

### Root-facing price duality

For root base `x`, current root surplus `delta`, and response `D`, elementary
root reselection/release closes outside

\[
\delta\le v_r(D)\le x.
\]

Inside this band the exact compensation price is

\[
\pi_r(D)=v_r(D)-\delta,
\qquad
0\le\pi_r(D)\le x-\delta,
\]

which equals the general holder price with root slack `delta`.  Thus the
root-facing branch is a bounded holder-price separator, not a third
independent obstruction.

### Normalization bypass

Against each of the three current owner reservoirs disjoint from a globally
minimum ledger-free response `E`, minimal threshold extraction yields either
a common-safe packet paying that observer against `E`, or a reversed
common-safe desired packet.

If all three reservoirs reverse, include the fourth physical edge by which
the target owner supplies `E` to its source.  Every owner then supplies one
desired packet along a nonself edge.  The four-edge functional graph contains
a directed cycle, and pairwise disjointness makes it supplier-closed PI.
Therefore an exact normalization survivor must contain at least one safe
threshold-payment packet.  Raising the threshold to the complete active-
target envelope makes that packet universal for its observer row. Including
the protected floor gives a two-core/two-hole reduction except in one label
pattern: the payment owner is the response source, both other reversals have
that same source, and the source's whole current bundle is common-safe.  The
survivor is exactly a safe center plus three disjoint safe offers, all desired
by the center. The all-unsafe, source-inactive-leaf, and unsafe-center
recurrences are eliminated.

A final canonical test swaps one leaf's offer to the center and the safe
center bundle back to that leaf.  Success gives two protected cores and
enters two-hole machinery.  Therefore the exact star survivor has the
three-row rejection certificate

\[
v_h(U_s)<\max\{F_h,\tau_h(O_h)\}
\quad\text{for every leaf }h.
\]

## Typed branch status

| Branch | Exact status |
|---|---|
| Strict capture | Proper packet reduction or atomwise-critical holder-price separator; `(|K|-1)mu<=d` |
| Equality critical | No strict packet-size charge; separately valid sacrifice/root handoff still required |
| Base-floor debt | Protected matching/compression routes apply; a mixed observer-payment separator may remain |
| Release failure | Supplier closure is mandatory; supplied cycle is PI, outside supplier grows the component, overlapping-core holder wall remains |

## Smallest remaining theorem

The next load-bearing statement is a **safe-center star allocation-or-price
lemma**.  Starting with the three offers and their exact physical holders,
it must prove one of:

1. an EFX allocation of one offer to the center and protected bundles to the
   three leaves;
2. a supplier-closed desired cycle and hence PI;
3. a strict source/target-rank or proper-retired-packet reduction;
4. a root/anchor operation; or
5. an exact three-way holder-price separator for the offer suppliers.

The target envelope resolves same-target observer debt.  The remaining
difficulty is leaf allocation: all three safe offers have the same desired
source, so response rank is one, while transferring any arm may require a
different holder compensation.

## Reproduction

Run:

```bash
pytest -q \
  tracks/parkability/test_retired_packet_charge_anchor_gate.py \
  tracks/parkability/test_whole_retired_packet_atomwise_criticality.py \
  tracks/parkability/test_root_facing_anchor_surplus_band.py \
  tracks/parkability/test_root_facing_holder_price_duality.py \
  tracks/parkability/test_normalization_bypass_reservoir_reversal.py \
  tracks/parkability/test_normalization_bypass_three_reservoir_fan.py \
  tracks/parkability/test_target_envelope_universal_payment_or_pi.py \
  tracks/parkability/test_target_envelope_protected_pair_or_star.py \
  tracks/parkability/test_safe_center_three_offer_return_or_rejection.py \
  tracks/parkability/test_retired_packet_collision_atomic_normal_form.py \
  tracks/parkability/test_retired_packet_charge_anchor_checkpoint.py
```

The arithmetic audits use exact QF_LRA/QF_LIA.  The 324 fan assignments are
an exhaustive finite audit of source labels only, not a valuation-cell
search and not a premise of the analytic functional-graph proof.

# Retirement-supplier return admissibility correction

**Date:** 2026-08-14

**Status:** exact statement-integrity correction; strict release is repaired
by the clean controlled-release theorem and equality is separately eliminated
by the base-restoration packet-spread theorem

## Finding

In an exact `T_{L,times}^*` record, a ledger entry

\[
 (\alpha,K,u,F^{\rm ret})
\]

states that `K` was removed from a root target under label `alpha`, paid to
historical recipient `u`, and certified at the retirement-time floor.  The
record also identifies the current holder and every later signed movement.
It does **not** assert that returning `K`, or an arbitrary subpacket
`T subseteq K`, to `u` is currently an admissible operation.

The frozen global contract is explicit: an operation is not admissible merely
because it respects a ledger convention or conserves goods.  It must be an
actual `G0--G10` operation with all current floors, protected cores,
suppliers, releases, and response coordinates verified.

## Exact mismatch

The proved root safe-whole-hit operation has a current common-safe core
`D superseteq K` and assigns **that core** to its named current protected
source/colliding recipient `t`.  The existing root-sourced sacrifice handoff
likewise uses an actual current-safe response and its displaced source.

The supplier-return candidates instead:

1. select `K` or an arbitrary `T subseteq K`;
2. assign it to historical recipient `u`, who need not equal `t`; and
3. use the signed retirement record as the asserted admission rule.

No proved transition supplies those three premises.  Downward safety of
`T subseteq D` proves only observer safety of the target; it neither pays the
current intended recipient's typed floor nor authorizes assignment to `u`.
The exact root-margin identities and target-separation statements remain
correct if the missing operation is independently admitted.

## Consequence and repair

The original historical-reversal justification in the following files is
invalid:

- `RETIREMENT_SUPPLIER_ROOT_PACKET_RELEASE_OR_UNDERPAYMENT_THEOREM_20260814.md`;
- `RETIREMENT_SUPPLIER_SUBPACKET_RELEASE_OR_ATOMWISE_POOL_DOMINANCE_THEOREM_20260814.md`;
- the atomwise packet-price headline in the second Aug-14 checkpoint.

The strict branch is nevertheless admitted by
`ROOT_STRICT_CLEAN_SUBPACKET_RELEASE_ADMISSION_THEOREM_20260814.md`.  It gives
the returned packet alone to the sacrificed named owner, sends her displaced
bundle to charity, and proves that every failed EFX test has proper packet
intersection.  This establishes the weak packet-price and atomwise cuts
without treating provenance as a transfer right.

The direct priority argument does not repair root equality: once the root
returns to base, a sacrificed later owner or an already under-base priority
coordinate prevents an automatic lexicographic contradiction. Equality is
instead eliminated by
`ROOT_EQUALITY_BASE_RESTORATION_PACKET_SPREAD_ADMISSION_THEOREM_20260814.md`:
nondegeneracy identifies the unique base-restoration support, after which one
incoming or off-packet good makes the root strict and spreads `K`. The
strongest unconditional root statements are therefore the strict packet-
price cut and

\[
 v_r(R)\le v_r(D)-\delta
\]

for every compatible exterior mode in the root safe-whole-hit theorem.  It
uses the actual common-safe core `D` and named current recipient.  A proper
subpacket is admitted only under the recipient-feasibility and typed
sacrifice hypotheses of the priority-sacrifice split theorem.

## Smallest live provenance/underpayment theorem

Starting from the exact originating `G0--G10` row, prove that one of the
following is available:

1. the historical recipient `u` is the current typed recipient `t` and the
   packet/subpacket meets the required floor;
2. strict aggregate underpayment forces a different retired packet or anchor
   label with a well-founded global decrease;
3. failure of those premises forces a root/anchor exchange, PI cycle,
   response-rank improvement, or contradiction to the retirement-time
   floor; or
4. an exact full-contract state realizes the underpayment mismatch and thereby
   refutes the proposed bridge.

Historical provenance remains evidence about where `K` moved, not a transfer
option.  Strict release is valid because the clean sacrifice construction is
proved independently of that inference.

## Claim boundary

This correction invalidates no packet accounting, root-margin identity,
support split, nonroot envelope descent, admitted safe-core complete-pool
reduction, or the separately proved strict/equality packet-spread releases.
It withdraws the unsupported historical-reversal inference and the earlier
priority-based equality argument. It does not prove or refute
`T_{L,times}^*`, GG, four-agent EFX, or
general additive EFX.

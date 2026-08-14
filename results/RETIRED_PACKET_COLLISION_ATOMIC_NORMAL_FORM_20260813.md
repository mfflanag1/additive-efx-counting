# Retired-packet collision atomic normal form

**Date:** 2026-08-13

**Status:** cap-free reduction of `T_{L,times}^*` to one holder-price
separator family; the payment/anchor gate remains open

## Input and branch order

Use the frozen charge-or-anchor contract. Let `K` be the named nonempty
retired packet, `h` its current holder, `s` the colliding recipient, and
`A=B dot-union K_s` the original candidate cell. Process recipient-floor
failure, equality, observer/base-floor debt, and release failure in the
contracted order.

The exact accounting is

\[
v_s(K_s)=\mu_s+d_s,
\qquad
p_h(K_s)=\max\{0,v_h(K_s)-\sigma_h\}.             \tag{1}
\]

The first identity never pays the second across independent valuation rows.

## Step 1: direct holder compensation when available

Range over the complete physically releasable return family `mathcal J_h`,
including the old bundle released when `K` was retired and every packet in
its signed supplier component. If some admissible `J` pays (1), transfer
`K_s` to the recipient and `J` to `h`, close the supplier set, and recompute
all EFX comparisons.

- An EFX result is lexicographically above the globally maximal base because
  the earlier protected root remains strict.
- An internally supplied desired cycle is PI.
- A globally minimum new response avoiding `K_s`, or meeting a proper
  nonempty subpacket, reduces the collision incidence or `K`.
- A response adding a matchable source/target reduces response-rank
  deficiency.

The only exact recurrence of this test retains the whole packet `K_s`, the
same deficient response relation, and the same holder-price or observer
separator.

## Step 2: priority-valid sacrifice when direct payment fails

Direct payment is not a prerequisite for an EFX endpoint. Keep the earlier
strict root represented and test the colliding assignment while allowing the
later holder to be the sacrificed owner. Apply the protected whole-bundle
acceptance graph to the tested allocation.

1. A perfect protected matching is an EFX lexicographic contradiction.
2. A two-head alternating obstruction has a root-covered maximum matching
   and enters rank-three compression or the two-core/two-hole boundary.
3. A one-head row accepting a nonroot target enters the nonroot compression
   star; payment of its displaced later owner is unnecessary.
4. The only one-head row not covered is a nonroot head whose sole accepted
   target is the root target.

The rank-three and nonroot compression stars are processed by the existing
cut-and-choose and `2 x 2` response results. They give EFX, PI, a strict
rank/source improvement, or an empty-target/lower-dimensional response. At
an exact `T_{L,times}^*` recurrence, any remaining response meeting a proper
subpacket of `K_s` reduces `K`. A newly selected ledger-free response reduces
the current hitting incidence, but an already repeated normalization-bypass
response is a separate atomic survivor below; it is not counted as progress
again.

## Atomic survivor A: whole-packet bilateral ping-pong

The sacrificed holder's globally minimum response to the recipient's new
target contains all of `K_s`. The reverse sacrifice/compression returns all
of `K_s` to `h`; every proper subpacket, ledger-free replacement, and
matchable outside source has already been exhausted. The two time-adjacent
responses cannot be called a PI two-cycle because their physical cores both
use the same packet `K_s`.

The exact surviving data are:

1. `s` loses her typed floor when `K_s` is cancelled;
2. `h` loses her admissible floor or direct safety when `K_s` is transferred;
3. every globally minimum repair on either side contains the whole same
   packet;
4. the response relation remains rank deficient; and
5. no disjoint supplier-closed compensation packet pays the losing side.

The whole-packet atomwise-criticality lemma sharpens the strict-capture
version.  If any `g in K_s` has recipient value below the strict margin
`mu_s`, deleting `g` leaves a strict safe candidate with a proper collision
packet.  Hence the exact survivor satisfies

\[
v_s(g)\ge\mu_s\quad(g\in K_s),
\qquad
(|K_s|-1)\mu_s\le d_s.                           \tag{2}
\]

In particular `mu_s>d_s` forces `K_s` to be a singleton.  The remaining
**atomwise-critical whole-packet bilateral deadlock** is not reversed by
recipient capture alone.

## Atomic survivor B: root-facing anchor-critical packet

If the unique underfunded head accepts only the root target, apply the
root-anchored two-hole selector. A successful partition enters the preceding
two-hole outcomes. Every failure identifies a least good that is either
root-floor/EFX critical or belongs to the protected anchor.

If a post-handoff-safe backup root response exists and pays every unchanged
target, the retire-on-backup exchange returns the old anchor to its supplier
and closes by controlled anchor release. Generic `T_{L,times}^*` does not
include that safety/payment premise. The survivor is therefore the
**root-facing anchor-critical packet**: every holder-paying/root-feasible
repair cuts the anchor or violates the root floor, and no independently safe
paid backup is present.

The root-facing surplus-band dichotomy sharpens this survivor. If the root
bundle has value `x+delta` and `D` is a globally minimum safe response, then
`v_r(D)>x` reselects `D`, while `v_r(D)<delta` releases `D` and leaves its
complement strictly above the base. Hence survivor B additionally satisfies

\[
\delta\le v_r(D)\le x.
\]

In particular it is impossible when the current root bundle is worth more
than twice the base root bundle.

The root-facing holder-price duality further shows that the surviving band
is not a separate payment phenomenon.  If released packet `R` accompanies
the split, the root's exact compensation price is

\[
\pi_r(D)=v_r(D)-\delta,
\qquad 0\le\pi_r(D)\le x-\delta,                 \tag{3}
\]

which is precisely the general holder release price with root slack
`delta`.  Survivor B is therefore the root-labeled bounded subcase of the
same holder-price separator appearing in A.

## Atomic survivor C: normalization-bypass recurrence

The original active selector collides with `K_s`, but canonical cancellation
preserves its recipient floors and produces a non-EFX allocation whose
globally minimum response `E` is ledger-free. The same complete allocation,
response, rank-deficient matching, and colliding original selector then
repeat. Since `E` already avoids `K_s`, its first extraction cannot be
reported again as a reduction of hitting incidence.

If the complete continuation pool generated by `E` also avoids retired
support, the state projects to the parked-support subtype
`T_{L,perp}^*`; closing that subtype is a different theorem. Otherwise the
first later continuation meeting retired support returns to survivor A or B
with an exact first-collision label. The unresolved case is an exact
alternation between the ledger-free response and a colliding selector with
neither rank improvement nor a permanent selector-priority change.

The normalization-bypass reservoir-reversal lemma now processes `E` against
every disjoint current owner reservoir.  Inclusion-minimal extraction at the
corresponding observer threshold gives either a disjoint current-safe payment
packet or a reversed disjoint current-safe desired packet.  A proper hit on
`K_s` shrinks the collision, a whole hit returns to A or B, and a newly
matchable source/target reduces rank deficiency.

If all three reservoirs reverse unsafely, the three-reservoir fan theorem
adds the fourth physical edge supplying `E` and obtains a supplier-closed PI
cycle in every source pattern.  Consequently the exact C survivor is
narrower than an arbitrary reset: at least one reservoir supplies a safe
packet `Q` with `v_h(Q)>=tau_h(E)`, while the same deficient response relation
persists.

The protected target-envelope refinement sends every all-unsafe pattern to
PI.  A safe envelope packet owned by someone other than the response source,
or an unsafe reversal with a different source, enters the existing two-core /
two-hole machinery.  The sole new local survivor is the **safe-center three-
offer star**: the center's whole bundle is common-safe, while three disjoint
safe offers from the other owner bundles are all desired by that center.  An
unsafe center would itself create a supplier-closed PI 2-cycle.

The canonical center-return test then swaps a leaf's own offer to the center
and the common-safe center bundle to that leaf.  A successful protected row
enters two-hole machinery.  Hence the exact star survivor additionally obeys

\[
v_h(U_s)<\max\{F_h,\tau_h(O_h)\}
\qquad\text{for all three leaves }h.              \tag{4}
\]

It is a three-row center-return rejection separator.

Finally split on the first-priority root.  If the center is not the root,
the root is one of the three offer suppliers, so its arm is exactly the
root-holder price gate or a protected two-core/two-hole input.  If the center
is the root, canonical normalization first retains every retired good that
cannot leave the old root.  An unsafe enlarged root core returns to the named
collision branches.  If the retained root core is safe, allocate the
complement EFX among the other three agents; every remaining failure is
exactly the already-certified one-core/three-hole external-star normal form.
Thus C introduces no third independent separator.  Its residual content is
the inherited root-centered external-star signs or the existing holder-price
collision, both with retired-packet provenance intact.

The ledger-normalized external-star ascent theorem eliminates those signs as
an independent recurrence.  A root-to-hole wall gives a strictly higher safe
root candidate, a distinct nonroot response, or a retired collision; the
executed root value cannot rise indefinitely over the finite bundle set.  At
a state with no root-to-hole wall, every hole-to-root wall extracts a safe
proper response inside the root core and enters root reselection, controlled
release, retired collision, or the bounded root-holder price band.  Thus C
also returns to the holder-price family or already existing rank/two-hole
progress.

The smallest missing operation is now a star allocation or three-way holder-
price argument: assign one offer to the center while protecting its supplier
and the two remaining leaves, or show that all three failed arm transfers
enter the already isolated holder-price family.

## Typed branches

### Strict capture

`mu_s>0` supplies recipient surplus but not holder payment. Direct
compensation, protected sacrifice, and response-rank routing leave only
atomic survivor A, B, or the normalization-bypass survivor C.

### Equality critical

`mu_s=0` supplies no strict recipient margin. The earlier strict root still
makes a separately valid EFX sacrifice endpoint lexicographic, but no such
handoff is assumed when its physical/protected premises fail. The survivor
is the equality-labeled version of A or B, or a weakly paid instance of C;
it cannot be promoted to a strict response.

### Base-floor debt

The exact mixed old/new separator is an underfunded protected row. The
protected matching/compression chain either upgrades that row, reduces rank
deficiency, or reaches the same root-facing/whole-packet/bypass survivors.
Supplier saturation alone does not pay this debt.

### Release failure

Every proposed edge is closed under its signed suppliers. An outside supplier
strictly enlarges the owner component; at four-owner saturation an internally
supplied disjoint cycle is PI. A repeated release failure with overlapping
cores is not PI and belongs to whole-packet survivor A; a root-only supplier
cut belongs to B.

## Exact remaining theorem

The original charge-or-anchor theorem is now equivalent, within the frozen
`T_{L,times}^*` interface, to eliminating the one holder-price separator
family represented by A and B:

1. eliminate the atomwise-critical whole-packet bilateral deadlock, already
   localized by (2), through a rank-improving third response or a physically
   compensated transfer; and
2. pay or contradict the bounded root-holder price (3), or construct a
   controlled release valid at its equality boundary; and
3. carry every normalization/two-hole return through the ledger-normalized
   external-star ascent, which now routes back to 1--2 or strict rank/root
   progress rather than forming a separate terminal.

The complete-pool threshold reversal sharpens 1--2.  If the complete
downward-closed compatible compensation pool reaches the holder price, an
inclusion-minimal crossing packet either pays safely or reverses into a
genuine current-safe response.  Hence after response/rank routing the exact
remaining scalar certificate is

\[
v_h(\mathcal R_h)<p_h
\]

for the complete compatible pool `mathcal R_h`.

If one is false, the missing operation is respectively controlled
unretirement/packet splitting or controlled anchor release with explicit
observer debt; normalization no longer adds a separate missing operation.
A counterexample must still
satisfy global GG maximality; the existing local payment witnesses do not.

## Dependencies and claim boundary

This reduction uses the protected-bundle Hall dichotomy, one-head nonroot
compression, alternating two-head root-covered compression, two-hole
cut-and-choose, `2 x 2` response closure, root-anchored one-head selector,
and the conditional retire-on-backup theorem, each with its original
premises.

The root-facing survivor is further reduced by
`ROOT_FACING_ANCHOR_SURPLUS_BAND_DICHOTOMY_20260813.md`.
Its exact payment wall is identified by
`ROOT_FACING_HOLDER_PRICE_DUALITY_LEMMA_20260813.md`.

The strict whole-packet survivor is further reduced by
`WHOLE_RETIRED_PACKET_ATOMWISE_CRITICALITY_LEMMA_20260813.md`.

The normalization-bypass survivor is further reduced by
`NORMALIZATION_BYPASS_RESERVOIR_REVERSAL_LEMMA_20260813.md`.
Its all-unsafe branch is sharpened by
`NORMALIZATION_BYPASS_THREE_RESERVOIR_FAN_DICHOTOMY_20260813.md`.
The complete-target envelope and protected pair/star reduction are in
`TARGET_ENVELOPE_UNIVERSAL_PAYMENT_OR_PI_LEMMA_20260813.md` and
`TARGET_ENVELOPE_PROTECTED_PAIR_OR_SAME_SOURCE_STAR_LEMMA_20260813.md`.
The star's direct return is resolved by
`SAFE_CENTER_THREE_OFFER_RETURN_OR_REJECTION_LEMMA_20260813.md`.
Its fixed-priority routing is
`SAFE_CENTER_THREE_OFFER_PRIORITY_SPLIT_REDUCTION_20260813.md`.
The inherited star signs are reduced to ascent/rank/root price by
`LEDGER_NORMALIZED_ROOT_EXTERNAL_STAR_ASCENT_OR_PRICE_THEOREM_20260813.md`.
The final holder gate is sharpened by
`COMPLETE_HOLDER_PRICE_POOL_REVERSAL_OR_UNDERPAYMENT_LEMMA_20260813.md`.

The reduction is cap-free and performs no valuation-cell or residual-only
search. It does not eliminate A--C, refute them under complete GG
maximality, close `T_{L,times}^*`, close GG, or prove four-agent/general EFX.

# Cap-free seven-endpoint or hidden-split reduction

**Date:** 2026-08-14

**Status:** exact cap-free reduction; hidden-split conversion remains open

## Theorem

Consider a physical saturated root-facing rank-three fixed-`U` state whose
named packet pieces compress to the twelve symbols

\[
a_0,a_1,h,j,k,q_0,l,e,m,g_q,g_r,p
\]

used by the allocated-`E` form-2 master.  Interpret every response, EFX tail,
and desired-core predicate in the physical state using deletion of one
physical good.  Then at least one of the following holds:

1. one of `Z1,...,Z7` is a complete physical EFX allocation using at most
   four support-provenance transfer edges;
2. the physical state contains a closed pairwise-disjoint family of
   common-safe desired cores, hence a generalized PI; or
3. there is a selected nonsingleton packet atom `C`, an observer `i`, and a
   least physical good `g` strictly inside `C` such that, for the relevant
   bundle/core `S`,

   \[
   v_i(g)<v_i(S)-1\le
   \min_{D\in\mathcal C(S)}v_i(D),                 \tag{1}
   \]

   where `mathcal C(S)` is the compressed-atom partition of `S`.

Alternative 3 is the **strict hidden-minimum split**.  It is a proper physical
split of `C`; its statement is independent of `|C|` and of the total number
of goods.

## Proof

Compress every named physical packet piece to one additive atom carrying its
total value for each observer.

### Step 1: transfer the master premises

The allocated-`E` master uses only the following kinds of facts:

- positivity, normalization, and comparisons of packet totals;
- positive common-safe response predicates on named packet unions;
- negative response/PI predicates on enumerated named packet unions;
- the induced response graph, its exact form-2 edge pattern, and the absence
  of response rank four.

Total statements are unchanged by compression.  A physically common-safe
bundle remains safe after an entire compressed atom is deleted, because
deleting the whole atom removes at least as much value as deleting one good.
Thus every required physical response remains a compressed response.

Suppose instead that a compressed response, edge, or desired core appears
where its physical analogue is forbidden.  Desire is unchanged by
additivity, so the discrepancy must be in common safety.  The physical
packet-compression hidden-minimum lemma then gives (1), which is alternative
3.  Consequently, if alternative 3 does not occur, every response predicate
used by the master agrees between the compressed and physical readings.  The
compressed totals therefore satisfy the complete allocated-`E` form-2
master, including its response graph and PI-free premises.

### Step 2: invoke the exact bounded dichotomy

The dual-verified twelve-atom theorem states that every model of that master
has either a compressed generalized PI or one of the seven compressed EFX
endpoints.

If it supplies a compressed generalized PI, source desire and disjointness
are preserved on physical expansion.  If any expanded core is not physically
common-safe, the hidden-minimum lemma again gives alternative 3.  Otherwise
the expanded family is a physical generalized PI, giving alternative 2.

If it supplies a compressed endpoint `Zk`, completeness and its support-edge
count are unchanged on physical expansion.  If the expanded allocation is
not physical EFX, apply the hidden-minimum lemma to a failing observer-target
bundle and obtain alternative 3.  Otherwise it is a complete physical EFX
allocation with the same at-most-four support edges, giving alternative 1.

This exhausts the cases.

## What this removes

Arbitrary packet cardinality is no longer an unstructured obstruction to the
seven-endpoint proof.  No new qualitative failure can appear merely because
a packet contains three, ten, or a thousand goods: every compression failure
has the strict form (1).  The remaining work is about supplier, priority, and
anchor compatibility of that proper split, not packet size.

## Sharpening on the PI-clause branch

Every clause in the minimized certificate has three or four pairwise-
disjoint compressed desired cores. The cap-free physical Hall-lift lemma
shows that expansion of such a clause has the sharper trichotomy:

1. a physical generalized PI;
2. a common-safe desired core sourced by an owner outside the represented
   source set, hence an external response/component coordinate; or
3. an explicit Hall-deficient subset of the represented sources.

See `DISJOINT_COMPRESSED_CORE_PHYSICAL_HALL_LIFT_LEMMA_20260814.md`. Thus an
unsafe expanded PI clause need not remain merely a least-good witness: global
minimal-core extraction turns it into the exact owner-side Hall obstruction
being studied in the companion track. Hidden-minimum splitting remains the
primitive discrepancy for transfer of the master premises and for a
compressed EFX endpoint that fails physical EFX.

The minimized 425-clause proof core alone cannot guarantee that the selected
compressed EFX allocation is nearly owner-paid: exact profiles defeat
all-owner, fixed-`d`, one-hole, and two-hole variants. Every such profile has
another generalized PI, however, so this does not settle the strengthening on
the fully PI-free domain. See
`SEVEN_ENDPOINT_PAYMENT_STRENGTHENING_NO_GO_20260814.md`.

The complete PI pool does yield a valid strengthening. The dual-verified
`ALLOCATED_E_TWO_PAYMENT_HOLE_SEVEN_ENDPOINT_THEOREM_20260814.md` proves that
every fully generalized-PI-free compressed profile has one of `Z1`--`Z7`
complete EFX with at most two owners below their base utilities. Payment is
preserved exactly on physical expansion because it depends only on packet
totals. Hence if that endpoint fails physical EFX, every failed observer
outside the at-most-two hole set exposes a base-desired response; only the two
hole owners can require current/decorated debt accounting.

Combining this with the physical Hall-lift lemma gives the sharper cap-free
frontier:

1. physical complete EFX through at most four support edges;
2. physical generalized PI or external response augmentation;
3. a minimal Hall deficiency, which has a near-perfect one-hole response
   matching and at most three response edges; or
4. a physically unsafe compressed EFX endpoint with at most two base-payment
   holes and an explicit hidden-minimum/current-response witness.

Thus neither arbitrary packet cardinality nor an arbitrary number of payment
holes remains in the declared form-2 chart.

## Interface with the companion EFX-2 track

When the hidden atom is the retired packet in the companion track, its
proper-retired-packet split theorem converts recipient-feasible hidden splits
into physical separation, after which a target-local response cannot
reassemble the retired packet. Its strict-root-overpayment lemma also closes
every compatible such split that pays the root with positive slack.

Accordingly, after a provenance argument identifies an alternative-3 witness
with that retired-packet interface, it must survive one of the exact companion
obstructions:

- recipient top-up deficiency/indivisibility;
- absence of any root-paying compatible packet; or
- the equality case, which bundle nondegeneracy collapses to the unique
  signed base-restoration exchange and its hitting cut.

These are structural restrictions on the hidden split.  They are not assumed
away here.

## Verification record

The bounded input is
`results/ALLOCATED_E_SEVEN_ENDPOINT_BOUNDED_DICHOTOMY_20260813.md`, backed by
the independent minimized-core replay
`results/allocated_e_form2_all_allocation_minimized_unsat_core_audit.json`.

The cap-free compression implication is proved in
`results/PHYSICAL_PACKET_COMPRESSION_HIDDEN_MINIMUM_LEMMA_20260814.md` and
independently audited for arities 1 through 12 by
`tracks/parkability/audit_packet_compression_hidden_minimum.py`; every
negated implication is UNSAT.

## Claim boundary

Proved: subject to the declared physical analogues of the allocated-`E`
form-2 master premises, a cap-free trichotomy between four-edge complete EFX,
physical generalized PI, and the explicit strict hidden-minimum split (1).

Not proved: that every saturated GG state falls into this allocated-`E`
form-2 chart, that every hidden split preserves all protected owner floors,
that every hidden atom routes to the companion retired packet,
that every Hall deficiency collapses to the companion two-creditor form,
that the base-restoration hitting cut forces PI or lexicographic progress, or
the universal four-edge/general EFX theorem.

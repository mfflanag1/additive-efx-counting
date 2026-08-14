# External-Hall full-owner recruitment lemma

**Date:** 2026-08-14

**Status:** cap-free component reduction; only the represented-cycle form-R3
`2x1` star remains outside the full-owner charity-exchange terminal

## Initial matching components

Reverse the selected rank-three matching before parking the singleton
charity.  At the owner-component level the two exact response forms have

\[
 R_2:\quad \{r,q\}\mid\{s,d\},
 \qquad
 R_3:\quad \{r,q,s\}\mid\{d\}.                 \tag{1}
\]

Packet cardinalities and values do not affect (1).

Let `J` be an inclusion-minimal external Hall defect in the universally safe
source-parking relation.  Thus either

\[
 |J|=2,\ |N(J)|=1,
 \qquad\text{or}\qquad
 |J|=3,\ |N(J)|=2,                               \tag{2}
\]

and every target in `J` has a response neighbor.  Attach every response
incidence between `J` and `N(J)` to the physical owner-component graph (1).

## Recruitment theorem

Exactly one of the following holds.

1. The resulting decorated response component contains all four owners.
2. The selected relation is `R3`, `J` and `N(J)` partition the three
   represented owners `{r,q,s}`, and the defect is a `2x1` star.  Equivalently
   the only owner outside the decorated component is `d`.

For `R2`, a `2x1` star uses three distinct owners and therefore meets both
two-owner components in (1); its two response incidences join them.  A `3x2`
defect uses all four owners and also joins the components.

For `R3`, every defect involving `d` joins the singleton component to the
represented three-cycle.  In a `3x2` defect, even when `d` is the unmatched
target of the displayed near-perfect fork, minimality gives `d` a neighbor
in `N(J)`, so the complete decorated relation still recruits it.  The only
way not to recruit `d` is therefore to place the two star targets and its
one external source entirely in `{r,q,s}`.

No valuation or packet-size assumption is used.

## Consequence under the frozen saturation contract

For every outcome 1 response, the fixed-U state already contains the full
signed response data, all-owner coverage, and the component-wide selectors
listed in items 7--12 of
`FIXED_U_RANK_THREE_FOUR_EDGE_PREMISE_LEDGER_20260813.md`.  If a bridge,
redistribution, new response/release label, PI component, or strict
same-record progress exists, saturation is contradicted.  Otherwise the
response reaches the exact full-owner base-margin separator excluded by
`UNIVERSAL_FULL_OWNER_CHARITY_EXCHANGE_EXTRACTION_THEOREM_20260812.md`.

Thus, subject to statement-integrity verification that the accumulated
source-parking response carries the same complete signed decoration required
by that theorem, every external Hall fork and every star involving `d`
closes cap-free.  The external-Hall part of the active fixed-U theorem reduces
to three owner-label cases:

\[
 \{q,r\}\leftarrow\{s\},\qquad
 \{q,s\}\leftarrow\{r\},\qquad
 \{r,s\}\leftarrow\{q\}.                        \tag{3}
\]

Each star contains one selected `R3` cycle edge and one represented-cycle
chord.  Its remaining physical obstruction is exactly the edge-overflow
case in which the chord core mixes retained target support with a proper
incoming matching packet.  The next lemma need only handle this
three-owner chord while recruiting or safely parking `d`.

## Claim boundary

Proved: the cap-free owner-component classification (1)--(3).

Conditional composition: full-owner defects close only after checking that
the source-parking response satisfies the exact decorated-response and
base-margin interface of the cited full-owner theorem.  This document does
not silently infer those scalar premises from graph connectivity.

Not proved: closure of the three represented-cycle stars, the unconditional
fixed-U four-edge theorem, or general additive EFX.

# Rank-three matching charity-relay four-edge theorem

**Date:** 2026-08-14

**Status:** candidate cap-free reduction; the imported complete collision
closure has an unproved nonroot normalization-bypass branch

## Frozen rank-three input

Let `(Y,{p})` be a saturated root-facing rank-three state from
`FIXED_U_RANK_THREE_FOUR_EDGE_PREMISE_LEDGER_20260813.md`.  Let the selected
nonself response matching `M` have three distinct represented sources

\[
                         S=\{r,q,s\}
\]

and three distinct physical owner targets.  The first-priority root `r` is
represented and the unique unmatched source is the sacrifice-eligible owner
`d`.  For each `i in S`, let

\[
 C_i\subseteq Y_{t(i)}.                            \tag{1}
\]

This is the selected physical common-safe desired core at its recorded
base/current floor.  The root edge of `M` is the permanent ordinary anchor,
so its selected core additionally satisfies

\[
                         v_r(C_r)>v_r(X_r).        \tag{1a}
\]

No base-payment assertion is needed for the other two represented sources:
their later floors will be recomputed at the displayed allocations.
Distinct matching targets make the three cores disjoint.  The singleton
charity good `p` is positive and base-safe.  No response-graph or packet-size
strengthening is added here.

## Matching rotation with charity retained

For every owner target `j`, let `O_j` be the unique selected core removed
from `Y_j`, or the empty packet if `j` is the unmatched target.  Define the
partial support allocation `B` by

\[
 B_i=(Y_i\setminus O_i)\mathbin{\dot\cup}C_i
       \quad(i\in S),
 \qquad
 B_d=Y_d\setminus O_d,                            \tag{2}
\]

and leave `{p}` in charity.  This conserves every good and uses precisely
the at-most-three reversed matching pairs `t(i)->i`.  In particular,

\[
 v_r(B_r)\ge v_r(C_r)>v_r(X_r).                  \tag{3}
\]

Thus the selected matching itself supplies the strict first-priority root;
no detachable old root surplus, donor payment, or residual provenance is
needed.

## Stage, retire, and return the charity singleton

Use two complete allocations:

\[
 R=(B_r+\{p\},B_q,B_d,B_s),
 \qquad
 D=(B_r,B_q,B_d+\{p\},B_s).                      \tag{4}
\]

Relative to the original support state `(Y,{p})`, each allocation uses the
three reversed matching pairs plus one charity pair.  Hence both use at
most four support-provenance transfer edges, regardless of packet sizes.
Both have the first-priority root strictly above the base by (3).

Test `R` first.  If it is EFX, it is the required endpoint.  Otherwise apply
the controlled floor reset at the actual allocation `R`, retain the physical
matching/anchor/supplier decoration, and adopt a globally minimal failed
response coordinate.

Next move only `p` from the staged root to `d`, obtaining `D`.  If `D` is
EFX, stop.  Otherwise reset at `D`, adopt its globally minimal failed
response, and record the move `r->d:{p}` as a one-good retirement under the
unchanged selected root-anchor support `C_r`.  Its new holder `d` pays the
retirement-time reset floor

\[
                         F_d=v_d(B_d+p).          \tag{5}
\]

Finally retest `R` by returning the whole retired singleton `p` from `d` to
the root.  Owners `q,s` are unchanged, the already-strict root improves, and
`d` is the unique reset-floor hole.  The retired good captures that deficit
exactly:

\[
 F_d-v_d(B_d)=v_d(p)>0.                           \tag{6}
\]

Canonical cancellation of the attempted return leaves `p` with its current
holder `d` and restores exactly the already failed complete allocation `D`
and its adopted response.  The returned allocation `R` is also already
known non-EFX from the first test.  Therefore, at a saturated exact repeat,
the packet, retirement supplier/current holder, same physical root anchor,
protected-floor capture (6), colliding return, failed canonical
normalization, and repeated signed response form a complete
normalization-bypass/protected-floor `T_{L,times}^*` certificate.

Commit `34709c9ce22dbde23a5fa381a2ccea7898dfe1ca` claims to exclude that
terminal, but `NONROOT_NORMALIZATION_BYPASS_COLLISION_GAP_20260814.md` shows
that its cited dependencies do not cover a nonroot holder when the repeated
normalized response avoids `p`.  Hence simultaneous failure of `R,D`
currently reduces to that exact gate; it is not yet contradictory.

## Why this reaches the full active predicate

The construction uses only data explicitly required by the frozen target:

1. the current physical allocation and singleton charity;
2. the selected rank-three nonself matching;
3. its three disjoint physical base-desired cores, including the represented
   first-priority root;
4. the unique unmatched sacrifice-eligible owner; and
5. exact current suppliers and the signed response record.

It does not pass through the allocated-`E` twelve-atom chart, assume a
release-compatible owner cycle, split a named packet, or invoke a bounded
atomization.  The matching rotation gives three owner edges and the charity
relay gives the fourth.

## Semantic dependency and claim boundary

The physical allocation, edge, strict-root, reset-payment, capture, and
cancellation statements are theorem-level identities and are independently
replayed by
`audit_rank_three_matching_charity_relay_four_edge.py`.

One proof-language question remains load-bearing before unconditional
promotion: the controlled reset must be accepted as an actual signed-state
operation at both `R` and `D`, so that the response at `D` licenses the
retirement insertion and the fixed return selector enters the frozen
collision theorem.  This is the same new operation already isolated for
external review in `STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMISSION_THEOREM_20260814.md`,
not a new valuation inequality.

Closure of the missing normalization-bypass branch would prove the complete
active saturated rank-three fixed-`U` four-edge objective with unrestricted
packet sizes.  This document does not yet prove that branch, the global
BCFF-to-GG import, four-agent additive EFX, or general additive EFX.

## Cross-state localization update (2026-08-14)

The disjoint bypass is no longer an arbitrary repeated response.  Applying
`SINGLETON_RELAY_CROSS_STATE_RESPONSE_LOCALIZATION_LEMMA_20260814.md` to the
two rows in (4) gives an exhaustive cap-free split.  Every response avoiding
`p` is either a safe desired response at both probes, or its failure to cross
from one probe to the other is confined to a singleton-width interval in
one of exactly two rows:

\[
 v_r(B_r)<z\le v_r(B_r+p),
 \qquad\text{or}\qquad
 v_d(B_d)<z\le v_d(B_d+p).
\]

The same localization holds for observer safety thresholds.  Thus the live
composition problem is now: route a shared safe response through the exact
rank-three relation, or eliminate the simultaneous `r/d` singleton-critical
separator using the saturated response/support record.  No response sourced
by `q` or `s`, and no unbounded residual packet, creates another scalar
branch.  This sharpens but does not close the theorem.

## Four-placement upgrade (2026-08-14)

The two critical safety bands disappear if the singleton is tested at all
four owners.  Each test still uses the same three reversed matching pairs
plus one charity pair, so the four-edge bound is unchanged.  Choose a failed
response of globally minimum cardinality across the four complete probes.
By `FOUR_PLACEMENT_SINGLETON_RESPONSE_TRANSPORT_LEMMA_20260814.md`, every
response avoiding `p` is safe at all four probes and remains desired at all
but possibly the placement that parks `p` at its own source.

Thus observer-safety transport is no longer the live scalar gate.  The
remaining obstruction is a source-parking/matching problem for universally
safe minimum cores: either parking neutralizes the current core and raises
minimum response size, another source supplies a same-size core, or a
response hits `p`.  A Hall-compression lemma for the accumulated cores would
complete the relay route; it is not proved here.

The disputed root-holder collision theorem can also be removed from this
route.  Test the three probes placing `p` at `q,d,s`.  A response hitting `p`
then has a nonroot holder.  A root source is the saturated strict-anchor
reselection exit; a nonroot source enters the strict safe-envelope descent.
See `NONROOT_THREE_PLACEMENT_RELAY_COLLISION_ELIMINATION_20260814.md` and
`NONROOT_SINGLETON_HIT_SAFE_ENVELOPE_DESCENT_LEMMA_20260814.md`.  Hence the
only live relay branch is disjoint universally safe source-parking Hall
compression; neither the root singleton supplier-star nor the overclaimed
complete `T_{L,times}^*` composition is needed.

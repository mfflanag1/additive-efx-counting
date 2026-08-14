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

The surviving Hall relation is also sharply classified.  By
`FOUR_OWNER_NONSELF_MINIMAL_HALL_DEFECT_CYCLE_LEMMA_20260814.md`, every
internal inclusion-minimal defect contains a 2- or 3-cycle and is the
generalized-PI exit after parking `p` outside that cycle.  Hence only two
external-source shapes remain: two targets with one source, or three targets
with two sources including one outside the target set.  The unresolved issue
is now physical supplier compatibility/one-hole repair for those two stars,
not an arbitrary rank-three response graph.

For the `2x1` star, the signed edge budget is now exact; see
`TWO_TARGET_EXTERNAL_SOURCE_FOUR_EDGE_SUPPORT_FRONTIER_20260814.md`.  The
charity path stays within four original supplier pairs only when the chosen
response redirects the target's incoming matching packet, with a narrowly
specified return-to-supplier exception allowing retained support.  A generic
mixed residual response necessarily creates a fifth edge.  Thus the next
analytic decision is whether saturation forces one of those compatible
cores, or instead forces the `3x2` fork/matching change.

The `3x2` fork is now completely classified at the signed-support level by
`THREE_TARGET_EXTERNAL_SOURCE_FORK_EDGE_CANCELLATION_FRONTIER_20260814.md`.
Across the two exact response forms and all role/support incidences, 156 of
720 nonempty fork patterns use at most four original supplier pairs; the
other 564 are excluded by edge count alone.  Every feasible fork satisfies
the exact cancellation condition that each newly created supplier pair is
offset by exhaustion/return of an old matching pair.  The remaining theorem
is consequently a valuation/saturation decision on a finite 2x1-plus-156
signed support menu, followed by a cap-free argument that overflowing mixed
cores activate support refinement rather than recurrence.

## Full-owner recruitment and represented-star absorption update

The external Hall menu does not remain a generic finite valuation problem.
At the owner-component level, every `R2` star/fork and every `R3` fork or
star involving `d` recruits all four owners.  Under the frozen saturation
contract those responses enter the component-wide selector and, after its
nonterminal outcomes are excluded, the exact full-owner charity-exchange
separator.  Only three `R3` stars wholly inside `{r,q,s}` avoid that immediate
recruitment; this classification is exact and cap-free.

For each residual star, complete both incoming cycle packets and move both
star targets to their common source.  The two corresponding old cycle edges
cancel, leaving exactly the other two represented suppliers pointing to the
common source; charity adds the third edge.  Any repeated response by that
same source into either depleted target uses an existing pair and strictly
shrinks a finite residual union.  Hence a sole-source represented star cannot
recur.  See `EXTERNAL_HALL_FULL_OWNER_RECRUITMENT_LEMMA_20260814.md` and
`R3_REPRESENTED_STAR_DOUBLE_ABSORPTION_LEMMA_20260814.md`.

The live branch is now the first *different* old represented response source
after double absorption.  A new source/core/release coordinate is saturation
progress; a response involving `d` is full-owner recruitment.  What remains
to prove is that an already recorded response wholly inside the represented
component closes physical generalized PI or carries the exact signed
base-margin data needed by the full-owner theorem.

## Root-preserving represented-star update

The two represented stars whose common source is later than the protected
root admit a sharper physical operation.  Complete the incoming packet at
the nonroot star target, but move only the chosen response core at the root.
The unused part of the root's incoming packet remains at the root.  One old
cycle edge is therefore preserved and the other is cancelled; exact signed
enumeration leaves at most three owner-transfer pairs, so charity is the
fourth edge.

Let `A` be the permanent root anchor and `E_r` the chosen response core in
the root target.  The operation is priority-valid whenever

\[
                  v_r(A\setminus E_r)>v_r(X_r).
\]

If this inequality fails, additivity forces the exact alternative

\[
 v_r(E_r\cap A)\ge v_r(A)-v_r(X_r)>0.
\]

See `R3_LATER_SOURCE_ROOT_PRESERVING_STAR_FRONTIER_LEMMA_20260814.md`.
Consequently the different-source represented branch is no longer an
untyped PI/base-margin alternative.  Its sole scalar terminal is a
current-safe later-source response into the root whose physical anchor
intersection covers the root's entire strict permanent-anchor margin.
Converting that captured packet into a release-compatible PI/full-owner
exchange or a strict replacement anchor remains unproved.

The first uncrossing layer is now exact.  Retain a packet `H` from the
captured anchor overlap, move the rest of the response, and give the charity
singleton to the response source.  This preserves the four-edge bound.  It
returns to the strict-root continuation whenever

\[
 v_r(H)>v_r(X_r)-v_r(A\setminus E_r),
 \qquad
 v_x(H)<v_x(E_r)-F_x+v_x(p).
\]

If no such packet exists, an inclusion-minimal root-feasible `H_*` satisfies
a sharp bicriteria separator: deleting any one of its goods destroys the
root threshold, while its source value covers the whole response margin plus
the singleton.  See
`R3_SINGLETON_COMPENSATED_ANCHOR_UNCROSSING_FRONTIER_20260814.md`.  The
separator is scalar-feasible, so its elimination must use complete signed
supplier/saturation data; the two valuation rows alone cannot finish the
theorem.

An exact bounded decision now supplies a concrete routing target.  In the
allocated-E form-0 twelve-atom cell, complete generalized-PI exclusion forces
an EFX allocation on the single Hamiltonian path

\[
             \mathrm{charity}\to r\to q\to d\to s.
\]

All 343 stay-or-forward packet choices were negated; the master became UNSAT
after 21,934 PI cuts and replays from a 70-cut core.  See
`ALLOCATED_E_FORM0_HAMILTONIAN_PATH_BOUNDED_THEOREM_20260814.md`.  The
remaining cap-free theorem is therefore not arbitrary graph search: it is a
three-cut path-partition lemma whose failure must activate closed PI or the
full-owner base-margin separator.  The bounded result does not itself prove
that lift or cover form 2.

The cap-free algebra behind the form-0 path is also exact.  Its three reverse
response cores strictly pay the three downstream owners, and only the root
can be unpaid.  The failure inequality is a single root-capture separator;
see `FORM0_FULL_OWNER_HAMILTONIAN_PATH_PAYMENT_LEMMA_20260814.md`.  This
places form 0 directly at the existing full-owner signed-interface audit.
The surviving form-2 R3 cycle remains the genuinely distinct branch.

Its first explicit compensation topology is now cap-free as well.  Two
responses into the root either uncross into a three-edge supplier star, with
only the `r,d` payment identities left, or their overlap captures both source
margins.  See
`FORM2_ROOT_STAR_DISJOINT_OR_DOUBLE_CAPTURE_FRONTIER_20260814.md`.  Hence the
R3 terminal is no longer a generic shared-target overlap: it is a
double-margin physical packet coupled to the root/current-only-`d` two-hole
separator.

The second menu topology reduces to a single path packet as well.  Returning
the ordinary `d->q` core and compensating `q` from the root gives the
three-edge path `charity->r->q->d`; only a lower bound in the `q` row and an
upper bound in the root row constrain the compensation packet.  See
`FORM2_Q_COMPENSATION_PATH_PACKET_FRONTIER_20260814.md`.  Its failure packet
is exactly the bicriteria anchor-capture object already isolated above.

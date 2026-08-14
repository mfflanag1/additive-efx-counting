# Fixed-U generalized-PI/capture checkpoint

**Date:** 2026-08-13

**Status:** cap-free structural progress; universal four-edge conclusion open

## Cap-free packet-compression update (2026-08-14)

The packet-size interface has now been reduced exactly. Compress each named
physical packet piece to its total value. If any response, desired-core, or
endpoint that is safe in the compressed model fails a physical single-good
tail, the least physical good lies strictly inside a nonsingleton compressed
atom and satisfies

\[
v_i(g)<v_i(S)-1\le \min_{C\in\mathcal C(S)}v_i(C).
\]

Combining this hidden-minimum lemma with the dual-verified seven-endpoint
bounded theorem yields a cap-free trichotomy: complete physical EFX through
one of the seven at-most-four-edge endpoints, physical generalized PI, or an
explicit strict hidden-minimum split. See
`CAPFREE_SEVEN_ENDPOINT_OR_HIDDEN_SPLIT_REDUCTION_20260814.md`.

Thus unrestricted packet cardinality is no longer the open issue. The live
branch is provenance-routing and conversion of the decorated hidden split;
once it lies in the retired-packet interface, the remaining cases are
recipient top-up deficiency or the root/base-restoration hitting cut.

On the three-/four-core PI side, global minimal-core extraction gives an
additional cap-free reduction: every expanded compressed clause yields a
physical generalized PI, an external response source, or an exact Hall-
deficient owner subset. See
`DISJOINT_COMPRESSED_CORE_PHYSICAL_HALL_LIFT_LEMMA_20260814.md`. Hence the
remaining unsafe-core branch is an owner-side Hall/provenance obstruction,
not an unclassified physical-tail failure.

The minimized 425-clause core does not itself strengthen the seven endpoints
to a paid or nearly paid endpoint: exact profiles force one, two, and finally
three simultaneous payment holes while preserving those 425 exclusions. But
each profile has another generalized PI, so the fully PI-free strengthening
was initially undecided. See
`SEVEN_ENDPOINT_PAYMENT_STRENGTHENING_NO_GO_20260814.md`.

That complete gate is now closed. Two independent encodings prove that every
fully generalized-PI-free profile in the twelve-atom form-2 cell has one of
the seven EFX endpoints with at most two base-payment holes. A minimized core
uses 1,966 three-/four-owner PI clauses and all seven endpoints. See
`ALLOCATED_E_TWO_PAYMENT_HOLE_SEVEN_ENDPOINT_THEOREM_20260814.md`.

Since payment survives physical packet expansion exactly, only two observers
can require current/decorated debt accounting when such a compressed endpoint
fails physical EFX. Every other failed observer is automatically base-desired.

## Complete all-allocation R3 bounded decision

The repaired allocated-`E` R3 cell has now been decided against the complete
93,480-member menu of nonempty-owner allocations using at most four support
edges. Exact dynamic CEGAR and an independent literal-tail replay are both
UNSAT. Core minimization leaves only seven explicit complete allocations and
425 three-/four-owner generalized-PI clauses. See
`ALLOCATED_E_SEVEN_ENDPOINT_BOUNDED_DICHOTOMY_20260813.md`.

This supersedes the unresolved R3 status recorded below for the earlier
generalized-PI-only continuation. It is a bounded theorem, not the cap-free
result. The remaining gate is physical-tail compression plus the root/
protected-holder anchor conversion for arbitrary multi-good packets.

## What changed

The prior bounded frontier was incorrectly calibrated against ordinary PI
cycles only. The four apparent selector counterprofiles all contain exact
generalized self-PI cycles. In fact the old full-capture and two-bare masters
force the single edge

\[
                       s\xrightarrow{\{l\}\mid\{p\}}s,
\]

so neither atomization belongs to the saturated domain. A deletion-minimal
UNSAT core in each response form contains only the exclusion of that edge.

The correction is cap-free: whenever an owner replaces part of its base
bundle by a nonempty packet drawn only from base charity and strictly desires
the resulting common-safe core, the corresponding self-edge is a length-one
generalized PI cycle.

## New exact characterization

After canonicalizing generalized champion edges to their assigned desired
cores, a PI cycle exists if and only if some nonempty owner set has:

1. one minimal common-safe desired core per source;
2. pairwise-disjoint cores; and
3. every core good base-owned by a participating owner or base charity.

The cyclic target order is arbitrary. This converts release compatibility
from a labeled-cycle search into a closed set-packing problem.

Two cap-free consequences now apply to every rank-three state:

- the three selected disjoint cores must import base support from unmatched
  owner `d`, or they themselves form PI;
- every common-safe desired core of `d` has its entire strict response margin
  captured by the selected core union, or its disjoint remainder completes a
  four-core PI family.

Thus simultaneous full-margin capture is necessary, not merely one branch
of a named topology argument.

## Repaired finite decision

The first nonvacuous twelve-good repair moves the external good `l` of
`E={e,l}` from base charity to `d`, moves `j` from base charity to `q`, and
leaves only `gr` unallocated. Required responses now import allocated support
and are not one-edge PI cycles.

The exact decision machinery now includes:

- all generalized self-PI exclusions;
- the analytic rank-three full-capture exclusions;
- 110 fixed-core-anchored exclusions;
- every closed two-owner core family (11,298 exact clauses); and
- lazy exact cuts for higher-order closed core families.

Both response forms admit initial models after the complete pairwise layer,
but every such model exposes many three-/four-owner closed core families.
After exact linearization of common safety and 14,249 distinct higher-order
family cuts, form R2 is UNSAT. An independent rebuild with a different seed
reproduces UNSAT and validates every cut; see
`ALLOCATED_E_FORM_R2_GENERALIZED_PI_EXCLUSION_THEOREM_20260813.md`. Form R3
reached a 30-round limit after 23,403 recorded cuts and remains unresolved.
A hash-validated flattening of the complete resume chain restored 23,847
distinct cuts (the earlier one-hop resume format had omitted older cuts),
and a controlled continuation reached its declared 20-round limit after
28,820 distinct cuts. It remained SAT at every round with fresh generalized-
PI families, so the bounded R3 cell is still unresolved—not a counterprofile
and not an UNSAT theorem. The complete chain is preserved in
`allocated_e_capture_form2_pairlinear_flattened_resume_v2.json`.

Complete self-/pair-PI-freeness does not force any of the four simplest
placements of residual `H` and charity `p`. An exact form-R3 profile defeats
all four, but has 3,233 higher-order closed core families and 197 unrestricted
three-/four-edge EFX escapes. This retires a fixed residual-placement proof
while strengthening the dynamic support-dependency interpretation; see
`ALLOCATED_E_FOUR_RESIDUAL_SELECTOR_REFUTATION_20260813.md`.

## Exact remaining gate

The universal theorem has the following sharper fork.

1. **Higher-order closure:** use the rank-three base-response cores and the
   ordinary `d->q` core to force a closed disjoint three-/four-core family,
   while separately converting or closing the current-only `d->r` wall.
   The exact characterization then gives generalized PI for the base-core
   branch and excludes the saturated state.
2. **Capture reversal:** construct a complete EFX allocation through at most
   four support edges from simultaneous full-margin capture, using a split of
   the contested selected cores plus donor compensation/charity; or produce a
   full-premise rational countermodel.

The payment geometry outside this fork is already closed: incoming response
cores strictly pay their recipients, the captured-support star pays `d`
within four edges, and full base-support closure pays every captured donor.
What remains is joint observer safety and compression of donor compensation
to four physical supplier-recipient pairs.

## Payment-hole compression update

Every near-perfect three-response matching gives a complete candidate on
three reversed response pairs plus one charity pair. A backward hole-pushing
operation trims outgoing cores and moves charity toward the unmatched target
without creating another edge. Every paid represented owner can be repaired
this way. The process therefore either gives an all-owner-paid four-edge
candidate or reaches `d` with one item-critical packet retained from a
minimal `d`-response core. That packet strictly captures `d`'s whole response
margin; see `BACKWARD_HOLE_PUSHING_D_CAPTURE_LEMMA_20260813.md`.

For the ordinary base-desired `d->q` core, minimality then leaves only two
scalar cases: complete core retention and a bare `d` deficit, or a proper
retained packet satisfying the strict two-floor band
`v_d(D)+v_d(Y_d)+chi<2F_d`; see
`MINIMAL_D_CORE_FULL_RETENTION_OR_TWO_FLOOR_POLARITY_LEMMA_20260813.md`.
The `d->r` strong-wall core may be only current-desired while `d` is below
base, so it cannot be inserted into base generalized PI. Its owner-payment
status was initially separate; the half-floor update below closes payment
without falsely promoting the core to a base response.

**Half-floor update.**  The owner-payment part of that mixed branch is now
closed cap-free.  If the ordinary `d->q` core `Q` is a singleton, it already
pays `d` above base.  Otherwise positivity and
`v_d(W)>=tau_d(Q)` force `v_d(W)>F_d/2`; the strong root wall forces
`tau_d(A)>v_d(W)>F_d/2`. Inside the packet obtained by deleting a least-`d`
good from `A`, choose a minimal current-safe core valued above `W`. Retaining
`W` and importing that unrestricted core strictly base-pays `d`; its full
value is at most every other observer's base floor. See
`HALF_FLOOR_CURRENT_WALL_LIFT_LEMMA_20260813.md`.  What remains mixed is not
payment of `d`, but observer-safe integration of the enlarged `d` target (or
the saturated decorated-response exit it triggers).

Splitting the root core sharpens that boundary. For every nonempty root
packet `C` already committed to another response source, its complement
`R=A-C` is full-value base-safe for every observer. Either `W+R` pays `d`, or
`C` has `d`-value strictly larger than
`v_d(A)+v_d(W)-F_d>2v_d(W)-F_d>0`. See
`HALF_FLOOR_ROOT_COMPLEMENT_OR_CAPTURE_LEMMA_20260813.md`. Thus every
nonsingleton mixed-wall survivor carries a positive quantitative capture,
not merely an unclassified current/base mismatch.

The two `d`-row capture inequalities alone do not contradict each other.
`DUAL_D_CAPTURE_SCALAR_COMPATIBILITY_NO_GO_20260813.md` gives an exact
rational scalar model realizing both simultaneously. Consequently the next
uncrossing step must use the retained packet's other-owner criticality,
observer safety, crossed support, generalized PI, or physical edge geometry;
another one-row inequality combination is a blocked route.

The current-wall terminal nevertheless has a second four-edge endpoint.
Move the root-retained packet `H` to `d` on the already active root-to-`d`
edge and retarget charity from `d` to root owner `r`. The new `d` bundle is
`W+D` and is paid. Either charity replaces `H` well enough to pay `r`, or
both `r` and `d` strictly rank `H` above charity. See
`CURRENT_WALL_CHARITY_RETARGET_OR_UNANIMOUS_CAPTURE_LEMMA_20260813.md`.
Thus the live current-wall payment separator is the explicit two-row
unanimous polarity, with observer safety and provenance closure still open.

The bounded R2 proof has also been mined from 14,249 higher-order cuts to a
stable 32-clause deletion-minimal layer and a categorized 92-assertion full
core. It needs no ordinary PI exclusion, rank-at-most-three formula, response
nonedge, or upper value bound. The decoded clauses form an alternating
closed-core uncrossing network; see
`ALLOCATED_E_R2_CORE_COMPRESSION_CHECKPOINT_20260813.md`.

## Evidence tier

- Generalized self-PI exclusion: cap-free proof plus independent exact audit.
- Closed disjoint-core characterization/capture: cap-free proof plus 40,824
  independent combinatorial records and QF-LRA margin audit.
- Repaired allocated-support cell: R2 exactly excluded and independently
  replayed; R3 unresolved under losslessly resumed higher-order refinement.
- Backward hole pushing/minimal-core polarity: cap-free conditional proofs
  plus exact graph/QF_LRA audits.  The current-only `d->r` owner-payment gap
  is closed by the half-floor lift; base-core uncrossing at `q` and observer
  safety of the enlarged `d` target remain open.
- Original four-edge theorem: open; no full-premise countermodel exists.

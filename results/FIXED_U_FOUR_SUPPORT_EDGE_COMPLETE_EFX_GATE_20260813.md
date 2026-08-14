# Fixed-U four-support-edge complete-EFX gate

**Date:** 2026-08-13

**Status:** exact target frozen; three edges are refuted, four-edge universality
is not yet proved; the former twelve-good residual decision cell is now
excluded by generalized self-PI and cannot serve as the universal frontier

## Frozen statement

Let `Y` be a saturated root-facing rank-three physical state in the fixed-`U`
recurrence, with four owner bundles and the singleton charity packet `{p}`.
For a complete allocation `Z`, put an edge `u -> i` when `Z_i` contains a
nonempty packet whose physical supplier in `Y` was `u`, where `u` is an owner
or charity and retained goods create no edge.

The target is:

> There is a complete EFX allocation `Z` whose distinct directed
> support-provenance packet-edge count is at most four.

Packet cardinalities and the number of goods in `Y` are unrestricted.  The
edge count is from the saturated physical support state, not from the older
GG base.  This distinction is necessary: the two provenance conventions give
different radii even in the canonical twelve-atom reconstruction.

The exact noncircular state data and saturation exclusions are frozen in
[`FIXED_U_RANK_THREE_FOUR_EDGE_PREMISE_LEDGER_20260813.md`](FIXED_U_RANK_THREE_FOUR_EDGE_PREMISE_LEDGER_20260813.md).
In particular, the twelve-atom response-rank gates are necessary proxies,
not the definition of a saturated state.

## Cap-free topology reduction

Completeness forces the singleton charity packet to move to one owner, using
one edge.  Hence every candidate within the target bound consists of

\[
  c\to b
\]

together with at most three directed owner-to-owner packet edges.  Each edge
may carry any nonempty subset of its supplier's physical bundle, and packets
on distinct outgoing edges are disjoint.  Conversely every such packet
system is a complete allocation with at most four support-provenance edges.

Thus the cap-free question is not a moved-good-radius statement.  It is an
arbitrary-subset feasibility theorem over a finite directed topology menu.
Owner paths, branching, and cycles must all be allowed.

Across the first seven exact adversarial profiles, 164 transfer topologies
occur and an exact set-cover calculation needs three topologies.  One profile
has no complete EFX realization on any of the 24 charity-rooted Hamiltonian
owner paths.  Therefore the tempting proof “donate the charity token and
follow one simple blocker path” is already false under the declared necessary
packet/rank premises.  A proof must either derive an additional saturation
inequality excluding that profile or allow branching, owner cycles, or a
disconnected compensating component.

There is nevertheless a useful cap-free reduction: every one of the seven
profiles has a completion in which each physical supplier has outdegree at
most one.  A minimum cover within this **functional packet** family still has
size three.  Hence the next analytic search may restrict each supplier to one
arbitrary packet without restricting packet cardinality, but it must retain
functional owner cycles, paths, and branching trees.  This is computational
evidence, not yet a universal restriction lemma.

A later frozen snapshot through iteration 21 contains 22 adversarial
profiles: three have minimum two edges, fourteen minimum three, and five
minimum four.  Every profile still has a functional completion.  The exact
minimum functional cover has grown to four topologies—one Hamiltonian path,
one connected branching tree, and two disconnected owner-cycle forms.  This
strengthens the functional-packet signal while simultaneously showing that
the path-only hypothesis is not an adequate relaxation.

The functional search was stopped at its next clean checkpoint, through
iteration 25.  Its 26 exact profiles consist of one minimum-two, fifteen
minimum-three, and ten minimum-four cases.  Every profile again has a
functional completion, but the minimum exact topology cover has grown to
five and the Hamiltonian-path family still fails to cover the profiles.
This frozen evidence is recorded in
[`fixed_u_four_edge_topology_cover_analysis_functional_round25.json`](fixed_u_four_edge_topology_cover_analysis_functional_round25.json).
That run was frozen at a clean checkpoint.  The later refutation of every
fixed response-derived topology menu has revived functionality as the live
stronger conjecture: proving it would imply the actual gate, while a
functional counterprofile would still leave nonfunctional four-edge closure
available.

## Exact sharpness

The independently audited iteration 1 of
[`fixed_u_rank_three_root_facing_support_edge_cegar.json`](fixed_u_rank_three_root_facing_support_edge_cegar.json)
has no complete EFX allocation using zero through three edges and has exactly
33 using four.  Those witnesses occupy 16 directed graphs; some are connected
five-vertex components, some contain owner two-cycles, and some are
disconnected.  See
[`FIXED_U_SUPPORT_EDGE_THREE_NO_GO_20260813.md`](FIXED_U_SUPPORT_EDGE_THREE_NO_GO_20260813.md).

Therefore a proof cannot be reduced to a charity-rooted tree, a bilateral
swap, or a three-edge repair.

## Candidate saturated-walk proof and its exact missing implication

The natural proof starts by donating `{p}` to a blocker and follows unsafe
owner targets with deletion-minimal response packets.  Full signed source
margins are intended to preserve payment, while common safety preserves
observer EFX.  At a saturated state, a genuinely new response, strict support
growth, same-record utility progress, or rank augmentation is unavailable;
a repeated internally released owner walk is intended to be PI.  With four
owners, a simple walk after `c -> b` uses at most three owner edges.

The load-bearing implication is not yet established:

> After each blocker repair, one can choose a single packet from the unsafe
> target so that the receiving blocker becomes safe and paid, the donating
> source remains paid, all earlier repaired comparisons remain safe, and no
> physical supplier must send to a second new recipient—unless one of the
> exact saturated exits occurs.

The existing singleton-charity exchange walk does **not** prove this.  It
parks a replacement owner good in charity and ends with nonempty charity;
quietly dropping that replacement would amount to solving the present gate.
Likewise, graph saturation alone does not supply the payment and observer
inequalities.  This implication must be proved from the signed packet margins
or refuted by a full-premise positive rational state.

A second tempting shortcut is also false.  Iteration 6 has the ordinary
common-safe response cycle

\[
 q\to r:\{a_1,h\},\qquad
 s\to q:Q,\qquad
 r\to s:E.
\]

Rotating these cores and returning the root residual `a0` to `r` leaves
`d` at `v_d(W)=319/410<1`; moreover `d` and `s` still have walls against the
resulting root target, with thresholds `863/615` and `481/246` respectively.
Thus a bare cycle in the subset-response relation is not a full
release-compatible PI certificate.  It cannot be excluded without the exact
signed residual/payment labels demanded by the saturated statement.

### Corrected rank-three response interface

The abstract five-target rank-three census cannot be inserted directly here.
Every one of its three minimum connected forms requires a desired response
into charity.  At a paid state whose singleton charity token is base-safe,
that response is impossible.  The earlier response-reversal construction is
therefore only an abstract conditional graph lemma, not the physical normal
form of this gate.

After excluding charity as a response target, the permanent anchor, the
recurrent unmatched edge `d -> q`, the mandatory strong-wall response
`d -> r`, and any rank-three owner matching give five nonself response edges
and force a directed owner cycle of length two or three. This cap-free graph
theorem is
[`PAID_SINGLETON_CHARITY_RANK_THREE_OWNER_CYCLE_LEMMA_20260813.md`](PAID_SINGLETON_CHARITY_RANK_THREE_OWNER_CYCLE_LEMMA_20260813.md).
The physical obstruction is now release compatibility of that short cycle,
followed by allocation of the singleton charity within the four-edge budget.

The five-edge relation itself has only two live forms. One of the four graph
forms is rank four, and another is impossible because the q-budget makes
`q -> d` force `q -> r`. The two survivors are a paid `r <-> q` cycle or a
paid `r -> q -> s -> r` cycle, while sacrificed `d` responds into both `r`
and `q`; see
[`EXACT_RANK_THREE_FIVE_RESPONSE_CLASSIFICATION_LEMMA_20260813.md`](EXACT_RANK_THREE_FIVE_RESPONSE_CLASSIFICATION_LEMMA_20260813.md).

Complete ordinary PI-freeness strengthens both forms. The whole owner cycle
cannot consist of ordinary base responses, so at least one cycle edge is
genuinely current-only. Reversing that edge pays its receiving owner strictly
above current utility even if she releases her entire current bundle; see
[`PI_FREE_RANK_THREE_CYCLE_CURRENT_EDGE_LEMMA_20260813.md`](PI_FREE_RANK_THREE_CYCLE_CURRENT_EDGE_LEMMA_20260813.md).
In fact every ordinary or current incoming response core strictly base-pays
its recipient. Only an owner with no incoming response—such as the sacrificed
owner or a path endpoint—can carry a payment deficit.

Each survivor contains two Hamiltonian owner response paths. Reversing one
and donating the charity token to its endpoint yields a complete allocation
on exactly four support edges. Three owners are automatically paid; the only
possible payment failure is the chosen endpoint's strict incoming-core
capture inequality. The endpoint choices are `{q,r}` or `{s,r}` in the two
forms; see
[`TWO_SURVIVOR_HAMILTONIAN_CHARITY_PATH_SELECTOR_LEMMA_20260813.md`](TWO_SURVIVOR_HAMILTONIAN_CHARITY_PATH_SELECTOR_LEMMA_20260813.md).

The two-cycle form has an additional branching completion: rotate the
`r <-> q` cores, give `d` a disjoint core from either target, and give charity
to `s`. This pays all four owners through exactly four edges. Its only
physical survivor is simultaneous full-margin overlap capture at both `r`
and `q`; see
[`TWO_CYCLE_BRANCHING_CHARITY_COMPLETION_LEMMA_20260813.md`](TWO_CYCLE_BRANCHING_CHARITY_COMPLETION_LEMMA_20260813.md).

The three-cycle form has six analogous branches: choose d's target in
`{r,q}`, omit one paid-cycle response, reverse the other two, and donate
charity to the omitted source. Two branches need no shared-target
disjointness; all pay three owners automatically. The exact residual is six
endpoint capture/observer inequalities; see
[`THREE_CYCLE_SIX_BRANCH_CHARITY_COMPLETION_LEMMA_20260813.md`](THREE_CYCLE_SIX_BRANCH_CHARITY_COMPLETION_LEMMA_20260813.md).

Finally, rotating the complete paid cycle and donating charity to `d` gives
one more four-edge endpoint in each form. All other owners are paid. In the
three-cycle case its only payment failure is exactly
`v_d(W)+v_d(p)<v_d(X_d)`; see
[`FULL_CYCLE_CHARITY_TO_SACRIFICED_COMPLETION_LEMMA_20260813.md`](FULL_CYCLE_CHARITY_TO_SACRIFICED_COMPLETION_LEMMA_20260813.md).

The first decision pass appeared to refute this selector. Exact
positive-rational profiles in both surviving response forms defeated the
union of every Hamiltonian-path, branching, and full-cycle topology above
while still admitting unrestricted complete EFX allocations on at most four
edges. See
[`TWO_SURVIVOR_NAMED_TOPOLOGY_SELECTOR_REFUTATION_20260813.md`](TWO_SURVIVOR_NAMED_TOPOLOGY_SELECTOR_REFUTATION_20260813.md).
That pass omitted generalized self-PI and is superseded as evidence about a
saturated state.

The refutation survives complete **ordinary PI-freeness**. Exact rational
profiles in both response forms have no ordinary common-safe desired-response
cycle and still defeat every named response-derived topology, while admitting
13 and 23 unrestricted four-edge EFX allocations respectively. Their simplest
escapes are reciprocal `r`--`d` support reassemblies rather than response
reversals; see
[`ORDINARY_PI_FREE_NAMED_TOPOLOGY_REFUTATION_20260813.md`](ORDINARY_PI_FREE_NAMED_TOPOLOGY_REFUTATION_20260813.md).

It does **not** survive the full generalized PI premise. Every displayed
counterprofile contains a one-edge generalized self-PI cycle. More strongly,
the declared master requires the common-safe desired core `E={e,l}` for `s`,
while `X_s={e,p}` and `l` is base charity. This is exactly the self-edge
`s -- {l}|{p} --> s`. A deletion-minimal core extraction shows that excluding
this single edge alone makes both response forms UNSAT; no ordinary PI
constraint is needed. See
[`GENERALIZED_SELF_PI_EXCLUSION_LEMMA_20260813.md`](GENERALIZED_SELF_PI_EXCLUSION_LEMMA_20260813.md)
and `generalized_pi_selector_form{0,2}_core.json`.

Accordingly the old twelve-good residual cell is empty in the saturated
domain. This is not a bounded proof of the frozen theorem: the cap-free state
may have a represented common-safe core that imports another owner's allocated
support rather than only replacing own support by charity. The live gate is
the release-dependency closure of those genuinely nonself imports.

Once a two- or three-owner cycle is release-compatible, every complete
allocation obtainable by sending an arbitrary residual subpacket along each
existing cycle edge and donating the singleton charity uses only three or
four edges. Every cycle owner is automatically paid by its incoming desired
core. Conditional on using this residual selector, the remaining condition
is observer safety; the selector is not exhaustive. See
[`RANK_THREE_CYCLE_RESIDUAL_CHARITY_NORMAL_FORM_LEMMA_20260813.md`](RANK_THREE_CYCLE_RESIDUAL_CHARITY_NORMAL_FORM_LEMMA_20260813.md).

On the displayed four-response subrelation, one can omit one owner response
and replace it by the charity donation. The other three responses reverse
along three owner edges. But the exact relation has the fifth mandatory
`d -> r` edge, so this is only a conditional selector, not the full normal
form. See
[`RANK_THREE_ONE_EDGE_CHARITY_SUBSTITUTION_LEMMA_20260813.md`](RANK_THREE_ONE_EDGE_CHARITY_SUBSTITUTION_LEMMA_20260813.md).

That response-core substitution is not the universal selector. A corrected
positive-rational profile has zero EFX candidates across the whole family,
yet exactly twenty unrestricted four-edge EFX allocations on eleven other
topologies. See
[`ONE_EDGE_CHARITY_SUBSTITUTION_BOUNDARY_20260813.md`](ONE_EDGE_CHARITY_SUBSTITUTION_BOUNDARY_20260813.md).
The theorem must therefore exploit arbitrary four-edge packet graphs and the
full signed margins; response edges cannot simply be identified with final
transfer edges.

The overlap itself has a cap-free dichotomy. Trimming one response core by
already selected support either leaves a disjoint common-safe desired core,
or the intersection captures that source's entire strict response margin. See
[`SHARED_TARGET_DOUBLE_RESPONSE_DISJOINT_OR_CAPTURE_LEMMA_20260813.md`](SHARED_TARGET_DOUBLE_RESPONSE_DISJOINT_OR_CAPTURE_LEMMA_20260813.md).
On the corrected owner cycle this is the exact release-compatibility survivor.

For any valid response reversal, the exact owner margin is
`m_i = Delta_i - L_i + I_i`. Any base- or current-desired incoming core pays
its owner automatically even after that owner releases an arbitrary
subpacket of its current bundle. Therefore every owner on a complete response
cycle is strictly base-paid; the only quantitative survivor for such owners
is the observer condition `m_i >= max_j b_ij`. See
[`RANK_THREE_FOUR_EDGE_SIGNED_MARGIN_IDENTITY_LEMMA_20260813.md`](RANK_THREE_FOUR_EDGE_SIGNED_MARGIN_IDENTITY_LEMMA_20260813.md).

## Flexible-topology pivot

Across the 25 profiles in the frozen corrected exact-response CEGAR census,
there are 215 feasible transfer topologies.  No selection of charity-rooted
Hamiltonian paths covers all profiles.  In contrast, four functional
topologies cover the entire observed set.  This is descriptive bounded
evidence, not a theorem; the exact census is
[`fixed_u_exact_owner_cycle_relation_topology_cover_round24.json`](fixed_u_exact_owner_cycle_relation_topology_cover_round24.json).

The next computational gate therefore blocks whole arbitrary-packet topology
families rather than individual allocations.  A SAT refinement supplies a
new topology outside the current menu; UNSAT would prove the bounded
twelve-atom four-edge theorem.  Analytically, the target is now a signed-
margin selector over flexible functional paths/cycles, not a response-path
endpoint lemma.

The initial four-topology cover is itself not universal.  In the exact `R3`
cell, a rational profile defeats all 1,465 allocations supported by that
menu but has 58 unrestricted four-edge EFX allocations, including three-edge
witnesses.  The exact replay is
[`exact_response_functional_cover_form2_audit.json`](exact_response_functional_cover_form2_audit.json).
The corresponding `R2` decision returned `unknown (timeout)`, so no claim is
made there.  Topology-level CEGAR now enlarges the menu only with maximal
functional four-edge witnesses; the fixed four-topology menu is retired.

The response classification nevertheless supplies a better *payment*
skeleton than the earlier Hamiltonian construction.  Start at sacrificed
`d`, follow only the shortest response path needed to repair it, reverse
that path, and give charity to its endpoint.  This uses three functional
edges in `R2` and four in `R3`, preserves every off-path paid owner, and
leaves only one endpoint payment inequality.  See
[`SACRIFICED_SOURCE_SHORTEST_CHARITY_PATH_LEMMA_20260813.md`](SACRIFICED_SOURCE_SHORTEST_CHARITY_PATH_LEMMA_20260813.md).
If paid, any observer failure becomes a complete decorated current response;
the live analytic gate is exact repeated-component extraction or reversal of
simultaneous endpoint capture.

There is also a common paid-cycle candidate: rotate only the paid response
cycle and give charity to `d`.  It uses three edges in `R2` and four in `R3`;
all represented owners are paid, and the only possible payment failure is
the bare deficit `v_d(W)+v_d(p)<v_d(X_d)`.  See
[`PAID_CYCLE_CHARITY_TO_SACRIFICED_LEMMA_20260813.md`](PAID_CYCLE_CHARITY_TO_SACRIFICED_LEMMA_20260813.md).
The two shortest paths plus this paid cycle reduce each response form to
three explicit functional payment candidates before decorated-response
closure.

In the declared twelve-atom cell, the payment decision has an even smaller
UNSAT core.  The model hard-codes both positive `q0=Q\K` and the provenance
identity `X_d=H+(K-J)+G_q`.  Then `d(K+H)>d(X_d)` gives `d(J)>d(G_q)`, while
`d(W)>=tau_d(Q)>=d(K)`; consequently `W+H` strictly pays `d`.  Moving only
`H` to `d` and charity to `s` strictly pays all four owners on two edges.
See
[`ROOT_FACING_TWO_EDGE_STRICT_PAYMENT_COMPLETION_LEMMA_20260813.md`](ROOT_FACING_TWO_EDGE_STRICT_PAYMENT_COMPLETION_LEMMA_20260813.md).
This is exact only under those two structural hypotheses.  The general GG
premises neither align `K-J` with old `d`-support nor exclude `K=Q`.
Arbitrary captured-own-support return—not observer safety alone—is therefore
the current universal payment gate.

Its support geometry is now cap-free. Returning every base-`d` good from
each represented current supplier to `d`, and sending all charity to `d`,
uses at most four edges and strictly pays `d`; see
[`CAPTURED_OWN_SUPPORT_FOUR_EDGE_STAR_LEMMA_20260813.md`](CAPTURED_OWN_SUPPORT_FOUR_EDGE_STAR_LEMMA_20260813.md).
For donor `i`, the exact final margin is
`Delta_i-v_i(Y_i cap X_d)`. Hence the universal gate has narrowed to
simultaneous donor captured-margin inequalities and the decorated observer
response they generate.

The cap-free surplus-star selector makes this simultaneous failure exact: it
is a separable three-knapsack certificate, not a missing graph topology. A
failed star forces at least one captured donor margin; see
[`FOUR_EDGE_SURPLUS_STAR_SELECTOR_LEMMA_20260813.md`](FOUR_EDGE_SURPLUS_STAR_SELECTOR_LEMMA_20260813.md).

Captured donor payment can now be removed globally. Take the least owner set
closed under displaced base-support holdings, starting at `d`, and return all
of that component's base support simultaneously. Every closure owner is paid
exactly; see
[`BASE_SUPPORT_CLOSURE_PAID_COMPONENT_LEMMA_20260813.md`](BASE_SUPPORT_CLOSURE_PAID_COMPONENT_LEMMA_20260813.md).
An attempted strengthening from an external charity token to a two-bare
PI-free separator is invalid: minimality for a strict owner does not imply
common safety for every observer. Therefore the repaired full-capture cell
is not analytically excluded; see the correction in
[`EXTERNAL_TOKEN_TWO_BARE_CLOSURE_SEPARATOR_LEMMA_20260813.md`](EXTERNAL_TOKEN_TWO_BARE_CLOSURE_SEPARATOR_LEMMA_20260813.md).

The live gate is consequently no longer donor payment in the old
twelve-atom provenance cell. It is cap-free response compression of a paid,
connected support closure: saturation must force common-safe full response
rank, strict owner/support progress, PI, or a four-edge complete EFX shortcut.
Every response into a reassembled closure target is either an old ordinary
base response or uses externally supplied support and attaches charity/an
outside owner; see
[`CLOSED_BASE_SUPPORT_RESPONSE_OLD_OR_GROWTH_LEMMA_20260813.md`](CLOSED_BASE_SUPPORT_RESPONSE_OLD_OR_GROWTH_LEMMA_20260813.md).
Thus the final analytic survivor is a repeated labeled Hall defect after all
external component attachments have saturated; already-internalized external
response edges remain part of the record.

## Current exact decisions

Three complementary decisions are running or frozen:

1. adaptive exact CEGAR, which stops immediately if a profile has no complete
   EFX allocation or has minimum support-edge count at least five; and
2. a direct conjunction of the negations of all 116,596 complete allocations
   using at most four edges in the canonical twelve-atom cell; and
3. topology-level CEGAR, which adds every arbitrary-packet allocation
   supported by a selected transfer graph in one refinement.

The first one-hour direct run returned `unknown (timeout)`.  It is retained
as a computational boundary only, not as positive or negative evidence.  A
second encoding removes 23,116 impossible empty-owner allocations.  Separate
30-minute exact decisions for `R2` and `R3` both also returned `unknown
(timeout)` after blocking all 93,480 remaining allocations.  These are honest
computational boundaries, not evidence for either verdict. The narrower
functional decisions blocked 76,692 allocations in each form and likewise
returned `unknown (timeout)`. They are retained as honest boundaries, not the
current analytic gate; see
[`PAID_FUNCTIONAL_FOUR_EDGE_SELECTOR_REDUCTION_20260813.md`](PAID_FUNCTIONAL_FOUR_EDGE_SELECTOR_REDUCTION_20260813.md).

An UNSAT result proves only the declared atomization, but supplies a finite
allocation core from which to seek the missing inequality.  A SAT result is
only a necessary-premise countermodel until full response saturation and
signed recurrence reachability are independently checked.

## Exact claim boundary

The four-edge theorem, its cap-free lift, and the fixed-`U` recurrence remain
open.  The durable result at this checkpoint is the exact support-provenance
definition, the cap-free topology reduction, and the independently verified
sharpness of four edges in the canonical cell.

# Three-nonsingleton contraction target

**Date:** 2026-08-09

**Status:** active general-EFX gate; the eight selected-cycle classes are
now exhaustive and the length-two class is reduced to a three-packet flower

## Target theorem

Let `X` be a globally lexicographically maximal noncomplete partial EFX
allocation for four positive, nondegenerate additive agents in the BCFF
one-charity normal form. Suppose exactly three allocated bundles are
nonsingletons.

Prove that the selected basic-cycle structure yields at least one of:

1. a complete EFX allocation;
2. a partial EFX allocation with strictly larger fixed-order lexicographic
   potential, preferably one with at most two nonsingleton bundles.

The first outcome proves existence for the instance, the second contradicts
global maximality. There is no separate equal-potential contraction outcome:
nondegeneracy makes every agent's bundle utility injective, so equality of
the full ordered utility vector forces every assigned bundle to remain the
same and cannot reduce the number of nonsingletons.

## Why this is the highest-leverage next gate

The exactly-two branch is now closed. The exactly-three branch is the
smallest state class not covered by that theorem and retains one singleton
anchor, so it is structurally closer to the successful reservoir arguments
than the all-four-nonsingleton branch. Its key task is not another fixed
priority table: it is to manufacture a second singleton, or to identify the
precise obstruction preventing that contraction.

## Required proof program

1. Select one incoming basic champion or parallel envy edge per bundle and
   classify simple cycles by the number and placement of genuine champion
   edges, allowing all extra graph edges.
2. For every surviving class, attempt a cap-free `top/bottom` rotation that
   empties one large owner's residual bundle while preserving EFX.
3. Route every failed rotation through an explicit generalized PI cycle or a
   strict lexicographic improvement. Do not assume chordlessness, unique
   champion decompositions, bounded packet sizes, or a fixed item cap.
4. Use exact arithmetic or SMT only to enumerate symbolic inequality cells,
   falsify candidate lemmas, and extract small cores. The final theorem must
   be an arbitrary-packet analytic argument with replayable audits.
5. Audit every BCFF interface directly against the published definitions,
   especially generalized-edge release sets and the treatment of internal
   bottom edges.

## First bounded milestone

The first milestone is complete. The exact census has eight directed classes,
and none is a direct instance of an exactly-two-nonsingleton theorem. The
length-two `GG` class now reduces cap-free to a three-packet flower: the
external large owner has no incoming ordinary envy edge and therefore has a
nonself genuine incoming `f`-champion arm. See
[`THREE_NONSINGLETON_CYCLE_CENSUS_AND_FLOWER_REDUCTION_20260809.md`](THREE_NONSINGLETON_CYCLE_CENSUS_AND_FLOWER_REDUCTION_20260809.md).

The length-two flower is now further reduced by an exhaustive common-safe
cover theorem. All 864 source/priority cells have either a direct improving
cover or a cover with one unpaid mutual-cycle owner placed after a strict
improver. A four-cover strict-cycle lemma closes another 148 cells, leaving
284 cells in which simultaneous failure is consistent only in the relaxed
independent-total/tail abstraction. A true-tail atomic audit reduces this to
116 bounded cells but supplies an exact two-good exchange witness after all
one-good transfers are blocked. This rules out continuing by fixed radius.
The second alternative has now occurred. An exact full-`X_q` model blocks
every priority-directed one- and two-good exchange, including a source-safe
improving bottom swap, while its nearest improving EFX allocation is a
three-good connected owner/charity multigraph. Moreover, the external swap-blocker edge need
not have its incoming good released by the apparent flower cycle. See
[`FULL_CAPTURE_SWAP_PI_GATE_REFUTATION_20260810.md`](FULL_CAPTURE_SWAP_PI_GATE_REFUTATION_20260810.md).

The next research output must therefore be a cap-free component-growth
lemma: follow the unsupplied incoming good of each blocker through successive
owners until the component yields a lex-improving EFX allocation, a
release-compatible PI edge set, or an impossible strict item-order cycle.
The component must be a slot multigraph and may involve charity: blocking
all simple three-good owner paths still leaves an exact model whose nearest
partial escape is a three-edge `q--charity` packet replacement.

The variable-charity hybrid-wall theorem now removes the cardinality
restriction, and the packet-for-charity replacement lemma supplies the exact
opposite-sign obstruction rule for a component incident to charity. The
remaining construction premise is to select the first improving packet or
exchange component from the flower data; once a feasible endpoint is named,
the distinguished lex-component corollary grows to it in finitely many slot
components.

An exact strengthening now blocks every one-recipient packet-for-charity
replacement as well. Its nearest partial and complete escapes are three-edge
hub-splitting components: one owner receives one good (or `f`) while sending
two goods to two distinct recipients. The selector must therefore range over
packet partitions at a hub, not just subsets sent to charity.

The charity-rooted hub-split obstruction lemma now classifies every failure
of such a split cap-free. A failed hub target supplies an incoming subset of
`{f}` while releasing the whole hub packet; every failed leaf target supplies
its disjoint packet cell as an incoming set. Directed wall cycles are
therefore release-compatible PI edge sets. The exact remaining selector gate
is to choose the hub and partition so that an open wall source or a strict
Hall-deficient target set cannot persist under component growth.

The canonical star as a direct EFX endpoint is now exactly refuted as well. A
bounded full-capture cell survives after every improving two-leaf split from
arm owner `c` is blocked. But exact most-envious-source enumeration finds two
PI response matchings among its six arm-owner splits, plus two open and two
Hall-deficient cases. Thus the corrected EFX-or-response-Hall selector
survives; only its unmatched cases require component growth. The nearest
complete EFX endpoint is a five-good component on `q,c,s,charity`.

A stronger exact gate now forbids both EFX arm-owner splits and internal
arm-owner response matchings. It remains SAT by making every two-leaf split
from `c` ineligible. The same model has an outright EFX split from mutual-
cycle owner `q`. Hence the next selector must range across all nonsingleton
hubs and prove a cross-owner eligibility dichotomy; flower championship does
not privilege `c` in its own valuation row.

That endpoint-selection gate is now closed in a simpler form.  In every hard
packet-minimum flower cell, the later owner on the mutual `r,q` champion
cycle values `f` above at least one good of her current bundle.  Replacing
that good by `f` is therefore an improving singleton packet-for-charity
operation.  The analytic proof uses three lex-valid common-safe covers; an
exact arbitrary-packet audit checks all 1,020 surviving source/support/order
cells, with the later owner individually forced in every cell.  See
[`FLOWER_LATER_OWNER_SINGLE_REPLACEMENT_SELECTOR_LEMMA_20260810.md`](FLOWER_LATER_OWNER_SINGLE_REPLACEMENT_SELECTOR_LEMMA_20260810.md).

The live flower gate is no longer selection of a first packet.  It is the
termination of the dependency exposed by the packet-for-charity obstruction
lemma: an EFX replacement closes immediately, a target wall supplies a
generalized `({f}|{g})` edge into the later mutual owner, and a charity wall
has the opposite strict polarity.  Exact adversarial profiles realize only
the open-source response branch after all one-leaf completions are tested,
so the next theorem must grow that released-good dependency to an EFX
allocation or a release-compatible PI edge set.

The charity-wall branch is now absorbed into that same response component.
If an owner envies the released packet `R`, then `R subseteq X_q` is
automatically common-safe and that owner strictly desires it.  Her
self-absorption edge consumes exactly what the replacement edge releases.
If `q` sources the replacement target the pair is PI; otherwise a PI-free
survivor exposes a new owner or a two-target Hall defect missing `q`.  See
[`PACKET_REPLACEMENT_CHARITY_ABSORPTION_LEMMA_20260810.md`](PACKET_REPLACEMENT_CHARITY_ABSORPTION_LEMMA_20260810.md).

The target-wall branch also has a cap-free full-complement return.  Every
external desired response to `X_q-R+f` must retain `f`, so it is `K+f` and
releases exactly `X_q\K`.  Giving that whole release with `X_a` back to the
source closes a PI two-cycle whenever `q` responds.  A PI-free survivor must
instead satisfy the strict core-capture interval
`q(X_a)<q(K)<q(X_q)-q(f)`, or expose another named Hall source.  See
[`PACKET_REPLACEMENT_COMPLEMENT_RETURN_LEMMA_20260810.md`](PACKET_REPLACEMENT_COMPLEMENT_RETURN_LEMMA_20260810.md).
The other mutual owner `r` cannot satisfy this interval, because
`q(T_r+f)>q(X_q)` and positivity imply
`q(X_r)>q(X_q)-q(f)`.  Thus only `c,s` remain as terminal sources.
For either external survivor, `T_r` always contains a minimal packet paying
`q`'s capture deficit.  The canonical root flip gives `K+f` to the source,
the released complement plus `X_a` and that packet to `q`, and compensates
`r` from a disjoint part of `X_q\K`.  Its internal response SDR is PI.  The
live selector is now the two-row compensation system (13) in the cited
lemma, rather than existence of a first payment packet.

A value-maximal choice among **all** eligible replacement packets supplies
a further cap-free invariant. Writing `sigma=q(f)-q(R)`, every nonempty
packet left in `X_q-R` crosses that slack, and every improving exchange from
the selected side to the residual side jumps by more than `sigma`. Thus a
surviving core capture leaves a nonempty threshold-crossing pivot and the
replacement cannot drift through a sequence of smaller positive gains.
This is a global frontier potential, not the refuted fixed-bundle endpoint;
the live task is to prove that external-owner augmentation increases the
component before this frontier can fall, or to extract the resulting strict
item-order cycle. See
[`MAXIMAL_REPLACEMENT_FRONTIER_EXCHANGE_LEMMA_20260810.md`](MAXIMAL_REPLACEMENT_FRONTIER_EXCHANGE_LEMMA_20260810.md).

Testing the whole payment reservoir against the whole released complement
also turns root-flip failure into a signed dichotomy. Unless the aggregate
flip already closes, either `r(T_r)>r(X_q-K)` or
`q(X_q-K)>q(f)>q(X_a)`. Thus the remaining augmentation no longer begins
from an unstructured two-row subset-sum failure: it begins from one of two
explicit root/external polarities. See
[`PACKET_REPLACEMENT_AGGREGATE_ROOT_FLIP_POLARITY_LEMMA_20260810.md`](PACKET_REPLACEMENT_AGGREGATE_ROOT_FLIP_POLARITY_LEMMA_20260810.md).

The full two-row selector now has a cap-free adaptive implementation. Grow
a minimal `q`-payment packet in `T_r` and a minimal `r`-compensation packet
in `X_q-K` only when the opposite inequality breaks. Each repair strictly
enlarges one packet, so the finite repair tree terminates. A successful leaf
is the canonical root flip; an exhausted leaf carries either a payment-
critical root wall or the strict external order
`q(X_q-K)>q(f)>q(X_a)`. See
[`ALTERNATING_PAYMENT_COMPENSATION_CHAIN_LEMMA_20260810.md`](ALTERNATING_PAYMENT_COMPENSATION_CHAIN_LEMMA_20260810.md).

The required multi-owner continuation now has a single cap-free support
theorem. Orient any packet-transfer tree away from the owner receiving `f`.
Every child packet is released by its parent target, so any internal
response SDR is PI; an EFX endpoint closes directly, and every other state
names an open source or minimal Hall defect. This covers the observed
depth-two escapes `r -> {q,c}, c -> s` and `q -> c -> s` without a move-
radius assumption. See
[`CHARITY_ROOTED_TRANSFER_TREE_RESPONSE_HALL_LEMMA_20260810.md`](CHARITY_ROOTED_TRANSFER_TREE_RESPONSE_HALL_LEMMA_20260810.md).

The Q-exhausted leaf now canonically changes the root. Writing
`E=(X_q-K)-H`, exhaustion forces `q(f)>q(E)+q(X_a)`. Therefore `q` can
replace `E` by `f` and transfer `E` to `a`, keeping `r` fixed and improving
`q`. This is a complete one-edge transfer tree; it either closes directly,
closes through PI, or exposes the next owner/Hall boundary. See
[`Q_EXHAUSTION_ROOT_SWITCH_LEMMA_20260810.md`](Q_EXHAUSTION_ROOT_SWITCH_LEMMA_20260810.md).

The responder's released old bundle is now part of the compensation
reservoir as well. Alternating minimal repairs over
`(X_q-K)+X_a` either close, root-switch on Q-exhaustion, or force the single
strong wall `r((X_q-K)+X_a)<r(P)`. See
[`RELEASED_OWNER_COMPENSATION_CHAIN_LEMMA_20260810.md`](RELEASED_OWNER_COMPENSATION_CHAIN_LEMMA_20260810.md).

When a root-switch leaf exposes a new source `b`, rotate its desired subset
to `b` and the unused offer plus `X_b` back to the old leaf. This either
strictly grows the represented-owner set or forces an exact old-leaf capture
wall, with release-compatible response support in the growth branch. On the
hardened profile the sequence is `{q,s}->{q,c,s}` and then exposes `r`.
See
[`OPEN_LEAF_SOURCE_ROTATION_LEMMA_20260810.md`](OPEN_LEAF_SOURCE_ROTATION_LEMMA_20260810.md).

This source rotation now iterates. At each open-source step, either the old
sink remains improved and the represented owner set grows, or it captures
the desired subset above the new source bundle plus the sink's whole prior
improvement margin. Successful steps preserve disjoint/internal release
support. The hardened Q-wall grows through all four owners and then closes
by the exact PI matching `q<-s,c<-c,r<-r,s<-q`. The universal residual is
therefore the strict sink-capture branch or an all-owner Hall defect, not the
previous bounded adversary. See
[`OUTSIDE_SOURCE_SINK_AUGMENTATION_LEMMA_20260810.md`](OUTSIDE_SOURCE_SINK_AUGMENTATION_LEMMA_20260810.md)
and
[`hardened_q_wall_sink_augmentation_pi_audit.json`](hardened_q_wall_sink_augmentation_pi_audit.json).

The full-reservoir R-wall is possible only for a top-capturing response.
Writing `K_T=K intersect T_q` and `K_B=K intersect B_q`, the wall forces
`r(K_T)>r(B_q-K_B)+r(X_a)`. In particular every bottom-only response core
closes through compensation or root-switch/component growth. The residual
root/order selector need address only this sharply oriented top-core branch.
See
[`FULL_RESERVOIR_R_WALL_TOP_CAPTURE_LEMMA_20260810.md`](FULL_RESERVOIR_R_WALL_TOP_CAPTURE_LEMMA_20260810.md).

For that top core, transfer `K_T` to `r`, give `f` to `q`, and return a
minimal packet `P' subseteq T_r` with `q(P')+q(f)>q(K_T)`. This closes unless
the strict critical order
`r(P')>r(K_T)>r(B_q-K_B)+r(X_a)` holds. Hence the remaining R-side selector
is an explicit reverse-order exchange cell with deletion-critical `P'`.
See
[`TOP_CORE_ROOT_EXCHANGE_LEMMA_20260810.md`](TOP_CORE_ROOT_EXCHANGE_LEMMA_20260810.md).

Two natural ways of freezing the selected operation are now exactly refuted.
Neither fixing the selected singleton replacement nor first enlarging it to
an inclusion-maximal packet below `f` guarantees an EFX completion that keeps
the earlier mutual owner nonworse. Each countermodel nevertheless has a
two-good EFX lex escape that fixes the earlier owner and improves the later
owner. Thus dependency termination must allow the distinguished owner's
bundle itself to evolve. The corrected bounded target is existence of any
EFX completion that keeps the earlier mutual owner weakly nonworse and makes
the later mutual owner strictly better; the cap-free proof target remains an
adaptive component construction. See
[`FIXED_REPLACEMENT_LEX_COMPLETION_REFUTATIONS_20260810.md`](FIXED_REPLACEMENT_LEX_COMPLETION_REFUTATIONS_20260810.md).

The first cap-free flexible-completion subcase is now closed.  If the
external `(B_q|B_r)` desired bundle captures all of both `B_q` and `T_r`,
two allocations suffice: either `q` replaces `B_q` by `f`, or `r` receives
`T_q+f` while `q` receives `T_r+B_q`.  Failure of the first operation forces
the payment inequality needed by the second.  This is an arbitrary-packet
theorem mined from a deletion-minimal two-allocation QF_LRA core.  See
[`FLOWER_DUAL_FULL_CAPTURE_ESCAPE_LEMMA_20260810.md`](FLOWER_DUAL_FULL_CAPTURE_ESCAPE_LEMMA_20260810.md).

Consequently the flexible `GG` gate now requires a nonempty residual top
packet `J=T_r\(A_r\cap T_r)`.  The dual rotation localizes every remaining EFX failure
to strong envy of `A_r+J`.  The associated generalized edge may discard all
of `J` and reproduce the original bottom edge, so retained-top cardinality
is not yet a monotone potential.  The next theorem must force residual
retention/recapture, maintain a Hall-augmentable family of alternative
desired bundles, or exactly refute all such adaptive operations.

Three additional cap-free rotations now force every such residual state
into one aggregate polarity cell.  The earlier mutual owner ranks `f` above
the later owner's bottom `B_q`, while the later owner ranks `B_q` above `f`,
`T_r` above `T_q`, and `B_q` above `B_r`.  Any failure of one of these signs
is already the required flexible EFX escape.  Thus residual recapture may
assume this opposite-sign orientation rather than handling arbitrary owner
rows.  See
[`FLOWER_THREE_ROTATION_POLARITY_LEMMA_20260810.md`](FLOWER_THREE_ROTATION_POLARITY_LEMMA_20260810.md).

A fourth, early-root charity rotation strengthens this to a strict opposite
bottom ordering: `r(B_r)>r(B_q)` but `q(B_q)>q(B_r)`.  The minimal residual
global-lex master is exactly UNSAT and has a dual-solver five-allocation core,
but aggregate packet lifting does not close the cell.  A solver-free exact
audit gives a positive nondegenerate 15-good state blocking a nine-candidate
aggregate family; its first lex escape splits `K` and `B_q`, transfers the
`B_q` good to `r`, and sends the `K` good to charity.  This establishes that
the next cap-free primitive must permit a strictly improving earlier root and
a losing later donor.  The exhaustive wall classification for that primitive
is
[`LEX_ROOTED_OWNER_CHARITY_DONATION_OBSTRUCTION_LEMMA_20260810.md`](LEX_ROOTED_OWNER_CHARITY_DONATION_OBSTRUCTION_LEMMA_20260810.md).

The residual payment threshold now selects a stronger operation without any
item cap.  A minimal `q`-paying packet `L subseteq T_r` produces a rotation
that strictly improves both mutual owners, parks the complement safely, and
can fail only at the evolved target `B_q+L`.  Partitioning the released
residual among the root and external blockers has exact response-Hall release
support; every internal response matching is PI.  The earlier root is always
payable from the residual.  Any external owner unpayable even by the full
residual must satisfy the sharp reverse polarity `B_q>R`.  Consequently the
live selector is reduced to simultaneous payment/Hall augmentation for only
`c,s`, or a root flip driven by that explicit polarity.  See
[`FLOWER_MINIMAL_PAYMENT_RESIDUAL_ROTATION_LEMMA_20260810.md`](FLOWER_MINIMAL_PAYMENT_RESIDUAL_ROTATION_LEMMA_20260810.md),
[`FLOWER_TWO_ROOT_RESIDUAL_SPLIT_RESPONSE_HALL_LEMMA_20260810.md`](FLOWER_TWO_ROOT_RESIDUAL_SPLIT_RESPONSE_HALL_LEMMA_20260810.md),
and
[`FLOWER_RESIDUAL_WALL_PAYMENT_POLARITY_LEMMA_20260810.md`](FLOWER_RESIDUAL_WALL_PAYMENT_POLARITY_LEMMA_20260810.md).

The external response chain is now proved finite without an item cap.  A
response source `a` either admits an ordinary/residual return from `q`, which
closes PI, satisfies the low-return inequality `q(X_a+R)<=q(X_q)`, or exposes
a named non-`q` response source.  Only the other external owner can be new,
so at most one augmentation remains before the relation is closed.  See
[`FLOWER_EXTERNAL_RETURN_AUGMENTATION_LEMMA_20260810.md`](FLOWER_EXTERNAL_RETURN_AUGMENTATION_LEMMA_20260810.md).

Keeping the unused complement of the external desired bundle strengthens
this reduction.  If `A subseteq W` is the external source's response bundle,
the return target is `X_a+R+(W\A)`.  Its edge has disjoint, internally
supplied incoming packets and therefore closes PI whenever `q` is its
source.  A PI-free survivor must satisfy the strict capture system
`q(W\A)<q(X_q)-q(X_a+R)` and
`q(X_a+R)<q(X_q)-(q(W)-q(X_q))`, or expose a named internal Hall defect.
See
[`FLOWER_COMPLEMENT_RETURN_AUGMENTATION_LEMMA_20260810.md`](FLOWER_COMPLEMENT_RETURN_AUGMENTATION_LEMMA_20260810.md).

The component library now also covers owner-rooted exchange stars, not only
charity-rooted hubs. A hub may receive a packet from one donor while
partitioning its released packet among that donor and other leaves. Any
internal response SDR is automatically a release-compatible PI edge set;
otherwise the exact remainder is open or Hall deficient. This is the
smallest operation required by the surviving connected-transfer profiles.
The live task is elimination of the remaining two-external-owner weighted
payment/Hall deficiency, not selection of a first residual component or
another fixed packet core. See
[`OWNER_ROOTED_HUB_SPLIT_RESPONSE_HALL_LEMMA_20260810.md`](OWNER_ROOTED_HUB_SPLIT_RESPONSE_HALL_LEMMA_20260810.md).

The strict top-core reverse-order leaf now factors back into that same
response-Hall architecture.  The root's desired `T_q+f` bundle and
`B_r>=f` force `r(T_q)>r(T_r)`; if the direct core exchange also has
`r(P')>r(K_T)`, the complementary top packets satisfy the reverse strict
order.  Meanwhile the live `q`-bottom polarity forces `q(T_r)>q(T_q)`, so
the minimal-payment residual rotation always restarts.  This does not yet
exclude a later revisit, but it removes top-core exchange as an independent
terminal mechanism. See
[`TOP_CORE_RESIDUAL_RESET_LEMMA_20260811.md`](TOP_CORE_RESIDUAL_RESET_LEMMA_20260811.md).

An inclusion-minimal all-four-owner response Hall defect is now also reduced
cap-free: its source neighborhood has size exactly three, and those three
sources match three distinct targets.  Giving each source its disjoint
desired core and consolidating every leftover good with the unique missing
source converts the defect to one residual-payment inequality.  Failure is
the explicit aggregate capture certificate (7); success leaves an EFX/PI
check or a missing-source recapture, rather than another arbitrary
four-target Hall relation.  The live termination problem is therefore a
single residual payment/root-change/recapture potential. See
[`ALL_OWNER_HALL_RESPONSE_COMPRESSION_LEMMA_20260811.md`](ALL_OWNER_HALL_RESPONSE_COMPRESSION_LEMMA_20260811.md).

The compressed endpoint now has a canonical cap-free selector.  Give each
response edge the value, in the missing source's row, of its cheapest
common-safe desired core and add one zero-cost dummy source.  A
minimum-cost perfect matching pays the unique residual owner exactly when
its cost is at most the value of all other base bundles plus `f`.  If every
matching is too expensive, assignment duality supplies explicit source and
target potentials certifying the obstruction.  Once paid, the three cores
are common-safe, so only the residual bundle can be an EFX wall; swapping
its response core with the corresponding source-owned core preserves this
one-wall normal form or yields one strict recapture inequality.  The next
proof obligation is to contradict the weighted dual/recapture orientation
using the flower inequalities or use it to force the final root change. See
[`WEIGHTED_RESPONSE_COMPRESSION_DUAL_LEMMA_20260811.md`](WEIGHTED_RESPONSE_COMPRESSION_DUAL_LEMMA_20260811.md).

The priority-sensitive endpoint is sharper still.  An unpaid compression
means its response cores captured a packet `C` from the missing source's
own base bundle worth more, in that row, than every unselected external good
`E`.  The missing source cannot be `r`: every root target contains the
common-safe desired core `T_q+f`, so `r` is always a response source.  Hence
every unpaid state is sacrifice-eligible.  Its EFX failures form only a
two-sided star between the missing owner and the three common-safe cores,
and between the source owners and the residual.  Whenever the same source
appears on both sides, one recapture strictly increases the missing owner's
residual utility; finite maximality eliminates all such aligned pairs.  The
sole terminal architecture is now a disjoint cross-star with the strict
four-level order recorded in (10), plus its one-sided degenerations. See
[`LEX_SACRIFICED_RESPONSE_COMPRESSION_LEMMA_20260811.md`](LEX_SACRIFICED_RESPONSE_COMPRESSION_LEMMA_20260811.md)
and
[`ROOT_ANCHORED_COMPRESSION_STAR_LEMMA_20260811.md`](ROOT_ANCHORED_COMPRESSION_STAR_LEMMA_20260811.md).

The response-compression theorem now covers the earlier closed Hall leaves,
not only a defect containing all four targets.  Every inclusion-minimal
deficient target set `U` has exactly `|U|-1` response sources, every
prescribed response edge extends to a near-perfect matching, and the union
of target owners and source owners can be recompressed into common-safe
desired cores plus a residual pool for the unmatched owners.  In the live
two-target/one-outside-source case, the remaining selector is exactly a
two-way partition of that pool.  A newly hardened subset-sum-injective
adversary has only the defects `{q,s}->{c}`, `{q,c}->{c}`, and
`{c,s}->{c}`; the first owner-union compression, using core `{z}`, has an
exact complete EFX lex endpoint.  Thus the previous targeted countermodel is
escaped, while the cap-free two-way residual partition theorem remains the
live gate. See
[`MINIMAL_HALL_OWNER_UNION_COMPRESSION_LEMMA_20260811.md`](MINIMAL_HALL_OWNER_UNION_COMPRESSION_LEMMA_20260811.md)
and
[`owner_union_compression_hardened_profile_audit.json`](owner_union_compression_hardened_profile_audit.json).

## Claim boundary

Closing this target would eliminate the exactly-three-nonsingleton branch.
It would still not resolve general four-agent additive EFX until the
all-four-nonsingleton branch and the nonnegative/tie limiting wrapper are
closed and the full argument receives independent expert review.

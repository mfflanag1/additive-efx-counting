# Nonroot three-placement relay collision elimination

**Date:** 2026-08-14

**Status:** cap-free removal of the root-holder collision dependency from the
rank-three relay; universally safe source-parking Hall compression remains

## Three complete probes

Use the reversed rank-three matching allocation `B` and place the positive
singleton `p` in turn at each nonroot owner `q,d,s`.  Every displayed
allocation uses the same at most three reversed matching supplier pairs plus
one charity pair, hence at most four packet-transfer edges.

If one probe is EFX, it is the required endpoint.  Otherwise extract an exact
globally minimum current-safe/current-desired response at each failed probe.

## A response hitting `p` is nonroot-held

At all three probes the current holder of `p` is nonroot.  If an extracted
response core `D` contains `p`, then

\[
 \{p\}\subseteq D
\]

with `D` common-safe at the actual probe floors and with its actual named
source and supplier.  These are precisely the hypotheses of
`NONROOT_SINGLETON_HIT_SAFE_ENVELOPE_DESCENT_LEMMA_20260814.md`.  A root
source is the strict anchor-reselection outcome already excluded by the
active saturation predicate.  For a nonroot source, safe sacrifice either
produces a response disjoint from `p` or replaces `D` by a strictly smaller
envelope still containing `p`.  The chain terminates; the singleton itself
cannot be a strong-envy target.

Consequently no saturated survivor of the three nonroot probes has to invoke
the disputed root singleton supplier-star theorem.  Every surviving adopted
response may be taken disjoint from `p`.

## Transport after whole-hit elimination

Among the surviving responses at the three probes, choose one of globally
minimum cardinality.  The proof of
`FOUR_PLACEMENT_SINGLETON_RESPONSE_TRANSPORT_LEMMA_20260814.md` uses only the
two placements being compared, so it applies verbatim to this three-state
family.  The selected physical core is safe at all three nonroot probes.  It
is desired at all three when its source is the root, and otherwise at every
probe except possibly the one parking `p` at that nonroot source.

Thus the exact remaining alternatives are:

1. a root-sourced universally safe response active at all three probes;
2. a nonroot-sourced universally safe response neutralized only by parking
   `p` at its source; or
3. another source/core of the same or larger response cardinality at that
   parking state.

These are source-parking/Hall alternatives.  They contain no root-held
retired singleton, no cross-state observer-safety band, and no unrestricted
packet-size exception.

## Consequence and boundary

The four-edge relay route no longer needs the overclaimed complete
`T_{L,times}^*` theorem or its root-holder supplier-star branch.  It needs
only the independently stated nonroot safe-envelope descent for a hitting
response, followed by matching/Hall compression of universally safe
disjoint responses.

This lemma does not prove supplier compatibility of the accumulated cores,
close their Hall deficiency, complete the fixed-`U` theorem, or prove
four-agent/general additive EFX.

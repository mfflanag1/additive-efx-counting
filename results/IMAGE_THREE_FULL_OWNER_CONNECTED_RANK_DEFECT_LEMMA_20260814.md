# Image-three full-owner connected rank-defect lemma

**Date:** 2026-08-14

**Status:** cap-free owner-graph classification; full owner recruitment is
automatic, while response-rank augmentation remains obstructed by capture

## Statement

Let `N` contain four owners and let `f:N->N` be a nonself response map:

\[
                         f(t)\ne t\qquad(t\in N).               \tag{1}
\]

Assume `|im(f)|=3`.  Form the undirected owner graph with an edge
`{t,f(t)}` for every target `t`.  This graph is connected.  Consequently an
image-three response fan already lies in one physical current-holder/source
component containing all four owners.

## Proof

Every connected component has at least two vertices because (1) forbids a
self-loop as a component.  If the four-vertex graph were disconnected, it
would therefore consist of two components of size two.  On a two-vertex
component, a nonself map that stays inside the component must swap the two
vertices.  Both vertices of each component would occur in the image, making
`f` surjective on all four owners.  This contradicts `|im(f)|=3`.

No valuation, good, packet-size, or supplier-purity assumption is used.

## Exact defect

Connectedness does not give response rank four.  There is one missing source
`m` and one duplicated source `a`.  The missing source's mandatory response
cannot simply augment a disjoint rank-three selection: by the two-choice fan
capture lemma, generalized-PI-freeness forces its complete strict margin to
intersect both one-core-per-represented-source choices.

Thus the survivor is exactly:

> a connected full-owner physical response component of source rank three,
> with the missing source's desired core margin captured by the represented
> fan union.

This rules out further owner recruitment as the needed progress coordinate.
The next operation must uncross the captured missing-source core, create a
disjoint fourth response, or enter the saturated full-owner base-margin
terminal without assuming response rank four.

## Relation to component extraction

The existing saturated represented-component extraction theorem uses a
rank-`|C|` Hamiltonian response path inside component `C`.  Here `C=N` but
the displayed fan has rank three.  Therefore owner connectedness alone does
not satisfy that theorem's hidden rank hypothesis.  Any composition claiming
otherwise is invalid.

## Claim boundary

Proved: connectedness of every one of the 48 nonself image-three maps and
the exact interpretation as a full-owner rank defect.  Not proved: rank-four
augmentation, reversal of the missing-source capture, satisfaction of the
base-margin extraction premises, a four-edge EFX allocation, or the fixed-
`U` theorem.

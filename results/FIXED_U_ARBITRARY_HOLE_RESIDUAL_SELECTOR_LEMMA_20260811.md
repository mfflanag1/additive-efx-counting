# Fixed-U arbitrary-hole residual selector lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of every active or source-inactive nonroot
core wall for any distinguished missing source; only the root-facing handoff
survives

## Selector family

Fix retained support `U`, the permanent root response core, and a nonroot
owner `d`. Let `F_d(U)` be the finite family of complete root-anchored
compressed states satisfying:

1. `d` is unrepresented and owns a distinguished residual cell `W`;
2. every represented source owns a pairwise-disjoint common-safe desired
   core; and
3. every exchange respects the fixed removed support `U`.

The family permits one, two, or three represented nonroot cores, any
corresponding additional residual cells, and either an active or inactive
distinguished hole. If it is nonempty, choose a state maximizing

\[
 v_d(W),                                             \tag{1}
\]

with deterministic tie-breaking only afterward. This is a single-row
selector; division by `v_d(X_d)` gives an equivalent scale-invariant
coordinate.

## Theorem

At the selected state, no strong-envy wall from `d` to a nonroot selected
core can be terminal. Every such wall gives at least one of:

1. whole-core rank descent with a strict same-row residual gain;
2. an unsafe-core response augmentation;
3. an EFX lexicographic endpoint or release-compatible PI component; or
4. a contradiction to (1).

Consequently every surviving selected-core wall of the distinguished hole is
root-facing.

## Active whole-core case

Let `A_j` be a nonroot common-safe desired core held by source `j`. If `d`
has a desired response into `A_j`, common-safe target-response rigidity makes
it the whole core. Apply whole-core return/two-hole descent to `A_j+W`,
retaining the root anchor and every other selected core. The strict inherited
potential clause gives `d` a new cell `W'` with

\[
 v_d(W')>v_d(W).                                    \tag{2}
\]

An EFX endpoint or internal SDR closes. Every other root-anchored output
still belongs to `F_d(U)` and contradicts (1). Thus an active nonroot core
edge cannot survive merely because full-priority matching protects its
current source.

## Source-inactive case

Suppose instead that `d` strongly envies `A_j` but has no desired response
into it. Apply source-inactive core/residual repair to `A_j+W`.

At a successful common-safe leaf, `j` remains represented, the root anchor
and `U` are unchanged, and the new residual again satisfies (2). The new
state lies in `F_d(U)` and contradicts (1). If the repaired core is unsafe,
globally minimal desired-subset extraction gives the named augmentation.

At J-exhaustion, stop representing nonroot `j`, keep the root anchor and all
other cores, and apply two-hole cut-and-choose to `A_j+W`, with `d` as the
divider. Its inherited-potential clause again gives (2). Lower response rank
is allowed in `F_d(U)`. An EFX endpoint closes by global lex maximality, an
internal SDR is PI, and every other root-anchored output contradicts (1).

Whole-core response, successful source-inactive repair, and nonroot
J-exhaustion exhaust a nonroot selected-core wall. Only a wall against the
permanent root core can survive. \(\square\)

## Consequence for the third-owner fork

If the exchange-stable two-row frontier leaves an external source below
base, treat that source as `d` and maximize its residual over every root-
anchored compression rank before selecting another packet. Whether `d` is
response-active or response-silent, it cannot circulate among external
cores: whole-core descent, source-inactive repair, or nonroot exhaustion
strictly raises the same globally maximized residual.

Thus the remaining third-owner operation is no longer an arbitrary external
hole repair. It is the physical root-facing top/floater or captured-bottom
handoff after all same-row nonroot compensation has been globally optimized.

## Verification and boundary

[`fixed_u_arbitrary_hole_residual_selector_audit.json`](fixed_u_arbitrary_hole_residual_selector_audit.json)
records exact dependency hashes for response rigidity, whole-core descent,
source-inactive repair, two-hole descent, and full-priority matching, and
checks all three strict same-row gains symbolically.

This lemma does not close the root-facing selector, terminate its captured-
bottom/root-budget frontier, select the final surplus-budgeted fork, close
`GG`, or prove four-agent/general additive EFX.

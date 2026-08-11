# Fixed-U arbitrary-hole residual selector lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of every nonroot source-inactive wall for any
distinguished missing source; only the root-facing handoff survives

## Selector family

Fix retained support `U`, the permanent root response core, and a nonroot
owner `d`. Let `F_d(U)` be the finite family of complete root-anchored
compressed states satisfying:

1. `d` is unrepresented and owns a distinguished residual cell `W`;
2. every represented source owns a pairwise-disjoint common-safe desired
   core;
3. `d` has no desired response into any active target;
4. every exchange respects the fixed removed support `U`.

The family permits one, two, or three represented nonroot cores and any
corresponding additional residual cells. If it is nonempty, choose a state
maximizing

\[
 v_d(W),                                             \tag{1}
\]

with deterministic tie-breaking only afterward. This is a single-row
selector; division by `v_d(X_d)` gives an equivalent scale-invariant
coordinate.

## Theorem

At the selected state, no source-inactive strong-envy wall from `d` to a
nonroot selected core can be terminal. Every such wall gives at least one of:

1. `d` becomes response-active;
2. an unsafe-core response augmentation;
3. an EFX lexicographic endpoint or release-compatible PI component; or
4. a contradiction to (1).

Consequently every surviving source-inactive wall of the distinguished hole
is root-facing.

## Proof

Let `A_j` be a nonroot common-safe desired core held by source `j`, and apply
the source-inactive core/residual repair to `A_j+W`.

At a successful common-safe leaf, `j` remains represented, the root anchor
and `U` are unchanged, and the new `d` residual satisfies

\[
 v_d(W')>v_d(W).                                    \tag{2}
\]

If `d` is still response-inactive, the new state lies in `F_d(U)` and
contradicts (1). If `d` becomes active, use full-priority anchor-constrained
matching. If the repaired core is unsafe, globally minimal desired-subset
extraction gives the named augmentation.

At J-exhaustion, stop representing nonroot `j`, keep the root anchor and all
other cores, and apply two-hole cut-and-choose to `A_j+W`, with `d` as the
divider. Its inherited-potential clause gives `d` a new cell `W'` satisfying
(2). Lower response rank is allowed in `F_d(U)`. An EFX endpoint closes by
global lex maximality, an internal SDR is PI, and response activation exits
to the full-priority selector. Otherwise the resulting state again belongs
to `F_d(U)`, contradicting (1).

Successful repair and J-exhaustion are exhaustive. Thus only a wall against
the permanent root core can survive. \(\square\)

## Consequence for the third-owner fork

If the exchange-stable two-row frontier leaves an external source below base,
treat that source as `d` and maximize its residual over every root-anchored
compression rank before selecting another packet. A response-active `d`
enters the triangular full-priority matching chain. A response-silent `d`
cannot circulate among external cores: every nonroot wall either activates
it, augments the owner component, closes, or violates (1). It reaches the
root-facing selector directly.

Thus the remaining third-owner operation is no longer an arbitrary external
hole repair. It is the physical root-facing top/floater or captured-bottom
handoff after all same-row nonroot compensation has been globally optimized.

## Verification and boundary

[`fixed_u_arbitrary_hole_residual_selector_audit.json`](fixed_u_arbitrary_hole_residual_selector_audit.json)
records exact dependency hashes for source-inactive repair, two-hole descent,
full-priority anchor matching, and the permanent-anchor theorem, and checks
the same-row strict-max implications symbolically.

This lemma does not close the root-facing selector, terminate its captured-
bottom/root-budget frontier, select the final surplus-budgeted fork, close
`GG`, or prove four-agent/general additive EFX.

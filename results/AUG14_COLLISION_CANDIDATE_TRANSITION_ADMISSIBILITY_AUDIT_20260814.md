# Aug-14 collision-candidate transition-admissibility audit

**Date:** 2026-08-14

**Correction (2026-08-14):** the claimed admission of the complete-current-
exterior supplier star overlooked the frozen declared-floor requirement.
The operation empties later owners and is conditional until their floors are
paid or an explicit controlled reset is proved.  The base-charity reset
remains admitted.  See
`ROOT_GLOBAL_SUPPLIER_STAR_FLOOR_ADMISSIBILITY_GAP_20260814.md`.

**Verdict:** the base-charity reset is admitted, but the complete-current-
exterior supplier star remains conditional at the declared-floor gate.  Its
composition with `T_q+f` is therefore not yet a closure theorem.

**Equality-face update (2026-08-14).**  The base-donation row remains invalid
as a generic full-restoration rewrite. Its unique nondegenerate root-equality
specialization is now admitted by a different local construction: reuse the
already admitted equality packet `S^-`, then leave one incoming packet good
at the root or add one off-packet donation. See
`ROOT_EQUALITY_BASE_RESTORATION_PACKET_SPREAD_ADMISSION_THEOREM_20260814.md`.

**Global-operation update (2026-08-14).**  The complete supplier-star
sacrifice explicitly names every current exterior holder and eliminates all
strict/equality subpacket payments. Its exterior identity forces the packet
into `X_r`. Moving the base charity singleton to `X_r` then gives the one-good
reset without changing any owner bundle or reversing any retired transfer.

## Governing rule

The frozen contracts impose two independent requirements:

1. a proposed allocation must conserve physical goods, floors, signed
   suppliers, releases, and the current root/anchor obligations; and
2. progress is recorded only after one of the actual `G0--G10` operations
   adopts the tested allocation, response, or anchor coordinate.

Bare feasibility and a smaller intersection `D cap K` do not meet the second
requirement. A response found at a counterfactual allocation cannot decrease
the collision coordinate of the current state unless an admitted operation
reaches that allocation.

## Candidate audit

| Candidate | Exact part that survives | Missing admission premise | Current use |
|---|---|---|---|
| complete-current-exterior subpacket sacrifice | exact root margin, proper packet response, and equality packet spread | positive declared floors of emptied later owners, unless a controlled reset is proved | conditional global root cut |
| base-charity reset `X_r+f` | only the enlarged root target can be unsafe; every whole-`K` response has the exact on/off form | none: charity supplies `f` and every owner keeps her base bundle | admitted one-good normalization |
| base restoration plus one-good root donation | every target has proper/empty `K` intersection in the stated on/off-packet geometries | generic restoration can move retired goods away from recorded holders; the unique admitted equality return now supplies a local decomposition only on the equality face | conditional in general; equality face closed |
| exterior pooling `(X_r-g)+O`, singleton `{g}` | wall localization and atomwise exterior-dominance inequality are exact at that allocation | positive declared floors of emptied donors; exterior dominance is conditional | conditional strict branch |
| singleton isolation plus arbitrary two-agent EFX complement | singleton target is universally safe and all test-allocation responses avoid `{g}` | no admitted operation implements the complement repartition with its supplier/floor handoff | conditional wall-localization lemma |
| proper nonroot split inside the stated strict-root sacrifice interface | target locality puts `T` and `K-T` in different cells | valid only under the theorem's explicit strict-root, protected-target, and compression premises; it is not a generic state rewrite | retain as a typed conditional transition theorem |

## Consequence for the research frontier

Conditional on crossing the root-side floor-admission gate, the resulting
cut is immediately contradictory under the frozen anchored `GG` interface. Exterior dominance says
`v_r(k)>v_r(G-X_r)` for `k in K subseteq X_r`; the permanent old edge gives
`T_q+f subseteq G-X_r` with `v_r(T_q+f)>v_r(X_r)>=v_r(k)`. Thus the
The live task is therefore a floor-compatible supplier-star or controlled
floor reset; without it the response-source/debt-to-anchor conversion may
still be needed for `T_{L,times}^*`.

## Claim boundary

This audit retains the warning against generic counterfactual rewrites while
promoting only the base-charity reset.  The old-root-core contradiction is
conditional on the supplier-star floor gate, so `T_{L,times}^*` remains
open; nothing here proves four-agent or general additive EFX.

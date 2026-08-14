# Liquidated-root three-source physical-compression frontier

**Date:** 2026-08-14

**Status:** exact cap-free packet-size census inside the declared whole-cell
normal form; it isolates six five-edge source maps but does not prove the
fixed-`U` theorem

## Setting

Work at the liquidated-root state from
`FIXED_U_ROOT_RESIDUAL_NONEMPTY_LIQUIDATION_REDUCTION_LEMMA_20260814.md`.
Label the root `0`.  Its pure anchor cell is supplied by a fixed
`q in {1,2,3}`; its residual `Y_0` is supplied by `0`; and each ordinary
nonroot cell is supplied by its own owner.  Charity is the singleton `p`.

Let `f(t)` be the nonself source desiring the common-safe core in target
cell `t`.  Assume `f` has image size three.  Thus it has one missing source
`m` and one duplicated source `a`.

The whole-cell normal form chooses one target cell for each represented
source, sends that entire cell to its named source, retains the one omitted
target cell, routes the entire root residual `Y_0` to any owner, and gives
`p` to `m`.  In the missing-supplies-duplicate class, the omitted target is
`m`.  In the foreign-duplicate class, either of the two targets naming `a`
may be omitted.

Replacing a desired core by its whole target cell cannot hurt its recipient.
Routing the disjoint whole residual `Y_0` to any already paid owner also
cannot hurt payment.  These are packet-size-free monotonicity operations.

## Exact census

For each fixed anchor supplier `q`, there are 48 nonself image-three maps.
The exhaustive audit minimizes the number of distinct original
supplier-to-destination pairs over every allowed omission and all four
destinations of `Y_0`, including the charity-to-`m` pair.

The minimum-edge distribution is:

| source-map class | 3 edges | 4 edges | 5 edges |
|---|---:|---:|---:|
| nonroot missing, foreign duplicate | 6 | 12 | 0 |
| nonroot missing, missing supplies duplicate | 6 | 12 | 0 |
| root missing, foreign duplicate | 2 | 4 | 0 |
| root missing, missing supplies duplicate | 0 | 0 | 6 |

Therefore **42 of the 48** maps fit within four physical pairs.  The exact
survivors are the **six root-missing, missing-supplies-duplicate maps**.
For every anchor supplier, each survivor needs five distinct pairs inside
this whole-cell normal form: three nonroot source moves, the anchor-supplier
return to the root, and charity to the root.  Free rerouting of `Y_0` cannot
cancel any of them.

Across all three choices of `q`, the replay histogram is 42 three-edge,
84 four-edge, and 18 five-edge labelled configurations.
The regression test independently reconstructs the census with integer edge
masks and reproduces both the histogram and the exact six survivor maps.

## Payment interpretation

For the 18 nonroot-missing maps in the missing-supplies-duplicate class,
the duplicate-omission argument already proves strict payment of all four
owners, now with an unconditional at-most-four original-pair construction
in this liquidated-root cell basis.

The six root-missing maps in that class are likewise all-owner paid, but the
normal form costs five pairs.  They are the sharp physical obstruction to
this particular compression.

All 24 foreign-duplicate maps fit topologically within four pairs.  Their
missing owner may lose its selected cell and is not automatically paid by
`p`; the paid-hole trimming/double-capture lemma is still required.  Hence
the census does not by itself produce an EFX endpoint.

## Claim boundary

Proved: exhaustive minimality within the stated whole-cell normal form,
uniformly in the anchor supplier and without a packet-size cap; 42/48 maps
admit at most four physical pairs, and the remaining six are exactly the
root-missing missing-supplies-duplicate maps.

Not proved: minimality over arbitrary split packets or cyclic packet graphs;
payment closure of the foreign-duplicate class; observer EFX safety;
decorated-repeat termination; the universal rank-three fixed-`U` theorem;
four-agent additive EFX; or general additive EFX.

## Next exact target

Attack only the six survivor maps.  Either split or cyclically reroute the
root anchor so that one of the five pairs cancels while retaining root
payment and represented-source margins, or prove from the full signed
PI-free saturation ledger that one of their three nonroot source moves is
release-compatible generalized PI.  A proof confined to whole cells cannot
close this class.

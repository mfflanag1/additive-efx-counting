# Liquidated-root three-source physical-compression frontier

**Date:** 2026-08-14

**Status:** exact conditional census inside a pure-cell liquidated-root
normal form; applicability to the accumulated reservoir fan is not proved

## Setting

Consider the liquidated-root cell basis suggested by
`FIXED_U_ROOT_RESIDUAL_NONEMPTY_LIQUIDATION_REDUCTION_LEMMA_20260814.md`.
Label the root `0`.  Its pure anchor cell is supplied by a fixed
`q in {1,2,3}`; its residual `Y_0` is supplied by `0`; and each ordinary
nonroot cell is supplied by its own owner.  Charity is the singleton `p`.

Let `f(t)` be the nonself source desiring the common-safe core in target
cell `t`.  Assume `f` has image size three.  Thus it has one missing source
`m` and one duplicated source `a`.

The census additionally assumes the following **pure-cell lift**, which is
not supplied by the corrected reservoir-fan theorem:

1. each selected core is contained in the displayed single original-
   supplier cell for its target;
2. enlarging it to that whole cell still pays its named source; and
3. the source's desire does not depend jointly on a root-residual packet
   that is routed to a different owner.

These conditions hold for a response in an ordinary nonresidual target of a
single liquidation probe.  They do not automatically hold for four fan
cores accumulated across different probes or later decorated states.  Such
cores may mix several original suppliers.

The whole-cell normal form chooses one target cell for each represented
source, sends that entire cell to its named source, retains the one omitted
target cell, routes the entire root residual `Y_0` to any owner, and gives
`p` to `m`.  In the missing-supplies-duplicate class, the omitted target is
`m`.  In the foreign-duplicate class, either of the two targets naming `a`
may be omitted.

Under the pure-cell lift, replacing a desired core by its whole displayed
cell cannot hurt its recipient.  Routing the disjoint whole residual `Y_0`
to an already paid owner also cannot hurt payment.  Without item 3, splitting
the residual away from the named response source may destroy payment.

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
the duplicate-omission argument proves strict payment of all four owners.
The census supplies an at-most-four original-pair construction only when the
additional pure-cell lift above is verified for those selected cores.

The six root-missing maps in that class are likewise all-owner paid, but the
normal form costs five pairs.  They are the sharp physical obstruction to
this particular compression.

All 24 foreign-duplicate maps fit topologically within four pairs.  Their
missing owner may lose its selected cell and is not automatically paid by
`p`; the paid-hole trimming/double-capture lemma is still required.  Hence
the census does not by itself produce an EFX endpoint.

## Claim boundary

Proved: exhaustive minimality within the stated conditional whole-cell normal form,
uniformly in the anchor supplier and without a packet-size cap; 42/48 maps
admit at most four physical pairs, and the remaining six are exactly the
root-missing missing-supplies-duplicate maps.

Not proved: the pure-cell lift for the accumulated reservoir fan; independent
routing of `Y_0` when it contributes to a desired core; minimality over
arbitrary split packets or cyclic packet graphs;
payment closure of the foreign-duplicate class; observer EFX safety;
decorated-repeat termination; the universal rank-three fixed-`U` theorem;
four-agent additive EFX; or general additive EFX.

## Next exact target

First prove or refute the pure-cell lift from the actual decorated response
supports.  If it holds, attack the six survivor maps by splitting or
cyclically rerouting the root anchor.  If it fails, the correct target is the
original support set `Pi` in the duplicate-omission lemma, not this idealized
cell census.

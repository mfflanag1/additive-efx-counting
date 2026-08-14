# Fixed-U support-edge three-edge no-go

**Date:** 2026-08-13

**Status:** exact bounded sharpness result; four support-provenance packet
edges are necessary in the declared root-facing rank-three atomization

## The exact profile

Iteration 1 of
[`fixed_u_rank_three_root_facing_support_edge_cegar.json`](fixed_u_rank_three_root_facing_support_edge_cegar.json)
is a strictly positive rational twelve-atom profile satisfying all declared
`A,H,Q,W,K,J,L,M` packet premises, the named common-safe retained cores
`r:A`, `q:Q`, and `s:E`, and the root-facing orientation

\[
 v_d(W)<\tau_d(A),\qquad
 v_d(W)\ge \tau_d(Q),\tau_d(E),v_d(P).
\]

The complete ordinary/current subset-response relations have maximum rank
three at support, maximum ordinary rank two at the split, and maximum mixed
rank three at reassembly.  Thus the profile is not one of the earlier hidden
rank-four or nonroot-wall false frontiers.

## Exact support-provenance census

Measure a packet edge from the physical support state

\[
 r:A+H,\quad q:Q,\quad d:W,\quad s:E,\quad c:P.
\]

One edge is one ordered pair `(initial supplier, final owner)` carrying at
least one good; an edge may carry an arbitrarily large packet in the target
cap-free formulation.  The independent exact-arithmetic audit enumerates
every complete allocation using at most four such edges:

| exact packet edges | allocations examined | complete EFX allocations |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 4 | 0 |
| 2 | 288 | 0 |
| 3 | 8,016 | 0 |
| 4 | 108,288 | 33 |

The 33 four-edge allocations agree exactly with the solver menu.  They use
16 distinct directed transfer graphs.  Twenty-two are connected on charity
and all four owners; the remaining witnesses include genuine owner swaps and
disconnected components.  Thus neither a three-edge selector nor a single
tree topology can prove the desired universal statement.

## Consequence

The proposed four-edge theorem is sharp already in its canonical finite
cell.  Any cap-free proof must permit:

1. donation of the complete singleton charity packet;
2. three additional owner packet edges;
3. owner cycles as well as paths; and
4. multiple outgoing packets from one physical supplier.

The remaining target is exactly to prove that edge five is never necessary
under the full saturated root-facing rank-three premises, or to produce a
profile for which every four-edge completion fails.

## Boundary and replay

This profile encodes the packet, root-facing, and necessary response-rank
conditions.  It does **not** encode the full signed recurrence history,
deterministic selector reachability, or every saturation/Hall-reset premise.
It proves bounded sharpness, not the universal four-edge theorem and not a
counterexample to complete additive EFX.

```bash
/private/tmp/efx-charity-py/bin/python -m \
  tracks.parkability.audit_fixed_u_support_edge_three_no_go \
  --source results/fixed_u_rank_three_root_facing_support_edge_cegar.json \
  --iteration 1 \
  --output results/fixed_u_support_edge_three_no_go_audit.json

/private/tmp/efx-charity-py/bin/pytest -q \
  tracks/parkability/test_fixed_u_support_edge_three_no_go.py
```

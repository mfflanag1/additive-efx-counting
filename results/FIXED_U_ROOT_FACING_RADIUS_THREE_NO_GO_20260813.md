# Fixed-U root-facing radius-three no-go

**Date:** 2026-08-13

**Status:** exact bounded falsification of every at-most-three-good EFX
selector in the declared root-facing rank-three cell; cap-free termination
remains open

## Exact root-facing profile

Round 13 of
[`fixed_u_rank_three_root_facing_cegar.json`](fixed_u_rank_three_root_facing_cegar.json)
is a strictly positive rational twelve-atom profile satisfying:

1. the complete declared `A,H,Q,W,K,J,L,M` packet premises;
2. named base-common-safe desired cores `r:A`, `q:Q`, and `s:E`;
3. response rank at most three at support, split, and reassembly, even after
   adjoining every same-state current-safe decorated response;
4. the exact root-facing wall orientation
   \[
   v_d(W)<\tau_d(A),
   \quad v_d(W)\ge\tau_d(Q),\tau_d(E),v_d(P).
   \]

The exact rational values of the final display are

\[
v_d(W)=561/574<81/82=\tau_d(A),
\]

\[
\tau_d(Q)=1149/1435,
\quad \tau_d(E)=848/1435,
\quad v_d(P)=1691/2870.
\]

Thus this is not one of the earlier nonroot-wall or hidden-rank-four false
frontiers.

## Exhaustive no-go

Independent exact enumeration gives:

| exact moved-good radius | assignments examined | EFX lex improvements |
|---:|---:|---:|
| 0 | 1 | 0 |
| 1 | 48 | 0 |
| 2 | 1,056 | 0 |
| 3 | 14,080 | 0 |
| 4 | 126,720 | 44 |

The 44 radius-four allocations match the CEGAR menu exactly. Every one has
a connected active supplier graph. Their topologies include four-node paths,
owner cycles, charity-rooted exchanges, and cycles in which charity both
donates and receives.

Therefore an analytic closure restricted to one bilateral swap or a
three-good/three-edge transfer is false at the exact root-facing packet and
rank boundary. The next cap-free lemma must allow four physical packet edges
with unrestricted packet cardinalities, or derive strict historical progress
before demanding EFX.

## Claim boundary

This profile is still not a full fixed-`U` countermodel. It does not encode
exact historical reachability through every deterministic selector, the
complete signed response/release record at two repeated occurrences, or all
Hall resets. Those premises could exclude it. Conversely, the 44 EFX escapes
show it is not an additive-EFX counterexample.

[`audit_fixed_u_root_facing_radius_three_no_go.py`](../tracks/parkability/audit_fixed_u_root_facing_radius_three_no_go.py)
uses exact `Fraction` arithmetic, independently reconstructs the packet
premises and response relations, and enumerates all assignments through
radius four.

```bash
/private/tmp/efx-charity-py/bin/python -m \
  tracks.parkability.audit_fixed_u_root_facing_radius_three_no_go \
  --source results/fixed_u_rank_three_root_facing_cegar.json \
  --iteration 13 \
  --output results/fixed_u_rank_three_root_facing_no_go_audit.json
```

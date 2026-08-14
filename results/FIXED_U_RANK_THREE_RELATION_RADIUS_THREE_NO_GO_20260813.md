# Fixed-U rank-three-relation radius-three no-go

**Date:** 2026-08-13

**Status:** exact bounded falsification of every at-most-three-good EFX
selector after imposing the necessary response-rank gates; cap-free recurrence
termination remains open

## Stronger adversarial cell

The earlier packet-only radius-three no-go could be dismissed because its
available response relation already had rank four. The strengthened decision
therefore recomputes every base-common-safe and same-state current-safe
desired subset at all three physical partitions:

1. the retained-support state;
2. the sacrificed-donor split; and
3. donor reassembly.

It requires the named retained cores `r:A`, `q:Q`, and `s:E` to be actual
base-common-safe desired cores. It forbids a rank-four mixed response matching
at support and reassembly and a rank-four ordinary SDR at the split. These
are necessary conditions for a saturated rank-three recurrence: every
excluded rank-four state enters existing response/PI or Hamiltonian closure.

## Exact result

Round 4 of
[`fixed_u_rank_three_relation_cegar_v3.json`](fixed_u_rank_three_relation_cegar_v3.json)
is a strictly positive rational twelve-atom profile satisfying all declared
packet premises and these response gates. Its exact maximum response ranks
are:

| physical state | ordinary rank | current rank | mixed rank |
|---|---:|---:|---:|
| support | 3 | 3 | 3 |
| split | 3 | 2 | 3 |
| reassembly | 3 | 3 | 3 |

Solver-independent exhaustive enumeration gives:

| exact moved-good radius | assignments examined | EFX lex improvements |
|---:|---:|---:|
| 0 | 1 | 0 |
| 1 | 48 | 0 |
| 2 | 1,056 | 0 |
| 3 | 14,080 | 0 |
| 4 | 126,720 | 31 |

The independently enumerated 31 radius-four allocations equal the recorded
CEGAR menu exactly. Hence the statement

> every rank-three fixed-`U` packet separator has an immediate EFX lex
> improvement moving at most three physical goods

is false even after the necessary full-relation rank gates are imposed.

## What the 31 escapes say

The surviving radius-four operations are not one fixed rooted tree. Their
supplier graphs include charity donation followed by a `d/s` bilateral
exchange, charity-to-`d` paths with root or protected-owner compensation, and
four-owner cycles. The correct cap-free operation must therefore allow:

- charity both to donate and receive replacement packets;
- four packet edges, with unrestricted packet cardinality; and
- either a connected cyclic exchange or strict response/support progress.

This points back to the two-hole connected charity-exchange lemma, not a
smaller-radius selector.

## Exact boundary

This is a bounded no-go theorem, not a fixed-`U` countermodel. The encoding
still omits the complete historical signed-response record, deterministic
anchor-priority selection, exact reachability through every reset, and a
genuine repeated transition. Those premises may exclude the profile or force
one of the radius-four packet graphs cap-free.

[`audit_fixed_u_rank_three_relation_no_go.py`](../tracks/parkability/audit_fixed_u_rank_three_relation_no_go.py)
uses exact `Fraction` arithmetic, enumerates all 141,905 assignments through
radius four, reconstructs every subset response relation independently of
Z3, and verifies the exact menu equality.

```bash
/private/tmp/efx-charity-py/bin/python -m \
  tracks.parkability.audit_fixed_u_rank_three_relation_no_go \
  --source results/fixed_u_rank_three_relation_cegar_v3.json \
  --iteration 4 \
  --output results/fixed_u_rank_three_relation_no_go_audit.json
```

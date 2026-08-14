# Fixed-U radius-three exchange no-go

**Date:** 2026-08-13

**Status:** exact bounded falsification of a three-good terminal selector; the
cap-free fixed-`U` recurrence remains open

## Question

The named packet recurrence has base allocation

\[
X_r=\{a_0,m\},\quad X_q=\{q_0,a_1\},\quad
X_d=\{h,k,g_q\},\quad X_s=\{e,p\},\quad
P=\{j,l,g_r\}.
\]

It satisfies the complete twelve-atom packet premises currently encoded:
base EFX and charity safety, strict desired cores, inclusion-minimal `K`, the
strict `q`-budget separator, `J/L` substitution, failure of every residual
subset `M subseteq W`, split payment with `s` sacrificed, and reassembly
payment with `d` sacrificed.

A tempting closure was that these inequalities must admit an EFX
lexicographic improvement changing at most three physical goods. That claim
is false.

## Exact no-go profile

Round 10 of
[`fixed_u_full_packet_batch_cegar.json`](fixed_u_full_packet_batch_cegar.json)
is a strictly positive rational valuation profile satisfying every declared
packet inequality. Independent exhaustive enumeration gives:

| exact number of moved goods | allocations examined | EFX lex improvements |
|---:|---:|---:|
| 0 | 1 | 0 |
| 1 | 48 | 0 |
| 2 | 1,056 | 0 |
| 3 | 14,080 | 0 |
| 4 | 126,720 | 52 |

Thus every one-step, bilateral, and three-good exchange fails, while the
profile is not a terminal obstruction: exactly 52 radius-four EFX lex
improvements exist. The independently enumerated set is byte-normalized and
equals the 52-allocation solver menu recorded by the batched CEGAR.

The two radius-four rounds do not share one fixed transfer graph. Their
escapes include charity-rooted replacements, owner cycles, and disconnected
simultaneous exchanges. Therefore neither “one more local edge” nor one fixed
three-owner cycle is a justified universal operation.

## Consequence for the cap-free proof

The fixed-`U` termination argument must do at least one of the following:

1. permit a four-packet connected exchange whose packets may contain
   arbitrarily many goods;
2. use response/support/history progress rather than demand an immediate EFX
   allocation; or
3. derive additional full-state inequalities (response saturation,
   reachability, signed-repeat consistency, or Hall-reset premises) that
   exclude this bounded packet profile.

This is a no-go theorem for a proposed proof route, not a counterexample to
fixed-`U` termination. In particular, the profile does **not** encode response
saturation, a genuine reachable repeated state, or all Hall resets. It does
not refute four-agent additive EFX.

## Independent replay

[`audit_fixed_u_radius_three_exchange_no_go.py`](../tracks/parkability/audit_fixed_u_radius_three_exchange_no_go.py)
uses exact `Fraction` arithmetic and independent exhaustive enumeration; it
does not call Z3 or import the CEGAR implementation.

```bash
/private/tmp/efx-charity-py/bin/python tracks/parkability/audit_fixed_u_radius_three_exchange_no_go.py \
  --source results/fixed_u_full_packet_batch_cegar.json \
  --iteration 10 \
  --output results/fixed_u_radius_three_exchange_no_go_audit.json
```

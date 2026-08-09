# Adaptive-root/order bridge: exact obstruction and missing operation

**Date:** 2026-08-09

**Status:** exact atomic refutation of the root-only bridge; its missing
cap-free suffix operation is now supplied by the reservoir-exchange theorem

**Scope:** four positive additive agents, one charity good, strict alternating
seven-good atom

## Result

Changing the root or priority order does not by itself close the two surviving
orders `(p,s,r,q)` and `(s,p,q,r)`. There is an exact alternating profile in
which:

1. both canonical promoted root rotations fail EFX strictly;
2. both canonical anchored root rotations are EFX, but they improve only in
   the already-settled orders `(p,q,r,s)` and `(s,r,q,p)`;
3. both bottom-for-charity exchanges and the direct cross-bottom swap also
   fail EFX; and
4. the smallest EFX escape in a surviving order is an **anchored suffix
   transfer**: move one top subgood from `r` to `q`, leaving both singleton
   roots and the charity good fixed.

Thus an adaptive root or priority selection cannot replace the packet-selection
step. The smallest missing operation in this countermodel is a one-subpacket
anchored suffix transfer. For arbitrary packets, its cap-free replacement is
the external-observer-safe reservoir exchange now proved in
[`ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md`](ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md).

This does not refute the broad statement “some external-observer-safe EFX
improvement exists”; the displayed suffix transfer is such an improvement.
It refutes the proposed *bridge mechanism* consisting only of root flip,
half-turn, priority relabeling, and the three most immediate two-good
exchanges. Complete four-agent additive EFX remains open.

## Countermodel

Order agents as `(p,r,s,q)` and goods as
`(tr,br,tq,bq,x,y,f)`. The base allocation is

\[
X_p=\{x\},\quad X_r=\{tr,br\},\quad
X_s=\{y\},\quad X_q=\{tq,bq\},
\]

with `f` unallocated. Values are:

| agent | tr | br | tq | bq | x | y | f |
|---|---:|---:|---:|---:|---:|---:|---:|
| p | 4 | 23 | 2 | 2 | 31 | 29 | 29 |
| r | 6 | 49 | 6 | 6 | 52 | 58 | 3 |
| s | 25 | 25 | 29 | 4 | 58 | 62 | 37 |
| q | 1 | 4 | 5 | 3 | 39 | 7 | 1 |

The base utilities are `(31,55,62,8)`. Exact replay verifies all strict
alternating structural premises used by the atomic cell: base EFX, charity
dominance, ordinary envy edges `r -> s` and `q -> p`, selected champion
sets `tr+f` and `tq+f`, absence of all other basic desired families, and
absence of the four compatible cross-bottom families.

## Why the two root choices fail

For root `p`, the promoted rotation has utility vector `(33,58,33,39)`.
It fails EFX because `s`, owning value 33, sees a deletion remainder of
`p`'s bundle worth 37.

For the half-turn root `s`, the promoted rotation has utility vector
`(27,58,66,39)`. It fails EFX because `p`, owning value 27, sees a deletion
remainder of `s`'s bundle worth 29.

The anchored root-flip fallbacks are EFX, with deltas respectively

\[
(0,+3,0,0),\qquad (0,0,0,+31).
\]

Those deltas improve only after `q` or `r` is placed before the singleton
owner who may be sacrificed. They do not yield a contradiction to
maximality in either surviving order.

Priority relabeling alone cannot repair this: the allocation and champion
premises are order-independent, but lexicographic maximality is not. A state
chosen maximal for one order cannot simply be declared maximal for another.

## Exact smallest missing operation

For surviving order `(s,p,q,r)`, transfer `tr` from `r` to `q` and change
nothing else:

\[
Y_p=\{x\},\quad Y_r=\{br\},\quad Y_s=\{y\},\quad
Y_q=\{tr,tq,bq\},
\]

with `f` still unallocated. Its utility vector is `(31,49,62,9)`, hence its
delta is `(0,-6,0,+1)`. It is EFX and lexicographically improves the base in
order `(s,p,q,r)`. The exhaustive `5^7` allocation census proves that one
changed good is minimal and that this is the unique one-good improving EFX
allocation for that order.

For the other surviving order `(p,s,r,q)`, the minimum is three changed
goods: promote `p` to `tr+f`, leave `br` with `r`, retain `s=y` and `q=X_q`,
and release `x`. This is the residual-preserving promoted-root operation,
not the canonical four-bundle rotation.

These witnesses identify the necessary cap-free operation class:

> **Anchored suffix reallocation.** Keep the first singleton root fixed and
> repartition selected safe subpackets among the other three agents, allowing
> a later-priority owner to lose utility.

The one-good transfer is only its atomic shadow. In arbitrary packets one
must select a subpacket whose every one-good deletion is safe for the fixed
external observer. That is precisely the unresolved packing premise in the
two-safe-bundle reduction; a fixed whole-packet transfer is not valid.

## Global-potential audit

Pareto maximality is not a viable replacement selector. The previously
frozen profile `V*` is an alternating, compatible-family-free EFX allocation
with no Pareto-improving partial EFX allocation among all `5^7` assignments,
yet every first-priority agent has a sacrificing lexicographic escape. This
exactly separates Pareto maximality from the global lexicographic premise.

As an adversarial check, all six strict fixed-order countermodels have a
Pareto handoff, and 17 of the 19 frozen eleven-good/q-face profiles have one
inside the 39,366-member singleton-return family. The remaining two also
have unrestricted Pareto-EFX handoffs, found by exact QF_LIA and directly
replayed. Those corpus facts show that Pareto selection often helps, but
`V*` proves it cannot be the universal argument.

## Verification

Primary artifacts:

- `alternating_adaptive_root_or_two_good_bridge.json`: generated strict
  countermodel after blocking both promoted rotations, both bottom-charity
  exchanges, and the cross-bottom swap;
- `alternating_adaptive_root_order_bridge_audit.json`: structural replay,
  strict EFX-failure witnesses, and exhaustive surviving-order census;
- `decide_adaptive_root_promotion_bridge.py`: exact QF_LRA generator; and
- `audit_adaptive_root_order_bridge.py`: frozen-model verifier.

SHA-256:

- generated countermodel: `910d1eb36f0b027aafb4a1b07bacd509981053492541ee1365b815e02223411f`;
- frozen audit: `7ff3a15b31e6e06f96d440be2e750bb26816f9663c6c6c83dd11dc576b3d9669`;
- generator: `715feea61ea80db87ffd87c8884a9ce718e5f5f384c8ab3688306afa15098fd1`;
- audit script: `0be05f945ae9c3064d024d578f7cf0d02b0d341d6c9d6076b5922e6a25ddd083`.

Shortest replay:

```bash
PYTHONPATH=/private/tmp/efx-z3 python3 \
  tracks/parkability/audit_adaptive_root_order_bridge.py \
  --output /tmp/adaptive-root-order-audit.json
cmp results/alternating_adaptive_root_order_bridge_audit.json \
  /tmp/adaptive-root-order-audit.json
```

The counterexample is a SAT witness: its substantive claims are checked by
direct integer arithmetic and exhaustive enumeration, rather than relying on
an UNSAT certificate. The structural-cell membership check is independently
rebuilt from the frozen profile with Z3 5.0.0.

## Research consequence

The adaptive-order route has reached a clean stopping boundary:

- **closed:** canonical root selection is insufficient, even in the atom;
- **identified:** the smallest absent move is an anchored safe-subpacket
  suffix transfer;
- **now closed:** the cap-free anchored-suffix/two-safe packing lemma, by the
  reservoir threshold reversal; and
- **not useful:** more fixed-size cells or larger blind rival pools.

Accordingly, this counterexample is now a diagnostic rather than the live
gate. Root/order adaptation selects a half-turn, while the reservoir-exchange
lemma supplies the required suffix reallocation. The remaining EFX program
must move to the four hard orders whose external-observer candidate was
already exactly refuted.

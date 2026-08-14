# Terminal-path charity-placement bicriteria lemma

**Date:** 2026-08-14

**Status:** cap-free strengthening of the terminal compensator frontier;
two charity placements give a paid three-edge endpoint or nested exact
critical packets

## Terminal path and available charity

Use the terminal canonical path

```text
m -> y -> x -> q.
```

Let `C subseteq B_q` be the ordinary base-desired core for the missing owner
`m`, let `D subseteq B_x` be the final path core desired by `q`, and write

```text
Delta_i = v_i(B_i)-v_i(X_i) >= 0   for i != m,
theta = v_q(C)-Delta_q.
```

Core `C` alone strictly base-pays `m`. Therefore the positive singleton
charity good `p` need not be assigned to `m`; it can subsidize either side
of the `x -> q` compensator.

Because `C subseteq B_q`, `theta <= v_q(X_q)`. Since `D` is desired by `q`
above `B_q`, the complete packet `D` satisfies every threshold below.

## Placement Q: charity pays the terminal owner

Choose an inclusion-minimal packet `P_q subseteq D` satisfying

```text
v_q(P_q) >= theta-v_q(p),
```

using `P_q=empty` when the right side is nonpositive. Give `C` to `m`,
`P_q+p` to `q`, and retain every other good. The only possible unpaid owner
is `x`, and it is paid exactly when

```text
v_x(P_q) <= Delta_x.
```

On success the nonempty current-holder pairs are contained in

```text
q -> m:C,  x -> q:P_q,  charity -> q:p.
```

Thus the allocation uses at most three current-holder edges.

## Placement X: charity protects the predecessor

Choose an inclusion-minimal packet `P_x subseteq D` satisfying

```text
v_q(P_x) >= theta.
```

Give `C` to `m`, `P_x` to `q`, and `p` to `x`. Owner `x` is paid exactly
when

```text
v_x(P_x) <= Delta_x+v_x(p).
```

Again there are at most three current-holder edges:

```text
q -> m:C,  x -> q:P_x,  charity -> x:p.
```

## Nested critical-packet failure

Choose `P_x` first and then choose `P_q subseteq P_x` inclusion-minimal for
the lower threshold `theta-v_q(p)`; the full `P_x` always meets it. If both
placements fail, the nested packets satisfy

```text
P_q subseteq P_x subseteq D,
v_q(P_q) >= theta-v_q(p),
v_q(P_q-g) < theta-v_q(p)        for every g in P_q,
v_x(P_q) > Delta_x,
v_q(P_x) >= theta,
v_q(P_x-g) < theta               for every g in P_x,
v_x(P_x) > Delta_x+v_x(p).
```

Thus charity failure is not the single separator in the earlier terminal
lemma. It is the stronger statement that the packet frontier crosses both
corners of the charity-width rectangle: subsidizing the recipient still
overcharges the donor, and subsidizing the donor still undercompensates it.

## Relation to the earlier terminal lemma

`CANONICAL_PATH_BASE_RESPONSE_PREFIX_OR_TERMINAL_SPLIT_LEMMA_20260814.md`
sent `p` to `m`. That construction remains correct, but it is payment-wise
dominated because `C` already strictly pays `m`. The two placements above
strictly weaken its surviving terminal obstruction and should replace it in
subsequent arguments.

## Physical and theorem boundary

The displayed count is by current holder. Packets `C` and `P_q` or `P_x`
may mix several frozen-`Y` suppliers, so no four-edge physical-provenance
claim follows automatically.

Proved: exact payment identities, existence and nested minimality of the two
packets, the two at-most-three-current-holder-edge endpoints, and the
two-corner critical alternative. Not proved: contradiction of the critical
system from signed saturation, frozen-supplier compression, observer EFX
safety, decorated recurrence, the fixed-`U` theorem, or additive EFX.

# Paid-hole core trimming or double-capture lemma

**Date:** 2026-08-13

**Status:** cap-free reversal of every paid-hole endpoint failure unless one
item-critical packet captures the response source's full margin

## Setting

Use a three-edge near-perfect response matching from the three-matching hole
interface. Let `h` be its unmatched response source and assume `h` is already
weakly base-paid in the physical state:

\[
                         v_h(Y_h)\ge v_h(X_h).     \tag{1}
\]

Suppose target `h` supplies a desired common-safe core `O` to matched source
`k`. Write

\[
                   R=Y_h\setminus O,
       \qquad \mu_k=v_k(O)-v_k(X_k)>0.            \tag{2}
\]

The untrimmed matching candidate gives `R+P` to `h`. Its exact failure is

\[
                         v_h(R+P)<v_h(X_h).        \tag{3}
\]

## Minimal hole repair

Because `R+O=Y_h`, (1) and positivity imply

\[
                         v_h(R+P+O)>v_h(X_h).      \tag{4}
\]

Choose an inclusion-minimal packet `H subseteq O` such that

\[
                         v_h(R+P+H)\ge v_h(X_h).  \tag{5}
\]

It is nonempty by (3). Minimality makes every retained item critical:

\[
 v_h(R+P+H-g)<v_h(X_h)\qquad(g\in H).             \tag{6}

Retain `H` at target owner `h`, send only `O-H` to source `k`, and leave all
other matching transfers unchanged. This uses exactly the same physical
supplier-recipient pairs as the original near-perfect matching: retaining a
subpacket creates no edge. Charity still sends `P` to `h`, so the complete
allocation uses at most four edges.

Deleting `H` preserves common safety of the response core. Therefore, if

\[
                         v_k(O\setminus H)>v_k(X_k),              \tag{7}

then `O-H` remains a desired common-safe core for `k`. Equations (5) and (7)
pay both `h` and `k`; the other two matched sources remain strictly paid by
their unchanged cores. This gives an all-owner-paid complete candidate on at
most four edges.

If (7) fails, additivity yields the exact double-capture certificate

\[
                         v_k(H)\ge\mu_k.           \tag{8}

Thus the same nonempty physical packet `H` is simultaneously:

1. inclusion-minimal for repairing the target owner's payment deficit; and
2. large enough in the response source's row to capture the source's entire
   strict response margin.

No unnamed endpoint deficit remains.

## Application to rank three

The two replacement matchings at the fixed-U gate leave a represented owner
unmatched, so hypothesis (1) holds for that hole owner; the replaced selected
core is unused, so no disjointness from it is required. However, all *other*
matched sources must also be paid. This is automatic for the `d->q`
replacement because that `d` core is base-desired. It is not automatic for
the `d->r` replacement, whose strong-wall core may be only current-desired
while `d` lies below base.

Thus the lemma unconditionally produces the item-critical double-capture
packet for the `d->q` replacement. The same conclusion at target `r` is
conditional on a base-desired `d` core or a separate signed proof that the
current-only core pays `d`. Generalized PI-freeness likewise gives base-core
overlap capture unconditionally only at `q`. The selected matching may leave
sacrificed `d` unmatched; its survivor is the bare deficit
`v_d(Y_d+P)<v_d(X_d)`.

The active closure-or-transfer obligation is therefore sharper:

- one bare `d` deficit; and
- two item-critical packets, each valued above the full response margin of
  its displaced represented source.

If either trimmed response remains desired, the four-edge paid candidate is
immediate and observer failure enters the saturated decorated-response
machinery. Only simultaneous double capture survives.

## Boundary

This lemma is cap-free in goods, packet sizes, and values. It proves
conservation, payment, and preservation of the four-edge graph after
trimming. It does not prove observer safety, show that simultaneous
double-capture packets are disjoint or release-compatible, eliminate the
bare `d` deficit, or finish the universal theorem.

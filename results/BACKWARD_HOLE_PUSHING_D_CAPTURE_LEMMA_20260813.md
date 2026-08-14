# Backward hole-pushing `d`-capture lemma

**Date:** 2026-08-13

**Status:** cap-free compression of a near-perfect response path to an
all-owner-paid four-edge candidate or one item-critical `d`-margin capture

## Response-path geometry

Let a three-edge response matching on four owners have unique directed path

\[
 t_0\longrightarrow t_1\longrightarrow\cdots
 \longrightarrow t_k=h,                          \tag{1}
\]

from its unmatched owner target `t_0` to its unmatched response source `h`.
Other components, if any, are directed owner cycles. For each path edge
`t_j->t_{j+1}`, let

\[
 C_j\subseteq Y_{t_{j+1}}                       \tag{2}
\]

be the desired common-safe core assigned to source `t_j`.

Reverse every response edge and initially give charity `P` to `h`. Cycle
sources receive full desired cores and are strictly paid. Along the path,
only the unmatched source can initially lack an incoming desired core.

## Backward hole pushing

Process the path from `h=t_k` backward. Whenever `t_j` would be underpaid
after the core `C_{j-1}` is removed from its physical bundle, retain an
inclusion-minimal packet

\[
                         H_{j-1}\subseteq C_{j-1}                \tag{3}
\]

that pays `t_j` **without** charity, and send only `C_{j-1}-H_{j-1}` to
source `t_{j-1}`. Then move the complete charity packet from `t_j` to
`t_{j-1}`. Retention creates no transfer edge, trimming preserves common
safety, and charity still has exactly one recipient. Thus every intermediate
and final construction remains within the same three response pairs plus one
charity pair.

For every already-paid represented owner, the repair packet exists: retaining
all of `C_{j-1}` restores the complete current bundle `Y_{t_j}`, in addition
to any incoming packet, and hence reaches `v_{t_j}(X_{t_j})`. Inclusion
minimality makes every good in `H_{j-1}` critical for that owner's payment.

If the trimmed incoming core still pays its source, the hole disappears. If
not, the only underpaid source moves from `t_j` to its predecessor
`t_{j-1}`. Because (1) is a simple path, this process cannot revisit a
represented owner.

## Only possible terminal obstruction

Assume every represented owner is already paid and that the response core
received by sacrificed `d` is base-desired. The only owner for whom full
retention of its outgoing core need not repair payment is then `d` itself.
Therefore backward pushing has exactly two outcomes:

1. every owner is paid, giving a complete candidate through at most four
   support edges; or
2. the hole reaches `d` after the physical target of a desired `d`-core
   `D` retained a packet `H subseteq D`.

If `d` is internal to the path, pushing the charity farther requires paying
`d` without it. Failure after `d` retains its entire outgoing core is

   \[
        v_d(Y_d)+v_d(D\setminus H)<v_d(X_d).                    \tag{4}
   \]

Write `mu_d=v_d(D)-v_d(X_d)>0`. Rearranging (4) gives the strict capture

\[
                  v_d(H)>
                  \mu_d+v_d(Y_d)>mu_d.                         \tag{5}
\]

Hence the retained packet captures more than the complete strict response
margin of `D`; it also covers the value of `d`'s whole current bundle. The
packet is item-critical for paying the represented owner who retained it.

When `d` is the unmatched target `t_0`, it has no outgoing core to retain and
keeps the charity. The terminal test is instead

\[
        v_d(Y_d)+v_d(D\setminus H)+v_d(P)<v_d(X_d),             \tag{6}
\]

which strengthens (5) to

\[
        v_d(H)>\mu_d+v_d(Y_d)+v_d(P).                           \tag{7}
\]

Thus both positions force strict full-margin capture; R3 supplies the
additional charity term, while R2 needs only (5).

## Consequence for the two fixed-U forms

Replacing the selected core at target `q` by the ordinary base-desired
`d->q` core produces precisely such a path in each form:

- R2 gives a path in which `d` is internal and its predecessor is the paid
  unmatched target `s`;
- R3 gives a Hamiltonian path beginning at target-hole `d`.

The R2 geometry strengthens the generic internal bound. When the hole reaches
`d`, retain all of `d`'s outgoing core and leave charity at `d`; its
predecessor `s` remains paid from its unchanged current bundle even if it
receives no core. Thus R2 can fail only if

\[
        v_d(Y_d)+v_d(D\setminus H)+v_d(P)<v_d(X_d),             \tag{8}
\]

exactly as in R3. Both fixed-U forms therefore satisfy the uniform strict
capture

\[
        v_d(H)>\mu_d+v_d(Y_d)+v_d(P).                           \tag{9}
\]

Thus the endpoint-capture condition for the `d->q` replacement can be
replaced by one canonical certificate: an item-critical packet inside that
base-desired `d` core satisfying (9). Combined with generalized-PI
full-margin capture by the selected union, a saturated survivor has two
competing full-margin captures of this response—one forced by PI-freeness and
one forced by backward payment repair.

The second strong-wall edge `d->r` may be only current-desired. Since `d` is
below base, receiving such a core does not automatically pay it. The same
argument at target `r` is therefore conditional on a base-desired core or an
additional signed residual inequality. The unconditional remaining theorem
has one base-core uncrossing branch at `q` and one mixed current/base branch
at `r`.

**Nonsingleton-wall update.** The additional signed inequality is now
available without making the wall core base-desired. If `Q` is nonsingleton,
`v_d(W)>F_d/2`; inside `A` minus a least-`d` good there is a minimal
current-safe core `D` with `v_d(D)>v_d(W)`. Hence `W+D` base-pays `d`, and the
same backward walk terminates either paid or with
`v_d(H)>v_d(W)+v_d(D)+v_d(P)-F_d>v_d(P)`. See
`CURRENT_WALL_BACKWARD_HOLE_CAPTURE_LEMMA_20260813.md`. If `Q` is singleton,
the ordinary `d->q` packet itself is base-paying. Thus mixed-status owner
payment is closed; capture uncrossing and observer safety remain.

The remaining analytic step is to uncross those two captures. A disjoint
remainder gives generalized PI or a paid path; complete overlap must produce
a release-compatible repeated component or a four-edge rerouting.

## Boundary

This lemma proves termination of the payment-hole walk and its exact final
inequality when the matched `d` core is base-paying. It does not prove that
the resulting paid candidate is EFX, uncross the PI/payment captures, convert
the current-only `d->r` edge to a base-paying response, establish release
compatibility, or finish the active fixed-U theorem.

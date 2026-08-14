# R3 two-target root-path supplier-compatibility lemma

**Date:** 2026-08-14

**Status:** cap-free closure of the favorable Hall-matching shape to a
four-edge candidate; backward path, singleton star, and foreign import remain

## The residual support state

Use the nonrecruiting output of the root-star leaf-liquidation lemma.  In
roles `(x,y,z,d)`, where `x=r` is the strict root and `z` holds the singleton,
the only signed owner pairs are

\[
                         y\to x,\quad z\to x,
                         \quad z\to y,            \tag{1}
\]

and the charity pair is `charity -> z`.  The only possible nonrecruiting
failed-response targets are `x,y`; nonself response sources lie in `x,y,z`.

If both targets have response neighbors and Hall's condition holds, a
two-edge response matching has exactly one of three shapes:

\[
 y\to x, x\to y;\qquad
 y\to x, z\to y;\qquad
 z\to x, x\to y.                                \tag{2}
\]

The first is the internal two-cycle.  Its two desired cores lie in disjoint
targets; reversing them while retaining target residuals strictly improves
both sources, so it is the release-compatible PI exit.  The second is the
backward/root-loss path.  The third is the favorable root path.

## Favorable root path

Let `D_x subseteq B_y` be the root's desired core in target `y` and let
`D_z subseteq B_x` be the singleton holder's desired core in target `x`:

\[
 v_x(D_x)>v_x(B_x)>v_x(X_x),
 \qquad v_z(D_z)>v_z(\{p\}).                     \tag{3}
\]

Assume `D_z` is contained in the physical `z`-supplied cell currently held
by `x`.  Form

\[
\begin{aligned}
 Z_x&=(B_x\setminus D_z)\mathbin{\dot\cup}D_x,\\
 Z_y&=(B_y\setminus D_x)\mathbin{\dot\cup}\{p\},\\
 Z_z&=D_z,\\
 Z_d&=B_d.
\end{aligned}                                    \tag{4}
\]

This conserves all goods and empties charity.  The root is strict because
`Z_x` contains `D_x`, which alone is worth more than its previous bundle.
The singleton holder is strict because it receives `D_z`.

No new owner supplier pair is created.  Moving `D_x` from `y` to `x` uses
only the already present pairs `y -> x` and `z -> x`, because `B_y` contains
only `y`- and `z`-supplied support.  Moving `D_z` back to `z` can only delete
part or all of `z -> x`.  Parking `p` at `y` replaces `charity -> z` by
`charity -> y`.  Hence the final support is contained in

\[
 y\to x,\qquad z\to x,\qquad z\to y,
 \qquad charity\to y,                            \tag{5}
\]

and uses at most four packet-transfer edges for arbitrary packet sizes.

If (4) is EFX, it is the required strict-root lexicographic endpoint.  If it
is not EFX, globally minimal extraction supplies the next exact decorated
response at this explicit four-edge probe; a new record/progress/full-owner
response is handled by saturation, while an exact old record is the remaining
repeat gate.

## Exact residual classification

After the internal two-cycle and the favorable supplier-compatible root path
are removed, the two-target root-star survivor has only:

1. Hall failure, necessarily the singleton-source star `z -> {x,y}`;
2. the backward path `y -> x` and `z -> y`, whose first response removes support
   from the protected root and needs signed cancellation or anchor retention;
3. a favorable root path in which every usable `z -> x` core imports
   non-`z` support; or
4. an exact repeated decorated response at the candidate (4).

Thus the remaining physical obstruction is not arbitrary Hall deficiency.
It is root capture or indispensable foreign-support import by the singleton
holder, plus exact repeat closure.

## Claim boundary

Proved: the three matching shapes, internal-cycle PI, conservation, strict
root/source payment, and the four-edge supplier identity for the favorable
path.  Not proved: observer safety of (4), closure of its exact response
repeat, the backward path, the singleton star, contradiction of foreign
support import, the later-source anchor separator, fixed-`U`, or general EFX.

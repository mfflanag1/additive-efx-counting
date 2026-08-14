# R3 root-star different-source leaf-liquidation lemma

**Date:** 2026-08-14

**Status:** cap-free four-edge reduction of the first different-source
continuation to a two-target represented residual or full-owner recruitment

## Input after root-source double absorption

Use the represented `R3` star whose common source is the first-priority root
`x=r`.  After completing both incoming matching packets and absorbing the
two star targets, the exact signed-support identity of
`R3_REPRESENTED_STAR_DOUBLE_ABSORPTION_LEMMA_20260814.md` leaves only

\[
                         y\to x,\qquad z\to x,    \tag{1}
\]

among owner-transfer pairs, where `{y,z}={q,s}`.  Let the nonempty residual
bundles at those targets be `R_y,R_z`; target exhaustion is a separate strict
support-consumption exit.  The unmatched owner `d` is unchanged.  The
positive singleton `p` is parked at one of `y,z` by the double-absorption
probe.  Write `P_y` for `{p}` when it is at `y` and the empty packet
otherwise.

The root retains its permanent desired anchor, so

\[
                         v_x(B_x)>v_x(X_x).        \tag{2}
\]

Suppose the first response not sourced by `x` is, without loss of generality,
a represented response by `y` into the other residual.  After the separately
proved singleton-hit descent it may be taken disjoint from `p`, so some
nonempty `F subseteq R_z` satisfies

\[
                         v_y(F)>v_y(R_y+P_y).      \tag{3}
\]

## Liquidate the response target

Positivity and `F subseteq R_z` imply

\[
                         v_y(R_z)>v_y(R_y+P_y).    \tag{4}
\]

Give the **whole** residual `R_z` to `y`, and give `p` to the now empty target
`z`.  Leave `x,d`, and `R_y` unchanged.  The resulting complete allocation is

\[
 (B_x,\ R_y+R_z,\ \{p\},\ B_d)                  \tag{5}
\]

in role order `(x,y,z,d)`.  Relative to the original saturated support state,
its only possible supplier pairs are

\[
 y\to x,\qquad z\to x,\qquad z\to y,
 \qquad charity\to z.                            \tag{6}
\]

Hence (5) uses at most four packet-transfer edges, independently of the
sizes of `R_y,R_z`.  Owner `y` strictly improves from the absorbed probe by
(4), even when it releases `p`: the whole packet `R_z` alone exceeds its
former bundle `R_y+P_y`.  The root remains strictly above its GG base by (2).

## Failure localization

If (5) is EFX, its strict root makes it the required lexicographic endpoint.
Otherwise extract a globally minimum failed response at the actual final
utilities.

The singleton target `{p}` owned by `z` cannot be an EFX-failure target:
deleting its only good leaves value zero, while every owner has positive
utility.  Therefore every failed response has target in `{x,y,d}`.

If its source or target is `d`, adjoining it to the already connected
represented component recruits all four owners and enters the full-owner
decorated continuation.  Otherwise its source lies in `{x,y,z}` and its
target lies in `{x,y}`.  Thus the sole non-recruiting survivor is an exact
**two-target represented residual**.  The former arbitrary different-source
continuation, and the whole target `z`, are eliminated.

The symmetric statement holds when `z` is the first different source and
`R_y` is liquidated.

## Consequence and boundary

The root-source represented star cannot terminate at an untyped different
old source.  It yields one of:

1. target exhaustion/support progress;
2. a complete four-edge EFX/lex endpoint;
3. full-owner recruitment; or
4. a decorated response supported on only the two represented targets
   `{x,y}` (symmetrically `{x,z}`).

This lemma proves conservation, strict-root preservation, source payment,
the four-edge identity, and failure localization.  It does not close the
two-target represented residual, prove the full-owner base-margin interface,
handle the later-source anchor-capture stars, finish fixed-`U`, or prove
four-agent/general additive EFX.

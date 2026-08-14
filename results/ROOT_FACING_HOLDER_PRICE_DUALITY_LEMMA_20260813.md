# Root-facing holder-price duality lemma

**Date:** 2026-08-13

**Status:** cap-free identification of the root-surplus loss band with the
general holder-compensation separator

## Exact root split

Let the globally maximal base give the first-priority root value `x>0`.
At a root-facing survivor let the current root target be

\[
H=D\mathbin{\dot\cup}C,
\qquad
v_r(H)=x+\delta,
\qquad
\delta>0,                                        \tag{1}
\]

where `D` is a globally minimum current-safe response.  Let `R` be any
physically released packet disjoint from `C` and `D` that is admissible for
the root under the signed supplier record.

If `D` is assigned to its response source and the root receives `C+R`, then

\[
v_r(C+R)-x
 =\delta-v_r(D)+v_r(R).                           \tag{2}
\]

Define the root compensation price

\[
\pi_r(D)=\max\{0,v_r(D)-\delta\}.                 \tag{3}
\]

Equation (2) gives the exact thresholds:

\[
v_r(C+R)\ge x
 \iff v_r(R)\ge v_r(D)-\delta,                    \tag{4}
\]

and strict inequality holds on both sides simultaneously.  Equality in
(4) preserves only the base root floor and must retain the equality-critical
observer audit; it is not silently called a strict root improvement.

## Identity with the holder release price

Treat the root as the holder of transferred packet `D`, with current bundle
`H`, required floor `x`, and slack

\[
\sigma_r=v_r(H)-x=\delta.
\]

The general holder price is therefore

\[
p_r(D)=\max\{0,v_r(D)-\sigma_r\}
      =\max\{0,v_r(D)-\delta\}
      =\pi_r(D).                                  \tag{5}
\]

Thus the root-facing loss band is an instance of the same physical payment
gate as the whole-packet holder wall, not an independent scalar obstruction.

## Price in the surviving band

Inside the root-surplus band

\[
\delta\le v_r(D)\le x,                            \tag{6}
\]

the price is nonnegative and bounded:

\[
0\le\pi_r(D)=v_r(D)-\delta\le x-\delta.          \tag{7}

Any admissible `R` strictly above this price gives a strict-base controlled
root release.  Failure of every such `R` is the exact root-row holder-price
separator.  If `v_r(D)>x`, root-high reselection applies instead; if
`v_r(D)<delta`, the unassisted complement is already strictly above `x`.

## Claim boundary

This lemma proves the price identity, compensation threshold, and bounded
separator.  It does not guarantee that an admissible released packet exists,
promote weak equality to a strict endpoint, pay other observer rows, close
the atomwise whole-packet or safe-payment normalization walls, close
`T_{L,times}^*`, or prove four-agent/general EFX.


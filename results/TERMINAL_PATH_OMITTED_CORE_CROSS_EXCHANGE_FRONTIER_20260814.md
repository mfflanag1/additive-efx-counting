# Terminal-path omitted-core cross-exchange frontier

**Date:** 2026-08-14

**Status:** cap-free closure of two of the four terminal role maps whenever
the omitted core uncrosses from the missing owner's base response; failure is
one exact shared-target capture

## Terminal path

Use a terminal instance of the canonical fixed-role path

\[
                    m\longrightarrow y\longrightarrow x
                     \longrightarrow q,          \tag{1}
\]

where `m=d` is the missing source and `q` is the ordinary base-response
target.  Let

\[
 C\subseteq B_q,qquad v_m(C)>v_m(X_m)           \tag{2}
\]

be the ordinary `m->q` core, and let

\[
 D\subseteq B_x,qquad v_q(D)>v_q(B_q)           \tag{3}
\]

be the final path core.  The omitted duplicate-target response supplies a
second core `E subseteq B_q`, desired either by `x` or by `y`.

Among the four terminal fixed-role maps, the omitted source is `x` in
exactly two and `y` in exactly two.

## Predecessor-duplicate cross exchange

Suppose the omitted core is desired by `x`.  If `E\setminus C` contains a
common-safe desired subcore `E'` for `x`, form

\[
\begin{aligned}
 Z_m&=B_m+C+p,\\
 Z_x&=(B_x\setminus D)+E',\\
 Z_q&=(B_q\setminus(C\cup E'))+D,
\end{aligned}                                     \tag{4}
\]

and leave `y` unchanged.

Owner `m` is strictly base-paid by `C`; owner `x` is strictly paid by `E'`;
owner `q` is strictly paid by `D`; and `y` remains weakly base-paid.  The
only current-holder pairs are

\[
              x\to q:D,qquad q\to x:E',qquad
              q\to m:C,qquad charity\to m:p.    \tag{5}
\]

Thus (4) is an all-owner-paid complete four-edge candidate with unrestricted
packet sizes.  At mixed later states, each displayed packet can still induce
several frozen-`Y` supplier pairs; (5) is a current-holder count.

If no desired subcore remains in `E\setminus C`, let `F_x` be the response
floor and `mu_x=v_x(E)-F_x>0`.  Then

\[
 v_x(E\setminus C)\le F_x,qquad
 v_x(E\cap C)\ge\mu_x.                           \tag{6}

\]

So failure is exactly full-margin capture of the omitted predecessor's
response inside the missing owner's base-paying core.

## First-source duplicate

If `E` is desired by `y`, the analogous uncrossed exchange pays `y`, but
owner `x` still has to release a compensator to terminal `q`.  It therefore
returns to the terminal bicriteria packet of
`CANONICAL_PATH_BASE_RESPONSE_PREFIX_OR_TERMINAL_SPLIT_LEMMA_20260814.md`.
Failure to uncross `E` again gives (6) with source `y`.

## Exact reduction

The four terminal maps therefore divide into:

1. two predecessor-duplicate maps: a four-edge paid cross exchange or one
   shared-target capture packet;
2. two first-source-duplicate maps: the terminal bicriteria split, together
   with the same disjoint-or-capture alternative at `q`.

## Claim boundary

Proved: the `2+2` role split, conservation and payment of the uncrossed
predecessor exchange, its four current-holder edges, and the exact overlap-
capture inequality.  Not proved: reversal of the capture, elimination of the
remaining two terminal split gates, frozen-supplier compression, observer
EFX safety, or the fixed-`U` theorem.

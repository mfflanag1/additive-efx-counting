# Forced-`GGS` off-good response PI reduction theorem

**Date:** 2026-08-14

**Supersession (2026-08-14):** this is a conditional diagnostic. The full
anchored `GG` collision is already contradicted before the response-profile
stage.

**Status:** cap-free closure of every off-good response sourced by `q` and one
additional singleton-source orientation; three external-source off-good
profiles and all on-good profiles remain

## Forced `GGS` roles

The singleton-source elimination theorem leaves source pair `{c,q}`, with
singleton non-source `s`. Let `a in {c,q}` be the unique ordinary envier of
`s`, and let `b` be the other source. The forced cycle is

\[
 b\xrightarrow{G}a\longrightarrow s\xrightarrow{G}b. \tag{1}
\]

Thus there are exactly two role orientations:

\[
\begin{array}{c|ccc}
a & b\xrightarrow{G}a & a\to s & s\xrightarrow{G}b\\
\hline
c & q\xrightarrow{G}c & c\to s & s\xrightarrow{G}q\\
q & c\xrightarrow{G}q & q\to s & s\xrightarrow{G}c.
\end{array}                                      \tag{2}
\]

The original `GG` flower retains the genuine edge

\[
 r\xrightarrow{G}q.                             \tag{3}
\]

## Off-good response

Suppose the charity-reset whole-`K` response is off-good:

\[
 D=X_r-L,
 \qquad L\subseteq X_r-K,                       \tag{4}
\]

with named nonroot source `i`. Since `D subseteq X_r` is strictly desired by
`i`, additivity gives the ordinary envy edge

\[
 i\longrightarrow r.                            \tag{5}
\]

### Response source `q`

For either row of (2), (5) and (3) form

\[
 q\longrightarrow r\xrightarrow{G}q.
\]

This cycle has exactly one genuine edge, consumes only the charity packet on
that edge, and is a basic release-compatible PI cycle. Hence `i=q` is
impossible.

### Ordinary source `a=q` and response source `s`

In the second row of (2), combine

\[
 r\xrightarrow{G}q\longrightarrow s\longrightarrow r.
\]

Again there is exactly one genuine edge, so this is PI. Hence when `a=q`, the
only off-good response source that survives is `i=c`.

### Exact off-good survivors

The one-genuine-cycle test leaves precisely

\[
 (a,i)\in\{(c,c),(c,s),(q,c)\}.                 \tag{6}
\]

These profiles have two genuine edges on the shortest evident closing cycle;
both consume `f`, so the same argument cannot declare them PI.

## On-good boundary

For an on-good response

\[
 D=(X_r-L)+f,
 \qquad v_r(L)>v_r(f),                           \tag{7}
\]

the response edge into `r` itself consumes `f`. Combining it with (1) or (3)
therefore uses at least two overlapping `f`-edges. No on-good source is closed
by the present PI test.

## Claim boundary

This theorem closes the stated off-good source profiles by explicit
one-genuine-edge PI cycles and leaves the exact set (6). It does not make
overlapping `f`-edges release-compatible, eliminate (6) or (7), use the
retirement supplier or debt cycle, close `T_{L,times}^*`, GG, four-agent EFX,
or general additive EFX.

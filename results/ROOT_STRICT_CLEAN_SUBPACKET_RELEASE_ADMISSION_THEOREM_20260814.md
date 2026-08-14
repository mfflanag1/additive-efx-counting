# Root-strict clean subpacket-release admission theorem

**Date:** 2026-08-14

**Status:** cap-free admission of every strictly root-paying packet or
subpacket release; its equality face is separately eliminated by the
base-restoration packet-spread theorem

**Composition update.**  This theorem alone deliberately retains equality.
`ROOT_EQUALITY_BASE_RESTORATION_PACKET_SPREAD_ADMISSION_THEOREM_20260814.md`
uses nondegeneracy and the GG base support to turn every admitted equality
mode into a strict packet-spread move.

## Exact input

Let an exact `T_{L,times}^*` state have first-priority root `r` with

\[
 Z_r=K\mathbin{\dot\cup}H,
 \qquad v_r(Z_r)=x+\delta,
 \qquad \delta>0,                               \tag{1}
\]

where `x=v_r(X_r)` and `K` is the named nonempty retired packet.  Let
`u != r` be its named historical recipient.  Choose a nonempty
`T subseteq K` and a currently compatible, supplier-closed, `K`-free
exterior packet `R`.  Compatibility includes canonical normalization of
every other retired packet; this theorem does not move such a packet merely
because it lies in an exterior bundle.

## Clean controlled-release allocation

Form a complete physical candidate as follows:

\[
 Z'_r=(K-T)+H+R,
 \qquad Z'_u=T.                                 \tag{2}
\]

Every exterior donor keeps the complement of its contribution to `R`.
Every other nondisor keeps its current target.  Move the displaced old
bundle of `u`, and every unused donor residual that its existing target rule
does not retain, to charity.  Thus `u` is explicitly the sacrificed later
owner; the proof does not claim that historical provenance makes the old
transfer reversible.

All goods have one destination.  The packet edge is supplied by its current
holder `r`, every exterior piece keeps its current supplier, and no PI edge
is declared.  Consequently (2) is a controlled root/anchor release candidate
with an exact signed release record, rather than an inferred `G0--G10`
historical reversal.

The root margin is exactly

\[
 v_r(Z'_r)-x=\delta-v_r(T)+v_r(R).              \tag{3}
\]

Hence the candidate is root-strict when

\[
 v_r(R)>v_r(T)-\delta.                          \tag{4}
\]

## Packet reduction after every failed EFX test

If (2) is EFX under (4), its first-priority root value exceeds `x`, contrary
to global lexicographic maximality.  Otherwise extract a globally
minimum-cardinality desired response at the actual candidate.

The only targets meeting `K` are

\[
 K\cap Z'_r=K-T,
 \qquad K\cap Z'_u=T.                           \tag{5}
\]

If `T` is proper, each intersection in (5) is proper, so every response has
zero or proper `K`-intersection.

If `T=K`, the root target avoids `K` and `u` owns exactly `K`.  A target
equal to a singleton cannot be strongly envied under positive valuations.
For a multigood target, any EFX wall against `K` supplies a desired deletion
`K-g`; therefore the globally minimum response inside that target is a
proper subset of `K`.  All responses against other targets avoid `K`.

Thus every non-EFX strict candidate has an actual response with strictly
smaller packet intersection.  Adopting that tested response is outcome 4 of
the charge-or-anchor contract.  The allocation itself records controlled
anchor release; no history-only label is counted as progress.

## Exact survivor

Let `mathfrak R_T` be the complete family of currently admitted compatible
exterior modes for `T`.  If no permitted outcome occurs, then

\[
 \max_{R\in\mathfrak R_T}v_r(R)
 \le v_r(T)-\delta
 \qquad(\varnothing\ne T\subseteq K).           \tag{6}
\]

For any exterior family common to all singleton releases, with
`M_r=max_R v_r(R)`, (6) yields the valid weak atomwise charge

\[
 v_r(g)\ge\delta+M_r\qquad(g\in K).             \tag{7}
\]

Summing and using `v_r(K)<=x+delta` gives

\[
 (|K|-1)\delta+|K|M_r\le x.                    \tag{8}
\]

## Equality boundary

When equality holds in (4), the root returns exactly to base.  The clean
candidate sacrifices `u`, so fixed-priority improvement is not automatic.
Keeping `u`'s old bundle can remove that loss, but other owners in the
current state need not all meet their base-priority coordinates.  Therefore
neither proper donor-free equality nor whole-packet equality is closed by
this theorem without an additional prefix-payment premise.

In particular, (6)--(8) are weak inequalities.  The earlier claimed
universal sharpening `v_r(g)>delta` is withdrawn.

## Claim boundary

This theorem supplies the missing transition admission for every strict
packet/subpacket return, proves proper packet-response reduction, and
establishes the weak atomwise exterior-pool charge.  It does not close root
equality, prove a positive common-pool lower bound, normalize an incompatible
second retired packet, close `T_{L,times}^*`, GG, four-agent EFX, or general
additive EFX.

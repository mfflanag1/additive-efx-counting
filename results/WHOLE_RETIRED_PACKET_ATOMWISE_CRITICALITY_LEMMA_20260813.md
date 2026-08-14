# Whole retired-packet atomwise criticality lemma

**Date:** 2026-08-13

**Status:** cap-free proper-packet reduction for strict capture; the surviving
whole packet is atomwise margin-critical

## Exact strict-capture input

Let the strict colliding candidate for recipient `s` be

\[
A=B\mathbin{\dot\cup}K,
\qquad
\mu=v_s(A)-F_s>0,
\qquad
d=F_s-v_s(B)>0.                                  \tag{1}
\]

Then

\[
v_s(K)=\mu+d.                                    \tag{2}
\]

Deletion of goods from the candidate preserves target safety.  Each proper
subpacket candidate is still subjected to the complete holder-payment,
observer, and release audit; the lemma does not declare a scalar candidate
executed.

## Proper-packet reduction

For any good `g in K`,

\[
v_s(B+K-g)-F_s=\mu-v_s(g).                       \tag{3}
\]

If `v_s(g)<mu`, the right-hand side is positive.  Thus `B+K-g` is a strict,
safe candidate whose collision packet is the proper subset `K-g`.  Its
successful canonical processing strictly reduces the named collision
packet; any failure carries a strictly smaller packet into the corresponding
typed floor/payment/release separator.

Consequently a whole-packet recurrence in which every proper collision has
already been exhausted must satisfy

\[
v_s(g)\ge\mu\qquad(g\in K).                       \tag{4}
\]

## Multiplicity charge

Summing (4), then using (2), gives

\[
|K|\mu\le v_s(K)=\mu+d,
\qquad
(|K|-1)\mu\le d.                                 \tag{5}
\]

This is a packet-size-independent inequality, not a bounded valuation-cell
argument.  Two immediate consequences are:

- if `mu>d`, then `|K|=1`;
- more generally, a survivor with `|K|>=q+1` has `q mu<=d`.

Thus strict capture either exposes a proper retired subpacket for exact
processing or localizes survivor A to an atomwise-critical packet with the
quantitative charge (5).  Equality-critical capture (`mu=0`) receives no
size information from this argument and remains separately typed.

## Claim boundary

The lemma proves the exact deletion identity, proper-packet candidate, and
atomwise/multiplicity charge.  A failed smaller-packet candidate must still
be routed through its physical holder and supplier closure; the inequality
does not pay that holder.  It does not eliminate an atomwise-critical packet,
close equality/base-debt/release branches, close `T_{L,times}^*`, or prove
four-agent/general EFX.


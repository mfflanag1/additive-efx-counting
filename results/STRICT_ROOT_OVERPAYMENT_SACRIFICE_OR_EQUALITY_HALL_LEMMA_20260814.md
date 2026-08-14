# Strict root overpayment sacrifice or equality-Hall lemma

**Date:** 2026-08-14

**Status:** cap-free elimination of joint recipient payment whenever a split
has a strictly overpaying root-compensation packet

## Exact root split

Let protected holder `h=r` be the first-priority root. Write

\[
v_r(Y_r)=x+\delta,
\qquad
\delta>0,                                        \tag{1}
\]

where `x` is the globally maximal base root value. For a nonempty proper
retired-packet split `K=T dot-union U`, transferring `T` away gives root
release price

\[
b_r(T)=\max\{0,v_r(T)-\delta\}.                 \tag{2}
\]

Let `R` be a physically compatible supplier-closed packet, disjoint from
`K` and retained protected support, that is assigned to the root.

## Strict-overpayment branch

The root's exact post-transfer margin over the base is

\[
v_r(Y_r-T+R)-x
 =\delta-v_r(T)+v_r(R).                          \tag{3}
\]

Inside the surviving root loss band `v_r(T)>delta`, equation (3) gives

\[
v_r(Y_r-T+R)>x
\iff
v_r(R)>b_r(T).                                   \tag{4}
\]

Suppose (4) holds. Give `T` to the colliding recipient, leave `U` with the
root, and give `R` to the root. Do **not** require the recipient to retain
her auxiliary floor; she is a later designated sacrifice. Other nonroot
donors may also lose auxiliary floors. The complete EFX and supplier audit
is still performed.

If the result is EFX, (4) makes it a strict first-priority lexicographic
improvement. If it is not EFX, extract a globally minimum response at the
actual allocation. Since `T` and `U` are in different targets, every retired
hit lies in a proper subset of `K`. A supplied cycle is PI; an outside
supplier or new response coordinate is rank/component progress; a
ledger-free root-star wall enters the existing external-star ascent or root
price routing. Thus a strictly overpaying root packet eliminates the need
for a simultaneous recipient top-up.

## Equality-Hall terminal

Consequently, after strict-overpayment routing, a protected-root split can
remain in the two-creditor Hall obstruction only if either:

1. no compatible root-payment packet reaches `b_r(T)`; or
2. every surviving compatible root-payment packet is equality-critical:
   \[
   v_r(R)=b_r(T).                                 \tag{5}
   \]

In branch 2 the root finishes exactly at `x`. A recipient packet is then
needed for the typed floor/priority handoff, and joint incompatibility is a
genuine equality-Hall face rather than a generic packing failure.

The strict/equality scalar obstruction in the two-creditor theorem realizes
(5) exactly, confirming that weak payment cannot be promoted without a
separate priority-valid operation.

## Typed branches

- **Strict capture:** `mu>0` does not by itself make root payment strict;
  the remaining difficulty may still be equality (5) in the root row.
- **Equality capture:** both recipient and root can be equality-critical;
  no strict endpoint is inferred.
- **Base-floor debt:** all nonroot auxiliary floors may be waived only
  because the first-priority root is strict in (4). No root debt is waived.
- **Release:** `R` is used only after supplier closure. Any incompatible
  packet remains in the Hall cut.

## Claim boundary

This lemma proves the exact root margin identity and priority-valid sacrifice
under strict root overpayment. It does not force a root-paying packet,
eliminate exact equality (5), prove every downstream root-star wall closes,
eliminate the equality-Hall terminal, close `T_{L,times}^*`, or prove
four-agent/general EFX.


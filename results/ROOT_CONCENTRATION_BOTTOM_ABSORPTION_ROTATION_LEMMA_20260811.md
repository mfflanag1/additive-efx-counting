# Root-concentration bottom-absorption rotation lemma

**Date:** 2026-08-11

**Status:** cap-free conversion of the third-owner fork's aggregate root-
concentration branch; response/Hall termination with retained bottom support
remains open

## Full-capture support

Use the full-capture `GG` flower notation

\[
 X_r=T_r\mathbin{\dot\cup}B_r,
 \qquad X_q=T_q\mathbin{\dot\cup}B_q,
\]

with a nonempty captured bottom packet

\[
 \varnothing\ne H\subseteq B_r.                   \tag{1}
\]

The live mutual edges give

\[
 v_r(T_q+f)>v_r(X_r),
 \qquad v_q(T_r+f)>v_q(X_q),                        \tag{2}
\]

and the bottom polarity gives

\[
 v_q(B_q)>v_q(f).                                   \tag{3}
\]

The aggregate root-concentration certificate from a failed third-owner
replacement may strengthen (1), but the construction below needs only the
physical support and (2)--(3).

## Bottom-absorption rotation

Define

\[
 Y_r=T_q+f+H,
 \qquad Y_q=T_r+B_q,
 \qquad Y_c=X_c,
 \qquad Y_s=X_s,                                    \tag{4}
\]

and leave

\[
 P_Y=B_r\setminus H                                \tag{5}
\]

as charity. These bundles partition all goods.

The root strictly improves by (2) and positivity. For `q`, subtract (3) from
the second inequality in (2):

\[
 v_q(T_r)>v_q(T_q)+v_q(B_q)-v_q(f)>v_q(T_q),
\]

so

\[
 v_q(T_r+B_q)>v_q(T_q+B_q)=v_q(X_q).               \tag{6}
\]

Both external owners are unchanged.

## Charity and wall localization

Every observer dominates the charity. Choose any `h in H`; base EFX against
`X_r` gives

\[
 v_i(X_i)\ge v_i(X_r-h)
 \ge v_i(B_r\setminus H).                          \tag{7}
\]

The external targets are unchanged. Every changed observer is weakly better
than at the base, so no new wall can point to an unchanged target. Therefore
every EFX failure of (4)--(5) points to exactly one of

\[
 T_q+f+H
 \quad\text{or}\quad
 T_r+B_q.                                           \tag{8}
\]

A globally minimal desired subset of a failed target is common-safe and
supplies a named response source. The root target retains the permanent core
`T_q+f`; the `q` target records the complete opposite mutual replacement.
Thus an EFX endpoint is a strict lexicographic improvement, an internal SDR
is tested for release compatibility, and every survivor is an explicit
owner-growth or Hall boundary on the two changed targets.

## Retained-bottom consequence

Operation (4) is the exact alternative to returning `H` through an
underfunded third-owner fork: keep the root-expensive packet at the root and
route the opposite mutual top to `q`. Record

\[
 V'=V\cup H\subseteq B_r                            \tag{9}
\]

as absorbed bottom support. If `H` contains a good not previously in `V`,
this is strict finite support growth. At fixed `V`, the universal retained-
bottom reset records in `S subseteq V` every live bottom good consumed by a
disjoint retained response core. Such a reset preserves support, strictly
grows `S`, or captures the remaining root response margin. The proof may not
treat a packet contained in `V` as newly absorbed.

This shows why retained top support `U` alone is insufficient at the final
fork. The smallest additional combinatorial coordinate is the nested pair
`(V,S)`: bottom support absorbed by (4), and the portion later committed to
retained response cores.

## Verification and boundary

[`root_concentration_bottom_absorption_rotation_audit.json`](root_concentration_bottom_absorption_rotation_audit.json)
checks support conservation, both strict mutual improvements, charity
dominance, and exact wall localization symbolically.

This lemma converts aggregate root concentration to a canonical partial
allocation and a finite bottom-support update. Together with the universal
retained-bottom reset, only the support-disjoint repeated-bottom Hall state
and reverse-support component remain. It does not terminate either state,
close every donor choice, close `GG`, or prove four-agent/general additive
EFX.

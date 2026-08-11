# Captured-q-margin anchored residual-rotation lemma

**Date:** 2026-08-11

**Status:** cap-free conversion of terminal q-margin capture; termination of
the resulting evolved-target response/Hall boundary remains open

## Retained payment packet

Use the removed-top retention potential with nonempty

\[
 U\subseteq T_r.
\]

The live flower polarity gives

\[
 v_q(T_r)>v_q(T_q).                                  \tag{1}

If `v_q(U)>v_q(T_q)`, put `K=empty`. Otherwise choose an inclusion-minimal
packet

\[
 K\subseteq T_r\setminus U
\]

such that

\[
 v_q(U+K)>v_q(T_q).                                  \tag{2}

Existence follows from (1). Put

\[
 L=U+K,
 \qquad R=(T_r\setminus L)+B_r.                      \tag{3}

## Anchored residual rotation

Assign

\[
 Y_r=T_q+f,
 \qquad Y_q=B_q+L,
 \qquad Y_c=X_c,
 \qquad Y_s=X_s,
\]

and leave `R` as charity. The earlier root strictly improves because
`T_q+f` is her desired mutual core. Equation (2) makes the later mutual
owner strictly improve:

\[
 v_q(B_q+L)>v_q(B_q+T_q)=v_q(X_q).                  \tag{4}

Every owner dominates the charity packet. Choose any `ell in L`. Base EFX
against `X_r` gives, for every observer `i`,

\[
 v_i(X_i)\ge v_i(X_r-\ell)\ge v_i(R).                \tag{5}

The root target is common-safe and the two external targets are unchanged.
Therefore exactly one of the following occurs:

1. `Y` is EFX with charity and closes the flower;
2. some observer in `{r,c,s}` strongly envies the sole evolved target
   `B_q+L`, producing the existing `(L|T_q)` response/Hall component.

No other EFX or charity wall is possible.

## Potential compatibility

Update the retained removed support from `U` to `L`.

- If `K` is nonempty, then `U` grows strictly before the response boundary
  is entered.
- If `K` is empty, the already retained packet itself pays the full
  `T_q` replacement. The proof no longer needs to restore the q-oriented
  mutual core: it remains in the residual-rotation/response-Hall branch.

Thus terminal failure of `D(U)` to remain desired never resets the global
potential. It either forces a fresh support increase or canonically changes
to the evolved-target component with all of `U` still removed.

For nonempty `K`, minimality also records

\[
 v_q(U+K-k)\le v_q(T_q)
 \qquad(k\in K),                                     \tag{6}

so every newly added good is payment-critical relative to the retained
packet.

## Verification and claim boundary

[`captured_q_margin_anchored_residual_rotation_audit.json`](captured_q_margin_anchored_residual_rotation_audit.json)
checks both-owner improvement, charity containment, strict support growth,
and the relative minimality certificate.

This lemma converts q-margin capture but does not eliminate the resulting
evolved-target wall, prove its response relation has an SDR, terminate an
unsafe/root-sourced continuation, close `GG`, or prove four-agent/general
additive EFX.

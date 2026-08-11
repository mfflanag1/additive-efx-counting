# Paid-anchor disjoint-recapture dichotomy

**Date:** 2026-08-11

**Status:** cap-free reduction of represented-source recapture to a paid
disjoint pivot, unsafe augmentation, or an exact paid-anchor hitting set;
termination of the two strict polarities remains open

## Protected paid anchor

After omitted-hole compression, the missing owner `d` holds

\[
 W=Y_d\mathbin{\dot\cup}R,                         \tag{1}
\]

where `Y_d` is her entire target from the paid pre-compression splice. Hence

\[
 v_d(Y_d)\ge v_d(X_d).                             \tag{2}
\]

Every represented source `i` holds a pairwise-disjoint common-safe desired
core `A_i`. Suppose a represented source `i` responds to `W`.

## Disjoint response branch

If `R` contains a common-safe desired core `D` for `i`, recapture it:

\[
 Z'_i=D,
 \qquad
 Z'_d=A_i+(W\setminus D).                          \tag{3}
\]

Because `D subseteq R`, the new residual still contains all of `Y_d`.
Therefore

\[
 v_d(Z'_d)\ge v_d(Y_d)\ge v_d(X_d),                \tag{4}
\]

independently of the ordinary recapture inequality
`v_d(D)-v_d(A_i)<=v_d(W)-v_d(X_d)`. Source `i` is strict, every other
represented source is unchanged and strict, and the hole remains paid.

Choose the original paid-anchor compression globally maximizing `v_d(W)`
over this fixed owner/support family. If (3) does not close by EFX or an
internal response SDR, maximality and nondegeneracy force

\[
 v_d(D)>v_d(A_i).                                  \tag{5}
\]

Indeed the reverse strict inequality would make the new paid residual in
(3) strictly more valuable to `d`, while equality between distinct supports
is excluded.

## No disjoint common-safe response

Suppose `R` contains no common-safe desired core for `i`.

1. If `v_i(R)>v_i(X_i)`, choose an inclusion-minimal desired subset
   `D subseteq R`. It is not common-safe and therefore supplies the existing
   unsafe-core response augmentation.
2. If `v_i(R)<=v_i(X_i)`, let `C subseteq W` be any desired response core for
   `i`. Additivity gives
   \[
   \begin{aligned}
   v_i(C\cap Y_d)
     &=v_i(C)-v_i(C\cap R)\\
     &\ge v_i(C)-v_i(R)\\
     &\ge v_i(C)-v_i(X_i)>0.                       \tag{6}
   \end{aligned}
   \]
   Thus the protected paid target captures at least the entire strict
   response margin. This is an exact hitting-set packet, not an untyped
   recapture failure.

The three branches—paid disjoint recapture with polarity (5), unsafe
augmentation, and paid-anchor capture (6)—are exhaustive.

## Consequence

Recompression after a paid bottom-tail splice cannot lose payment and cannot
hide a response in an arbitrary residual. Every surviving response either
preserves the entire paid anchor, augments the response relation, or consumes
the paid anchor by a margin-covering packet. The live recurrence is therefore
the interaction of the strict `d`-order (5) with the cross-row hitting set
(6); ordinary residual-payment failure has disappeared.

## Verification and boundary

[`paid_anchor_disjoint_recapture_dichotomy_audit.json`](paid_anchor_disjoint_recapture_dichotomy_audit.json)
checks support conservation, anchor containment, automatic hole payment,
the residual-maximality polarity, and the hitting-set inequality symbolically.

This lemma does not reverse (5) or (6), prove every unsafe augmentation grows
rank before returning, close a repeated anchor-consuming component, close GG,
or prove four-agent/general additive EFX.

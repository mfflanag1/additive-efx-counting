# Flower residual-wall payment polarity lemma

**Date:** 2026-08-10

**Status:** cap-free analytic payment theorem; simultaneous external payment
and Hall-deficient termination remain open

## Statement

Use the minimal-payment residual rotation

\[
Y_r=T_q+f,
\qquad
Y_q=W=B_q+L,
\qquad
R=(T_r\setminus L)+B_r.
\]

Suppose observer `i` strongly envies `W`.  If even giving all of `R` to `i`
would not pay that wall,

\[
v_i(Y_i)+v_i(R)<\tau_i(W), \tag{1}
\]

then

\[
v_i(B_q)>v_i(R). \tag{2}
\]

In the live flower polarity, observer `r` can never satisfy (1).  Hence every
root wall can be repaired by retaining an inclusion-minimal packet
`R_r subseteq R` such that

\[
v_r(T_q+f+R_r)\ge\tau_r(B_q+L). \tag{3}
\]

Only the external owners `c,s` can remain individually unpayable; each such
owner must have the strict residual polarity (2).

## Proof

Every intended owner in the minimal-payment rotation weakly improves, so
`v_i(Y_i)>=v_i(X_i)`.  Base EFX against

\[
X_r=L+R
\]

gives

\[
v_i(Y_i)\ge v_i(L)+v_i(R)-m_i(L+R). \tag{4}
\]

On the other hand,

\[
\tau_i(W)=v_i(B_q)+v_i(L)-m_i(B_q+L). \tag{5}
\]

Combining (1), (4), and (5), and cancelling `v_i(L)`, yields

\[
v_i(B_q)>
2v_i(R)-m_i(L+R)+m_i(B_q+L). \tag{6}
\]

Because `R` is nonempty and valuations are positive,

\[
m_i(L+R)\le v_i(R),
\qquad
m_i(B_q+L)>0.
\]

The right side of (6) is therefore strictly larger than `v_i(R)`, proving
(2).

For `i=r`, the early-root polarity lemma gives

\[
v_r(B_r)>v_r(B_q).
\]

Since `B_r subseteq R`, positivity implies

\[
v_r(R)\ge v_r(B_r)>v_r(B_q),
\]

contradicting (2).  Thus all of `R` pays any root wall.  Finiteness lets us
delete goods until an inclusion-minimal paying packet `R_r` remains, proving
(3). \(\square\)

## Component consequence

Insert the selected `R_r` into the root-retained cell of the two-root
residual-split response-Hall lemma.  The original evolved-`q` wall by `r` is
then paid.  Any new wall must be against the enlarged root target, the
evolved `q` target, or an augmented external leaf, and all response incoming
sets remain supplied by the same two-root component.

Thus the remaining payment selector is genuinely two-external-owner:

1. find disjoint packets paying the `c,s` walls; or
2. use an unpayable polarity `v_i(B_q)>v_i(R)` or a two-owner weighted Hall
   deficiency to flip/grow the component.

The scalar implication replays in
[`flower_residual_wall_payment_polarity_audit.json`](flower_residual_wall_payment_polarity_audit.json).

## Claim boundary

The theorem always pays the earlier root and sharply orients every
individually unpayable external wall.  It does not guarantee simultaneous
disjoint payments for `c,s`, eliminate their strict polarities, close a
response Hall deficiency, close `GG`, or prove four-agent additive EFX.

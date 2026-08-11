# Flower early-root charity rotation lemma

**Date:** 2026-08-10

**Status:** cap-free analytic strengthening of the live flower polarity;
adaptive item-level dependency closure remains open

## Statement

Let `(X,{f})` be a positive additive EFX-with-charity allocation, with `r`
earlier than `q` in the fixed priority.  Write

\[
X_r=T_r\mathbin{\dot\cup}B_r,
\]

where both packets are nonempty.  Assume the displayed mutual-flower bundle

\[
D_q=T_r+f
\]

is common-safe.  Then either

\[
Y=(T_r+f,\ X_q,\ X_c,\ X_s;\ B_r)
\]

is an EFX-with-charity allocation that strictly improves `r`, or

\[
v_r(f)\le v_r(B_r). \tag{1}
\]

Consequently, in the live cell of the three-rotation polarity lemma, global
lexicographic maximality forces

\[
v_r(B_r)\ge v_r(f)>v_r(B_q), \tag{2}
\]

while that lemma already gives

\[
v_q(B_q)>v_q(B_r). \tag{3}
\]

Thus `r` and `q` strictly rank the two bottom packets in opposite orders.
The statement is independent of both packet cardinalities.

## Proof

Every assigned bundle of `Y` is common-safe: `r` receives `D_q`, and every
other owner keeps her base bundle.  The new charity packet `B_r` is dominated
by every owner.  Indeed, for any observer `i` and any `t in T_r`, base EFX
against `X_r` gives

\[
v_i(X_i)\ge v_i(X_r-\{t\})\ge v_i(B_r).
\]

If `v_r(f)>v_r(B_r)`, then

\[
v_r(T_r+f)>v_r(T_r+B_r)=v_r(X_r).
\]

Hence all EFX and charity inequalities hold and the earliest changed owner
`r` strictly improves.  This proves the dichotomy.  At a globally
lexicographically maximal state the first alternative is impossible, so
(1) holds.  Combining it with the previously proved live polarity
`v_r(f)>v_r(B_q)` gives (2), and the existing `q`-row inequality gives (3).
\(\square\)

## Why this matters

The residual flower wall is now an opposite-order packet problem rather
than only an opposite `f/B_q` problem.  Aggregate packet order is not enough
to choose a successful item exchange: an exact realizable packet model
blocks the finite aggregate candidate family and escapes only after splitting
`K` and `B_q` at individual goods.  Therefore the next operation must follow
an item-level blocker through an owner/charity component; another aggregate
rotation cannot close the bridge.

The scalar implication replays in
[`flower_early_root_charity_rotation_audit.json`](flower_early_root_charity_rotation_audit.json).

## Claim boundary

This lemma strengthens the live polarity but does not select an improving
item exchange, terminate the released-good dependency, close `GG`, or prove
four-agent additive EFX.

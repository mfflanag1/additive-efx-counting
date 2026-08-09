# Alternating extension-or-handoff reduction

**Date:** 2026-08-09

**Status:** strict bridge exactly refuted; broader cap-free theorem unaffected

**Order:** `(p,s,q,r)`; the half-turn is symmetric

## Setup

Write

\[
X_p=\{x\},\quad X_s=\{y\},\quad
X_r=T_r\mathbin{\dot\cup}B_r,\quad
X_q=T_q\mathbin{\dot\cup}B_q,
\]

and let `f` be the charity good. Put

\[
D_p=T_r+f,\qquad D_s=T_q+f,\qquad R=B_r+B_q.
\]

Assume all four compatible cross-bottom families are absent. A set is
*desired* when it is common-safe at the base and strictly improves its
source.

This note analyzes a hypothetical failure of both requested branches:

1. no rooted EFX allocation fixing `p={x}` lexicographically improves the
   base in `(p,s,q,r)`; and
2. no EFX allocation gives `p` any desired subset of `X_r+f`.

## Desired-set transversal forced by failure

Let `E subseteq X_r+f` be desired by `p`. If a desired set `C` for `r`,
disjoint from `E,x,y`, exists, then

\[
(Y_p,Y_r,Y_s,Y_q)=(E,C,\{y\},\{x\})
\]

is EFX: `p,r,q` strictly exceed their base utilities, `s` retains its base
singleton, and `E,C` are common-safe. Likewise, a desired `s`-set `C`
disjoint from `E,x,y` gives

\[
(Y_p,Y_r,Y_s,Y_q)=(E,\{y\},C,\{x\}).
\]

Therefore failure of the promoted branch forces:

> **Transversal condition.** Every desired set sourced by `r` or `s` and
> disjoint from `x,y` intersects every `p`-desired subset of `X_r+f`.

This is cap-free and uses no fixed move menu.

## The common-safe residual core

The residual `R=B_r+B_q` is disjoint from `D_p`. Compatible-family absence
rules out every `p`- or `q`-desired subset of `R`: it is a suboffer of
`X_r+B_q`. The transversal condition rules out every `r`- or `s`-desired
subset of `R`.

If some agent valued `R` above her base, the minimal-crossing fact would
produce a desired subset of `R`, a contradiction. Hence

\[
v_i(R)\le b_i\qquad(i=p,r,s,q),
\tag{1}
\]

so `R` is common-safe.

Two further strict inequalities are forced. If

\[
v_q(R)\ge \tau_q(D_s),
\]

then `(p,r,s,q)=(x,y,D_s,R)` is EFX and improves `s`, contradicting the
anchored failure. Thus

\[
v_q(R)<\tau_q(D_s).
\tag{2}
\]

If

\[
v_r(R)\ge \tau_r(D_p),
\]

then `(p,r,s,q)=(D_p,R,y,x)` is an EFX same-offer promotion. Thus

\[
v_r(R)<\tau_r(D_p).
\tag{3}
\]

Finally, apply the root-flip lemma to any `p`-desired
`E subseteq X_r+f`. The promoted root-flip is excluded, so its anchored
mate `(p,r,s,q)=(x,y,E,X_q)` is EFX. Since it fixes `p,q`, improves `r`,
and cannot lexicographically improve the base, necessarily

\[
v_s(E)<b_s.
\tag{4}
\]

Equations (1)--(4) are the exact cap-free cross-source residual.

## Boosted handoff reduction

The ordinary two-safe reduction is stronger than necessary. Let `D,Q` be
disjoint bundles containing neither `x` nor `y`. Suppose `D` is desired by
`s` and

\[
\begin{aligned}
\tau_p(Q)&\le b_p,\\
\tau_r(Q)&\le v_r(y),\\
\tau_s(Q)&\le v_s(D),\\
v_q(Q)&\ge\tau_q(D).
\end{aligned}
\tag{5}
\]

Then

\[
(Y_p,Y_r,Y_s,Y_q)=(\{x\},\{y\},D,Q)
\tag{6}
\]

is EFX and improves `s`. The first three inequalities in (5) are exactly
the comparisons to `Q` made by `p,r,s`; the fourth is `q`'s comparison to
`D`. Comparisons to `D` by `p,r` are base-safe, `r` strictly improves on
`y`, `s` strictly improves on `D`, and singleton comparisons vanish. This
proves (6).

Unlike the earlier two-safe pair, `Q` need not be common-safe at the base:
the recipients `r=y` and `s=D` provide strictly higher moving ceilings.

## Former source wall

Start with `D_s` and `U=X_r+B_q`, as in the reservoir-exchange theorem, and
put `t=tau_q(D_s)`. If a minimal `q`-threshold subset of `U` satisfies the
three moving-ceiling conditions in (5), the boosted handoff is obtained.
If it violates one of them, a minimal desired subset inside an unsafe
deletion is sourced by `r` or `s`, because compatible-family absence excludes
`p,q` on `U`.

An `s`-sourced reversal also closes the gate: use that desired set as `D`
and `D_s` as `Q`. Minimality gives
`v_q(D_s)>=tau_q(D)`, while common safety of `D_s` gives the other three
inequalities in (5).

Consequently the only surviving wall of the reduction was:

> There is an `r`-desired set `A subseteq X_r+B_q`, below the relevant
> `q` threshold, and `A` intersects every `p`-desired subset of `X_r+f`.

In particular `A` intersects `D_p`, hence contains a good of `T_r`. The
eight-good counterexample below realizes failure of the strict bridge:
neither an anchored escape nor a desired promotion from the original
champion offer exists. Thus the proposed uncrossing cannot be universal.

## Exact eight-good refutation

The first non-atomic cell already refutes the strict target. Take packet
sizes

\[
(|T_r|,|B_r|,|T_q|,|B_q|)=(1,1,2,1).
\]

The positive integer profile is frozen in
[`alternating_variable_extension_1121_refutation.json`](alternating_variable_extension_1121_refutation.json).
An independent exhaustive audit checks the structural premises and all
\(5^8=390{,}625\) allocations. Exactly 162 allocations are EFX and improve
the base lexicographically in order `(p,s,q,r)`, but none keeps `p={x}` and
none gives `p` a desired subset of `X_r+f`. See
[`alternating_variable_extension_1121_refutation_audit.json`](alternating_variable_extension_1121_refutation_audit.json).

The smallest missing move changes four goods and is the cross-face exchange

\[
(Y_p,Y_r,Y_s,Y_q)
=
(B_r+\{t_q^0\}+B_q,\ T_r,\ \{y\},\ \{t_q^1,x\}),
\]

leaving `f` in charity. Its utilities are `(1104,22,539,252)`, versus base
utilities `(1078,24,539,61)`. The new `p` bundle is desired at the base but
is not contained in `X_r+f`. The allocation is EFX and improves the first
priority coordinate. Exhaustive enumeration proves that no outside escape
changes fewer than four goods.

This is precisely the operation omitted by the strict bridge: an
opposite-reservoir or cross-face desired-root promotion. It is already
allowed by the dual-reservoir trichotomy, so the refutation does not weaken
the cap-free alternating global-lex theorem and is not a counterexample to
EFX.

## Earlier adversarial evidence and boundary

The boosted handoff exists in all 18 frozen eleven-good profiles, the strict
cross-source/no-two-safe-pair profile, the three-pair residual profile, and
the new profile with no same-offer promotion at all. This is evidence, not a
cap-free existence proof.

The exact profile
[`alternating_no_same_offer_promotion_dominance_2222_audit.json`](alternating_no_same_offer_promotion_dominance_2222_audit.json)
has no EFX escape promoting `p` to any desired subset of `X_r+f`, while both
an anchored repair and an opposite-reservoir promotion exist. It proves that
the anchored branch is genuinely indispensable, but it does not refute the
two-branch dichotomy.

One additional binary-cell implication is exact UNSAT: after imposing the
hard `p/r` cross-source residual and excluding every same-offer two-safe
pair, it is impossible for every qualifying opposite-reservoir `p`-set `P`
to satisfy `v_s(P+f)<=b_s`. Thus some `P+f` crosses `s` in that cell. See
[`alternating_cross_source_no_s_augmented_reversal_2222.json`](alternating_cross_source_no_s_augmented_reversal_2222.json).
This identifies a plausible circuit-uncrossing move but is not used as a
cap-free premise.

The unrestricted strict extension-or-handoff lemma is false. Its smallest
known repair is to admit the cross-face promotion above, which returns the
statement to the already-proved dual-reservoir trichotomy. Complete
four-agent additive EFX is not claimed.

# Normalization-bypass reservoir reversal lemma

**Date:** 2026-08-13

**Status:** cap-free reduction of every ledger-free repeated response to a
two-safe reservoir pair, a new desired source, or a retired-packet collision

## Input

Let `Z^-` be the canonical ledger-free allocation in a normalization-bypass
state. Let

\[
b_i=v_i(Z^-_i)
\]

and let `E` be a globally minimum current response at `Z^-`, desired by
source `s`. Thus

\[
v_s(E)>b_s,
\qquad
\tau_i(E)\le b_i\quad(i\in N).                  \tag{1}
\]

Choose any owner `h` whose current bundle

\[
U=Z^-_h
\]

is disjoint from `E`. Such an owner exists whenever `E` lies in one physical
target, and there are three choices other than that target owner. Put

\[
t=\tau_h(E).
\]

Equation (1) gives

\[
v_h(U)=b_h\ge t.                                 \tag{2}

## Minimal threshold extraction

Choose an inclusion-minimal packet `Q subseteq U` satisfying

\[
v_h(Q)\ge t.                                     \tag{3}

The family is nonempty by (2). Exactly one of the following occurs.

### 1. Safe payment packet

If

\[
\tau_i(Q)\le b_i\quad(i\in N),                  \tag{4}

then `E` and `Q` are disjoint current-safe packets, `E` is desired by `s`,
and `Q` pays `h` against `E`:

\[
v_h(Q)\ge\tau_h(E).                              \tag{5}

This is a two-safe response/payment pair available for matching or
compression.

### 2. Unsafe threshold reversal

Otherwise some observer `i` and some `g in Q` satisfy

\[
v_i(Q-g)>b_i.                                    \tag{6}

Inside `Q-g`, choose an agent/subset pair `A` of globally minimum cardinality
among all subsets desired over the current allocation. Then `A` is desired,
current-safe, and disjoint from `E`. Minimality of `Q` at threshold `t`
gives

\[
v_h(A)\le v_h(Q-g)<t\le v_h(E).                 \tag{7}

Thus `(A,E)` is again a two-safe pair: `A` supplies a desired response and
`E` pays owner `h` against `A`.

No packet-size bound or valuation discretization is used.

## Collision and rank routing

Apply the construction to each current owner bundle disjoint from `E`.

- If a selected `Q` or `A` meets a proper nonempty subpacket of the named
  retired packet `K`, the collision packet strictly shrinks.
- If it contains all of `K`, the state enters the whole-packet or root-facing
  collision geometry with an exact first-hit label.
- If it avoids retired support and introduces a matchable desired source or
  target, response-rank deficiency strictly decreases.
- A rank-four family of pairwise-disjoint current-safe/current-desired cores
  is an EFX contradiction; an internally supplied desired cycle is PI.

If all three disjoint owner reservoirs take the unsafe-reversal branch, the
three-reservoir fan dichotomy applies.  The three reversed packets together
with `E` either have four distinct sources, giving a rank-four current-
response EFX contradiction, or carry an exact duplicated/missing-source
certificate, and in every source pattern the four physical supplier-response
edges contain a supplier-closed PI cycle.

Consequently an exact normalization-bypass survivor must make every
reservoir reversal ledger-free yet fail to add a matchable source/target.
Safe payment packets leave the same deficient response relation, while the
all-unsafe case closes by PI.  Therefore the only ledger-free bypass survivor
contains at least one **safe threshold-payment packet**; it is not an
all-unsafe or same-source recurrence.

## Claim boundary

This lemma proves threshold-selector nonemptiness, the safe/reversal
dichotomy, current safety of the reversed desired set, and exact external
payment inequality (7). It does not prove that the resulting safe pairs
always complete a rank-four matching, eliminate the safe-payment wall,
close the whole-packet/root-facing branches, close
`T_{L,times}^*`, or prove four-agent/general EFX.

The all-unsafe source fan is sharpened separately in
`NORMALIZATION_BYPASS_THREE_RESERVOIR_FAN_DICHOTOMY_20260813.md`.

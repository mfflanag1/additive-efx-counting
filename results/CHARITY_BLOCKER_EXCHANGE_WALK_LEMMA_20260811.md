# Charity-blocker exchange-walk lemma

**Date:** 2026-08-11

**Status:** cap-free termination of singleton-charity safety by connected
exchange, EFX/lex improvement, or permanent response augmentation

## Unsafe replacement charity

Let `(Y,{g})` be an all-owner-paid noncomplete candidate obtained during the
repeated-support splice:

\[
 v_i(Y_i)\ge v_i(X_i)qquad(i\in N).               \tag{1}

\]

Suppose the singleton charity is unsafe for owner `i`:

\[
 v_i(g)>v_i(Y_i).                                  \tag{2}

\]

Then `{g}` is strictly desired by `i` relative both to `Y_i` and to the base
`X_i`.  A singleton is automatically common-safe because its EFX threshold
after deleting its only good is zero.  Thus every charity blocker is also a
named ordinary response source.

## One exchange step

Choose any good `h in Y_i`, give `g` to `i`, and make `h` the new singleton
charity:

\[
 Y_i'=(Y_i\setminus\{h\})+g,
 \qquad P'=\{h\}.                                  \tag{3}

\]

The blocking owner strictly improves relative to the current candidate:

\[
 \begin{aligned}
 v_i(Y_i')-v_i(Y_i)
 &=v_i(g)-v_i(h)\\
 &>v_i(Y_i)-v_i(h)\ge0.                            \tag{4}
 \end{aligned}

\]

Every other owner bundle is unchanged, so all owners remain weakly paid and
the original earlier strict root gain is preserved.  Goods are conserved and
the two packet moves `charity -> i:g` and `i -> charity:h` form a connected
exchange step.

## Finite exchange walk

If the new charity `{h}` is unsafe, apply (3) to one of its blockers.  At
every step exactly one owner bundle changes and that owner's utility strictly
increases; no other owner utility decreases.  Because the ground set is
finite, each owner has finitely many bundle values.  Therefore the walk cannot
revisit an allocation and terminates after finitely many exchanges.

The time-ordered packet walk is release-compatible.  Consecutive steps share
the charity token, so after cancelling goods merely passed through charity,
all nontrivial net transfers remain in one connected component on the
participating owners and charity whenever its final good differs from the
initial one.

At termination exactly one of the following holds.

1. Every owner-target comparison and the final singleton charity are safe.
   The allocation is EFX with charity and lexicographically improves `X`.
2. The charity is safe but an owner target is unsafe.  Globally minimal
   current-response extraction gives the ordinary or surplus-decorated
   permanent response augmentation already proved for paid splices.
3. Before continuing, the singleton response `(i,{g})` is new at the fixed
   repeated-support state.  Recording it is an ordinary permanent response
   augmentation.  If it is old, performing (3) still gives strict same-owner
   utility progress, so it cannot be an idempotent reset.

Thus singleton-charity failure cannot survive as a scalar budget separator
or force restoration of the old charity good.

## Global consequence

The charity-budget premise of the charity-exchange endpoint need not be
guessed in advance.  Starting from any all-owner-paid splice, the exchange
walk either enforces it, closes by EFX/lex improvement, or produces permanent
response/current-utility progress.  The exact fixed-U cyclic witness is one
instance of the terminating exchange branch.

## Verification and boundary

[`charity_blocker_exchange_walk_audit.json`](charity_blocker_exchange_walk_audit.json)
checks singleton common safety, strict blocker improvement, preservation of
all other utilities, finite-state nonrecurrence, and the exhaustive terminal
classification.

This lemma assumes singleton charity and an all-owner-paid input.  It does not
close owner-target decorated-response recurrence after charity becomes safe,
force payment before the walk, close the full repeated-support theorem, close
GG, or prove four-agent/general additive EFX.

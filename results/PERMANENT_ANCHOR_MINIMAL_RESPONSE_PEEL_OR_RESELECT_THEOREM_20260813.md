# Permanent-anchor minimal-response peel-or-reselect theorem

**Date:** 2026-08-13

**Status:** cap-free resolution of the permanent-anchor hitting-set
recurrence and its associated source-inactive loss-band recurrence

## Post-recruitment input

Let `X` be the globally lexicographically maximal partial EFX base, with
first-priority root `r`, and put

\[
 x=v_r(X_r).
\]

At the exact sacrifice-handoff state `Y`, the root target is

\[
 B=K\mathbin{\dot\cup}E,                         \tag{1}
\]

where the old permanent anchor and recruited response satisfy

\[
 v_r(K)>x,
 \qquad v_r(E)>p:=v_r(Y_r^{\rm pre})\ge x.       \tag{2}
\]

The pre-recruitment root floor `p` pays every target left unchanged by the
sacrifice handoff.  The recruited response is not assumed to remain
observer-safe after the displaced owner is sacrificed.

Suppose `B` is unsafe in the complete handoff allocation.  Among all
agent/subset pairs desired relative to that allocation, choose a subset
`D subseteq B` of globally minimum cardinality and let `i` be its source.
Thus

\[
 v_i(D)>v_i(Y_i).                                 \tag{3}
\]

The mixed hitting case has `D intersect K` and `D intersect E` both
nonempty.  The proof below also applies to an anchor-only source-inactive
response `D subseteq K`.

## Properness and exact safety

Because `B` is unsafe, a blocking observer desires a one-good deletion of
`B`.  Hence global minimum cardinality gives

\[
 \varnothing\ne D\subsetneq B.                  \tag{4}
\]

If some observer strongly envied `D`, deleting that observer's least good
would give a smaller desired subset, contradicting minimality.  Therefore
`D` is safe relative to the complete handoff allocation.  These two facts do
not use safety of `E` after the sacrifice.

Put `C=B\setminus D`.  Exactly one of the following two branches applies.

## Branch I: current-phase root reselection

If

\[
 v_r(D)>x,                                       \tag{5}
\]

give `D` to the root and release `C` with its complete signed provenance.
The target `D` is safe at the exact handoff floors by the preceding argument,
is strictly desired by the root over the globally maximal base, and is
physically disjoint from every target retained after the exchange.  This is
a valid current-phase root-anchor reselection, outcome 4 of the recurrence
contract.  It does not promote `D` to the old base-anchor class.

Safety persists through this exchange: every nonroot observer keeps the same
assigned bundle, while the root owns the target herself.  Root walls against
other targets, if any, are kept as exact labels; anchor reselection is not
misreported as an EFX endpoint.

## Branch II: paid permanent peel

Suppose instead that

\[
 v_r(D)\le x.                                    \tag{6}
\]

Replace the source's old bundle by `D`, give `C` to the root, and release the
source's old bundle to charity or the labeled residual pool.  Feasibility
follows from (4).  The source strictly improves by (3), and `D` is a safe
target.  Most importantly, additivity and (2), (6) give

\[
 \begin{aligned}
 v_r(C)
 &=v_r(K)+v_r(E)-v_r(D)\\
 &>x+p-x=p.                                      \tag{7}
 \end{aligned}
\]

Thus the old anchor's strict surplus pays for the entire root value of the
peeled response.  The root remains above its pre-recruitment floor and still
pays every unchanged target.  The physical root support strictly shrinks
from `B` to `C`.

The target `D` remains safe after the move.  Every observer other than the
root and source keeps the same assigned value, the source strictly improves,
and in the root row

\[
 \tau_r(D)<v_r(D)\le x\le p<v_r(C).              \tag{8}
\]

Hence assigning `D` to its source introduces no wall against `D`.

Record `D` in the **retired root-support ledger**.  The ledger is globally
monotone: an entry is never erased.  Under the old anchor label, every later
root-target selector is restricted to its complement.  A retired good may
return to the root only under a different, explicitly recorded anchor
exchange; it never reconstructs the old labeled state.  The ledger update is
strict because `D` is nonempty, and the family of physical support/anchor
labels is finite because the ground set is finite.  Therefore this branch is
outcome 3 of the recurrence contract.  An exact state containing the old
root support `B` cannot recur with the same ledger and anchor label.

Every EFX failure after the peel keeps an exact label.  The new source target
`D` is safe, the root pays unchanged targets, and other assigned bundles do
not change.  A surviving wall is therefore against the reduced root target,
or is a pre-existing sacrificed/residual wall.  The theorem needs no generic
Hall classification and makes no claim that the peeled candidate is already
EFX.

## Mixed hitting-set recurrence

For a mixed `D`, (5) gives a valid safe root reselection and (6) gives strict
retired-support progress.  These alternatives are exhaustive.  Hence an
exact mixed permanent-anchor response cannot recur while all five closing
outcomes fail.

Notice that the argument uses the permanent anchor only through its strict
root surplus in (2).  No fixed valuation cap, item bound, residual-payment
search, or response-order case split is present.

## Source-inactive loss band

If the globally minimum response is anchor-side and source-inactive, it is
nonempty, proper, and safe at the handoff floors; apply the identical
root-value dichotomy.  If (5) holds, reselect it as the current root anchor.
If (6) holds, peel it and pay the root by (7).  If some previously named
source-inactive core is not globally minimum, the globally minimum response
is processed instead and still changes the anchor label or ledger before the
old loss-band state can recur.  Thus the source-inactive loss band cannot
recur with the same permanent anchor and retired-support ledger.

This is stronger and safer than keeping `E` alone: the proof never assumes
that `E` remains observer-safe after the sacrifice.

## Exact recurrence audit

The full signed-state record contains the allocation, charity, matching,
hole, physical response support, releases, anchor label, and retired
root-support ledger.  Branch I changes the anchor/release record.  Branch II
strictly enlarges the retired ledger and changes the root support.  Full
signed reconstruction therefore rules out an exact recurrence in either
branch unless a separately labeled closing transition has occurred.

## Claim boundary

This theorem resolves the permanent-anchor hitting-set recurrence theorem
under the frozen post-recruitment contract, by outcomes 3 or 4, and removes
the associated source-inactive loss-band recurrence.  It does not terminate
pre-existing residual walls, prove that a later phase change cannot occur,
close other GG state classes, or prove four-agent/general additive EFX.  A
future composition must carry the retired-support ledger explicitly; it may
not restore peeled goods through an unlabeled orientation reset.

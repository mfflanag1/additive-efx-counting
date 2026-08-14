# Ledger-normalized root external-star ascent-or-price theorem

**Date:** 2026-08-13

**Status:** cap-free elimination of recurrent root-to-hole signs and reduction
of terminal hole-to-root signs to the retired-collision/root-price branches

## Exact external-star state

Let `X` be the globally maximal base with first-priority root `r` and

\[
x=v_r(X_r).
\]

At one ledger-normalized state, let the root hold a safe core `A` with

\[
v_r(A)=x+\delta,
\qquad \delta>0,                                  \tag{1}
\]

and let every other good be allocated EFX among the three nonroot owners as
`P_h`.  Retired goods that cannot be released under the current physical
label remain with their recorded holders.  Hence the only possible EFX
failures are root-star comparisons.

## Root-to-hole wall: strict finite ascent or rank progress

Suppose the root strongly envies a hole bundle:

\[
v_r(A)<\tau_r(P_h).                               \tag{2}
\]

Choose `g in P_h` with `v_r(P_h-g)>v_r(A)`.  Inside `P_h-g`, choose a subset
`D` of globally minimum cardinality among all subsets desired by some owner
relative to the current allocation.  Then `D` is current-safe.

- If the source of `D` is `r`, then `v_r(D)>v_r(A)`.  Canonically normalize
  every retired transfer.  If the resulting retained root core is safe, use
  it as the new root core and allocate the exact complement EFX among the
  other three owners.  The root value strictly increases.
- If the source is nonroot, `A` and `D` are disjoint safe protected cores
  with distinct represented owners.  They enter the existing two-core/two-
  hole response-Hall machinery.
- If canonical normalization of either route hits retired support or makes
  the retained enlarged root core unsafe, process the named proper/whole
  collision or its globally minimum normalized response.  It is not counted
  as root ascent until an actual safe root core is adopted.

There are finitely many root bundles in a fixed finite instance.  Therefore
the first branch cannot recur indefinitely: every executed ledger-normalized
root ascent strictly raises `v_r(A)`.  Outside a retired collision or rank-
two continuation, the process reaches a state with no root-to-hole wall.

## Hole-to-root wall: safe split and root-price trichotomy

At a state with no root-to-hole wall, suppose hole `h` strongly envies the
root core.  Some deletion `A-g` is desired by `h` over `P_h`.  Choose a
globally minimum desired subset

\[
D\subseteq A-g.                                   \tag{3}
\]

Then `D` is nonempty, proper, and current-safe.  Its source is nonroot:
positivity gives `v_r(D)<v_r(A)`, so the root cannot desire it over her
current bundle.  Put `C=A-D`.

Canonical retired-support normalization is applied first.  A hit on the
named retired packet returns to the proper/whole collision audit.  In the
ledger-free split, exactly one root-value branch applies:

1. if `v_r(D)>x`, `D` is a safe base-improving root reselection, subject to
   retaining any nonreleasable retired support and rechecking the enlarged
   target;
2. if `v_r(D)<delta`, assign `D` to its response source and retain `C` at
   the root, since
   \[
   v_r(C)=x+\delta-v_r(D)>x;                      \tag{4}
   \]
3. otherwise
   \[
   \delta\le v_r(D)\le x,                         \tag{5}
   \]
   the split lies in the exact root-surplus loss band, whose compensation
   price is `v_r(D)-delta`.

Thus a terminal hole-to-root sign gives root reselection, controlled release,
retired collision, or the already isolated bounded root-holder price.

## Consequence for the three-offer normalization branch

After the priority split sends a root-centered safe three-offer state into
the one-core/three-hole external-star normal form, its root-to-hole signs
cannot recur without strict finite root ascent or rank/collision progress.
Its remaining hole-to-root signs reduce to the root-price/collision family.
The external star therefore contributes no independent terminal separator
inside `T_{L,times}^*`.

## Claim boundary

This theorem proves the strict root-ascent potential and the terminal split
trichotomy.  It does not pay the surviving holder-price separator, prove
safety of a ledger-retained enlarged root core without recomputation,
terminate every downstream two-hole collision, close `T_{L,times}^*`, or
prove four-agent/general EFX.


# Rank-three cycle-residual charity normal-form lemma

**Date:** 2026-08-13

**Status:** cap-free complete-allocation and payment normal form; universal
observer-safety selection remains

## Cycle data

Let

\[
 i_0\to i_1\to\cdots\to i_{k-1}\to i_0,
 \qquad k\in\{2,3\},                               \tag{1}
\]

be the forced release-compatible response cycle.  For each source `i`, let
`D_i` be its nonempty base-common-safe desired core inside the next target's
physical bundle.  Since cycle targets are distinct, the cores are pairwise
disjoint.  For every physical cycle owner `j`, write

\[
 Y_j=D_{\operatorname{pred}(j)}\mathbin{\dot\cup}R_j. \tag{2}
\]

Let `{p}` be the singleton charity.

## Complete residual selector

Choose an arbitrary subpacket `S_j subseteq R_j` for each cycle supplier and
one cycle owner `b` to receive `p`.  Define

\[
 Z_i=D_i
      \mathbin{\dot\cup}S_{\operatorname{next}(i)}
      \mathbin{\dot\cup}(R_i\setminus S_i),        \tag{3}
\]

and add `p` to `Z_b`.  Owners outside the cycle remain unchanged.

Equation (3) conserves every good.  Supplier `j` sends the single packet

\[
 D_{\operatorname{pred}(j)}\mathbin{\dot\cup}S_j  \tag{4}
\]

to its predecessor and retains `R_j-S_j`.  Thus all movement uses exactly
the `k` reversed cycle edges plus the charity edge `charity -> b`:

\[
 k+1\le4.                                          \tag{5}
\]

Packet cardinalities are unrestricted.

## Owner payment

Every cycle owner receives its desired core `D_i`.  Since

\[
 v_i(D_i)>v_i(X_i),                                \tag{6}
\]

all other terms in (3) are nonnegative and every cycle owner is strictly
above base for every residual selection.  Outside owners retain their paid
bundles.  Therefore payment and completeness are automatic throughout the
selector family.

## Exact remaining inequality

The four-edge theorem on a release-compatible cycle is now equivalent to
finding `b` and `(S_j)` such that

\[
 v_h(Z_h)\ge\tau_h(Z_i)
 \qquad(h\ne i).                                   \tag{7}
\]

The family includes retaining every residual, rotating every entire cycle
bundle, and every intermediate arbitrary packet split.  It is not a moved-
good-radius restriction.  If (7) fails for every selection, a proof must use
the globally minimal failed target to obtain a new signed response/support
record or an exact full-margin overlap separator.  A countermodel must make
all these inequalities fail while satisfying the complete saturation ledger.

## Verification and boundary

[`audit_rank_three_cycle_residual_charity_normal_form.py`](../tracks/parkability/audit_rank_three_cycle_residual_charity_normal_form.py)
independently audits all abstract residual-send/retain patterns for cycle
lengths two and three, every charity recipient, exact conservation, empty
charity, and the three/four-edge bounds.  Each residual atom represents an
arbitrary packet, so the support proof is cap-free.  It also verifies owner
payment in exact QF-LRA.

This lemma does not prove the universal observer-safety selector (7), make
overlapping dynamic response cores disjoint, or finish the four-edge theorem.

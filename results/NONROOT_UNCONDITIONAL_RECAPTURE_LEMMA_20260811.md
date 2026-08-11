# Nonroot unconditional-recapture lemma

**Date:** 2026-08-11

**Status:** cap-free composition lemma; terminal two-residual and
J-exhausted/root-facing branches remain open

## Statement

Use a rank-three maximum-matching compression of a four-owner flower
component.  Let `d` be its unique unmatched owner, let `W` be her residual
bundle, and let every `i != d` hold a pairwise-disjoint common-safe desired
core `A_i`.  The root-anchoring lemma gives

\[
 d\ne r.                                               \tag{1}
\]

Suppose a represented source `i` responds to `W` with a common-safe desired
core `D_i subseteq W`.  Perform the usual recapture

\[
 Z'_i=D_i,
 \qquad
 Z'_d=A_i+(W\setminus D_i),                            \tag{2}
\]

and leave every other selected core fixed.

Then (2) is a complete priority-valid candidate **without any payment
premise for `d`**.  Every owner other than `d` receives a common-safe bundle
she strictly prefers to her base bundle.

## Priority split

If `d` is external, both mutual owners `r,q` retain desired cores, so an EFX
instance of (2) is the requested flexible improvement.  If `d=q`, the
earlier mutual owner `r` retains a desired core, so an EFX instance is a
strict improvement in the fixed priority even if `q` loses.  Equation (1)
excludes the only invalid case, `d=r`.

Thus the payment condition

\[
 v_d(D_i)-v_d(A_i)
 \le v_d(W)-v_d(X_d)                                  \tag{3}
\]

is not a feasibility condition for recapture.  It only decides which wall
normal form follows.

## Exhaustive continuation

1. If (3) holds, `d` is weakly nonworse.  No owner can fail against a
   selected core, so every wall is against the new residual.
2. If (3) fails, the new residual is below `v_d(X_d)`.  The exact
   own-capture identity and lex-sacrificed compression lemma apply.  Every
   wall is either `d` against a selected core or a represented source
   against the residual.

In the second branch, aligned walls advance the residual potential,
source-active disjoint walls admit a hole pivot, and source-inactive walls
enter the finite core/residual repair chain.  Hence the strict recapture
polarity

\[
 v_d(D_i)>v_d(A_i)+v_d(W)-v_d(X_d)                    \tag{4}

\]
is no longer a terminal alternative.  It is precisely the entrance
condition to the priority-valid sacrificed-owner machinery.

## Proof

The bundles in (2) partition `A_i+W`; every other bundle is unchanged.
Source `i` desires `D_i`, and every other represented source retains her
desired core.  Common safety is inherited by all three selected cores.
The priority conclusion follows from (1) and the two cases above.

If the new residual pays `d`, every owner is weakly nonworse and all core
targets are common-safe, proving branch 1.  If it does not pay `d`, every
represented source is still strictly above base and safe against every
core.  Owner `d` is automatically safe against her own residual.  Therefore
only the two wall types in branch 2 remain.  Expanding the new residual
utility gives (3) exactly, so its negation is (4).  No packet cardinality is
used. \(\square\)

## Composition boundary

For rank-three maximum-matching compressions, this lemma removes
"unpayable recapture" as a separate proof outcome.  The surviving
single-residual branches are now only:

1. J-exhausted unanimous core dominance;
2. a priority-invalid root-facing pivot; or
3. a recurrence among otherwise valid hole/repair states.

Rank-two maximum matchings still leave two residual owners and require the
two-way residual-pool selector.  The lemma therefore does not close the
`GG` flower, the other selected-cycle classes, or four-agent additive EFX.

## Verification

[`nonroot_unconditional_recapture_audit.json`](nonroot_unconditional_recapture_audit.json)
checks the recapture partition, the exact paid/unpaid identity, both
priority branches, and the two-sided wall localization under Z3 5.0.0 and
4.15.3.

# Third-owner root-replacement fork lemma

**Date:** 2026-08-11

**Status:** cap-free necessary-and-sufficient packet selector for the final
third-owner fork; elimination of its exact two-row donor blockade remains open

## Captured-source state

Let the root currently hold packet pool `R`, including a nonempty packet
`C` extracted from a common-safe desired source core `A`. The captured source
`a` holds

\[
 A'=A-C+B
\]

and is at or below base, while returning all of `C` restores it strictly:

\[
 v_a(A'+C)=v_a(A+B)>v_a(X_a).                      \tag{1}
\]

Let a third source `b` hold a disjoint common-safe desired core `D`, with
margin

\[
 \mu_b=v_b(D)-v_b(X_b)>0.                          \tag{2}
\]

## Fork packets

Choose packets

\[
 K\subseteq D,
 \qquad G\subseteq R\setminus C.
\]

Return `C` to `a`, move `K` from `b` to the root, and move `G` from the root
to `b`:

\[
 Y_r=R-C-G+K,
 \qquad Y_a=A'+C,
 \qquad Y_b=D-K+G.                                 \tag{3}
\]

All other targets remain fixed. This is the connected three-owner fork

\[
 r\longrightarrow a:C,
 \qquad b\longrightarrow r:K,
 \qquad r\longrightarrow b:G.
\]

The packet `C` returns to its original source, while `K,G` form the donor's
root-replacement exchange.

Put the exact root replacement requirement

\[
 \delta_r=v_r(X_r)-v_r(R-C).                       \tag{4}
\]

Then (3) pays all three affected sources exactly when

\[
 v_r(K)-v_r(G)\ge\delta_r                           \tag{R}
\]

and

\[
 v_b(K)-v_b(G)<\mu_b.                               \tag{B}
\]

Equation (1) pays `a`; (R) pays the root; and (B) is equivalent to
`v_b(D-K+G)>v_b(X_b)`.

## Global selector and exact failure

Let

\[
 \mathcal F_b={(K,G):K\subseteq D,
 G\subseteq R\setminus C,
 v_r(K)-v_r(G)\ge\delta_r\}.                       \tag{5}
\]

There are exactly three alternatives.

1. **Aggregate root concentration.** `F_b` is empty. Since `G=empty` is
   root-best for every fixed `K` and `K=D` maximizes root value, this is
   equivalent to
   \[
   v_r(D)<\delta_r.                                 \tag{6}
   \]
2. **Fork success.** Some pair in `F_b` satisfies (B). Then all three
   affected sources are strictly or weakly paid. If their changed targets
   satisfy the surplus-budget inequalities, the connected-component theorem
   gives an EFX lexicographic improvement. Otherwise a failed threshold
   supplies the named response augmentation.
3. **Donor blockade.** `F_b` is nonempty but every root-feasible replacement
   captures the donor's whole margin:
   \[
   v_b(K)-v_b(G)\ge\mu_b
   \qquad((K,G)\in\mathcal F_b).                    \tag{7}
   \]

Equivalently, choose a root-feasible pair maximizing
`v_b(G)-v_b(K)`. It succeeds precisely when that maximum is greater than
`-mu_b`; otherwise (7) is the exact separating certificate.

## Consequence

The final third-owner operation is not an unspecified transfer tree. It is
the finite packet optimization (5): replace the captured packet's root value
from one protected core while using the root pool to keep that donor above
base. Failure has only two meanings—root value is concentrated in `C` beyond
the donor's entire core, or every root-feasible replacement captures the
donor's response margin.

The construction composes with an arbitrary number of selected donor cores:
apply (5) to the union of their disjoint cores and partition `K` by source.
A successful multi-donor pair is a root-centered connected fork; a failed
pair identifies at least one donor-margin capture or the aggregate
root-concentration inequality.

## Verification and boundary

[`third_owner_root_replacement_fork_audit.json`](third_owner_root_replacement_fork_audit.json)
checks support conservation, all three payment equivalences, emptiness of the
root-feasible family, and the donor-separation alternative symbolically.

This lemma identifies the exact smallest operation outside the globally
exhausted two-row frontier. It does not contradict (6) or (7) from the GG
flower inequalities, prove every changed target is surplus-budgeted, close
the terminal fork, close `GG`, or prove four-agent/general additive EFX.

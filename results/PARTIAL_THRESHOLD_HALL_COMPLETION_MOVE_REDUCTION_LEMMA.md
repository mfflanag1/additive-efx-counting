# Completion-move reduction for a floater swap

## Statement

Let two one-floater states be related by an owner-minimum swap at source
bundle \(q\):

\[
(X,f)\longrightarrow(X',g),\qquad
X'_q=X_q-g+f,\quad f'=g.
\]

Complete the old state by inserting \(f\) at host \(h\), and complete the new
state by inserting \(g\) at host \(h'\). If the new complete partition has
strictly larger optimal bottleneck EFX margin than every completion of the
old state, then \(h'\ne q\). Subject to this exclusion, the change between
the complete partitions has exactly one of three forms:

1. \(q=h\): a one-good transfer of \(g\) from \(q\) to \(h'\);
2. \(q\ne h\) and \(h'=h\): a two-bundle swap of \(f\) and \(g\) between
   \(h\) and \(q\);
3. \(q\ne h\) and \(h'\notin\{h,q\}\): a three-bundle augmenting path,
   sending \(f\) from \(h\) to \(q\) and \(g\) from \(q\) to \(h'\).

The statement holds for any number of agents and any bundle sizes.

## Proof

If \(h'=q\), reinserting \(g\) into \(X'_q=X_q-g+f\) produces exactly
\(X_q+f\), while every other bundle is unchanged. This is the old state's
completion with host \(q\). The new partition therefore cannot have margin
strictly larger than the best old completion. Hence \(h'\ne q\).

In the old completion, \(f\) is at \(h\) and \(g\) is at \(q\). In the new
completion, \(f\) is at \(q\) and \(g\) is at \(h'\). If \(q=h\), only \(g\)
moves, from \(q\) to \(h'\). If \(q\ne h=h'\), the goods exchange bundles.
If the three indices are distinct, they form the displayed augmenting path.
These cases are exhaustive. \(\square\)

## Four-agent evidence

The exact 46-profile threshold-plateau audit contains 4,848 selected strict
margin-improving steps:

- 2,374 one-good transfers;
- 2,440 two-bundle swaps; and
- 34 three-bundle augmenting paths.

All 4,848 release and insert owner-minimum goods, and none reinserts the new
floater at its source. The census is a regression check, not the proof.

## Claim boundary

The reduction classifies a strict improvement once it exists. It does not
prove that every blocked maximum admits such a move.

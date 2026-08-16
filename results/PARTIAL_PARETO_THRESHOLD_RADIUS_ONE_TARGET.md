# Pareto-threshold radius-one Hall target

## Selector

Let \((X,f)\) range over eligible four-agent one-floater EFX states.  Thus
the allocated bundles are EFX and

\[
v_i(X_i)\ge v_i(f)\qquad(i=0,1,2,3).
\]

First restrict to states whose own-utility vectors are Pareto efficient in
this eligible family.  Among those states, maximize

\[
\Theta(X,f)=\sum_i
\frac{v_i(X_i)-\min_{g\in X_i}v_i(g)}{v_i(M)}.
\]

The live target is:

> Some Pareto-efficient \(\Theta\)-maximizer admits a complete four-bundle
> partition obtained by inserting \(f\), moving at most one previously
> allocated good between bundle labels, and Hall-rematching agents to the
> resulting bundles.

Together with the almost-full theorem of Berger, Cohen, Feldman, and Fiat,
this statement would prove complete EFX existence for four positive-additive
agents.  It does not by itself prove general additive EFX.

## Why this selector is better aligned with the published machinery

A Pareto-improvable champion cycle produces another partial EFX allocation
that Pareto dominates the current state.  Selecting on the Pareto frontier
therefore rules out every such cycle before threshold maximality is invoked.
This imports the central exchange mechanism of Berger--Cohen--Feldman--Fiat
without tying the proof to their ordinary lexicographic potential.  The
threshold objective then supplies a separable weighted contradiction for
the residual exchanges that are not Pareto improvements.

The source paper explicitly presents generalized championship as orthogonal
to the choice of potential and identifies the final unallocated good as the
next open step: <https://arxiv.org/abs/2102.10654>.

## Exact falsification boundary

The radius-zero strengthening is false.  In
`partial_hall_completion_anneal_seed619b.json`, exhaustive selection leaves
a unique Pareto-efficient threshold maximizer

\[
(X_0,X_1,X_2,X_3;f)
=(\{3,6\},\{1,2,7\},\{0,4\},\{5\};8).
\]

All four direct insertions are Hall-blocked.  A radius-one completion exists:
insert good 8 into the first bundle, move good 3 from the first to the second
bundle, and retain the identity matching, giving

\[
(\{6,8\},\{1,2,3,7\},\{0,4\},\{5\}).
\]

Thus the one-old-good move is not an expository convenience; it is necessary
for this selector.

## Finite evidence

- `partial_hall_pareto_threshold_corpus134_scan.json`: all 134 recursively
  extracted hard Hall-obstruction profiles have direct Hall completion at a
  selected maximizer.
- `partial_hall_pareto_threshold_full_corpus_scan.json`: 237 distinct stored
  positive four-agent profiles with 7--10 goods; exactly one radius-zero
  failure and zero radius-one failures.  Every selected maximizer in every
  profile has a radius-one completion.
- The selected implementation is checked against an independent literal
  Pareto-frontier and exact-Fraction threshold calculation on the small
  regression instance in `test_parkability.py`.

These are falsification results, not a proof.

## Missing analytic gate

At a selected state, every Pareto-improvable cycle is impossible.  Assume
every radius-one complete partition is Hall deficient.  The remaining gate
is to show that its champion/generalized-champion structure forces either:

1. a Pareto-improvable cycle, contradicting Pareto efficiency; or
2. another Pareto-efficient eligible state with strictly larger \(\Theta\).

Because \(\Theta\) is separable by owner bundle, its change decomposes over
weak components of a multi-good transfer graph exactly as normalized
utilitarian welfare does.  If individual positive components are not EFX,
the proved transfer-component dependency lemma places their cross-component
violations on a directed cycle.  The specific missing inequality is that the
weighted threshold gains around one such dependency cycle dominate the
threshold losses, or else expose the radius-one Hall completion.

## Claim boundary

Four-agent EFX and general additive EFX remain unresolved.  The proved
content is the Pareto-cycle exclusion principle, the existing component and
Hall reductions, the exact radius-zero counterexample above, and the bounded
corpus audits.  The radius-one selector is a theorem target.

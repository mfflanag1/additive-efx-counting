# Normalized-threshold Hall completion target

## Exact candidate

Let \((X,f)\) be an eligible one-floater partial EFX allocation for four
positive-additive agents: the allocated bundles are EFX and no agent prefers
the unallocated good \(f\) to her own bundle.  For a bundle \(B\), define the
owner threshold

\[
\tau_i(B)=v_i(B)-\min_{g\in B}v_i(g)
\]

and the normalized threshold potential

\[
\Theta(X,f)=\sum_i \frac{\tau_i(X_i)}{v_i(M)}.
\]

The live theorem target is:

> Among the globally \(\Theta\)-maximal eligible states, at least one state
> admits a host for \(f\) such that the resulting four bundles have an EFX
> feasibility graph with a perfect matching.

If true, this proves complete EFX existence for four additive agents: start
from the known one-unallocated-good EFX allocation, select the promised
maximizer, insert the floater, and use the perfect matching to assign the four
complete bundles.

This is not yet a theorem and it does not by itself prove general additive
EFX.  The general case also needs a way to reduce a charity set of up to
\(n-1\) goods one good at a time while preserving eligibility.

A subsequent Pareto-frontier refinement is recorded in
`PARTIAL_PARETO_THRESHOLD_RADIUS_ONE_TARGET.md`.  Its direct-insertion
strengthening is exactly false, but the version allowing one old-good move
survives the broader stored corpus and interfaces more directly with the
published champion-cycle machinery.

## Exact evidence and falsifications

- `partial_hall_threshold_corpus189_scan.json`: 134 recursively discovered
  exact hard \(4\times9\) profiles; every profile had a threshold-maximal
  eligible state admitting direct Hall completion.  In fact, this corpus also
  had an identity-insertable maximizer in every profile.
- `partial_threshold_maximality_anneal_seed113.json`: refutes the stronger
  identity-completion selector.  Its two threshold maximizers both block
  identity insertion, but Hall rematching completes both.
- `partial_hall_threshold_then_utilitarian_corpus189_scan.json`: refutes using
  normalized utilitarian welfare as a fixed tie-break for identity insertion.
  The surviving claim is existential within the threshold-maximal plateau.
- `partial_threshold_hall_maximality_anneal_seed127.json`: 1,800 adversarial
  iterations found no Hall-selector counterexample.
- `partial_hall_threshold_guided_seed139.json`: 1,600 maximality-guided
  iterations kept a fixed radius-one Hall obstruction below global maximum
  (exact ratio \(20669/26465\)); all three global threshold maximizers were
  Hall-completable.

Computational survival is evidence only.  The result boundary remains:
**identity selector refuted; threshold-maximal Hall selector open; four-agent
and general additive EFX unresolved.**

The broader 237-profile census and the threshold-neutral exchange mechanism
are now recorded in `PARTIAL_THRESHOLD_PLATEAU_CYCLE_TARGET.md`.  That file
supersedes fixed tie-break attempts: minimizing normalized owner utility
inside the maximum plateau is exactly false, while the existential plateau
selector still has no stored-profile counterexample.

## Missing analytic gate

Assume every direct-insertion graph at every \(\Theta\)-maximal eligible state
fails Hall.  Extract a deficient agent set and prove that its wall inequalities
permit either:

1. an eligible exchange/restart with strictly larger \(\Theta\); or
2. a move within the same \(\Theta\)-plateau that strictly reduces a finite
   Hall-defect invariant.

The key local fact available for such an exchange is that replacing an
observer-minimum good \(g\) in a bundle by a larger floater \(f\) cannot lower
that observer's threshold.  The unresolved issue is coupling these
observer-wise gains with ownership and cross-block EFX constraints.

## Replay boundary

The strongest proved Hall reduction remains independently replayable with:

```bash
make verify-partial-hall-pair-extraction
```

The threshold selector is currently a research target, not part of that
verified theorem.

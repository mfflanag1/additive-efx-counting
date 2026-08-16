# EFX goal-reset checkpoint — 2026-08-02

## Exact status

Neither four-agent additive EFX nor general additive EFX has been resolved.
No counterexample to either claim is known from this campaign. No campaign
solver process is active.

The strongest new proved ingredient is the cap-free four-agent owner-minimum
Hall-pair extraction theorem. From an eligible one-floater EFX state, failure
of direct insertion and the owner-minimum transfer family forces a
two-agent/one-neighbor Hall trap. This is a reduction theorem, not a completion
theorem.

Replay it with:

```bash
make verify-partial-hall-pair-extraction
```

## Final bounded refinement after the original checkpoint

The strongest selector target at the final stop is now the
**Pareto-threshold radius-one Hall selector** in
`PARTIAL_PARETO_THRESHOLD_RADIUS_ONE_TARGET.md`. Select an eligible state on
the Pareto frontier, maximize normalized owner-threshold potential there,
then insert the floater, move at most one old good, and Hall-rematch.

The direct-insertion strengthening is exactly false on one stored profile.
The radius-one version survives 237 distinct stored positive four-agent
profiles with 7--10 goods, including all 134 recursively extracted hard Hall
obstructions. This is evidence, not a theorem. Its advantage over the
threshold-only selector is analytic: Pareto efficiency first excludes every
Pareto-improvable champion cycle from the Berger--Cohen--Feldman--Fiat
framework, leaving threshold maximality to handle the residual exchanges.

No solver or scan is active at this stop. The focused parkability suite passes
31 tests.

## Strategy audit completed at this stop

The maximum-Nash, Pareto, fixed-cell rival-menu, and bounded local-completion
branches have been refuted or exhausted at the claimed scope. A subsequent
audit found a sharper surviving four-agent selector: normalized owner-threshold
maximality

\[
\Theta(X,f)=\sum_i\frac{v_i(X_i)-\min_{g\in X_i}v_i(g)}{v_i(M)}.
\]

The live route is therefore:

1. start from the known four-agent one-floater EFX allocation;
2. choose a globally \(\Theta\)-maximal eligible state;
3. insert the floater into some host and rematch the resulting bundles through
   their EFX feasibility graph;
4. prove that at least one threshold-maximal state/host has a perfect matching.

Step 4 is the missing breakthrough lemma. It would prove four-agent EFX but
would not yet prove general EFX.

The stronger identity-insertion version is exactly false: seed 113 has two
threshold maximizers and blocks identity insertion at both, while Hall
rematching completes both. A normalized-utilitarian fixed tie-break also fails
for identity insertion. The surviving claim is existential within the full
threshold-maximal plateau.

The evidence frozen at this stop is exact but computational: all 134 hard
profiles in the recursive obstruction corpus have a Hall-completable threshold
maximizer; a 1,800-iteration Hall adversary found none; and a final
1,600-iteration maximality-guided run kept its planted Hall obstruction at the
exact score ratio \(20669/26465\), with all three global maximizers
Hall-completable. See `PARTIAL_THRESHOLD_HALL_COMPLETION_TARGET.md` for the
claim boundary and artifacts.

## Independent gate reviews

Three bounded reviews finished before this checkpoint.

- The original Hall–pseudo-cycle skeleton is not justified: for Hall size
  three, deletion of the essential edge does not directly produce the needed
  champion entry. The weakest plausible replacement is a **deficient-block
  partial-restart lemma** allowing ownership to change while bundles outside
  the deficient block stay fixed. Its likely obstruction is cross-block EFX.
- A precise computational decision gate remains: delete the fixed perturbed
  good and permit at most one transfer among the remaining goods. Test whether
  the resulting partition always admits a partial EFX matching. This is viable
  in all Hall branches, but even a proof would be only an entry lemma unless it
  preserves a continuation invariant.
- In the seven-good Hall-size-four core, a seven-state
  **exchange-or-extra-wall** lemma may require only the local inequalities
  \(\delta<v_0(c)\) and \(\delta<v_0(d)\). The moving-agent inequalities are
  elementary; coupling the Hall witnesses across all seven feasibility graphs
  is the unproved part. Without those local wall-gap inequalities, radius two
  is false by an exact positive counterexample.

## Best restart point

Do not restart the strict-minimum CEGAR merely to accumulate more blockers.
First decide the following analytic fork:

> If every direct insertion at every threshold-maximal eligible state fails
> Hall, can its deficient set be converted either into a strict increase in
> normalized owner-threshold potential or into an equal-potential move that
> strictly reduces a finite Hall-defect invariant?

Do not begin another broad search before attacking this analytic gate. If it
stalls, encode the abstract deficient-set exchange rather than accumulating
more fixed-size positive instances; do not treat bounded UNSAT alone as
resolution.

For general \(n\), the cap-free transfer-component and dependency-cycle lemmas
survive, but the four-agent almost-complete starting theorem does not. A general
resolution therefore needs an additional induction/partial-allocation
invariant after the four-agent conversion mechanism is understood.

## Related detailed checkpoint

The exact strict-minimum solver state, tie correction, and longer replay command
remain in `results/PARTIAL_HALL_CONVERSION_CHECKPOINT_20260802.md`.

# Minimum-slot orbit completion target

## Candidate four-agent theorem

Let \((X,f)\) be a globally normalized-owner-threshold-maximal eligible
one-floater EFX allocation for four positive-additive agents.  Select one
owner-minimum good \(g_i\in X_i\) from each bundle and freeze the four cores

\[
R_i=X_i-\{g_i\}.
\]

Consider the at most

\[
5!=120
\]

states obtained by permuting the five tokens

\[
g_0,g_1,g_2,g_3,f
\]

among the four parking slots attached to \(R_0,R_1,R_2,R_3\) and the floater
slot.  Retain only eligible states.

The live theorem target is:

> For some choice of the four tied owner minima, the eligible part of this
> minimum-slot orbit contains a state whose floater can be inserted into one
> core-plus-token bundle and whose four complete bundles admit an EFX perfect
> matching.

By the minimum-slot permutation plateau lemma, every eligible orbit state is
another global threshold maximum.  Therefore this target, combined with the
known existence of a four-agent EFX allocation with one unallocated good,
would prove complete additive EFX existence for four agents.

This is not proved.

## Adversarial update

The fixed-core statement is false without global maximality, already in the
canonical (4\times9) pair-base stress cell.  Exact CEGAR has constructed
positive valuations with unique owner minima for which every eligible state
in the complete 120-state token orbit is Hall-blocked.  In all such models
found, however, the canonical base is not globally threshold-maximal.

After 141 cumulative rounds the exact search contains 137 orbit-completion
blockers and 42 global-maximality witnesses, with no globally maximal blocked
orbit and no UNSAT proof.  A separate exact-preserving anneal raised a blocked
orbit's fixed-to-global threshold ratio from 0.848293 to 0.961317.  Its best
Hall deficit is (1/55584), but its threshold-maximality deficit remains
(3857/55584).  The winning competitor moves core goods, so it lies outside
the five-token orbit.

The corrected live alternative is therefore: orbit blockage must force either
a completion inside the orbit or an eligible positive-gain core-token
exchange.  See `PARTIAL_THRESHOLD_CORE_TOKEN_EXCHANGE_GATE.md` for the exact
artifacts and claim boundary.

The nearest-higher-state audit sharpens "core-token exchange" to a finite
balanced menu: 32 swaps and 112 three-slot cycles.  A positive exact boundary
model has no improving swap but does have an improving three-owner cycle, so
cycles are necessary.  The current canonical-pair target is to prove that this
distance-three menu always contains a gain whenever the token orbit is
blocked.  Its arbitrary-core generalization remains the theorem needed for
four-agent EFX.

## Why this is the current highest-leverage gate

The target keeps arbitrary bundle sizes inside the frozen cores but reduces
the exchange dynamics to five named tokens.  It contains:

- all owner-minimum floater swaps;
- owner-minimum exchanges between bundles;
- longer parking cycles; and
- the simultaneous cycle moves needed to cancel local EFX-wall dependencies.

It also respects the exact negative evidence.  Purely local two-source and
fixed-radius old-good exchange lemmas are false away from the global threshold
plateau, while every eligible minimum-slot permutation at a true global
maximum is automatically threshold-neutral.

## Exact evidence

The exact-rational artifact
`partial_hall_threshold_plateau_exact_path_audit.json`, SHA-256
`16d1d9041c32278cf243462d8bea679926cced30817c21b34b9f2f53448fcdb2`,
checks all 15,557 global threshold maxima in the 46-profile hard corpus.
Every one of the 7,655 blocked maxima reaches a completing maximum through a
strictly Hall-margin-increasing path inside one fixed-core, five-token orbit.
The maximum path length is two.

This is much stronger than the originally selected 4,847-state census, but it
is still finite evidence.  Every audited profile already has a completing
global maximum.

## Analytic route

Choose an eligible orbit state maximizing \(H\).  If \(H<0\), take a strict
bottleneck Hall cut.

1. In the full-cut branch, use the one-bottleneck normal form: one equality
   edge enters the unique missing bundle and the other three matching edges
   are strict.
2. Attempt the two canonical token transpositions.  A successful one strictly
   crosses the critical cut.
3. If a transposition is ineligible, record its exact incoming-target or
   owner-shortfall wall.  Follow the required token to another parking slot.
4. Finiteness of the five slots produces a directed token cycle.  Apply the
   entire cycle simultaneously; threshold maximality is preserved by the
   permutation lemma.
5. Prove that either the cycle state is eligible and strictly augments the cut,
   or its remaining walls identify a positive-gain core-token exchange.
6. Use global threshold maximality to exclude that exchange.  This is the new
   gate exposed by the adversarial models; a contradiction confined to frozen
   cores is not currently justified.

The size-two and size-three critical cuts require the same construction with
multiple equality edges crossing the cut.  The bottleneck cut lemma supplies
their exact multiplicity.

## General-EFX boundary

The token-orbit target would resolve the four-agent one-charity-good problem,
not general additive EFX.  General EFX still requires a compatible way to
choose and absorb a token from a charity set containing several goods.  The
charity Hall-absorption equivalence identifies that later gate, but does not
prove it.

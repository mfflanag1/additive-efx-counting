# EFX breakthrough route audit — 2026-08-03

## Decision

The campaign is not continuing the previous completion-cut search.  That
route hit the predeclared diminishing-return boundary: the last exact
all-strict cover closed 2 of 16 leaves and timed out on 14 twice, without a
model.  It remains frozen as a reproducible bounded result.

The current primary route is the charity Hall-absorption program, but only
under an adversarial survival rule.  It is retained because one explicit
lemma would imply both four-agent and general additive EFX, not because it is
the newest route.  The proof search is being widened with owner-Pareto
exchange cycles imported from a separate constructive paradigm.

## Route tournament

| Route | Theorem leverage | Present evidence | Main risk | Decision |
|---|---:|---|---|---|
| Charity Hall absorption | Resolves four-agent and general EFX from known partial-allocation theorems | Exact matching equivalence; cap-free plateau and obstruction lemmas; selector survives every scanned profile | The absorption-gradient statement may hide all the original difficulty | Primary, with falsification gates |
| Four-agent champion-cycle completion | Directly resolves four agents | Starts from the published one-charity theorem and has a finite four-vertex obstruction graph | Existing proofs already stop at the final unallocated good; case explosion | Secondary language for proving the four-agent specialization |
| Owner-Pareto swap saturation | Strengthens either route, but does not alone absorb charity | Cap-free plateau lemma; closely parallels a successful four-agent EF2X technique | Third-party EFX constraints can block otherwise improving swaps | Newly activated auxiliary route |
| Unit-bundle/dumping decomposition | Resolves arbitrary-agent multigraph valuations | The June 2026 algorithm makes progress by fixing two-agent unit bundles and shortening envy paths | A general additive good has no canonical pair of incident agents, so the invariant does not lift directly | Mine its rerouting idea, reject a direct reduction |
| Growing near-diagonal theorem, e.g. \(m\leq2n\) | Would imply general EFX by Neoh--Teh's padding theorem | Several structural pair/favorite lemmas already proved | Prior fixed-shape selectors and local augmentations have exact counterexamples | Keep as independent fallback, not current engine |
| Nash/price extremum | Potentially general | Maximum-Nash direct-completion selector has an exact refutation | Optimizes the wrong local object | Retired unless a genuinely new invariant appears |
| Fixed-cell SAT/CEGAR closure | Can settle bounded cases and mine lemmas | Strong finite exclusions and 127/128 sign regimes | Solver growth is not converting to a cap-free theorem | Diagnostics only; no open-ended continuation |

## Adversarial survival evidence

For the selector that first maximizes normalized owner-threshold potential
and then maximizes charity-absorption margin:

- every eligible maximum absorbed in 199 random positive \(4\times8\),
  charity-size-two profiles;
- the selector absorbed on all 47 stored hard profiles at charity size two
  and all 30 admitting a charity-size-three state;
- it absorbed on all 22 eligible random \(5\times8\), charity-size-two
  profiles;
- every one of 288 one-entry replacements around a zero-margin boundary
  remained nonnegative; and
- a 241-profile simulated-annealing walk beginning on a zero-margin boundary
  also found no negative margin.

The follow-up stress pass adds:

- a 161-profile exact adversarial walk from a zero-margin \(5\times8\),
  charity-size-two boundary;
- a constructed eligible \(5\times9\), charity-size-three zero-margin
  boundary and a 101-profile adversarial walk from it; and
- seven exhaustive normalized integer domains containing 811,315 distinct
  valuation profiles in total. These include all rowwise-primitive
  \(3\times4\), cap-three profiles at charity size one and all
  \(3\times5\), cap-two profiles at charity size two. No negative selector
  margin occurs; 153,675 profiles lie exactly on margin zero.

These are falsification attempts, not a theorem.  A single negative profile
retires the extremal selector immediately without refuting EFX existence.

## Anti-local-minimum gates

The absorption route continues only while it passes all three gates:

1. **Counterexample gate.** Search directly for a negative-margin global
   threshold maximum, especially beyond \(n=4\), rather than accumulating
   only positive random samples.
2. **Proof-compression gate.** Every computational pattern must become a
   cap-free Hall, exchange, or wall-cycle statement.  More solver cuts without
   a shorter analytic invariant do not count as progress.
3. **Move-completeness gate.** Do not assume charity/minimum swaps are the
   only useful moves.  Include owner-Pareto exchange cycles and generalized
   champion cycles, then classify the residual obstruction after saturation.

## Immediate analytic target

Choose a fixed-charity-cardinality EFX state lexicographically maximizing
\((\Theta,\Lambda)\), where \(\Theta\) is normalized owner-threshold potential
and \(\Lambda\) is the lexicographically maximum sorted vector of all matched
Hall slacks. Its first coordinate is the old bottleneck margin \(\beta\).
Saturate the state under:

1. eligible charity/minimum exchanges;
2. eligible owner-Pareto item-exchange cycles; and
3. eligible connected transfer unions with positive total normalized-
   threshold gain, even when some participating owner loses; and
4. bundle rematchings certified by the Hall graph.

The owner-exchange equality characterization proves that strict Pareto cycles
on the plateau only permute unique minimum-slot tokens. They cannot supply the
core-changing moves seen in the hardest exact boundaries. The third move
class is therefore essential: global maximality excludes every eligible
positive-*total*-gain union, not merely exchanges that improve each owner.

If \(\Lambda_1=\beta<0\), take an inclusion-minimal strict Hall cut. The next proof
unit is to show that the opposite-sign eligibility walls around this cut
either form an admissible exchange cycle crossing the cut or sum to an
eligible positive-total-gain transfer union. If neither exists, the walls
must sum to an impossible strict inequality cycle. The full signature allows
tight matching edges to be improved sequentially rather than all at once.
For four agents the proper cuts have
sizes two and three and the full cut has the one-bottleneck-edge normal form,
so this is a finite *structural* classification rather than another valuation
cap search.

The first exchange certificate in that classification is now proved: if each
matched bundle receiver likes its incoming exchange good and every external
observer weakly prefers the outgoing good, all matched Hall slacks improve
coordinatewise. Hence any failed certificate supplies a specific external
observer with the opposite strict sign. The remaining theorem must show that
these observer dependencies close into a profitable eligible transfer union
or an inconsistent strict cycle.

## Stop/switch conditions

Switch away from the primary route if any of the following occurs:

- an exact negative selector profile is independently replayed;
- a complete four-agent wall-cycle classification contains a realizable
  saturated obstruction with no improving move; or
- two further bounded research passes add no cap-free implication beyond the
  current obstruction taxonomy.

Absent one of those events, the route remains the highest-leverage live
program because its successful endpoint is exactly the two requested
theorems, while the independent near-diagonal route requires another global
reduction after its own hard combinatorial lemma.

## Primary literature anchors

- Berger, Cohen, Feldman, and Fiat, *(Almost Full) EFX Exists for Four Agents
  (and Beyond)*, arXiv:2102.10654.
- Ashuri, Gkatzelis, and Sgouritsa, *EF2X Exists for Four Agents*,
  arXiv:2412.00254.
- Neoh and Teh, *Understanding EFX Allocations: Counting and Variants*,
  AAAI 2025 / arXiv:2504.03951.
- Afshinmehr et al., *EFX Allocations Exist on Multi-Graphs*,
  arXiv:2606.18665.

## Claim boundary

No four-agent or general additive EFX theorem is claimed.  The audit records a
research-direction decision, proved supporting lemmas, falsification results,
and explicit conditions for abandoning the current route.

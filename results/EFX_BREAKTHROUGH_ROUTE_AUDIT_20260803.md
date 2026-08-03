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
\((\Theta,U,\Lambda)\), where \(\Theta\) is normalized owner-threshold
potential, \(U\) is the owner-utility vector in an arbitrary fixed agent order,
and \(\Lambda\) is the lexicographically maximum sorted vector of all matched
Hall slacks. Its first coordinate is the old bottleneck margin \(\beta\).
The utility layer excludes threshold-neutral Pareto-improving champion cycles;
Pareto improvement alone does not imply an increase in \(\Theta\).

This revised order has been tested exactly on 47 hard profiles--the complete
46-profile plateau corpus plus the Chaudhury lex-potential counterexample--for
all 24 agent orders. Every one of the 1,128
profile/order-specific \((\Theta,U)\)-maximal tie sets contains an absorbing
state, so the final \(\Lambda\) tie-break selects one. This is exact corpus
evidence only; the cap-free selector theorem remains the target. See
[`threshold_utility_tiebreak_corpus_audit.json`](threshold_utility_tiebreak_corpus_audit.json).
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

The dominant four-agent subcase is now separated completely. Across 4,847
selected exact plateau transitions, 4,323 have an identity optimal matching,
one negative slack, and a one-step completion. In 4,320 of them the unique bad
agent receives the charity good, releases one owner minimum, and that minimum
replaces the charity good in the same old host. The cap-free unique-defect
handoff lemma proves that this move completes whenever its eligible-swap,
two-external-row, and one bad-row conditions hold. The remaining proof task is
existence of such a released minimum at the extremal state, not verification
of the resulting allocation.

Under the earlier \((\Theta,\Lambda)\) selection, the lexicographic signature
removed even the handoff's bad-row closure requirement. If the released owner
minimum produced an eligible swap, both external rows ranked it below the old
charity good, and the bad row ranked the charity good strictly above it, the
new identity candidate improved its unique negative slack while every other
slack stayed nonnegative. That argument remains valid for the older extremum
but cannot be invoked after inserting \(U\) unless the utility vector is also
preserved.

The Pareto-sensitive utility layer supplies a different, stronger test. By the
owner-minimum swap lemma, every eligible such swap is \(\Theta\)-neutral at a
global maximum. If the bad row strictly prefers the charity good to the
released minimum, the swap itself strictly improves \(U\), before any
completion is attempted. Under the revised extremum the full-witness handoff
therefore needs only an eligible bad-owner minimum with that strict order;
the two external item orders and Hall signature are unnecessary in this
subcase.

The matching side of this gate is also completely classified. Every
four-agent unique-defect failure has one of only three Hall witnesses: the
bad/host pair sees only the host; the bad/host/one-external triple sees only
the host and that external's bundle; or the full set is deficient because
nobody accepts the bad bundle. This replaces the arbitrary 16-edge graph by
three cap-free valuation cases.

The exact data aligns perfectly with that trichotomy: all 4,320 canonical
bad-source handoffs are full witnesses; the three noncanonical transitions
are precisely two pair records and one triple record. The pair uses an
external-source charity swap, while the triple uses an allocated-bundle swap
and nonidentity rematching. The proof should therefore attack the full
witness with the minimum handoff and reserve distinct exchange arguments for
the two proper-cut cases.

A fresh anti-overfitting test rejects a tempting shortcut inside the full
witness. The corpus suggests that redirecting the charity good from host
\(h\) to the unique bad bundle \(b\) either absorbs or leaves only \(h\) bad.
This is false without global extremality: an exact positive-additive
four-agent, six-good witness makes two external agents bad after redirection.
The same state is nevertheless directly absorbable through a third host, so
it does not challenge the selector. See
[`PARTIAL_THRESHOLD_HOST_REDIRECTION_AUDIT.md`](PARTIAL_THRESHOLD_HOST_REDIRECTION_AUDIT.md).
Any valid redirection argument must therefore use global
\((\Theta,U,\Lambda)\)-maximality; the local Hall topology alone is
insufficient.

The next adversarial layer retires bounded local gradients even inside the
full/unique-defect branch. State-level reciprocity, minimum swaps, and the
complete radius-two menu all have exact counterexamples. A targeted walk then
found a full/unique-defect profile with no improving state through radius
three. Its first escape is one connected radius-four component spanning all
four owners and leading directly to absorption. See the
[`full unique-defect connected-component gate`](PARTIAL_THRESHOLD_FULL_UNIQUE_DEFECT_COMPONENT_GATE.md).
The proof must therefore cancel Hall walls over whole connected owner
components; another fixed-radius ladder is explicitly retired.

The cap-free transfer-component hybrid lemma supplies the replacement
invariant. Between any two fixed-charity EFX states, owner-threshold gain is
exactly additive over transfer components, and every infeasible partial
component is blocked only by an EFX/charity inequality crossing its component
cut. This converts the remaining problem from item-radius enumeration to a
dependency-growth and wall-cancellation statement, uniformly for four and
arbitrary numbers of agents.

The unique-defect hypothesis also now connects rigorously to the independent
champion-cycle route. The bad agent is the unique strong envier of the
augmented host and therefore \(f\)-champions that host. Its minimal desired
subset either discards exactly \(f\), producing an ordinary envy edge, or
retains \(f\) and releases a nonempty bottom bundle. This bridge supplies the
EFX-preserving construction mechanism that raw transfer walls lacked.

The hardest radius-three counterexample confirms that this is not merely a
change of terminology. Its forced champion edge and one reciprocal champion
edge form an ordinary-envy/champion two-cycle whose Pareto-improvable
reallocation is EFX with charity, strictly raises \(\Theta\), and is directly
absorbable. Thus the champion construction recovers an improving four-good
connected transfer that every item-local move through radius three misses.
The exact endpoint and replay are recorded in
[`unique_defect_radius3_gradient_counterexample.json`](unique_defect_radius3_gradient_counterexample.json).

This also sharpens the next decision gate. The live task is not to search for
larger-radius moves; it is to classify the four-vertex champion graph around
the forced edge and prove that either a charity-cardinality-preserving champion
edge set has nonnegative total threshold change or the signed component walls
force a different positive-threshold transfer. A merely Pareto-improving edge
set is insufficient.

That distinction is exact, not cosmetic. All 4,320 full/unique-defect corpus
states have a reciprocal singleton-discard champion two-cycle with exactly
zero threshold change, so the new utility tie-break excludes every one. A
separate positive \(4\times6\) state satisfies the same local Hall/champion
topology but both reciprocal cycles lower \(\Theta\) by \(31/1430\). It lies
strictly below two absorbing global \(\Theta\)-maximizers. Thus global
maximality or signed-wall cancellation is genuinely necessary. See the
[`reciprocal-champion threshold gate`](RECIPROCAL_CHAMPION_THRESHOLD_GATE.md).

The first wall-propagation step is now cap-free. At a fixed-cardinality
\((\Theta,U)\) maximum, every owner-improving charity/minimum swap is
ineligible and produces, in another agent's row, either a positive
incoming-target sign or an opposite charity sign. With one charity good and a
nonsingleton source, only the positive sign remains, in the sharpened form
that the blocker ranks the floater above both the released minimum and its
least-valued remaining source good. The incoming wall also constructs a
generalized \(\{f\}\mid\{g\}\)-champion edge releasing \(g\). Thus the live
gap is now cycle closure/cardinality control, not conversion of walls into
champion edges. The apparent singleton exception is also eliminated:
successive charity walls form a nonrepeating chain of singleton owners and
must terminate at a nonsingleton positive target wall, since any repetition
would be a threshold-neutral Pareto-improving singleton cycle.

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

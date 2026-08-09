# Four-agent EFX breakthrough restart

**Date:** 2026-08-09
**Research objective:** prove that every four-agent additive-goods instance
admits a complete EFX allocation, for an arbitrary number of goods
**Current status:** open; no complete proof is claimed

## Breakthrough target

> **Target A — four-agent additive EFX.** For every finite set of goods and
> every four nonnegative additive valuations, there is a complete EFX
> allocation.

This is the smallest unresolved agent count for general additive goods. A
proof would be a genuine mathematical breakthrough. It would not resolve
the problem for five or more agents.

The working contradiction setup starts from Berger--Cohen--Feldman--Fiat
(BCFF). In a hypothetical counterexample, choose a globally
lexicographically maximal partial EFX allocation. The established reductions
give one unenvied charity good, four nonempty allocated bundles, and at least
two nonsingleton bundles.

## What is already closed cap-free

1. **Zero or one nonsingleton bundle.** The one-large champion reduction
   either completes EFX or produces forbidden lexicographic/Pareto progress.
2. **Exactly two nonsingletons, shortest genuine cycle of length two.** The
   trapped-source return theorem closes all distinct- and shared-source
   cases using singleton envy returns.
3. **Local alternating-cycle shortcuts.** Every compatible cross-bottom
   shortcut would be a forbidden PI certificate. An exact seven-good
   obstruction proves that such shortcuts need not exist even at an
   EFX-Pareto-maximal state. Therefore a Pareto-only completion of this
   proof route is impossible.

These are structural theorems for arbitrary bundle sizes under the BCFF
positive/nondegenerate convention, not bounded-value searches. Their
nonnegative/tie wrapper and external human review remain outstanding.

## Immediate theorem target

> **Target B — priority-sensitive two-large closure.** A globally
> lexicographically maximal noncomplete four-agent EFX state cannot have
> exactly two nonsingleton bundles.

The shortest genuine champion cycle leaves three residual topologies:

| Residual | Exact missing step |
|---|---|
| Length three | reroute a bottom edge whose source is the second large owner or the external singleton |
| Length four, adjacent large targets | escape a source trapped in the downstream two-vertex envy segment |
| Length four, alternating large targets | construct a lexicographic reallocation even when all four compatible cross-bottom families are absent |

The alternating case is the discriminating gate. Its candidate lemma is:

> For the fixed priority order, an alternating state with all four compatible
> cross-bottom families empty admits an EFX reallocation that preserves every
> earlier-priority utility and strictly raises the first utility that changes.

The statement must permit sacrifice of later-priority agents. The frozen
profile `V*` is EFX-Pareto-maximal and blocks all local families, yet has an
EFX escape for every possible first-priority agent.

## Immediate computational experiment

Build an exact global-lex CEGAR for the minimal `2+2+1+1` atom:

1. fix the alternating base allocation and one priority order;
2. impose positivity, subset nondegeneracy, EFX, charity dominance, the
   exact chordless champion cycle, and absence of all compatible families;
3. for every rival partial allocation, require either an EFX violation or
   failure to lexicographically dominate the base;
4. search all priority-role types;
5. if SAT, audit the model exactly and use it to repair or refute Target B;
6. if UNSAT, shrink the rival/inequality core and convert the recurring
   escape motif into a human lemma valid for arbitrary bundle sizes.

**Current outcome.** The exact seven-good atom is UNSAT for all 24 priority
orders. Sixteen orders have a one-rival certificate and the largest of the
remaining deletion-minimal menus has five rivals. See
[ALTERNATING_GLOBAL_LEX_ATOMIC_THEOREM.md](ALTERNATING_GLOBAL_LEX_ATOMIC_THEOREM.md).
The live task is now the cap-free packet lift, not further priority-order
enumeration.

This experiment is a lemma discriminator, not a finite-case theorem. An
UNSAT result for seven atomic goods is publishable evidence only after its
core is converted to a cap-free analytic argument.

## Full proof ladder after Target B

1. Prove the priority-sensitive alternating escape.  Eighteen of its 24
   priority-role orders are now closed cap-free: the original sixteen easy
   orders plus `(p,q,r,s)` and `(s,r,q,p)` by the
   [root-flip lemma](ALTERNATING_ROOT_FLIP_LEMMA.md).
2. Reuse its exchange invariant to close the length-three and adjacent
   length-four residues, yielding Target B.
3. Generalize the invariant from two bottom packets to three nonsingleton
   bundles. The desired statement is a packet-flow augmentation lemma: a
   lex-maximal obstruction has a compatible closed exchange or contracts to
   a state with fewer nonsingleton bundles.
4. Extend the same contraction/closed-flow dichotomy to four nonsingleton
   bundles.
5. Combine those cases with BCFF's one-charity theorem and the one-large and
   length-two reductions to prove Target A.
6. Add the perturbation/limit wrapper for nonnegative valuations and ties.
7. Obtain two independent mathematical reviews, then formalize the finite
   graph/case layer and release a referee-grade proof package.

## Parallel falsification target

The existing adaptive-priority direct-insertion conjecture remains a useful
secondary route: at least one priority order might have an insertable
lexicographic maximum. Its fixed-order version is already refuted, and exact
work has closed only finitely many candidate cells. It should receive
bounded falsification effort, not displace Target B unless it yields either
a full counterexample across all priority groups or a small recurring
analytic core.

## Stop/go criteria

- **Continue the alternating route** if exact models repeatedly expose a
  small menu of priority-dependent escape allocations or UNSAT cores shrink
  to a bounded family of inequality motifs.
- **Repair the lemma** if a globally lex-maximal atom exists; identify the
  weakest additional premise forced by a hypothetical no-complete-EFX
  instance.
- **Pivot away** if several structurally distinct SAT models defeat every
  natural priority potential and no invariant survives.
- **Do not count as breakthrough:** a fixed value cap, a fixed number of
  goods, a solver stall, an empirical floor, or an unreviewed proof sketch.

## Durable evidence

- [One-large champion closure reduction](ONE_LARGE_CHAMPION_CLOSURE_REDUCTION.md)
- [Two-genuine-edge recycling reduction](TWO_GENUINE_EDGE_RECYCLING_REDUCTION.md)
- [Length-two trapped-source closure theorem](TRAPPED_SOURCE_RETURN_LENGTH_TWO_CLOSURE_THEOREM.md)
- [Alternating local obstruction](ALTERNATING_CROSS_BOTTOM_LOCAL_OBSTRUCTION.md)
- [Exact alternating-obstruction audit](alternating_cross_bottom_obstruction_audit.json)
- [Alternating global-lex atomic exclusion](ALTERNATING_GLOBAL_LEX_ATOMIC_THEOREM.md)
- [All-orders minimal-core audit](alternating_global_lex_atomic_core_audit.json)
- [Anchored-or-promoted atomic target](ALTERNATING_ANCHORED_OR_PROMOTED_TARGET.md)
- [Cap-free alternating root-flip lemma](ALTERNATING_ROOT_FLIP_LEMMA.md)
- [Root-flip split-packet core audit](alternating_root_flip_split_core_audit.json)
- [Adaptive-priority completion target](ADAPTIVE_PRIORITY_COMPLETION_TARGET.md)

## Primary literature boundary

- Berger, Cohen, Feldman, and Fiat,
  [*Almost Full EFX Exists for Four Agents (and Beyond)*](https://arxiv.org/abs/2102.10654).
- Current general-open-status reference:
  [arXiv:2601.03438](https://arxiv.org/abs/2601.03438).
- A recent positive result for restricted multigraph valuation structure,
  not general additive valuations:
  [arXiv:2606.18665](https://arxiv.org/abs/2606.18665).

# EFX breakthrough alignment audit

**Date:** 2026-08-02  
**Goal:** complete additive EFX, beginning with a rigorous four-agent
one-unallocated-good completion theorem.  
**Verdict:** the Hall route remains plausible, but the fixed (4\times9)
rival-menu loop has reached its useful stopping point. Further menu growth
would be proof mining without a credible lift. The program must now operate at
arbitrary bundle size.

## The implication chain that would constitute a breakthrough

1. Begin with an arbitrary four-agent additive instance and an EFX allocation
   (X) with one unallocated good (f), supplied by the known almost-complete
   four-agent theorem.
2. Select (X) maximally from the finite family of eligible one-floater EFX
   allocations, using a potential or lexicographic rule.
3. If assigning (f), moving one old good, and rematching enlarged bundles all
   fail, extract a Hall-deficient pair of agents with one common acceptable
   bundle.
4. Convert that pair trap into another eligible partial EFX allocation with
   strictly larger selector value.
5. Contradict maximality, so a Hall completion exists and yields a complete EFX
   allocation.

Steps 3--4 are the central missing theorem. A proof for one fixed bundle shape
or nine named goods does not complete this chain.

## Results that genuinely transfer beyond the fixed cell

- The maximum-bundle neighbor lemma eliminates singleton Hall deficiency for
  arbitrary numbers of agents and goods.
- Transfer-component potential decomposes exactly for arbitrary additive
  instances.
- Failed component allocations induce a directed dependency cycle; this is
  cap-free in agents and goods.
- The two-wall conversion and six-wall replacement lemmas are cap-free local
  exchange theorems.
- The opposite-third-pairing lemma is cap-free in the number of irrelevant
  goods: seven explicit walls force a strict two-agent Pareto improvement.

These are useful ingredients because they speak about symbolic bundles and
comparison walls, not integer caps or one valuation corpus.

## Results that do not themselves advance the implication chain

- A 15-rival menu covering a finite corpus is not a theorem and is exactly
  refuted by a later SAT model.
- The seven- and eight-rival positive-sum conversions are exactly refuted.
- The nine-rival global gate is solver-unknown after 120 seconds.
- Frozen comparison-cell UNSAT cores prove only those cells until their wall
  patterns are abstracted and covered.
- The canonical shape
  ((\{6,7\},\{1,2,3\},\{0,4\},\{5\});f=8) has no proved reduction from an
  arbitrary four-agent one-floater allocation.

Accordingly, no further rival is to be added merely because it covers a new
model. A new fixed-cell computation is justified only when it decides a stated
abstract lemma or extracts a reusable symbolic wall pattern.

## Live theorem target

### Pair extraction: closed

The arbitrary-bundle statement is proved in the
[owner-minimum Hall-pair extraction theorem](PARTIAL_HALL_OWNER_MINIMUM_EXTRACTION_THEOREM.md).
Sixteen QF_LRA cases cover every singleton pattern; Z3 proves all sixteen
UNSAT and cvc5 independently proves the five symmetry representatives. Thus
every eligible four-agent one-floater EFX state either completes after direct
insertion or one selected owner-minimum transfer, or a candidate graph exposes
a two-agent/one-neighbor Hall trap. The earlier exhaustive audit of 128,131
eligible states is corroborating evidence, not the theorem's basis.
The bounded owner-minimum transfer subfamily also decides every audited state:
127,081 complete and 1,050 expose a pair trap. By contrast, direct insertion
alone has an exact positive $4\times9$ counterexample. Hence the live proof
must retain a transfer, but need not yet quantify over every old good.

### Abstract pair-trap exchange lemma

Let (X=(X_0,X_1,X_2,X_3);f) be a selector-maximal one-floater EFX allocation
for four positive-additive agents. Suppose every allocation obtained by
placing (f), moving at most one old good, and permuting the resulting bundles
fails EFX. Then some bounded union of transfer components yields an eligible
one-floater EFX allocation (Y) with strictly larger selector value.

The target must quantify over arbitrary finite bundles. Named-good lemmas may
be used only after translating their hypotheses into roles such as moving
good, displaced good, common Hall neighbor, observer, and dependency-cycle
edge.

The first exact conversion attempt is now resolved negatively. Allocating the
old floater and releasing one selected owner-minimum good does not always
produce an improving eligible state. The exact counterexample is not globally
utilitarian-maximal; its nearest improvement is a two-good swap at owner
distance two with gain $11/1072$. The active gate is therefore the
[pair-trap two-good conversion target](PARTIAL_HALL_PAIR_TRAP_CONVERSION_GATE.md),
not a return to unrestricted finite menus.

## Go/no-go gates

1. **Pair extraction (closed):** every Hall-blocked state supplies a
   two-agent/one-neighbor trap after an appropriate star move, without assuming
   the fixed (2+3+2+1) shape.
2. **Wall conversion (current active gate):** prove that every such trap triggers a cap-free exchange
   lemma or a weighted dependency-cycle contradiction.
3. **Eligibility preservation:** show the constructed exchange remains EFX and
   preserves floater nonenvy.
4. **Selector increase:** show strict increase in a well-founded selector.
5. **Completion:** apply Hall matching to the enlarged bundles.

Failure of gate 1 or 2 should be documented by an exact symbolic
counterexample and used to change the selector or move family. It should not be
answered by silently enlarging a finite menu.

## Honest distance assessment

The work now has a cap-free, dual-solver-verified pair-extraction theorem and
several local exchange lemmas. It is materially closer to a four-agent proof,
but the arbitrary-bundle pair-trap conversion theorem is still missing and is
logically indispensable. General $n$ is farther still. The highest-value next
result is a proof or decisive refutation of that conversion lemma.

# Dated prior-art note — four-split refutation and the five-edge whole-role closure (2026-08-26)

Scope: the statements in `FIXED_U_FOUR_SPLIT_EDGE_CAP_BOUNDARY_20260826.md`.  This is a
targeted positioning note, not a novelty opinion.

- **Chaudhury, Garg, Mehlhorn (EC 2020 / SICOMP).**  EFX exists for three additive agents.
  Our four-agent form-2 model starts where their case analysis ends; nothing here re-proves
  or contradicts the three-agent theorem.
- **Berger, Cohen, Feldman, Fiat (AAAI 2022; arXiv:2102.10654 full build).**  EFX for four
  agents with at most one unallocated good, via cancelable valuations and the "most envious
  agent" exchange.  Their donated-good mechanism is the ancestor of this program's charity
  source `p`; the four-edge support cap is a program-internal invariant, not a BCFF
  statement.  The consolidated corpus (`cc/consolidation-20260816`) audits the BCFF import
  separately; the present note relies on none of it.
- **Akrami, Alon, Chaudhury, Garg, Mehlhorn, Mehta (2022–2023).**  EFX with bounded charity
  and EFX for three agents with general monotone valuations.  Charity-bounded results are the
  right comparison class for a five-edge whole-role allocation: every allocation produced here
  is complete (no charity remainder), so bounded-charity theorems are neither used nor
  contradicted.
- **Alkassar, Fouz, Mehlhorn (arXiv:2608.08590).**  Complete EFX for four additive agents with
  at most nine goods.  The obstructing realization here has 23 physical goods; AFM does not
  apply, and every obstruction is cap-free SAT, so no EFX claim conflicts with AFM.  The
  program's rule "any candidate with at most nine goods is a bug" was checked and is vacuous
  for this cell.
- **Program-internal predecessors.**  `FIXED_U_SPLIT_SWITCHING_COMPLETION_THEOREM_20260821`,
  `FIXED_U_DYNAMIC_ANCHOR_EXTRACTION_REFUTATION_20260821`,
  `FIXED_U_PATTERN_DEPENDENT_MIXED_MENU_REFUTATION_20260821`.  Each quantified a *selector*
  over realizations; the present oracle quantifies an *allocation per cell* and is therefore
  strictly weaker as a hypothesis and strictly stronger as a refutation.

What is new relative to all of the above: (i) the exact realization cell with no four-edge EFX
allocation at any split count; (ii) the identification of the four-edge cap, not splitting,
as the operative obstruction (zero-split closure at five edges, 293/293 in the ledgers);
(iii) the symbolic whole-role edge-cap CEGAR over the form-2 master.  No claim about general
additive EFX is made.

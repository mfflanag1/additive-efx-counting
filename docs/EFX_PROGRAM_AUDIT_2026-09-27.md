# EFX research program: consolidated audit, 27 September 2026

This is the current navigation and claim-boundary record for the goods/counting
and adjacent chores program. It supersedes older status summaries, not the
underlying historical evidence. It is an internal source, literature and replay
audit, **not an independent proof of every archived theorem or external acceptance**.
The cooperative-game PXC/Lmin/Lmax program is separate and is not included here.

**16 October correction:** the selector/maximality portion of the admission gap
is closed by [BCFF-based repair](global-admission/RESTRICTED_SELECTOR_COMPATIBILITY_20261016.md).
The older A0 framing overlooked BCFF Theorem 5.1's improvement guarantee. This
does not establish physical fixed-U admission or general EFX.

## Bottom line

There are defensible paper-sized contributions, but no resolution of general
additive EFX and no verified final reduction that makes such a resolution imminent.
The cleanest result is the counting paper. The chores paper has a potentially
stronger existence increment, but its surviving novel range rests on less portable
computational evidence. The goods structural work is valuable chiefly as a
conditional exclusion theorem, exact obstructions to proposed completion rules,
and a much sharper description of the missing global argument.

Do not translate elapsed compute, the number of passed profiles, or the number of
refuted selectors into a percentage of the general theorem solved.

## 1. What the questions mean

For goods, EFX asks for an assignment of every item such that nobody envies another
person after **any one good is removed from that other person's bundle**. For
chores, the removal is instead from the dissatisfied person's **own** bundle.
The difference matters: a chores theorem is not a goods theorem.

The counting project asks a different question: when fair allocations exist, how
few labeled fair allocations can a valuation matrix have? An example with exactly
four fair allocations is an upper bound on the minimum possible count, not a proof
that every four-person instance has at least four, or even one.

The structural goods campaign starts with almost-complete fair allocations and
tries to redistribute packets to finish them. A failure of a particular packet
rule only refutes that rule. It is not a failure of EFX itself.

## 2. Contribution and confidence ledger

| Result | Exact scope and evidence | Current assessment |
|---|---|---|
| Six count-n examples | Positive additive instances at (4,7), (5,8), (6,9), (4,8), (4,9), (4,10), with exactly 4,5,6,4,4,4 labeled EFX allocations. Three implementations enumerate the allocations. | Strongest self-contained paper result. Candidate new minimum-count upper bounds; unrestricted lower-bound tightness is not proved. |
| Generalized parking criterion | Necessary and sufficient observer/host slack inequalities for assigning a leftover good to a fixed EFX base; seven exact certificates. | A proved local characterization and useful explanation of the witnesses. Do not market this elementary algebra alone as a field-level breakthrough. |
| Bounded counting theorem | Every positive integer 4-by-7 matrix with entries in {1,2,3,4} has at least four labeled EFX allocations. Reconstructed 1,240-allocation terminal pool, independent CNF, retained DRAT proof. | Finite computer-assisted theorem, subject to encoding correctness. The magnitude bound is essential to the claim. |
| Bounded two-safe-bundle theorem | External-observer lemma on the declared {1,2}^4 packet grid; checkpoint 723dec6 with independent replay and a finite census. | A bounded auxiliary result, not a cap-free lemma. |
| Two-nonsingleton composition | Consolidation at a8e925e proposes a repaired conditional exclusion argument and a nice-cancelable extension. Assumes a globally selected partial EFX state in the required one-charity normal form. | Substantial candidate structural theorem. BCFF imports and all composition cases still need external mathematical review. The selection interface is supplied separately by the 16 October BCFF repair corollary in the declared positive nondegenerate additive scope. |
| Four-edge completion obstruction | Exact physical cell defeats every allocation allowed by the declared four-support-transfer-edge model, including its permitted splits; five edges complete the cell. F4 checkpoint 712a40e. | A rigorous obstruction to that capped mechanism, NOT an EFX counterexample. |
| Dynamic-anchor, packet and normal-form classifications | Fixed-U model tests, exact residuals and the 316 atomic / 679 physical response-relation classifications. | Useful specification and falsification work; not universal physical admission or a general closure proof. |
| Three-agent common-three-value chores through m=11 | Entire positive ratio continuum, via structural/geometry reductions and finite profile sweeps. Evidence tiers differ sharply by m. | Specialist-review candidate. Current potentially novel existence window is m=9,10,11, not m=7..11. No complete Lean formalization or fresh full larger-range replay. |

The historical missing 45 entries in the counting search's terminal log were not
recovered. The paper instead uses an explicitly reconstructed sufficient terminal
pool. The displayed (4,7) count-four witness is outside the bounded {1,2,3,4}
box; combining those two facts does not prove an unrestricted equality theorem.

## 3. What changed or was withdrawn

1. **Small goods existence is no longer the novelty target.**
   [Alkassar–Fouz–Mehlhorn, arXiv:2608.08590](https://arxiv.org/abs/2608.08590)
   gives four-agent additive existence through nine goods. Earlier local (4,8)
   existence work cannot now be sold as the program's frontier contribution.
   Counting those allocations remains a separate question.
2. **The floor-reset T_L,times closure is retired.** The other EFX task's older
   final answer described a complete proof at 34709c9. The later August 16 referee
   report and model checks supersede it: the legal successor/containment and
   well-foundedness steps were not established. Arithmetic tests did not prove
   those steps. Use the consolidation branch, not the optimistic earlier summary.
3. **Four support-transfer edges are insufficient for the exact F4 cell.**
   Specifically this is the pattern-mixed profile `fixed_u_tame_or_anchor_cegar_20260821.json`,
   with two-good side bits `{gq:r,h:r,j:d,j:q,l:r,m:s}=1`, all others zero.
   Increasing split freedom did not repair its cap. The same cell has a five-edge
   EFX completion, so there is no contradiction to general existence.
4. **Exactly five response edges was an inserted hypothesis, not a theorem.**
   The proposed mandatory d-to-r response is absent in 363 of 679 physical-master
   relations. Response edges and allocation transfer edges are different objects.
5. **Seven and eight chores have been overtaken in existence scope.**
   [Zhang, arXiv:2609.10585](https://arxiv.org/abs/2609.10585), submitted 6 September,
   claims all nonnegative additive three-agent instances with seven or eight chores,
   a class containing our common positive three-value setting. It is an unrefereed
   computer-assisted preprint; this audit verifies its stated scope, not its proof.
   We found no direct overlap covering our whole nine-to-eleven range. That negative
   search is provisional, not a priority certificate. Shared-minimum nine-chore
   cases also follow from the cited insertion approach; the paper flags this overlap.

The broad monotone/submodular EFX counterexamples in
[Akrami et al.](https://arxiv.org/abs/2604.18216) are not additive counterexamples.
The goods additive counting conjecture and the general goods existence problem
must not be confused with their broader-class counterparts.

## 4. What the later goods work actually buys

The F4 handoff describes 408 retained profiles: one refuted capped case, 405
profiles reported closed at four edges and at most three anchor splits, and two
UNKNOWN/timeouts. Its closing-cover result quantifies over the declared relaxed
realization space of each fixed profile, not the entire infinite master.
The separate archived one-hot verification has 404 fully passing records out of
407, two records without checks, and one passing cover whose lower-split-cap
minimality check returned UNKNOWN. Thus it does not independently verify every
minimality assertion in the prose. The four focused tests were rerun on
27 September; the full 408-profile campaign was not. UNKNOWN is not UNSAT, and
relaxed marginal profiles need not be physical games.

Do not confuse the F4 cell with the different six-response physical residual in
section 4-prime of the normal-form theorem: that other residual **does** close at
four edges using one split role (menu six over its two-good realizations).

The most consequential finding is the **admission gap**. The physical fixed-U
master encodes selected base layouts, role totals/minima, bounds and packet
inequalities (P1–P9). The global lexicographic condition, PI-freeness, reachability,
exact response-count claim, desired cores and saturation (P10–P15) are not encoded
in that master; parts of P13 are separately derived or verified, while other
parts are assumed or inserted. P1–P9 themselves include an underived value box
`v<16`, fixed support layout and chosen root-facing branch. The completed
classifications therefore describe their models,
not every arbitrary four-agent instance. Neither the form-2 nor the larger
physical five-edge continuation had a completed universal certificate in the
reviewed checkpoints.

In ordinary language: we have studied how to finish a carefully arranged puzzle,
and learned several ways that do not always work. We have not shown that every
original puzzle can first be put into that arrangement. Proving that admission
step is higher-value than solving more examples of the arranged puzzle.

## 5. Review depth and remaining external obligations

**Counting:** three-way exhaustive witness checks, exact parking certificates
and the full retained DRAT proof were rerun on 27 September. Together with
historical independent encoding work, these support a focused
specialist review now. Still audit the mapping from valuations to CNF, slot
protection/completeness, reconstruction, and the literature claim about counts.
DRAT checking verifies a propositional formula, not the mathematical encoding.

**Chores:** exact independent geometry and representative differential checks are
good evidence. The complete historical m=7 sweep recorded 227 direct DRAT checks,
but deleted the proofs and retained hashes/verdicts. One regenerated proof is
retained in the September 5 review packet. The m=8..11 sweeps are not all
proof-producing; the higher rungs also use learned menus and cited safe-complement
theorems. Hash consistency is not a new solver execution. The full eleven-item
theorem is not a Lean theorem. A specialist should audit the quotient, geometry,
menu exhaustiveness, positive-cost conventions, safe-complement imports and the
surviving m=9..11 novelty before submission.

**Structural goods:** source and premise review plus focused regressions; not a
fresh audit of every search in the archive. External review should start with the
conditional two-nonsingleton theorem, the corrected selection import and physical admission, then the physical
four-edge obstruction. The retired closure must remain retired unless a new proof
fixes the actual missing transition.

AI cross-review this round independently found the chores novelty change and
proof-retention/timing overstatements. Findings were checked against primary
sources and the repository records before edits. Such review is not specialist
acceptance or a mathematical correctness certificate. Detailed checks are in
[the dated replay record](audit/2026-09-27/VERIFICATION.md).

## 6. Git preservation and navigation

The primary repository is
[mfflanag1/additive-efx-counting](https://github.com/mfflanag1/additive-efx-counting).
The chores repository is
[mfflanag1/counterexample-hunt, efx2](https://github.com/mfflanag1/counterexample-hunt/tree/main/efx2).
Both were private when inspected; no visibility change is authorized or made.

Main is the reviewed publication/index surface, not the union of every experimental
branch. This update brings the September 5 review preparation into version control,
adds the current audit and admission brief, and preserves the missing F4 branch.
It does not silently merge unproved research statements into the counting paper.
See [the pinned branch index](RESEARCH_BRANCH_INDEX.md).

The old standalone review ZIPs remain unchanged locally. Their manifests bind
their original standalone directory layout, not today's repository. The imported
review directories explain that distinction. No compiled solver binaries, huge
regenerable live-row tables, temporary runs or PXC branches are part of this update.
Vanished untracked scratch files in old temporary worktrees are not claimed recovered.

## 7. Highest-value next steps

1. Send the counting manuscript and compact replay package to a fair-division
   specialist. Ask specifically about the count-minimum novelty and bounded-CNF
   reduction, not whether this solves general EFX.
2. Review the chores m=9..11 reduction independently. A retained, independently
   checkable certificate for a surviving novel rung is more valuable than more
   low-item computation now covered by broader work.
3. Resume goods only against [ADMIT4](global-admission/GLOBAL_ADMISSION_CAMPAIGN.md).
   The joint selection gate is now closed using BCFF Theorem 5.1, not merely its
   existence corollary. Next derive the physical role/support/base extraction
   from that selected state, including all alternatives and original goods.
   A counterexample to an unconditional sublemma need not refute admission
   under a no-complete-EFX antecedent.
4. After admission, close the entire admitted physical domain and prove pullback
   and termination. Admission alone does not prove local closure, and closure alone
   does not prove admission. The starting target fixes an owner priority and
   assumes nondegenerate positive valuations; use the corrected selection and supply
   the tie/zero extension before asserting the unrestricted four-agent theorem.
   Four-agent existence for arbitrary item counts would
   itself be a major advance, but would still not settle arbitrary-agent EFX.

**Level:** credible specialized research-paper / thesis-chapter contributions,
conditional on the indicated external checks; no established field-level
breakthrough. The honest progress is a better-founded publication portfolio and
a sharper, still substantial missing theorem—not a nearly completed general proof.

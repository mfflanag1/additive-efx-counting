# Restricted selectors and improving exits: the BCFF repair

Date: 16 October 2026. Status: conventional corollary of a published theorem;
independent source review and exact calibration passed. This corrects the program's
admission audit. It is not a new four-agent EFX existence theorem.

## 1. Frozen instance, selection class, and priority

Exactly four labeled agents N share a finite set G of ORIGINAL goods. Valuations
are additive, strictly positive, and bundle-nondegenerate: distinct subsets have
distinct values for each agent. The verifier uses rational inputs; the argument
also permits real values. No packet graph, bundle shape, goods count, or transfer
cap is assumed.

A state A=(A_0,A_1,A_2,A_3;P_A) partitions G, including its unallocated pool P_A.
EFX means v_i(A_i)>=v_i(A_j minus {g}) for every i,j and every g in A_j.
Charity safety means v_i(A_i)>=v_i(P_A) for every i. Fix a permutation pi ONCE.
The priority objective u_pi lists the four own utilities in that order. Relabeling
a champion graph must transport pi, not replace it. Empty bundles are allowed.

Let F be ALL partial EFX states on G, without any charity-safety constraint.
Define S={A in F: |P_A|<=1 and A is charity-safe}. S includes complete states.
The selector maximizes u_pi lexicographically over S. Computational tie breaking
between equal utility tuples is not part of the mathematical potential. Maximizing
over exactly-one-good states is not our definition; under no complete EFX they
coincide.

## 2. Published input: stronger than almost-full existence

Primary source: Berger, Cohen, Feldman, Fiat, *(Almost Full) EFX Exists for Four
Agents (and Beyond)*, [arXiv:2102.10654v2](https://arxiv.org/pdf/2102.10654v2),
full version. Definition 2.3, printed page 6, fixes an arbitrary priority order.
Theorem 5.1, page 13, supplies a strictly lex-improving EFX successor from EVERY
four-agent EFX state with at least two unallocated goods. Its successor need not
have fewer unallocated goods. The page-14 roadmap covers every VIP after graph
relabeling. We use the paper's standing nondegeneracy convention. Lemma 2.4's
proof, page 6, supplies the pool-replacement operation proved below. Theorem 5.1
is an external dependency, not independently re-proved or formally checked here.

Internal provenance: `a8e925e:results/BCFF_IMPORT_AUDIT_20260816.md`.
The September A0 campaign used only the almost-full existence conclusion and
failed to apply this stronger improvement theorem to selection. The August import
audit had already spot-checked Theorem 5.1; that source audit was not incorrect.
The later claim that selector compatibility remained open was incorrect here.

## 3. Conventional proof

**Pool-replacement lemma.** If A is EFX and an agent envies P_A, there is a
Pareto-improving EFX state B on the same original goods.

Choose T subset P_A of minimum cardinality among subsets envied by some agent,
and choose i with v_i(T)>v_i(A_i). Give T to i, keep the other bundles, and set
P_B=(P_A minus T) union A_i. For every g in T, minimality gives
v_j(T minus {g})<=v_j(A_j) for every j. Hence unchanged observers do not strongly
envy the new bundle. The improved recipient cannot acquire strong envy of an
unchanged bundle. Other comparisons are unchanged; self comparisons use
nonnegativity. This proves EFX, conservation, and strict Pareto improvement.
Neither the old nor the new pool must be safe.

**Repair theorem.** Every A in F has Z in S with u_pi(Z)>=lex u_pi(A), reached
by finitely many strictly improving EFX steps unless A already lies in S.
If A is outside S, u_pi(Z)>lex u_pi(A).

At a state outside S apply these rules in order:

1. With at least two unallocated goods, apply BCFF Theorem 5.1 using pi.
2. Otherwise charity is envied; apply the pool-replacement lemma.

Each step preserves F and strictly increases the same u_pi. Among at most 5^|G|
labeled assignments, no state can recur. Thus the run reaches S in at most
5^|G|-1 steps. Pool size need not decrease: the well-founded progress measure is
the finite rank of the utility tuple, not the number of unallocated goods. This
is a termination bound, not an efficiency claim. If A is in S, choose Z=A.

**Selector equality.** The sets of lexicographic maximizers of F and S coincide.
In particular S is nonempty and every global maximum is safe with at most one
unallocated good.

F is finite and nonempty (the empty allocation is EFX). A maximum in F cannot
lie outside S by either improvement rule. Conversely, if X maximizes S and
Y in F improves X, its repair Z satisfies u_pi(Z)>=lex u_pi(Y)>lex u_pi(X),
contradicting S-maximality. No nonexistence-of-complete-EFX assumption was used.

**Exit-compatibility corollary.** Let X in S and let an actual program transition
produce Y on the original goods. A complete EFX Y is a terminal exit regardless
of utility. A partial EFX Y with u_pi(Y)>lex u_pi(X) repairs to Z in S with
u_pi(Z)>lex u_pi(X). If repair produces a complete state, it is also terminal.
No intermediate pool-size or pool-safety condition is needed. At an S-maximum
the latter kind of exit is therefore impossible.

This covers EVERY genuine EFX-improving move, not just a menu. It does not turn
a non-EFX assignment, response label, or marginal feasibility profile into an
exit. Repair need not preserve individual utility floors, packet shape, support
caps, charity identity, or previous role labels. None is part of frozen S.

## 4. Frozen actual transition family

Source pin: `a8e925eafce4c5e637c0d35ed8f02b6b2e801189`; filenames are in
`results/`. Each schema includes all its physical subset choices, not a bounded
menu. Source proofs remain dependencies; this compatibility argument is not a
fresh proof of every order-closing lemma. Endpoint certificates must establish
original-good conservation, EFX, and the fixed-priority sign.

| Schema and source | Actual operation and antecedents | Compatibility |
|---|---|---|
| Whole-bundle envy rotation; `TRAPPED_SOURCE_RETURN_LENGTH_TWO_CLOSURE_THEOREM.md` | Rotate existing bundles along a strict envy cycle | EFX, Pareto; original safe charity unchanged |
| Clean absorption; `TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md` | Give f to target w when X_w+f is common-safe | Complete EFX; no lex test needed |
| Envied-charity replacement; same composition | Replace an owner's bundle by envied singleton f | EFX, Pareto; repair applies, though impossible at an S-state |
| Basic/generalized PI cycles; composition, trapped-source theorem, BCFF Lemma 3.5 | Disjoint desired cores with certified releases and all cycle premises | Source-certified Pareto EFX; repair discarded complement |
| Easy-priority singletonization; `ALTERNATING_EASY_PRIORITY_ESCAPE_LEMMA.md`, `ADJACENT_LARGE_GLOBAL_LEX_TARGET_20260809.md` | Give earliest changing owner an envied singleton, preserve stated earlier owners, singletonize others | EFX by deletion to empty; repair arbitrary discards |
| Root flip; `ALTERNATING_ROOT_FLIP_LEMMA.md` | Base EFX, r envies singleton y, q envies singleton x, p desires common-safe D subset X_r+f; choose EFX member of two alternatives | Source proves an EFX-improving alternative for the transported order; repair bottom |
| Reservoir extraction; `LENGTH_THREE_RESERVOIR_ORDER_ESCAPE_THEOREM.md`, `ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY.md`, `ALTERNATING_TWO_SAFE_BUNDLE_REDUCTION.md` | Desired/common-safe packets and all stated observer thresholds | Repair after the source proves EFX and priority signs |
| Adjacent repartition; `ADJACENT_LARGE_GLOBAL_LEX_TARGET_20260809.md` | Disjoint R,Q in reservoir, desiredness/common safety and required observer threshold | Repair the source-certified EFX-improving endpoint |
| Ledger cancellation; `GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPOSITION_THEOREM_20260813.md` | Cancel retired transfers, recompute current holders and floors | A ledger/response is not an exit: verify EFX endpoint separately |
| Controlled floor reset; `TLX_CLOSURE_REFEREE_REPORT_20260816.md`, `TLX_SUCCESSOR_MODEL_CHECK_20260816.md` | Retired supplier-star operation | Excluded: completeness without EFX does not qualify |

The first eight rows do not assert that an applicable exit exists in every global
configuration. That is an admission/closure obligation. The two repair rules in
Section 3 are an explicitly proved extension of this pre-existing move family,
not a restriction excluding troublesome exits.

## 5. Global-admission consequences and boundaries

**A0 closes in the frozen four-agent scope.** Select a maximum over F or,
equivalently, S. If no complete EFX allocation exists, the safe pool has exactly
one good. Genuine PI improvements and singleton-discard escapes are legitimate
contradictions to maximality; their discarded goods do not create another gap.

**Still open:** physical fixed-U role extraction; derivation rather than insertion
of P1–P15; the identity of the selected state versus intermediate base/support
states; coverage of response/cycle alternatives; local closure on the genuinely
admitted domain; and original-good pullback. Compatibility validates the potential
interface, not every premise in the historical two-nonsingleton or fixed-U proof.
A complete exit may lower priority utility. Even a future four-agent theorem
would not settle arbitrary-agent additive EFX.

**Ties/zeros:** we do not claim fixed-initial-state lex repair after a generic
perturbation: that perturbation can destroy the initial state's EFX inequalities.
For an eventual existence theorem, select afresh within a nondegenerate instance
and transfer only the final EFX allocation back, with a separate wrapper. The
pool-replacement proof itself does tolerate ties and zero values.

## 6. Verification boundary

An independent exhaustive enumerator checks all original-good assignments on
declared small instances and separately reports F, safe F, S, exactly-one-safe,
and complete maxima. This calibrates the proof; it does not prove the universal
theorem. A separate exact verifier checks repair traces and rejects non-EFX
inputs, duplicated/missing goods, changed priorities, and non-strict steps.

Negative controls: an out-of-class EFX improvement may enter repair; a complete
EFX utility loss is a valid terminal exit; complete non-EFX resets and equality
in the objective are not valid improving exits. The archived 4x9 example must
retain 103 complete EFX allocations, 322 exactly-one-safe states, and its stated
unique restricted maximum.

Novelty: a program-integration corollary and audit correction, not a new field
result. The published BCFF theorem remains explicitly external-trusted.

See the [verification and review record](SELECTOR_COMPATIBILITY_VERIFICATION_20261016.md),
[code-review dispositions](SELECTOR_COMPATIBILITY_CODE_REVIEW_20261016.md), and
[reproduction commands](../../tracks/selector_compatibility/README.md).

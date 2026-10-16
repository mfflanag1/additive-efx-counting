# A1: physical entry, state separation, and the missing admission theorem

16 October 2026. Research checkpoint, not a proof of ADMIT4 or general EFX.

## 1. Scope and exact target

Work with four strictly positive additive valuations on one finite physical ground set G,
and a fixed owner priority pi. Initially assume bundle nondegeneracy: distinct subsets
have distinct value to each observer. Let O be a lexicographic maximum of **all** partial
EFX allocations, including complete allocations and without a charity restriction.
By the [A0 theorem](RESTRICTED_SELECTOR_COMPATIBILITY_20261016.md), O has safe charity
of size at most one. Under the additional hypothesis that no complete EFX allocation
exists, write its charity as {p}. Propositions 1-3 explicitly assume that O has
nonempty singleton charity {p}; A0 alone allows a complete O. With this singleton
condition assumed directly, these propositions do not otherwise require the
no-complete-EFX hypothesis. This distinction matters in calibrations.

For an allocation Z, write u_i(Z)=v_i(Z_i). A bundle C is **O-common-safe** if
v_i(C minus {g}) <= u_i(O) for every observer i and every physical good g in C.
Write tail_i(C)=max({v_i(C minus {g}):g in C} union {0}). For nonempty C this is
v_i(C)-min_{g in C}v_i(g), not total minus minimum role-total.

The unresolved target is a branch-exhaustive implication from this physical O to
either a complete EFX allocation, a genuine same-priority improving partial EFX
allocation, or a physical witness in a specified fixed-U domain whose closing exits
have one of those two meanings. The special numerical layout is not an antecedent.

This checkpoint proves a physical entry lemma and several normalization/interface
lemmas. It does **not** construct the complete fixed-U witness or all its inequalities.
The entry/core argument is standard champion-style reasoning, recorded here to close
the program's actual interface; no novelty priority is claimed for it.

## 2. A physical configuration that really follows from O

### Proposition 1: common-safe augmented cores

For each owner j, form the actual set T_j=O_j union {p}. Consider all subsets of T_j
that some observer i strictly prefers to O_i. This family is nonempty because j
strictly prefers T_j. Choose an inclusion-minimal member C. Then C is nonempty and
O-common-safe. Indeed, if any deletion C minus {g} were strictly preferred to some
O_i, C would not be minimal. Positivity also ensures that checking all single
deletions checks every proper subset. Record every observer i who strictly prefers C,
giving a physical decorated edge i -> j with core C contained in T_j.

This constructs a finite nonempty incoming-edge family at every target j, by
enumerating actual subsets if necessary. It neither replaces packets by atoms nor
assumes any numerical master inequality. Multiple cores and champions may be retained;
the conclusions below hold for every choice, not only a favorable tie-break.

### Proposition 2: disjoint-core cycle exchange

Take a directed simple cycle of these decorated edges, allowing length one.
If its selected cores are pairwise disjoint, assign each source i the core on its
outgoing edge, keep every nonparticipant's original bundle, and send every other
good to charity. This is a physical allocation: each core is contained in the original
bundle of a participating target plus {p}, so it cannot intersect a nonparticipant.

Every participant strictly improves and every nonparticipant retains its utility.
For any observer, a new recipient bundle is O-common-safe; a retained bundle already
satisfied original EFX. The observer's new own utility has not decreased, so all EFX
inequalities still hold. This is a strictly Pareto-improving partial EFX allocation,
hence strictly improves every fixed owner priority. No assertion that the new charity
is safe or singleton is needed: A0 optimized over all partial EFX allocations.

Consequently no such disjoint-core cycle can occur at O. A self edge would itself
give a one-vertex cycle, so no augmented minimal core has its own target as a champion.

### Corollary 3: a genuine multi-charity-use cycle

The finite decorated graph has an incoming edge at every vertex, and thus a directed
cycle. Distinct target bundles O_j are disjoint, so two cores on a simple cycle can
intersect **only at p**. Proposition 2 implies that every decorated simple cycle uses
p in at least two selected cores. The safe pool excludes {p} itself as an envied core,
so each p-containing core also contains a good of its target's old bundle.

We have therefore derived a cycle of length 2, 3, or 4 with at least two p-using
cores from the physical selected state. We have **not** derived that the cycle has
length two, that exactly three bundles are nonsingleton, or that either particular
core intersection has the later twelve-role form. Graph direction is source/champion
to target; these are response/core edges, not a count of transfer edges in an exit.

Ordinary envy cycles are excluded by the same replacement argument (or direct bundle
rotation). This does not exclude longer decorated cycles whose cores conflict on p.
Resolving those conflicts is precisely the next branch theorem, not a bookkeeping step.

### Corollary 3a: physical retained/residual splits and their actual payments

Every extracted core has one of two types. If it does not contain p, it equals its
whole target bundle O_j: a proper subset R of O_j cannot be strictly preferred to
any own bundle, since choosing g in O_j minus R gives
v_i(R)<=v_i(O_j minus {g})<=u_i(O) by original EFX.

If the core contains p, write C=R union {p} with R contained in O_j. Safety rules
out R empty. At a global maximum, R cannot equal O_j either: then j would strictly
prefer C, creating the forbidden self edge of Proposition 2. Thus both physical
parts R and D=O_j minus R are nonempty. In particular every p-using edge targets a
nonsingleton original bundle, and the cycle of Corollary 3 has at least two such targets.

This gives genuine packet inequalities with the **original O floors**. For each
champion i of C,

    0 <= u_i(O)-v_i(R) < v_i(p).

The weak lower bound is EFX/proper-subset safety; the strict upper bound is desire
for C. For every observer k and physical good g in R,

    v_k(R)+v_k(p)-v_k(g) <= u_k(O),
    v_k(R) <= u_k(O).

These are common-safety after deleting g and p respectively. Finally no self
champion at target j means v_j(C)<=u_j(O), hence

    v_j(D) >= v_j(p).

Under bundle nondegeneracy the lower source margin and target residual comparison
are strict (R differs from O_i, and D differs from {p}); the weak versions above
do not need nondegeneracy. Nothing here identifies R or D with the later A,H,J,K,L,W
packets or pays a cycle whose p-cores overlap. It is a physical split lemma, not
the missing joint exchange theorem.

### Exact obstruction to an unconditional two-cycle shortcut

The existing nine-good selector calibration has the unique global maximum
O=({6,7},{1,2,3},{0,4},{5}; charity {8}), in priority 0,1,2,3.
Its independent complete allocation-space audit is
`results/selector_compatibility_4x9_exact_audit_20261016.json`.
Exhausting every augmented subset gives exactly these minimal envied cores:

| target j | core | all champions i |
|---|---|---|
| 0 | {6,8} | 1,2,3 |
| 1 | {2,3,8} | 2 |
| 2 | {4,8} | 3 |
| 3 | {5} | 1 |

With source-to-target orientation the only decorated simple cycle is
`1 -> 3 -> 2 -> 1`; its three cores use good 8 twice. There is no two-cycle.
Thus global selection, safe singleton charity, positive nondegeneracy and three
nonsingleton bundles do not by themselves force a two-cycle in this **specified**
augmented minimal-core graph. Also nine goods cannot realize twelve nonempty disjoint
roles. These are exact obstructions to unconditional intermediate claims, not to
ADMIT4: the instance has 103 complete EFX allocations and fails its no-complete-EFX
antecedent. Nor does the check quantify over all differently defined historical
generalized-response graphs. The complete-allocation branch remains essential.

## 3. Three different states must not share the symbol X

The literal source predicate is frozen in `references/a1_source/`, from commit
5d13f17e8258f2d9386467838d48c482cf72b071. Its roles are nonempty disjoint physical
subsets whose union is G; in the atomic version each is a single good. Denote its
numerical `BASE` by B and its `SUPPORT_STATE` by Y, reserving O for the selected state.

| owner | original selected O | numerical base B | support Y |
|---|---|---|---|
| r | O_r | a0 union m | a0 union a1 union h |
| q | O_q | q0 union a1 | j union k union q0 |
| d | O_d | h union k union gq | m union gq union gr |
| s | O_s | e union p | l union e |
| charity | one original good p_O | j union l union gr | role p |

The table deliberately distinguishes p_O from numerical role p: their equality
also needs a physical construction. It is not established by reusing the letter.

### Proposition 4: B cannot be O

The literal B pool contains three nonempty disjoint roles, hence at least three
physical goods. O has one. Therefore B and O cannot be the same allocation, under
any owner relabeling or nonempty expansion of the roles. The base has four nonsingleton
owner bundles as well. Allowing empty j,l,gr would change the literal master and its
strict-positive hypotheses; it is not a harmless realization of this layout.

If a physical B satisfying the master really exists on the same instance, it is EFX
by P3, and it is strictly lexicographically below O. For nondegenerate valuations,
equality of every owner's utility would force equality of each owner's bundle, and
then of charity, contradicting the previous paragraph. Alternatively A0's imported
BCFF improvement theorem applies directly to the three-or-more-good pool.
In particular, imposing P10 global maximality **at B itself** together with physical
P1/P3 is inconsistent in the declared nondegenerate scope, not an extra admissible
master constraint that remains to be encoded.

### Proposition 5: Y cannot be O

Put A=a0 union a1, H=h, Q=j union k union q0, E=l union e, W=m union gq union gr.
The physical root-wall predicate P7 asserts

    v_d(W) < tail_d(A).

For disjoint nonempty H and A, tail_d(A union H) >= tail_d(A): retain a good attaining
the maximum deletion in A and add H. Thus

    u_d(Y) = v_d(W) < tail_d(A) <= tail_d(A union H) = tail_d(Y_r).

This is a literal EFX violation, witnessed by deleting a minimum-d-valued physical
good of A from Y_r. Y is a probe, not an EFX allocation to which global maximality
can directly be applied. If the wall used atom/role deletion instead, physical tails
are at least that large, so the same obstruction persists.

These are no-identification lemmas, not a refutation of a possible O-to-B-to-Y
construction. A legal construction and its threshold comparisons remain to be proved.

## 4. Normalization: a restriction removed, and a threshold retained

### Proposition 6: the literal value box is redundant conditional on B

Let B be any physical positive-additive EFX allocation with safe pool. Normalize each
observer by beta_i=v_i(B_i)>0. Let R be a nonempty proper subset of some B_t.
If t=i, positivity gives v_i(R)/beta_i<1. If t differs from i, choose a physical
good g in B_t outside R. Then

    v_i(R) <= v_i(B_t minus {g}) <= beta_i.

A role contained in the safe pool also has normalized value <=1; when it is a proper
subset of that pool positivity makes this strict. Every literal B role satisfies one
of these cases, since each owner bundle has at least two nonempty roles and the pool
has three. Hence for all roles R and observers i,

    0 < v_i(R)/beta_i <= 1 < 16.

Every physical minimum is at most the role's total and satisfies the same bound.
With bundle nondegeneracy, even the foreign-bundle inequality is strict: B_t minus {g}
and B_i are distinct physical subsets, so their values cannot be equal.

This corrects the historical ledger's claim that the `<16` box is an independently
load-bearing restriction **inside this literal base-EFX cell**. It does not remove
the layout, positivity, or proper-subset hypotheses, and it proves no global admission.
The frozen historical documents are preserved unchanged; this is the dated correction.

The proper-subset qualifier is essential. With four goods and all agents having raw
values (M^3,M^2,M,1), M>=3, the unique global lexicographic EFX maximum for priority
0,1,2,3 gives good i to owner i. All EFX bundles have at most one good: if a bundle
had at least two, an empty owner would strongly envy it. Among such allocations,
lexicographic maximization assigns the distinct values greedily. Base-M subset sums
are distinct. After own-value normalization, observer 3 values owner 0's singleton at
M^3, unbounded. At M=3 the independent enumeration checks all 625 allocations, finds
209 partial EFX allocations and that unique maximum. The example has complete EFX:
it refutes only an unconditional global singleton bound, NOT ADMIT4's antecedent.

### Proposition 7: normalization does not reset global priority thresholds

Suppose an O/B construction is eventually proved. Set w_i=v_i/beta_i and
gamma_i=w_i(O_i). Positive coordinate-wise rescaling preserves the fixed-priority
lexicographic order. Proposition 4 yields

    (1,1,1,1) <lex_pi gamma.

The numerical master's partial-exit condition compares an exit with (1,1,1,1).
That is not the global contradiction threshold. A partial EFX exit Z must satisfy

    (w_i(Z_i))_i >lex_pi gamma.

If d_i=w_i(Z_i minus B_i)-w_i(B_i minus Z_i), its correct test is
`1+d >lex_pi gamma`, not `d >lex_pi 0`. It remains possible to prove that a particular
exit clears gamma, but improvement over B alone is insufficient. A complete EFX exit
requires no such comparison and still supplies the desired contradiction to nonexistence.

## 5. Minimum faithful physical extraction certificate

A certificate must carry one ground set and one valuation table, the original O and
priority, the role-to-good partition, B and Y (plus every intermediate state), and
the normalization beta and original threshold gamma. Every inequality must say
whether its floor is u(O), u(B), or the current state's own utility.

For every owner i, full signed differences I_i=Y_i minus B_i and D_i=B_i minus Y_i
reconstruct Y_i=(B_i minus D_i) union I_i. The complement reconstructs charity.
For a longer path, indicator differences telescope exactly, including the charity
coordinate. These identities check conservation, not the legality of a claimed
operation, selector minimality, or reachability. Those require separate certificates.

For each nonempty physical role R, derive T_{R,i}=sum_{g in R}v_i(g) and
M_{R,i}=min_{g in R}v_i(g) from these same goods. Whole-role EFX is checked by
`sum T - min M`, not by role totals as though they were single goods. Abstract
totals/minima can describe whole-role allocation tests but do not establish a
common split-good identity or a transition on the original instance.

For example a two-good role of values 1/2,1/2 has physical tail 1/2, not the atomic
tail 0 of a single role of total 1. Splitting an atom while preserving its total
can destroy an EFX comparison. No packet expansion may silently import atomic EFX.

## 6. P1-P15 derivation ledger after this checkpoint

| premise | what follows from the global physical entry | missing argument |
|---|---|---|
| P1: twelve nonempty roles, literal B | no; O has a different pool | partition construction, empty-role cases, full accounting |
| P2: positive values, `<16` | positivity given; box follows from P1/P3 by Proposition 6 | derive that particular B first |
| P3: normalized B EFX, safe pool | O is EFX and safe, but O is not B | construct B; normalize it without forgetting gamma |
| P4: support/split/reassembly layouts | actual augmented cores and signed allocations exist | derive these three particular layouts and their legal uses |
| P5: minimality, budgets, residual failure, utility signs | common-safe minimal cores follow from Proposition 1 | derive each named packet relation and its floor |
| P6: retained A,Q,E desired/common-safe cores | a family of O-common-safe cores follows | identify these named cores and compare B/O floors |
| P7: particular root-facing wall | if assumed it proves Y is non-EFX | exhaustive wall/observer branch choice |
| P8: no rank-four matching | disjoint common-safe improving cycles excluded | show this response definition gives legal disjoint allocations at O thresholds |
| P9: no self response | no self augmented-core edge at O by Proposition 2 | transfer result to the master's different support and floors |
| P10: global maximum | supplied for O by A0 | cannot attach it to B or Y |
| P11: generalized PI-freeness | every genuine Pareto-improving EFX exit excluded | verify each generalized exit is EFX on original goods |
| P12: reachability and ledgers | exact differences reconstruct a given state | construct the trace, not just its encoding |
| P13: rank-three, selected r->q, exact five edges | a multi-p-use cycle exists | neither rank-three nor five-edge restriction derived |
| P14: decorated response data | physical cores can be retained exactly | obtain later released/residual/floor data legally |
| P15: saturation | global optimum excludes legal improving EFX exits | prove continuation/repair covers every purported failure |

In particular Q0=Q minus K is **not** automatically nonempty. The frozen
`ROOT_FACING_TWO_EDGE_STRICT_PAYMENT_COMPLETION_LEMMA_20260813.md` explicitly requires
nonempty Q0 and the provenance identity B_d=H union (K minus J) union Gq.
It says that neither follows from the general earlier selector. These are precisely
the positive q0 role and d{h,k,gq} placement hard-coded in the numerical base.
Its strict-payment candidate is not itself established EFX.

## 7. First remaining theorem: branch-exhaustive physical admission

Do not start another terminal-template census. Starting with the physical cores of
Section 2, prove one of the following for **every** admissible selected state:

1. A complete EFX allocation on G; or
2. an actual partial EFX allocation strictly above O in the fixed priority; or
3. an explicit physical trace and partition into a declared fixed-U domain, with
   all floors and failure inequalities proved, not assumed.

At the first graph split, resolve the longer multi-p-use cycles as well as a two-cycle,
and all possible original bundle cardinality patterns. The archived three-nonsingleton
census lists GG, GGL, GGS, GGG, GGLS, GGSL, GLGS, GGGS and reduces only GG to a flower.
It explicitly does not close the other seven. Its alphabet and cycle selection are
that archive's conventions; Section 2 does not assert an identification of its new
core graph with every historical chosen graph. The four-nonsingleton entry is also
not supplied by that result. A proof restricted to a GG flower must be labeled as
such and cannot discharge ADMIT4.

Within a genuine GG branch, prioritize the physical provenance alternatives Q0 empty
versus nonempty and the position of K minus J. If the literal B cannot be reached,
enlarge the local domain explicitly, recompute its floors against O, and mark which
old closure claims no longer apply. Merely renaming B to O is ruled out above.

## 8. Verification and boundary

The source manifest pins exact predicate files. The new verifiers use physical goods
and rational arithmetic independently of the old SMT encoding:

- `tracks/physical_admission/extract_champion_cores.py`: complete local enumeration
  of common-safe minimal envied cores and decorated simple cycles, plus physical
  construction/recheck of any disjoint cycle exchange. It does not certify global
  maximality; the nine-good calibration imports that fact only from the earlier
  complete 5^9 enumeration.
- `tracks/physical_admission/verify_state_separation.py`: direct base/support checks,
  role-bound witnesses, conservation, and the small singleton-bound calibration.

Fresh run counts, hashes, hostile-review findings and commands belong in the companion
verification record. Passing finite checks calibrates the conventional proofs; it is
not evidence that the missing branch-exhaustive theorem has been proved.

**Result boundary:** A1 now has a physical entry construction and a corrected
three-state/threshold interface. The full physical fixed-U extraction remains open.
The value box is not the obstruction within the literal base cell; layout/provenance,
branch coverage, and comparison to original global floors are. No EFX counterexample,
new global existence theorem, or field-level breakthrough is claimed here.

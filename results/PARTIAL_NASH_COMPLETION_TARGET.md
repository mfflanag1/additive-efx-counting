# Partial-EFX Maximum-Nash Completion: Refutation and Structural Record

**Status:** exactly refuted at four agents and nine goods  
**Scope of refutation:** the direct-insertion selector only  
**Still open:** complete EFX for general additive valuations

## Refuted statement

Let \(\mathcal E(V)\) be the finite family of allocations \((X,f)\) in which
exactly one good \(f\) is unallocated, \(X\) is EFX, and

\[
v_i(X_i)\ge v_i(f)\qquad\text{for every agent }i.
\]

For positive valuations, every own-bundle utility in this family is positive.
Define

\[
\operatorname{NW}(X)=\prod_{i=0}^3 v_i(X_i).
\]

> **Refuted partial-EFX maximum-Nash completion conjecture.** Some state in
> \(\arg\max_{(X,f)\in\mathcal E(V)}\operatorname{NW}(X)\) permits direct
> insertion of \(f\) into one of its four bundles while preserving EFX.

The objective is invariant under independent positive rescaling of valuation
rows. Normalizing each row to total value one therefore changes neither the
maximizers nor the claim.

The conjecture is false. The exact $4\times9$ profile in
[PARTIAL_NASH_COMPLETION_REFUTATION.md](PARTIAL_NASH_COMPLETION_REFUTATION.md)
has a unique maximum-product eligible state, and that state is blocked at all
four hosts. Exhaustive literal, core-iterator, and vectorized enumerators
agree. The profile has 83 complete EFX allocations, so this refutes the
selector rather than complete additive EFX.

## Why it would have proved the four-agent theorem

The published theorem of Berger, Cohen, Feldman, and Fiat gives every
four-agent additive instance an EFX allocation with at most one unallocated
good, with the unallocated set unenvied. In a hypothetical instance without a
complete EFX allocation, their state has exactly one floater and belongs to
\(\mathcal E(V)\). Thus \(\mathcal E(V)\) is nonempty.

Choosing a maximum-Nash member and inserting its floater would have produced
a complete EFX allocation, contradicting the hypothetical counterexample.
The usual perturbation closure then extends positive valuations to
nonnegative valuations.

That argument would settle four agents for arbitrarily many goods. It would
not by itself settle five or more agents, because the required almost-complete
starting theorem is four-agent specific.

## Safe floater-exchange lemma

The first cap-free exchange unit is already proved.

Let \((X,f)\in\mathcal E(V)\), let \(X_h\) contain at least two goods, and
choose \(r\in X_h\). Form \((Y,r)\) by replacing \(r\) with \(f\) in the
host bundle:

\[
Y_h=(X_h\setminus\{r\})\cup\{f\},
\qquad Y_i=X_i\quad(i\ne h).
\]

If

\[
v_h(f)\ge v_h(r)
\quad\text{and}\quad
v_i(f)\le v_i(r)\quad\text{for every }i\ne h,
\tag{1}
\]

then \((Y,r)\in\mathcal E(V)\). If the host inequality in (1) is strict,
then \(\operatorname{NW}(Y)>\operatorname{NW}(X)\).

To prove EFX, the host weakly improves and therefore retains all of its
observer inequalities. For another observer \(i\), comparison with \(Y_h\)
after removing \(f\) is comparison with \(X_h\setminus\{r\}\), already
covered by EFX of \(X\). After removing an old good \(g\ne r\), replace the
new \(f\) by \(r\) using \(v_i(f)\le v_i(r)\), and again apply the old EFX
inequality. Other targets are unchanged.

Floater nonenvy also survives. For \(i\ne h\), choose an old
\(g\in X_h\setminus\{r\}\). Old EFX gives

\[
v_i(X_i)\ge v_i(X_h\setminus\{g\})\ge v_i(r).
\]

The host's new bundle contains \(f\) and satisfies
\(v_h(Y_h)\ge v_h(f)\ge v_h(r)\). Finally, only the host's own utility
changes, proving the strict Nash increase.

Consequently a maximum-Nash state cannot contain such a strict safe
exchange. Any proof of the conjecture may therefore assume that every
potential improving replacement has a second agent who also ranks the
floater above the ejected good. Those agents supply the directed edges of
the remaining exchange-chain problem.

The proof has a permanent symbolic audit: the untouched part of the host
bundle is represented by a nonnegative aggregate, making the QF_LRA exchange
implications independent of bundle size, while a QF_NRA check proves strict
Nash increase. An independent literal verifier also exhausts all 256
two-agent, four-good profiles over values \(\{1,2\}\), covering 4,032 premise
exchanges including 1,344 strict ones. See
[safe_floater_exchange_lemma_audit.json](safe_floater_exchange_lemma_audit.json).

## Bundle cycles and the source host

The equality handoff extends to a full cap-free bundle-cycle lemma. If agents
on a directed cycle each weakly prefer the next agent's entire bundle,
rotating those bundles preserves EFX and floater nonenvy; one strict edge
strictly raises Nash welfare. Hence the strict-envy graph of a maximum-Nash
state is acyclic and has an unenvied source bundle.

If the source bundle were a singleton, floater nonenvy and source nonenvy
would make direct insertion valid. Thus any blocked maximum has a
nonsingleton source. Moreover, every witness blocking insertion at that
source removes an old host good \(r\) and satisfies

\[
v_i(X_h)\le v_i(X_i)
<v_i(X_h)-v_i(r)+v_i(f),
\]

so the blocking observer strictly prefers \(f\) to \(r\). This reduces the
unstructured all-host obstruction to the genuine floater-support chain. The
complete proof and permanent audit are in
[PARTIAL_NASH_SOURCE_HOST_REDUCTION.md](PARTIAL_NASH_SOURCE_HOST_REDUCTION.md).

## Floater substitution along a preference path

A third cap-free lemma handles a source blocker with a unique supporter.
Replace its removed good \(r\) by \(f\), make \(r\) the new floater, give the
modified host bundle to the supporter, and rotate old bundles along any weak
bundle-preference path from the source to that supporter. The resulting state
is eligible EFX and strictly raises Nash welfare. Thus a unique supporter at
a blocked maximum must be unreachable from its source. See
[PARTIAL_NASH_SUBSTITUTION_PATH_LEMMA.md](PARTIAL_NASH_SUBSTITUTION_PATH_LEMMA.md).

A broader local closure is false. The exact refutation in
[partial_nash_local_trichotomy_refutation_audit.json](partial_nash_local_trichotomy_refutation_audit.json)
has a blocked eligible state with no strict bundle cycle and no improving
eligible rematching among all 192 source substitutions. It is not a
maximum-Nash counterexample: 1,780 global eligible rivals have larger product.
Therefore the missing proof must exploit global Nash maximality, not only
the current bundle graph and a one-good source substitution.

## Exact evidence and falsification boundary

The pre-refutation corpus scan covered 155 distinct stored profiles and found
no blocked maximum. A new adversarial objective instead maximized the product
of the best all-realizations-blocked Pareto vector relative to the global
eligible maximum. Two independent runs crossed that gap. The promoted
counterexample was found at iteration 45 of random seed 211 and is replayed
from all 589,824 partial assignments in
[partial_nash_completion_refutation_audit.json](partial_nash_completion_refutation_audit.json).

The unique maximum has utility vector
$(9787,34360,30805,20512)$, product
$212486804036051200$, and no insertable host. The second-largest product is
$205476190869242880$. Its minimum EFX slack is 1,045, so the result is not a
floating-point tie or a weak-boundary artifact. A separate complete census
finds 83 complete EFX allocations.

The frozen profile, exhaustive audit, seed-211 discovery record, and audit
script have SHA-256 values
`928029ffcd6d4171e1733999fe6f6f0abf0d0d5ab6ffe1c7c0a3702215155981`,
`20f8804f932534242b196db6acbbca6d3c0434563ef3cdfed910e2babd412df6`,
`c70870d3965621d5b60044ebd3adf7a2058af9a6c2446b414ef5790c6a867211`,
and `fb666b2cd888e28f2bb104877b95f561f65d0006ea6304b4ebfd24d0c4a30e52`,
respectively. On 2026-08-02,
`make verify-partial-nash-completion-refutation` regenerated the exhaustive
audit and passed the byte-for-byte comparison with the frozen file.

The paragraphs below preserve the earlier search boundary as provenance; they
are superseded as evidence for survival of the selector.

The scanner reconstructs every recognized positive four-agent matrix in the
stored campaign corpus through nine goods. It selects Nash maximizers by the
exact integer product of own utilities, avoiding floating-point tie decisions.
At the pre-refutation checkpoint, all 155 profiles had an insertable maximum.
The current 157-profile rescan contains the exact counterexample, one negative
endpoint, and the same two exactly replayed equality profiles. The hash-bound
census is
[partial_nash_potential_corpus_scan.json](partial_nash_potential_corpus_scan.json).

Targeted annealing from the tight \((4,9)\) count-four witness reached an
exact zero-margin state after 1,200 iterations. A further 1,500-step
low-temperature continuation did not cross the wall. In the zero state, two
Nash-maximizing assignments swap a four-good bundle and a singleton between
agents 0 and 3; both agents are exactly indifferent and both assignments are
insertable at equality. Perturbations that delete one equality edge make the
other assignment strictly better. This is a concrete bundle-swap handoff,
not a proof that every wall has one.

The closest strict corpus profile also resisted a 1,200-step continuation
without a single improvement.

An exact QF_NRA CEGAR now probes a fixed candidate identity. It requires the
candidate to be eligible and blocked, and incrementally adds every partial
state that either has larger Nash product or is insertable with at least the
candidate's product. Five SAT masters accumulated 160 rivals; the sixth
timed out after 60 seconds. The proved bundle-cycle theorem then supplied 20
linear cycle cuts, an explicit source-host cut, and 20 cycle rivals. The
strengthened 180-rival master still timed out after 180 seconds without a
model or UNSAT proof. This is an inconclusive nonlinear-solver boundary, not
an exclusion theorem. The frozen endpoint is
[partial_nash_cegar_structural_session2.json](partial_nash_cegar_structural_session2.json).
Fixing each of the four possible source hosts in separate 60-second masters
also produced four timeouts. The exact branch ledger is
[partial_nash_cegar_source_split_gate.json](partial_nash_cegar_source_split_gate.json).

## Selectors already refuted

Pareto maximality of the own-utility vector is also insufficient. An exact
$4\times9$ profile has 43 Pareto-frontier utility vectors, one of which is
uniquely realized and blocked at every host. Its only eligible floater-
exchange neighbor is insertable but strictly lowers Nash product, whereas
every higher-product insertable state requires at least four good-owner
changes. The profile's maximum-Nash state remains insertable. See
[PARTIAL_PARETO_COMPLETION_GATE.md](PARTIAL_PARETO_COMPLETION_GATE.md) and
[partial_pareto_completion_refutation_audit.json](partial_pareto_completion_refutation_audit.json).

The superficially simpler linear rule

\[
\sum_i\frac{v_i(X_i)-v_i(f)}{v_i(M)}
\]

is exactly false. The matrix in
[partial_linear_potential_refutation.json](partial_linear_potential_refutation.json)
has 98 eligible states and 58 insertable states, but its unique linear
maximizer is blocked at all four hosts with insertion slacks
\((-5,-1,-1,-3)\). The same matrix refutes the floater-ratio Nash and
floater-surplus Nash rules. Ordinary normalized utilitarian and anonymous
leximax selection were already refuted by the fixed-order obstruction.

These failures were useful calibration, but maximum Nash welfare of own
bundles is now refuted as well. No nearby static objective should be promoted
without a fresh falsification audit.

## Closed proof gate

The counterexample realizes exactly the premise the proposed proof hoped to
exclude: a maximum-Nash eligible state is blocked at every host. The source-
host, safe-exchange, and substitution-path lemmas still apply, but none forces
an improving rival or insertable equality state. Therefore no global rival-
extraction lemma with that conclusion can be true under only those premises.

The profile does have lower-product eligible states that permit insertion, so
controlled descent was the natural immediate repair. That repair is now
exactly refuted as well. A second profile has a unique blocked maximum-Nash
eligible state and all 24 of its same-floater, one-good-transfer neighbors are
ineligible. No same-floater insertable eligible state exists within owner
distance three; the nearest ones occur at distance four. See
[PARTIAL_NASH_LOCAL_COMPLETION_REFUTATION.md](PARTIAL_NASH_LOCAL_COMPLETION_REFUTATION.md).

Thus a surviving descendant must change the floater, jump multiple goods,
temporarily leave the eligible class, or optimize a genuinely nonlocal
reachability object. Static maximality plus local same-floater descent is
closed.

The most generous one-substitution version is now closed too. In a third
exact profile the unique blocked maximum has two source bundles. Replacing
any one of their five goods by the floater and applying any of the 24 bundle
permutations produces 120 distinct states, all of which fail partial EFX.
The profile has 87 complete EFX allocations. See
[PARTIAL_NASH_SOURCE_COMPLETION_REFUTATION.md](PARTIAL_NASH_SOURCE_COMPLETION_REFUTATION.md).

This exhausts the natural maximum-Nash branch: direct insertion,
same-floater local descent, and source-good substitution with arbitrary bundle
rematching are all exactly false.

## Executable artifacts

- Exact multi-potential census:
  [`analyze_partial_state_potentials.py`](../tracks/parkability/analyze_partial_state_potentials.py)
- Repository-wide Nash scan:
  [`scan_partial_nash_potential.py`](../tracks/parkability/scan_partial_nash_potential.py)
- Adversarial potential annealing:
  [`anneal_partial_linear_potential.py`](../tracks/parkability/anneal_partial_linear_potential.py)
- Fixed-candidate exact-NRA CEGAR:
  [`run_partial_nash_cegar.py`](../tracks/parkability/run_partial_nash_cegar.py)
- Frozen source-split solver boundary:
  [partial_nash_cegar_source_split_gate.json](partial_nash_cegar_source_split_gate.json)
- Cap-free safe-exchange audit:
  [`audit_safe_floater_exchange_lemma.py`](../tracks/parkability/audit_safe_floater_exchange_lemma.py)
- Bundle-cycle/source-host audit:
  [`audit_bundle_cycle_source_lemma.py`](../tracks/parkability/audit_bundle_cycle_source_lemma.py)
- Floater-substitution path audit:
  [`audit_floater_substitution_cycle_lemma.py`](../tracks/parkability/audit_floater_substitution_cycle_lemma.py)
- Local-trichotomy refutation audit:
  [`audit_partial_nash_local_trichotomy_refutation.py`](../tracks/parkability/audit_partial_nash_local_trichotomy_refutation.py)
- Pareto-selector refutation and local-isolation audit:
  [`audit_partial_pareto_completion_refutation.py`](../tracks/parkability/audit_partial_pareto_completion_refutation.py)
- Maximum-Nash direct-completion refutation:
  [PARTIAL_NASH_COMPLETION_REFUTATION.md](PARTIAL_NASH_COMPLETION_REFUTATION.md)
- Independent exhaustive refutation audit:
  [`audit_partial_nash_completion_refutation.py`](../tracks/parkability/audit_partial_nash_completion_refutation.py)
- Exact local-repair refutation:
  [PARTIAL_NASH_LOCAL_COMPLETION_REFUTATION.md](PARTIAL_NASH_LOCAL_COMPLETION_REFUTATION.md)
- Independent radius-three/radius-four audit:
  [`audit_partial_nash_one_transfer_refutation.py`](../tracks/parkability/audit_partial_nash_one_transfer_refutation.py)
- Exact source-completion refutation:
  [PARTIAL_NASH_SOURCE_COMPLETION_REFUTATION.md](PARTIAL_NASH_SOURCE_COMPLETION_REFUTATION.md)
- Independent source-substitution audit:
  [`audit_partial_nash_source_completion_refutation.py`](../tracks/parkability/audit_partial_nash_source_completion_refutation.py)
- Frozen status and claim boundary:
  [partial_nash_potential_gate.json](partial_nash_potential_gate.json)

## Ordered next steps

1. Treat direct maximum-Nash completion as closed and refuted; do not spend
   further proof effort on global rival extraction from maximality alone.
2. Treat eligibility-preserving same-floater one-good descent as closed: its
   maximum-Nash state can be isolated, and direct completion can require four
   simultaneous owner changes.
3. Retire the maximum-Nash partial-state branch and return to the independent
   Hall/partition route. Any future partial-state selector must first survive
   all three frozen refutation profiles and must use structure beyond one
   source substitution.

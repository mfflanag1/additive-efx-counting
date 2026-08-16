# Radius-One Hall Completion Selectors

**Status:** arbitrary-state and Pareto-maximal radius one are exactly refuted;
normalized-utilitarian and maximum-Nash radius one remain live  
**Scope:** four agents, positive additive valuations, arbitrary goods  
**Would imply:** complete EFX for four additive agents  
**Not claimed:** a theorem, a proof for five or more agents, or general EFX

## Setup

Let \((X,f)\) be a partial EFX allocation for four agents with exactly one
unallocated good \(f\), and require floater nonenvy

\[
v_i(X_i)\ge v_i(f)\qquad(i=0,1,2,3).
\]

Call such a state *eligible*.  The original selector maximizes

\[
\operatorname{NW}(X)=\prod_{i=0}^3 v_i(X_i).
\]

For any four-bundle partition \(P=(B_0,B_1,B_2,B_3)\), form its EFX
feasibility graph: agent \(i\) is adjacent to bundle \(B_j\) precisely when

\[
v_i(B_j)\ge
\max_{k\ne j}\left(v_i(B_k)-\min_{g\in B_k}v_i(g)\right).
\]

The partition supports a complete EFX allocation exactly when this graph has
a perfect matching.

The sharper current selector instead maximizes the normalized utilitarian
potential

\[
\Phi(X,f)=\sum_{i=0}^3\frac{v_i(X_i)}{v_i(M)}.
\]

This is scale invariant, and after normalizing each row by \(v_i(M)\), all
optimality comparisons are linear.

## Two candidate statements

The radius-zero statement permits only placement of \(f\): choose a host
bundle \(X_h\), replace it by \(X_h\cup\{f\}\), and Hall-rematch the four
resulting bundles.

> **Radius-zero maximum-Nash Hall completion.** Some maximum-Nash eligible
> state and some host produce a feasibility graph with a perfect matching.

This statement is **false**.  The two exact maximum-Nash selector profiles in
the frozen corpus each have a unique maximum, and all four enlarged
partitions are Hall-deficient even after arbitrary bundle reassignment.
Thus allowing a rematching does not repair the maximum-Nash direct-insertion
conjecture.

The smallest surviving extension permits one previously allocated good to
move between bundle labels before rematching:

\[
Y_h=X_h\cup\{f\},\qquad
Y_s=X_s\setminus\{r\},\qquad
Y_t=X_t\cup\{r\},
\]

where \(r\in X_s\), \(s\ne t\); overlaps among \(h,s,t\) are allowed, and no
resulting bundle may be empty.  The unchanged bundles complete the
partition.

> **Radius-one maximum-Nash Hall completion candidate.** In every positive
> additive four-agent instance, some maximum-Nash eligible state has a
> radius-at-most-one partition whose feasibility graph has a perfect
> matching.

The following narrower sufficient statement is now the primary gate.

> **Radius-one normalized-utilitarian Hall completion candidate.** In every
> positive additive four-agent instance, every eligible state maximizing
> \(\Phi\) has a radius-at-most-one partition whose feasibility graph has a
> perfect matching.

## Why radius one would prove the four-agent theorem

Berger, Cohen, Feldman, and Fiat prove that every four-agent additive
instance has an EFX allocation with at most one unallocated good and with
the unallocated set unenvied.  In a hypothetical instance without complete
EFX, this supplies a nonempty eligible family with exactly one floater.
Choose an eligible state maximizing either surviving selector.  Its
radius-one candidate produces a complete four-bundle partition with a perfect
EFX matching, contradicting the hypothetical counterexample.  Standard
perturbation closure would then
extend the positive result to nonnegative valuations.

The argument is four-agent specific because its almost-complete starting
theorem is four-agent specific.

## Exact radius-zero refutation

In both hard profiles the unique maximum has

\[
X_0=\{6,7\},\quad X_1=\{1,2,3\},\quad
X_2=\{0,4\},\quad X_3=\{5\},\quad f=8.
\]

For the original maximum-Nash refutation profile, the four feasibility
graphs after placing \(f\) have minimal Hall obstructions of types

\[
2\to1,\qquad4\to3,\qquad2\to1,\qquad2\to1,
\]

respectively.  The source-substitution refutation profile has the same
radius-zero failure, including a first enlarged partition in which all four
agents accept only the enlarged source bundle.

Both profiles admit the same radius-one repair:

\[
\{6,7\},\{1,2,3\},\{0,4\},\{5\};f=8
\longmapsto
\{6,8\},\{1,2,3,7\},\{0,4\},\{5\}.
\]

In each case the identity assignment is already EFX.  The transfer replaces
good 7 by the floater in the two-good source and moves good 7 into the
three-good bundle.

The exhaustive audit also shows that a stronger statewise statement is
false.  Across the three frozen profiles, respectively 27 of 290, 43 of 314,
and 29 of 279 eligible states are radius-zero Hall-blocked.  The candidate
therefore needs its maximum-Nash selector or another global selection
principle.

## Exact statewise radius-one obstruction

The maximum-Nash qualification is essential even after allowing one old-good
move.  Exact QF_LRA found the strictly positive matrix

\[
\begin{pmatrix}
3&15&24&1223&1196&12&45&1265&15\\
605&614&6&18&54&1252&3&614&632\\
4667&3739&813&1346&418&9219&1254&3390&4272\\
5076&5020&1129&1297&3863&6345&6345&1297&5076
\end{pmatrix}.
\]

With \(f=8\) and

\[
X_0=\{6,7\},\quad X_1=\{1,2,3\},\quad
X_2=\{0,4\},\quad X_3=\{5\},
\]

the base is EFX and no agent envies the floater as a singleton.  Nevertheless
every one of the 91 distinct partitions obtained by assigning \(f\) and
moving at most one old good has a Hall-deficient feasibility graph.  A
solver-independent literal replay checks all \(91\cdot24=2{,}184\)
partition--matching pairs and finds zero completions across 54 distinct
feasibility graphs.

This does **not** refute the maximum-Nash radius-one candidate.  Exhaustive
enumeration finds 858 eligible states in the same profile.  Its unique
maximum-Nash state has floater 2 and permits radius-zero Hall completion.  The
displayed obstruction's Nash product is only about 5.58 percent of the global
eligible maximum.  Thus the exact obstruction sharpens the live analytic
gate: prove that a radius-one Hall-blocked state cannot maximize Nash welfare,
rather than try to prove that such states do not exist.

The exact obstruction family has since exposed a local-repair ladder.  Adding
linear clauses that forbid the nearest Pareto improvement produces, in order:

1. an obstruction whose nearest dominator is a one-good floater swap;
2. after excluding all improving eligible floater swaps, an obstruction whose
   nearest dominator is a two-agent good swap;
3. after excluding both, an obstruction whose nearest dominator is a
   three-agent one-good exchange cycle;
4. after excluding all one-good cycles, an obstruction whose nearest
   dominator is a two-agent floater-substitution path; and
5. after excluding every simple one-good cycle and floater path of length at
   most four, an obstruction whose nearest dominator changes four old-good
   owners simultaneously.

Thus no theorem based only on one-component path/cycle improvements can close
the radius-one Hall gate.  A global selector is essential.

Evidence:

- [partial_hall_radius_one_2321_lra_compact.json](partial_hall_radius_one_2321_lra_compact.json);
- [partial_hall_radius_one_2321_lra_compact.smt2](partial_hall_radius_one_2321_lra_compact.smt2); and
- [partial_hall_radius_one_2321_model_audit_compact.json](partial_hall_radius_one_2321_model_audit_compact.json).

## Finite evidence for radius one

The stored-profile scan reconstructs every recognized distinct positive
four-agent profile through nine goods in the current results corpus.  Among
189 distinct profiles, exactly two have a maximum-Nash radius-zero failure;
both have a radius-one completion.  No maximum-Nash radius-one failure was
found.  The available ten-good tight profile also has a radius-one
completion.

An exact normalized-utilitarian scan now covers 208 distinct stored positive
profiles through ten goods.  It finds eight profiles whose maximizing state
fails radius-zero Hall completion, but every maximizing state in every profile
has a radius-one completion.  This includes the earlier linear-potential,
Pareto, and maximum-Nash refutation profiles.  See
[partial_hall_utilitarian_corpus_scan.json](partial_hall_utilitarian_corpus_scan.json).

This is finite falsification evidence, not a theorem.  The statewise exact
obstruction above was generated outside that preexisting corpus and confirms
that the selector condition cannot be dropped.  The adversarial search
selects maximum-Nash states by exact integer products and minimizes the best
row-normalized EFX slack over every radius-one partition and all 24 bundle
matchings.  A negative endpoint would be an exact counterexample to the
candidate, not to complete EFX.  Initial runs remain on the positive side of
the boundary.

## Analytic proof gate

Assume a maximum-Nash state is directly blocked.  The established
bundle-cycle lemma gives an unenvied source bundle.  If insertion at a source
is blocked by observer \(i\) after removing \(r\in X_h\), then

\[
v_i(X_h)\le v_i(X_i)
<v_i(X_h)-v_i(r)+v_i(f),
\]

and hence \(v_i(f)>v_i(r)\).  Every source blocker therefore identifies a
candidate displaced good and a strict floater supporter.  The radius-one
claim asks whether one such displacement necessarily destroys all Hall
deficiencies after rematching.

A proof must establish one of the following equivalent covering conclusions:

1. one radius-one feasibility graph satisfies Hall's condition for all agent
   subsets; or
2. if every radius-one graph has a Hall-deficient subset, the associated
   strict inequalities imply an eligible state with larger Nash product.

The second route is the sharper target.  It would turn simultaneous Hall
obstructions into an exchange cycle or a safe floater substitution,
contradicting maximum Nash.  Existing safe-exchange and bundle-cycle lemmas
provide the size-one units, but no covering theorem for all Hall witness
types is yet proved.

For the normalized-utilitarian selector, the required contradiction is
strictly linear: it suffices to construct any eligible rival \((Y,g)\) with

\[
\sum_i\frac{v_i(Y_i)-v_i(X_i)}{v_i(M)}>0.
\]

This avoids the nonlinear product comparison and is why the utilitarian gate
now has priority.

## Exact Pareto-selector refutation

The stronger Pareto-maximal candidate is false.  Exact QF_LRA CEGAR terminated
after 44 iterations and 3,561 learned rival exclusions with the positive
matrix

\[
\begin{pmatrix}
36&4&12&1045&1041&8&1049&1093&24\\
978&25&25&1038&65&1093&1078&1078&10\\
915&72&8&879&128&963&1039&212&96\\
213&1&1&210&1&216&216&216&4
\end{pmatrix}.
\]

For the canonical base and floater above, the utility vector is
\((2142,1088,1043,216)\).  Exhaustive enumeration finds 992 eligible states
and no strict Pareto dominator.  Independently, every one of the 91 radius-one
partitions and all 2,184 partition--matching pairs fail.  The profile has 98
Pareto-frontier states; the displayed state is the unique radius-one-blocked
one among them.  This refutes only the Pareto selector, not maximum Nash,
normalized utilitarian selection, or complete EFX.

Authoritative artifacts:

- [partial_hall_pareto_cegar_session1.json](partial_hall_pareto_cegar_session1.json);
- [partial_hall_pareto_cegar_model_audit.json](partial_hall_pareto_cegar_model_audit.json); and
- [partial_hall_pareto_cegar_completion_audit.json](partial_hall_pareto_cegar_completion_audit.json).

The current decisive gate is the normalized-utilitarian analogue.  Its CEGAR
master excludes every eligible rival of strictly larger \(\Phi\); terminal
SAT would be an exact refutation, while UNSAT would prove the selector for the
canonical \(2+3+2+1\) base cell.  Its implementation is
[`run_partial_hall_utilitarian_cegar.py`](../tracks/parkability/run_partial_hall_utilitarian_cegar.py).

### Normalized-utilitarian obstruction ladder

The current finite theorem candidate can be stated cleanly.  In the canonical
nine-good cell

\[
X=(\{6,7\},\{1,2,3\},\{0,4\},\{5\}),\qquad f=8,
\]

every eligible radius-one Hall obstruction has another eligible state of
strictly larger \(\Phi\) whose owner vector differs in at most five
coordinates (counting a change to or from the floater).  Equivalently, a
radius-five local maximum of \(\Phi\) cannot be radius-one Hall blocked in
this cell.  This is the exact statement under decision; even a proof would
still require a lifting argument for other bundle shapes and numbers of
goods.

Exact local CEGAR has now ruled out a bounded-exchange shortcut.  For each
radius \(d=2,3,4\), there is a positive canonical radius-one Hall obstruction
with no eligible state of larger \(\Phi\) whose owner vector differs in at
most \(d\) coordinates.  In each resulting profile, exhaustive enumeration
finds that the nearest larger-\(\Phi\) state has distance exactly \(d+1\).

The certified ladder is:

1. distance two blocked, nearest improvement at distance three;
2. distance three blocked, nearest improvement at distance four; and
3. distance four blocked, nearest improvement at distance five.

Every terminal profile independently passes the 91-partition and 2,184
partition--matching replay.  These results refute only bounded local
improvement lemmas.  Each profile still has hundreds of global
normalized-utilitarian improvements, so the global selector remains live.
Radius five is the first hard boundary.  Two CEGAR schedules reached a common
416-rival master after 13 successful iterations; default-seed, seed-211, and
phase-selection-5 replays all returned `unknown` at their bounded timeouts.
This is not a theorem verdict.  The frozen boundary is
[partial_hall_utilitarian_local_r5_phase5_gate.json](partial_hall_utilitarian_local_r5_phase5_gate.json).

The factored replay introduces one Boolean variable for each agent--bundle
EFX edge, avoiding repeated arithmetic expansion across the 24 matchings.
Closing the 416 learned rivals under the base-cell stabilizer
(S_2\times S_3\times S_2) yields 3,187 distinct valid rival exclusions.
Ordering agent 0's values within the three nonsingleton base bundles is a
sound 24-fold symmetry reduction.  The resulting frozen master has SHA-256
`2605cc33df9eb1205433d03fdd3c590f0f69c38f95419570fa19349259301c9d`
and an exact eight-branch cube cover.  These reductions preserve
satisfiability; they do not themselves decide radius five.  A second exact
split composes with that cover to produce 32 depth-five leaves, with every
intermediate and leaf formula hash checked by
[partial_hall_utilitarian_local_r5_orbit_seed_cubes_d5.json](partial_hall_utilitarian_local_r5_orbit_seed_cubes_d5.json).

A second semantics-preserving factorization shares every repeated rival
eligibility comparison.  An exact symbolic audit proves equivalence for all
3,187 orbit-closed blockers, reducing them to 4,065 distinct comparison
atoms and shrinking the master from 8.1 MB to 4.3 MB.  The double-factored
master hash is
`e80bfbfe1bd31c98c503d91d075cdab0fd1d652569ade66481ba4de5557f2ebe`.

An independent cvc5 replay of the normalized double-factored master also
returned `unknown (TIMEOUT)`; this is provenance, not a theorem verdict.
Adversarial optimization subsequently reached a blocked state at
`0.9985823876150579` of the exact global normalized-utilitarian maximum.
Freezing its complete eligibility and Hall-edge cell yields a Z3/cvc5 UNSAT
system with a five-inequality human proof: the cell forces an eligible rival
to strictly improve agents 1 and 2 while leaving agents 0 and 3 unchanged. A
second, independently reached cell is also exact UNSAT, with an
eight-constraint core. These are local exclusion lemmas, not a cover of the
obstruction space. See
[PARTIAL_HALL_UTILITARIAN_FROZEN_CELL_GATE.md](PARTIAL_HALL_UTILITARIAN_FROZEN_CELL_GATE.md).
The cleaner core has also been lifted to a dual-verified analytic
completion-or-improvement lemma with 13 deletion-irreducible support
comparisons: either one of two explicit radius-one completions works, or an
explicit eligible partial allocation has strictly larger potential.
The algebraic pattern is now stated cap-free for arbitrary $n,m$ and
nonnegative additive valuations as the
[two-wall Hall conversion lemma](PARTIAL_HALL_TWO_WALL_CONVERSION_LEMMA.md).
It is conditional and therefore not yet the missing global completion
theorem.
The second frozen cell independently gives a cap-free
[six-wall replacement lemma](PARTIAL_HALL_SIX_WALL_REPLACEMENT_LEMMA.md),
another exact potential-improvement conversion type.
The known Pareto-maximal obstruction cell is separately excluded by a
[three-rival weighted-cycle certificate](PARTIAL_HALL_THREE_RIVAL_WEIGHTED_CYCLE.md),
whose 25 nonzero Farkas multipliers cancel exactly.

Artifacts:

- [partial_hall_utilitarian_local_cegar_session1.json](partial_hall_utilitarian_local_cegar_session1.json)
  and
  [partial_hall_utilitarian_local_cegar_session1_audit.json](partial_hall_utilitarian_local_cegar_session1_audit.json);
- [partial_hall_utilitarian_local_r3_cegar_session1.json](partial_hall_utilitarian_local_r3_cegar_session1.json)
  and
  [partial_hall_utilitarian_local_r3_cegar_session1_audit.json](partial_hall_utilitarian_local_r3_cegar_session1_audit.json); and
- [partial_hall_utilitarian_local_r4_cegar_session1.json](partial_hall_utilitarian_local_r4_cegar_session1.json)
  and
  [partial_hall_utilitarian_local_r4_cegar_session1_audit.json](partial_hall_utilitarian_local_r4_cegar_session1_audit.json); and
- [partial_hall_utilitarian_local_r5_orbit_seed_build.json](partial_hall_utilitarian_local_r5_orbit_seed_build.json),
  [partial_hall_utilitarian_local_r5_orbit_seed_master.smt2](partial_hall_utilitarian_local_r5_orbit_seed_master.smt2),
  and
  [partial_hall_utilitarian_local_r5_orbit_seed_cubes_d5.json](partial_hall_utilitarian_local_r5_orbit_seed_cubes_d5.json).
- [partial_hall_utilitarian_local_r5_double_factored_seed_build.json](partial_hall_utilitarian_local_r5_double_factored_seed_build.json),
  [partial_hall_utilitarian_local_r5_double_factored_audit.json](partial_hall_utilitarian_local_r5_double_factored_audit.json),
  and
  [partial_hall_utilitarian_local_r5_double_factored_seed_cubes_d3.json](partial_hall_utilitarian_local_r5_double_factored_seed_cubes_d3.json).
- [partial_hall_utilitarian_frozen_cell_seed17_cont117_core.json](partial_hall_utilitarian_frozen_cell_seed17_cont117_core.json)
  and
  [PARTIAL_HALL_UTILITARIAN_FROZEN_CELL_GATE.md](PARTIAL_HALL_UTILITARIAN_FROZEN_CELL_GATE.md).

## Reproduction

Exact audit of the three frozen profiles:

```sh
python tracks/parkability/audit_partial_hall_completion.py \
  results/partial_nash_completion_refutation_profile.json \
  results/partial_nash_one_transfer_refutation_profile.json \
  results/partial_nash_source_completion_refutation_profile.json \
  --output /tmp/partial_hall_completion_audit.json
```

Corpus scanner:

```sh
python tracks/parkability/scan_partial_hall_completion.py \
  --directory results --max-goods 9 \
  --output /tmp/partial_hall_completion_corpus.json
```

Rebuild the symmetry-closed radius-five master:

```sh
python tracks/parkability/run_partial_hall_utilitarian_local_cegar.py \
  --output /tmp/r5-orbit-build.json \
  --checkpoint /tmp/r5-orbit-checkpoint.json \
  --smt2-output /tmp/r5-orbit-master.smt2 \
  --max-iterations 0 --batch-size 32 --timeout-seconds 600 \
  --break-good-symmetry --radius 5 --random-seed 211 --factored-hall \
  --seed-from results/partial_hall_utilitarian_local_r5_cegar_session4_seed211.json \
  --symmetry-close
shasum -a 256 /tmp/r5-orbit-master.smt2
```

The expected master hash is
`2605cc33df9eb1205433d03fdd3c590f0f69c38f95419570fa19349259301c9d`.

Adversarial search:

```sh
python tracks/parkability/anneal_partial_hall_completion.py \
  --seed results/partial_nash_completion_refutation_profile.json \
  --iterations 2000 --random-seed 211 \
  --output /tmp/partial_hall_completion_anneal.json
```

Authoritative exact artifact:
[partial_hall_completion_refutation_audit.json](partial_hall_completion_refutation_audit.json).

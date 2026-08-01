# Cap-5 Full-Cell Closure in the Distinct-Half Branch

**Status:** independently corroborated finite-domain computer-assisted theorem  
**Scope:** four agents, nine goods, strictly positive integer item values at
most five, inside the strict-common-favorite distinct-half branch  
**Not claimed:** arbitrary integer values, real-valued instances, all
four-agent/nine-good instances, or general additive EFX

## Theorem

Let four agents have additive valuations for nine goods, with every item
value in \(\{1,2,3,4,5\}\). Assume:

1. good \(f\) is a strict common favorite;
2. every agent fails the favorite-singleton owner threshold, equivalently,
   if that agent's eight residual values are
   \(x_1\ge\cdots\ge x_8\) and \(F=v(f)\), then
   \[
   x_5+x_6+x_7>F,
   \qquad
   x_3+x_7>F\ \text{ or }\ x_4+x_5>F;
   \]
3. the half-favorite bipartite graph, joining agent \(i\) to each residual
   good \(g\ne f\) with \(2v_i(g)>v_i(f)\), has a matching saturating the
   four agents.

Then a complete EFX allocation exists. More precisely, at least one of the
following holds:

- a balanced partition of shape \(3+2+2+2\), with \(f\) in a pair,
  supports EFX; or
- two residual goods \(a,b\) have the property that **all 15** perfect
  pairings of the other six goods pass the favorite-triple Hall test for
  \(\{f,a,b\}\).

The second alternative supports EFX by the cap-free
[favorite-triple Hall characterization](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md).

## Basic explanation

After relabeling, agent \(i\) has a distinct representative good \(i+1\)
worth more than half its favorite. There are 840 ways to form a balanced
partition in which the favorite belongs to a pair. For any fixed two low
goods \(a,b\), there are 15 ways to pair the other six goods. Each pairing
works when its three pairs can be assigned to three different agents at
the thresholds

\[
v_i(P)\ge v_i(f)+\max\{v_i(a),v_i(b)\}.
\]

The computation assumes that selected favorite-pair partitions all fail
and that no low pair makes all 15 favorite-triple pairings work. It proves
those assumptions inconsistent. Therefore one of the two displayed repair
types must exist.

## Exact computational proof

The first encoding is a bounded CP-SAT model over the 36 item values. It
contains the three branch assumptions, directly forbids all 28 possible
full Hall cells, and obstructs a learned pool of favorite-pair partitions.
A 416-partition pool is infeasible. Assumption-core extraction reduces it
to 330 favorite-pair partitions.

The 330-partition core was then regenerated in a separate QF_LIA encoding:

- the CP model encodes the universal-threshold condition with integer and
  Boolean constraints; the arithmetic replay uses an exact sorting
  envelope;
- the CP and arithmetic formulas independently encode the no-full-cell
  Hall witnesses; and
- CP-SAT reports `INFEASIBLE`, while Z3 reports `unsat` on the integer
  arithmetic replay in 120.24 seconds.

Z3 assumption analysis then reduced the sufficient partition pool from 330
to 204 and finally 193. A third implementation translated that statement
to monotone-threshold CNF without importing either CP-SAT or the Z3
arithmetic encoder. It represents each item value with four order bits,
encodes strict sum inequalities with sequential counters, expresses the
universal-threshold premise through the independent four-set/pair-degree
characterization, and uses direct rejection witnesses for both Hall and
EFX failure.

CaDiCaL assumption shrinking reduced the 193-partition CNF pool to 17
partitions. A separate verifier establishes deletion minimality: all 17
together are inconsistent, while removing any one yields an exact
branch-valid cap-5 profile with no full Hall cell, repaired uniquely within
the core by the removed partition. The guard-free 17-core formula is:

- 337,000 variables;
- 702,820 clauses;
- 17,550,308-byte DIMACS input; and
- `UNSAT` in 11.54 CPU seconds in the frozen CaDiCaL 1.9.5 run.

CaDiCaL also emitted a 44,563,875-byte binary DRAT proof. The independent
`drat-trim` checker accepted it in 3.59 seconds, reducing the certificate to
54,688 input clauses and 92,744 proof lemmas with 593,400 resolution steps.
The compressed release proof is 9,073,548 bytes.

All inequalities are strict or weak integer inequalities exactly as
written; there is no numerical tolerance. The symmetry constraints are
without loss of generality: agents are ordered by favorite value, their
matched representative goods are relabeled as 1 through 4, and the four
unmatched goods are ordered by agent 0's values.

## Reproducibility and trust boundary

The deterministic manifest is
[efx49_distinct_half_full_cell_cap5_audit.json](efx49_distinct_half_full_cell_cap5_audit.json).
It reconstructs the 55-partition seed complement and 361 learned repairs,
checks the nested 416-to-330-to-204-to-193-to-17 partition chain,
revalidates all 17 deletion boundaries, checks the trace model against the
structural branch and the literal full-cell test, and pins every artifact
by SHA-256.

Primary artifacts:

- [CP-SAT CEGAR result](efx49_distinct_half_full_cell_cpsat_cegar_cap5_session1.json);
- [330-partition CP-SAT assumption core](efx49_distinct_half_full_cell_cpsat_cap5_core1.json);
- [independent QF_LIA result](efx49_distinct_half_full_cell_lia_cap5_core1_session1.json); and
- [self-contained QF_LIA formula](efx49_distinct_half_full_cell_lia_cap5_core1_session1.smt2);
- [204-partition](efx49_distinct_half_full_cell_lia_cap5_core2.json) and
  [193-partition](efx49_distinct_half_full_cell_lia_cap5_core3.json) Z3
  assumption cores;
- [deletion-minimal 17-partition core and boundary profiles](efx49_distinct_half_full_cell_cap5_minimal_core.json);
- [independent threshold CNF](efx49_distinct_half_full_cell_cap5_core17.cnf);
- [CaDiCaL result](efx49_distinct_half_full_cell_cap5_core17_cadical.json);
- [checked DRAT manifest](efx49_distinct_half_full_cell_cap5_core17_drat_verification.json); and
- [compressed binary DRAT proof](../output/cap5-certification/efx49_distinct_half_full_cell_cap5_core17.drat.xz).

The no-full-cell encodings also have positive and negative semantic controls
in
[efx49_distinct_half_full_cell_encoding_audit.json](efx49_distinct_half_full_cell_encoding_audit.json).
The threshold-CNF translation has its own four-way semantic polarity test:
[efx49_distinct_half_full_cell_cnf_encoding_audit.json](efx49_distinct_half_full_cell_cnf_encoding_audit.json).

This is a genuine bounded theorem, but it is not close to the general claim
by value-cap monotonicity: per-agent scaling does not reduce arbitrary
ratios to five levels. The CP-SAT, QF_LIA, and threshold-CNF results are
three separately audited encodings, and the final CNF verdict now has a
checked proof object. The remaining formal trust boundary is the semantic
translation from additive EFX to the CNF, which is protected by four
polarity controls but is not machine-proved in Lean. The next mathematical
step is not to promote the 17 literal templates: a cap-6 profile already
obstructs all of them while retaining 138 favorite-pair repairs. The
17-core instead occupies six of the ten natural representative/free-good
partition orbits. Their 624-partition symmetry closure is now exactly
refuted at cap 20: a branch-valid profile with no full Hall cell has all 45
favorite-pair repairs in two omitted orbits and has 900 labeled complete
EFX allocations. The certificate remains valid; only this proposed
cap-free generalization fails.
See [DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md](DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md).

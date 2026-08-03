# Cap-6 Full-Cell Closure in the Distinct-Half Branch

**Status:** independently certified finite-domain computer-assisted theorem  
**Scope:** four agents, nine goods, strictly positive integer item values at
most six, inside the strict-common-favorite distinct-half branch  
**Not claimed:** arbitrary integer values, real-valued instances, all
four-agent/nine-good instances, or general additive EFX

## Theorem

Let four agents have additive valuations for nine goods, with every item
value in \(\{1,2,3,4,5,6\}\). Assume:

1. good \(f\) is a strict common favorite;
2. every agent fails the favorite-singleton owner threshold, equivalently,
   if that agent's residual values are
   \(x_1\ge\cdots\ge x_8\) and \(F=v(f)\), then
   \[
   x_5+x_6+x_7>F,
   \qquad
   x_3+x_7>F\ \text{ or }\ x_4+x_5>F;
   \]
3. the half-favorite graph, joining agent \(i\) to residual good \(g\)
   when \(2v_i(g)>v_i(f)\), has a matching saturating all four agents.

Then a complete EFX allocation exists. More precisely, either:

- a balanced \(3+2+2+2\) partition with \(f\) in a pair supports EFX; or
- some residual pair \(a,b\) makes all 15 pairings of the other six goods
  pass the favorite-triple Hall test for \(\{f,a,b\}\).

The second alternative supports EFX by the cap-free
[favorite-triple Hall characterization](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md).

## What the computation proves

After relabeling a half-favorite matching as goods 1 through 4, there are
840 balanced partitions with the favorite in a pair. The computation
simultaneously assumes that selected partitions are Hall-obstructed and
that none of the 28 possible low pairs gives a full 15-pairing Hall cell.
It proves those assumptions inconsistent.

Three independent encodings support the conclusion:

1. CP-SAT learns a 401-partition obstruction pool and proves it
   infeasible; its assumption core has 359 partitions.
2. A separately generated sorting-based QF_LIA formula reconstructs that
   core and Z3 returns `unsat`; assumption extraction reduces it to 175
   partitions.
3. A monotone-threshold CNF implementation independently encodes the
   bounded arithmetic, universal-threshold premise, Hall-cell negation,
   and EFX obstructions.

Repeated CaDiCaL assumption reduction followed by a separate deletion
replay leaves 21 partitions. All 21 together are inconsistent; deleting
any one yields a branch-valid cap-6 profile with no full Hall cell for
which the deleted partition is the unique repair within the core.

The final guard-free CNF has:

- 557,152 variables;
- 1,145,090 clauses;
- 29,332,111 bytes of DIMACS; and
- a 75,953,525-byte binary DRAT proof.

`drat-trim` independently verifies the proof in 6.96 seconds. Its backward
core contains 97,980 input clauses and 169,654 proof lemmas, using
1,918,897 resolution steps. The compressed proof is 16,790,568 bytes.

All arithmetic is exact. The symmetry constraints are without loss of
generality: agents are ordered by favorite value, matched representatives
are relabeled 1 through 4, and unmatched goods 5 through 8 are ordered by
agent 0's values.

## Hall-witness proof mining

Across the 21 deletion boundaries, 572 of 588 low-pair cells already fail
through a single residual edge rejected by all four agents; only 9 cells
need a size-two Hall witness and 7 need a size-three witness. All 126 cells
whose low pair consists of two matched representatives have a size-one
witness. In 17 of the 21 profiles, one unrepresented edge is a witness for
all six representative-pair cells; the other four profiles have minimum
witness-edge covers of size two or three. This is descriptive certificate
data, not part of the theorem and not a cap-free lemma. The deterministic census is
[efx49_distinct_half_full_cell_cap6_hall_witness_census.json](efx49_distinct_half_full_cell_cap6_hall_witness_census.json).

## Reproducibility and trust boundary

The deterministic semantic manifest is
[efx49_distinct_half_full_cell_cap6_audit.json](efx49_distinct_half_full_cell_cap6_audit.json).
It reconstructs the CEGAR pool, validates the nested CP-SAT and QF_LIA
cores, checks the deletion-minimal 21-core, and binds the final CNF and
proof by SHA-256.

Primary artifacts:

- [CP-SAT CEGAR result](efx49_distinct_half_full_cell_cpsat_cegar_cap6_session1.json);
- [359-partition CP-SAT core](efx49_distinct_half_full_cell_cpsat_cap6_core1.json);
- [independent QF_LIA result](efx49_distinct_half_full_cell_lia_cap6_core1_session1.json);
- [self-contained QF_LIA formula](efx49_distinct_half_full_cell_lia_cap6_core1_session1.smt2);
- [175-partition QF_LIA core](efx49_distinct_half_full_cell_lia_cap6_core2.json);
- [verified deletion-minimal 21-core](efx49_distinct_half_full_cell_cap6_minimal_core_verified.json);
- [independent threshold CNF](efx49_distinct_half_full_cell_cap6_core21.cnf);
- [CaDiCaL result](efx49_distinct_half_full_cell_cap6_core21_cadical.json);
- [checked DRAT manifest](efx49_distinct_half_full_cell_cap6_core21_drat_verification.json); and
- [compressed proof](../output/cap6-certification/efx49_distinct_half_full_cell_cap6_core21.drat.xz).

This advances the certified finite ladder from cap 5 to cap 6. It does not
lift by scaling: arbitrary positive-real value ratios need not have a
six-level representative. The remaining high-leverage question is still a
cap-free selection lemma—currently the full-cell dichotomy or a smaller
partner/orbit family that implies it. The semantic translation to CNF is
audited with positive and negative controls but is not machine-verified in
Lean.

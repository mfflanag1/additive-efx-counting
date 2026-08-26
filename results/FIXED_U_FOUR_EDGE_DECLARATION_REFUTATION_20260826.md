# The universal four-split form-2 theorem is false: the four-edge declaration fails

**Date:** 2026-08-26  
**Branch:** `cc/efx-four-role-20260826` (off `codex/efx-fixed-u-resume-20260820`, 69c1dcd)  
**Status:** exact obstruction to the stated theorem, independently verified by
three encodings (z3 Boolean one-hot, z3 integer-owner, OR-tools CP-SAT). General
additive EFX is not refuted.

## 0. Verdict

The proposed theorem

> every admissible form-2 profile and every physical realization consistent with
> it admits a complete EFX allocation using at most four support-transfer edges
> and at most four split roles

is **false**, and it fails in the stronger of the two possible ways. The pinned
admissible profile `results/fixed_u_tame_or_anchor_cegar_20260821.json` has a
two-good realization -- obtained from the all-coincident realization by moving
observer `s`'s minimum-witness good in just the three roles `j`, `m`, `gq` --
for which **no complete EFX allocation with at most four support-transfer edges
exists at any number of split roles** (caps 0 through 12 and unbounded all
UNSAT). This is a counterexample of type (b): the four-edge declaration, not the
four-role budget, is what breaks. Five edges suffice, and with five edges **no
role needs to be split at all**.

Corrected parameter: the **support-edge count**, not the split multiplicity.
On every one of the 296 retained admissible form-2 profiles (205 chart-ledger
models, 81 tame-or-anchor rounds plus terminal, 7 dynamic-anchor rounds plus
terminal, the wild-forced terminal), the adversarial two-good CEGAR at **five
edges and zero splits** closes. The entire split apparatus of the last three
weeks is an artifact of the four-edge cap.

## 1. Definitions (unchanged)

Owners `r,q,d,s`; charity is a supplier only. Roles and suppliers are the
`SUPPORT_STATE` of `run_fixed_u_full_packet_terminal_cegar`: `r` supplies
`a0,a1,h`; `q` supplies `j,k,q0`; `d` supplies `m,gq,gr`; `s` supplies `l,e`;
charity supplies `p`. A profile is the exact rational `(T_i(role), M_i(role))`
table; admissibility is `build_physical_master(2)` SAT at those values
(replayed by every verifier). A two-good realization gives each non-singleton
role goods `role:0, role:1` with `v_i(role:0)=M_i+b_i(T_i-2M_i)`,
`v_i(role:1)=T_i-v_i(role:0)`; `b_i` is observer `i`'s side bit. A complete
allocation assigns every good to one of the four owners, every owner nonempty;
EFX is `U_i(B_i) >= U_i(B_j) - v_i(g)` for all `i != j`, `g in B_j`; an edge is
a pair `(supplier(role), owner)` with `owner != supplier`; a split role has
goods at two or more owners. The widest oracle ranges over every complete
allocation with the stated caps and nothing else.

## 2. Calibrations (all pass before any new claim)

* Baseline replay of the two 2026-08-21 audits: byte-identical,
  `0237ad9c...1365` and `359ed19d...9ba8`; `pytest -q
  tracks/parkability/test_fixed_u_pattern_mixed_four_split.py` 5 passed.
* The pinned product cell replays: split caps 0-3 UNSAT, 4 SAT, edges
  `charity->d, d->r, q->s, r->q`, split roles `{a0,j,k,m}`, values byte-equal
  to the pinned physical table (scratch oracle and both repo encodings).
* Master admissibility replay SAT in every verifier.

## 3. The obstruction (exact)

Side pattern (all other bits 0): `j:s=1, m:s=1, gq:s=1`. Minimality: the
pattern CEGAR with at most 1 and at most 2 side bits closes (UNSAT); at 3 bits
it returns this pattern. Physical values are frozen in
`results/fixed_u_four_edge_obstruction_20260826.json` (`physical_values`).

Verdict matrix (primary z3 one-hot / independent CP-SAT, both exact):

| edge cap | split cap | status |
|---|---|---|
| 3 | 0 / 4 / unbounded | UNSAT |
| 4 | 0 / 4 / unbounded | UNSAT |
| 5 | 0 | SAT, e.g. `charity->d, d->r, q->s, r->d, r->q`, no split |
| 5 | 4 / unbounded | SAT |
| none | 0 | SAT |

Kernel (`results/fixed_u_four_edge_obstruction_kernel_20260826.json`):

* all **1,196** four-edge support topologies (charity target x at most three
  owner edges) are individually UNSAT;
* deleting any single observer's EFX inequalities makes the four-edge system
  SAT -- all four observers are load-bearing;
* deleting any single ordered envy pair makes it SAT except `d->s`; so no
  single pair carries the obstruction: it is a genuinely global coordination
  failure, which is why no local menu, anchor or split rule could find it;
* exactly five five-edge topologies admit a zero-split complete EFX
  allocation, all containing the charity edge and four owner edges;
* weakened hypothesis: if `p` may stay with charity (incomplete allocation),
  four and even three edges suffice -- the forced charity transfer is the
  binding resource.

The two other adversarial patterns found first (`pinned_cap4/5/6` in the
scratch runs) have the same verdict matrix; the continuous two-good CEGAR
(interior side values) reproduces an obstruction as well.

## 4. Census of all retained admissible profiles (two-good realizations)

`results/fixed_u_four_edge_two_good_split_census_20260826.json`, 296 profiles,
adversarial min split count under the four-edge cap:

| min splits needed (worst two-good realization) | profiles |
|---|---:|
| 0 | 226 |
| 1 | 44 |
| 2 | 23 |
| 3 | 2 (`tameanchor_1cec10e1...`, one bit `m:s`; `tameanchor_911e2ab5...`) |
| 4 | 0 among worst cells; the pinned profile's 2026-08-21 product cell needs exactly 4 |
| none (four edges impossible) | 1 (the pinned profile) |

Five edges, zero splits: **296/296 closed**. These are the equality examples for
deliverable 4: profiles whose hardest two-good realization needs exactly 1, 2, 3
split roles under four edges, and the pinned cell needing exactly 4.

## 5. The split-role incidence/charge formulation and its exact failure

Charge a split role to the edge its non-supplier piece rides. In every
four-edge certificate found (the 2026-08-21 cell: `a0->r->q`, `j,k->q->s`,
`m->d->r`) the charge is injective, and the injectivity of forced splits to
support edges would indeed bound splits by edges. The obstruction shows the
premise is wrong: the binding constraint is not how many roles must split but
whether four edges can carry a complete EFX allocation at all. Once a fifth
edge is available the charge map is empty (no splits). The distinct-charge
lemma therefore fails vacuously rather than combinatorially: forced splits are
an artifact of an edge budget that is itself infeasible on some realizations.

## 6. Cap-free (three-or-more goods) probe and a solver warning

With every `T>=3M` role given three goods and real-valued adversarial
realizations, the five-edge zero-split CEGAR on the pinned profile closes in one
round. A four-edge three-good run reported an "obstruction" whose saved values
are SAT under the same caps on replay (z3 and CP-SAT): an in-loop z3 UNSAT on
the Boolean-PB-plus-LRA encoding was wrong. Consequence: **no z3-only UNSAT is
banked in this note**; every UNSAT that carries weight is confirmed by CP-SAT
(verdict matrix) and, for the four-edge topology census, by a CP-SAT replay
(`results/fixed_u_four_edge_topology_census_cpsat_20260826.json`: 1,196 UNSAT).

## 7. Interface handed to the complete-EFX closure (deliverable 6)

What the closure step may assume about the saturated fixed-U separator:

* not the four-edge declaration -- it is false for admissible form-2 data;
* on the 296 retained admissible profiles, every two-good realization admits
  a complete EFX allocation with **five** support-transfer edges and **no**
  split role (finite census, not a theorem);
* the sharp open lemma is the cap-free five-edge zero-split statement for every
  admissible profile and every realization, i.e. a five-edge whole-role
  selector theorem; its obstruction, if any, must be a profile outside the 296
  or a many-good realization, and any such claim must be CP-SAT-confirmed.

## 8. Hostile-review checklist

1. *Could the pattern solver's cut be unsound (an allocation excluded that is
   EFX elsewhere)?* The cut says only "this allocation is not EFX under the
   pattern", exact linear in side bits; obstruction claims never rely on cuts,
   only on the final oracle UNSAT, which is CP-SAT confirmed.
2. *Is the realization consistent with the profile?* Per role and observer the
   two goods have the prescribed sum and minimum; the independent verifier
   asserts both with `Fraction`.
3. *Is the profile admissible?* Master replay SAT (three verifiers).
4. *Nonempty-bundle constraint?* Dropping it does not change the four-edge
   verdict (kernel run).
5. *Is "complete" the right notion?* Yes by the stated theorem; the incomplete
   variant (p at charity) is recorded as a weakened-hypothesis countermodel.
6. *z3 soundness.* See section 6; the primary artifact's UNSAT rows are all
   duplicated by CP-SAT in the independent audit.
7. *Selector-artifact law.* No restricted driver is involved: the oracle is the
   widest allocation family, no template, no cap on splits.

## 9. Reproduction

```bash
python -m tracks.parkability.audit_fixed_u_four_edge_obstruction \
  --profile results/fixed_u_tame_or_anchor_cegar_20260821.json \
  --output results/fixed_u_four_edge_obstruction_20260826.json --timeout-seconds 120
python -m tracks.parkability.independently_verify_fixed_u_four_edge_obstruction \
  --profile results/fixed_u_tame_or_anchor_cegar_20260821.json \
  --primary-audit results/fixed_u_four_edge_obstruction_20260826.json \
  --output results/fixed_u_four_edge_obstruction_independent_audit_20260826.json
python -m tracks.parkability.analyze_fixed_u_four_edge_obstruction_kernel \
  --profile results/fixed_u_tame_or_anchor_cegar_20260821.json \
  --primary-audit results/fixed_u_four_edge_obstruction_20260826.json \
  --output results/fixed_u_four_edge_obstruction_kernel_20260826.json
pytest -q tracks/parkability/test_fixed_u_four_edge_obstruction.py
```

Not claimed: any EFX counterexample; any statement about profiles outside the
declared form-2 master; the five-edge zero-split law beyond the 296-profile
two-good census and the single three-good probe.

Frozen artifact hashes:

```text
b94b7e010f9c8aad82b738e2384ef46301adba4c9e648666d78d65ecf1d6fa73  results/fixed_u_four_edge_obstruction_20260826.json
33c143c43791f61e58142dacd67187eb2e7cd8ee2fbb1311311d2f1ede8068a2  results/fixed_u_four_edge_obstruction_independent_audit_20260826.json
c6fc68d7badb1952af27d0fd3ab7e70158023fe9e168fa8efeb291810a5907f5  results/fixed_u_four_edge_obstruction_kernel_20260826.json
6f8b49babdca87b93bc1abf1e0109431b132aa31d976c4fd6c50280a02c05791  results/fixed_u_four_edge_two_good_split_census_20260826.json
9e087f87c7cad7917a0e9dcbe371c480ded0c233226abd6a93314e2b494d6a4f  results/fixed_u_four_edge_topology_census_cpsat_20260826.json
```

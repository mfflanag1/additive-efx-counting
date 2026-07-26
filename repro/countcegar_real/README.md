# Exact-real counting CEGAR prototype

This package tests the unrestricted positive-real statement

> Every positive additive `4 x 7` valuation matrix has at least four
> EFX0 allocations.

It is a research prototype, not a completed theorem or a paper claim.

## Exact master

The master uses a homogeneous fixed-margin representation. It has real
variables `x[i,g] >= 1` and one common row total `T`, with

```text
sum_g x[i,g] = T
```

for every agent. Semantically, `v[i,g] = x[i,g]/T`; hence every row is
positive and normalized to sum one. Per-agent positive scaling does not change
EFX0.

For a pooled allocation `A`, observer `i`, target owner `j=A[g]`, and removed
good `g`, strong envy is represented by

```text
sum_{q in A_j \ {g}} x[i,q] - sum_{q in A_i} x[i,q] >= 1.
```

Three one-hot allocation slots protect at most three pooled EFX0 allocations.
Every other pooled allocation must have one of the unit-margin strong-envy
witnesses above. Row and column DoubleLex use equality or a first strict
difference of at least one.

### Formal soundness lemma

**Lemma (finite-pool protected-slot soundness).** Let `P` be any finite set of
labeled allocations. If either exact master is UNSAT on `P`, then every
strictly positive `4 x 7` additive valuation matrix has at least four EFX0
allocations.

**Proof.** Suppose instead that a positive valuation `v` has at most three
EFX0 allocations in total. Scale each agent's row independently so that every
row sums to one; this preserves all EFX0 comparisons. Among the finite orbit
under row and good permutations, choose a matrix whose row-major flattening is
lexicographically greatest. Its adjacent rows are nonincreasing in
lexicographic order, since otherwise swapping an inverted pair would increase
the flattening. Its adjacent columns are also nonincreasing: swapping an
inverted pair changes the flattening first in the earliest row where those
columns differ and increases it. Thus this orbit representative satisfies
semantic row and column DoubleLex. Agent and good relabeling preserves the
total number of labeled EFX0 allocations, so at most three members of `P` are
EFX0 for the representative.

Put those EFX0 members of `P` into the three protected slots, using arbitrary
values for unused slots. For every other allocation in `P`, non-EFX0 supplies
an observer, target bundle, and removed good with a strictly positive
strong-envy gap; select one such violation. Now take `delta` to be the minimum
of all normalized positive entries, all selected positive violation gaps, and
all positive first differences in unequal adjacent DoubleLex comparisons.
This is the minimum of a finite nonempty set of positive reals. Divide every
entry by `delta`. Rows still have one common total, entries are at least one,
and every selected violation and strict DoubleLex difference is at least one.
The protected-slot master is therefore SAT. The cardinality master is SAT for
the same valuation because exactly the EFX0 members of `P` make its equivalence
variables true and there are at most three.

Conversely, divide any fixed-margin model by its positive common row total.
This gives strictly positive normalized rows and preserves every weak EFX0
comparison. In the slot formulation, an EFX0 member of `P` cannot satisfy a
strong-envy disjunct, so it must match a slot. One one-hot slot cannot match two
distinct allocations, hence at most three members of `P` are EFX0. The
cardinality formulation states the same fact directly. Therefore any global
counterexample would satisfy both finite-pool masters, proving the
contrapositive. ∎

The unit margin is consequently exact, not a discretization.

## Differential tests

From the repository root:

```sh
python repro/countcegar_real/test_countcegar_real.py
```

The test fixes two positive matrices, including the paper's count-four
`t47.json`, and checks both the literal-slot and independent pooled-cardinality
formulations. Empty pools and pools with three EFX0 allocations must be SAT;
four distinct EFX0 allocations must be UNSAT; non-EFX0 allocations must be
killable. It also checks the lexicographic margin comparator, strict pool
validation, and exact rational-to-integer decoding. Additional regressions
exhaust all 64 binary `2 x 3` matrices and verify that every row/good
permutation orbit has a simultaneous DoubleLex representative, exercise a
fractional lex gap before and after global scaling, compare all `4^7` EFX0
predicates before and after rowwise rational integerization, and close a
controlled count-four master by adding its one fresh CEGAR cut. A two-invocation
integration case checks the checked/post-cut result fields, cumulative trace
numbering, and rejection of a mismatched resume pool.

## First feasibility run

The first master check warm-starts from the archived 1,240-allocation terminal
pool of the bounded `K=4` computation:

```sh
python repro/countcegar_real/countcegar_real.py \
  --seed-pool results/countpool_K4_complete.json \
  --pool-out results/countpool_real_4x7.json \
  --result-out results/countcegar_real_4x7.json \
  --trace-out results/countcegar_real_4x7.jsonl \
  --export results/countcegar_real_4x7.smt2 \
  --timeout-ms 300000 \
  --max-rounds 1
```

`SAT` is only a CEGAR candidate. The program clears rational denominators
exactly, enumerates all `4^7` allocations, and either reports a matrix with at
most three EFX0 allocations or adds fresh EFX0 allocations. `UNKNOWN` is
inconclusive. A solver-reported `UNSAT` requires an independent encoding or
proof artifact before promotion to a theorem.

No dominant-good, universal-minimum, distinct-row, or other structural cuts
from the older existence search are used here.

## Recorded feasibility checkpoint

On 2026-07-26, both formulations independently refined copies of the archived
1,240-allocation integer pool. Their resulting pools were merged and refined
again from a common 2,300-allocation seed. Every SAT model was integerized
exactly and checked over all `4^7` allocations before its fresh EFX0
allocations were added.

The slot run found candidates with 17 and 15 EFX0 allocations, then timed out
after 60 seconds on its third master check at pool size 2,328. The cardinality
run found candidates with 12, 23, 14, and 17 EFX0 allocations, then timed out
after 60 seconds on its fifth check at pool size 2,354. Their merged
2,380-allocation continuation pool is:

```text
results/countpool_real_4x7_checkpoint.json
SHA-256 83763a044c7f2874241c6caae606ac8d04a2b4c92c2897de70f3fd282195b69e
```

The terminal run records are
`results/countcegar_real_4x7_union_slots.json` and
`results/countcegar_real_4x7_union_cardinality.json`. Both say `UNKNOWN`; the
checkpoint is neither a theorem nor evidence for a counterexample. It is a
reproducible warm start for a longer run or a stronger exact-LRA backend.

The continuation was then run through both formulations again. Across the
retained branches there are 80 SAT-refinement rounds: 28 in the earlier slot
branch, 50 in the earlier/cardinality continuation, and one final check in
each formulation. The lowest-count master candidate encountered had eight
EFX0 allocations. Both exact verifiers agree on that count; the matrix and all
eight allocations are retained in
`results/countcegar_real_4x7_best8.json`. It is a CEGAR diagnostic, not an
extremal instance or a counterexample, since the paper already contains a
count-four witness.

The final slot check remained SAT, added 11 allocations, and produced a pool
of size 2,624. The final cardinality check on that pool also remained SAT,
added 12 allocations, and produced the current common continuation pool:

```text
results/countpool_real_4x7_final_cardinality.json
SHA-256 3cf2872437d134d2083c7bbdf9cb6e0837284e24c88da99dd126fcfb3e406ad2
```

The corresponding standalone formulas and run records are:

```text
results/countcegar_real_4x7_final_slots.smt2
results/countcegar_real_4x7_final_slots.json
results/countcegar_real_4x7_final_cardinality.smt2
results/countcegar_real_4x7_final_cardinality.json
```

Both JSON records say `CHECKPOINT`, not `UNSAT` or `WITNESS`. The final pool is
an ordinary set of allocations and can warm-start either formulation.

The checkpoint result schema distinguishes the pool actually checked from the
pool after refinement. `checked_pool_size` and `checked_pool_sha256` identify
the former. `cuts_added_after_last_check`, `export_formula_stage`, and
`export_formula_checked` state that a terminal `CHECKPOINT` export is the
post-cut formula and has not itself been checked. New trace records also carry
an invocation identifier, an invocation-local round, and a cumulative record
number. On `--resume`, the last trace pool hash and size must match the selected
source pool; older records without the new identifiers remain readable.

An independent line-by-line audit found no soundness or CEGAR-completeness
defect in the implementation. That audit is not a solver-independent
certificate: the two formulations still share normalization, bundle, and
symmetry code. Any eventual `UNSAT` result must still pass an independent
terminal encoding, preferably symmetry-free or proof-producing.

The closure validator checks every manifest hash, reconstructs all seven
retained trace branches from their pinned seed pools, independently recounts
every trace candidate over all `4^7` allocations, validates all added cuts,
and verifies the two union checkpoints and the best-eight provenance:

```sh
python repro/countcegar_real/validate_manifest.py
```

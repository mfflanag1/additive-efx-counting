# Allocated-E R2 core-compression checkpoint

**Date:** 2026-08-13

**Status:** exact bounded proof-mining result; candidate uncrossing pattern,
not a cap-free theorem

## Compression result

The repaired twelve-good R2 cell was originally excluded by 14,249
higher-order closed desired-core family clauses.  An assumption core reduced
that layer to 53 clauses.  Exact greedy deletion with two different shuffled
orders then produced the same 32-clause deletion-minimal higher-order core.
The 32 clauses split as follows:

\[
  14\text{ four-source families},\qquad
  12\text{ families on }\{q,r,s\},\qquad
  6\text{ other three-source families}.          \tag{1}
\]

Rebuilding the master with those 32 clauses and labeling all 11,635 base
assertions gives a 92-assertion minimized full core.  It contains exactly:

- 32 higher-order closed-core exclusions;
- 7 pairwise closed-core exclusions;
- 10 generalized self-core exclusions;
- 6 exclusions anchored by the mandatory selected cores;
- 37 numerical/base/response assertions.

The numerical part needs only eleven strict-positive atoms, four base
normalizations, thirteen base-EFX inequalities, the mandatory desired cores
for `r,q,s,d`, the three positive response edges `r->q`, `q->r`, `s->d`, and
the two root-wall comparisons against `A` and `Q`.

In particular, this proof core uses **no** ordinary-PI exclusion, no
rank-at-most-three formula, no response nonedge, no upper value bound, and no
`d`-tail comparison against `Q+H`.  The repaired contradiction is therefore
not an artifact of the exact five-edge relation or of an artificially tight
value box.

## Emerging pattern

The 55 PI-family clauses in the full core are a finite uncrossing network.
Its most frequent desired cores are the four mandatory/crossed packets

\[
 Q=\{j,k,q0\},\quad A=\{a0,a1\},\quad
 \{e,gr\}\text{ or }\{e,p\},\quad
 \{gq,m\}\text{ with optional }gr,l.             \tag{2}
\]

Self exclusions first force each desired packet using charity `gr` to import
another owner's base support. Pair and anchored exclusions then force the
import to cross one of the mandatory `A,Q,E` packets. The higher-order layer
closes the resulting alternating import walk. This is the bounded shadow of
the cap-free support-drainage theorem: a PI-free response family cannot stay
inside any proper source set.

The remaining analytic task is to replace the atom names in (2) by an
arbitrary alternating sequence of desired cores and prove one of two
outcomes:

1. the sequence closes, giving a closed disjoint desired-core family and
   hence generalized PI; or
2. it reaches the sacrificed owner in a way whose signed residual packets
   form an observer-safe four-edge charity extraction.

This is the proposed **alternating closure-or-transfer lemma**.  The bounded
core proves that its closure side is sufficient in the R2 atomization; it
does not yet prove the cap-free transfer side or the R3 case.

## Reproducible artifacts

- `allocated_e_form0_pi_unsat_core.json`: 53-clause SMT core.
- `allocated_e_form0_pi_greedy_minimal_core.json`: 32-clause deletion-minimal
  core.
- `allocated_e_form0_pi_greedy_minimal_core_seed1.json`: independent order,
  same 32 original indices.
- `allocated_e_form0_full_unsat_core.json`: categorized 92-assertion full
  core.
- `allocated_e_form0_full_unsat_core_analysis.json`: decoded family and
  numerical-premise inventory.
- `allocated_e_r2_core_compression_audit.json`: hash audit and different-seed
  UNSAT replay of the stable 32-family core.

The replay is exact QF_LRA under Z3 5.0.0.  Core minimization and decoding
share the bounded master implementation; independent human or formal audit
of the eventual cap-free lemma remains mandatory.

## Claim boundary

This checkpoint strengthens the bounded R2 theorem and identifies a small
proof graph. It neither proves that every cap-free packet state reduces to
these atoms, excludes R3, constructs the four-edge EFX endpoint, nor proves
the active fixed-`U` theorem.

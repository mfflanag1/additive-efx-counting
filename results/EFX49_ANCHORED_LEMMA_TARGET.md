# The Anchored \(4\times9\) Lemma Target

**Status:** conjectural analytic target. The complete formula has not been
proved UNSAT and no counterexample to the statement has been found.

## Statement

Let \(V\) be a strictly positive additive valuation matrix for four agents
and nine goods. Normalize every row to sum to one and suppose:

1. the strict favorite vector is \((0,0,1,2)\);
2. no good is a minimum-value good for all four agents; and
3. there is no peelable agent-good pair reducing the instance to the
   complete three-agent theorem.

Let \(\mathcal A_9\) contain the following unlabeled four-bundle partitions:

- **singleton-anchor branch:** good \(0\) is a singleton, goods \(0,1,2\)
  lie in distinct bundles, and no good in \(\{3,\ldots,8\}\) is a
  singleton;
- **balanced-boundary branch:** the bundle shape is \(3+2+2+2\), goods
  \(0,1,2\) lie in distinct bundles, and good \(0\) lies in a pair.

The exact census is

| branch | partitions |
|---|---:|
| singleton anchor | 473 |
| balanced boundary | 480 |
| total | 953 |

> **Candidate anchored \(4\times9\) lemma.** Some partition in
> \(\mathcal A_9\) has a perfect matching in its EFX-feasibility graph.

For a partition \(P=(B_0,\ldots,B_3)\), agent \(i\) is adjacent to bundle
\(B_b\) exactly when

\[
v_i(B_b)\ge
\max_{c\ne b}\left(v_i(B_c)-\min_{g\in B_c}v_i(g)\right).
\]

A perfect matching assigns every bundle to a distinct adjacent agent, and
is therefore exactly a complete EFX allocation. Thus the candidate lemma
would close the residual favorite-\(2+1+1\) cell at \(4\times9\).

## Why this is the right finite family

The certified \(4\times8\) favorite-\(2+1+1\) core lies in a 191-partition
anchored family with the same two geometric branches: protect shared
favorite \(0\) as a singleton, or move onto the all-pairs boundary.

At \(4\times9\), delete one of the six nonfavorite goods. The remaining
instance is \(4\times8\), where the anchored theorem applies. Reinserting
the deleted good into a bundle other than the bundle containing good \(0\)
produces exactly the two branches of \(\mathcal A_9\).

This isolates the human proof obligation:

> Among the six nonfavorite deletions, choose a \(4\times8\) anchored EFX
> base for which the deleted good can be reinserted without using the
> bundle containing shared favorite \(0\).

If every such reinsertion fails, the generalized parking criterion supplies
an explicit strict-envy witness. A concise proof should combine those six
witnesses into a threshold contradiction. This is the finite version of the
general minimal-counterexample \(f\)-envy-cycle gate.

## Exact computational evidence

Every hard rational model learned by the current cross-solver CEGAR loop has
at least one EFX-supporting partition in \(\mathcal A_9\):

| model | all EFX-supporting partitions | anchored supporting partitions |
|---|---:|---:|
| exact-count-four canonical witness | 4 | 3 |
| cvc5 model 1 | 159 | 111 |
| cvc5 model 2 | 119 | 86 |
| external model 3 | 78 | 57 |
| external model 4 | 61 | 38 |
| external model 5 | 13 | 13 |
| external model 6 | 58 | 31 |
| external model 7 | 19 | 14 |
| external model 8 | 13 | 13 |
| external model 9 | 33 | 6 |

These are exact full-universe counts, not samples. They are evidence for
problem selection only: finitely many covered models do not prove the lemma.

The complete 953-obstruction QF_LRA formula was normalized to strict SMT-LIB
and run with pinned cvc5 1.3.3. Two matching-clause runs with different
decision heuristics each reached a 900-second limit without returning `sat`
or `unsat`. Their correct status is `MASTER_UNKNOWN`.

The next exact decomposition is finite and audited. After fixing the strict
favorite pattern, there are \(8^4=4096\) possible strict second-favorite
vectors. Quotienting by the exact stabilizer of \((0,0,1,2)\)—swapping the
two shared-favorite agents, simultaneously swapping agents 2 and 3 with
goods 1 and 2, and permuting goods 3 through 8—leaves 57 orbits.

Inside a fixed top-two cell, the broad favorite-only row stabilizer must not
be used when equal-favorite agents have different second favorites. The
runners now reject that unsafe option. The sound configuration fixes one of
the 57 representatives and applies only the stabilizer preserving the full
top-two prefixes.

The first two fixed top-two calibrations, representatives \((1,2,2,1)\) and
\((1,1,2,3)\), also returned `MASTER_UNKNOWN` at 300 seconds. Thus splitting
the full 953-family formula by itself does not remove the computational
bottleneck. A solver-independent Hall-selector encoding likewise returned
`MASTER_UNKNOWN` at 900 seconds. A fourth encoding that inlined every
matching obstruction also returned `MASTER_UNKNOWN` at 900 seconds. The
learned-core CEGAR therefore remains the productive partition-search path;
the 953-family is retained as the concise human-proof target.

## Review artifacts

- Family census:
  [efx49_partition_211_anchored953_audit.json](efx49_partition_211_anchored953_audit.json)
- Frozen partition pool:
  [efx49_partition_211_anchored953_pool.json](efx49_partition_211_anchored953_pool.json)
- First external-solver record:
  [efx49_partition_211_anchored953_external_session1.json](efx49_partition_211_anchored953_external_session1.json)
- Second decision-heuristic record:
  [efx49_partition_211_anchored953_external_session2.json](efx49_partition_211_anchored953_external_session2.json)
- Standard Hall-selector record:
  [efx49_partition_211_anchored953_hall_external_session2.json](efx49_partition_211_anchored953_hall_external_session2.json)
- Inline-matching record:
  [efx49_partition_211_anchored953_inline_external_session1.json](efx49_partition_211_anchored953_inline_external_session1.json)
- Reproducible family generator:
  [`build_anchored49_pool.py`](../tracks/parkability/build_anchored49_pool.py)
- Exact top-two orbit census:
  [efx49_partition_211_second_favorite_orbits.json](efx49_partition_211_second_favorite_orbits.json)

## What success would and would not establish

An independently proof-checked UNSAT result would establish the candidate
lemma and close one canonical favorite-pattern cell of \(4\times9\).
Additional favorite multiplicity cells would still remain, and even a full
\(4\times9\) theorem would not resolve additive EFX for arbitrary numbers of
goods or agents.

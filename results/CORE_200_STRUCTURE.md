# Structural Audit of the 200-Partition `favorite-211` Core

**Snapshot:** 2026-07-30 EDT  
**Status:** exact descriptive analysis of the initial 200-partition core and
the final 130-partition deletion-minimal UNSAT core; the smaller formula has
an independently checked cvc5 CPC/Ethos proof

## What this core is

The `favorite-211` terminal cell has canonical favorite pattern

\[
(0,0,1,2).
\]

Agents 0 and 1 share favorite good 0, while agents 2 and 3 favor goods 1 and
2. The complete terminal formula obstructs all 1,701 unlabeled nonempty
partitions of eight goods into four bundles. Z3 first reduced those
obstructions to 216 partitions and then to a 200-partition assumption core.
The 200-partition formula replays UNSAT in Z3 and was also solved by cvc5.

An assumption core is sufficient for contradiction, but it need not be
minimal. Its contents can depend on assertion and solver order. The final
130-partition result is stronger: all 130 single-partition deletions are SAT,
so every survivor is individually indispensable relative to this core. This
is deletion minimality, not a claim that 130 is the smallest possible core
cardinality.

Frozen source artifacts:

- result JSON SHA-256:
  `7ee82523bf38bdfae529873cb2600f509f07e6d5e7a3d5e0147c5cb3e223506d`;
- standalone SMT-LIB SHA-256:
  `7c25dae47bec3dd8626dfb82cce4ad6cd6e18dbd302174f7d3b9f2a58f645c60`.

Final shrink artifacts:

- result JSON SHA-256:
  `df6d0e38fa7669de2f507fe81f94854c6119e8e151fe0627d153e49db0f88f41`;
- standalone SMT-LIB SHA-256:
  `1cff0b5abdd564f066c48750471ef392e72d0e3d25e7f7f005bb2c9448fa64a8`;
- structure audit SHA-256:
  `5f5bb1fc9fdc8b3e5a62abbb9a98eabd01ac3c8369e319ccdf90ac7d30dd7e41`.

Independent reduced-core certificate:

- certificate JSON SHA-256:
  `4d8df6cc15470fba59dc11dde7269d1883a923db9414ce118505e18b0f70e6da`;
- CPC proof SHA-256:
  `13aa60b6f0fbdf264c368bf7a2021f9d6d8845cae4d7eec69bb59b96b0996eca`;
- CPC proof size: 220,777,714 bytes and 2,032,963 proof-step lines;
- cvc5 solve: 314.402 seconds; and
- Ethos check: 150.521 seconds, verdict `correct`.

The certificate is
[`favorite-211.shrunk.certificate.json`](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/core-shrinking/favorite-211.shrunk.certificate.json).

## Deletion-shrinking result: 130 partitions

The resume-safe shrinker replayed the 200-partition source as UNSAT, used
coarse block sizes \(32,16,8,4,2\), and then tested individual deletions. It
performed 298 exact solver checks. The final formula replayed UNSAT in
269.835 seconds.

The shape distribution evolved as follows:

| Bundle-size shape | Initial 200 | Intermediate 176 | Final 130 |
|---|---:|---:|---:|
| \(3+2+2+1\) | 98 | 80 | 59 |
| \(2+2+2+2\) | 51 | 45 | 20 |
| \(4+2+1+1\) | 30 | 30 | 30 |
| \(3+3+1+1\) | 20 | 20 | 20 |
| \(5+1+1+1\) | 1 | 1 | 1 |
| **Total** | **200** | **176** | **130** |

All ten partitions that paired favorite goods 1 and 2 disappeared. Thus
every final partition puts the three distinct favorite goods \(0,1,2\) in
separate bundles.

The 176-partition intermediate core had an especially simple exact
description:

1. all 131 partitions in which good 0 is a singleton, favorite goods
   \(0,1,2\) are in separate bundles, and no nonfavorite good is a singleton;
2. 45 partitions of shape \(2+2+2+2\), in which good 0 is paired with a
   nonfavorite good.

The first piece is a complete combinatorial family: an independent
enumeration of all 1,701 nonempty four-bundle partitions finds exactly those
131 partitions, and all 131 occur in the core. The second piece is a
solver-selected subset of the 60 possible anchored \(2+2+2+2\) partitions;
it is not invariant under all permutations of goods \(3,\ldots,7\), so its
individual membership must not be overinterpreted.

The final core remains inside exactly the same two families, but deletion
shrinking selects 110 of the 131 singleton-0 partitions and 20 of the 60
anchored \(2+2+2+2\) partitions. Its exact description is therefore:

1. 110 partitions with good 0 singleton, favorite goods separated, and no
   nonfavorite singleton;
2. 20 anchored pair partitions of shape \(2+2+2+2\).

The single-deletion log covers all 130 survivors with SAT results. Because
the active constraint set only shrinks, each earlier SAT deletion instance
is a superset of the corresponding final deletion instance. Satisfiability
is preserved under removing constraints, proving that every final survivor
is individually indispensable. As a consequence, every one of the five
surviving shape classes is also jointly necessary relative to this core.

The executable audit is
[`analyze_shrunk_core.py`](../tracks/parkability/analyze_shrunk_core.py), and
its hash-bound snapshot is
[`favorite-211.structure.json`](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/core-shrinking/favorite-211.structure.json).

The final marginal counts are:

| Good | Size 1 | Size 2 | Size 3 | Size 4 | Size 5 |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 110 | 20 | 0 | 0 | 0 |
| 1 | 26 | 63 | 31 | 10 | 0 |
| 2 | 26 | 63 | 31 | 10 | 0 |
| 3 | 0 | 59 | 50 | 20 | 1 |
| 4 | 0 | 60 | 49 | 20 | 1 |
| 5 | 0 | 60 | 49 | 20 | 1 |
| 6 | 0 | 63 | 46 | 20 | 1 |
| 7 | 0 | 68 | 41 | 20 | 1 |

This sharpens the analytic hypothesis. The contradiction appears to contain
an **anchored contested-favorite wall**: isolate the shared favorite good 0,
keep the other two favorite representatives separate, and distribute the
nonfavorite goods without creating another singleton. Twenty pair partitions
cover the boundary where good 0 absorbs one extra good.

A promising human-proof target is consequently no longer “some anchored
partition works,” but the more precise disjunction:

> either one of 110 singleton-0 anchored partitions has a perfect EFX
> matching, or one of a small covering family of anchored pair partitions
> does.

This is an exact description of the checked core, but converting the
130-way disjunction into a short analytic argument remains open. The next
step is proof-dependency and Hall-deficiency analysis inside these two
families.

## Exact deletion witnesses: first 54 of 130

The resume-safe
[`analyze_core_deletion_witnesses.py`](../tracks/parkability/analyze_core_deletion_witnesses.py)
has extracted exact integer valuations for 54 single-partition deletions.
Each valuation was checked independently against every core partition:
exactly the removed partition supports an EFX matching among the 130. The
same valuation was then checked against all 1,701 partitions.

This sample corrects a tempting but false interpretation of deletion
minimality. The removed core partition need not be the only working
partition in the full universe. Full-universe support ranges from 1 to 11
partitions in the current sample, with mean \(3.72\); only 13 of 54 witnesses
have support count one. The core is therefore an exact covering certificate,
not a canonical classification of every EFX allocation.

The successful removed partition is also usually not supported by a unique
assignment of bundles to agents. Its perfect-matching count ranges from 1 to
12; only one of the 54 witnesses has a unique perfect matching. Thus
the useful analytic invariant is more likely a family of Hall inequalities
than one distinguished allocation.

The first 34-witness graph statistics sharpen the contested-favorite
interpretation.
In the successful removed partitions, the two agents sharing favorite good
0 have mean feasibility degrees \(3.42\) and \(3.23\), while the two agents
with distinct favorite goods have mean degrees \(2.32\) and \(2.84\).
Agents 0 and 1 are feasible for all four bundles in 19 and 12 witnesses,
compared with 1 and 6 for agents 2 and 3. A plausible human target is
therefore to let the shared-favorite agents absorb residual bundles while
the distinct-favorite agents determine the constrained matching.

Across the \(54\times129=6,966\) obstructed core graphs there are 580
distinct feasibility-graph signatures. An exact set-cover calculation over
all Hall-deficient agent masks needs ten masks to cover this sample; the
size-ten cover is unique. Thus the frequency of a few dominant primary masks
does not justify a short three-case Hall proof.

The cleaner analytic target is the invariant 191-partition family containing
the certified core: all 131 singleton-0 anchor partitions plus all 60
favorite-separated four-pair partitions. The certified 130-core implies
that some partition in this invariant family has a feasible perfect matching
under the favorite-211 terminal assumptions. The Lean module
[`Anchored211.lean`](../formal/efx48/EFX48/Anchored211.lean) defines that
statement and proves it suffices to eliminate the favorite-211 cell. A
concise human proof remains open.

The live machine-readable sample is
[`favorite-211.deletion-witnesses.json`](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/core-shrinking/favorite-211.deletion-witnesses.json).
The hash-bound Hall-pattern audit is
[`favorite-211.hall-patterns.json`](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/core-shrinking/favorite-211.hall-patterns.json).

## Exact shape distribution

| Bundle-size shape | Core count |
|---|---:|
| \(3+2+2+1\) | 98 |
| \(2+2+2+2\) | 51 |
| \(4+2+1+1\) | 30 |
| \(3+3+1+1\) | 20 |
| \(5+1+1+1\) | 1 |
| **Total** | **200** |

The single \(5+1+1+1\) partition is

\[
\{0\},\quad \{1\},\quad \{2\},\quad \{3,4,5,6,7\}.
\]

Thus every shape occurring in the complete \(4\)-bundle universe survives
the current core, but \(3+2+2+1\) and \(2+2+2+2\) supply nearly three quarters
of it.

## Favorite-good geometry

The three distinct favorite goods are \(0,1,2\). Their organization is
striking:

- in 190 of 200 partitions, goods \(0,1,2\) occur in three separate bundles;
- in the other 10, goods 1 and 2 are paired while good 0 remains separate;
- good 0 is never bundled with good 1 or good 2;
- good 0 is a singleton in 141 partitions and belongs to a pair in the other
  59;
- goods 1 and 2 are singletons only 31 and 29 times, respectively; and
- none of the five nonfavorite goods \(3,\ldots,7\) is ever a singleton.

The bundle-size distributions are:

| Good | Size 1 | Size 2 | Size 3 | Size 4 | Size 5 |
|---|---:|---:|---:|---:|---:|
| 0 | 141 | 59 | 0 | 0 | 0 |
| 1 | 31 | 119 | 40 | 10 | 0 |
| 2 | 29 | 119 | 42 | 10 | 0 |
| 3 | 0 | 112 | 67 | 20 | 1 |
| 4 | 0 | 113 | 66 | 20 | 1 |
| 5 | 0 | 113 | 66 | 20 | 1 |
| 6 | 0 | 114 | 65 | 20 | 1 |
| 7 | 0 | 111 | 68 | 20 | 1 |

The five nonfavorite goods are close to exchangeable in these marginal
counts. Goods 1 and 2 are also nearly symmetric. Good 0—the favorite shared
by two agents—is the unique distinguished object.

## Provisional structural interpretation

The core appears concentrated on the boundary of the favorite-matching
lemma. If all four agents had distinct favorite representatives, pairing
each representative with one remaining good would immediately give EFX.
The `favorite-211` cell misses that construction only because two agents
compete for good 0.

The core repeatedly tests partitions that:

1. isolate the three available favorite representatives;
2. keep the contested favorite 0 very small; and
3. distribute the five nonfavorite goods among the remaining bundle
capacity.

This suggests a possible analytic route: prove that under the two residual
exclusions, some partition of this “three favorite anchors plus distributed
remainders” form must have a perfect EFX matching. A contradiction might
then be expressible as a small collection of threshold inequalities attached
to the contested good 0, rather than as all 1,701 partition obstructions.

That statement is presently only a research hypothesis. Deletion minimality
shows that every displayed partition and shape class is necessary relative
to the final core. The first 31 deletion witnesses now identify exact
Hall-deficient agent sets and feasibility graphs, but a complete or
human-readable threshold contradiction is not yet known.

## Next tests

Completed:

- coarse-to-fine and individual deletion shrinking;
- standalone Z3 replay of the 130-partition formula;
- exact deletion-minimality audit; and
- shape-class necessity as a consequence of individual indispensability.

Remaining:

1. Complete the remaining 76 deletion witnesses.
2. Translate the failed edges in the invariant 191-partition family into
   explicit additive threshold
   inequalities and search for short positive linear combinations producing
   a Farkas contradiction.
3. Test whether the same anchor structure appears in the other seven
   terminal cells after core extraction.

The key distinction for subsequent reports is:

> **Indispensable relative to this core** is now proved by deletion tests.
> **Globally unavoidable in every proof** would require a different,
> stronger argument.

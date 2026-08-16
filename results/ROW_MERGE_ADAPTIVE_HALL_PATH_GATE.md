# Row-Merge Adaptive Hall-Path Gate

**Status:** the first adaptive Hall-neighborhood selector is exactly refuted
on the frozen generic-wall corpus  
**Scope:** four positive-additive agents, nine goods, one generic feasibility
edge crossing  
**Not claimed:** a refutation of all adaptive exchange chains, the full
515-partition chain candidate, row-merge continuation, or complete additive
EFX

## Basic idea

At the post-wall partition, the feasibility graph has no perfect matching and
bundle 0 is outside the neighborhood of the all-agent Hall blocker. Think of
bundle 0 as a hole. The tested adaptive rule does the following:

1. find an inclusion-minimal Hall-deficient set of agents whose neighborhood
   omits the current hole;
2. move one good from a non-singleton bundle in that neighborhood into the
   hole;
3. declare the source bundle to be the new hole, recompute the graph, and
   repeat.

The initial hole and all later source bundles are distinct, so at most three
transfers form a genuine simple path through the four labeled bundles. The
rule branches over every permitted Hall witness, source, and good. It succeeds
if any branch creates a perfect matching.

## Exact frozen-corpus result

The solver-free replay gathered 38 exact model occurrences from the topology
and valuation-ranked CEGAR traces. Twelve older occurrences were correctly
excluded because their wall step changed two feasibility edges. The remaining
26 generic occurrences deduplicate to 25 valuation profiles.

The adaptive Hall-hole rule succeeds on 20 of the 25 distinct generic
profiles and fails on five. Nineteen covered profiles have a two-transfer
repair; one first succeeds at three transfers. Across the covered profiles
there are 107 successful adaptive paths. The five failed profiles exhaust
19--35 reachable rule states each without finding a perfect matching.

One compact failed profile is round 5 of the three-policy ranked-path trace:

\[
V^-=
\begin{pmatrix}
2&18&20&1&3&19&7&7&3\\
1&17&20&1&10&8&5&16&3\\
9&6&20&1&10&10&1&5&13\\
9&1&20&1&4&11&8&8&13
\end{pmatrix}.
\]

The post-wall matrix changes only entry \((0,2)\), from 20 to 22. Its
feasibility graph changes only edge \((0,0)\), from present to absent. The
exhaustive adaptive replay visits 19 states; six branches reach the
three-transfer depth limit and seven stop because no permitted Hall-
neighborhood move remains. None supports a perfect matching under this rule.
The same model still has seven supporting partitions among the three-policy
ranked menu, so this is a selector failure rather than an absence of local or
global EFX repairs.

The other four exact failures occur in rounds 1 and 3 of the ladder-4 trace,
the two-orientation cycle-023 gate, and round 3 of the pool-64 trace. Their
source hashes, value hashes, state counts, and terminal histograms are frozen
in
[row_merge_q4_adaptive_hall_path_analysis.json](row_merge_q4_adaptive_hall_path_analysis.json).

## Exact boundary

This result rules out only the rule “always fill the current hole from the
current minimal Hall block's existing neighborhood” while preserving a
simple labeled-bundle path. It does not rule out:

- choosing a source outside that neighborhood;
- moving into a different missing bundle;
- allowing a cycle or a repeated bundle;
- using non-minimal Hall sets or valuation slack to anticipate the next
  blocker; or
- the existential full 515-partition exchange-chain candidate, which remains
  undecided.

The correct analytic successor would therefore need a less local invariant:
the current minimal blocker alone does not identify a safe source. This is a
finite exact negative gate, not a universal impossibility theorem.

## Reproduction

Run:

```sh
make verify-row-merge-adaptive-hall-path-gate
```

The target reconstructs the corpus from hash-bound source traces, replays all
Hall-hole branches without a solver, and compares the JSON byte for byte.

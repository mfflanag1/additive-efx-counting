# Rank-One Core/Shape Ladder Gate

**Status:** cap-5 repeated-resident menu compressed and dual-encoded; cap-6
continuation remains SAT through 196 cuts  
**Scope:** four agents, nine goods, a strict common favorite, the selected
rank-one residual state, resident rows 1 and 2 equal, and the 45-state
extended-bridge repair family  
**Not claimed:** a cap-6 theorem, a cap-free repeated-resident theorem,
coverage of pairwise-distinct residents, or general complete EFX

## Basic explanation

The existing bounded theorem used 392 favorite-singleton partitions as
obstructions. Assumption-core extraction and counterexample-guided replay now
show which parts of that menu are actually doing work.

At cap 4, only 29 favorite-singleton partitions are needed. Every one has
residual bundle sizes (3+3+2). At cap 5, the exact same 29 balanced
partitions remain as one layer, but they no longer suffice. A shared
112-partition core closes under both independent encodings:

| residual sizes beside the favorite | partitions in the cap-5 core |
|---|---:|
| (3+3+2) | 29 |
| (4+2+2) | 35 |
| (4+3+1) | 48 |
| (5+2+1) | 0 |
| (6+1+1) | 0 |

Thus the cap-5 core is not an unrelated larger certificate: its balanced
layer is literally the cap-4 core, and it adds exactly two unbalanced shape
layers.

## Exact cap-4 core

Starting from the independently verified 392-cut cap-4 Hall master, repeated
assumption-core extraction gave

\[
392\to90\to60\to39\to34\to29.
\]

The terminal 29 assumptions and the 45 bridge obstructions are infeasible,
and the terminal subset was replayed as infeasible in a fresh solve. The
hash-pinned core is
[efx49_common_favorite_rank1_extended_bridge_collision12_cap4_hall_core6.json](efx49_common_favorite_rank1_extended_bridge_collision12_cap4_hall_core6.json).
It is a sufficient core, not a deletion-minimality claim.

## Exact cap-5 compression

The 29-partition menu is not cap-free. At cap 5, the profile

\[
\begin{pmatrix}
5&2&1&1&1&1&1&4&1\\
5&1&4&1&1&1&1&3&1\\
5&1&4&1&1&1&1&3&1\\
5&1&4&1&1&1&1&3&1
\end{pmatrix}
\]

blocks the 29 partitions and all 45 bridges but has 52 other
favorite-singleton repairs: 30 of residual shape (4+2+2), 15 of shape
(4+3+1), and 7 of shape (5+2+1). This exactly refutes the proposed
cap-free 29-menu lemma.

Two counterexample-guided additions close cap 5 at 165 cuts. Assumption-core
extraction through the matching encoding then reduces that menu to 112. The
same exact 112 partitions close in the independent duplicate-Hall encoding.
The sources are:

- [112-partition matching core](efx49_common_favorite_rank1_extended_bridge_collision12_cap5_shapeaware_matching_core1.json);
- [same-menu Hall replay](efx49_common_favorite_rank1_extended_bridge_collision12_cap5_matching_core112_hall_replay.json).

Both sources are solver-level bounded certificates rather than external proof
logs. Their importance is proof compression: the same finite menu works in
two logically independent encodings, and its shape layers are explicit.

## Exact cap-6 SAT ladder

The 112-partition cap-5 core is also not cap-free. Four literal-audited cap-6
models give the following CEGAR trace:

| active cuts before solve | new singleton repairs | repair shapes | solve time |
|---:|---:|---|---:|
| 112 | 6 | (6\times(5+2+1)) | 71.91 s |
| 118 | 27 | (12\times(3+3+2),15\times(4+2+2)) | 77.18 s |
| 145 | 51 | (30\times(3+3+2),20\times(4+3+1),1\times(5+2+1)) | 87.10 s |
| 196 | 15 | (15\times(4+2+2)) | 222.66 s |

Every trace model blocks all 45 extended-bridge repairs. Every trace model
also has all three resident rows identical, even though only rows 1 and 2
were constrained equal. The first and last matrices are

\[
\begin{pmatrix}
6&5&1&1&1&1&1&4&1\\
6&5&1&1&1&1&1&4&1\\
6&5&1&1&1&1&1&4&1\\
6&5&1&1&1&1&1&4&1
\end{pmatrix},
\qquad
\begin{pmatrix}
6&1&1&1&2&2&1&4&1\\
6&4&4&4&1&1&3&1&4\\
6&4&4&4&1&1&3&1&4\\
6&4&4&4&1&1&3&1&4
\end{pmatrix}.
\]

The 15 repairs from the last solved model were added, producing a 211-cut
pool. That 211-cut master has **not** been run. The honest endpoint is
therefore “SAT through 196 cuts,” not a cap-6 theorem and not a 211-cut
stall.

The independent aggregate
[efx49_common_favorite_rank1_core_shape_ladder_audit.json](efx49_common_favorite_rank1_core_shape_ladder_audit.json)
recomputes every singleton census with both a literal matching loop and the
graph enumerator, rechecks every bridge failure, confirms the shared cap-5
menu, and validates every source and proto hash.

## What the ladder rules out

Two plausible analytic shortcuts are now exactly false.

1. **Fixed balanced menu.** The 29 balanced cap-4 partitions do not extend to
   cap 5.
2. **Bundle-size induction.** Adding one representative layer for each
   residual size does not suffice. Later cap-6 profiles escape through new
   origin placements in (3+3+2) and (4+2+2), shapes already present in
   the cap-5 core.

The missing information is therefore origin-sensitive and cardinal: which
goods came from the contested triple (A), the other triple (B), and the
pair (C), together with their rowwise values.

## Analytic target

When the three residents are identical, their rows have one common
neighborhood (S) in any favorite-singleton feasibility graph. Hall's
condition reduces to a two-case statement:

1. (|S|\ge3); and
2. if (|S|=3), the owner accepts the unique bundle outside (S).

This suggests an origin-sensitive split/merge lemma rather than another
fixed-radius rule:

> Starting from the rank-one partition (A\mid B\mid C), select the least
> resident-valued good in a rejected side bundle and follow the canonical
> split/merge chain that preserves the owner threshold. Unless a 45-state
> bridge is already EFX, the chain must either give the residents three
> feasible bundles and the owner the fourth, or strictly reduce a named
> resident gap potential.

This is a target, not a theorem. The cap-6 profiles show that bundle size
cannot be the potential: the chain must remember the (A/B/C) origin and the
resident comparison

\[
v(A)-\min A>\max\{v(B),v(C)\}.
\]

The next bounded diagnostic is the unsolved 211-cut cap-6 master. The next
mathematical task is to derive the gap potential from the eight origin
signatures in the 29-partition cap-4 core and test it against all four cap-6
trace profiles. Because repeated resident rows already lie inside the known
three-types existence theorem, any resulting lemma should ultimately be
transferred to the pairwise-distinct-resident branch rather than treated as
the final existence result.


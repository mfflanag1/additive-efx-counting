# Distinct Half-Favorite Gate

**Status:** open cap-free subcase  
**Scope:** four agents, nine goods, strict common favorite, universal owner
threshold failure  
**Closed sibling branch:** the common-three half-favorite branch  
**Not claimed:** EFX existence in this subcase or in general

## Exact reduction

Let \(f\) be the strict common favorite and, for agent \(i\), sort the
residual values as

\[
x^i_1>\cdots>x^i_8.
\]

Universal failure of the favorite-singleton owner threshold is exactly

\[
x^i_5+x^i_6+x^i_7>v_i(f)
\quad\text{and}\quad
\bigl(
x^i_3+x^i_7>v_i(f)
\ \text{or}\
x^i_4+x^i_5>v_i(f)
\bigr)
\tag{1}
\]

for every agent. The proof is
[OWNER_THRESHOLD_SHAPE_ENVELOPE.md](OWNER_THRESHOLD_SHAPE_ENVELOPE.md).
In particular every agent has at least three residual goods worth more
than half its favorite. Hall's theorem then gives either:

1. four distinct half-favorite representatives, one per agent; or
2. the same set of exactly three half-favorites for every agent.

The second case is closed by
[COMMON_THREE_LEXICOGRAPHIC_PARKING_LEMMA.md](COMMON_THREE_LEXICOGRAPHIC_PARKING_LEMMA.md).
Thus only case 1 remains in the universal-threshold subcase. Relabeling
agents and goods normalizes one saturating matching to

\[
2v_i(i+1)>v_i(f),\qquad i=0,1,2,3.
\tag{2}
\]

This normalization is cap-free.

## Two shortcuts that fail

The density in (1) does not force four disjoint pairs that can be assigned
so every owner receives value at least its favorite. A strict,
row-distinct profile witnessing this is

\[
\begin{array}{c|rrrrrrrrr}
 &f&1&2&3&4&5&6&7&8\\ \hline
0&216&115&114&113&112&111&96&95&94\\
1&216&111&115&114&113&112&94&96&95\\
2&216&112&111&115&114&113&95&94&96\\
3&216&113&112&111&115&114&96&94&95
\end{array}
\tag{3}
\]

Each row has five “high” residual goods. A pair reaches 216 only if it
contains \(f\) or two high goods: even the largest high--low pair is
\(115+96<216\). At most one disjoint pair can contain \(f\), and five high
goods support at most two disjoint high--high pairs. Hence four such pairs
are impossible. Nevertheless

\[
\{f,1\}\mid\{2,3\}\mid\{4,5\}\mid\{6,7,8\}
\]

supports EFX, and exact enumeration finds 60 balanced EFX partitions and
1,440 labeled complete EFX allocations.

A second tempting shortcut is to require a balanced partition in which
every deletion remainder is bounded by every observer's favorite, while
each bundle can be assigned to an owner who values it at least as much as
its favorite. This also fails in strict generic position:

\[
\begin{array}{c|rrrrrrrrr}
 &f&1&2&3&4&5&6&7&8\\ \hline
0&89&53&75&74&73&72&71&70&69\\
1&43&16&38&37&36&35&34&33&32\\
2&43&16&32&38&37&36&35&34&33\\
3&43&16&33&32&38&37&36&35&34
\end{array}
\tag{4}
\]

Every balanced partition contains a triple. Even the two least valuable
goods among any residual triple exceed the observer's favorite in every
row, so no triple is globally favorite-bounded. Yet the same displayed
partition supports EFX; exact enumeration finds 240 balanced EFX
partitions and 2,537 labeled complete EFX allocations.

The executable audit
[efx49_distinct_half_normal_form_boundaries_audit.json](efx49_distinct_half_normal_form_boundaries_audit.json)
checks strictness, row distinctness, (1), all 966 literal residual
threshold obstructions per owner, both zero-target censuses, and complete
EFX enumeration.

These boundaries show that the missing proof must use agent-relative EFX
comparisons and assignment exchanges. A universal favorite floor is too
coarse.

## Triple-aware owner-floor closure

The four-pair shortcut fails because a triple is sometimes needed from the
outset. The following weaker starting statement is now analytically proved:

> **Favorite-pair owner-floor lemma.** Under (1) and (2), there are a good
> \(p\ne f\), a partition of the other seven goods into bundles of sizes
> \(3,2,2\), and an assignment of
> \[
> \{f,p\},\quad T,\quad P,\quad Q
> \]
> to the four agents such that every owner \(i\) receives a bundle \(B_i\)
> with \(v_i(B_i)\ge v_i(f)\).

The cap-free proof is
[DISTINCT_HALF_DENSITY_FLOOR_LEMMA.md](DISTINCT_HALF_DENSITY_FLOOR_LEMMA.md).
It in fact needs only \(x_5+x_6+x_7>F\), at least three half-favorites per
agent, and the saturating half-favorite matching. It reduces the construction
to a classified family of four three-element sets and explicitly chooses the
favorite partner, the two floor pairs, and the triple.

There are 840 unlabeled partitions of this form. Matching-clause and
Hall-obstruction QF_LRA encodings independently return UNSAT; the frozen
audit is
[efx49_distinct_half_floor_dual_encoding_audit.json](efx49_distinct_half_floor_dual_encoding_audit.json).
They are now independent checks of the analytic theorem rather than its
primary trust boundary.

Z3's minimized assumption core reduces the 840 matching obstructions to 22
favorite-pair partitions:
[efx49_distinct_half_floor_minimized_core.json](efx49_distinct_half_floor_minimized_core.json).
The core is retained as a historical proof-mining artifact, not an
independently checked minimal certificate. The analytic proof supersedes
the need to convert it into a Hall/Farkas certificate.

This owner-floor state is exactly the triple-aware normal form missing from
the four-pair construction. Every EFX comparison against a pair is
automatically safe, because deleting one good leaves an item worth at most
the observer's favorite. Only comparisons against the triple can fail.

## Surviving EFX target

The favorite-pair balanced lemma is false. The strict profile

\[
\begin{pmatrix}
100&1&2&55&69&59&96&77&95\\
100&5&17&73&69&62&55&68&53\\
100&8&1&48&73&69&61&67&65\\
100&8&1&55&79&90&71&66&82
\end{pmatrix}
\]

satisfies (1) and the distinct-representatives alternative, but no one of
the 840 favorite-pair balanced partitions has a perfect EFX-feasibility
matching. The same profile has 324 complete EFX allocations, all using the
favorite triple \(\{f,1,2\}\). The literal census is
[efx49_distinct_half_favorite_pair_rank_boundary_audit.json](efx49_distinct_half_favorite_pair_rank_boundary_audit.json).

The favorite-triple-only target is false in the opposite direction. A
second strict, item-distinct branch profile has zero EFX-supporting states
among all 420 favorite-triple partitions, but 356 favorite-pair EFX
partitions and 1,906 complete EFX allocations. See
[efx49_distinct_half_favorite_triple_boundary_audit.json](efx49_distinct_half_favorite_triple_boundary_audit.json).
Hence both alternatives below are necessary.

The replacement target must therefore contain two alternatives:

> **Favorite-pair/favorite-triple Hall dichotomy.** Under (1) and the
> distinct-representatives alternative (2), either some favorite-pair
> balanced partition supports an EFX matching, or there are two goods
> \(a,b\) such that the remaining six goods can be partitioned into three
> pairs \(P_1,P_2,P_3\) that can be matched to three distinct agents using
> edges
> \[
> v_i(P_j)\ge F_i+\max\{v_i(a),v_i(b)\}.
> \]

The second alternative is exactly EFX by the cap-free
[favorite-triple Hall characterization](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md).
The remaining work is the dichotomy itself—convert the simultaneous Hall
obstruction to all 840 favorite-pair partitions into an edge-labeled
three-pair matching avoiding the three possible Hall witnesses.

The stronger observer-independent condition in
[COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md](COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md)
remains a useful sufficient special case.

The cap-free
[ONE_DEFECT_FAVORITE_TRIPLE_CONVERSION_LEMMA.md](ONE_DEFECT_FAVORITE_TRIPLE_CONVERSION_LEMMA.md)
sharpens that conversion when one wants to move the favorite back into a
pair. For existence, two universally safe pairs plus one pair with at most
one rejecter already satisfy the favorite-triple Hall criterion, with no
comparison condition.

Examples (3) and (4) show why this argument must remain agent-relative:
neither a universal pair floor nor a globally safe triple is available.
The host also cannot be frozen throughout the maximization. A strict
row-distinct profile has a non-EFX fixed-host lexicographic maximum even
though it has 369 favorite-pair balanced EFX partitions. Its exact audit is
[efx49_distinct_half_fixed_host_lex_boundary_audit.json](efx49_distinct_half_fixed_host_lex_boundary_audit.json).
Thus any proof of the first alternative must allow ownership of the triple
to move along the alternating path; if that process cannot terminate with a
favorite-pair EFX state, its obstruction must instead identify the two
  goods parked with the favorite in the second alternative.

The analytic floor construction itself also cannot simply be strengthened
to EFX. A strict generic branch-valid profile has 728 allocations of the
proof's bottom-aware/high--high-pair form and none is EFX, while the profile
still has 306 favorite-pair balanced EFX partitions and 1,364 labeled
complete EFX allocations. The exact audit is
[efx49_distinct_half_structured_floor_boundary_audit.json](efx49_distinct_half_structured_floor_boundary_audit.json).
Consequently the final argument must leave the initial construction family,
not merely optimize within it. The former rank-plateau formalization of
that escape is also false; its exact boundary and the common-low repair are
documented in
[DISTINCT_HALF_RANK_AUGMENTATION_GATE.md](DISTINCT_HALF_RANK_AUGMENTATION_GATE.md).

The replacement conversion problem is frozen in
[DISTINCT_HALF_CONVERSION_DICHOTOMY_GATE.md](DISTINCT_HALF_CONVERSION_DICHOTOMY_GATE.md).
A diversified 24-favorite-pair/9-repair exact master remains `unknown` after
300 seconds. Independently, exact-census search reached a profile with no
favorite-pair EFX partition, exactly one common-low repair, and 252 complete
EFX allocations. This is a one-repair positive boundary, not a theorem or a
counterexample. It sharpens the sufficient proof target to forcing at least
one repair from the simultaneous favorite-pair Hall obstructions; the
agent-relative favorite-triple Hall condition remains the weaker exact
fallback.

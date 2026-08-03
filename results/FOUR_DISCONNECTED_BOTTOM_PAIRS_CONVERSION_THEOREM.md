# Four Disconnected Bottom Pairs Conversion Theorem

**Status:** cap-free, proof-checked computer-assisted theorem  
**Scope:** four additive agents, nine goods, a strict common favorite, and
universal owner-threshold failure  
**Not claimed:** the other ten all-distinct bottom-pair patterns, the full
four-agent/nine-good case, or general additive EFX

## Statement

Let four agents have positive additive valuations over nine goods. Suppose
all four strictly prefer one singleton good $f$ to every other singleton,
and suppose the universal owner-threshold-failure condition used in the
common-favorite reduction holds. Suppose the eight residual goods can be
partitioned into four disjoint pairs

\[
L_1,L_2,L_3,L_4,
\]

such that $L_i$ is a bottom-two pair for agent $i$.

Then at least one of the following holds:

1. a selected favorite-triple Hall cell is full; or
2. a favorite-pair conversion generated from one of $L_1,\ldots,L_4$
   supports a complete EFX allocation.

Consequently this selected-bottom-pair geometry cannot occur in the
residual branch with no favorite-pair EFX allocation and no selected full
Hall cell.

## Basic explanation

For a selected low pair $L_i=\{h,\ell\}$, pair the other six residual
goods in every possible way. Each failed favorite-triple pairing supplies
six natural conversions: pair $f$ with one low good and add the other low
good to one of the three paired edges. Taking this menu over all four
selected pairs yields 360 distinct balanced partitions.

The exact linear-arithmetic formula asks for a valuation profile satisfying
the branch assumptions while obstructing every one of those 360
partitions. It is inconsistent. Therefore either one of the selected Hall
cells was already full or at least one conversion succeeds.

This is the maximally disconnected member of the eleven all-distinct
patterns: every residual good lies in exactly one selected pair. It is the
first proof-checked theorem in the all-distinct census.

## Certification

The selected-pair geometry has a 384-action relabeling group and the 360
conversions split into four exact orbits of sizes 24, 48, 96, and 192. The
full formula returned `unsat` under:

- Z3 with the cardinal threshold encoding;
- a separate Z3 sorting-network encoding;
- a fresh Z3 5.0 process replaying the frozen sorting formula; and
- pinned cvc5 1.3.3 on a syntax-only normalized QF_LRA formula.

cvc5 emitted a 27,789,102-byte CPC proof with 339,968 proof-step lines.
Ethos 0.2.3 checked the derivation and returned `correct`.

The hash-pinned aggregate record is
[efx49_bottom_pattern19_conversion_audit.json](efx49_bottom_pattern19_conversion_audit.json).
The independent structural records are the
[symmetry audit](efx49_four_disconnected_edges_pattern_symmetry_audit.json)
and
[conversion-orbit audit](efx49_bottom_pattern19_conversion_orbit_audit.json).
The checked proof is
[efx49_bottom_pattern19_conversion_selector_symmetric_sorting.cpc](efx49_bottom_pattern19_conversion_selector_symmetric_sorting.cpc).

## Six-conversion canonical core

Proof mining compresses the 360 conversions to six. After the same
384-action canonicalization, label the selected bottom pairs

\[
\{1,2\},\quad\{3,4\},\quad\{5,6\},\quad\{7,8\}.
\]

It is sufficient to retain only

\[
\begin{aligned}
&\{f,7\}\mid\{1,4\}\mid\{2,6,8\}\mid\{3,5\},\\
&\{f,7\}\mid\{1,4,8\}\mid\{2,6\}\mid\{3,5\},\\
&\{f,7\}\mid\{1,6\}\mid\{2,4,8\}\mid\{3,5\},\\
&\{f,8\}\mid\{1,4,7\}\mid\{2,6\}\mid\{3,5\},\\
&\{f,8\}\mid\{1,6\}\mid\{2,4,7\}\mid\{3,5\},\\
&\{f,8\}\mid\{1,6,7\}\mid\{2,4\}\mid\{3,5\}.
\end{aligned}
\]

All six lie in the largest conversion orbit. They use the two residual
perfect matchings

\[
\{\{1,4\},\{2,6\},\{3,5\}\},\qquad
\{\{1,6\},\{2,4\},\{3,5\}\},
\]

which share the edge $\{3,5\}$, and split evenly between favorite partners
7 and 8. Both ordinary and minimized Z3 assumption extraction return this
same six-partition core, and the unguarded compact formula replays `unsat`.
Pinned cvc5 independently returns `unsat` on the 355 KB normalized formula;
its 8,863,864-byte, 112,158-step CPC proof is accepted as `correct` by
Ethos.

The core is deletion-minimal. Six separate exact solves remove one
partition at a time; every five-partition remainder is satisfiable, and in
each resulting profile the omitted partition itself supports EFX. Thus all
six listed conversions are necessary for this particular canonical core,
although other six-case cores may exist.

The canonicalization is essential to this particular concise statement.
Deleting the symmetry cuts makes the fixed six-partition formula
satisfiable; the exact positive boundary is recorded in
[efx49_bottom_pattern19_conversion_selector_sorting_core1_without_symmetry.json](efx49_bottom_pattern19_conversion_selector_sorting_core1_without_symmetry.json).
Thus the human target is a WLOG canonical six-conversion argument, not a
claim that these six labeled partitions work before relabeling.

The core, orbit classification, and checked compact proof are
[efx49_bottom_pattern19_conversion_selector_sorting_core2_minimized.json](efx49_bottom_pattern19_conversion_selector_sorting_core2_minimized.json),
[efx49_bottom_pattern19_conversion_selector_sorting_core1_analysis.json](efx49_bottom_pattern19_conversion_selector_sorting_core1_analysis.json),
and
[efx49_bottom_pattern19_conversion_selector_sorting_core1_cpc_ethos.json](efx49_bottom_pattern19_conversion_selector_sorting_core1_cpc_ethos.json).
The deletion audit is
[efx49_bottom_pattern19_conversion_selector_sorting_core2_minimality_audit.json](efx49_bottom_pattern19_conversion_selector_sorting_core2_minimality_audit.json).
All compact-core gates are collected and hash-pinned in
[efx49_bottom_pattern19_six_conversion_core_audit.json](efx49_bottom_pattern19_six_conversion_core_audit.json).

## Remaining boundary

Nine all-distinct selected-bottom-pair patterns remain after the separate
four-cycle theorem. Closing them would
finish the strict-common-favorite/universal-threshold conversion gate at
$(4,9)$, but it would still leave the mixed-threshold branch and the broader
general additive-EFX problem open.

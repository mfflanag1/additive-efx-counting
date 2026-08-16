# Strict-Common-Favorite Universal-Threshold EFX Theorem

**Status:** cap-free, proof-checked computer-assisted theorem  
**Scope:** four agents, nine goods, positive additive valuations, a strict
common favorite, and universal owner-threshold failure  
**Not claimed:** the threshold-passing/Hall-deficient branch, the full
four-agent/nine-good cell, or general additive EFX

## Statement

Let four agents have positive additive valuations over nine indivisible
goods. Suppose one good $f$ is a strict singleton favorite of every agent.
For each agent $i$, sort the other eight singleton values as

\[
x_{i1}\ge x_{i2}\ge\cdots\ge x_{i8},\qquad F_i=v_i(f).
\]

Assume every row satisfies

\[
x_{i5}+x_{i6}+x_{i7}>F_i,
\qquad
x_{i3}+x_{i7}>F_i\ \text{or}\ x_{i4}+x_{i5}>F_i. \tag{1}
\]

Then the instance admits a complete EFX allocation.

The same conclusion extends by closure to nonnegative valuations when $f$
is only a weak common favorite, provided the two inequalities in (1) remain
strict. Add $\varepsilon$ to every residual singleton and $2\varepsilon$ to
$f$. The perturbed profile is positive and has a strict common favorite;
the first inequality gains $\varepsilon$ of slack and the second keeps its
original slack. Apply the positive theorem along a sequence
$\varepsilon\downarrow0$. There are finitely many allocations, so one occurs
on an infinite subsequence, and its weak EFX inequalities survive in the
limit.

By the owner-threshold shape envelope, (1) says exactly that no agent can
own the singleton $f$ while the other eight goods are split into three
bundles that pass that owner's scalar EFX threshold. The theorem therefore
closes the entire universal owner-threshold-failure branch, not merely the
earlier distinct-half-representative subbranch.

## Basic explanation

Choose two least-valued residual goods for each agent. Regard the four
chosen pairs as edges of a multigraph on the eight residual goods.

If one pair is bottom-two for at least three agents, the proof-checked
three-agent-bottom conversion theorem already constructs EFX. Otherwise no
chosen edge occurs more than twice. There are then only 20 graph shapes up
to relabeling: two with multiplicities $2+2$, seven with multiplicities
$2+1+1$, and eleven with four distinct edges.

For a selected low pair $\{a,b\}$, split the other six residual goods into
three pairs. Either the favorite-triple partition

\[
\{f,a,b\}\mid P\mid Q\mid R
\]

passes the exact Hall matching test, or move one of $a,b$ into one of
$P,Q,R$ and pair the other low good with $f$. These are the favorite-pair
conversions. The finite proof checks show that in each of the 20 graph
shapes it is impossible for every selected favorite-triple cell to have a
Hall failure while every conversion is EFX-infeasible. Hence some complete
EFX allocation exists.

## Proof architecture

For each agent choose an arbitrary bottom-two pair among the eight residual
goods.

1. If any residual pair is bottom-two for at least three agents, apply the
   [three-agent-bottom pairing conversion theorem](THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md).
   It gives either a Hall-valid favorite-triple partition or a complete EFX
   conversion.
2. Otherwise every chosen pair has multiplicity at most two. The exhaustive
   [bottom-pair census](efx49_bottom_pair_pattern_census_audit.json)
   canonicalizes all 30,681 labeled four-edge multisets to exactly 20
   patterns.
3. The two $2+2$ patterns are closed by the
   [overlapping](OVERLAP_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md) and
   [disjoint](DISJOINT_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md)
   double-bottom theorems.
4. All seven $2+1+1$ patterns are closed by the
   [repeated bottom-pair exclusion theorem](REPEATED_BOTTOM_PAIR_EXCLUSION_THEOREM.md).
5. The eleven $1+1+1+1$ formulas cover canonical indices 9 through 19.
   Each formula contains exactly the premises above, the relevant
   bottom-order inequalities, theorem-preserving relabeling cuts, one Hall
   failure in every selected low-pair cell, and obstructions to the complete
   conversion family. Both exact-real Z3 encodings and pinned cvc5 return
   `unsat` in all eleven cases. Pinned cvc5 emitted a CPC derivation for
   every case, and Ethos accepted every proof as `correct`.

The cases in steps 3--5 exhaust the multiplicity-at-most-two branch. The
Hall characterization turns any surviving full cell into complete EFX, and
any surviving conversion is already a complete EFX-supporting partition.
This proves the stated implication.

## Certification record

The eleven all-distinct cases are collected in
[efx49_all_distinct_bottom_pair_conversions_audit.json](efx49_all_distinct_bottom_pair_conversions_audit.json).
Their checked CPC files total 383,418,002 bytes and 4,603,008 proof-step
lines. The complete case split, including the three-agent-bottom theorem,
both $2+2$ patterns, and all seven $2+1+1$ patterns, is hash-pinned in
[efx49_common_favorite_universal_threshold_efx_audit.json](efx49_common_favorite_universal_threshold_efx_audit.json).
Across the component proofs used by that aggregate, Ethos checked
723,786,758 proof bytes and 8,552,082 proof-step lines.

The computer-assisted argument is finite and cap-free over positive real
valuations, but it is conditional on (1) and the strict common favorite.
It does not address instances where some favorite-singleton owner passes
the scalar threshold but the residual three-agent allocation fails its Hall
matching test. That mixed threshold/Hall branch is the next common-favorite
gate. Two exact balanced-only boundaries and the refutation of a fixed
one-transfer repair rule are recorded in
[MIXED_THRESHOLD_HALL_GATE.md](MIXED_THRESHOLD_HALL_GATE.md).

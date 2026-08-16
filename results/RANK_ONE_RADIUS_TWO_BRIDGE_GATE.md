# Rank-One Radius-Two Bridge Gate

**Status:** the 21-state contested-partner and 30-state bridge lemmas are
exactly refuted; the 45-state successor closes for identical residents at
cap 6 and for any repeated resident row at cap 5, but remains open generally  
**Scope:** four additive agents, nine goods, a strict common favorite, and a
threshold-safe rank-one residual state  
**Not claimed:** an EFX counterexample, closure of the common-favorite cell,
or general additive EFX

**Prior-work calibration:** for four agents, any repeated valuation row means
there are at most three valuation types. Complete EFX existence for that
larger class is already known from Ghosal, Prakash, Nimbhorkar, and Varma,
*EFX Exists for Three Types of Agents* (EC 2025,
[doi:10.1145/3736252.3742509](https://doi.org/10.1145/3736252.3742509)).
The bounded repeated-resident results below are therefore local proof-mining
statements about the 45-repair family, not new existence theorems.

## Exact refutation

Let (f=0), (A=\{1,2,3\}), (B=\{4,5,6\}), and (C=\{7,8\}). The
positive cap-6 profile

\[
\begin{pmatrix}
6&3&3&3&2&2&1&5&4\\
5&4&3&3&1&1&2&3&3\\
5&3&4&4&2&1&1&3&3\\
5&3&4&4&2&1&1&3&3
\end{pmatrix}
\tag{1}
\]

has the following independently replayed properties.

1. (f) is the strict favorite of every agent.
2. Agent 0 passes the singleton-owner threshold on (A\mid B\mid C).
3. In the resident graph, agents 1, 2, and 3 accept only (A), so its matrix
   is exactly
   \[
   \begin{pmatrix}1&0&0\\1&0&0\\1&0&0\end{pmatrix}.
   \]
4. None of the 966 residual partitions supports EFX with (f) as a
   singleton.
5. All 21 contested-partner repairs fail. These comprise the three direct
   states
   \[
   \{f,a\}\mid A-a\mid B\mid C,
   \]
   the nine AAB states
   \[
   \{f,a\}\mid ((A-a)+x)\mid(B-x)\mid C,
   \]
   and the nine BCC states
   \[
   \{f,a\}\mid(A-a)\mid(B-x)\mid(C+x),
   \]
   for (a\in A) and (x\in B). Every one of the 21 failures has exactly
   one bundle with no feasible agent neighbor.

Thus the proposed implication “favorite-singleton EFX or a contested-partner
repair” is false, even under the strongest local zero-neighbor form of Hall
failure.

This is not an EFX counterexample. Literal enumeration finds 285 supporting
unlabeled partitions, all of shape (3+2+2+2), and 3,168 labeled complete
EFX allocations.

## The missing bridge orbit

Exactly nine of the 63 balanced partitions within transfer distance two are
EFX-supporting. They form one complete origin orbit:

\[
\boxed{\{f,x\}\mid(A-a)\mid((B-x)+a)\mid C}
\qquad(a\in A,\ x\in B). \tag{2}
\]

In words, pair the favorite with a good from the *other* triple (B), then
move a good of the contested triple (A) into the depleted (B)-bundle.
For profile (1), the feasibility graph of every partition in (2) is the
complete (4\times4) graph. These are the only distance-two repairs.

The earlier cap-20 boundary profile had repairs in both contested-partner
nine-orbits and in this same bridge orbit. The union of the 21 contested
states and the nine bridge states is therefore the smallest currently
surviving origin-invariant family across both adversarial profiles.

## Exact decision boundary

A symmetry-reduced cap-6 CP-SAT master blocked all 30 states and imported
313 independently reconstructed singleton obstructions from the refutation
CEGAR trace. It returned `UNKNOWN` after 60 seconds before producing a model.
This does not prove or refute the 30-state implication.

## Superseded target-zero checkpoint

A subsequent exact local search found a cap-6 profile that blocks all 30
contested-or-bridge states. This shows that the 30-state family is not an
unconditional repair rule; the no-singleton alternative must do real work.
The profile still has exactly 30 favorite-singleton supporting partitions,
split evenly between residual shapes (3+3+2) and (4+2+2). Exact
coordinate descent reduced this count along

\[
59,51,42,39,36,33,30
\]

while preserving all 30 exchange obstructions.

Its only six EFX-supporting balanced radius-two states occupy a fourth orbit,
`partnerC_tripleBBB_pairsAA_AC`. Across all partitions it has 213 supporting
partitions and 1,414 labeled complete EFX allocations. The independently
replayed checkpoint is
[efx49_common_favorite_rank1_bridge_checkpoint_audit.json](efx49_common_favorite_rank1_bridge_checkpoint_audit.json).
It was not a refutation of the singleton-or-exchange lemma. The next section
records the later zero-singleton refutation that supersedes it.

## Exact refutation of the 30-state bridge lemma

Exact obstruction-pool optimization subsequently reached the positive cap-6
profile

\[
\begin{pmatrix}
6&1&1&1&3&3&3&4&1\\
5&4&4&4&2&2&2&1&3\\
5&4&4&4&2&2&2&1&3\\
5&4&4&4&2&2&2&1&3
\end{pmatrix}.
\tag{3}
\]

Literal replay, independent of the optimizing master, verifies all of the
following.

1. Item (f) is the strict favorite of all four agents, agent 0 passes the
   selected threshold test, and the three resident rows of the residual graph
   are exactly ((1,0,0)).
2. None of the 966 favorite-singleton partitions supports EFX.
3. None of the 30 contested-or-bridge partitions supports EFX.
4. The profile is not a complete-EFX counterexample: 264 unlabeled
   partitions support EFX, all of shape (3+2+2+2), yielding 2,790 labeled
   complete EFX allocations.

The Hall failures have an unusually clean two-row form because the three
resident valuation rows are identical. Among the 966 singleton candidates,
927 fail because the three residents collectively see at most two bundles;
the remaining 39 fail because all four agents are confined to three bundles.
Among the 30 local repairs the same split is 9 and 21. There are no residual
failure types outside these two Hall certificates. Quotienting the residual
goods by their four valuation types compresses the 966 labeled-item
partitions to 120 bundle-type classes: 116 use the first Hall witness and
only four use the second. This is the current route to a short human-checkable
refutation table.

The CP-SAT CEGAR trace grew from 30 to 218 singleton indicators and ended at
an optimal fixed point with zero singleton support. The independently replayed
record is
[efx49_common_favorite_rank1_bridge_refutation_audit.json](efx49_common_favorite_rank1_bridge_refutation_audit.json),
with the hash-pinned optimization source and exported proto stored beside it.
The zero witness itself, rather than the optimizer's optimality claim, is
already sufficient to refute the local implication.

## The surviving 45-state family

Profile (3) has exactly 15 supporting distance-two partitions. They occupy
two origin orbits:

- six states in `partnerC_tripleBBB_pairsAA_AC`; and
- nine states in `partnerB_tripleACC_pairsAA_BB`.

Adding these to the refuted 30-state family gives a 45-state union that covers
the nearest repairs of every adversarial profile audited so far. A first
cap-6 exact campaign found profiles blocking all 45 states and reduced the
favorite-singleton alternative to six partitions. That six-support profile
is an exact Hamming-two local minimum, but no positive global floor or zero
witness is yet certified. Its matrix is

\[
\begin{pmatrix}
6&3&3&3&3&1&1&4&1\\
6&5&5&5&3&1&1&1&4\\
6&5&5&5&3&1&1&1&4\\
6&5&5&5&3&1&1&1&4
\end{pmatrix}.
\tag{4}
\]

The frozen source is
[efx49_common_favorite_rank1_extended_bridge_checkpoint_profile.json](efx49_common_favorite_rank1_extended_bridge_checkpoint_profile.json).

Independent replay finds that all six singleton repairs have residual shape
(4+2+2). No partition in the entire 63-state balanced radius-two
neighborhood supports EFX. Across all shapes, however, the profile has 192
supporting partitions and 2,196 labeled complete EFX allocations, so it is
not a counterexample to complete EFX. Its exact one- and two-coordinate
neighborhoods contain 15,930 cap-6 mutations; 1,866 of the two-coordinate
neighbors still block all 45 repairs, but none improves the singleton count.
See
[efx49_common_favorite_rank1_extended_bridge_checkpoint_audit.json](efx49_common_favorite_rank1_extended_bridge_checkpoint_audit.json)
and
[efx49_common_favorite_rank1_extended_bridge_checkpoint_local_audit.json](efx49_common_favorite_rank1_extended_bridge_checkpoint_local_audit.json).

## Identical-resident bounded theorem candidate

Every current extremal profile has three identical resident valuation rows.
In that subcell, the 45-state implication closes at cap 6. A self-contained
pool of 392 of the 966 singleton partitions, together with the 45 repairs,
is infeasible under both the matching-clause and Hall-selector encodings.
The matching master closes in 38.81 seconds and the Hall master in 62.13
seconds. The six-support profile (4) proves nonvacuity and gives the current
upper bound.

Thus the dual-encoded bounded theorem candidate is:

> For positive integer values at most 6, in the selected rank-one cell with
> three identical resident rows, either a favorite-singleton partition or
> one of the 45 extended-bridge partitions supports EFX.

The hash-pinned aggregate is
[efx49_common_favorite_rank1_extended_bridge_identical_audit.json](efx49_common_favorite_rank1_extended_bridge_identical_audit.json).
This is not yet externally proof-logged, does not cover unequal residents,
and does not extend above cap 6. The unequal-resident 392-cut decision master
remains `UNKNOWN` after 900 seconds, 164,587 conflicts, and 736,252 branches.

## Repeated-resident cap-5 extension

The identical-row premise can be weakened at cap 5. Under the existing
lexicographic resident symmetry, any repeated resident row lies in one of
two adjacent cases: rows 1=2 or rows 2=3. Both cases are infeasible with the
same 392 singleton obstructions and 45 repairs under two quotient encodings.
The first retains the 12 distinct matchings left after swapping the duplicate
agents. The second reduces Hall failure to seven weighted observer subsets,
49 selectors per partition. Exhaustive replay over all 4,096 possible
three-row neighborhood graphs verifies that this compressed Hall test is
equivalent to failure of a four-agent perfect matching.

Thus the new dual-encoded bounded theorem candidate is:

> For positive integer values at most 5, in the selected rank-one cell with
> at least two identical resident valuation rows, either a favorite-singleton
> partition or one of the 45 extended-bridge partitions supports EFX.

All four cap-5 masters close in 123.78--160.76 seconds. A cap-4 profile, hence
also a cap-5 profile, lies in the cell, blocks all 45 repairs, and has 225
singleton supports, proving nonvacuity. See
[efx49_common_favorite_rank1_extended_bridge_collision_cap5_audit.json](efx49_common_favorite_rank1_extended_bridge_collision_cap5_audit.json).
The separately retained cap-4 rung closes in 27.44--36.67 seconds.
At cap 6, however, both adjacent cases remain `UNKNOWN` after 600 seconds in
the quotient-matching encoding and 900 seconds in the quotient-Hall encoding.
A subsequent sound ladder split required at least one value equal to 6, since
the cap-5 subcell is already closed; both adjacent cases again returned
`UNKNOWN` after 600 seconds. Pairwise-distinct residents and the general
unequal-resident local lemma remain open. Because the repeated-row existence
case is already covered by the three-types theorem above, further compute is
lower priority than the genuinely four-type rank-one branch and the cap-free
row-merge continuation gate. The attempted rank-two selection shortcut is
now exactly false even with four pairwise nonproportional rows.

Subsequent core extraction sharpens the row-1=row-2 case without changing
that boundary. At cap 4, 29 favorite-singleton obstructions suffice, all of
residual shape (3+3+2). At cap 5, the same 29 partitions form the balanced
layer of a 112-partition core; the other 83 partitions have shapes
(4+2+2) and (4+3+1). The exact same 112-partition menu is infeasible
under the duplicate-matching and duplicate-Hall encodings. It is not
cap-free: four cap-6 masters remain SAT through 196 active cuts and generate
a current 211-cut pool whose master has not been run. See
[RANK_ONE_CORE_SHAPE_LADDER_GATE.md](RANK_ONE_CORE_SHAPE_LADDER_GATE.md) and
[efx49_common_favorite_rank1_core_shape_ladder_audit.json](efx49_common_favorite_rank1_core_shape_ladder_audit.json).

The refutation itself closed through five exact CEGAR models. The first
session found (290,13,6) new singleton supports; the resumed session found
(4,0). The terminal profile was then replayed without trusting the solver's
reported census: all 966 singleton partitions, all 21 contested states, all
63 radius-two states, all 7,770 unlabeled four-bundle partitions, and all
(4^9) labeled allocations were independently enumerated. Every supporting
partition also received a literal EFX matching replay.

The hash-pinned record is
[efx49_common_favorite_rank1_contested_refutation_audit.json](efx49_common_favorite_rank1_contested_refutation_audit.json),
generated by
[audit_common_favorite_rank1_contested_refutation.py](../tracks/parkability/audit_common_favorite_rank1_contested_refutation.py).

## Basic meaning and next lemma

The failed 21-state rule always kept the favorite partner inside the
contested bundle (A). Profile (1) shows that this role restriction is the
mistake: every such move can be killed by an empty bundle while all nearest
repairs switch the favorite partner to (B) and send one (A)-good back in
the opposite direction.

The next analytic target is therefore the **extended rank-one bridge lemma**:

> If a threshold-safe (3+3+2) residual state has resident graph rank one,
> then either some favorite-singleton partition supports EFX or one of the
> 45 extended-bridge radius-two partitions supports EFX.

The 30-state version of this implication is false by profile (3); the
45-state version is proved only in the bounded identical-resident subcell and
remains conjectural in general. Even a full proof would close
only the rank-one subcase of the mixed common-favorite branch; rank two, the
other favorite-multiplicity cells, and general additive EFX would remain.

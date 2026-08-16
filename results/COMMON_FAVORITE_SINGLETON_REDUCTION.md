# Favorite-Singleton Reduction

**Status:** exact analytic reduction  
**Scope:** arbitrary nonnegative additive valuations and any number of goods  
**Not claimed:** that the threshold condition always holds

## Lemma

Let \(N\) be a set of agents, \(M\) a set of goods, \(a\in N\), and
\(f\in M\). Let \(Y=(Y_j)_{j\in N\setminus\{a\}}\) be an allocation of
\(M\setminus\{f\}\) among the other agents. Define the complete allocation
\(X\) by

\[
X_a=\{f\},\qquad X_j=Y_j\quad(j\ne a).
\]

Then \(X\) is EFX if and only if:

1. \(Y\) is EFX among \(N\setminus\{a\}\); and
2. for every \(j\ne a\),

\[
v_a(f)\ge
v_a(Y_j)-\min_{g\in Y_j}v_a(g),
\]

with the right-hand side interpreted as \(0\) when \(Y_j=\varnothing\).

Equivalently, if

\[
\tau_a(Y)=
\max_{j\ne a}
\left(v_a(Y_j)-\min_{g\in Y_j}v_a(g)\right),
\]

then the singleton completion is EFX exactly when \(Y\) is EFX for the
remaining agents and \(v_a(f)\ge\tau_a(Y)\).

## Proof

Comparisons between two agents other than \(a\) are exactly the EFX
comparisons in \(Y\), giving condition 1.

For any \(i\ne a\), the only removed-good comparison against
\(X_a=\{f\}\) removes \(f\) and leaves the empty bundle. Nonnegativity gives
\(v_i(Y_i)\ge0\), so these comparisons always hold.

The remaining comparisons are from \(a\) to some \(Y_j\). Additivity makes
the strongest one

\[
v_a(Y_j)-\min_{g\in Y_j}v_a(g),
\]

which yields condition 2. These exhaust all ordered agent pairs. \(\square\)

## Three-agent corollary for four agents

For four agents, remove \(a\) and \(f\). Complete EFX exists for the three
remaining additive agents. Therefore a complete four-agent EFX allocation
with \(f\) isolated exists whenever at least one three-agent EFX allocation
\(Y\) of \(M\setminus\{f\}\) satisfies

\[
\tau_a(Y)\le v_a(f).
\]

The unresolved content is no longer three-agent existence. It is the
selection problem:

> Given a common favorite \(f\), can one choose its singleton owner \(a\)
> and a three-agent EFX allocation of the remaining goods whose
> \(a\)-threshold is at most \(v_a(f)\)?

The assignment labels can be removed completely. For each residual bundle
partition, build the resident agent--bundle feasibility graph. The
partition yields a favorite-singleton completion exactly when the owner's
scalar threshold passes and the resident graph has a perfect matching.
This equivalent Hall form, including the exact obstruction alternatives,
is proved in
[`FAVORITE_SINGLETON_HALL_LEMMA.md`](FAVORITE_SINGLETON_HALL_LEMMA.md).

## One scalar formulation of the missing lemma

For each prospective owner \(a\), let \(\mathcal E_a\) be the nonempty set
of three-agent EFX allocations of \(M\setminus\{f\}\) among
\(N\setminus\{a\}\), and define

\[
\Delta_a(V)=
\max_{Y\in\mathcal E_a}\bigl(v_a(f)-\tau_a(Y)\bigr),
\qquad
\Delta(V)=\max_{a\in N}\Delta_a(V).
\]

The lemma above gives the exact equivalence

\[
\text{a complete EFX allocation isolates }f
\quad\Longleftrightarrow\quad
\Delta(V)\ge0.
\]

Consequently the cap-free common-favorite target for four agents and nine
goods can be stated in one line:

> **Threshold-alternative conjecture.** If \(f\) is a common favorite and
> \(\Delta(V)<0\), then some partition of shape \(3+2+2+2\) supports a
> complete EFX allocation.

This statement is equivalent to the proposed balanced-or-common-favorite-
singleton dichotomy. It is stronger as a proof target because it removes
all quantifiers over the singleton branch: those have been compressed into
the four well-defined maxima \(\Delta_a\).

### Exact second-favorite decomposition

If the threshold alternative is false, every candidate allocation in both
branches has a strict violated inequality. Because there are finitely many
candidates, a sufficiently small perturbation preserves the failure while
making every row ranking strict and keeping \(f\) as the unique common
favorite. Thus a counterexample can be searched in generic position.

After fixing \(f=0\), each agent's second favorite is one of goods 1 through
8. Agent permutations and permutations of those eight goods leave only the
five multiplicity orbits below:

| Orbit | Representative | Raw vectors |
|---|---|---:|
| \(4\) | \(1111\) | 8 |
| \(3+1\) | \(1112\) | 224 |
| \(2+2\) | \(1122\) | 168 |
| \(2+1+1\) | \(1123\) | 2,016 |
| \(1+1+1+1\) | \(1234\) | 1,680 |

These counts sum to all \(8^4=4{,}096\) strict vectors. The frozen census is
[`efx49_common_favorite_second_orbits_audit.json`](efx49_common_favorite_second_orbits_audit.json).
Closing these five exact linear-real-arithmetic cells would prove the
threshold alternative throughout the common-favorite cell; it would not by
itself cover the other four favorite-multiplicity orbits.

## Why this is now the main analytic gate

The cap-12 rank-gap boundary profile has no EFX allocation of balanced shape
\(3+2+2+2\), but it has 838 complete EFX allocations. Every supporting
unlabeled partition isolates the common favorite. Thus the singleton branch
is not an artificial fallback; it is the exact repair forced by the first
balanced-shape failure.

The first dual-encoded cap-12 theorem package used:

- 424 balanced partitions; and
- 48 partitions with the common favorite as a singleton.

A countermodel-guided sparse rebuild shows that only the following two
singleton partitions are needed, in the canonical unused-good order:

\[
\{f\}\mid\{1,2\}\mid\{3,4\}\mid\{5,6,7,8\},
\qquad
\{f\}\mid\{1,2\}\mid\{3,4,6\}\mid\{5,7,8\}.
\]

Matching-clause and Hall-selector encodings both close the resulting
426-partition pool. The frozen sparse audit is
[`efx49_rankgap12_sparse_common_audit.json`](efx49_rankgap12_sparse_common_audit.json).

This suggests the general common-favorite dichotomy:

> either a balanced Hall matching exists, or the singleton-owner threshold
> problem has a solution.

Proving that dichotomy without a value cap would be a genuine bridge toward
general additive EFX. The tempting stronger shortcut—show that failure of
these two canonical singleton repairs forces one of the balanced Hall
matchings—is now refuted. The unrestricted-real frontier profile avoids the
entire 446-partition cap-13 pool, which contains all 426 cap-12 sparse
partitions, yet has 104 EFX allocations on 39 previously unseen
favorite-singleton partitions.

Therefore a cap-free proof cannot freeze the three-agent remainder to the
two canonical repairs, or even to the full finite cap-13 repair pool. It
must solve the existential selection problem over the available
three-agent EFX allocations. The present lemma isolates precisely that
remaining condition and removes every other EFX comparison from the
singleton branch.

The cap-13 experiments show that “common” is not essential. In the
\(3+1\) and \(2+2\) favorite orbits, the first balanced-shape failures are
again repaired only by isolating one of the designated favorite goods. The
lemma itself already applies to any selected \(f\); common-favorite
structure is relevant only to proving that some owner/allocation satisfies
the threshold. The broader analytic conjecture is therefore:

> every four-agent/nine-good instance has either a balanced EFX allocation
> or an EFX allocation that isolates some agent's favorite good.

## Unrestricted-real stress test

The first arbitrary-positive-real common-favorite profile found outside the
cap-13 sparse pool does not refute the structural conjecture. Exhaustive
literal enumeration finds 104 complete EFX allocations supported by 39
unlabeled partitions. Every supporting partition isolates the common
favorite, but none is balanced; the shapes range from \(4+2+2+1\) through
\(6+1+1+1\). Every agent can serve as the singleton owner in at least one
allocation, and the minimum owner-threshold slack is only one in the
integerized profile. This is useful negative guidance: a proof of the
singleton branch cannot impose a nearly balanced shape on the remaining
three-agent allocation or rely on a uniformly generous threshold margin.

The independently regenerated census is
[`efx49_common_favorite_real_frontier_audit.json`](efx49_common_favorite_real_frontier_audit.json).
The profile is a rigorous countermodel to the frozen finite repair pool,
not to EFX existence. A direct linear-real-arithmetic search against the
union of all balanced partitions and all common-favorite-singleton
partitions timed out after 300 seconds without a model or an infeasibility
verdict; an independent Hall-selector formulation timed out after 600
seconds on the same 447-partition pool.

The converse shortcut is false as well. A second strict common-favorite
profile has 2,231 complete EFX allocations supported by 514 partitions,
and every one has shape \(3+2+2+2\); it has no singleton EFX allocation at
all. Directly enumerating the three-agent selection problem finds between
356 and 364 residual EFX allocations for each possible singleton owner,
but zero pass the owner's threshold; even the best slacks are negative
(from \(-581\) to \(-2417\)), so \(\Delta(V)=-581\). In the singleton-only
profile, \(\Delta(V)=63{,}375\). In particular, the residual-threshold
\(6+1+1+1\) family cannot replace the balanced branch. Its frozen audit is
[`efx49_common_favorite_real_balanced_boundary_audit.json`](efx49_common_favorite_real_balanced_boundary_audit.json).

Together the two profiles show that the word “either” in the proposed
balanced-or-favorite-singleton dichotomy is essential. The active search
therefore targets the union, not either branch in isolation.

The partition-level Hall audit sharpens this comparison. The balanced-only
profile fails the owner threshold on all 3,864 owner--residual-partition
pairs, while the singleton-only profile has 80 pairs passing both the
threshold and resident matching gates. See
[efx49_common_favorite_hall_boundaries_audit.json](efx49_common_favorite_hall_boundaries_audit.json).
Universal threshold failure is therefore a clean first analytic subcase,
but not the full conjecture: a threshold-passing partition can still be
blocked by resident Hall deficiency.

The universal-threshold subcase is now closed by the
[strict-common-favorite universal-threshold theorem](COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_THEOREM.md).
The mixed complement is genuinely different. Exact cap-20 profiles have
many threshold-passing residual partitions but no Hall-valid
favorite-singleton partition; all of their complete EFX support is balanced.
One of them also blocks all six one-transfer repairs of a fixed
threshold-passing \(3+3+2\) partition. The surviving gate and the complete
literal censuses are in
[MIXED_THRESHOLD_HALL_GATE.md](MIXED_THRESHOLD_HALL_GATE.md).

The owner-only side of that subcase has an exact two-shape characterization.
For sorted residual values \(x_1\ge\cdots\ge x_8\), the best threshold over
all \(3+3+2\) partitions is
\(\max\{x_1,x_3+x_7,x_4+x_5\}\), while the best threshold over all
\(4+2+2\) partitions is
\(\max\{x_1,x_5+x_6+x_7\}\). Every safe residual shape can be reduced,
without increasing its threshold, to one of these two shapes. Hence
universal threshold failure is equivalent to

\[
x_5+x_6+x_7>v_a(f)
\quad\text{and}\quad
\bigl(x_3+x_7>v_a(f)\ \text{or}\ x_4+x_5>v_a(f)\bigr).
\]

In particular at least five residual goods are worth more than one third of
the favorite, and the residual row has total value greater than
\(7v_a(f)/3\). The proofs and exhaustive grid audit are in
[OWNER_THRESHOLD_SHAPE_ENVELOPE.md](OWNER_THRESHOLD_SHAPE_ENVELOPE.md).

See [RANK_GAP_EFX_4X9.md](RANK_GAP_EFX_4X9.md) for the finite theorem and
sharpness census.

An extreme subcase now has its own exact Hall formulation. If two more
goods are also isolated and the remaining goods form one residual bundle,
all threshold conditions are equivalent to a matching that saturates the
three singleton goods. See
[RESIDUAL_THRESHOLD_MATCHING_LEMMA.md](RESIDUAL_THRESHOLD_MATCHING_LEMMA.md).

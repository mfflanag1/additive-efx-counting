# Favorite-Singleton Hall Lemma

**Status:** proved analytic equivalence  
**Scope:** arbitrary nonnegative additive valuations, any number of agents
and goods  
**Not claimed:** that a partition satisfying the two conditions always
exists

## Statement

Let \(N\) be a set of \(n\) agents, let \(M\) be a set of goods, fix an
agent \(a\in N\) and a good \(f\in M\), and let

\[
\mathcal P=\{B_1,\ldots,B_{n-1}\}
\]

be an unlabeled partition of \(M\setminus\{f\}\) into \(n-1\) bundles.
Empty bundles may be included if desired. Define

\[
\theta_i(B_k;\mathcal P)
=
\max_{\ell\ne k}
\left(v_i(B_\ell)-\min_{g\in B_\ell}v_i(g)\right),
\]

where every empty-bundle threshold is interpreted as zero. Construct the bipartite graph
\(G_{a,\mathcal P}\) whose left vertices are the residents
\(N\setminus\{a\}\) and whose right vertices are the bundles in
\(\mathcal P\). Put an edge \(i\sim B_k\) exactly when

\[
v_i(B_k)\ge \theta_i(B_k;\mathcal P).
\tag{1}
\]

For the prospective singleton owner, define

\[
\tau_a(\mathcal P)
=
\max_{B\in\mathcal P}
\left(v_a(B)-\min_{g\in B}v_a(g)\right).
\tag{2}
\]

Then the partition

\[
\bigl\{\{f\}\bigr\}\cup\mathcal P
\]

supports a complete EFX allocation in which agent \(a\) receives
\(\{f\}\) if and only if

1. \(v_a(f)\ge\tau_a(\mathcal P)\); and
2. \(G_{a,\mathcal P}\) has a perfect matching.

Equivalently, condition 2 may be replaced by the Hall inequalities

\[
|N_{G_{a,\mathcal P}}(Q)|\ge |Q|
\qquad(Q\subseteq\mathcal P).
\tag{3}
\]

## Proof

Suppose first that conditions 1 and 2 hold. Give each resident the bundle
matched to it and give \(\{f\}\) to \(a\). By (1), every resident satisfies
all EFX comparisons against the other residual bundles. A resident cannot
strongly envy \(\{f\}\), because removing its only good leaves the empty
bundle. Condition 1 gives all comparisons from \(a\) to the residual
bundles. These exhaust the ordered agent pairs, so the allocation is EFX.

Conversely, suppose the displayed partition supports EFX with \(a\) owning
\(\{f\}\). Each resident owns a distinct residual bundle. Its EFX
comparisons give (1), so the owner--bundle pairs form a perfect matching in
\(G_{a,\mathcal P}\). The singleton owner's comparisons give
\(v_a(f)\ge\tau_a(\mathcal P)\). Hall's theorem gives the equivalent form
(3). \(\square\)

## Exact obstruction form

For fixed \(a,f\), there is no EFX allocation isolating \(f\) at owner
\(a\) if and only if every residual partition \(\mathcal P\) has at least
one of the following certificates:

\[
\tau_a(\mathcal P)>v_a(f),
\tag{threshold obstruction}
\]

or a bundle subfamily \(Q\subseteq\mathcal P\) with

\[
|N_{G_{a,\mathcal P}}(Q)|<|Q|.
\tag{Hall obstruction}
\]

Thus the favorite-singleton branch is not an opaque existential search over
labeled allocations. It is a partition theorem with one scalar gate and
one standard matching gate.

For four agents and nine goods, each owner produces only a three-by-three
resident graph. Its Hall failure has exactly three forms:

1. some residual bundle is feasible for no resident;
2. two residual bundles are collectively feasible for at most one
   resident; or
3. all three residual bundles are collectively feasible for at most two
   residents.

This is the natural interface for a concise Farkas or exchange proof of the
common-favorite threshold alternative: a hypothetical failure must choose a
threshold or one of these three Hall obstructions for every residual
partition, while every balanced four-bundle partition simultaneously has a
four-agent Hall obstruction.

## Relation to the current frontier

The earlier
[favorite-singleton reduction](COMMON_FAVORITE_SINGLETON_REDUCTION.md)
quantified over three-agent EFX allocations. The present lemma quotients out
the assignment labels and replaces “the residual allocation is EFX” by a
perfect matching on its bundle partition. It is logically equivalent, but
it aligns the singleton branch with the same partition/Hall language used
by the balanced branch and by the exact solver certificates.

The
[residual-threshold matching lemma](RESIDUAL_THRESHOLD_MATCHING_LEMMA.md)
is the special case where the residual partition consists of two more
singletons and one residual bundle. In that shape the resident and external
conditions collapse further to a single matching that saturates the three
singleton goods. The lemma here applies to every residual shape and is the
appropriate analytic target after that extreme-shape shortcut was
falsified.

The executable semantic audit
[favorite_singleton_hall_lemma_audit.json](favorite_singleton_hall_lemma_audit.json)
checks the equivalence against literal EFX on all 4,096 positive
three-agent/four-good profiles over values \(\{1,2\}\), all three singleton
owners, and all three residual two-bundle partitions (36,864
owner--partition checks). It is a regression check for the encoding, not a
substitute for the proof above.

The two unrestricted-real boundary profiles give a sharper \(2\times2\)
gate census in
[efx49_common_favorite_hall_boundaries_audit.json](efx49_common_favorite_hall_boundaries_audit.json).
The singleton-only profile has 80 owner--partition pairs that pass both
gates. In the balanced-only profile, the owner threshold fails on every one
of the \(4\cdot966=3{,}864\) owner--partition pairs, including partitions
whose resident graph is Hall-deficient. This identifies a clean first
subcase of the full threshold alternative:

> if every owner fails the scalar threshold on every residual partition,
> prove that a balanced partition has a four-agent perfect matching.

This subcase is strictly weaker than the full desired theorem. In general,
a partition may pass the owner threshold while failing the resident Hall
gate, so \(\Delta<0\) only says that no partition passes both conditions.

That mixed possibility is now known to be essential, not merely logical.
Two exact positive profiles contain 114 and 273 threshold-passing
owner--partition pairs respectively, but no partition isolating the common
favorite supports EFX. Every EFX-supporting partition in both profiles is
instead balanced of shape \(3+2+2+2\). A third profile refutes repairing a
fixed threshold-passing \(3+3+2\) partition by one of its six one-good
favorite-pair transfers. See
[MIXED_THRESHOLD_HALL_GATE.md](MIXED_THRESHOLD_HALL_GATE.md) and the frozen
[mixed-boundary audit](efx49_common_favorite_mixed_hall_boundaries_audit.json).
Thus the remaining proof must use the Hall witness to reach the balanced
branch, while allowing the selected owner and residual partition to change.

## Canonical \(3+3+2\) threshold wall

Assume \(f\) is a favorite of owner \(a\), and sort the values of the eight
residual goods as

\[
x_1\ge x_2\ge\cdots\ge x_8.
\]

Consider the owner-specific residual partition

\[
\{x_1,x_2\}
\;\middle|\;
\{x_3,x_7,x_8\}
\;\middle|\;
\{x_4,x_5,x_6\},
\tag{4}
\]

where the symbols denote the corresponding goods. Its three owner
thresholds are

\[
x_1,\qquad x_3+x_7,\qquad x_4+x_5.
\]

The first is at most \(v_a(f)\) because \(f\) is a favorite. Consequently,
partition (4) passes the owner threshold if and only if

\[
x_3+x_7\le v_a(f)
\quad\text{and}\quad
x_4+x_5\le v_a(f).
\tag{5}
\]

This is an exact calculation: a pair's threshold is its larger item, and a
triple's threshold is the sum of its two larger items.

Hence the universal-threshold-failure subcase necessarily satisfies, in
every row,

\[
x_3+x_7>v_a(f)
\quad\text{or}\quad
x_4+x_5>v_a(f).
\tag{6}
\]

For four agents this gives 16 binary branch vectors, or five multiplicity
patterns under agent permutation. The goods occupying the ranks may differ
by row, so (6) is a compact analytic case split, not a proof that a balanced
matching exists.

Together with the exact \(4+2+2\) envelope, this condition is also
sufficient for universal threshold failure after adding
\(x_5+x_6+x_7>v_a(f)\). Every other residual shape either is \(4+2+2\) or
can be reduced to \(3+3+2\) or \(4+2+2\) without increasing the threshold.
Thus the full owner-only obstruction is exactly

\[
x_5+x_6+x_7>v_a(f)
\quad\text{and}\quad
\bigl(x_3+x_7>v_a(f)\ \text{or}\ x_4+x_5>v_a(f)\bigr).
\]

See
[OWNER_THRESHOLD_SHAPE_ENVELOPE.md](OWNER_THRESHOLD_SHAPE_ENVELOPE.md).

### Half-favorite matching dichotomy

For each agent \(a\), define its residual half-favorite set

\[
H_a=\{g\ne f:v_a(g)>\tfrac12v_a(f)\}.
\]

Either disjunct in (6) implies \(|H_a|\ge3\). Indeed, the first implies
\(x_3>\tfrac12v_a(f)\), and the second implies the stronger
\(x_4>\tfrac12v_a(f)\), hence \(|H_a|\ge4\).

Form the bipartite graph from the four agents to the eight residual goods,
with edge \(a\sim g\) when \(g\in H_a\). Then exactly one of the following
holds:

1. the graph has a matching saturating all four agents; or
2. all four sets \(H_a\) are the same three-good set, and every row uses
   only the first disjunct of (6).

To prove this, suppose the graph has no saturating matching. Every nonempty
agent subset has at least three neighbors because each of its agents has
degree at least three. Thus no subset of at most three agents violates
Hall's inequality. The full four-agent set must be deficient, so its
neighborhood has size at most three. Every \(H_a\) has size at least three,
forcing all four sets to equal the same three-good neighborhood. A row
satisfying the second disjunct would have at least four neighbors, a
contradiction. \(\square\)

This turns the universal-threshold subcase into two item-geometric branches:
four distinct half-favorite representatives, or three common contested
representatives. A completion proof is still needed in the first branch;
the second branch closes below.

### Four-pair normal form in the common-three branch

In the second branch, write the common three-good set as \(H\) and the
other five residual goods as \(L\). For every agent, the goods in \(H\) are
exactly its three residual goods worth more than half the common favorite.
Because only the first disjunct of (6) remains, \(x_3+x_7>v_a(f)\).
Consequently at least four goods in \(L\) satisfy

\[
v_a(\ell)>v_a(f)-x_3.
\tag{7}
\]

Choose one agent to receive \(f\), and biject the three other agents with
the three goods in \(H\). Build a bipartite graph from these three agents to
\(L\), joining agent \(a\) to \(\ell\) when (7) holds for that agent. Every
left vertex has degree at least four in a five-good set, so Hall's theorem
gives a matching saturating the three agents. Pair each matched agent's
good \(h\in H\) with its matched low good \(\ell\). Since
\(v_a(h)\ge x_3\), every such owner values its pair strictly above
\(v_a(f)\).

Pair the fourth agent's common favorite \(f\) with one unused low good and
leave the last low good \(r\) unallocated. The resulting four allocated
bundles are pairs. Every owner values its pair at least \(v_a(f)\), while
every observer values each individual target good at most its own value for
\(f\). Removing either good from a target pair therefore leaves value at
most the observer's own bundle value. The partial allocation is EFX.
Moreover every owner values its bundle at least \(v_a(f)\ge v_a(r)\), so
the floater is unenvied.

Thus the common-three branch always has a canonical four-pair, one-floater
EFX normal form.

This parking gate has a compact exact form. Write the pair at host \(h\) as
\(\{q_h,\ell_h\}\), where \(q_h\in H\cup\{f\}\), and let \(r\) be the
floater. For every observer \(k\), \(q_h\) is worth more than either low
good \(\ell_h,r\). Adding \(r\) at \(h\) is EFX if and only if

\[
v_k(q_k)+v_k(\ell_k)
\ge
v_k(q_h)+\max\{v_k(\ell_h),v_k(r)\}
\qquad(k\ne h).
\tag{8}
\]

The host's own comparisons remain safe because its bundle only improves;
all nonhost targets are unchanged. For a nonhost observer, the right side
of (8) is exactly the value of the enlarged target triple after its
least-valued good is removed.

### Lexicographic parking lemma

The parking gate always has a solution in the common-three branch.
More precisely, let \(Q=H\cup\{f\}\). A **valid pair state** consists of
a bijection from the four agents to four disjoint pairs

\[
\{q_k,\ell_k\},\qquad q_k\in Q,\quad \ell_k\in L,
\]

using every anchor in \(Q\), together with the one unused low good \(r\),
such that

\[
v_k(q_k)+v_k(\ell_k)\ge v_k(f)
\qquad(k\in N).
\tag{9}
\]

Such a state exists. Assign \(f\) to any one agent and the three goods in
\(H\) to the other three. Each of those three agents has at least four
qualifying neighbors in the five-good set \(L\), so Hall's theorem matches
them to distinct qualifying lows. Give any fourth low to the \(f\)-agent
and leave the last low unused.

Fix an agent \(h\), place it last in an ordering of the agents, and choose a
valid pair state whose vector of own-pair utilities is lexicographically
maximal in that order. Then adding its floater \(r\) to \(h\)'s pair is
EFX.

To prove this, suppose an earlier agent \(k\ne h\) violates (8). Let
\(s\in\{\ell_h,r\}\) be whichever of those two lows \(k\) values more.
Then

\[
v_k(q_h)+v_k(s)
>
v_k(q_k)+v_k(\ell_k)
\ge v_k(f),
\tag{10}
\]

so \(\{q_h,s\}\) is a valid and strictly improving pair for \(k\).
After making that replacement, the two available lows for \(h\) are
\(\ell_k\) and the other member of \(\{\ell_h,r\}\). If \(q_k=f\), either
low produces a valid pair for \(h\). If \(q_k\in H\), at most one of the
five lows is nonqualifying for \(h\), so at least one of these two available
lows, say \(t\), satisfies

\[
v_h(q_k)+v_h(t)>v_h(f).
\]

Give \(\{q_k,t\}\) to \(h\) and leave the other available low unused. This
is another valid pair state. Every agent preceding \(k\) in the fixed order
is unchanged, while \(k\) strictly improves by (10); changes to \(h\) occur
last. This contradicts lexicographic maximality. Thus every nonhost
observer satisfies (8).

Finally, for every observer, each anchor is worth at most its favorite and
each low is worth at most half its favorite. Hence (9) already makes every
comparison against the three nonhost pairs EFX. The host's bundle only
improves when \(r\) is added, and the preceding argument makes every
comparison against the resulting triple EFX. The completed allocation is
therefore EFX. \(\square\)

Consequently, under universal threshold failure, the common-three side of
the half-favorite dichotomy always admits a complete EFX allocation of
shape \(3+2+2+2\), with the four goods in \(H\cup\{f\}\) separated. The
only remaining item-geometric branch of this subcase is the existence of
four distinct half-favorite representatives.

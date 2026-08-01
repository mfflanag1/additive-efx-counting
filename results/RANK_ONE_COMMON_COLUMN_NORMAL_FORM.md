# Rank-One Common-Column Normal Form

**Status:** proved analytic reduction; all one-transfer successors refuted  
**Scope:** four agents, a favorite singleton, and a threshold-safe residual
partition into three bundles  
**Not claimed:** complete EFX for the mixed branch or the common-favorite cell

## Normal-form lemma

Let agent \(a\) pass the favorite-singleton owner threshold on a residual
partition \(A\mid B\mid C\). If the three-resident feasibility graph has
matching rank one, then, after renaming the bundles, every resident accepts
only \(A\). Moreover, for every resident \(i\),

\[
v_i(A)-\min_{g\in A}v_i(g)
>
\max\{v_i(B),v_i(C)\}. \tag{1}
\]

Every row of a residual feasibility graph is nonempty: a bundle of maximum
total value is feasible for that agent because every other bundle becomes
no larger when one good is removed. In a bipartite graph with three
nonempty resident rows, matching rank one therefore forces all edges into
one common column; otherwise edges in two distinct rows and columns give a
matching of size two.

Call the common bundle \(A\), and suppose without loss of generality that
\(v_i(B)\ge v_i(C)\). Bundle \(B\) is infeasible for resident \(i\). Its
violated comparison cannot be against \(C\), since every proper remainder
of \(C\) has value at most \(v_i(C)\le v_i(B)\). It must be against a
remainder of \(A\), proving

\[
v_i(A)-\min_{g\in A}v_i(g)>v_i(B).
\]

This is (1).

## Owner-switch reduction

Equation (1) makes the threshold status of every resident transparent. The
same partition passes resident \(i\)'s owner threshold exactly when

\[
v_i(A)-\min_{g\in A}v_i(g)\le v_i(f), \tag{2}
\]

because both side-bundle thresholds are strictly smaller than the left side
of (2).

If the original owner \(a\) accepts either side bundle and some resident
satisfies (2), switch the singleton owner to that resident. Two remaining
residents accept \(A\), while \(a\) accepts the side bundle, so the new
resident graph has matching rank at least two. Consequently, any rank-one
state that cannot be improved by this owner switch has one of two exact
forms:

1. all three residents satisfy the strict density wall
   \(v_i(A)-\min A>v_i(f)\); or
2. the original owner also accepts only \(A\), so all four agents share the
   same unique feasible residual bundle.

If \(A\) is a pair, its threshold is one singleton value and hence is at
most the common favorite. Thus every resident satisfies (2), leaving only
the owner-switch or four-agent-common-column subcases. If \(A\) is a
triple, the first alternative becomes the concrete high-pair inequality
that the two largest goods of \(A\) sum above the favorite in every resident
row.

## Triple-conversion boundary

For a \(3+3+2\) residual partition with common triple \(A\), the first
candidate lemma was:

> Either some favorite-singleton partition supports EFX, or moving one good
> of \(A\) next to \(f\) produces an EFX partition of shape \(3+2+2+2\).

The no-singleton hypothesis is necessary but not sufficient. The first
exact positive matrix in
[efx49_common_favorite_rank1_triple_gate_audit.json](efx49_common_favorite_rank1_triple_gate_audit.json)
passes the selected threshold, has resident graph

\[
\begin{pmatrix}1&0&0\\1&0&0\\1&0&0\end{pmatrix},
\]

and blocks all three conversions. It nevertheless has 116
favorite-singleton supporting partitions and 301 complete EFX allocations.

The sharp version is now exactly refuted as well. A cap-20 profile excludes
all 966 favorite-singleton partitions and blocks all six one-good transfers
from either triple onto the favorite. Literal enumeration nevertheless finds
366 EFX-supporting partitions, all of shape \(3+2+2+2\), and 1,259 complete
EFX allocations. Its nearest 15 repairs are exactly two transfers away.
The independently reconstructed census is
[efx49_common_favorite_rank1_local6_boundary_audit.json](efx49_common_favorite_rank1_local6_boundary_audit.json).

The exact successor is therefore a radius-two exchange lemma. There are 63
balanced partitions within two transfers of the selected state. A cap-20
CEGAR master blocked all 63, learned 256 singleton obstructions from its
first exact model, and returned `UNKNOWN` on the next 30-second solve. This endpoint
neither proves nor refutes the radius-two implication.

This normal form remains the first analytic reduction inside the mixed Hall
branch: it replaces an arbitrary rank-one graph by one named bundle, one
strict inequality per resident, and two owner-switch subcases. Any successful
conversion proof must now use a genuinely two-step exchange or a larger
adaptive family. Rank two and its zero-neighbor/two-bundle Hall forms remain
separate successor gates.

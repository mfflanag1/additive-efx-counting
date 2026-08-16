# Common-Three Lexicographic Parking Lemma

**Status:** cap-free analytic proof  
**Scope:** four agents, nine goods, nonnegative additive valuations  
**Consequence:** closes one of the two branches forced by universal failure
of the common-favorite singleton threshold  
**Not claimed:** general additive EFX existence

## Basic idea

Suppose all four agents have the same favorite good \(f\), the same three
other goods that each values above half of \(f\), and five remaining “low”
goods. Suppose also that every agent has at most one low good that cannot be
paired successfully with all three high goods.

First allocate four anchor--low pairs, leaving one low good out. Among all
such valid partial allocations, choose one that lexicographically maximizes
the agents' own values, with a designated host placed last in the priority
order. If an earlier agent would strongly envy the host after the leftover
good is added, that agent can take a strictly preferred pair from the host.
The host can absorb the displaced anchor with one of two available lows,
because at most one low is bad for it. This improves the lexicographic
vector before the last coordinate, a contradiction. Therefore the leftover
good can be added to the host.

## Theorem

Let \(N\) contain four agents and let the goods be

\[
\{f\}\mathbin{\dot\cup}H\mathbin{\dot\cup}L,
\qquad |H|=3,\quad |L|=5.
\]

For every agent \(i\), assume:

1. \(f\) is a strict favorite;
2. \(v_i(h)>\tfrac12v_i(f)\) for every \(h\in H\);
3. \(v_i(\ell)\le\tfrac12v_i(f)\) for every \(\ell\in L\); and
4. at least four goods \(\ell\in L\) satisfy

\[
v_i(h)+v_i(\ell)>v_i(f)
\qquad\text{for every }h\in H.
\tag{1}
\]

Then a complete EFX allocation exists. It may be chosen with shape
\(3+2+2+2\), with the four anchors in \(H\cup\{f\}\) lying in different
bundles.

## Proof

Call a low good satisfying (1) **qualifying** for agent \(i\). A valid pair
state assigns the four anchors \(H\cup\{f\}\) bijectively to the agents,
pairs each anchor with a distinct low good, leaves one low \(r\) unallocated,
and gives every agent \(i\) a pair \(B_i=\{q_i,\ell_i\}\) satisfying

\[
v_i(B_i)\ge v_i(f).
\tag{2}
\]

At least one valid pair state exists. Give \(f\) to any one agent and
bijection the three high goods with the other three agents. Each of those
three agents has at least four qualifying neighbors among five lows, so
Hall's theorem matches them to distinct qualifying lows. Give any remaining
low to the \(f\)-agent and leave the fifth low unallocated.

Fix any agent \(z\), order the other three agents before \(z\), and choose a
valid pair state whose vector

\[
(v_{i_1}(B_{i_1}),v_{i_2}(B_{i_2}),v_{i_3}(B_{i_3}),v_z(B_z))
\]

is lexicographically maximal. We claim that adding \(r\) to \(B_z\) is EFX.

Every anchor is worth at most \(v_i(f)\) to observer \(i\), and every low is
worth at most \(\tfrac12v_i(f)\). Thus (2) makes every EFX comparison against
an unchanged pair safe. The host \(z\)'s own bundle only improves. It remains
to check another agent \(k\ne z\) against the enlarged host bundle
\(\{q_z,\ell_z,r\}\).

For observer \(k\), the anchor \(q_z\) is strictly more valuable than either
low. Consequently the largest remainder after deleting one good from the
host triple has value

\[
v_k(q_z)+\max\{v_k(\ell_z),v_k(r)\}.
\tag{3}
\]

Suppose \(k\) fails this comparison, and let \(s\in\{\ell_z,r\}\) maximize
\(v_k(s)\). Then

\[
v_k(q_z)+v_k(s)>v_k(B_k)\ge v_k(f),
\tag{4}
\]

so \(\{q_z,s\}\) is a valid pair that strictly improves \(k\).

Give this pair to \(k\). The two lows now available for \(z\) are
\(\ell_k\) and the other good in \(\{\ell_z,r\}\setminus\{s\}\). If
\(q_k=f\), pairing \(q_k\) with either one satisfies (2). If \(q_k\in H\),
at most one of all five lows is nonqualifying for \(z\), so at least one of
these two available lows, say \(t\), satisfies (1). Give
\(\{q_k,t\}\) to \(z\) and leave the other available low unallocated.

This is another valid pair state. All agents preceding \(k\) in the fixed
order are unchanged, \(k\) strictly improves by (4), and any change to
\(z\) occurs in the last coordinate. This contradicts lexicographic
maximality. Hence no \(k\ne z\) fails (3), and adding \(r\) to \(B_z\)
produces a complete EFX allocation. \(\square\)

## Why this condition arises

Under universal failure of the favorite-singleton owner threshold, sorting
the eight residual values in each row yields

\[
x_3+x_7>v_i(f)
\quad\text{or}\quad
x_4+x_5>v_i(f).
\]

Every row therefore has at least three residual half-favorites. Hall's
theorem gives either four distinct half-favorite representatives, or the
same set of exactly three half-favorites for all four agents. In the latter
case only the first rank inequality can occur, and it implies that at least
four of the five lows satisfy (1). The theorem therefore closes the entire
common-three branch. The distinct-representatives branch remains open.

## Reproducibility boundary

The proof above is finite and analytic; it does not depend on a value cap or
solver output. The executable audit
[efx49_common_three_lex_parking_audit.json](efx49_common_three_lex_parking_audit.json)
constructs the prescribed lexicographic state and checks literal EFX on an
exhaustive small grid plus deterministic exact-integer stress profiles. It
is a regression test for the construction, not a substitute for the proof.

The exact QF_LRA workbench
[decide_common_three_anchored.py](../tracks/parkability/decide_common_three_anchored.py)
also encodes the negation of all 240 anchor-separated balanced partitions.
The complete matching-clause and Hall-selector formulas both returned exact
unsat over normalized positive reals. Their scopes and frozen SMT-LIB
hashes are checked together in
[efx49_common_three_dual_encoding_audit.json](efx49_common_three_dual_encoding_audit.json).
These are adversarial computational checks; the theorem does not rely on
either solver result, and neither result is an independently proof-checked
certificate.

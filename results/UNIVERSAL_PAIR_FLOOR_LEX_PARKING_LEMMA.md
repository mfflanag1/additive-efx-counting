# Universal Pair-Floor Lexicographic Parking Lemma

**Status:** cap-free analytic proof  
**Scope:** any number of agents, exactly \(2n+1\) goods, additive valuations  
**Not claimed:** that the pair-floor premise follows in every additive instance

## Theorem

Let \(N\) contain \(n\) agents and let \(M\) contain \(2n+1\) goods. Suppose
there is a good \(f\) such that, for every agent \(i\),

1. \(f\) is a favorite good; and
2. every two distinct residual goods \(g,h\in M\setminus\{f\}\) satisfy

\[
v_i(g)+v_i(h)\ge v_i(f).
\tag{1}
\]

Then a complete EFX allocation exists. It may be chosen with one bundle of
size three and \(n-1\) bundles of size two.

## Proof

A **valid pair state** partitions \(2n\) goods into \(n\) pairs, assigns one
pair \(B_i\) to every agent, leaves one good \(r\) unallocated, and satisfies

\[
v_i(B_i)\ge v_i(f)\qquad(i\in N).
\tag{2}
\]

Such a state exists: leave \(f\) unallocated, partition the \(2n\) residual
goods arbitrarily into pairs, and assign the pairs arbitrarily. Condition
(1) gives (2).

Fix an agent \(z\), place it last in an ordering of the agents, and choose a
valid pair state whose vector of own-pair utilities is lexicographically
maximal in that order. We claim that adding \(r\) to \(B_z\) is EFX.

Every individual good is worth at most \(v_i(f)\) to observer \(i\), so (2)
makes every comparison against an unchanged pair EFX. The host's own bundle
only improves. If some other agent \(k\) strongly envies the enlarged host
bundle \(B_z\cup\{r\}\), then one of its three two-good remainders, say
\(S\), satisfies

\[
v_k(S)>v_k(B_k)\ge v_k(f).
\tag{3}
\]

Give \(S\) to \(k\). The three goods now available for \(z\) are the old
pair \(B_k\) and the one good in
\((B_z\cup\{r\})\setminus S\). Any two of these three goods form a valid
pair for \(z\): a pair containing \(f\) has value at least \(v_z(f)\) by
nonnegativity, while a pair not containing \(f\) satisfies (1). Give any
such pair to \(z\) and leave the third good unallocated.

This is another valid pair state. Every agent before \(k\) in the fixed
order is unchanged, \(k\) strictly improves by (3), and any change to \(z\)
occurs last. This contradicts lexicographic maximality. Hence no nonhost
agent strongly envies the enlarged host bundle, and the completed
allocation is EFX. \(\square\)

## Relation to the \(4\times9\) gate

For four agents and nine goods, the theorem closes the regime in which each
agent's two least-valued residual goods already sum to at least its common
favorite. The exact universal owner-threshold condition in
[OWNER_THRESHOLD_SHAPE_ENVELOPE.md](OWNER_THRESHOLD_SHAPE_ENVELOPE.md) does
not imply this pair floor; for example

\[
(F;x_1,\ldots,x_8)=(7;4,4,4,4,4,2,2,1)
\]

has universal threshold failure but violates (1). Thus this lemma is a
genuine general analytic bridge, but the distinct-half-favorite-
representatives branch in
[UNIVERSAL_THRESHOLD_BALANCED_GATE.md](UNIVERSAL_THRESHOLD_BALANCED_GATE.md)
still requires a triple-aware or longer alternating exchange.

The executable semantic audit
[universal_pair_floor_lex_parking_audit.json](universal_pair_floor_lex_parking_audit.json)
checks the construction for all 289 qualifying two-agent profiles over
values \(\{1,2\}\), plus deterministic three- and four-agent exact-integer
stress profiles, for 1,090 designated-host completions. It is a regression
test, not a substitute for the proof.

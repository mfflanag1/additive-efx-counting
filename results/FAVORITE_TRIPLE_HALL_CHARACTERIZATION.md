# Favorite-Triple Hall Characterization

**Status:** cap-free analytic equivalence  
**Scope:** four nonnegative additive agents, nine goods, strict common
favorite  
**Role:** exact conversion criterion for balanced partitions with the favorite
in the triple

## Theorem

Let the agents have nonnegative additive valuations. Let \(f\) be a strict
favorite of every agent and write
\(F_i=v_i(f)\). Fix two residual goods \(a,b\), and partition the other six
goods into three pairs \(P,Q,R\). Put

\[
T=\{f,a,b\},\qquad
\theta_i(a,b)=F_i+\max\{v_i(a),v_i(b)\}.
\]

Form a bipartite graph between the three pairs \(P,Q,R\) and the four
agents. Join pair \(S\) to agent \(i\) exactly when

\[
v_i(S)\ge \theta_i(a,b). \tag{1}
\]

Then the partition \(T\mid P\mid Q\mid R\) supports a complete EFX
allocation if and only if this graph has a matching saturating the three
pair vertices. Under such a matching, give the pairs to their matched
agents and give \(T\) to the unmatched agent.

Equivalently, Hall's three conditions are:

1. every pair has at least one accepting agent;
2. every two pairs together have at least two accepting agents; and
3. the three pairs together have at least three accepting agents.

## Proof

For observer \(i\), deleting one good from \(T\) leaves at most

\[
F_i+\max\{v_i(a),v_i(b)\}=\theta_i(a,b),
\]

because \(f\) is the most valuable good. Deleting one good from any of
\(P,Q,R\) leaves a single residual good, whose value is strictly below
\(F_i\), and hence below \(\theta_i(a,b)\). Thus the largest EFX target
remainder in the whole partition is exactly \(\theta_i(a,b)\).

The triple itself is feasible for every agent because

\[
v_i(T)=F_i+v_i(a)+v_i(b)\ge\theta_i(a,b).
\]

A pair \(S\) is feasible for agent \(i\) exactly when (1) holds. Therefore
the full EFX-feasibility graph consists of one universal triple column and
the pair--agent graph defined above. It has a perfect matching exactly when
the three pair columns can be matched to three distinct agents. Hall's
theorem gives the three displayed conditions. \(\square\)

## Consequences

The
[common-low favorite-triple lemma](COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md)
is the complete-bipartite special case of this theorem.

More importantly, if two pairs are accepted by every agent and the third
pair is rejected by at most one agent, the original favorite-triple
partition is already EFX-supporting: assign the triple to the possible
rejecter. No pair-comparison condition and no movement of a low good are
needed for existence. The exchange in
[ONE_DEFECT_FAVORITE_TRIPLE_CONVERSION_LEMMA.md](ONE_DEFECT_FAVORITE_TRIPLE_CONVERSION_LEMMA.md)
remains useful only when one specifically wants to move the favorite back
into a pair.

The exact obstruction to a fixed favorite-triple partition is now one of
three small Hall witnesses:

- a pair rejected by all four agents;
- two pairs whose accepting agents lie in one common agent; or
- three pairs whose accepting agents lie in at most two common agents.

This is the concise analytic interface needed for proof mining. It replaces
the stronger intersection-graph demand that every selected pair be accepted
by every observer.

## Two-core/Tutte corollary

Fix \(a,b\) and suppose two agents \(c,d\) accept every one of the 15 pairs
among the other six goods under (1). Let \(B\) be the graph on those six
goods whose edges are rejected by both of the other two agents. Then every
one of the 15 perfect pairings supports EFX if and only if \(B\) has no
perfect matching.

Indeed, every selected pair has the two common neighbors \(c,d\). The
one-pair and two-pair Hall inequalities are therefore automatic. The
three-pair Hall inequality fails exactly when none of the three selected
edges has an accepting agent outside \(\{c,d\}\), which says exactly that
the selected perfect matching lies in \(B\). This proves the equivalence.

Tutte's theorem can now be used on one concrete bad-edge graph without
discarding all agent-relative information. A sufficient selection target
for the distinct-half branch is:

> Conditional on no favorite-pair EFX partition, find \(a,b\) and two
> common accepting agents for all residual edges such that the corresponding
> outsider-rejection graph \(B\) has no perfect matching.

The current tight no-favorite-pair boundaries satisfy this condition. It is
a proof target, not yet a proved consequence of the distinct-half
hypotheses.

The low pair cannot be restricted to the four half-favorite
representatives. A strict zero-favorite-pair boundary has representatives
(1,2,3,4), no representative-pair/complementary-agent two-core, and a
unique unrestricted witness at lows (5,6) with core agents (1,3).
Thus the live selection target must range over all 28 low pairs and all six
agent pairs; see
[efx49_distinct_half_canonical_two_core_boundary_audit.json](efx49_distinct_half_canonical_two_core_boundary_audit.json).

The two-core condition is sufficient but not necessary for a *full Hall
cell*, meaning that all 15 perfect pairings work for the same \(a,b\). A
cap-20 branch profile has a full Hall cell at \(a,b=7,8\) while having no
two-core witness at any low pair. It also retains 20 favorite-pair EFX
partitions, so it does not refute the conditional two-core target. It does
show that the following intermediate selection statement is strictly more
flexible and should be tested first:

> Conditional on no favorite-pair EFX partition, find \(a,b\) for which
> every perfect pairing of the other six goods satisfies the three Hall
> conditions above.

This full-cell target is stronger than the exact conversion gate, which
needs only one working pairing, but weaker than forcing a two-core witness.
The audited zero-favorite-pair boundaries all satisfy it.

### Exact six-vertex Tutte classification

Because \(B\) has exactly six vertices, the condition “\(B\) has no perfect
matching” has only three possible structural witnesses:

1. \(B\) itself has at least two odd components;
2. deleting one vertex leaves at least three odd components; or
3. deleting two vertices leaves four isolated vertices, equivalently those
   two vertices cover every edge of \(B\).

To see this, Tutte's theorem supplies a set \(U\) with
\(o(B-U)>|U|\). The parity of \(o(B-U)\) equals the parity of \(6-|U|\).
For \(|U|=0,1,2\), this gives respectively the three cases above. For
\(|U|\ge3\), at most \(6-|U|\le |U|\) vertices remain, so the strict Tutte
inequality is impossible. Conversely, each displayed witness is a direct
Tutte obstruction.

Thus the live two-core selection lemma can be attacked through three
concrete outsider-rejection patterns rather than an arbitrary graph
condition. The exhaustive audit
[efx49_six_vertex_tutte_classification_audit.json](efx49_six_vertex_tutte_classification_audit.json)
checks the equivalence against all \(2^{15}\) labeled graphs on six
vertices.

The executable audit
[efx49_favorite_triple_hall_characterization_audit.json](efx49_favorite_triple_hall_characterization_audit.json)
compares the criterion with the literal EFX-feasibility graph on every
favorite-triple balanced partition of deterministic test profiles. It is a
regression check for the proof, not a substitute for it.

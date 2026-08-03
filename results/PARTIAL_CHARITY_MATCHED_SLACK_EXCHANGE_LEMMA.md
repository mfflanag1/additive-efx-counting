# Matched-slack exchange lemma

## Statement

Fix a complete candidate bundle partition \(Y=(Y_1,\ldots,Y_n)\), a
remaining charity set \(R\), and a perfect assignment \(\pi\). Let \(a_q\)
be the agent matched to bundle \(q\), so \(\pi(a_q)=q\).

Select some bundle slots. In every selected slot \(q\), replace one good
\(g_q\in Y_q\) by an incoming good \(h_q\), with the selected outgoing and
incoming goods forming a permutation so that the bundles remain a partition.
Call the resulting bundles \(Y'\). Assume:

\[
v_{a_q}(h_q)\geq v_{a_q}(g_q)
\qquad\text{for every selected }q, \tag{1}
\]

while every agent not matched to that bundle weakly prefers the outgoing
good:

\[
v_i(h_q)\leq v_i(g_q)
\qquad\text{for every selected }q\text{ and }i\ne a_q. \tag{2}
\]

Then every matched acceptance slack under the same assignment weakly
increases:

\[
s'_{i,\pi(i)}\geq s_{i,\pi(i)}
\qquad(i\in N).
\]

If (1) is strict for at least one selected slot, the corresponding matched
slack increases strictly. Consequently the sorted matching-slack vector
strictly lexicographically improves.

## Proof

Fix agent \(i\), matched to bundle \(q=\pi(i)\). Condition (1) says the value
of her assigned bundle weakly increases. If her slot is not selected, its
value is unchanged.

For every competing selected bundle \(k\ne q\), agent \(i\) is not its
matched agent. Condition (2) therefore gives
\(v_i(h_k)\leq v_i(g_k)\). For additive valuations,

\[
\tau_i(S)=v_i(S)-\min_{g\in S}v_i(g)
\]

is the sum of the \(|S|-1\) largest singleton values. Replacing one singleton
by a weakly smaller value cannot increase this sum, so
\(\tau_i(Y'_k)\leq\tau_i(Y_k)\). Unselected competing bundles and the
remaining charity \(R\) are unchanged. Thus the left side of agent \(i\)'s
acceptance inequality weakly rises while every term on its right side weakly
falls, proving weak slack improvement.

If (1) is strict in slot \(q\), agent \(a_q\)'s assigned-bundle value rises
strictly and her right side does not rise, so her matched slack rises strictly.
The lexicographic conclusion follows from the charity lexicographic
bottleneck lemma. \(\square\)

## Receiver-edge polarity

The same calculation has a quantitative form that explains the dependency
walls. Replace \(g\in Y_q\) by \(h\), keep all other bundles and charity
fixed, and put

\[
d_i=v_i(h)-v_i(g),\qquad
\delta_i=\tau_i(Y_q-g+h)-\tau_i(Y_q).
\]

Because \(\tau_i\) is the sum of all but the smallest singleton value,
changing one coordinate by \(d_i\) gives

\[
\min\{0,d_i\}\leq\delta_i\leq\max\{0,d_i\}. \tag{3}
\]

Agent \(i\)'s acceptance-edge slack **to** bundle \(q\) changes by exactly
\(d_i/v_i(M)\): only the left side of that edge changes. Every edge from
\(i\) to another bundle changes in the opposite weak direction, by magnitude
at most \(|d_i|/v_i(M)\), because only the competing threshold
\(\tau_i(Y_q)\) can change on its right side.

Thus an external observer with the obstructing sign \(d_i>0\) loses slack on
its current off-target edge only because it gains strictly more slack toward
the modified target bundle. The wall is simultaneously a candidate
alternating-matching edge. This is the bridge between sign-dependency cycles
and the critical Hall cut: reroute the observer to the bundle whose change
hurt it, then continue from the receiver displaced by that rerouting.

## Extremal consequence

Select an EFX-with-charity state by the extremal pair
\((\Theta,\Lambda)\). Suppose an eligible fixed-charity-cardinality exchange
induces, for a \(\Lambda\)-optimal absorption candidate, a completed-bundle
exchange satisfying (1)--(2), with at least one strict matched-agent
comparison. If the state exchange preserves \(\Theta\), it contradicts
maximality of \(\Lambda\). If it increases \(\Theta\), it already contradicts
the first extremal coordinate.

Therefore a hypothetical blocked extremal state must obstruct every such
exchange in one of three explicit ways:

1. a matched receiver prefers its outgoing good;
2. an external observer also strictly prefers the incoming good; or
3. all matched-receiver comparisons are equal.

The second case is the useful dependency wall. It names an external observer
whose row has the opposite sign from the intended matched receiver. Chaining
these observer dependencies around a critical Hall cut is now the exact
remaining route to either a positive-total-gain transfer union or an
impossible strict sign cycle.

## Connection to charity/minimum exchanges

Swapping a charity good into one allocated bundle and then absorbing the
released minimum into a *different* host induces, at the completed-partition
level, precisely a two-bundle item exchange. A longer simultaneous
charity/minimum cycle induces a cyclic instance of the lemma. Reinserting the
released good into its original source reconstructs the old completion
candidate and gives equality, explaining why the new host must differ from
the source in every strict gradient step.

## Claim boundary

The lemma is cap-free and valid for arbitrary numbers of agents and goods.
It proves a sufficient exchange certificate and identifies exact failure
walls. It does not prove that every negative-signature critical Hall cut
contains such a certificate, so four-agent and general EFX remain open.

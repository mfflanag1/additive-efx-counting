# General owner-exchange plateau lemma

## Statement

Let \((X,P)\) be an EFX allocation with charity for positive-additive
agents, and fix the charity cardinality \(|P|\).  For a nonempty bundle
\(S\), write

\[
\tau_i(S)=v_i(S)-\min_{g\in S}v_i(g)
\]

and define the normalized owner-threshold potential

\[
\Theta(X,P)=\sum_i \frac{\tau_i(X_i)}{v_i(M)}.
\]

Suppose \((X,P)\) globally maximizes \(\Theta\) among all EFX-with-charity
states with the same charity cardinality.  Choose distinct owners
\(i_1,\ldots,i_k\), one good \(g_r\in X_{i_r}\) from each selected bundle,
and cyclically send \(g_r\) to owner \(i_{r+1}\), with indices modulo \(k\).
Assume every receiving owner weakly prefers her incoming good to her outgoing
good:

\[
v_{i_{r+1}}(g_r)\geq v_{i_{r+1}}(g_{r+1})
\qquad(r=1,\ldots,k).
\]

If the resulting state \((X',P)\) is again EFX with charity, then

\[
\Theta(X',P)=\Theta(X,P).
\]

In particular, every eligible mutually owner-improving two-good swap and
every eligible owner-Pareto exchange cycle stays on the global threshold
plateau.

Moreover, every *strict* comparison in such a plateau exchange has a rigid
minimum-slot normal form. If owner \(i\) releases \(g\), receives \(h\), and
\(v_i(h)>v_i(g)\), then:

1. \(g\) is the unique \(i\)-minimum of \(X_i\); and
2. \(v_i(h)\) is no larger than the \(i\)-minimum of \(X_i-g\).

Thus the incoming good becomes an owner minimum and the rest of the bundle is
unchanged. Every strict owner-Pareto plateau cycle is exactly a permutation of
minimum-slot tokens over fixed bundle cores.

## Proof

For additive valuations, \(\tau_i(S)\) is the sum of the \(|S|-1\) largest
singleton values in \(S\).  Replacing one coordinate of this multiset by a
weakly larger coordinate cannot decrease that sum.  Hence, for every owner
participating in the cycle,

\[
\tau_{i_r}(X'_{i_r})\geq \tau_{i_r}(X_{i_r}).
\]

Every other owner's bundle is unchanged, as is the charity set.  Therefore
\(\Theta(X',P)\geq\Theta(X,P)\).  The new state belongs to the same feasible
fixed-cardinality domain, while \((X,P)\) is a global maximizer.  Strict
increase is impossible, so equality holds.

For the final statement, fix a participating owner \(i\) with
\(v_i(h)>v_i(g)\). We have already shown that every owner's threshold change
is nonnegative. Their normalized sum is zero, so each individual change is
zero. If \(g\) were not the unique minimum, replacing it by a strictly more
valuable good would strictly increase the sum of the \(|X_i|-1\) largest
singleton values. Hence \(g\) is the unique minimum. Let \(s\) be the minimum
value in \(X_i-g\). If \(v_i(h)>s\), the new \(|X_i|-1\) largest-value sum
would exceed the old one by \(v_i(h)-s>0\). Therefore
\(v_i(h)\leq s\), proving the minimum-slot normal form. \(\square\)

## Why this widens the live route

The charity/minimum exchange lemma moves a good between charity and one
allocated bundle. This lemma supplies an independent family of plateau
moves entirely inside the allocated partition. Its equality characterization
also explains why the fixed-core token orbit is not an arbitrary
computational restriction: every strictly owner-improving Pareto exchange at
a true global maximum necessarily lies in that orbit. It is the exact
owner-threshold analogue of the pairwise swap-optimization technique used in
the constructive four-agent EF2X algorithm: first eliminate mutually
beneficial item inversions between owners, then analyze only the
swap-saturated obstruction.

The unified absorption target can therefore be strengthened without changing
its extremal setup:

> Starting from a \(\Theta\)-maximal state with negative absorption margin,
> use eligible charity/minimum exchanges **and** eligible owner-Pareto
> exchange cycles to reach a state with strictly larger absorption margin.

This statement is still unproved.  The lemma only proves that all such
eligible moves remain on the first extremal plateau; it does not prove that a
useful move exists or that EFX-with-charity eligibility is preserved.

## Claim boundary

The plateau lemma is cap-free and valid for arbitrary numbers of agents,
goods, and charity goods under positive additive valuations.  It is a local
structural lemma, not a proof of four-agent or general EFX existence.

## Related primary source

The swap-optimization inspiration is Section 3.4 of Ashuri, Gkatzelis, and
Sgouritsa, *EF2X Exists for Four Agents*, arXiv:2412.00254.  Their feasibility
invariant is different; the argument above is specific to the normalized
owner-threshold plateau used here.

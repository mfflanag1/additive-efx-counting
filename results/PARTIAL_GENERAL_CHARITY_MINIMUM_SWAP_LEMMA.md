# Charity/minimum exchange lemma

## Setup

Let \((X,P)\) be an EFX allocation with charity for positive additive
valuations:

\[
v_i(X_i)\geq v_i(P)\qquad(i\in N).
\]

Define

\[
\tau_i(X_i)=v_i(X_i)-\min_{g\in X_i}v_i(g),
\qquad
\Theta(X,P)=\sum_i\frac{\tau_i(X_i)}{v_i(M)}.
\]

Choose a charity good \(f\in P\), an owner \(q\), and an owner-minimum good
\(g\in X_q\). Exchange them:

\[
X'_q=X_q-g+f,\qquad X'_i=X_i\ (i\ne q),\qquad
P'=P-f+g.
\]

## Plateau theorem

If \((X,P)\) globally maximizes \(\Theta\) among EFX-with-charity states with
\(|P|\) goods, and \((X',P')\) is again such a state, then

\[
\Theta(X',P')=\Theta(X,P)
\]

and \(f\) is an owner-minimum good of \(X'_q\).

The proof is identical to the one-floater case. Put \(R=X_q-g\). Then

\[
\tau_q(X'_q)-\tau_q(X_q)
=v_q(f)-\min\!\left\{v_q(f),\min_{x\in R}v_q(x)\right\}\geq0,
\]

and all other threshold terms are unchanged. Eligibility plus global
maximality forces equality.

## Exact obstruction signs

If the exchange is not eligible, at least one of the following walls occurs.

### Incoming-target wall

For an external agent \(i\ne q\),

\[
v_i(X_i)<\tau_i(X_q-g+f).
\]

Old EFX gives \(v_i(X_i)\geq\tau_i(X_q-g+g)\), so monotonicity of the
fixed-core threshold function forces

\[
v_i(f)>v_i(g). \tag{T}
\]

There is a sharper exact form. Put

\[
r_{iq}=\min_{x\in X_q-g}v_i(x),
\]

with \(r_{iq}=+\infty\) when \(X_q=\{g\}\). Then

\[
\tau_i(X_q-g+f)-\tau_i(X_q)
=\max\{0,v_i(f)-r_{iq}\}
 -\max\{0,v_i(g)-r_{iq}\}. \tag{T1}
\]

Hence an incoming-target wall actually forces

\[
v_i(f)>\max\{v_i(g),r_{iq}\}. \tag{T2}
\]

In particular, this wall is impossible when \(X_q\) is a singleton.

### External charity wall

For an external agent \(i\ne q\),

\[
v_i(X_i)<v_i(P-f+g).
\]

Old charity dominance gives \(v_i(X_i)\geq v_i(P)\), and subtraction yields

\[
v_i(g)>v_i(f). \tag{C}
\]

### Source-owner EFX shortfall

For \(q\) and some \(j\ne q\),

\[
v_q(X_q-g+f)<\tau_q(X_j).
\]

Old EFX gives \(\tau_q(X_j)\leq v_q(X_q)\), hence

\[
v_q(g)>v_q(f). \tag{S}
\]

### Source-owner charity wall

For \(q\),

\[
v_q(X_q-g+f)<v_q(P-f+g).
\]

Writing \(A=v_q(X_q-g)\) and \(C=v_q(P-f)\), old charity dominance and the
new failure give

\[
A+v_q(g)\geq C+v_q(f),
\qquad
A+v_q(f)<C+v_q(g).
\]

These inequalities are jointly possible only if

\[
v_q(g)>v_q(f), \tag{SC}
\]

because otherwise the first lower bound on \(A-C\) is at least the strict
upper bound supplied by the second.

## Unified wall dichotomy

Every failure therefore has one of two opposite row-wise signs:

\[
\begin{array}{c|c}
\text{wall type} & \text{forced comparison}\\ \hline
\text{incoming target} & v_i(f)>v_i(g)\\
\text{external charity} & v_i(g)>v_i(f)\\
\text{source EFX or charity} & v_q(g)>v_q(f).
\end{array}
\]

When \(P=\{f\}\) and \(X_q\) is nonsingleton, the new floater \(g\) is
automatically unenvied by old EFX, so the external-charity wall disappears.
The lemma then specializes exactly to the one-floater obstruction lemma.

## Pareto-sensitive fixed-cardinality dependency corollary

Among the global \(\Theta\)-maxima at a fixed charity cardinality, additionally
maximize the owner-utility vector in a fixed lexicographic order. If owner
\(q\) strictly prefers a chosen charity good \(f\) to her own minimum \(g\),
then the \(f/g\) swap is ineligible. Otherwise the plateau theorem would keep
\(\Theta\) fixed while strictly improving only owner \(q\)'s utility.

The two source-owner wall types are impossible because both force
\(v_q(g)>v_q(f)\). Every failed improving swap therefore produces, in some
other agent's row, exactly one of two opposite signs:

\[
\begin{array}{c|c}
\text{incoming-target wall}&v_i(f)>v_i(g),\\
\text{external-charity wall}&v_i(g)>v_i(f).
\end{array}
\]

This is the arbitrary-charity signed dependency supplied by the revised
extremum. The positive target sign has the sharper top-two form (T2).

## Pareto-sensitive one-floater dependency corollary

Among the global \(\Theta\)-maxima, additionally maximize the owner-utility
vector in a fixed lexicographic order. Let \(P=\{f\}\), let \(X_q\) be
nonsingleton, and let \(g\) be a \(q\)-minimum satisfying

\[
v_q(f)>v_q(g). \tag{P}
\]

Then the \(f/g\) swap is ineligible, and there exists an external agent
\(i\ne q\) such that

\[
v_i(X_i)<\tau_i(X_q-g+f)
\quad\text{and}\quad
v_i(f)>\max\{v_i(g),\min_{x\in X_q-g}v_i(x)\}. \tag{D}
\]

Indeed, if the swap were eligible, the plateau theorem would preserve
\(\Theta\) while (P) strictly improved only owner \(q\)'s utility,
contradicting the secondary extremum. Ineligibility must therefore have one
of the wall types above. Nonsingleton one-floater swaps have no external
charity wall. Both source-owner walls force \(v_q(g)>v_q(f)\), contradicting
(P). Only an incoming-target wall remains, and (T2) gives its sharpened
strict sign.

Thus every improving owner-minimum swap at the selected extremum points to a
different blocking agent with the same row-wise orientation between \(f\)
and the released minimum. For singleton \(X_q\), an external charity wall is
an additional residual branch.

## Incoming wall-to-champion corollary

Every incoming-target wall for the attempted \(f/g\) swap produces a
generalized champion edge into source bundle \(q\) with label
\(\{f\}\mid\{g\}\). Put

\[
T=(X_q-g)+f.
\]

The wall says that some agent strongly envies \(T\), so some proper subset of
\(T\) is envied. Among all subsets of \(T\) envied by at least one agent,
choose an inclusion-minimal set \(A\), and choose an agent \(a\) who envies
it. No agent strongly envies \(A\), since deleting the witnessing good would
give a smaller envied subset. Hence \(a\) is most envious of \(T\), which is
exactly the generalized edge

\[
a\mathrel{\smash{\xrightarrow{\{f\}\mid\{g\}}}}q.
\]

The edge releases \(g\), together with any additional discard
\(T-A\). Therefore every positive one-floater dependency wall is not merely a
sign: it supplies an EFX-preserving generalized-champion construction step.
The remaining difficulty is to reallocate all additional discarded goods
while preserving charity cardinality and nonnegative total threshold change.

## Singleton-chain elimination lemma

The singleton exception in the one-floater dependency corollary cannot cycle
indefinitely. Work at a \((\Theta,U)\)-maximal one-floater state. Suppose
\(X_{q_0}=\{g_0\}\) and

\[
v_{q_0}(f)>v_{q_0}(g_0).
\]

The direct swap has unchanged owner threshold and improves \(q_0\), so it is
ineligible. An incoming-target wall is impossible because the replacement
bundle \(\{f\}\) has threshold zero, and the source walls have the wrong
strict sign. Hence some agent envies the proposed charity singleton \(g_0\).

If that agent also owns a singleton \(X_{q_1}=\{g_1\}\), then
\(v_{q_1}(g_0)>v_{q_1}(g_1)\). Continue in this way. After distinct singleton
owners \(q_0,\ldots,q_k\) have been found, consider the prefix rotation

\[
Y_{q_0}=\{f\},\qquad
Y_{q_r}=\{g_{r-1}\}\ (1\le r\le k),
\qquad P_Y=\{g_k\},
\]

with all other bundles unchanged. Every changed owner strictly improves, all
changed target bundles are singletons, and all unchanged EFX comparisons
remain valid. Thus \(Y\) is EFX; only dominance of its charity good can fail.

No charity blocker can be an earlier chain owner. If \(q_j\) blocked
\(g_k\), then rotating the original singleton goods on the subcycle
\(q_j,q_{j+1},\ldots,q_k\) would strictly improve every owner on that cycle,
preserve the original charity \(f\), preserve every owner threshold at zero,
and remain EFX with charity. This contradicts the secondary utility maximum.
Therefore every singleton blocker is new. Since there are finitely many
agents, the process either produces an eligible prefix rotation--again a
contradiction--or reaches an agent \(i\) with a nonsingleton bundle and

\[
v_i(g_k)>v_i(X_i). \tag{SC1}
\]

In the latter case let \(x\) be an \(i\)-minimum and extend the prefix by

\[
Z_i=X_i-x+g_k,qquad P_Z=\{x\}.
\]

All prefix owners still improve, and (SC1) makes owner \(i\) improve. More
strongly, if \(r=\min_{y\in X_i-x}v_i(y)\), then

\[
\tau_i(Z_i)-\tau_i(X_i)=v_i(g_k)-r>0. \tag{SC2}
\]

Hence \(\Theta(Z)>\Theta(X)\). The new charity good \(x\) is automatically
dominated: for every other agent \(a\), old EFX and nonsingularity give
\(v_a(X_a)\ge\tau_a(X_i)\ge v_a(x)\), while every prefix owner only became
better off; owner \(i\)'s new utility exceeds \(v_i(g_k)>v_i(x)\). All EFX
comparisons are unchanged except comparisons against
\(Z_i\). Consequently either \(Z\) is eligible, contradicting primary
\(\Theta\)-maximality, or an incoming-target wall strongly envies \(Z_i\).
In the latter case the wall-to-champion corollary produces a generalized
\(\{g_k\}\mid\{x\}\)-champion edge into \(i\), using the good released by the
singleton prefix and releasing \(x\) plus its additional discard.

Thus every improving one-floater minimum-swap obstruction, including a
singleton source, terminates in a positive incoming-target wall and a
generalized champion edge. What remains unproved is that the resulting
champion/dependency edges can be combined into one charity-cardinality-
preserving component with nonnegative total threshold change.

## Breakthrough target exposed by the lemma

Starting from the known EFX-with-charity allocation, choose a global
\(\Theta\)-maximum at fixed charity cardinality and then maximize an exact
Hall-completion margin. To reduce the charity by one, it would suffice to
prove:

> If no charity good can be absorbed, the sign-labeled walls of all
> charity/minimum exchanges contain a simultaneous exchange cycle that is
> EFX-with-charity eligible and either improves \(\Theta\) or strictly
> improves the Hall-completion margin.

The plateau theorem would exclude the first outcome at a global maximum;
finiteness would exclude endless strict Hall-margin improvement. This target
specializes to the four-agent one-floater gate and scales to arbitrary
\(n\) and \(|P|<n\).

## Claim boundary

The exchange and wall classification are proved. The simultaneous-cycle
existence statement is not proved. Accordingly this document does not claim
four-agent or general additive EFX.

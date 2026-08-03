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
v_i(f)>v_i(g). \tag{D}
\]

Indeed, if the swap were eligible, the plateau theorem would preserve
\(\Theta\) while (P) strictly improved only owner \(q\)'s utility,
contradicting the secondary extremum. Ineligibility must therefore have one
of the wall types above. Nonsingleton one-floater swaps have no external
charity wall. Both source-owner walls force \(v_q(g)>v_q(f)\), contradicting
(P). Only an incoming-target wall remains, and (T) gives its strict sign.

Thus every improving owner-minimum swap at the selected extremum points to a
different blocking agent with the same row-wise orientation between \(f\)
and the released minimum. For singleton \(X_q\), an external charity wall is
an additional residual branch.

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

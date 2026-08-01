# Small-Integer Counterexample Bound

**Status:** proved analytic lemma. This makes every fixed \((n,m)\)
additive-EFX existence question decidable by a finite integer search. It does
not bound the number of goods in a smallest counterexample and therefore does
not resolve the general conjecture.

## Theorem

Fix \(n\ge 2\) agents and \(m\ge 2\) goods. If there is a nonnegative
additive valuation profile with no complete EFX allocation, then there is
such a profile with strictly positive integer item values satisfying

\[
1\le v_i(g)\le K_m
\quad\text{for every agent \(i\) and good \(g\),}
\qquad
K_m=\left\lfloor m^{m/2}\right\rfloor .
\]

The bound is independent of the number of agents because each agent's
valuation row may be scaled independently without changing any EFX
comparison.

For \(m\ge3\), the bounded representative may also be required to preserve every strict
within-row item ranking of a generic perturbation of the original profile.
Thus a proof may split the bounded search into strict ranking or favorite
cells without losing completeness.

In particular,

| goods \(m\) | sufficient integer cap \(K_m\) |
|---:|---:|
| 8 | 4,096 |
| 9 | 19,683 |
| 10 | 100,000 |

Thus a counterexample at \((4,9)\), if one exists, has a positive-integer
representative with every entry at most 19,683.

## Proof

Let \(V\) be a nonnegative additive counterexample. For every complete
allocation \(A=(A_1,\ldots,A_n)\), choose one EFX violation: an observer
\(i=i(A)\), a target \(j=j(A)\ne i\), and a good \(r=r(A)\in A_j\) such
that

\[
\sum_{g\in A_j\setminus\{r\}}v_i(g)
-
\sum_{g\in A_i}v_i(g)>0. \tag{1}
\]

There are finitely many complete allocations, so all chosen inequalities
remain strict after a sufficiently small positive perturbation of every
item value. We may therefore assume that \(V\) is strictly positive.

Fix an agent \(i\). If desired, first choose a strict ranking of its item
values after the positive generic perturbation and include all adjacent
ranking differences among the strict linear forms below. Scale row \(i\) so
that its item values
\(x=(x_1,\ldots,x_m)\) sum to one. Let \(\mathcal W_i\) be the chosen
witness inequalities (1) whose observer is \(i\), together with those
optional ranking inequalities, and write each of them as a linear form
\(L(x)>0\). Consider the linear program

\[
\begin{aligned}
\text{maximize}\quad &\delta\\
\text{subject to}\quad
&\sum_{g=1}^m x_g=1,\\
&x_g\ge\delta &&(g=1,\ldots,m),\\
&L(x)\ge\delta &&(L\in\mathcal W_i),\\
&\delta\ge0.
\end{aligned} \tag{2}
\]

The normalized original row makes (2) feasible with \(\delta>0\). Its
feasible region is compact, so it has an optimal vertex
\((x^\star,\delta^\star)\), and \(\delta^\star>0\).

There are \(m+1\) variables. An optimal vertex is determined by the
normalization equality and \(m\) linearly independent active inequalities.
Let \(B\) be the resulting nonsingular integer \((m+1)\times(m+1)\)
coefficient matrix. Every row of \(B\) has Euclidean norm at most
\(\sqrt m\):

- the normalization row has \(m\) coefficients equal to one;
- an item-floor row has only the coefficients of \(x_g\) and \(\delta\);
- a witness row contains coefficients in \(\{-1,0,1\}\) on two disjoint
  allocation bundles, with one target good removed, plus the coefficient of
  \(\delta\), so it has at most \(m\) nonzero entries; and
- when \(m\ge3\), a ranking row has the two compared item coefficients and
  the coefficient of \(\delta\); and
- the row for \(\delta\ge0\) has one nonzero entry.

The right-hand side is zero except for the normalization equality, whose
right-hand side is one. By Cramer's rule, the numerator \(N_g\) of
\(x_g^\star\) is the determinant obtained by replacing the \(x_g\) column
of \(B\) with this right-hand side. Expanding along that replacement column
leaves an \(m\times m\) determinant whose rows still have norm at most
\(\sqrt m\). Hadamard's inequality therefore gives

\[
|N_g|\le(\sqrt m)^m=m^{m/2}. \tag{3}
\]

All coefficients are integral, so the common denominator is
\(D=|\det B|\). Since \(x_g^\star\ge\delta^\star>0\), orienting the signs
consistently gives positive integers \(N_g\). Multiplying row \(i\) by
\(D\) produces the positive-integer row
\((N_1,\ldots,N_m)\). Every witness slack is a positive integer because it
was at least \(\delta^\star>0\), and (3) gives

\[
1\le N_g\le \left\lfloor m^{m/2}\right\rfloor.
\]

Repeat this construction independently for every agent. Independent
positive scaling of valuation rows preserves all EFX inequalities. Every
complete allocation still violates its originally selected inequality, so
the resulting bounded positive-integer profile has no complete EFX
allocation. \(\square\)

## Consequences

1. **Fixed-cell decidability.** Enumerating the finite box
   \(\{1,\ldots,K_m\}^{n\times m}\) and checking every allocation is a
   complete decision procedure. The raw enumeration is enormous, but it is
   unconditional.
2. **Sound bounded encodings.** A SAT, SMT, or MILP proof covering the full
   cap \(K_m\) proves existence for that fixed \((n,m)\); it is not merely a
   “no small counterexample” result.
3. **What remains unbounded.** The theorem gives no universal cap on \(m\).
   Resolving all additive instances still requires a structural theorem or
   a counterexample at some finite \(m\).

## Relation to the current campaign

The 2026 monotone-valuation disproof treats subset values as independent
finite variables. Additivity collapses those variables to item weights but
introduces linear-arithmetic consistency. The theorem above supplies the
missing finiteness bridge: for each fixed number of goods, the additive
search may also be reduced to a finite integer domain, with an explicit cap.

The immediate computational target is not literal enumeration up to 19,683.
It is to exploit the cap in bit-vector or pseudo-Boolean encodings, symmetry
breaking, and proof-producing CEGAR for the first open \(4\times9\) cell.

# Three-rival weighted-cycle exclusion

## Scope

This is an exact exclusion lemma for the complete comparison cell containing
the known Pareto-maximal $4\times9$ radius-one Hall obstruction. It is not
a proof of the global normalized-utilitarian selector and is not cap-free in
the number of goods.

Normalize every valuation row so $v_i(M)=1$, and let

\[
X=(\{6,7\},\{1,2,3\},\{0,4\},\{5\});f=8.
\]

The cell retains 992 eligible one-floater states. If $X$ were a global
maximizer of normalized-utilitarian potential, it would in particular weakly
beat these three eligible rivals:

\[
\begin{aligned}
Y^0&=(\{4,7\},\{1,2,3\},\{6,8\},\{5\});f=0,\\
Y^1&=(\{7,8\},\{4,6\},\{0,3\},\{2,5\});f=1,\\
Y^2&=(\{7,8\},\{3,4\},\{0,6\},\{2,5\});f=1.
\end{aligned}
\]

Those three maximality inequalities are incompatible with 20 comparison
walls from the cell.

## Exact weighted contradiction

The deletion-irreducible core contains:

- two row-normalization equalities;
- two strict-positivity inequalities;
- five weak comparisons from eligible states;
- thirteen strict comparisons witnessing ineligible states; and
- the three maximality inequalities for $Y^0,Y^1,Y^2$.

The rational Farkas certificate is recorded term-by-term in
[`partial_hall_utilitarian_frozen_cell_pareto_farkas.json`](partial_hall_utilitarian_frozen_cell_pareto_farkas.json).
Multiplying every coefficient by 200 gives the following integer multiplier
blocks, in artifact order:

\[
\begin{array}{c|l}
\text{block}&\text{multipliers}\\ \hline
\text{row equalities}&-3,\ 3\\
\text{strict positivity}&8,\ 12\\
\text{eligible comparisons}&8,\ 4,\ 4,\ 18,\ 6\\
\text{ineligible witnesses}&5,\ 8,\ 3,\ 24,\ 3,\ 14,\ 20,\ 20,\ 4,\ 21,\ 31,\ 24,\ 3\\
\text{maximality}&40,\ 4,\ 8
\end{array}
\]

Every valuation-variable coefficient and the constant term cancel exactly.
All inequality multipliers are nonnegative, while the multipliers on strict
inequalities sum to 200. The weighted assumptions therefore say
$0>0$, a contradiction.

Hence every valuation profile in this complete comparison cell has at least
one of the following: a changed eligibility/Hall wall, or an eligible rival
among $Y^0,Y^1,Y^2$ with strictly larger normalized-utilitarian potential.
In particular, the known Pareto-maximal obstruction cannot itself be a
normalized-utilitarian maximizer.

## Verification and interpretation

- [`partial_hall_utilitarian_frozen_cell_pareto_core.json`](partial_hall_utilitarian_frozen_cell_pareto_core.json)
  records the deletion-irreducible 25-constraint core.
- [`partial_hall_utilitarian_frozen_cell_pareto_core.smt2`](partial_hall_utilitarian_frozen_cell_pareto_core.smt2)
  has SHA-256
  `c947f990fa784e33ba46ad1b23ab05c3d89a7476161a51f965c297e9b84e8300`.
- Its syntax-normalized cvc5 replay has SHA-256
  `e9ea1443492f11cdc7556259b3a7e53e9f6a604b99f01af1a2ccfb6df43aa4a8`.
  Z3 and cvc5 independently return `UNSAT`.

This identifies a third analytic mechanism: some Hall cells are excluded not
by one Pareto conversion, but by a normalized-potential cycle involving
several eligible rivals. The remaining fixed-cell proof problem is to cover
all comparison cells by the two cap-free conversions, weighted cycles of
this kind, or explicit complete allocations.

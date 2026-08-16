# Six-wall replacement lemma

## Statement

Let $p,q,r,s,t,u,w,z,f$ be distinct goods and let $v$ be a
nonnegative additive valuation. Suppose

\[
\begin{aligned}
v(r+s)&\ge v(p),\\
v(u)&\ge v(r+z+f),\\
v(p+q)&<v(r+z+f),\\
v(u)&<v(w+f),\\
v(w+s)&<v(p+f),\\
v(r+t+f)&<v(p).
\end{aligned}
\]

Then $v(q)<v(f)$.

Consequently, if an eligible partial EFX state $X$ assigns an agent a
bundle containing $q$, leaves $f$ unallocated, and the state obtained by
replacing $q$ with $f$ is also eligible, the replacement state strictly
improves that agent and leaves every other bundle unchanged. It therefore
Pareto-dominates $X$.

## Proof

Write the value of each good using the same lowercase letter. The first,
fifth, and sixth comparisons imply

\[
s\ge p-r>f+t,
\qquad
w+s<p+f,
\qquad\text{hence}\qquad
w<f+r.
\]

The second and fourth comparisons then give

\[
f+z+r\le u<w+f<2f+r,
\qquad\text{so}\qquad z<f.
\]

Finally,

\[
p+q<r+z+f
\quad\text{and}\quad
p>r+t+f
\]

imply $q<z-t\le z<f$. Thus $v(q)<v(f)$.

## Concrete cell and verification

The second frozen obstruction uses

\[
(p,q,r,s,t,u,w,z,f)=(0,1,2,3,4,5,6,7,8)
\]

for agent 1. Its improving eligible state changes
$\{1,2,3\}$ to $\{2,3,8\}$ and leaves good 1 unallocated. The exact
source is
[`partial_hall_utilitarian_frozen_cell_seed23_core.json`](partial_hall_utilitarian_frozen_cell_seed23_core.json).

The algebraic negation is
[`partial_hall_six_wall_algebra.smt2`](partial_hall_six_wall_algebra.smt2).
Z3 and cvc5 independently return `UNSAT`. As with the two-wall lemma, the
remaining global task is to connect failures of these six walls to explicit
completion moves or to additional conversion types.

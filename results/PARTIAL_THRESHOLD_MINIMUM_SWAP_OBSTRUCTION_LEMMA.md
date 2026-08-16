# Owner-minimum floater-swap obstruction lemma

## Statement

Let \((X,f)\) be an eligible one-floater EFX allocation for positive-additive
agents.  Fix an owner \(s\) whose bundle is nonsingleton, choose any
owner-minimum good

\[
g\in\arg\min_{x\in X_s}v_s(x),
\]

and form \((Y,g)\) by setting

\[
Y_s=X_s-\{g\}+\{f\},
\qquad Y_i=X_i\quad(i\ne s).
\]

Then every agent weakly prefers her bundle in \(Y\) to the new floater
\(g\).  Moreover, \(Y\) is EFX unless at least one of the following two
cross-wall certificates occurs:

1. **incoming-target wall:** some observer \(i\ne s\) satisfies
   \[
   v_i(X_i)<\tau_i(Y_s);
   \]
2. **owner-shortfall wall:** owner \(s\) and some target \(j\ne s\) satisfy
   \[
   v_s(Y_s)<\tau_s(X_j).
   \]

Every incoming-target wall forces

\[
v_i(f)>v_i(g)
\quad\text{and}\quad
v_i(f)>min_{x\in X_s\setminus\{g\}}v_i(x).
\]

Every owner-shortfall wall forces

\[
v_s(f)<v_s(g).
\]

The statement is cap-free in agents, goods, and valuation magnitudes.

## Proof

Write \(R=X_s\setminus\{g\}\), which is nonempty.

First check the new floater.  For an observer \(i\ne s\), base EFX gives

\[
v_i(X_i)\ge\tau_i(X_s).
\]

For every good \(x\in X_s\), nonsingleton additivity gives
\(\tau_i(X_s)\ge v_i(x)\): after removing an \(i\)-minimum good, the
residual contains either \(x\) or another good worth at least \(x\).
In particular, \(v_i(X_i)\ge v_i(g)\).  For owner \(s\), positivity and
the owner-minimum property imply

\[
v_s(Y_s)=v_s(R)+v_s(f)>v_s(g),
\]

because \(R\) contains a good worth at least \(v_s(g)\).  Thus no agent
envies the new floater.

All EFX comparisons between two unchanged bundles are inherited from \(X\).
The only remaining comparisons are from an unchanged observer \(i\ne s\)
to changed target \(Y_s\), and from changed owner \(s\) to an unchanged
target \(X_j\).  Their failures are exactly certificates 1 and 2.

For the sign consequences, put

\[
r_i=\min_{x\in R}v_i(x).
\]

The replacement changes observer \(i\)'s target threshold by

\[
\tau_i(Y_s)-\tau_i(X_s)
=\max\{v_i(f)-r_i,0\}-\max\{v_i(g)-r_i,0\}.
\]

An incoming-target wall, together with base EFX, says

\[
\tau_i(Y_s)>v_i(X_i)\ge\tau_i(X_s),
\]

so the displayed difference is positive.  This is possible only when
\(v_i(f)>r_i\) and \(v_i(f)>v_i(g)\).

Finally, an owner-shortfall wall and base EFX give

\[
v_s(X_s)-v_s(g)+v_s(f)
=v_s(Y_s)
<\tau_s(X_j)
\le v_s(X_s).
\]

Cancellation yields \(v_s(f)<v_s(g)\).

## Interface with the breakthrough gate

At a global threshold maximum, the
`PARTIAL_THRESHOLD_MAXIMUM_SWAP_REDUCTION_LEMMA.md` shows that any swap not
blocked by these walls stays on the same threshold plateau.  Therefore the
exact Hall-gradient lemma has only one substantive task: use the direct Hall
obstruction (or the owner-minimum pair trap) to select a source whose two
wall families are absent and whose swap improves the exact completion margin.

For four agents with all four bundles nonsingleton, universal failure of the
four owner-minimum swaps yields a finite dependency digraph of incoming-target
and owner-shortfall walls.  Turning a directed cycle in that graph into a
strict Hall-margin improvement or an impossible weighted inequality is the
remaining analytic conversion step.  No such cycle contradiction is claimed
here.

Singleton source bundles require a separate branch: swapping their only good
reverses floater dominance unless owner and floater tie.  The cap-free
owner-minimum pair-extraction theorem already isolates singleton patterns,
so a complete proof must combine this lemma with that existing case split.

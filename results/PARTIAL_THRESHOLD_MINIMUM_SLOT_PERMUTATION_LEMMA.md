# Minimum-slot permutation plateau lemma

## Proved cap-free lemma

Let \((X,f)\) be an eligible one-floater EFX allocation for positive-additive
agents, globally maximizing

\[
\Theta(X,f)=\sum_i\frac{\tau_i(X_i)}{v_i(M)}.
\]

For every owner \(i\), select one owner-minimum good

\[
g_i\in\arg\min_{g\in X_i}v_i(g)
\]

and write \(R_i=X_i-\{g_i\}\).  Regard

\[
\{g_i:i\in N\}\cup\{f\}
\]

as \(n+1\) **parking tokens**, assigned initially to the \(n\) owner slots
and one floater slot.

Permute those tokens arbitrarily among the same \(n+1\) slots.  If owner
\(i\) receives token \(q_i\), set

\[
Y_i=R_i\cup\{q_i\},
\]

and leave the token assigned to the floater slot unallocated.  If the
resulting state \(Y\) is eligible, then

\[
\Theta(Y)=\Theta(X).
\]

Moreover, whenever \(R_i\ne\varnothing\), its incoming token is an owner-
minimum good in the new bundle:

\[
v_i(q_i)\le\min_{x\in R_i}v_i(x).
\]

The result holds for arbitrary numbers of agents and goods, tied minima, and
permutations with any number of disjoint cycles.  Singleton bundles cause no
exception: their core is empty and every singleton replacement has threshold
zero.

## Proof

Because \(g_i\) is owner-minimum,

\[
\tau_i(X_i)=v_i(R_i).
\]

For any incoming token \(q_i\),

\[
\tau_i(R_i\cup\{q_i\})
=v_i(R_i)+v_i(q_i)
-\min\bigl(v_i(q_i),\min_{x\in R_i}v_i(x)\bigr)
\ge v_i(R_i),
\]

with both sides zero when \(R_i=\varnothing\).  Thus every normalized owner
threshold weakly increases, so \(\Theta(Y)\ge\Theta(X)\).  Eligibility puts
\(Y\) in the domain on which \(X\) is globally maximal, forcing equality.
Since every summand's change was nonnegative, every owner term is individually
equal.  For nonempty \(R_i\), equality in the display is equivalent to
\(v_i(q_i)\le\min_{x\in R_i}v_i(x)\), proving the minimum-slot conclusion.
\(\square\)

## Consequences for the Hall-gradient program

The earlier owner-minimum floater-swap lemma is the transposition between one
owner slot and the floater slot.  The present result also permits:

- a transposition of owner-minimum goods between two owner slots;
- a cycle through several owner slots with the floater unchanged; and
- an augmenting cycle through the floater and any number of owners.

Therefore the correct plateau object is the finite permutation graph of
minimum-slot tokens, not merely the radius-one floater-swap graph.  If every
single-token exchange is blocked by an EFX wall, the wall dependencies can be
followed until a directed cycle appears; applying the entire token cycle at
once is automatically threshold-nondecreasing, and if eligible it remains on
the global maximum plateau.

The missing theorem is now an eligibility-and-Hall statement: in the
four-agent critical-cut branches, show that the wall-dependency graph contains
a token cycle whose simultaneous permutation is eligible and whose completion
strictly augments the bottleneck Hall cut.  This lemma supplies plateau
preservation but does not prove that such a cycle exists.


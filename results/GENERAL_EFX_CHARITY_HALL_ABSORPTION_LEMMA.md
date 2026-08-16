# Charity-good Hall absorption lemma

## Exact equivalence

Let \(X=(X_1,\ldots,X_n;C)\) be an EFX allocation with charity set \(C\),
and suppose every agent weakly prefers her assigned bundle to the entire
charity set:

\[
v_i(X_i)\ge v_i(C)\qquad(i\in N).
\]

Choose a charity good \(f\in C\) and a host label \(h\).  Define the new
bundle partition

\[
B_h=X_h\cup\{f\},
\qquad B_j=X_j\quad(j\ne h),
\]

and remaining charity \(C'=C\setminus\{f\}\).  Build a bipartite graph from
agents to bundle labels, putting edge \(i\sim j\) exactly when both

\[
v_i(B_j)\ge\max_{k\ne j}\tau_i(B_k)
\tag{EFX feasibility}
\]

and

\[
v_i(B_j)\ge v_i(C')
\tag{charity dominance}
\]

hold.  Then the partition \(B\), together with charity \(C'\), supports an
EFX allocation in which no agent envies the remaining charity if and only
if this graph has a perfect matching.

The equivalence holds for arbitrary additive valuations, numbers of agents,
goods, and charity-set sizes.

## Proof

If the graph has a perfect matching, assign each agent her matched bundle.
The first edge condition gives every EFX comparison from that agent to every
other bundle, while the second gives her comparison to \(C'\).  Conversely,
any assignment of these bundles that is EFX and dominates \(C'\) pairs each
agent with a distinct label satisfying both edge conditions, hence is a
perfect matching.  Hall's theorem gives the equivalent deficient-set form.

## Iterative consequence

Suppose a class of instances has an EFX-with-charity allocation satisfying
the displayed charity-dominance condition, and suppose the following
absorption statement holds whenever its charity is nonempty:

> Some \(f\in C\) and host \(h\) make the augmented feasibility graph above
> admit a perfect matching.

Apply the matching, replace \(C\) by \(C-\{f\}\), and repeat.  Charity size
strictly decreases, while the hypotheses are preserved by the two edge
conditions.  After \(|C|\) steps the charity is empty and the allocation is
complete EFX.

Thus this absorption statement is sufficient to prove general additive EFX.
It is not proved here.

## Relation to the four-agent threshold route

When \(C=\{f\}\), the remaining charity is empty and the charity-dominance
edge condition is automatic.  The graph is exactly the direct-completion
graph used by the threshold--Hall program.  Therefore the four-agent theorem
is the singleton-charity base case of this arbitrary-\(n\) absorption
framework.

For \(|C|>1\), owner-minimum floater swaps do not automatically preserve the
charity condition: replacing absorbed \(f\) by a released good \(g\) changes
the charity from \(C\) to \(C-\{f\}+\{g\}\), which some observer may value
more.  This is the first genuine obstruction to lifting the threshold-plateau
proof verbatim.  A general proof needs either:

1. a move that absorbs \(f\) without releasing another good; or
2. a potential and exchange rule that makes the whole charity set decrease
   for every observer while preserving EFX.

The lemma isolates the exact matching target but does not establish either
mechanism.  General additive EFX remains unresolved.

# Bottleneck Hall-cut normal form

## Theorem

Let \(L\) and \(R\) be sets of \(n\) agents and bundles, and attach a real
score \(s_{ij}\) to every pair \((i,j)\in L\times R\). Define

\[
\beta=\max_{\pi:L\to R\ {\rm bijective}}\ \min_{i\in L}s_{i,\pi(i)}.
\]

Let \(G_{\geq}\) contain the edges with \(s_{ij}\geq\beta\), and let
\(G_{>}\) contain the edges with \(s_{ij}>\beta\). Then \(G_{\geq}\) has a
perfect matching and \(G_{>}\) does not.

If \(S\subseteq L\) is an inclusion-minimal Hall-deficient set in \(G_{>}\)
and \(k=|S|\), then

\[
|N_{G_{>}}(S)|=k-1. \tag{1}
\]

Moreover:

1. for every \(i\in S\), the other \(k-1\) agents \(S\setminus\{i\}\)
   have a strict matching into \(N_{G_{>}}(S)\);
2. every perfect matching of \(G_{\geq}\) uses at least one edge from \(S\)
   to \(R\setminus N_{G_{>}}(S)\), and every such edge has score exactly
   \(\beta\); and
3. if \(S=L\), there is a perfect matching consisting of exactly one
   score-\(\beta\) edge into the unique missing bundle and \(n-1\) strict
   edges.

## Proof

The definition of \(\beta\) and finiteness of the set of bijections give a
perfect matching in \(G_{\geq}\). A perfect matching in \(G_{>}\) would have
minimum score strictly greater than \(\beta\), a contradiction.

Minimality of \(S\) says every proper subset \(A\subsetneq S\) satisfies

\[
|N_{G_{>}}(A)|\geq |A|. \tag{2}
\]

For \(k>1\), apply (2) to \(S\setminus\{i\}\). Its neighborhood is contained
in \(N_{G_{>}}(S)\), so the latter has size at least \(k-1\). Hall deficiency
gives size at most \(k-1\), proving (1). For \(k=1\), deficiency directly
gives an empty neighborhood. Hall's theorem applied to each
\(S\setminus\{i\}\) proves assertion 1.

A perfect matching of \(G_{\geq}\) assigns the \(k\) members of \(S\) to
distinct bundles, while only \(k-1\) bundles lie in their strict
neighborhood. At least one matched edge therefore leaves that neighborhood.
It is weak but not strict, so its score is exactly \(\beta\). This proves
assertion 2.

Finally suppose \(S=L\). Equation (1) leaves a unique bundle
\(r^*\in R\setminus N_{G_{>}}(L)\). Take any weak perfect matching and let
\(i^*\) be the agent it matches to \(r^*\). Assertion 1 supplies a strict
matching of \(L\setminus\{i^*\}\) onto the \(n-1\) strict-neighborhood
bundles. Combine it with the weak edge \((i^*,r^*)\), whose score is exactly
\(\beta\). This proves assertion 3. \(\square\)

## EFX specialization

For a complete bundle partition \(Y=(Y_1,\ldots,Y_n)\), use normalized EFX
edge scores

\[
s_{ij}=\frac{v_i(Y_j)-\max_{\ell\ne j}
\bigl(v_i(Y_\ell)-\min_{g\in Y_\ell}v_i(g)\bigr)}{v_i(M)}.
\]

Then \(\beta\geq0\) exactly when the partition supports an EFX assignment.
When \(\beta<0\), the theorem gives an exact critical obstruction at the best
possible assignment margin. For four agents, an inclusion-minimal critical
set has size 1, 2, 3, or 4, with respectively 0, 1, 2, or 3 strict
neighbors.

Thus the size-two and size-three branches are not separate graph-theoretic
phenomena. In both, the missing analytic step is the same: modify the partial
allocation so that a score-\(\beta\) edge crossing the critical cut becomes
strict without destroying the matching on the other side. The full-cut
branch additionally permits the exact one-equality-edge normal form.

## Proper-cut factorization or expansion

Put \(T=N_{G_>}(S)\), \(U=L\setminus S\), and \(W=R\setminus T\). Take a
weak perfect matching \(M\), and choose an agent \(a\in S\) that \(M\)
matches into \(W\); at least one exists. There are two possibilities.

1. The weak graph induced between \(U\cup\{a\}\) and \(W\) has a perfect
   matching. Combining it with the strict matching of
   \(S\setminus\{a\}\) into \(T\) gives a full matching with exactly one
   critical-cut crossing from \(S\) to \(W\).
2. That residual graph is Hall-deficient. If \(Q\subseteq U\cup\{a\}\) is
   a residual Hall witness, then \(Q\cap U\ne\varnothing\), and
   \(S'=S\cup(Q\cap U)\) is a strictly larger Hall-deficient set in \(G_>\).

For the second claim, \(a\) has a weak neighbor in \(W\), so a deficient
\(Q\) cannot consist only of \(a\). Also

\[
N_{G_>}(S')\subseteq T\cup N_{G_{\geq}[U,W]}(Q).
\]

If \(a\in Q\), the right side has size at most
\((|S|-1)+|Q\cap U|=|S'|-1\). If \(a\notin Q\), its size is at most
\(|S'|-2\). Thus \(S'\) is Hall-deficient.

This dichotomy explains the extra equality crossings possible for proper
cuts. Either the cut factors into a strict internal matching plus a smaller
weak residual problem, or its obstruction necessarily expands to additional
agents. For four agents, a size-three failure of factorization expands
immediately to the full cut; a size-two failure expands to size three or
four.

## Verification and boundary

The script tracks/parkability/audit_bottleneck_hall_cut.py exhaustively checks
all 27,713 nonmatchable strict bipartite graphs on \(4+4\) vertices, their
31,556 inclusion-minimal deficient sets, and 757,344 weak matching
extensions.

This cap-free graph lemma does not prove that the required
valuation-dependent allocation modification exists. It therefore does not
by itself prove four-agent or general additive EFX.

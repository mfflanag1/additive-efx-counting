# Distinct-Half Density Floor Lemma

**Status:** cap-free analytic theorem  
**Scope:** four agents, nine goods, strict common favorite  
**Not claimed:** that the resulting owner-floor allocation is EFX

## Theorem

Let \(f\) be a strict common favorite and write \(F_i=v_i(f)\). For each
agent \(i\), sort the eight residual values as

\[
x^i_1\ge\cdots\ge x^i_8.
\]

Assume

\[
x^i_5+x^i_6+x^i_7>F_i
\tag{1}
\]

and that at least three residual goods have value strictly greater than
\(F_i/2\). If the four agents have distinct representatives among their
half-favorite goods, then the goods admit a partition

\[
\{f,p\}\mid P\mid Q\mid T,
\qquad |P|=|Q|=2,\quad |T|=3,
\tag{2}
\]

and an assignment of its bundles such that every owner \(i\) receives a
bundle \(B_i\) with

\[
v_i(B_i)\ge F_i.
\tag{3}
\]

This strictly strengthens the previously dual-encoded owner-floor theorem:
the exact universal-threshold hypothesis is used only through (1) and the
three-half-favorites consequence.

## A set-system lemma

The construction rests on the following finite lemma.

> Let \(A_0,\ldots,A_3\) be three-element subsets of an eight-element set,
> and suppose they have a system of distinct representatives. For each
> \(i\), let \((s_i,\ell_i)\) be two distinct elements outside \(A_i\).
> Then there are four distinct agents \(a,b,c,d\) for which one of the
> following holds:
>
> 1. there are disjoint two-subsets
>    \(P_b\subseteq A_b\setminus\{\ell_d\}\) and
>    \(P_c\subseteq A_c\setminus\{\ell_d\}\); or
> 2. there are disjoint two-subsets
>    \(P_b\subseteq A_b\setminus\{s_d\}\) and
>    \(P_c\subseteq A_c\setminus\{s_d\}\), and
>    \(\ell_d\in P_b\cup P_c\).

To prove it, suppose neither alternative exists for any \(d\). Two
three-sets support disjoint two-subsets after deleting one element exactly
when their remaining union has size at least four. Failure of the first
alternative, applied with either of the two other agents as \(d\), therefore
implies

\[
|A_i\cup A_j|\le4
\qquad(i\ne j).
\tag{4}
\]

Thus every two \(A_i\)'s intersect in at least two elements. A family of
three-sets with this property has one of two forms:

1. all its sets contain a common two-element core \(C\); or
2. all its sets lie inside one four-element set \(W\).

For completeness, take two distinct sets with intersection \(C\) and union
\(W\). Any third set either contains \(C\), or the two intersection
conditions force it to lie in \(W\). A set of the latter type intersects a
set \(C\cup\{z\}\) with \(z\notin W\) in only one element. Hence the two
forms cannot mix.

In the four-set case, write \(A_i=W\setminus\{z_i\}\). If two of the three
sets other than \(A_d\) are distinct, failure of the first alternative
forces \(\ell_d=z_d\). Since \(s_d\notin A_d\) and \(s_d\ne\ell_d\), it lies
outside \(W\). The two distinct sets then support disjoint pairs covering
all of \(W\), including \(\ell_d\), which is the second alternative. Hence
the other three sets must be identical for every \(d\). All four sets are
then identical, contradicting the existence of four distinct
representatives.

In the common-core case, write

\[
A_i=C\cup\{z_i\}.
\]

The representatives condition implies that at least two distinct values
occur among the \(z_i\)'s. For a fixed \(d\), the other three \(z\)'s cannot
contain three distinct values: failure of the first alternative would force
\(\ell_d\) to belong simultaneously to every two-element pair of them. If
the other three contain exactly two values \(\alpha,\beta\), failure of the
first alternative forces
\(\ell_d\in\{\alpha,\beta\}\). Failure of the second then forces
\(\{s_d,\ell_d\}=\{\alpha,\beta\}\), so \(z_d\notin\{\alpha,\beta\}\).

Now inspect the multiplicities of the \(z_i\)'s. Three or four distinct
values leave three distinct values after deleting a suitable agent, which
is impossible. With two distinct values, a \(2+2\) split lets us choose any
\(d\), and a \(3+1\) split lets us choose \(d\) from the majority. In
either case the other three agents use both values while \(z_d\) is one of
them, contradicting the preceding conclusion. This proves the set-system
lemma.

## Proof of the theorem

For agent \(i\), let

\[
H_i=\{g\ne f:2v_i(g)>F_i\},
\]

and let \(s_i,\ell_i\) be its second-least and least residual goods. Remove
these two goods and write

\[
K_i=H_i\setminus\{s_i,\ell_i\}.
\]

Every \(K_i\) has at least three elements. If \(s_i\le F_i/2\), neither
bottom good belongs to \(H_i\), so \(K_i=H_i\). If \(s_i>F_i/2\), the seven
largest residual goods are all half-favorites, leaving at least six after
the two bottom goods are removed.

The \(K_i\)'s also have distinct representatives. Since each has size at
least three, Hall can fail only for the set of all four agents, and then
their union would have size three. In that event every \(K_i\) would be the
same three-set. A \(K_i\) of size three cannot arise from the
\(s_i>F_i/2\) case, so \(K_i=H_i\) for every agent, contradicting the
assumed distinct representatives of the \(H_i\)'s.

Choose distinct representatives in the \(K_i\)'s and extend each selected
representative to a three-set \(A_i\subseteq K_i\). Apply the set-system
lemma.

In its first alternative, put \(p=\ell_d\). Give \(\{f,p\}\) to \(a\),
\(P_b\) to \(b\), \(P_c\) to \(c\), and the three remaining residual goods
to \(d\). In its second alternative, use \(p=s_d\) and the same assignment.

The favorite pair clears \(a\)'s floor. Each of \(P_b,P_c\) consists of
two half-favorites for its owner and therefore clears that owner's floor.
In the first alternative the remaining triple avoids \(\ell_d\), so its
three goods are drawn from the seven largest residual goods of \(d\). Its
value is at least

\[
x^d_5+x^d_6+x^d_7>F_d.
\]

In the second alternative the favorite pair removes \(s_d\), while one of
the two assigned pairs absorbs \(\ell_d\). The remaining triple avoids both
bottom goods and is at least as valuable as
\(x^d_4+x^d_5+x^d_6\), which is no smaller than the preceding bound. This
proves (3).

## Connection to universal threshold failure

Exact universal owner-threshold failure is

\[
x^i_5+x^i_6+x^i_7>F_i
\quad\text{and}\quad
\bigl(x^i_3+x^i_7>F_i\ \text{or}\ x^i_4+x^i_5>F_i\bigr).
\]

The first conjunct is (1). The first disjunct in parentheses implies that
the top three goods exceed \(F_i/2\); the second implies that the top four
do. Hence the theorem analytically proves the owner-floor starting state in
the entire distinct-representative universal-threshold branch.

The exhaustive audit
[efx49_distinct_half_density_floor_lemma_audit.json](efx49_distinct_half_density_floor_lemma_audit.json)
checks all 175,615 symmetry-normalized four-set families with an SDR. It is
a regression test for the proof, not a substitute for it.

The theorem is sharp as a starting state rather than an EFX normal form.
A strict branch-valid profile has 728 allocations produced by the
bottom-aware/high--high-pair conditions above and zero EFX allocations
among them, although it has many balanced EFX allocations outside that
family. See
[efx49_distinct_half_structured_floor_boundary_audit.json](efx49_distinct_half_structured_floor_boundary_audit.json).

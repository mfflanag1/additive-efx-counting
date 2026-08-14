# Branch-tree base cancellation or closed-union lemma

**Date:** 2026-08-14

**Status:** cap-free exact characterization of net base-signed disconnection;
refutes the stronger whole-return shortcut

## Three physical holder maps

Let `X`, `Y`, and `Z` be allocations of the same finite good set among the
four owners and charity.  For a good `g`, write

\[
 b(g)=\text{holder in }X,\qquad
 y(g)=\text{holder in }Y,\qquad
 z(g)=\text{holder in }Z.                         \tag{1}
\]

The frozen four-edge goal counts the nonempty `Y->Z` supplier pairs
`(y(g),z(g))`.  The older GG signed record instead uses the net pairs
`(b(g),z(g))`.  Composition must therefore be performed good by good; a
`Y`-supplier label cannot be substituted for a base-origin label.

For one `Y`-relative packet edge `u->v` carrying packet `P`, the exact
base-origin decomposition is

\[
 P=(P\cap X_v)\mathbin{\dot\cup}
   \mathop{\dot\bigcup}_{a\ne v}(P\cap X_a).       \tag{2}
\]

The first packet is returned base-`v` support and disappears from the net
`X->Z` transfer graph.  Every nonempty `P cap X_a`, `a ne v`, creates the net
pair `a->v`.  Hence the whole `Y` edge disappears exactly when `P subseteq
X_v`; mixed packets can partially cancel and change their supplier label.

## Closed-union theorem

Let `H_X(Z)` be the undirected net base-transfer graph: its vertices are the
owners and charity, and it contains `{a,v}` whenever some good has
`b(g)=a`, `z(g)=v`, and `a!=v`.

For any vertex set `K`, put

\[
 X(K)=\mathop{\dot\bigcup}_{a\in K}X_a,
 \qquad
 Z(K)=\mathop{\dot\bigcup}_{a\in K}Z_a.           \tag{3}
\]

Then the following are equivalent:

1. no edge of `H_X(Z)` crosses `K | K^c`;
2. for every good `g`, `b(g) in K` iff `z(g) in K`;
3. `X(K)=Z(K)` as physical good sets.              \tag{4}

The proof is immediate good by good.  An edge crosses the cut exactly when
the two membership indicators in item 2 differ; equality of the unions in
item 3 is exactly equality of those indicators for every good.

Consequently `H_X(Z)` is disconnected if and only if there is a nonempty
proper `K` whose aggregate base support is restored exactly:

\[
                            X(K)=Z(K).             \tag{5}
\]

Every connected component of `H_X(Z)` is therefore a closed base-support
block.  This statement is cap-free and does not refer to packet sizes or the
intermediate state `Y`.

## Exact counterexample to the whole-return shortcut

Take the `Y`-relative Hamiltonian branch

```text
charity -> r -> s -> q -> d.
```

Let its four moved goods have the following base origins:

| current edge | base origin | final holder |
|---|---|---|
| `charity->r` | `s` | `r` |
| `r->s` | `q` | `s` |
| `s->q` | `r` | `q` |
| `q->d` | `charity` | `d` |

No packet is returned to its base owner: every base origin differs from its
final holder.  Nevertheless the net graph has exactly two components,

\[
                         \{r,q,s\}\mid\{d,\mathrm{charity}\}, \tag{6}
\]

with the first three net edges forming a triangle and the last joining
charity to `d`.  Add a private retained good to each vertex if nonempty
bundles are desired; this does not change either graph.

Thus the tempting implication

> disconnected after cancellation `=>` some entire branch packet returned
> to its recipient's base bundle

is false.  Any proof using it must be discarded.

## Consequence for the fixed-U gate

For a paid six-branch probe, the current `Y->Z` graph is a four-edge spanning
tree.  After exact composition with `X->Y`, either:

1. the net signed graph remains connected; or
2. it splits into nontrivial closed base-support blocks satisfying (5).

The second outcome is not an untyped cancellation case.  It is an exact
aggregate reassembly interface.  `BASE_SUPPORT_CLOSURE_PAID_COMPONENT_LEMMA_20260813.md`
shows how closed support pays its owners, while
`SATURATED_REPRESENTED_COMPONENT_CHARITY_EXTRACTION_THEOREM_20260813.md`
can close a proper represented block only after response-rank and outsider
safety are verified.  Those two conditions, not packet cardinality, are the
remaining cancellation obligations.

## Claim boundary

Proved: the per-packet composition identity (2), the closed-union
characterization (4)--(5), and the exact counterexample (6).

Not proved: response rank or outsider safety of every closed block,
conversion of every block into PI/progress/EFX, the supplier-capture branch,
the fixed-`U` theorem, or general EFX.

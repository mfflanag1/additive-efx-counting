# Trapped-source return theorem for a length-two genuine cycle

## Setting

Work in the BCFF nondegenerate convention. Let \(X\) be a globally
lexicographically maximal four-agent partial EFX allocation with sole
unallocated good \(f\), and assume no agent envies \(\{f\}\). Suppose exactly
two owners \(r,q\) have nonsingleton bundles and the selected shortest
\(f\)-champion cycle is

\[
r\xrightarrow{f}q\xrightarrow{f}r. \tag{1}
\]

Both edges are genuine and decompose

\[
X_r=T_r\mathbin{\dot\cup}B_r,\qquad
X_q=T_q\mathbin{\dot\cup}B_q, \tag{2}
\]

with nonempty bottoms. Let \(a,d\) be the two singleton owners outside the
cycle. BCFF Theorem 3.16 gives, for each bottom, either a good internal edge
or an external edge.  In a two-cycle the only good internal `B_r`-edge is
the edge from `r` into `q`; together with `q -f-> r` it is already a PI
cycle.  Symmetrically, the only good internal `B_q`-edge closes with
`r -f-> q`.  Global maximality excludes both internal alternatives, so each
bottom has an external edge:

\[
e_r:\ a_r\xrightarrow{B_r\mid B_q}q,\qquad
e_q:\ a_q\xrightarrow{B_q\mid B_r}r,\qquad
a_r,a_q\in\{a,d\}. \tag{3}
\]

The second field is the prescribed release, not the corresponding discard.
Thus \(e_r\) nominally consumes \(B_r\) and releases \(B_q\), while \(e_q\)
nominally consumes \(B_q\) and releases \(B_r\). Their desired blocks may
discard part of an incoming packet; this does not affect PI feasibility.

## Singleton return fact

> **Lemma 1.** Every singleton owner has an incoming ordinary envy edge.

**Proof.** If no agent envies singleton \(X_a\), then no agent strongly envies
\(X_a\cup\{f\}\): deleting \(f\) leaves the unenvied singleton, while deleting
its singleton good leaves the unenvied charity. Positive additivity makes
owner \(a\) strictly prefer the pair. Hence \(a\) is a clean self-\(f\)
champion and absorption is complete EFX, contradicting maximality.
\(\square\)

The ordinary envy graph is acyclic, since an envy cycle is already a basic
PI cycle.

## Closure theorem

> **Theorem 2.** Configuration (1)--(3) cannot occur at a globally maximal
> noncomplete state.

### Distinct external sources

Suppose \(a_r\ne a_q\). Rename them \(a,d\), so

\[
a\xrightarrow{B_r\mid B_q}q,\qquad
d\xrightarrow{B_q\mid B_r}r. \tag{4}
\]

Choose an incoming envy edge into each singleton. If \(r\to a\), then

\[
a\xrightarrow{B_r\mid B_q}q\xrightarrow{f}r\longrightarrow a \tag{5}
\]

is PI. Symmetrically, \(q\to d\) closes

\[
d\xrightarrow{B_q\mid B_r}r\xrightarrow{f}q\longrightarrow d. \tag{6}
\]

Assume neither edge exists. An incoming envier of \(a\) is then \(q\) or
\(d\), and an incoming envier of \(d\) is \(r\) or \(a\). The four
combinations close as follows.

1. If \(q\to a\) and \(r\to d\), use the two vertex-disjoint cycles

   \[
   a\xrightarrow{B_r\mid B_q}q\longrightarrow a,\qquad
   d\xrightarrow{B_q\mid B_r}r\longrightarrow d. \tag{7}
   \]

   Their packet supply is mutual: the first generalized edge releases
   \(B_q\), and the second releases \(B_r\).
2. If \(q\to a\) and \(a\to d\), then

   \[
   d\xrightarrow{B_q\mid B_r}r\xrightarrow{f}q
   \longrightarrow a\longrightarrow d \tag{8}
   \]

   is PI.
3. If \(d\to a\) and \(r\to d\), then

   \[
   a\xrightarrow{B_r\mid B_q}q\xrightarrow{f}r
   \longrightarrow d\longrightarrow a \tag{9}
   \]

   is PI.
4. The remaining combination \(d\to a\) and \(a\to d\) is an envy cycle.

Every case contradicts global maximality.

### Shared external source

Suppose \(a_r=a_q=a\), and let \(d\) be the other singleton owner. If
\(r\to a\), cycle (5) closes. If \(q\to a\), the symmetric cycle using
\(e_q\) closes. Assume neither. Lemma 1 and acyclicity force

\[
d\longrightarrow a. \tag{10}
\]

An incoming envier of \(d\) cannot be \(a\), since that would make an envy
two-cycle. Hence either \(r\to d\) or \(q\to d\). In the first case,

\[
a\xrightarrow{B_r\mid B_q}q\xrightarrow{f}r
\longrightarrow d\longrightarrow a \tag{11}
\]

is PI. In the second,

\[
a\xrightarrow{B_q\mid B_r}r\xrightarrow{f}q
\longrightarrow d\longrightarrow a \tag{12}
\]

is PI. This again contradicts maximality. \(\square\)

The proof does not need the shared-source envy exception in BCFF Corollary
3.18. Singleton nonabsorption supplies the return path even when both
external bottom edges use the same source.

## Consequence and boundary

> **Corollary 3.** In a globally maximal four-agent one-charity obstruction
> with exactly two nonsingleton bundles, the selected shortest genuine
> \(f\)-cycle cannot have length two.

The theorem is cap-free and does not require complete retention of a nominal
incoming bottom. It uses global maximality to exclude direct absorption,
envy cycles, and each displayed PI cycle. It assumes the external edges
supplied by BCFF Theorem 3.16 and does not extend that theorem to longer
cycles.

Primary source for the internal/external alternative and the two-cycle good
edge specialization: Berger--Cohen--Feldman--Fiat, Theorem 3.16 and the
length-two application in the proof of Lemma 6.2,
[arXiv:2102.10654](https://arxiv.org/abs/2102.10654).

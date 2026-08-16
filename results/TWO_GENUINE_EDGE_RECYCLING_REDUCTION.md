# Two-genuine-edge recycling reduction

**Status:** cap-free local propagation theorem and exact cycle-length
obstructions  
**Scope:** a globally lexicographically maximal four-agent EFX allocation
with one unenvied charity good and exactly two nonsingleton bundles  
**Boundary:** closes the length-two cycle and every compatible cross-bottom
source; the remaining length-three/four configurations are isolated below

## Two genuine edges

Let `r` and `q` own the two nonsingleton bundles. By the
[`one-large champion closure reduction`](ONE_LARGE_CHAMPION_CLOSURE_REDUCTION.md),
every selected `f`-champion cycle in a noncomplete global maximum contains
both `r` and `q`. The edges entering them genuinely retain `f`, have no
parallel envy edges, and decompose

\[
X_r=T_r\mathbin{\dot\cup}B_r,
\qquad
X_q=T_q\mathbin{\dot\cup}B_q, \tag{1}
\]

with nonempty bottoms. Every cycle edge entering one of the other two
agents is an ordinary envy edge between singleton bundles.

Choose a shortest such `f`-champion cycle in the full champion graph. It
has no self-`f`-champion and no internal `f`-champion chord: either would
give a shorter cycle. At a global maximum a self edge would also itself be
a one-edge PI cycle.

## Local BCFF propagation does not need a good full cycle

The proofs of BCFF Lemmas 3.13 and 3.14 use only local decomposition and
missing-edge hypotheses. The following restricted versions therefore
remain valid even when singleton edges elsewhere on the cycle discard `f`.

> **Adjacent-large seed lemma.** Suppose the cycle contains the consecutive
> genuine edges
>
> \[
> p\xrightarrow{f}r\xrightarrow{f}q. \tag{2}
> \]
>
> Then some agent `a` satisfies
>
> \[
> a\xrightarrow{B_r\mid B_q}q. \tag{3}
> \]

**Proof.** Agent `r` genuinely `f`-decomposes `q`, agent `r` is itself
`f`-decomposed by `p`, and shortestness excludes `r` as a self-`f`-
champion. BCFF Observation 2.11 gives

\[
T_r<_rT_q.
\]

Additivity then gives

\[
X_r=T_r\cup B_r<_rT_q\cup B_r.
\]

The set on the right is envied, so it has a most-envious agent. This is
exactly (3), with the corresponding discard chosen by that agent. \(\square\)

> **Local propagation lemma.** Suppose
> \(k\xrightarrow{B_r\mid B_j}j\), agent `k` genuinely `f`-decomposes
> \(u=\operatorname{succ}(k)\), `j` is `f`-decomposed, and `k` does not
> `f`-champion `j`. Assume also that \(B_r\cap X_u=\varnothing\), so the
> proposed incoming packet is disjoint from the target bundle. Then some
> agent `a` satisfies
>
> \[
> a\xrightarrow{B_r\mid B_u}u. \tag{4}
> \]

**Proof.** BCFF Observation 2.11 gives \(T_j<_kT_u\). The first edge says
that `k` envies a subset of \(T_j\cup B_r\), hence the full set. Additivity
gives

\[
X_k<_kT_j\cup B_r<_kT_u\cup B_r.
\]

A most-envious agent of the last set supplies (4). This is exactly the
argument of BCFF Lemma 3.14; no property of cycle edges not incident to
`k`, `j`, or `u` is used. \(\square\)

These edges may discard part of their nominal incoming packet. Incoming-
clean normalization can shrink `B_r`, but this does not affect the PI
argument below: every retained subpacket is still released by the root
edge in (2).

## The compatible replacement certificate

Keep the root edge \(p\xrightarrow{f}r\), which releases `B_r`, and replace
the other genuine edge \(r\xrightarrow{f}q\) by any generalized-champion
edge

\[
r\xrightarrow{H\mid S}q,
\qquad H\subseteq B_r. \tag{5}

\]

Keep the remaining singleton envy segment from `q` back to `p`. These
edges form a PI cycle: `f` supplies the root, the root releases `H`, and
all incoming packets are disjoint. BCFF Lemma 3.5 then gives a partial EFX
allocation strictly Pareto dominating the alleged global maximum. Thus no
edge (5) can exist in a maximal obstruction.

In particular, if the source `a` in the seed lemma is `r`, (3) is exactly
such a replacement. The rest of the analysis determines where the forced
source can hide when it is not compatible.

There is one further excluded source. In (2), the predecessor `p` cannot be
the source in (3). If it were, the seed championship would give

\[
X_p<_pT_q\cup B_r.
\]

Because `p` genuinely decomposes `r`, does not `f`-champion `q`, and `q` is
decomposed, BCFF Observation 2.11 gives \(T_q<_pT_r\). Additivity then gives

\[
X_p<_pT_q\cup B_r<_pT_r\cup B_r=X_r,
\]

contradicting the absence of a parallel envy edge on the genuine root edge
\(p\xrightarrow{f}r\). Hence

\[
a\notin\{r,p\} \tag{6}

\]

at a global maximum: `r` would close a PI cycle, and `p` is impossible.

## Length two: compatible external-source obstruction

Let

\[
r\xrightarrow{f}q\xrightarrow{f}r
\]

be the shortest cycle. Applying the seed lemma in each direction gives a
`B_r`-edge into `q` and a `B_q`-edge into `r`. For the first, source `r`
would be the compatible replacement and source `q=pred(r)` is forbidden by
(6). Thus every forced `B_r` source lies outside the two-cycle. The same
holds symmetrically for `B_q`.

The cycle is a good `f`-cycle: it has no parallel envy edge and shortestness
excludes internal chords. Therefore BCFF Theorem 3.16 and Corollary 3.18
apply literally. At a global maximum all its good bottom edges are excluded
by the replacement certificate, so both bottoms have external edges from
the two singleton agents. If the two selected external bottom edges share
one source, Corollary 3.18 forces that singleton to envy `r` or `q`.

This residue is closed by the
[`trapped-source return theorem`](TRAPPED_SOURCE_RETURN_LENGTH_TWO_CLOSURE_THEOREM.md).
Every singleton has an incoming envy edge, since otherwise clean
self-`f` absorption completes EFX. With distinct external bottom sources,
the four possible envy predecessors close a PI cycle or two mutually
supplied disjoint PI cycles. With a shared source, acyclicity forces an envy
return through the other singleton. Thus a globally maximal obstruction
cannot have a length-two shortest genuine cycle. An independent audit found
the cases exhaustive and verified that PI feasibility does not require
retention of the full nominal packet.

## Length three: owner-or-external obstruction

Up to reversal of names, the cycle is

\[
p\xrightarrow{f}r\xrightarrow{f}q\longrightarrow p, \tag{7}

\]

where `p` is a singleton owner and the last edge is envy. Let `d` be the
singleton agent outside the cycle. The adjacent-large seed lemma gives an
edge (3). Its source cannot be `r`, by the replacement certificate, and
cannot be `p=pred(r)`, by (6). The only possibilities are therefore

\[
a\in\{q,d\}. \tag{8}

\]

If `a=q`, the discovered bottom edge is a generalized self-edge at the
second large target. It cannot be combined with the root edge into a
vertex-disjoint PI cycle using the known edges. If `a=d`, the packet is
consumable only from the unique external vertex, and a return path through
`d` is missing. These are exact compatible-source obstructions; the local
propagation lemma rules out no further source because both `q` and `d`
have outgoing envy or no cycle edge rather than a genuine decomposition.

## Length four with adjacent large targets

Write the cycle as

\[
p\xrightarrow{f}r\xrightarrow{f}q
 \longrightarrow s\longrightarrow p, \tag{9}

\]

where `p,s` own singleton bundles and the last two edges are envy. Again
the seed lemma gives (3). Source `r` would close the compatible PI cycle,
and source `p=pred(r)` is impossible by (6). There is no external vertex,
so every forced source lies in the downstream envy segment:

\[
a\in\{q,s\}. \tag{10}

\]

Neither source can be advanced by BCFF Lemma 3.14: their outgoing cycle
edges are envy edges and do not `f`-decompose their successors. Ordinary
envy does imply that further sets obtained by adding `B_r` are envied, but
the most-envious source of such a set is uncontrolled. The exact adjacent
length-four obstruction is therefore source trapping in the two-vertex
envy segment `q -> s`.

## Length four with separated large targets

The alternating topology is

\[
p\xrightarrow{f}r\longrightarrow s
 \xrightarrow{f}q\longrightarrow p, \tag{11}

\]

with singleton owners `p,s`. No vertex is both `f`-decomposed and the
source of a genuine edge to the other large target. Consequently the
adjacent-large seed lemma has no starting point; this is exactly where the
BCFF propagation proof stops.

Either of the following edges would nevertheless close a PI cycle:

\[
s\xrightarrow{H\mid S_q}q\quad(H\subseteq B_r),
\qquad
p\xrightarrow{K\mid S_r}r\quad(K\subseteq B_q). \tag{12}

\]

For the first, keep the root \(p\xrightarrow{f}r\), the envy edge
`r -> s`, the generalized edge into `q`, and the envy edge `q -> p`.
The second is symmetric. Hence both compatible edge families in (12) are
absent in a maximal obstruction.

This is not merely an untried application of Theorem 3.16. The cycle in
(11) is not good: its singleton-target edges discard `f` and have parallel
envy edges. More importantly, neither large bottom has the consecutive
decomposition inequality \(T_r<_rT_q\) or \(T_q<_qT_r\) used to show that
a cross-bottom offered set is envied. The
[`alternating local obstruction`](ALTERNATING_CROSS_BOTTOM_LOCAL_OBSTRUCTION.md)
is positive, subset-nondegenerate, EFX-Pareto-maximal, has exactly this
chordless champion cycle, and blocks all four cycle-compatible cross-bottom
families. It is not globally lexicographically maximal for any agent order.
The exact separated-cycle gate is therefore a **priority-sensitive
lexicographic escape**, not another Pareto-improving packet edge.

## Resulting gate

The two-genuine-edge problem is now reduced without any value or bundle-size
cap:

1. **length two:** closed cap-free by singleton envy returns and mutually
   supplied external bottom edges;
2. **length three:** the forced adjacent-bottom source is either the second
   large owner or the unique external singleton;
3. **length four, adjacent:** the forced source is trapped in the
   two-vertex downstream envy segment; and
4. **length four, separated:** even all four compatible cross-bottom
   families may be absent at an EFX-Pareto-maximal state; only global
   lexicographic sacrifice remains available in the exact obstruction.

Any compatible source found outside these lists gives a PI cycle and
contradicts global maximality. Closing the breakthrough gate now requires
priority-sensitive return/reallocation theorems for the length-three and
length-four residues. The alternating theorem must permit later-priority
agents to lose utility while fixing every earlier coordinate and improving
the first changed coordinate; no Pareto-only statement can be universal.
Standard good-cycle propagation alone does not provide this.

## Primary source

Berger, Cohen, Feldman, and Fiat,
[*Almost Full EFX Exists for Four Agents (and Beyond)*](https://arxiv.org/abs/2102.10654),
Observations 2.11 and 3.11, Lemmas 3.13--3.14, Theorem 3.16, and Corollary
3.18.

# Alternating easy-priority escape lemma

**Status:** cap-free analytic lemma
**Scope:** four normalized monotone agents (nice cancelable after BCFF Lemma
A.1), arbitrary top/bottom bundle sizes, an alternating genuine champion
cycle with two singleton owners
**Boundary:** closes 16 of 24 priority-role orders; eight singleton-first
orders remain

## Statement

Let a partial EFX allocation have the alternating topology

\[
p\xrightarrow f r\longrightarrow s
\xrightarrow f q\longrightarrow p,
\]

where \(X_p=\{x\}\) and \(X_s=\{y\}\). Thus the ordinary envy edges give

\[
v_r(y)>v_r(X_r),\qquad v_q(x)>v_q(X_q). \tag{1}
\]

Fix a lexicographic priority order. If the order

1. begins with `r` or `q`,
2. begins with `p,r`, or
3. begins with `s,q`,

then the base allocation is not globally lexicographically maximal among
partial EFX allocations.

These conditions cover 16 of the 24 agent orders.

## Proof

Every allocation in the proof gives each agent at most one good. Such an
allocation is automatically EFX: deleting the only good from any nonempty
target bundle leaves the empty set, which no agent with a nonnegative own
bundle can strongly envy.

If `r` is first, give `r` the good `y`. Give the other agents any three
distinct remaining goods, for example `x`, `f`, and one good from \(X_q\),
and leave everything else unallocated. By (1), the first priority agent
strictly improves.

If the order begins `p,r`, keep \(Y_p=\{x\}\), give \(Y_r=\{y\}\), and
give `s,q` distinct singleton goods chosen from `f` and \(X_q\). Agent `p`
is unchanged and `r` strictly improves, so the new allocation
lexicographically dominates the base.

The cases beginning with `q` or `s,q` are symmetric: give `q` the singleton
`x`, preserve \(Y_s=\{y\}\) when `s` is earlier, and singletonize the other
bundles. \(\square\)

## Exact remaining priority orders

Only the following eight orders can support a globally maximal alternating
obstruction:

\[
\begin{array}{llll}
(p,s,r,q),&(p,s,q,r),&(p,q,r,s),&(p,q,s,r),\\
(s,p,r,q),&(s,p,q,r),&(s,r,p,q),&(s,r,q,p).
\end{array}
\]

In every remaining order, a singleton owner occurs first and blocks transfer
of that singleton to its incoming envier. A proof must preserve that first
singleton owner's utility while finding a later improvement.

## Consequence for the atomic certificate

The 16 one-rival cores in
[`ALTERNATING_GLOBAL_LEX_ATOMIC_THEOREM.md`](ALTERNATING_GLOBAL_LEX_ATOMIC_THEOREM.md)
are instances of this lemma. Only the eight multi-rival atomic cores contain
new information. Therefore the packet-lift program should focus exclusively
on those eight orders, beginning with `(p,s,r,q)` up to the half-turn
symmetry exchanging `p` with `s` and `r` with `q`.

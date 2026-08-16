# Diagonal-or-host lemma for direct floater insertion

## Lemma

Let $X=(X_0,\ldots,X_{n-1})$ be a partial EFX allocation under nonnegative
additive valuations, and let $f$ be an unallocated good. Fix a host label $h$
and form the complete partition

\[
P_h=X_h\cup\{f\},\qquad P_j=X_j\quad(j\ne h).
\]

In the EFX-acceptability graph of $P$, every agent $i$ is adjacent to at least
one of bundle labels $i$ and $h$.

Equivalently, if inserting $f$ into $X_h$ destroys agent $i$'s edge to its
original bundle, then the enlarged host bundle is EFX-acceptable to $i$.
The result is cap-free in agents and goods. Floater nonenvy is not required.

## Proof

The host agent $h$ accepts $P_h$: its candidate bundle has only increased,
while every competing bundle and every competing one-good residual is
unchanged from the base EFX allocation.

Now fix $i\ne h$. If $P_i=X_i$ remains acceptable, the claim is immediate.
Otherwise, some one-good residual newly exceeds $v_i(X_i)$. All nonhost
bundles are unchanged, and base EFX already bounds every one-good residual of
them by $v_i(X_i)$. Hence the violating residual must belong to the enlarged
host: for some $g\in P_h$,

\[
v_i(P_h\setminus\{g\})>v_i(X_i).
\]

Nonnegativity gives

\[
v_i(P_h)\ge v_i(P_h\setminus\{g\})>v_i(X_i).
\]

For every nonhost target $X_j$ with $j\ne i$, base EFX gives

\[
v_i(X_j\setminus\{x\})\le v_i(X_i)<v_i(P_h)
\]

for all $x\in X_j$. Residuals of $X_i$ itself are no larger than $v_i(X_i)$.
Thus $P_h$ dominates every one-good residual of every competing bundle, so it
is EFX-acceptable to $i$.

## Hall consequence for four agents

Write $G^h$ for the graph after direct insertion into host $h$. The lemma
provides the spanning row-wise alternatives

\[
N_{G^h}(i)\cap\{i,h\}\ne\varnothing\qquad(i=0,1,2,3).
\]

Therefore a failed identity matching is not an arbitrary $4\times4$ Hall
obstruction: every lost diagonal edge is replaced by the same host column.
The only larger minimal defects still needing reduction are configurations in
which several rows share the host but retain enough common extra columns to
avoid a two-row/one-column defect.

This condition alone does not force a perfect matching or a pair trap. The
exact positive counterexample in
[`partial_hall_direct_pair_extraction_counterexample_audit.json`](partial_hall_direct_pair_extraction_counterexample_audit.json)
has only $3\to2$ and $4\to3$ Hall defects under direct insertion. An
owner-minimum transfer resolves it. Consequently the next lemma must combine
the diagonal-or-host structure with the edge monotonicity of that transfer;
pure graph theory for a single host is insufficient.

# Alternating cross-bottom local obstruction

**Status:** strict local counterexample and exact no-PI boundary
**Scope:** positive additive valuations, four agents, two two-good large
bundles, and one charity good
**Boundary:** local EFX and even Pareto maximality do not force a compatible
cross-bottom edge; global lexicographic maximality is not refuted

## The four compatible families

Consider the alternating basic-champion cycle

\[
p\xrightarrow{f}r\longrightarrow s
 \xrightarrow{f}q\longrightarrow p, \tag{1}
\]

where the unlabelled arrows are envy edges and

\[
X_r=T_r\mathbin{\dot\cup}B_r,
\qquad
X_q=T_q\mathbin{\dot\cup}B_q. \tag{2}
\]

There are four, rather than two, compatible generalized-champion source
families.  Retaining the root edge \(p\xrightarrow f r\), either

\[
r\xrightarrow{H\mid S}q
\quad\hbox{or}\quad
s\xrightarrow{H\mid S}q,
\qquad H\subseteq B_r, \tag{3}
\]

closes a PI cycle: the first gives the three-cycle `p -> r -> q -> p`,
and the second gives the full four-cycle in (1).  Symmetrically, retaining
\(s\xrightarrow f q\), either

\[
q\xrightarrow{K\mid S}r
\quad\hbox{or}\quad
p\xrightarrow{K\mid S}r,
\qquad K\subseteq B_q, \tag{4}
\]

closes a three- or four-cycle.  The root edge releases the incoming bottom
packet, so every edge in (3) or (4) is compatible after incoming-clean
normalization.  At a Pareto-maximal EFX allocation all four families are
therefore empty.

The standard BCFF cross-bottom seed is narrower.  It prescribes release of
the other large bottom:

\[
B_r\mid B_q\text{ into }q,
\qquad
B_q\mid B_r\text{ into }r. \tag{5}
\]

Its full offered sets are \(T_q+B_r\) and \(T_r+B_q\).  Empty prescribed
release is also allowed in (3)--(4), however, and offers the larger sets
\(X_q+B_r\) and \(X_r+B_q\).  This distinction is essential.

## Strict obstruction to the standard seeds

Order the goods as

\[
t_r,b_r,t_q,b_q,x,y,f
\]

and allocate

\[
X_p=\{x\},\quad X_r=\{t_r,b_r\},\quad
X_s=\{y\},\quad X_q=\{t_q,b_q\},
\]

leaving `f` unallocated.  The following positive additive profile is a
strict, nondegenerate perturbation of the small hand profile:

| agent | \(t_r\) | \(b_r\) | \(t_q\) | \(b_q\) | \(x\) | \(y\) | \(f\) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `p` | 5002 | 1008 | 4004 | 1016 | 10064 | 1032 | 6001 |
| `r` | 5001 | 5002 | 4004 | 4008 | 1016 | 11032 | 4064 |
| `s` | 4004 | 1008 | 5002 | 1016 | 1032 | 10064 | 6001 |
| `q` | 4001 | 4002 | 5004 | 5008 | 11016 | 1032 | 4064 |

The own utilities are \((10064,10003,10064,10012)\).  Direct calculation
gives all of the following.

1. `X` is EFX and every owner strictly prefers her bundle to `f`.
2. The exact ordinary envy graph is `r -> s`, `q -> p`.
3. The exact basic `f`-champion graph is the four-cycle (1).  Its unique
   selected desired sets are respectively
   \(\{t_r,f\},\{y\},\{t_q,f\},\{x\}\).
   Thus there are no self-champions or champion chords.
4. None of the four sources in (3)--(4) envies the corresponding standard
   offered set in (5).  Hence all four standard cross-bottom edges are
   absent.

This does **not** block the full compatible families.  Agent `r` is most
envious of \(X_q+B_r\), producing

\[
r\xrightarrow{B_r\mid\varnothing}q, \tag{6}
\]

and `q` symmetrically supplies
\(q\xrightarrow{B_q\mid\varnothing}r\).  The two shortcuts give exactly
the two Pareto-dominating EFX allocations in the exhaustive census:

\[
\begin{aligned}
&\{t_r,f\}\mid\{b_r,t_q,b_q\}\mid\{y\}\mid\{x\},\\
&\{x\}\mid\{y\}\mid\{t_q,f\}\mid\{t_r,b_r,b_q\}.
\end{aligned} \tag{7}
\]

Thus the repaired hand profile refutes the *standard-seed* implication,
but its pooling escape is the missing three-cycle family, not an escape
outside the four families.

## A strict obstruction to all four compatible families

Keep the first and third rows above and replace the two large-owner rows by

| agent | \(t_r\) | \(b_r\) | \(t_q\) | \(b_q\) | \(x\) | \(y\) | \(f\) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `r` | 9001 | 1064 | 1004 | 1008 | 1016 | 11032 | 1002 |
| `q` | 1004 | 1008 | 9001 | 1064 | 11032 | 1016 | 1002 |

Call the resulting profile `V*`.  Its own utilities are
\((10064,10065,10064,10065)\).  The same direct checks prove that the base
allocation is EFX, strictly charity-dominating, and has exactly the envy
and basic-champion edges in (1), with the same unique desired sets.

For each family, even its largest possible offer is strictly below the
candidate source's own bundle:

| source and target | largest offer | source value | own value | margin |
|---|---|---:|---:|---:|
| `r` into `q` using \(H\subseteq B_r\) | \(X_q+B_r\) | 3076 | 10065 | 6989 |
| `s` into `q` using \(H\subseteq B_r\) | \(X_q+B_r\) | 7026 | 10064 | 3038 |
| `q` into `r` using \(K\subseteq B_q\) | \(X_r+B_q\) | 3076 | 10065 | 6989 |
| `p` into `r` using \(K\subseteq B_q\) | \(X_r+B_q\) | 7026 | 10064 | 3038 |

Positive additivity makes every offer obtained by shrinking the incoming
packet or enlarging the prescribed release still less valuable.  No source
can envy any subset of such an offer.  Therefore **every edge in all four
families (3)--(4) is absent**, for every prescribed target release.

The construction is nondegenerate, not merely tie-broken informally.  Each
entry has the form \(1000a_g+2^{e_g}\), with the seven binary corrections
distinct within a row and summing to less than 1000.  Equal subset values
would first require equal integer parts and then equal binary signatures,
which forces the same subset.  All displayed structural inequalities have
large strict margins.

## Exact no-PI and global-maximality boundary

The full labelled census of all \(5^7\) assignments of the seven goods to
four agents or charity has these results for `V*`:

- 2263 assignments are EFX;
- none Pareto dominates the base allocation.

Consequently the base is EFX-Pareto-maximal and admits no BCFF PI cycle or
PI edge set: such a certificate would produce a Pareto-dominating partial
EFX allocation.  This strictly refutes the implication

> alternating EFX + exact chordless champion cycle + no PI certificate
> implies a compatible cross-bottom edge.

It does not refute the implication with **global lexicographic maximality**.
For each of the four possible first-priority agents the census contains an
EFX allocation that raises that agent's utility, while possibly lowering
another agent's.  Hence `V*` is not globally lexicographically maximal for
any agent order.  Pareto maximality and global lexicographic maximality
cannot be interchanged at this gate.

The exact replay is frozen in
[`alternating_cross_bottom_obstruction_audit.json`](alternating_cross_bottom_obstruction_audit.json)
and generated by
[`audit_alternating_cross_bottom_obstruction.py`](../tracks/parkability/audit_alternating_cross_bottom_obstruction.py).

## Resulting gate

Local BCFF propagation is exhausted in the alternating topology.  Neither
EFX, exact basic-champion structure, absence of self/chords, nor even
absence of every Pareto-improving EFX allocation forces a cross-bottom
edge.  The next lemma must use the part of global maximality not captured
by PI machinery:

> **Priority-sensitive alternating escape lemma (candidate).** For the
> fixed lexicographic agent order, an alternating state with all four
> compatible families empty admits a partial EFX reallocation that fixes
> every earlier-priority utility and strictly raises the first utility that
> changes.

The witness `V*` shows why such a lemma must allow sacrifice: its four
agentwise EFX escapes improve the chosen first agent but none Pareto
dominates.  A proof should therefore analyze bottom pooling and splitting
under terminal EFX thresholds, not search for another owner-monotone PI
cycle.  Proving this priority-sensitive escape, or constructing a truly
globally maximal alternating profile, is the exact remaining global gate.

The minimal `2+2+1+1` version of that gate is now closed for every priority
order by the exact
[`alternating global-lex atomic exclusion`](ALTERNATING_GLOBAL_LEX_ATOMIC_THEOREM.md).
Its largest deletion-minimal rival menu has five allocations. The unresolved
step is to lift those atomic menus to multi-good top and bottom packets while
preserving every one-good EFX deletion inequality.

## Primary source

Berger, Cohen, Feldman, and Fiat,
[*Almost Full EFX Exists for Four Agents (and Beyond)*](https://arxiv.org/abs/2102.10654),
Definitions 2.6--2.7 and 3.1--3.4 and Lemma 3.5.

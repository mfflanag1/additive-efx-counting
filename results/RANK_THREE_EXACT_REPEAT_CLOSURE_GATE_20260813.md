# Rank-three exact-repeat closure gate

**Date:** 2026-08-13

**Status:** exact graph-level counterexample to the rank-growth inference;
the full positive-additive GG recurrence remains undecided

**Applicability correction (2026-08-13):** this audit is an abstract
five-target response-graph counterexample. Its three minimum connected forms
all use a desired response into charity. Such an edge is impossible when the
current charity is a base-safe singleton and every owner is paid. Therefore
the audit still refutes the bare implication from graph coverage to rank four,
but its minimum forms are not realizations of the canonical paid
singleton-charity fixed-`U` cell. The applicable graph reduction is now the
forced owner-cycle lemma in
[`PAID_SINGLETON_CHARITY_RANK_THREE_OWNER_CYCLE_LEMMA_20260813.md`](PAID_SINGLETON_CHARITY_RANK_THREE_OWNER_CYCLE_LEMMA_20260813.md).

## The missing implication

The candidate fixed-`U` termination proof used the following implication:

> an exact repeated sacrificed-hole state with all four owners in one
> physical response component has a rank-four response matching, hence a
> unique owner hole and a Hamiltonian owner-to-charity path.

That implication is false. Physical owner coverage and response rank are
different invariants. An owner can join the physical component through a
response into the permanent anchor while remaining unmatched by the
anchor-constrained priority selector.

## Smallest normal form

Let `c` be the sacrifice-eligible external owner and retain the permanent
anchor `r -> q`. The four-edge response graph

\[
 r\to q,\qquad q\to s,\qquad s\to\mathrm{charity},
 \qquad c\to q                                      \tag{1}
\]

is connected on all four owners and charity and contains no directed owner
cycle. The maximum matching constrained to contain `r -> q` has rank three;
it represents `r,q,s` and leaves `c` unmatched. Two physical targets remain
unmatched. The edge `c -> q` is root-facing and cannot replace the forced
anchor.

Thus (1) is neither a rank-four Hamiltonian charity path nor a saturated
rank-`|C|` represented component. Exact signed-state reconstruction preserves
this fact; reconstruction cannot increase matching rank.

## Exhaustive audit

[`audit_rank_three_exact_repeat_gate.py`](../tracks/parkability/audit_rank_three_exact_repeat_gate.py)
enumerates every nonself response graph from four owners to four owner
targets plus charity while forcing `r -> q`. For each graph it independently
selects the maximum-cardinality matching and then the protected source
priority `(q,s,c)`. It retains precisely the connected, owner-cycle-free,
rank-three states in which `c` is unmatched and root-facing.

The audit also gives a positive rational realization of the smallest graph
as a response relation: singleton target atoms have common-safety threshold
zero; every displayed edge has source value `2` above a unit floor, and every
nonedge has value `1/2`. This proves that positivity and common safety alone
do not repair the rank gap.

Across all 32,768 response graphs, exactly 208 satisfy the connected,
cycle-free, rank-three root-facing filter. Their selected matchings collapse
to only three forms:

\[
\begin{array}{lll}
s\to r,&r\to q,&q\to c_0,\\
s\to c,&r\to q,&q\to c_0,\\
r\to q,&q\to s,&s\to c_0,
\end{array}
\]

where `c_0` denotes charity and every form also contains the unmatched
root-facing edge `c -> q`. The three corresponding owner-hole pairs are
`{c,s}`, `{r,s}`, and `{c,r}`. Thus the gate is finite at the response-graph
level even though its physical packets are cap-free.

## Exact remaining theorem

To close the fixed-`U` recurrence one must now prove one of the following
from the *additional packet and GG inequalities*, not from response-graph
coverage:

1. every exact rank-three root-facing repeat gains a fourth disjoint response
   edge;
2. a connected two-hole packet exchange is EFX/lex or PI;
3. retained/support/response progress is strict; or
4. no positive rational globally lex-maximal GG state realizes the normal
   form together with the bottom-tail and split-donor inequalities.

This is a graph-level counterexample to a proposed proof implication, not a
counterexample to the fixed-`U` theorem, four-agent EFX, or general EFX.

# Adaptive-Priority Completion Target

**Status:** open conjecture and active falsification target. It is not a
theorem. The fixed-order version is rigorously false.

## Statement

Let \(V\) be a strictly positive additive instance with four agents and more
goods than agents. For an agent order \(\pi\), consider the partial EFX
allocations with exactly one unallocated good \(f\) such that

\[
v_i(X_i)\ge v_i(f)\qquad\text{for every agent }i.
\]

Choose a state whose own-utility vector is lexicographically maximal in
order \(\pi\).

> **Adaptive-priority completion conjecture.** For at least one of the 24
> agent orders \(\pi\), some \(\pi\)-lexicographically maximal state permits
> direct insertion of its floater while preserving EFX.

The quantifiers matter. An arbitrarily fixed order does not work. The claim
only asks that one order work after the instance is known.

## Why this would be a breakthrough

Berger, Cohen, Feldman, and Fiat prove that every four-agent additive
instance has a partial EFX allocation with at most one unallocated good and
that the unallocated set is not envied. In a counterexample to complete EFX,
their allocation would leave exactly one good. Therefore the family being
maximized above is nonempty.

If the adaptive-priority conjecture holds, its successful lexicographic
maximum can be completed directly, contradicting nonexistence. Hence it
would prove:

> Every finite four-agent positive-additive instance admits a complete EFX
> allocation.

The usual open-set perturbation then extends the result to nonnegative
additive valuations. This would resolve the smallest-agent case of the
central additive-EFX problem for an arbitrary number of goods. It would not
by itself prove existence for five or more agents.

## The fixed-order obstruction

The source instance is adapted from Theorem 6.25 and Table 6.1 of Bhaskar
Ray Chaudhury's thesis,
[*Finding Fair and Efficient Allocations*](https://universaar.uni-saarland.de/bitstream/20.500.11880/31737/1/thesis.pdf).
The strictly positive, bundle-nondegenerate lift is

```text
    1     2     4     8    16    32  6208  4224   256
16385  4098 24580  4104    16 34848 31808   128  2304
10241     2 18436  8200 20496    32 29760   128  6400
    1     2     4     8 18448 20512 19520   128  4352
```

For every order beginning with agent 0, the unique lexicographic maximum is

\[
X_0=\{6,7\},\quad X_1=\{1,2,3\},\quad
X_2=\{0,4\},\quad X_3=\{5\},\quad f=8.
\]

It is strictly EFX, strictly dominates the floater for every agent, and is
blocked at all four hosts. Exact replay finds 322 eligible states and 103
complete EFX allocations. No complete EFX allocation gives agent 0 utility
as high as this state.

This blocks the six orders starting with agent 0. All 18 orders starting
with agents 1, 2, or 3 have an insertable lexicographic maximum, so the
adaptive conjecture survives.

## Adversarial evidence

A two-stage 15,000-step continuation starting from the obstruction:

- retained 6 blocked and 18 insertable orders;
- increased the eligible-state census from 322 to 612; and
- reduced the largest normalized rescue margin from \(0.3163\) to
  \(0.002263\).

The optimized integer matrix is

```text
  245  1910  1903    80   881    25  2716  2808   183
23979  1390 21394     5     1 29351 15642 25780   729
 7847     1 13208 13185 13910  3155  2311 27100 12978
    3   679  4089  9088  7984 17048 15728  6900  1456
```

An independent exact enumeration of the one-unallocated EFX states confirms
the 18/6 order split. Near-zero positive margins are not evidence of a
theorem: they may indicate either a complementary handoff or an
as-yet-uncrossed counterexample wall.

## First-agent compression

The 24 priority orders split into four groups of six according to their first
agent. Call a first agent *rescued* when at least one of its six orders has an
insertable lexicographic maximum. The adaptive-priority conjecture is exactly
the assertion that at least one first agent is rescued.

This grouping exposes the current boundary more clearly than the raw
24-order count. In the fixed-order counterexample and in both recorded
all-order annealing endpoints, agent 0 is unrescued in all six orders while
each of agents 1, 2, and 3 is rescued in all six. Thus every hard endpoint
has the exact group pattern

\[
(0,6,6,6).
\]

This is evidence, not a theorem. The strengthened falsification milestone is
now a profile with two distinct unrescued first agents, equivalently at least
12 blocked orders drawn from two complete first-agent groups. The shared
evaluator reports first-agent counts and margins directly, and the exact
CEGAR accepts repeatable `--first-agent` filters so that a selected pair can
be closed or witnessed without simultaneously forcing the other 12 orders.
An UNSAT endpoint still closes only the fixed candidate-identity cell.

The first two exact pair probes demonstrate both the value and the present
limit of this compression.  For the seed-93 candidate identities, the
agent-0/agent-1 cell closed UNSAT in Z3 after eight CEGAR iterations and
4,328 learned rivals.  Shrinking produced an 18-rival core that is UNSAT in
both Z3 and cvc5 1.3.3; cvc5 solved the normalized compact formula in 10.8
seconds.  This is a dual-solver exclusion of that fixed cell, not of every
possible candidate identity.  A second shrink removes item-value
distinctness and all but 35 individual state premises: the resulting
53-assumption core consists of 28 EFX inequalities, five failed-insertion
conditions, two floater-nonenvy inequalities, and the same 18 rival
blockers.  It is deletion-minimal in Z3 and independently UNSAT in cvc5 in
4.5 seconds.  This is the current analytic-lemma extraction target.  The
analogous agent-0/agent-2 cell ended
`MASTER_UNKNOWN` with 7,017 rivals and proves nothing either way.  The
hash-pinned ledger and compact formulas are rooted at
[`adaptive_priority_first_agent_pair_gate.json`](adaptive_priority_first_agent_pair_gate.json).

The first Hall-style extraction is exact but not yet human-sized.  Across
the 23 disjunctive witness conditions, local propagation forces only two
inequalities and then stops.  A witness-choice CEGAR learns 1,268 exact
linear-arithmetic conflicts; greedy deletion leaves 955, with conflict
arity ranging from two through five.  Conflicts of arity at most four still
admit a witness assignment, while including the 55 five-way conflicts
closes UNSAT.  Thus direct case transcription is not the desired lemma.
The next conversion step is to quotient these conflicts by row-local
preference-cycle or inequality templates.  Exact counts and the two forced
anchors are in
[`adaptive_priority_first01_hall_gate.json`](adaptive_priority_first01_hall_gate.json).

## Simultaneous-cell result and analytic conversion

The exact all-order search has now been run on five distinct candidate
cells whose blocked-state premises are jointly feasible. In each cell, the
candidate states can all be EFX, floater-nonenvying, and blocked
simultaneously, but they cannot also remain lexicographic maxima for their
24 associated priority orders:

| Seed cell | Distinct candidates | Learned rival clauses | Exact endpoint |
|---|---:|---:|---|
| trace92, iteration 5 | 4 | 420 | UNSAT |
| trace93, iteration 7117 | 6 | 309 | UNSAT |
| trace93, iteration 7244 | 6 | 448 | UNSAT |
| trace93, iteration 9744 | 5 | 964 | UNSAT |
| trace93, iteration 9884 | 5 | 660 | UNSAT |

These are fixed candidate cells, not an exhaustive theorem. The first cell
has a particularly small deletion-minimal core: two candidate states and
one takeover allocation. That core converts to the
[forced singleton-swap handoff lemma](FORCED_SINGLETON_SWAP_LEMMA.md), an
analytic statement valid for arbitrary goods and weak EFX.

In its abstract form, one state gives two goods \(p,q\) to agent \(a\) and
a good \(t\) to agent \(d\). A second state splits \(p,q\) as singleton
bundles between \(a,c\) and places \(t\) in agent \(b\)'s nonsingleton
bundle. Three failed direct insertions force

\[
v_a(p)>v_a(q)
\quad\text{and}\quad
v_c(q)>v_c(p).
\]

Swapping the singleton goods therefore preserves EFX and floater nonenvy
while strictly improving the second state in priority order
\((b,a,c,d)\). This is the first human proof lemma extracted from the
all-orders CEGAR handoff rather than merely a computational near-wall.

An exact census of the two annealing traces contains 44 improvement records
and 26 distinct candidate-identity cells. Only five cells permit all of
their candidate states to be blocked simultaneously; the table above is
exactly those five, and all five close once lex-maximality is imposed. This
is a complete audit of the recorded traces, not of the combinatorial
universe of possible candidate cells.

## Exact artifacts

- Positive generic fixed-order counterexample:
  [lexmax_partial_counterexample_4x9.json](lexmax_partial_counterexample_4x9.json)
- Counterexample replay:
  [`audit_lexmax_counterexample.py`](../tracks/parkability/audit_lexmax_counterexample.py)
- All-orders optimized search:
  [lexmax_all_orders_anneal_4x9_seed93.json](lexmax_all_orders_anneal_4x9_seed93.json)
- Exact 24-order replay:
  [lexmax_all_orders_seed93_exact_replay.json](lexmax_all_orders_seed93_exact_replay.json)
- Shared all-orders evaluator:
  [`fast_count.py`](../tracks/parkability/fast_count.py)
- Adversarial driver:
  [`anneal_lexmax_all_orders.py`](../tracks/parkability/anneal_lexmax_all_orders.py)
- Simultaneous exact CEGAR:
  [`run_adaptive_priority_cegar.py`](../tracks/parkability/run_adaptive_priority_cegar.py)
- Compact five-state-cell core:
  [adaptive_priority_seed93_compact_core.json](adaptive_priority_seed93_compact_core.json)
- Exact 44-record trace-cell census:
  [adaptive_priority_trace_cell_census.json](adaptive_priority_trace_cell_census.json)
- Forced singleton-swap theorem and proof:
  [FORCED_SINGLETON_SWAP_LEMMA.md](FORCED_SINGLETON_SWAP_LEMMA.md)
- Symbolic reconstruction audit:
  [`audit_forced_singleton_swap_lemma.py`](../tracks/parkability/audit_forced_singleton_swap_lemma.py)

## Ordered proof gates

1. Seek a structurally distinct fixed-cell witness with two unrescued first
   agents.  The seed-93 agent-0/agent-1 cell is now dual-solver UNSAT, while
   its agent-0/agent-2 probe is inconclusive.  Then extend any witnessed
   first-agent set toward all four; only a four-group witness refutes the
   conjecture.
2. Quotient the 955-conflict Hall diagnostic by row-local preference-cycle
   or inequality templates.  Direct case transcription and unit propagation
   are now closed as concise-proof routes for this cell.
3. Enumerate and canonicalize exchange motifs in deletion-minimal UNSAT
   cores from structurally different feasible cells.
4. Generalize the forced singleton-swap proof to bundles connected by one
   good transfer, then prove that every all-orders-blocked family contains
   one covered motif.
5. Only an analytic argument valid for an arbitrary number of goods would
   establish the four-agent breakthrough. Fixed-\(m\) experiments remain
   falsification and lemma-discovery tools.

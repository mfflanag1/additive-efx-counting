# Lex-Max Partial-Completion Target for \(4\times9\)

**Status:** **refuted at \(4\times9\)** by a strictly positive,
bundle-nondegenerate additive instance. This route cannot prove complete EFX,
even in the first open cell.

## The proposed lemma

Fix an ordering \(a_0,a_1,a_2,a_3\) of four agents. Consider all partial EFX
allocations of eight of nine positive-additive goods such that the one
unallocated good \(f\) is not envied as a singleton:

\[
v_i(X_i)\ge v_i(f)\qquad\text{for every agent }i.
\]

Order these states lexicographically by

\[
\bigl(v_{a_0}(X_{a_0}),v_{a_1}(X_{a_1}),
      v_{a_2}(X_{a_2}),v_{a_3}(X_{a_3})\bigr).
\]

> **Refuted lex-max completion lemma.** A lexicographically maximal state
> in this family permits the direct insertion of \(f\) into some bundle
> while preserving EFX.

The direct-insertion test for host \(h\) is exact. Because the base is
already EFX, insertion succeeds if and only if every observer \(i\ne h\)
satisfies

\[
v_i(X_i)\ge
v_i(X_h)+\max\{0,v_i(f)-\min_{g\in X_h}v_i(g)\}.
\]

## Why the lemma would have proved complete EFX at \(4\times9\)

Berger, Cohen, Feldman, and Fiat prove that every four-agent
positive-additive instance has a partial EFX allocation with at most one
unallocated good, and that no agent envies the unallocated set
([arXiv:2102.10654](https://arxiv.org/abs/2102.10654)).

Assume for contradiction that a \(4\times9\) instance has no complete EFX
allocation. Nonexistence is open: for every complete allocation, retain one
strictly violated EFX inequality and perturb the valuation matrix slightly.
Thus a counterexample may be assumed to have distinct values for every two
different bundles of an agent.

Apply the almost-full theorem. The resulting partial allocation must leave
exactly one good \(f\), and nondegeneracy makes
\(v_i(X_i)>v_i(f)\) strict. Choose a lexicographically maximal such state.
If the candidate lemma holds, insert \(f\) and obtain a complete EFX
allocation, a contradiction.

All four base bundles would be nonempty. If an agent owned the empty bundle,
positivity and EFX would force every other bundle to be a singleton, which
could allocate at most three of the eight base goods.

The ordered bundle-size vector is therefore a positive composition of eight
into four parts. There are only

\[
\binom{7}{3}=35
\]

such vectors. Relabeling the goods makes \(f=8\) and makes each owned bundle
a canonical interval. Consequently, the lemma reduces to 35 exact
QF_LRA cells. Their shape census is:

| unordered shape | ordered cells |
|---|---:|
| \(5+1+1+1\) | 4 |
| \(4+2+1+1\) | 12 |
| \(3+3+1+1\) | 6 |
| \(3+2+2+1\) | 12 |
| \(2+2+2+2\) | 1 |
| **total** | **35** |

This is a finite reduction of the entire \(4\times9\) theorem, not merely
the favorite-\(2+1+1\) valuation cell.

## Exact counterexample

Chaudhury's thesis gives a four-agent, nine-good additive obstruction to the
lexicographic-potential method (Theorem 6.25 and Table 6.1 of
[*Finding Fair and Efficient Allocations*](https://universaar.uni-saarland.de/bitstream/20.500.11880/31737/1/thesis.pdf)).
Starting from that table, replace every entry by

\[
v'_i(g)=1024v_i(g)+2^g.
\]

The resulting strictly positive valuation matrix is

```text
    1     2     4     8    16    32  6208  4224   256
16385  4098 24580  4104    16 34848 31808   128  2304
10241     2 18436  8200 20496    32 29760   128  6400
    1     2     4     8 18448 20512 19520   128  4352
```

The perturbation makes every two distinct bundles have different value for
every agent: the low-order term is the subset's unique binary mask, while
1024 exceeds the sum \(1+2+\cdots+256=511\).

Leave good 8 unallocated and allocate

\[
X_0=\{6,7\},\quad X_1=\{1,2,3\},\quad
X_2=\{0,4\},\quad X_3=\{5\}.
\]

Exact exhaustive replay gives:

- 322 one-unallocated EFX states whose floater is not envied;
- \(X\) is their unique lexicographic maximum for agent order
  \((0,1,2,3)\);
- the utility vector is \((10432,32782,30737,20512)\);
- the minimum base-EFX slack is 974;
- the four best insertion slacks are
  \((-5423,-2299,-2288,-2066)\), so every direct insertion fails; and
- there are 103 complete EFX allocations, but the largest utility agent 0
  receives in any of them is only 6464.

This is a robust counterexample to the proposed lemma, not a counterexample
to EFX existence. The frozen record is
[lexmax_partial_counterexample_4x9.json](lexmax_partial_counterexample_4x9.json);
[`audit_lexmax_counterexample.py`](../tracks/parkability/audit_lexmax_counterexample.py)
replays all \(9\cdot4^8\) partial assignments, all \(4^9\) complete
assignments, the strict slacks, and full subset nondegeneracy.

The instance does **not** refute an existential-order weakening. Its
lexicographic maximum is blocked for the six orders beginning with agent 0,
but insertable for all other 18 agent orders. Thus the precise surviving
question is whether every instance has *some* agent order whose maximum is
insertable. That statement is now a falsification target, not a claimed
lemma.

A 15,000-step two-stage adversarial continuation kept exactly 18 insertable
orders but drove the largest surviving normalized insertion margin from
\(0.3163\) to \(0.002263\). Exact integer replay still finds 18 insertable and
6 blocked orders. This near-wall behavior is useful evidence for a
complementary handoff, but it is neither a proof nor a counterexample:
[lexmax_all_orders_anneal_4x9_seed93.json](lexmax_all_orders_anneal_4x9_seed93.json).
The shared exact enumerator's 24-order replay is frozen in
[lexmax_all_orders_seed93_exact_replay.json](lexmax_all_orders_seed93_exact_replay.json).

## Historical falsification encoding

For a fixed candidate base \(X\), the master formula requires:

1. strictly positive, row-normalized additive valuations;
2. strict EFX inequalities for \(X\);
3. \(v_i(X_i)>v_i(f)\) for all agents;
4. a strict insertion failure for each of the four hosts; and
5. for every other one-unallocated assignment \(Y\), the implication

\[
\bigl(Y\text{ is EFX and its floater is not envied}\bigr)
\Longrightarrow
u(Y)<_{\mathrm{lex}}u(X).
\]

There are \(9\cdot4^8=589{,}824\) labeled partial assignments before
filtering. The CEGAR loop begins with the fixed candidate only. Every exact
rational model is exhaustively replayed over all partial assignments; all
eligible lexicographically nonlower rivals are then added to the master.

A terminal SAT model with no nonlower rival would have been an exact, strict,
open counterexample to the candidate lemma. The explicit counterexample
above now supplies that endpoint directly in the ordered \(2,3,2,1\) cell.
The incomplete \(5,1,1,1\) and \(2,2,2,2\) searches are retained only as
negative-methodology records.

## Earlier evidence and why it was insufficient

- The exact-count-four \(4\times9\) witness and every rational model learned
  by the partition CEGAR satisfy the lemma for all 24 agent orders.
- The known exact-count-four \(4\times10\) witness and three additional hard
  \(4\times10\) models also satisfy it for all 24 orders.
- A 5,000-step adversarial search drove the best normalized insertion margin
  to exactly zero but did not make it negative. Exact replay found two tied
  lex-max bases, both insertable.
- Eight hundred random strict perturbations of that zero-slack boundary
  remained insertable.
- The exact \(2\times3\) calibration cell learned one rival and then returned
  UNSAT.
- The \(4\times9\) \(1,1,1,5\) and \(2,2,2,2\) cells learned thousands
  of exact rival assignments without an endpoint.

Those tests missed the refuting ordered \(2,3,2,1\) cell. This is precisely
why falsification must range over every reduced cell before positive evidence
is promoted to a conjecture.

## Artifacts

- Exact CEGAR:
  [`run_lexmax_partial_cegar.py`](../tracks/parkability/run_lexmax_partial_cegar.py)
- Vectorized and exact adversarial audit:
  [`anneal_lexmax_partial.py`](../tracks/parkability/anneal_lexmax_partial.py)
- Zero-slack search record:
  [lexmax_partial_anneal_4x9_seed41.json](lexmax_partial_anneal_4x9_seed41.json)
- Exact positive generic counterexample:
  [lexmax_partial_counterexample_4x9.json](lexmax_partial_counterexample_4x9.json)
- All-orders adversarial continuation:
  [lexmax_all_orders_anneal_4x9_seed93.json](lexmax_all_orders_anneal_4x9_seed93.json)
- Exact 24-order replay:
  [lexmax_all_orders_seed93_exact_replay.json](lexmax_all_orders_seed93_exact_replay.json)
- \(1,1,1,5\) learned rival pool:
  [lexmax_partial_5111_pool.json](lexmax_partial_5111_pool.json)
- \(2,2,2,2\) learned rival pool:
  [lexmax_partial_2222_pool.json](lexmax_partial_2222_pool.json)

## Research consequence

The one-unallocated theorem cannot be completed for an arbitrarily fixed
agent order by maximizing the ordinary lexicographic own-utility vector and
then inserting the floater. Any viable proof must either choose the order
adaptively or permit the first agent's utility to decrease, exactly as the
complete EFX allocations in this instance do. The fixed-order CEGAR is
closed as a falsified route. Complete-allocation/Hall methods remain primary,
while the existential-order weakening receives adversarial testing only.

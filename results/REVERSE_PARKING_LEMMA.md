# Reverse Parking Lemma

**Status:** proved. The identity is already implicit in the independent
completion-first enumerator. The threshold-cycle normal form below is a new
derivation in this campaign; originality has not been checked.

First assume additive valuations. Let \(X=(X_0,\ldots,X_{n-1})\) be a
complete EFX\(_0\) allocation. For each agent \(h\), define its
**owner slack**

\[
  \sigma_h(X)=
  \min_{j\ne h}
  \left(
    v_h(X_h)-
    \left[v_h(X_j)-\min_{g\in X_j}v_h(g)\right]
  \right).
\]

The quantity is nonnegative because \(X\) is EFX\(_0\). Call
\((h,f)\), \(f\in X_h\), **owner-removable** when deleting \(f\) from
\(X_h\) leaves an EFX\(_0\) allocation of the other goods.

## Lemma

For an EFX\(_0\) allocation \(X\) and \(f\in X_h\), the pair \((h,f)\) is
owner-removable if and only if

\[
  v_h(f)\le \sigma_h(X).
\]

Consequently, parkable-deletion triples are in bijection with
owner-removable pairs in complete EFX\(_0\) allocations, and

\[
  P(V)=
  \sum_{X\in\operatorname{EFX}_0(V)}
  \sum_h
  \left|
    \{f\in X_h:v_h(f)\le\sigma_h(X)\}
  \right|,
\]

where \(P(V)\) is the number of labeled parkable triples.

### Proof

Delete \(f\) from \(X_h\). Every EFX inequality belonging to an observer
\(i\ne h\) either stays unchanged or becomes weaker: the only modified target
bundle is \(X_h\), and it loses a good. The only inequalities that can become
harder are those in which \(h\) is the observer, because its own value falls
from \(v_h(X_h)\) to \(v_h(X_h)-v_h(f)\). They all remain valid exactly when

\[
  v_h(X_h)-v_h(f)
  \ge
  v_h(X_j)-\min_{g\in X_j}v_h(g)
  \quad\text{for every }j\ne h,
\]

which is equivalent to \(v_h(f)\le\sigma_h(X)\).

Given an owner-removable pair, delete \(f\) to obtain an EFX\(_0\) base and
then park it back at \(h\); this is a parkable triple. Conversely, completing
any parkable triple gives an EFX\(_0\) allocation in which its floater is
owner-removable. The two maps preserve the labeled allocation, host, and
good, so they are inverse. ∎

## Equivalent obstruction statement

A valuation matrix has zero parkable triples if and only if every complete
EFX\(_0\) allocation is **deletion-rigid**:

\[
  \sigma_h(X)<\min_{f\in X_h}v_h(f)
  \qquad\text{for every agent }h
\]

(with the condition vacuous for an empty bundle).

This removes an unnecessary quantifier layer from the research problem.
Instead of selecting a seven-good EFX base and asking whether a deleted good
can be inserted, one may select a complete EFX allocation and ask whether one
owner has enough EFX slack to pay for one of its own goods.

## Threshold-max criterion and critical cycles

There is an even smaller existence criterion, which also makes sense for
arbitrary normalized monotone valuations. Write

\[
  \tau_i(S)=\max_{g\in S}v_i(S\setminus\{g\}),
  \qquad \tau_i(\varnothing)=0.
\]

For additive valuations this is
\(v_i(S)-\min_{g\in S}v_i(g)\). For a nonempty owner bundle \(X_h\), some
good is owner-removable if and only if

\[
  \tau_h(X_h)\ge \max_{j\ne h}\tau_h(X_j).
\]

In the additive case, the easiest good to remove is an \(h\)-least good in
\(X_h\). It is removable exactly when

\[
\begin{aligned}
\min_{f\in X_h}v_h(f)
&\le v_h(X_h)-\max_{j\ne h}\tau_h(X_j)\\
&\Longleftrightarrow
\tau_h(X_h)\ge\max_{j\ne h}\tau_h(X_j).
\end{aligned}
\]

For a general monotone valuation, choose a good \(f\in X_h\) attaining
\(\tau_h(X_h)=v_h(X_h\setminus\{f\})\). Removing \(f\) preserves all of
\(h\)'s observer inequalities exactly under the same threshold-max
condition. Every other observer's inequalities remain valid: only one
target shrinks, and monotonicity implies
\(\tau_i(X_h\setminus\{f\})\le\tau_i(X_h)\).

Thus a deletion-rigid complete EFX allocation has a graph-theoretic
signature: each owner \(h\) can choose a **critical target** \(c(h)\ne h\)
such that

\[
  \tau_h(X_{c(h)})>\tau_h(X_h).
\]

A critical target cannot be a singleton, because its threshold is zero.
Consequently the directed graph induced by nonsingleton-bundle owners has
out-degree at least one and no self-loop, so it contains a directed cycle.
At \((4,8)\) this gives an exact shape-by-shape obstruction:

| shape | rigid critical-cycle requirement |
|---|---|
| \(5111\) | impossible: there is only one nonsingleton bundle |
| \(4211\) | a forced 2-cycle between the 4- and 2-bundle owners |
| \(3311\) | a forced 2-cycle between the two 3-bundle owners |
| \(3221\) | a 2- or 3-cycle among the three nonsingleton owners |
| \(2222\) | a directed cycle among the four pair owners |

For \(4211\), with 4-bundle \(F\) and pair \(P\), rigidity is precisely

\[
  \max_h(P)>\operatorname{top3}_h(F)
  \quad\text{and}\quad
  \operatorname{top3}_p(F)>\max_p(P).
\]

For \(3311\), each triple owner must value the other triple's top two goods
more than the top two goods of its own triple. For \(2222\), an owner is
removable exactly when its pair contains one of its weakly favorite goods
in the entire instance; rigidity says every owner's strict favorite lies
outside its assigned pair.

EFX also puts every critical inequality in a narrow interval:

\[
  \tau_h(X_h)<\tau_h(X_{c(h)})\le v_h(X_h)
  =\tau_h(X_h)+\min_{f\in X_h}v_h(f).
\]

So the exchange problem is not an arbitrary preference cycle. Every strict
threshold improvement is smaller than one least-owned-good value. A
potential-maximal proof should exploit these narrow critical cycles.

## Threshold-Cycle Normal Form Theorem

For arbitrary normalized monotone goods valuations, every nonempty complete
EFX\(_0\) allocation can be transformed, by bundle rotations that preserve
EFX\(_0\), into a complete EFX\(_0\) allocation with an owner-removable
good.

Consequently,

\[
  \boxed{
  \text{a complete EFX}_0\text{ allocation exists}
  \quad\Longleftrightarrow\quad
  \text{a parkable-deletion triple exists}
  }.
\]

### Non-envied one-good normal form

For strictly positive additive valuations with \(m>n\), the normal form can
be strengthened:

> Complete EFX exists if and only if there is an EFX allocation of all but
> one good \(f\), no agent prefers the singleton \(\{f\}\) to its own bundle,
> and \(f\) can be inserted directly into some bundle while preserving EFX.

For the forward direction, apply the threshold-cycle theorem and choose an
owner-removable good \(f\) of minimum value to its owner \(h\). Let \(Y\) be
the EFX base after deleting \(f\). The bundle \(Y_h\) is nonempty. Otherwise
positivity and EFX for the empty-bundle owner would force each of the other
\(n-1\) bundles to be a singleton, although \(Y\) allocates
\(m-1\ge n\) goods.

Because \(f\) was least in \(X_h\), the nonempty remainder satisfies
\(v_h(Y_h)\ge v_h(f)\). For any other agent \(i\), choose
\(g\in X_h\setminus\{f\}\). EFX of the complete allocation gives

\[
v_i(Y_i)=v_i(X_i)\ge v_i(X_h\setminus\{g\})\ge v_i(f).
\]

Thus no agent envies the parked singleton, and reinserting it at \(h\)
recovers the complete EFX allocation. The reverse direction is immediate.

This strengthened normal form aligns the direct certificate with the
almost-full four-agent theorem: the remaining gate is not finding a
non-envied one-good partial EFX allocation, but choosing one whose floater
is directly insertable.

The obvious selection rule for that choice is false. Even at \(4\times9\),
a lexicographically maximal one-unallocated EFX allocation whose floater is
not envied need not permit any direct insertion. A strictly positive,
fully bundle-nondegenerate counterexample and exhaustive replay are recorded
in
[LEXMAX_PARTIAL_COMPLETION_TARGET.md](LEXMAX_PARTIAL_COMPLETION_TARGET.md).
Thus the normal form remains an exact equivalence, but it cannot be reached
by monotonically improving the ordinary lexicographic vector of agents'
own-bundle utilities.

### Proof

Start from a nonempty complete EFX\(_0\) allocation \(X\). Ignore owners of
empty bundles; their bundle threshold is zero.

If some owner \(i\) has

\[
  \tau_i(X_i)\ge\max_j\tau_i(X_j),
\]

the threshold-max criterion says a good attaining \(\tau_i(X_i)\) is
removable, and we are done. Otherwise choose for every nonempty-bundle owner
\(i\) a target \(c(i)\) maximizing \(\tau_i(X_j)\). Every choice is strict:

\[
  \tau_i(X_{c(i)})>\tau_i(X_i),
  \qquad c(i)\ne i.
\]

A strict target cannot be empty because monotonicity and normalization give
\(\tau_i(X_i)\ge0=\tau_i(\varnothing)\). Hence the functional digraph on
nonempty-bundle owners contains a directed cycle. Rotate the bundles along
that cycle, so each cycle agent \(i\) receives \(X_{c(i)}\). The multiset of
bundle contents is unchanged. Off-cycle agents retain their own bundles,
hence all of their EFX inequalities remain valid. A cycle agent \(i\) now
owns a bundle satisfying

\[
  v_i(X_{c(i)})
  \ge \tau_i(X_{c(i)})
  = \max_j\tau_i(X_j),
\]

so it too satisfies every EFX inequality after the rotation.

Now use the finite potential

\[
  \Phi(X)=\sum_i\tau_i(X_i).
\]

Every cycle agent's summand strictly increases, and every off-cycle summand
is unchanged. Thus the rotation strictly increases \(\Phi\). There are only
finitely many labeled allocations, so rotations cannot continue forever.
At termination some nonempty-bundle owner is threshold-maximal and therefore
has a removable good.

Deleting that good yields an EFX\(_0\) base and parking it back recovers the
complete allocation, proving the forward implication. The reverse
implication is immediate from the definition of a parkable triple. ∎

`core.threshold_cycle_normal_form` implements the constructive proof for
positive additive matrices and checks EFX preservation, strict potential
growth, and the terminal removable pair. The literal regression currently
covers all 240 EFX allocations arising from the 64 positive \(2\times3\)
matrices over \(\{1,2\}\), plus a directed \(4\times8\) instance on which a
three-agent threshold rotation raises the potential from 31 to 42.

### Research consequence

Parkable deletion is an exact normal form for EFX existence, not a strictly
stronger bridge. A zero-parkability matrix would necessarily have **zero**
complete EFX allocations. Conversely, proving parkability at \((4,8)\)
would prove the original open \((4,8)\) EFX cell with no loss.

For computation, the direct certificate universe is therefore the
\(4^8=65{,}536\) complete allocations, rather than the
\(8\cdot4^7\cdot4=524{,}288\) labeled deletion/base/host triples. An exact
counterexample master may negate complete EFX allocations directly; any
SAT-zero candidate is automatically a genuine additive-EFX counterexample,
and any global UNSAT proof establishes both EFX existence and parkability.

## Bundle-partition matching formulation

Fix an unlabeled partition

\[
  \mathcal B=\{B_0,\ldots,B_{n-1}\}
\]

of all goods into \(n\) nonempty bundles. Define a bipartite graph between
agents and bundles by putting edge \(iB_b\) exactly when

\[
  v_i(B_b)\ge \max_{c\ne b}\tau_i(B_c).
\]

An assignment of the fixed bundles to the agents is EFX\(_0\) if and only if
every assigned agent--bundle pair is an edge. Hence EFX allocations supported
on \(\mathcal B\) are in bijection with perfect matchings of this feasibility
graph.

This makes the threshold-cycle proof a top-trading-cycle statement inside a
fixed perfect-matching instance. If an assigned owner is not
threshold-maximal, direct it to a threshold-maximizing bundle. A directed
cycle rotates matched bundles, stays within the feasibility graph, and raises
the threshold potential.

At \((4,8)\), positivity rules out empty bundles in an EFX allocation. There
are only

\[
 S(8,4)=1{,}701
\]

relevant unlabeled partitions:

| shape | partitions |
|---|---:|
| \(5111\) | 56 |
| \(4211\) | 420 |
| \(3311\) | 280 |
| \(3221\) | 840 |
| \(2222\) | 105 |

A counterexample is equivalently a valuation matrix for which all 1,701
feasibility graphs are Hall-deficient. `lra_master.add_partition_obstruction`
encodes each graph with 16 shared edge variables and excludes its 24 perfect
matchings. `run_partition_lra.py` builds the complete exact QF_LRA master.
This is logically equivalent to negating all 40,824 onto allocations, but it
shares the 96 agent/bundle threshold comparisons within each partition.

## Favorite-good matching lemma

For \(2n\) goods, form the bipartite graph joining each agent to all of its
weakly favorite goods. If this graph has a matching saturating the agents,
then an EFX\(_0\) allocation exists.

Indeed, give each agent its matched favorite and pair the \(n\) unmatched
goods arbitrarily with the \(n\) matched goods. Agent \(i\)'s pair is worth
at least \(v_i(t_i)\), where \(t_i\) is its favorite. The EFX threshold of
every other pair is the value of one of its goods and is therefore at most
\(v_i(t_i)\). Thus every observer satisfies every EFX inequality.

Consequently, an additive EFX counterexample at \((4,8)\) must already have
a Hall-deficient agent--favorite-good graph. Since every agent has a
favorite, a deficient set has size two, three, or four. This gives a global
contested-peak reduction before any bundle partition is chosen.
`core.favorite_pair_allocation` implements the construction.
`ParkabilityLRAMaster(require_favorite_hall_deficiency=True)` encodes its
exact negation by ruling out all \(8P4=1{,}680\) favorite-good matchings.
Exhaustive tests cover all 256 positive binary \(2\times4\) matrices, plus
four-agent matched and deficient controls.

### Four generic favorite cells

Nonexistence is open in normalized valuation space. If \(V\) has no EFX
allocation, choose one strictly violated inequality for each of the finitely
many allocations. A sufficiently small perturbation preserves positivity
and every chosen violation, while making the eight entries in each row
pairwise distinct. Hence any counterexample implies a counterexample with a
unique favorite good for every agent.

For unique favorites, failure of the favorite-good matching condition simply
means that the four favorite labels are not all distinct. Up to relabeling
agents and goods, their multiplicities have only four forms:

| type | canonical strict favorite pattern |
|---|---|
| \(4\) | \((0,0,0,0)\) |
| \(3+1\) | \((0,0,0,1)\) |
| \(2+2\) | \((0,0,1,1)\) |
| \(2+1+1\) | \((0,0,1,2)\) |

Therefore closing these four open polyhedral cells closes the unrestricted
positive-real problem; ties do not require separate terminal cells.
`add_strict_favorite_pattern` supplies the exact inequalities, and
`run_partition_lra.py --favorite-pattern ...` emits a formula for an
individual cell. No DoubleLex constraint should be composed mechanically
with a fixed canonical pattern unless orbit completeness of the combined
symmetry restrictions is checked separately.

The optional `--favorite-pattern-stabilizer` is safe: it lexicographically
orders only agents sharing the same prescribed favorite and only columns
unused by the pattern. Those permutations preserve the selected cell, unlike
unrestricted DoubleLex.

If the type-\(4\) cell remains difficult, genericity gives a second exhaustive
split. Conditional on all agents strictly ranking good 0 first, their four
strict second-favorite labels among goods \(1,\ldots,7\) have, up to
relabeling, one of five types:

\[
1+1+1+1,\quad 4,\quad 3+1,\quad 2+2,\quad 2+1+1.
\]

The canonical second patterns are respectively
\((1,2,3,4),(1,1,1,1),(1,1,1,2),(1,1,2,2),(1,1,2,3)\).
`--second-favorite-pattern` encodes these strict two-good ranking prefixes,
and `--ranking-prefix-stabilizer` orders only agents and unused goods that
preserve the full prefix cell.

### Preliminary literature check

The ingredients have close precedents, but the exact normal form has not
yet been located:

- Akrami et al., *EFX Allocations: Simplifications and Improvements*
  ([arXiv:2205.07638](https://arxiv.org/abs/2205.07638)), define an
  EFX-feasible bundle using the maximum one-good-removed value.
- Ashuri, Gkatzelis, and Sgouritsa, *EF2X Exists for Four Agents*
  ([arXiv:2412.00254](https://arxiv.org/abs/2412.00254)), call a bundle
  maximizing that value **EFX-best** and explicitly observe that every
  EFX-best bundle is EFX-feasible. Their Lemma 3.38 also constructs the
  agent--bundle feasibility graph and invokes Hall's theorem to obtain a
  fair assignment. The fixed-partition matching formulation above should
  therefore be treated as standard machinery, not a novelty claim.
- Akrami et al., *A Counterexample to EFX*
  ([arXiv:2604.18216](https://arxiv.org/abs/2604.18216)), use the standard
  ordinary-envy-cycle reassignment as a sound search reduction, but a text
  search of the current paper did not reveal an EFX-best-cycle or
  owner-removal normal form.

The new step here is to orient the owners of an already EFX allocation
toward EFX-best bundles, rotate a directed cycle, and use the sum of
owner-assigned best-one values as a finite strict potential. This check is
preliminary rather than a novelty proof; broader citation and author checks
are still required before claiming originality.

## Near-zero chambers and a falsified floor

The exact no-universal-minimum search on 2026-07-29 produced

```text
13  54   2  81  31   3  77 231
22  69   2  40  77   5 127 150
 8  69   2 243  45   1 109  15
66 246  11 586 170   4 360  33
```

It has seven complete EFX\(_0\) allocations and eight owner-removable pairs:
five remove good 2 and three remove good 5. Six EFX allocations have one
removable good, one has two, and every other agent-good pair is rigid. A
normalized \(L_\infty\) LRA chamber search closed radii \(0.01\), \(0.02\),
\(0.05\), and \(0.10\) around a closely related eight-triple matrix. Three
independent annealing continuations reached eight triples and did not cross
below it.

That evidence briefly suggested an eight-triple floor in the
no-universal-minimum case. The exact chamber search promptly **falsified** it:
another radius-\(0.05\) run produced a six-triple rational matrix, and a
subsequent independently checked descent produced the following five-triple
matrix:

```text
 1421 17121 8750   2177 21588  32 30028 36963
    1 13400 5411  65857 42189 356 55887 53059
16915 73647 26095 207288 121230 58 210653 170674
    7 34784 9282 118071 83242  33 118120 108781
```

The literal base-first and completion-first enumerators both report exactly
five triples. The complete EFX\(_0\) count is four. Four triples delete good
5 from one base and park it at the four hosts; the fifth deletes good 0.
There is no universal-minimum good. An exact normalized radius-\(0.01\)
LRA chamber around this matrix closed after 224 pooled triples. A
radius-\(0.05\) continuation remained inconclusive after 100 refinements and
5,600 triples.

This is a useful failed conjecture, not a setback to the target: parkable
deletion only needs \(P(V)>0\). It shows that a proof cannot budget a fixed
factor-eight multiplicity. No positive floor stronger than one is currently
claimed.

## Shape-\(5111\) corollary

If a complete EFX\(_0\) allocation has one nonsingleton bundle and all other
bundles are singletons, then **every good in the nonsingleton bundle is
owner-removable**. Every other bundle has EFX threshold zero for that owner,
so its owner slack is its entire positive bundle value, which is at least the
value of each contained good.

At \((4,8)\), an EFX allocation of shape \(5111\) therefore supplies five
parkable triples. A zero-parkability matrix cannot admit this shape. There are
exactly

\[
  4\binom85 3!\cdot5=6{,}720
\]

labeled reverse certificates of this form (big-bundle owner, five goods,
singleton bijection, removable good). They can be loaded into the exact
master statically, eliminating the whole shape without waiting for candidate
models to reveal its certificates.

## Common-bottom-pair reduction

Suppose two goods \(f,g\) are the two bottom-ranked goods of every agent:

\[
  v_i(f),v_i(g)\le v_i(x)
  \quad\text{for every }i\text{ and }x\notin\{f,g\}.
\]

Let \(C\) be an EFX\(_0\) allocation of the other six goods. Two sufficient
conditions expose the mechanism seen in every current five-triple record.

1. If \(C\) has two distinct plain-envy sources \(h,k\), assign \(f\) to
   \(h\) and \(g\) to \(k\). For every observer, the inserted good is a
   minimum of its target bundle, so that target's EFX threshold becomes its
   old total value. The source inequalities supply exactly those bounds.
   The completion is EFX\(_0\), and either inserted good is removable.
2. More generally, suppose \(h\) is a source and assigning one bottom good
   \(f\) to \(h\) makes the seven-good allocation \(B\) envy-free. Assign
   \(g\) to any other bundle. That bundle contains only original goods, so
   \(g\) is its minimum for every observer; envy-freeness of \(B\) therefore
   makes the completion EFX\(_0\). Deleting \(g\) recovers \(B\), so \(g\)
   is owner-removable.

The second condition is **source equalization**. It has a transparent margin
form. Besides the unchanged non-envy inequalities among agents other than
\(h\), it asks

\[
\begin{aligned}
v_i(C_i)-v_i(C_h)&\ge v_i(f) &&(i\ne h),\\
v_h(f)&\ge \max_{j\ne h}\bigl(v_h(C_j)-v_h(C_h)\bigr).
\end{aligned}
\]

Thus \(f\) must be small enough not to destroy \(C_h\)'s source status for
the other agents, but large enough in \(h\)'s row to cure all of \(h\)'s
outgoing envy. In the five-triple matrix displayed above, deleting goods
0 and 5 leaves eight six-good EFX\(_0\) allocations, all with exactly one
source. For the allocation with source 2, adding good 5 satisfies these
two margin bounds and makes the seven-good base envy-free; good 0 then
parks at all four hosts. This explains the observed four-plus-one
certificate coupling.

The tempting lemma "every positive \(4\times6\) instance has an EFX
allocation with at least two sources" is false. Exact enumeration of

```text
18  1 11 52  6  7
16 19 18 21 16  5
13 10 14 20 13 17
18 10 11 19 14 10
```

finds 58 EFX\(_0\) allocations: 52 have one source and 6 have none. None
has two. This blocks the first sufficient condition as a proof of the
common-bottom-pair case and leaves source equalization as the live
low-count mechanism. The census is a regression in
`core.complete_efx0_source_census`.

Source equalization is not universal either. The common-bottom-pair instance

```text
14 31 18 26 31 10 31 45
 3 41  7 32 36  1 13 42
18 46 41 27 30 10 21 50
 2 44 29 31  9  8 28 45
```

has 92 EFX\(_0\) allocations after goods 0 and 5 are removed: 72 have one
source and 20 have none. No source can be equalized by either bottom good.
The full instance is nevertheless far from an obstruction, with 410
parkable triples and 280 complete EFX\(_0\) allocations. Consequently a
proof using this kernel needs a dichotomy: source equalization explains the
extremal charity chamber, while failure of equalization should force enough
slack elsewhere to obtain a different reverse certificate.

## Proof routes exposed by the lemma

1. **Critical-target cycles.** If an EFX allocation is deletion-rigid, choose
   for each nonsingleton owner \(h\) a target with strictly larger
   \(h\)-threshold. The resulting graph has one of the four cycle types
   above. A cycle exchange should be tested against a potential that
   lexicographically maximizes own-bundle thresholds or owner slacks, not
   merely utilities.
2. **Five fixed shapes.** At \((4,8)\), the complete shapes are
   \(5111,4211,3311,3221,2222\). The owner-slack condition is local to the
   owner and its critical targets, making a shape-by-shape exchange lemma
   substantially smaller than the original base-and-host formulation.
3. **Polyhedral chambers.** Once an EFX allocation and its critical targets
   are fixed, deletion-rigidity is a finite system of strict linear
   inequalities. Exact LRA can therefore falsify proposed exchange rules or
   close complete chambers without any integer value bound.
4. **Bottom-pair source-equalization dichotomy.** Source equalization exactly
   explains the current five-triple hard core but is not universal. Seek an
   exchange lemma saying either its two margin bounds hold, or their failure
   creates a removable good in another complete EFX allocation. Both the
   unconditional two-source shortcut and unconditional equalization are
   already refuted.

`tracks/parkability/independent.py::enumerate_completion_first` is a literal
machine check of the bijection, independent of the optimized base-first
enumerator.

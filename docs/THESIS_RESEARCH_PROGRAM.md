# Research program: from additive EFX counting to the existence frontier

- **Status:** internal planning memo
- **Frontier date:** 2026-07-26
- **Assumption:** a theorem-first, two-to-four-year PhD program in which the
  current paper is the candidate Chapter 1 and computation is used for
  discovery and certification, not as a substitute for an unrestricted
  theorem.
- **Convention:** EFX\(_0\) is the strong variant quantifying every good in the
  target bundle, including goods worth zero to the observer. “EFX” without a
  subscript refers to the usual positive-good convention. They coincide on the
  strictly positive instances that form the project's current core.

## Executive decision

There is a coherent PhD thesis here under the working title:

> **Counting, completion, and certification for EFX under additive
> valuations**

The thesis should not depend on solving the full additive EFX problem. Its
organizing spine should be the fixed-surplus regime \(s=m-n\), with exact
counting at \(s=3\), completion at \(s=4\), and proof-producing computation at
the first open cell \((4,8)\). These are organizing questions, not guaranteed
graduation outputs.

The unifying thesis claim is:

> Fixed surplus turns additive EFX existence and multiplicity into structured
> completion and obstruction systems; exact computation can discover,
> falsify, and certify the general lemmas governing those systems.

The graduation floor is portfolio-based: externally validate the current
paper, then produce two publishable general-\(n\) theorem chapters. A negative
structure or complexity theorem can count; a larger finite box cannot. At most
one additional chapter should depend on a cell-specific computer proof. An
all-\(n\) witness family counts as a theorem chapter only when paired with a
structural construction or classification result.

The recommended order is:

1. make the current exact-count paper the audited foundation;
2. test parkable deletion at \((4,8)\), then target the family \(m=n+4\);
3. keep the \(m=n+3\) count-\(n\) construction as the bounded hedge;
4. finish the exact-real certificate pipeline before scaling its
   proof-or-counterexample branch; and
5. use multi-floater completion as the longer-horizon route toward
   unrestricted additive valuations.

This is a barbell strategy: the near-diagonal work has publishable milestones,
while the completion and exact-real programs preserve genuine breakthrough
upside.

## What would count as success

| Level | Result | Assessment |
|---|---|---|
| Field-defining | Prove complete EFX always exists for additive goods, or give an exact additive-goods counterexample | Resolution of the central problem |
| Field-defining | Prove every positive additive instance with \(m\ge1\) has at least \(n\) complete labeled EFX\(_0\) allocations | Strictly stronger than existence |
| Major advance | Prove EFX for all additive instances with \(m=n+4\), or for four agents with arbitrary \(m\) | Strong thesis centerpiece |
| Field-defining reduction | Prove existence at \(m=n+f(n)\) for \(f(n)=\omega(1)\) | Neoh--Teh show that this would transfer to general existence |
| Strong frontier result | Settle universal existence at \((4,8)\), preferably prove its exact minimum count is four | First previously uncovered additive cell |
| Strong theory chapter | Prove the additive minimum count at \(m=n+3\) is exactly \(n\) | Natural completion of the current witness pattern |
| Supporting chapter | Classify fixed-surplus counting complexity or give a proof-producing exact-real method with a new certified cell | Valuable, but should accompany a general theorem |
| Current foundation | Six exact count-\(n\) witnesses, generalized parking, and the bounded \((4,7),K=4\) theorem | Focused paper and candidate Chapter 1, pending external review |

## Frontier audit

The statement still open is:

> Does every instance of indivisible **goods** with nonnegative **additive**
> valuations admit a complete EFX allocation?

No proof or additive-goods counterexample was found in the primary literature
through the frontier date. Recent papers continue to describe this additive
question as open; see
[Davidiuk et al. (2026)](https://arxiv.org/abs/2601.03438) and
[Afshinmehr et al. (2026)](https://arxiv.org/abs/2606.18665).

Important neighboring boundaries are:

| Regime | Current status |
|---|---|
| At most three additive agents | EFX exists: [Chaudhury--Garg--Mehlhorn](https://arxiv.org/abs/2002.05119) |
| At most \(n+3\) goods | EFX exists even for general monotone valuations: [Mahara](https://arxiv.org/abs/2107.09901) |
| At most three distinct additive valuation functions | EFX exists: [Prakash HV--Ghosal--Nimbhorkar--Varma](https://arxiv.org/abs/2410.13580) |
| All but two agents have identical additive valuations | EFX exists: [Ghosal--Prakash HV--Nimbhorkar--Varma](https://arxiv.org/abs/2301.10632) |
| Two positive additive goods types | EFX plus Pareto optimality exists: [Davidiuk et al.](https://arxiv.org/abs/2601.03438) |
| Multigraph-supported goods and cancelable valuations | EFX exists: [Afshinmehr et al.](https://arxiv.org/abs/2606.18665) |
| General monotone/submodular goods | EFX existence is false from \(m=n+5\): [Akrami et al.](https://arxiv.org/abs/2604.18216); a compact weighted-coverage example is due to [Mackenzie--Suzuki](https://arxiv.org/abs/2605.06451) |

The 2026 counterexamples do **not** use additive goods. The safe summary is:

> EFX existence is false for general monotone/submodular goods valuations but
> remains open for additive goods.

Because additive EFX is known for \(n\le3\) and general-monotone EFX is known
for \(m\le n+3\), the smallest uncovered additive cell is exactly
\((n,m)=(4,8)\). The first open near-diagonal family is \(m=n+4\).

### Counting frontier

[Neoh--Teh](https://arxiv.org/abs/2504.03951) determine the minimum number of
complete labeled strong-EFX allocations exactly as \(n!/(n-m)!\) for
\(m\le n\) and as
\(n\) for \(m=n+1\). Their general bounds at \(m=n+2\) are \(n\) and \(n^2\).
Beyond that boundary, any positive universal count lower bound is equivalent
to existence; the proposed lower bound of \(n\) is genuinely stronger.

Their conjecture of at least \(n\) allocations is false for general monotone
valuations after the 2026 counterexamples. For this program, define
\(\mathcal V^+_{n,m}=\mathbb R_{>0}^{n\times m}\), count complete labeled
allocations, use strong EFX\(_0\), and assume \(n,m\ge1\). The precise
positive-domain function is

\[
  f^+_{\mathrm{add}}(n,m)
  :=\min_{V\in\mathcal V^+_{n,m}}
    \#\{\text{complete labeled EFX}_0\text{ allocations of }V\}
  \stackrel{?}{\ge} n.
\]

On this positive domain, EFX and EFX\(_0\) coincide. The following elementary
closed-limit lemma handles zeros for unrestricted theorems.

> **Positive-to-nonnegative transfer.** If every positive \(n\times m\)
> additive instance has at least \(q\) complete labeled EFX\(_0\)
> allocations, then the same is true for every nonnegative instance.

For a nonnegative matrix \(V\), put \(V^\varepsilon=V+\varepsilon\mathbf1\)
and take any sequence \(\varepsilon_t\downarrow0\). Each \(V^{\varepsilon_t}\)
has a \(q\)-element subset of EFX\(_0\) allocations. There are finitely many
such subsets, so one subset recurs on an infinite subsequence. Every EFX\(_0\)
condition is a closed linear inequality; taking the limit preserves every
allocation in that subset. This proves the lemma. It does not transfer a
bounded-\(K\) theorem, because the perturbations leave the finite integer box.

Neoh--Teh also show that an existence theorem at
\(m=n+f(n)\) for an integer-valued \(f(n)=\omega(1)\), meaning
\(f(n)\to\infty\), would yield general existence.
This makes growing surplus a breakthrough target, not merely a distant
improvement over \(n+4\).

## Why the present project is a genuine backbone

The project supplies four kinds of leverage that most attacks on EFX do not
have together:

1. **Sparse-set targets.** The six exact count-\(n\) matrices show what a
   candidate extremal additive instance can look like at \(s=3,4,5,6\),
   including the first open cell \((4,8)\). They are upper-bound witnesses,
   not yet proved extremal.
2. **A local completion theorem.** The generalized parking inequality exactly
   characterizes when an EFX base survives insertion of one leftover good.
   The scratch multi-floater result already identifies the coupled completion
   constraints and a Hall-type sufficient condition.
3. **Geometry.** The chamber artifact shows that all six exact-count sets
   persist on full-dimensional positive neighborhoods. They are robust
   phenomena, not isolated integer coincidences.
4. **Audited exact computation.** The protected-slot CEGAR, independent CNF,
   DRAT evidence, and exact-real checkpoint give a credible starting point for
   proof-producing work.

The audit history is equally valuable. It rules out several tempting but
unsafe shortcuts: unjustified symmetry cuts, finite-box-to-real extrapolation,
naive rotation arguments, and promotion of a running solver state to a
theorem. Files under `results/` and `tracks/` remain hypothesis generators
unless their claims are independently re-established.

## Ranked research tracks

| Rank | Track | Upside | Tractability | First decisive test | Role |
|---:|---|---|---|---|---|
| 1 | Completion at \(m=n+4\) | Major advance, with a path toward full existence | Medium-high risk | Does a provably selected \(n+3\)-good EFX base always have a parkable deletion? | Primary theory spine |
| 2 | Exact count \(n\) at \(m=n+3\) | Strong theorem and direct continuation of the paper | Medium | Can an all-\(n\) count-\(n\) family be synthesized and proved without per-\(n\) tuning? | Bounded hedge |
| 3 | Charity-to-completion | Full additive existence | Very high risk | Do safe-Hall or coupled-completion selection conjectures survive exact small obstructions? | Long-horizon completion track |
| 4 | Proof-producing exact-real CEGAR | Can upgrade \((4,7)\) and independently resolve \((4,8)\) | Computationally hard but sharply specified | Can a symmetry-free master emit checked rational theory conflicts? | Certification tool |
| 5 | Chamber degree or signed index | Could prove multiplicity or existence globally | Speculative | Do exact wall crossings admit a locally conserved signed weight? | Short, gated moonshot |
| 6 | Fixed-surplus counting complexity | Solid independent theory | Medium | Does hardness persist for strictly positive values and constant \(m-n\)? | Fallback/support |

## Track 1: extend the existence diagonal

Let \(V\) be a positive additive instance with \(m=n+4\). For a good \(f\),
Mahara's theorem guarantees an EFX allocation \(B\) of the \(n+3\) goods
\(M\setminus\{f\}\). The current parking theorem says that putting \(f\) on
host \(h\) succeeds exactly when

\[
v_k(B_k)\ \ge\
v_k(B_h)+v_k(f)-\min_{g\in B_h\cup\{f\}}v_k(g)
\quad\text{for every }k\ne h.
\tag{P}
\]

The clean bridge conjecture is:

> **Parkable-deletion conjecture.** Every positive additive \(m=n+4\)
> instance has some deletion \(f\), some EFX base \(B\) on
> \(M\setminus\{f\}\), and some host \(h\) satisfying (P).

This conjecture is stronger than EFX existence: refuting it would refute this
proof route, not necessarily produce an EFX counterexample. Proving it would
settle the entire \(m=n+4\) family.

Failure has a precise certificate. For every candidate triple \((f,B,h)\),
some observer \(k\ne h\) has negative parking slack. Those observer--host
obstructions should be represented as a directed labeled graph and mined for
minimal cycles, alternating paths, and exchange moves. The goal is not merely
to show that a random base parks, but to identify a selection rule for \(B\)
whose obstruction graph cannot be sourceless.

Promising selection rules to test before trying to prove them are:

- a base produced by Mahara's potential-maximizing construction;
- a leximin or Nash-welfare-maximal EFX base within a deletion;
- a base maximizing the minimum parking slack over all deletions and hosts;
- a base lexicographically maximizing a vector of source and slack
  statistics.

No rule receives theoretical investment until exact search fails to produce a
small counterexample to the rule.

The first falsification run is finite and sharply defined. Over the positive
integer \(4\times8\), \(K\le4\) box, use a sound constraint master to search
for a matrix with zero parkable triples. For each candidate matrix, exact
enumeration scans

\[
  8\cdot4^7=131{,}072
\]

deletion allocations, retains every EFX base, and checks every host. A
dual-verified zero would kill the pure parkable-deletion route even if that
full matrix still has EFX allocations of another form.

Implementation began on 2026-07-26 in
[`tracks/parkability/`](../tracks/parkability/README.md): the current
workbench has a solver-free exact landscape evaluator, an independent literal
replay in two enumeration orders, and a symmetry-free bounded CEGAR. No
\(K=4\) terminal result is claimed.

### Fixed-surplus shape leverage

For \(n\ge4\), every complete EFX allocation with \(m=n+4\) and positive
values has no empty bundle. After omitting singleton bundles, only five
excess-good shapes remain:

\[
  5,\qquad 4+2,\qquad 3+3,\qquad 3+2+2,\qquad 2+2+2+2.
\]

For \(n=4\), these are \(5111,4211,3311,3221,2222\). This constant taxonomy is
available for every \(n\ge4\); extra agents simply hold singletons. It makes a
shape-by-shape exchange theorem plausible and gives solver cores a
human-readable target.

Simply saying that the absence of \(5111\) and \(2222\) should force one of the
three middle shapes only restates the residual \((4,8)\) problem. A useful
middle-corridor lemma must first derive new quantitative inequalities from the
absence of the two extreme shapes, then prove a middle shape under those
inequalities for a genuinely nontrivial class. Discovery data suggests that
all five shapes can matter, so no proof may discard a shape based only on
count-minimizing samples. Each proposed restriction should first be encoded
over exact reals and any decoded model exhaustively classified.

The completion theorem ladder is:

1. publish the audited one- and multi-floater characterizations with an
   algorithmic or structural extension;
2. prove parkable deletion for one new infinite class or one complete bundle
   shape, and classify minimal failures of the stronger statement;
3. prove parkable deletion for \(n=4\), thereby settling \((4,8)\), or abandon
   that bridge and settle \((4,8)\) through a direct five-shape theorem;
4. lift to \(m=n+4\) for all \(n\);
5. pursue four agents with arbitrary \(m\) or a diverging-surplus theorem.

## Track 2: settle the first unknown counting diagonal

The horizon theorem is

\[
  f^+_{\mathrm{add}}(n,n+3)=n.
\tag{C}
\]

The current project proves the upper bound for \(n=4,5,6\) by exact witnesses.
The full theorem has two logically independent halves:

1. construct a positive additive count-\(n\) instance for every \(n\);
2. prove that every positive additive instance at \(m=n+3\) has at least
   \(n\) labeled EFX allocations.

The construction problem should be treated as symbolic synthesis. Extract the
strict inequalities that preserve exactly the desired parking allocations,
solve them for \(n=4,\ldots,10\), and search for a formula in the
non-hub cross-value block. Candidate formulas should use explicit
scale-separated, permutation-killing matrices rather than an opaque
per-\(n\) optimizer output. A proof must eliminate all other allocations by
bundle-shape classes.

For the lower bound, the main routes are:

- show that Mahara's \(m=n+3\) construction has \(n\) distinct rooted outputs;
- cover valuation space with the EFX cones at multiplicity at least \(n\);
- derive \(n\) distinct completions from a controlled family of deletion
  bases;
- discover a signed topological index whose absolute value is \(n\).

The last route is deliberately speculative. Raw count parity and simple
congruences are not a sound basis for it; only an exact wall-crossing rule with
a locally conserved signed weight would justify continued work.

Proving (C) would be a strong standalone chapter even if unrestricted additive
EFX remains open. Proving the lower bound for arbitrary \(m\) would resolve the
global problem and should therefore be treated as a moonshot, not the first
deliverable.

The counting theorem ladder is:

1. an all-\(n\) count-\(n\) upper-bound construction with a symbolic kill map;
2. any new general-\(n\) multiplicity lower bound beyond mere existence at
   \(m=n+3\);
3. an exact count theorem for a nontrivial structural class;
4. the unrestricted \((4,7)\) lower bound of four;
5. the full equality \(f^+_{\mathrm{add}}(n,n+3)=n\).

## Track 3: turn charity into completion

Known partial-EFX results leave fewer than \(n\) goods unallocated
[Chaudhury et al.](https://arxiv.org/abs/1907.04596), and at most \(n-2\) for
additive or nice-cancelable valuations
[Berger--Cohen--Feldman--Fiat](https://arxiv.org/abs/2102.10654). The latter
paper's four-agent specialization leaves at most one good, which is the most
relevant starting point for a four-agent completion attack.
The scratch multi-floater theorem in this repository gives:

- an exact coupled criterion for injectively assigning the leftovers; and
- a sufficient Hall condition on the graph of individually safe
  leftover--host edges.

Fix a published partial-EFX algorithm \(\mathcal A\), and let
\(\mathcal T_{\mathcal A}(V)\) be its terminal outputs over all admissible
tie choices on instance \(V\). This makes the two nested research conjectures
precise:

> **Safe-Hall selection conjecture.** For every \(V\), some
> \((B,F)\in\mathcal T_{\mathcal A}(V)\) has a safe graph with a matching
> saturating \(F\).

> **Coupled-completion selection conjecture.** For every \(V\), some
> \((B,F)\in\mathcal T_{\mathcal A}(V)\) satisfies the exact observer-bonus
> criterion for an injective completion.

The first candidate for \(\mathcal A\) should be the
Berger--Cohen--Feldman--Fiat construction. Allowing an arbitrary partial
allocation with an empty leftover set would make either statement
tautological.

The first task is adversarial, not confirmatory: build a completion-landscape
workbench that enumerates all eligible bases for small exact instances and
asks for the smallest counterexample to each selection conjecture. It must
distinguish:

- failure of safe Hall;
- failure of the exact coupled criterion;
- success only after repartitioning base goods; and
- success of a complete EFX allocation outside the selected-base family.

If safe Hall fails often but coupled completion survives, develop an
augmenting-path theorem for the coupled inequalities. If both fail on small
instances, preserve the obstruction taxonomy and demote this route rather than
weakening the claim after the fact.

For the Berger construction, the smallest and strongest target is
\(n=4,r\le1\): prove that some reachable one-leftover terminal state parks, or
produce the minimal exact counterexample to that selection claim. A distinct
second target, using a construction allowed to leave two goods, is
\(n=4,r=2\) with two common-bottom leftovers. There the content is to force
two unenvied hosts; an acyclic envy graph guarantees only one source.

Success here would give the most direct route from the present parking theorem
to full additive existence.

## Track 4: a dual proof-or-counterexample exact-real program

There are two exact-real targets:

1. finish the current \((4,7)\) program proving at least four complete labeled
   EFX\(_0\) allocations over unrestricted positive reals;
2. prove or refute EFX\(_0\) existence at \((4,8)\), then attempt its stronger
   four-allocation lower bound.

The first target would remove the finite-\(K\) qualification from the current
paper. The second is the first open existence cell. Its existence master
should start with zero protected slots; only after that closes should it carry
the three slots needed for a tight count-four theorem.

For fixed \(n,m\), non-EFX can be witnessed by selecting one strict linear
inequality for every allocation. Normalize each positive row, then take the
minimum over the finitely many positive entries and selected strict gaps;
common scaling converts these to unit-margin real constraints. Each fixed
choice of violations yields a closed rational polyhedron. If that polyhedron
is nonempty, it has a rational feasible point; an assumed real counterexample
supplies at least one nonempty choice. This motivates an exact
SAT/linear-arithmetic program with no finite value bound. Any explicit bit
bound still needs a formally checked proof.

The `SAT` obligation depends on the target:

- for the \((4,7)\) count-four master, it must show at most three complete
  labeled EFX\(_0\) allocations;
- for the \((4,8)\) existence master, it must show zero;
- for the later \((4,8)\) count-four master, it must show at most three.

In every case a `SAT` result must provide an exact rational or integer matrix
and an exhaustive independent count. An `UNSAT` result must provide two
independent encodings and a checkable proof, preferably a Boolean proof plus
rational Farkas certificates or a proof-assistant-checked semantics layer.
Closing the positive-real \((4,8)\) existence master transfers to nonnegative
EFX\(_0\) by the closed-limit lemma above.

Warm pools, finite boxes, timeouts, and solver agreement without a proof
artifact are diagnostics only.

Solver traces should be mined for repeated small infeasible cores grouped by
the target's bundle shapes: \(4111,3211,2221\) at \((4,7)\), and the five
shapes above at \((4,8)\). The research payoff is highest if the computer
proof compresses into a human obstruction lemma that then lifts from \(n=4\)
to general \(n\).

The smallest certificate milestone is an independent, symmetry-free terminal
master whose infeasible rational theory conflicts carry checkable Farkas
multipliers, with a propositional proof over those conflicts. This is more
valuable than another long run sharing the current normalization and symmetry
code.

The sequence is mandatory: close end-to-end controls, replay the certificate
stack on the current \((4,7)\) problem, and only then authorize substantial
\((4,8)\) compute. A solver architecture without a terminal new theorem or
counterexample is not a thesis chapter.

## A short, gated geometry experiment

For each labeled allocation \(A\), the valuations for which \(A\) is EFX form
a product of polyhedral cones, one cone per observer row. The positive
valuation space is cut into finitely many chambers by bundle-comparison
hyperplanes. Universal existence is a covering statement by the allocation
cones; the \(n\)-allocation conjecture is a covering-multiplicity statement.

This creates a plausible degree-theoretic route:

1. enumerate exact adjacent chamber crossings in small cells;
2. characterize how EFX allocations enter and leave at a generic wall;
3. search for a signed local weight that cancels at every crossing;
4. compute its value in a trivial chamber.

The experiment receives at most six weeks initially. Continue only if a
nontrivial signed quantity survives exact wall-crossing tests and has a local
cancellation proof. An empirical parity pattern or a statistic that requires
global recomputation is not enough.

## Two supporting directions

### Fixed-surplus counting complexity

Neoh--Teh prove #P-completeness for counting EFX allocations, but their
hardness construction uses zero-valued goods and a surplus growing on the
order of \(\Theta(n^2\log n)\), which they relax to an \(O(n^3)\) statement.
It does not settle exact counting for strictly positive additive values at
constant \(s=m-n\).

The first-quarter feasibility question is deliberately narrow:

> Is counting complete labeled EFX\(_0\) allocations #P-complete for positive
> integer additive instances with \(m=n+3\)?

Mahara's existence theorem means this counting function never vanishes, so a
parsimonious reduction from a problem with zero-count instances is impossible.
Spend at most six weeks looking for a declared baseline-offset, metric, or
Turing reduction that preserves positivity and fixed surplus, or a structural
algorithm explaining why hardness is unlikely. If neither appears, drop this
as the designated fallback rather than expanding to a vague classification.

### Minimal-counterexample kernelization

The escalation route from \((4,8)\) to four agents with arbitrary \(m\) would
be a kernel theorem showing that any four-agent additive counterexample can be
compressed to eight goods. A more general target would compress any
\(n\)-agent counterexample to \(n+O(1)\), or at least \(O(n)\), goods. The
first credible subtarget is a safe merge or deletion lemma for goods that
never act as a critical removable minimum.

This is high risk. Merging and splitting goods changes the minimum-removal
term nonmonotonically, and fixed-cell rationality controls value magnitude,
not the number of goods. Kernelization should remain a moonshot until a safe
local reduction survives exact counterexample search.

## Proposed chapter architecture

### Graduation floor: an outcome-complete portfolio

1. **Candidate Chapter 1: sparse EFX sets.** Submit the current six witnesses,
   generalized parking theorem, and audited bounded computation for external
   review. Internal audit alone does not make it a thesis chapter.
2. **General-\(n\) completion theory.** Extend the multi-floater
   characterization with an algorithmic, complexity, matching, or obstruction
   theorem. If a universal selection conjecture is false, the replacement
   chapter must classify the failure boundary rather than merely print a
   counterexample.
3. **General-\(n\) fixed-surplus counting.** Deliver a structural all-\(n\)
   construction plus classification, a nontrivial multiplicity theorem, or
   the precise fixed-surplus complexity result.
4. **Optional certified frontier chapter.** Include \((4,7)\) or \((4,8)\)
   only if the certificate pipeline terminates in a new checked theorem or
   counterexample.

Graduation should require two substantive general-\(n\) contributions beyond
the externally validated foundation. No chapter may consist only of a larger
finite value box, more fitted witnesses, a running solver, or methodology with
no terminal result.

### Stronger thesis

Strengthen Chapters 2 and 3 to the exact theorem
\(f^+_{\mathrm{add}}(n,n+3)=n\) and a resolution of \((4,8)\), while retaining
the reusable completion/certification methods as a separate contribution.

### Breakthrough upgrade

Prove \(m=n+4\) for all \(n\), four-agent EFX for arbitrary \(m\), an
diverging-surplus theorem, the global count-\(n\) lower bound, or full additive
existence/nonexistence.

## First 90 days

Allocate researcher time provisionally as follows:

- **60% completion:** parkable deletion, obstruction graphs, and one
  general-\(n\) structural lemma;
- **25% counting hedge:** 20% on the uniform family or lower-bound ladder and
  5% on the fixed-surplus complexity feasibility probe;
- **15% certification:** an end-to-end certificate prototype, not a frontier
  compute campaign.

### Days 1--15: definitions and externalization

- Write a theorem dependency map for Mahara \(m\le n+3\), three-agent EFX,
  partial EFX with charity, and Neoh--Teh counting.
- Re-prove the single- and multi-floater criteria in a concise theory note.
- Audit and state the positive-to-nonnegative/EFX-variant transfer.
- Define one canonical JSON schema for deletion bases, parking slacks,
  obstruction graphs, bundle shapes, and exchange moves.
- Resolve the current paper's authorship metadata and prepare an external
  submission checklist.

### Days 16--45: falsify before proving

For completion, build the exact deletion-base landscape, search the
\(4\times8,K\le4\) box with a sound master, and minimize failures of each
base-selection rule. For counting, canonically relabel the \(n=4,5,6\)
witnesses, extract one strict kill map per witness, and test whether a
predeclared template can reach \(n=7\). For certification, demonstrate
independent rational theory conflicts and their checker on controls or the
current \((4,7)\) formulation.

The provisional certificate budget for this quarter is 500 CPU-hours and
100 GB of retained artifacts. A serious \((4,8)\) run requires a day-45
decision memo, a working end-to-end checker, and a new written compute/storage
budget.

### Day 45: choose, then deepen

Write a decision memo selecting one completion conjecture and one bounded
hedge. Days 46--90 deepen only those selections. Do not simultaneously launch
full \((4,8)\) CEGAR, an unrestricted family search, a geometry atlas, and a
new completion engine.

The day-90 deliverable is one reproducible package containing:

- a proved general lemma or a minimal exact counterexample to the lead
  conjecture;
- the smallest obstruction taxonomy supporting the next theorem;
- the selected hedge's binary gate artifact;
- the current paper's submission state; and
- a six-month proof plan or explicit pivot.

## Go/no-go gates

Track-specific gates are binary:

| Track | Gate artifact | Stop condition |
|---|---|---|
| Parkable deletion, day 90 | A dual-verified counterexample, or a checked \(K\le4\) closure **and** a proof for one new infinite class | If neither exists, drop canonical parkability as the primary route |
| Uniform count family, day 90 | An \(n=7\) instance produced by the predeclared template plus a symbolic kill-map schema | If absent, demote the uniform family and work on lower bounds instead |
| Certificate pipeline, day 90 | Independent symmetry-free master, checked rational conflict certificates, and end-to-end replay on a control | If absent, do not scale to \((4,8)\) |
| Chamber index, week 6 | A signed local crossing rule verified on a complete small atlas and admitting a proof sketch | If absent, end the index project |
| Fixed-surplus complexity, week 6 | A positivity-preserving reduction skeleton or a structural algorithmic invariant for \(m=n+3\) | If absent, remove it as the fallback |

Program gates are:

| Date | Required artifact | Otherwise |
|---|---|---|
| Month 3 | Current paper is submission-ready, with authorship and claim metadata resolved | Fix externalization before expanding the campaign |
| Month 6 | Current paper is submitted and one new theorem/certificate package is submission-ready | Reduce global-existence work to at most 25% |
| Month 12 | One new general-\(n\) contribution is submitted | Choose the best outcome-complete structural/complexity spine |
| Month 18 | The cell-specific track has a terminal checked result | Cap that track at 15% |
| Month 24 | Two submission-ready general-\(n\) chapters exist beyond the foundation | Re-scope the thesis with an adviser |
| Month 36 | Three defensible chapters have survived external feedback | Integrate; make any global resolution a bonus rather than a graduation dependency |

## Research standards inherited from the audit

1. State the valuation class, EFX variant, parameter cell, and numeric domain
   in every theorem.
2. Treat bounded integer, positive rational, and unrestricted nonnegative
   results as different claims until a proved transfer connects them.
3. Use only proved symmetry reductions. Keep a symmetry-free terminal
   formulation whenever feasible.
4. Verify every solver candidate with a definition-faithful exact
   implementation.
5. Require an independently checkable terminal certificate before promoting
   solver `UNSAT`.
6. Separate discovery scripts, checkpoints, and claim artifacts.
7. Maintain a counterexample ledger for every conjecture and supersede false
   statements visibly.
8. Prefer cores that suggest human lemmas over longer blind solver runs.

## Main risks and planned pivots

| Risk | Early signal | Pivot |
|---|---|---|
| Parking selection is false | Tiny exact instances defeat every natural base rule | Study coupled repartitioning or use parking only for counting constructions |
| Exact-real CEGAR does not close | Pools grow without reusable small cores | Change to branch-and-bound/Farkas or shape-decomposed masters; do not just add wall time |
| Count-\(n\) family needs opaque \(O(n^2)\) tuning | No fixed template works beyond fitted sizes | Prove an existential construction by probabilistic/linear-feasibility methods, or target a broader \(O(n)\) upper bound |
| Chamber index has no local conservation | Adjacent walls change every candidate weight inconsistently | End the experiment within six weeks |
| Literature advances overtake a parameterized target | A new paper settles the same regime | Move one rung outward using the same completion/certification machinery |
| The project accumulates only finite results | Each theorem adds a value bound or isolated cell | Require the next chapter to contain a general-\(n\), fixed-surplus, or formal reduction theorem |

## Immediate decision

For the next quarter, the primary theorem should be the parkable-deletion
bridge at \(m=n+4\), tested first at \((4,8)\). The bounded hedge should be the
all-\(n\) count-\(n\) construction at \(m=n+3\). The 15% exact-real budget
should continue the \((4,7)\) count branch and finish the certificate pipeline;
\((4,8)\) compute begins only after that gate, with existence before the
stronger four-allocation bound. The charity-to-completion and chamber-index
routes should remain strictly time-boxed moonshots.

That allocation of effort preserves a credible thesis if the global
conjecture survives and gives every successful intermediate lemma a direct
route toward a breakthrough.

# EFX(4,8) breakthrough-conversion audit

**Snapshot:** 2026-07-30 EDT  
**Current theorem:** every nonnegative additive four-agent, eight-good
instance admits a complete EFX allocation  
**Status:** internally verified bounded computer-assisted theorem; not yet
externally reproduced or peer reviewed

## Basic explanation

An EFX allocation divides all eight goods among the four agents so that, if
any agent compares its bundle with another agent's bundle after removing any
one good from the latter, the first agent does not prefer what remains.

The proof reduces a hypothetical counterexample to eight exact cases. In each
case, all 1,701 ways to split eight goods into four nonempty unlabeled bundles
are considered. A bundle can be assigned to an agent when owning it would
satisfy every EFX comparison. The split works exactly when this
agent-to-bundle graph has a perfect matching.

Lean checks the mathematical reduction. Exact arithmetic formulas say that
none of the 1,701 splits works. cvc5 produces eight proof objects and Ethos
accepts all eight. Independent parsers and a second direct-allocation
encoding check the most important representation boundaries.

## What changed in the conversion pass

### 1. The theorem now covers zero-valued goods

The earlier paper stated the result only for strictly positive weights.
That restriction has been removed.

For a fixed allocation, the weights making it EFX form a closed polyhedron.
There are finitely many complete allocations, so the set of weights admitting
some EFX allocation is closed and its complement is open. If a nonnegative
counterexample existed, adding the same sufficiently small positive
\(\varepsilon\) to every weight would leave it a counterexample while making
all weights strictly positive.

This argument is implemented in
[`Perturbation.lean`](../formal/efx48/EFX48/Perturbation.lean). The exported
nonnegative theorem is in
[`PublishedLifting.lean`](../formal/efx48/EFX48/PublishedLifting.lean).
The pinned Lean 4.32.1 build and axiom audit pass. The final theorem depends
only on `propext`, `Classical.choice`, and `Quot.sound`.

### 2. The novelty claim is narrower and better supported

The correct positioning is:

> This closes the first previously open **four-agent additive** cell beyond
> Mahara's \(m\le n+3\) boundary.

It is not the first \(m=n+4\) result. Akrami, Mayorov, Mehlhorn, Srinivas, and
Weidenbach prove the three-agent/seven-good monotone case and use certified
finite search. Their work is direct methodological precedent. The present
result is a four-agent additive analogue using exact linear arithmetic and
CPC/Ethos rather than SAT/DRAT.

The result is a real fixed-parameter theorem, but it does not resolve EFX for
four agents and arbitrarily many goods or the general additive conjecture.

Primary references:

- [Chaudhury--Garg--Mehlhorn: EFX exists for three agents](https://arxiv.org/abs/2002.05119)
- [Mahara: complete EFX through \(m\le n+3\)](https://doi.org/10.4230/LIPIcs.ESA.2021.66)
- [Berger--Cohen--Feldman--Fiat: almost-full EFX for four agents](https://doi.org/10.1609/aaai.v36i5.20410)
- [Akrami et al.: SAT/Lean frontier at \(m=n+4\) and counterexamples from \(m=n+5\)](https://arxiv.org/abs/2604.18216)

### 3. One concise analytic target is isolated

The difficult favorite-\(211\) terminal cell has favorite vector
\((0,0,1,2)\). Its 130-partition deletion-minimal UNSAT core lies inside an
invariant family of 191 partitions:

1. all 131 partitions in which good 0 is a singleton, favorite goods
   \(0,1,2\) are separated, and no nonfavorite good is a singleton; and
2. all 60 partitions into four pairs in which goods \(0,1,2\) are separated.

This yields the **anchored contested-favorite lemma**:

> For every positive normalized \(4\times8\) valuation with strict favorite
> vector \((0,0,1,2)\), distinct rows, no universal minimum, and no peelable
> pair, at least one of those 191 anchored partitions has a feasible perfect
> matching.

The current certificate proves this statement because it proves the stronger
existence claim inside a 130-partition subset. The new Lean module
[`Anchored211.lean`](../formal/efx48/EFX48/Anchored211.lean) defines the
invariant statement and proves that it alone eliminates the favorite-\(211\)
cell. What remains open is a concise human proof of the lemma.

### 4. Hall-mask compression was adversarially tested and rejected

The exact deletion-witness corpus now contains 54 witnesses. Across their
6,966 obstructed core graphs:

- there are 580 distinct feasibility-graph signatures;
- the most frequent primary Hall witness is the full four-agent set; but
- an exact set-cover calculation requires ten different nontrivial agent
  masks to cover the sample, with a unique minimum cover.

Therefore, a proof split into a few dominant Hall-agent masks is not supported
by the data. The higher-leverage route is to use the two anchored bundle
families and translate their failed edges into threshold inequalities.

The executable analysis is
[`analyze_hall_witness_patterns.py`](../tracks/parkability/analyze_hall_witness_patterns.py).
Its updated hash-bound output is
[`favorite-211.hall-patterns.json`](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/core-shrinking/favorite-211.hall-patterns.json).

## Review depth

Closed internal checks:

- full Lean build under pinned Lean 4.32.1;
- axiom audit, including the new nonnegative theorem;
- eight independent formula semantic audits;
- eight CPC proofs accepted by Ethos;
- 545,360 formula assertions matched to 545,360 CPC assumptions;
- eight-cell direct-allocation cross-check over 40,824 onto allocations per
  cell;
- deletion minimality for the 130-partition explanatory core;
- exact Hall-pattern recomputation for all 54 completed deletion witnesses;
- LaTeX build and visual inspection of every page of the revised manuscript;
- two prior independent internal adversarial reviews.

Still external:

- fair-division expert review;
- formal/certificate expert review;
- independent-machine replay; and
- ordinary peer review.

## Level of result

The appropriate classification is **a specialized research-paper theorem**:
stronger than a thesis exercise and potentially publishable as a
workshop-to-specialized-conference contribution if external review confirms
it. It is not presently a field-level breakthrough. A genuine breakthrough
conversion would require at least one of:

1. a short human proof of the anchored contested-favorite lemma that
   generalizes to the other cells;
2. an argument covering \(m=n+4\) for all \(n\) in the additive domain; or
3. a structural theorem for four agents and arbitrary numbers of goods.

## Remaining gates

1. Derive a threshold/Farkas proof of the anchored contested-favorite lemma.
2. Test the same invariant anchored-family formulation in the other seven
   terminal cells.
3. Publish the corrected immutable reviewer release and obtain an
   independent-machine replay.
4. Send the package to one fair-division expert and one
   formal-certification expert.

The revised submission source is
[`submission.tex`](../paper/efx48/submission.tex). The release PDF is rebuilt
from that source only after the remaining packaging checks pass.

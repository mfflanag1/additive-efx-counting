# Threshold-minimal bundle lemma

**Status:** cap-free analytic lemma  
**Scope:** arbitrary normalized monotone valuations; additive valuations are
not needed for the lemma itself  
**Role:** replaces atomic one-good safety by heterogeneous deletion thresholds

**Correction (2026-08-09):** Lemmas 1--2 below remain valid.  The original
two-slot alternating-cycle application was exactly refuted by a strictly
positive, subset-nondegenerate eleven-good profile.  In particular, the
structural alternating premises do not force one whole residual block that is
both threshold-safe and threshold-crossing.  See
[`threshold_two_slot_refutation_audit.json`](threshold_two_slot_refutation_audit.json).

## Threshold-safe sets

Fix nonnegative thresholds \(\tau_i\) for the agents. Call a set \(T\)
*threshold-safe* if

\[
v_i(T\setminus\{g\})\le \tau_i
\qquad\text{for every agent }i\text{ and every }g\in T. \tag{1}
\]

The thresholds need not be the agents' utilities in one common allocation.
They may instead be the minimum utilities required to tolerate a collection
of already-fixed target bundles.

## Minimal crossing theorem

> **Lemma 1.** Let \(S\) be a finite set of goods. If some agent \(k\)
> satisfies \(v_k(S)>\tau_k\), then there are an agent \(a\) and a nonempty
> subset \(T\subseteq S\) such that
>
> \[
> v_a(T)>\tau_a
> \]
>
> and \(T\) is threshold-safe.

**Proof.** Among all subsets \(R\subseteq S\) for which
\(v_i(R)>\tau_i\) for at least one agent `i`, choose an inclusion-minimal
one and call it \(T\). Choose any agent `a` crossing her threshold on
\(T\). For every \(g\in T\), the proper subset \(T\setminus\{g\}\) cannot
cross any agent's threshold, by minimality. Hence (1) holds. \(\square\)

With \(\tau_i=v_i(X_i)\), this is exactly the most-envious-subset argument
used by BCFF. The useful extension is that each \(\tau_i\) may be lower
than, equal to, or derived separately from the old own utility.

## Threshold assembly theorem

> **Lemma 2.** Let \(Y=(Y_1,\ldots,Y_n)\) be a partial allocation. If
> there are thresholds \(\tau_i\) such that
>
> 1. \(v_i(Y_i)\ge\tau_i\) for every agent `i`; and
> 2. every target bundle \(Y_j\) is threshold-safe in the sense of (1),
>
> then \(Y\) is EFX.

**Proof.** For every observer `i`, target `j`, and good \(g\in Y_j\),

\[
v_i(Y_i)\ge\tau_i\ge v_i(Y_j\setminus\{g\}).
\]

These are precisely the EFX inequalities. \(\square\)

## Alternating-cycle application

Suppose the higher-priority part of a proposed alternating escape has
already fixed disjoint bundles \(Z_1,\ldots,Z_k\). Define the terminal
threshold of every still-unassigned agent `i` by

\[
\tau_i=
\max_{j\le k}\max_{g\in Z_j}v_i(Z_j\setminus\{g\}). \tag{2}
\]

Any remaining agent who receives a bundle worth at least \(\tau_i\) will
not strongly envy a fixed target. Lemma 1 can extract a threshold-safe block
from any remaining pool that crosses some agent's threshold. Repeating the
operation on disjoint residual pools gives EFX by Lemma 2 as soon as all
agents are covered.

For the hard order `(p,q,r,s)`, the natural first fixed blocks are the
desired set \(T_r\cup\{f\}\) for `p` and the singleton `x` for `q`. The
problem becomes a two-agent matching question for `r,s`: assign the
singleton `y` and one threshold-safe subset of the remaining pool. The envy
edge `r -> s` makes `y` sufficient for `r`, while ownership makes it
sufficient for `s`. Thus only the second slot can be deficient.

## Refuted two-slot application

The former next target asserted that, after fixing `p`'s selected
top-plus-`f` block and `q`'s singleton, the residual pool must contain one
whole threshold-safe block crossing the terminal threshold of `r` or `s`.
This assertion is false.  The frozen refuting profile has:

- strictly positive values and distinct values for all subsets in every row;
- strict base EFX and charity dominance;
- the exact alternating envy and champion graphs;
- no compatible generalized cross-bottom family; and
- zero qualifying blocks among all 63 nonempty residual subsets.

The refutation is narrow.  It does not refute sequential extraction,
subpacket splitting, the full alternating escape, or complete EFX.  Indeed,
the same profile has lexicographically improving EFX reallocations obtained
by repartitioning several packets among the three later-priority agents.

## Repaired next gate

The live target is therefore an **external-observer-safe three-agent
improvement**.  Preserve the earliest singleton owner and repartition any
subcollection of the remaining goods among the other three agents.  Require
the resulting three-agent allocation to be internally EFX and every target
bundle to be deletion-safe for the preserved observer.  Under the alternating
champion and no-compatible-family premises, prove that one such partial
allocation lexicographically improves the base at the first later-priority
coordinate that changes.

This formulation permits the multiway splitting used by the exact escapes
and keeps Lemmas 1--2 as its threshold-safety primitives.  It is not yet
proved.

## Primary source connection

BCFF's definition of a most-envious agent and Lemma 3.5 motivate the
construction, but Lemmas 1--2 above are stated directly and proved
independently:

Berger, Cohen, Feldman, and Fiat,
[*Almost Full EFX Exists for Four Agents (and Beyond)*](https://arxiv.org/abs/2102.10654),
Section 2.3 and Definitions 3.1--3.4.

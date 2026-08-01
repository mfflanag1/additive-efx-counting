# One-Defect Favorite-Triple Conversion Lemma

**Status:** cap-free analytic lemma  
**Scope:** four additive agents and nine goods with a strict common favorite  
**Role:** optional conversion from a favorite triple to a favorite pair

## Stronger existence shortcut

For existence alone, the comparison assumption in this note is unnecessary.
If \(P,Q\) are safe for every agent and \(E\) has at most one rejecter
\(d\), then the original partition

\[
\{f,a,b\},\quad E,\quad P,\quad Q
\]

already supports EFX. Give the favorite triple to \(d\) (or to any agent
when \(E\) has no rejecter) and match the three pairs to the remaining
agents. This is the one-defect special case of the exact
[favorite-triple Hall characterization](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md).

The theorem below proves the additional conclusion that the same goods can
be rearranged into an EFX allocation with the favorite in a pair.

## Statement

Let \(f\) be a strict favorite of every agent and set \(F_i=v_i(f)\).
Choose two residual goods \(a,b\), and partition the other six goods into
three pairs \(E,P,Q\). Call a pair \(R\) *safe for agent \(i\)* when

\[
v_i(R)\ge F_i+\max\{v_i(a),v_i(b)\}. \tag{1}
\]

Assume:

1. \(P\) and \(Q\) are safe for all four agents; and
2. \(E\) is safe for at least three of the four agents.

If exactly one agent \(d\) rejects \(E\), also assume that \(P,Q\) can be
matched to two distinct agents in \(N\setminus\{d\}\) such that each
matched agent values its assigned pair at least as much as \(E\).

Then a complete EFX allocation exists.

More precisely:

- if \(E\) is safe for all four agents, every assignment of
  \(\{f,a,b\},E,P,Q\) is EFX;
- if exactly one agent \(d\) rejects \(E\), let \(h\in\{a,b\}\) be the
  good that \(d\) values more and let \(\ell\) be the other one. Then
  \[
  \{f,h\},\quad E\cup\{\ell\},\quad P,\quad Q \tag{2}
  \]
  admits an EFX allocation in which \(d\) receives \(\{f,h\}\), while the
  among the other three agents, the two agents in the stated matching
  receive \(P,Q\), and the remaining agent receives \(E\cup\{\ell\}\).

## Proof

If \(E\) is safe for everyone, all three pairs satisfy (1), so the
[common-low favorite-triple lemma](COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md)
applies.

Suppose instead that \(d\) is the unique agent rejecting
\(E=\{x,y\}\). Write values from \(d\)'s perspective without subscripts.
Then

\[
v(x)+v(y)<F+v(h). \tag{3}
\]

Every two-good remainder of the triple \(\{\ell,x,y\}\) is below
\(F+v(h)\). The \(x+y\) remainder is below it by (3). For either of the
other remainders,

\[
v(\ell)+v(x)<v(h)+F,\qquad
v(\ell)+v(y)<v(h)+F,
\]

because \(v(\ell)\le v(h)\) and every residual good is strictly less
valuable than \(f\). Deleting one good from \(P\) or \(Q\) also leaves a
singleton worth less than \(F\). Thus \(\{f,h\}\) is EFX-feasible for
agent \(d\).

Now fix any other agent \(i\). The pair \(E\) is safe for \(i\), so the
triple \(E\cup\{\ell\}\) has value at least \(F_i\). It is therefore
EFX-feasible against the favorite pair and against \(P,Q\), because their
one-good remainders are worth less than \(F_i\).

Suppose \(i\) is matched to \(P\). Its value is at least the right-hand
side of (1), and by assumption it is also at least \(v_i(E)\). These two
bounds dominate:

- the largest remainder \(F_i\) of the favorite pair;
- every singleton remainder of \(Q\); and
- every two-good remainder of \(E\cup\{\ell\}\).

For the last claim, the \(E\) remainder is bounded by the pair-comparison
assumption, while either remainder containing \(\ell\) is strictly below
\(F_i+\max\{v_i(a),v_i(b)\}\), since the other good is worth less than
\(F_i\). The same argument applies to the agent matched to \(Q\).

Hence the unmatched agent can own \(E\cup\{\ell\}\), while the two matched
agents can own \(P,Q\). Giving \(\{f,h\}\) to \(d\) completes an EFX
allocation. \(\square\)

## Remaining selection lemma

The proof problem is now purely combinatorial:

> **Conditional two-safe/one-almost-safe selection conjecture.** Under the
> exact universal owner-threshold envelope and a saturating half-favorite
> matching, assume no favorite-pair balanced partition supports an EFX
> matching. Then there are \(a,b\) and a perfect matching \(E,P,Q\) of the
> other six residual goods such that two matched edges have zero rejecting
> agents under (1), while the third has at most one rejecter.

The conditioning is essential: generic branch-valid profiles with
favorite-pair EFX need not contain any such cross-agent safe matching.
Either outcome already gives favorite-triple EFX by the stronger existence
shortcut. This explains the strict boundary that killed favorite-pair rank
augmentation: when its last universally safe edge is weakened, that edge
acquires one rejecter but the favorite-triple allocation remains EFX.

Proving the conditional selection conjecture closes the four-distinct-representative
side of universal threshold failure. It does not address the mixed
threshold/Hall branch or general additive EFX.

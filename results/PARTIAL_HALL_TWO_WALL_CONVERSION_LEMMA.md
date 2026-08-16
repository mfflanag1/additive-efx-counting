# Two-wall Hall conversion lemma

## Statement

Let $X$ be an eligible partial EFX allocation for nonnegative additive
valuations, with one unallocated good $f$. Choose two agents $a,c$, two
distinct goods $x,y\in X_a$, and write

\[
A=X_a,\qquad C=X_c,\qquad R=A\setminus\{x,y\}.
\]

Consider three candidate states:

1. **Direct insertion $D$:** give $f$ to agent $c$, changing $C$ to
   $C+f$.
2. **Transfer/rematch $T$:** form bundles $A-x+f$ and $C+x$, give
   $C+x$ to $a$, and give $A-x+f$ to $c$.
3. **Conversion state $Y$:** give $R+f$ to $a$, give $C+y$ to $c$,
   leave $x$ unallocated, and leave every other bundle unchanged.

Assume:

- every EFX inequality needed for $D$, except possibly
  $v_a(A)\ge v_a(C)$, holds;
- every EFX inequality needed for $T$, except possibly
  $v_a(C+x)\ge v_a(R+f)$, holds; and
- $Y$ is an eligible partial EFX allocation.

Then at least one of the following holds:

1. $D$ is a complete EFX allocation;
2. $T$ is a complete EFX allocation; or
3. $Y$ strictly improves $a$, weakly improves $c$, and leaves every other
   agent's utility unchanged. Thus $Y$ Pareto-dominates $X$. Under positive
   valuations, $c$ also improves strictly.

Consequently, if $X$ was selected to be Pareto-maximal among eligible
one-floater EFX states, the three support assumptions force a radius-one
complete EFX allocation.

## Proof

If $v_a(A)\ge v_a(C)$, all inequalities for $D$ hold by assumption, so
$D$ is EFX. If $v_a(C+x)\ge v_a(R+f)$, all inequalities for $T$ hold,
so $T$ is EFX.

Suppose both comparisons fail. Nonnegativity and additivity give

\[
v_a(A)<v_a(C)<v_a(C+x)<v_a(R+f).
\]

Thus agent $a$ strictly improves in $Y$. Agent $c$ changes from $C$
to $C+y$, so nonnegativity gives $v_c(C+y)\ge v_c(C)$. All other bundles
are unchanged, and $Y$ is eligible by assumption. Hence $Y$ Pareto-dominates
$X$. Under positive valuations, $v_c(y)>0$ makes $c$'s improvement strict as
well. This proves the trichotomy.

## Concrete $4\times9$ instance of the lemma

The frozen-cell core uses

\[
a=1,\quad c=2,\quad A=\{1,2,3\},\quad C=\{0,4\},
\quad x=2,\quad y=3,\quad f=8.
\]

Its 13 deletion-irreducible support comparisons prove the three semantic
support assumptions above. The resulting candidates are exactly the two
complete allocations and one improving partial allocation in
[`partial_hall_completion_improvement_lemma_seed17.json`](partial_hall_completion_improvement_lemma_seed17.json).

## Verification and boundary

The pure algebraic negation is
[`partial_hall_two_wall_algebra.smt2`](partial_hall_two_wall_algebra.smt2).
Both Z3 and cvc5 return `UNSAT`. The concrete 13-support implication is also
dual-verified; see
[`partial_hall_completion_improvement_lemma_seed17_cvc5.json`](partial_hall_completion_improvement_lemma_seed17_cvc5.json).

This lemma is cap-free and works for arbitrary numbers of agents and goods
with nonnegative additive valuations, but it is conditional. A four-agent
EFX proof still needs a structural
argument showing that every remaining Hall-deficient cell admits such a
choice of $a,c,x,y$, or belongs to another finite conversion type.

The exact corpus audit
[`partial_hall_two_wall_gate_corpus_audit.json`](partial_hall_two_wall_gate_corpus_audit.json)
quantifies this boundary. The lemma has two gates on the best 99.858%
near-maximal obstruction, but covers only one of six audited obstruction
profiles and does not cover the known Pareto-maximal obstruction. Thus it
must be combined with the normalized-potential selection argument or with
additional conversion lemmas.

# Endpoint hole/core-exchange selector lemma

**Date:** 2026-08-13

**Status:** cap-free exact selector for the unique path-core endpoint order;
GG does not yet force its success

## Endpoint state

Use the sole survivor of the paid-response path-core rotation lemma:

\[
 h_0\to h_1\to h_2\to h_3\to c,
 \qquad (\text{failed target},\text{source})=(h_1,h_3).
\]

After the forced rotation, cores `A_0,A_1,A_3` expose the rank-three path

\[
 h_0\to h_1\to h_3\to c,
\]

while `h_2` still holds `A_2+R_2` and the hole owner `h_0` holds `P`.
Let `b_0,b_2` contain every protected payment and observer-surplus floor
that must survive the splice.  The current state is feasible:

\[
 v_0(P)\ge b_0,
 \qquad v_2(A_2+R_2)\ge b_2.                     \tag{1}
\]

## Complete exchange family

Let

\[
 \mathcal H=\{H\subseteq A_2:
 v_2(H)>v_2(X_2),\ H\text{ is base-common-safe}\}.
\]

The family is nonempty because `A_2 in mathcal H`.  For every `H in
mathcal H` and `K subseteq P`, form

\[
 B_0(H,K)=(P\setminus K)+H,
 \qquad
 B_2(H,K)=R_2+(A_2\setminus H)+K.                \tag{2}
\]

This ranges over every two-packet alteration of the returned hole bundle
that moves a desired middle-owner core into the hole.  No item or value cap
is imposed.

Define the middle-feasible family

\[
 \mathcal F=\{(H,K):H\in\mathcal H, K\subseteq P,
 v_2(B_2(H,K))\ge b_2\}.                         \tag{3}
\]

## Exact trichotomy

1. **Rank-completing exchange.**  If some `(H,K) in mathcal F` also obeys

   \[
   v_0(B_0(H,K))\ge b_0,                          \tag{4}
   \]

   use (2).  Core `H` supplies the missing edge `h_2 -> h_0`; together
   with the three retained edges this gives the rank-four Hamiltonian path
   `h_2 -> h_0 -> h_1 -> h_3 -> c`.  All named protected floors and
   physical disjointness are preserved.
2. **Middle exhaustion.**  If `mathcal F` is empty, then every desired
   deletion from `A_2` costs more in row `h_2` than the entire returned
   hole packet can replace:

   \[
   v_2(H)>v_2(A_2+R_2+P)-b_2
   \qquad(H\in\mathcal H).                       \tag{5}
   \]
3. **Hole separator.**  If `mathcal F` is nonempty but (4) fails for every
   member, then

   \[
   v_0(K)-v_0(H)>v_0(P)-b_0
   \qquad((H,K)\in\mathcal F).                   \tag{6}
   \]

   Thus every packet that compensates the displaced middle owner consumes
   more than the complete hole-owner surplus even after crediting the moved
   desired core.

The alternatives are finite, disjoint, and exhaustive.  They replace the
generic phrase “alter the hole packet” by one exact optimized operation and
two explicit two-row inequalities.

## Necessity of a stronger GG inequality

The exact audit contains a positive-rational local model satisfying (1),
base common safety of `A_2`, current safety of `P`, inclusion-minimality of
both protected bundles, and nonempty `mathcal F`, but every feasible exchange
satisfies (6).  Therefore the endpoint exchange is not forced by payment,
safety, positivity, or minimal trimming alone.

To eliminate this separator one must import an identity-specific GG
inequality for one of the six anchored orders, permit a priority-valid
sacrifice of `b_0` or `b_2`, or recruit a packet outside `P+A_2+R_2`.
Repeating residual-only redistribution cannot address (6).

## Claim boundary

This lemma proves the complete cap-free exchange selector, rank-completion
when it succeeds, and the exact failure polarities.  Its rational model is
local, not a globally lex-maximal GG countermodel.  It does not eliminate
(5)--(6) from the flower inequalities, handle residual-essential repeated
responses, close GG, or prove four-agent/general additive EFX.

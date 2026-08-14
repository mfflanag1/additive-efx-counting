# Normalization-bypass three-reservoir fan dichotomy

**Date:** 2026-08-13

**Status:** cap-free PI closure of the entire all-unsafe reservoir fan

## Input

Use the normalization-bypass reservoir-reversal lemma at one exact current
state `Z^-`.  Let `E` be a globally minimum current-safe response desired by
source `s`, and suppose `E` is contained in one physical target.  Let
`U_1,U_2,U_3` be the three current owner bundles disjoint from that target.
Write `b_i=v_i(Z^-_i)` and retain the typed normalization premise

\[
b_i\ge v_i(X_i)\qquad(i\in N),                    \tag{0}
\]

where `X` is the globally lexicographically maximal base.

For each `U_k`, run the minimal-threshold construction at the corresponding
owner's threshold against `E`.  This theorem concerns the branch in which
all three threshold packets are unsafe.  The reversal lemma then produces

\[
A_k\subseteq U_k \qquad(k=1,2,3),                 \tag{1}
\]

where every `A_k` is current-safe and current-desired by a named source
`a_k`.  Because the reservoirs and `E` are physically disjoint,

\[
E,A_1,A_2,A_3
\quad\hbox{are pairwise disjoint}.                \tag{2}
\]

Moreover `a_k` is not the owner of `U_k`.  Indeed the reversal construction
has `A_k subseteq Q_k-g subsetneq U_k`; positivity gives

\[
v_k(A_k)<v_k(U_k)=b_k,                             \tag{3}
\]

whereas a response sourced by `k` would have value above `b_k`.

Let `j` own the physical target containing `E`.  The source `s` of `E` is
also different from `j`: positivity gives `v_j(E)<=v_j(Z^-_j)=b_j`, with
strict inequality when `E` is proper, whereas `E` is desired by `s` above
`b_s`.

## Full-source EFX endpoint

If

\[
\{s,a_1,a_2,a_3\}=N,                              \tag{4}
\]

then the four sources are distinct.  Assign each of `E,A_1,A_2,A_3` to its
named source.  Every assigned owner strictly improves over her value in
`Z^-`, and every target is safe relative to those old owner values.  Hence,
for every owner `i` and every other selected target `T`,

\[
\tau_i(T)
   \le v_i(Z^-_i)<v_i(\text{the response assigned to }i).       \tag{5}
\]

The selected allocation is EFX and strictly Pareto improves `Z^-`.  Since
the canonical state pays the globally maximal base floors, this is an EFX
lexicographic contradiction.

## Universal supplier-closed cycle endpoint

Independently of (4), direct the four physical supplier-source edges

\[
j\longrightarrow s,
\qquad
k\longrightarrow a_k\quad(k\ne j).              \tag{6}
\]

Every vertex has outdegree one and no edge is a self-loop.  Following edges
in this finite four-vertex graph must enter a directed cycle of length at
least two.  The packet on each cycle edge is supplied by its tail, desired
by its head, and pairwise disjoint from every other selected packet by (2).
Therefore the cycle is supplier-closed and is a release-compatible PI cycle.

Thus the all-unsafe fan always closes by PI; the full-source case additionally
has the direct EFX endpoint above.  If at least one reservoir instead yields
a safe threshold-payment packet, the state takes the payment/compression
branch of the reservoir-reversal lemma and is outside this theorem.

## Consequence for atomic survivor C

After proper retired-packet hits, whole-packet returns, new source/target
rank improvements, and safe-payment branches have been routed, the
normalization-bypass survivor cannot be all-unsafe.  It must carry at least
one **safe reservoir payment packet** `Q` with
`v_h(Q)>=tau_h(E)`.  The remaining obligation is to compose that exact
payment pair with the deficient response relation, or route its first
retired-support collision.

## Claim boundary

This theorem proves PI closure of the entire all-unsafe fan and the optional
rank-four EFX endpoint.  It does not eliminate the safe-payment branch,
prove that its partial payment completes a matching, close the whole-packet /
root-facing survivors, close `T_{L,times}^*`, or prove four-agent/general
EFX.

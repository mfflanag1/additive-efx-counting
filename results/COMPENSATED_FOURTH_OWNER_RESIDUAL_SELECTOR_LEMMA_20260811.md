# Compensated fourth-owner residual-selector lemma

**Date:** 2026-08-11

**Status:** cap-free completion of the four-owner payment layer for the
bottom-tail splice; observer-target safety and response augmentation remain
open

## Hole substitution and remaining q budget

Use the strict minimal-`K` separator and choose packets

\[
 J\subseteq K,
 \qquad L\subseteq E                               \tag{1}
\]

such that the hole remains strictly paid,

\[
 \nu_d+v_d(L)-v_d(J)>0,                            \tag{2}
\]

and returning `J` makes the remaining transfer q-admissible before reserving
fourth-owner compensation,

\[
 B_q:=\mu_q+v_q(W)-v_q(K\setminus J)\ge0.          \tag{3}
\]

The amount by which donation `L` exceeds the fourth owner's free margin is

\[
 \kappa_s=\max\{0,v_s(L)-\mu_s\}.                  \tag{4}
\]

## Canonical residual compensation

Choose

\[
 M^*\in\arg\max\{v_s(M):M\subseteq W,
                         v_q(M)\le B_q\}.           \tag{5}
\]

The family is nonempty because `M=empty` is feasible under (3). Exactly one
of the following occurs.

1. **Compensated four-owner splice.** If
   \[
   v_s(M^*)\ge\kappa_s,                            \tag{6}
   \]
   give `M^*` to `s`. Then
   \[
   v_s(E-L+M^*)\ge v_s(X_s).                       \tag{7}
   \]
   Moreover (3), (5), and additivity give
   \[
   v_q(W\setminus M^*)
   \ge v_q(K\setminus J)-\mu_q.                    \tag{8}
   \]
   Choose an inclusion-minimal `G_q subseteq W\setminus M^*` satisfying the
   right side of (8), and put
   \[
   G_r=W\setminus(M^*\cup G_q).                    \tag{9}
   \]
   The allocation
   \[
   \begin{aligned}
   Y_r&=A+G_r,\\
   Y_q&=Q-(K\setminus J)+G_q,\\
   Y_d&=(K\setminus J)+H+L,\\
   Y_s&=E-L+M^*
   \end{aligned}                                   \tag{10}
   \]
   pays root and hole strictly and pays `q,s` weakly. Its packet graph
   `r->d`, `q->d`, `s->d`, and `d->{r,q,s}` is connected after zero-packet
   edges are removed whenever all changed owners participate. A
   surplus-budgeted leaf is therefore an EFX lexicographic endpoint.
2. **Residual compensation separator.** If (6) fails, then every packet
   `M subseteq W` compatible with the remaining q budget satisfies
   \[
   v_q(M)\le B_q
   \quad\Longrightarrow\quad
   v_s(M)<\kappa_s.                                \tag{11}
   \]
   No allocation of the complete residual can both compensate `s` and leave
   enough q-value to finance `K\setminus J`. This is the exact final payment
   separator for the chosen hole substitution.

Globally maximize the left side of (6) over every pair `(J,L)` satisfying
(2)--(3), with deterministic tie-breaking afterward. If any compensated
four-owner payment exists in this packet geometry, this selector finds it;
otherwise its maximizing triple `(J,L,M^*)` supplies (11).

## Consequence

The bottom-tail recurrence no longer has an unspecified payment tree. Root
payment is automatic; `q` uses its canonical residual compensation; the
hole is restored by `K-J+H+L`; and the fourth owner is either within margin
or canonically compensated by `M^*`. Failure is a two-row residual separator,
not another rank reset.

Once (10) pays all owners, the only remaining checks are the observer-indexed
surplus inequalities. Any failed changed target has a globally minimal
desired subset and therefore enters the existing response-augmentation/
owner-coverage machinery. What remains to prove is that this augmentation
cannot return to the same separator without support or priority progress.

## Verification and boundary

[`compensated_fourth_owner_residual_selector_audit.json`](compensated_fourth_owner_residual_selector_audit.json)
checks residual partition, `s` payment, the q-budget cancellation, q payment,
root/hole payment, connected supplier support, and the global maximizing
failure implication.

This lemma does not force a successful `(J,L)`, discharge observer-target
surplus inequalities, eliminate recurrence after a response augmentation,
close GG, or prove four-agent/general additive EFX.

# Decorated-head alternating minimal-response lemma

**Date:** 2026-08-13

**Status:** cap-free conversion of every mixed-cycle wall target into a
candidate-safe response sourced by one of at most two decorated heads

## Paid residual-completed cycle

Use the residual-completed mixed-cycle allocation

\[
 Z_i=O_i\mathbin{\dot\cup}R_i
\]

from the decorated-head localization lemma. Every owner is strictly above
the base allocation. Let `T` be an allocated special target that is
current-safe relative to the preceding paid state `Y` but is unsafe in `Z`.
Thus some observer `h` has

\[
 v_h(Z_h)<\tau_h(T)\le v_h(Y_h).                 \tag{1}
\]

The localization lemma gives one of two outcomes for every such blocker:

1. an old-incoming self-response/source transition; or
2. `h` is a decorated head.

After excluding the first ordinary progress outcome, every blocker belongs
to a fixed head set `H` with

\[
 1\le |H|\le2.                                   \tag{2}
\]

## Alternating minimal extraction

Choose a blocker `h_0 in H`. Since (1) implies `v_{h_0}(T)>v_{h_0}(Z_{h_0})`,
choose an inclusion-minimal subset

\[
 A_0\subseteq T,
 \qquad v_{h_0}(A_0)>v_{h_0}(Z_{h_0}).          \tag{3}

Minimality gives

\[
 \tau_{h_0}(A_0)\le v_{h_0}(Z_{h_0}).           \tag{4}

Because threshold safety is downward closed and `A_0 subseteq T`, every
observer failure against `A_0` is again a failure against a current-safe
subtarget of the same residual-completed cycle. Hence a failing observer
outside `H` produces the old-incoming self-response outcome. If no such
progress occurs, only the other decorated head can block `A_0`.

Suppose `h_1 in H\setminus{h_0}` blocks `A_0`. Then

\[
 \tau_{h_1}(A_0)>v_{h_1}(Z_{h_1}),              \tag{5}

so some deletion `A_0-g` is already desired by `h_1`. Choose an
inclusion-minimal desired subset

\[
 A_1\subseteq A_0-g\subsetneq A_0.              \tag{6}

It is safe for `h_1`; only `h_0` may block it. Repeat, alternating the head
identity whenever the current core is unsafe. Every continuation is a
strict inclusion

\[
 T\supseteq A_0\supsetneq A_1\supsetneq A_2
 \supsetneq\cdots.                               \tag{7}

The finite ground set makes (7) terminate. At termination there is a core
`A* subseteq T` and a source `h* in H` such that

\[
 v_{h^*}(A^*)>v_{h^*}(Z_{h^*}),
 \qquad
 \tau_j(A^*)\le v_j(Z_j)\quad(j\in N).          \tag{8}

Thus `A*` is desired and safe relative to the complete paid candidate, and
its source is one of the at most two decorated heads.

## Consequences

Apply the construction independently to every unsafe target. Exactly one of
the following occurs.

1. A non-head old-incoming self-response gives a new source/core label,
   matching pivot, PI/support transition, or a named exact recurrence.
2. Every wall target has a candidate-safe response core whose source lies in
   the one- or two-element head set `H`.

In the second branch, the payment problem has become a response-Hall problem
with at most two distinguished sources. For one head, the selected head
responses form a common-source star. For two heads, every wall target has a
neighbor in the pair, so the two-by-two Hall normal form applies to every
two-target restriction. A covering matching gives disjoint safe desired
cores; a deficiency is a common-singleton star or an empty-source side and
must be composed with the opposite released-core block.

This is strictly stronger than saying that a head values the incoming
decorated core above its outgoing old core: it produces a fully
candidate-safe labeled response and terminates alternating cross-head safety
without any item or value bound.

## Claim boundary

This lemma proves alternating extraction, strict support descent, global
candidate safety, and head-source localization. It does not prove that the
resulting one-/two-source response relation has a rank-four completion,
eliminate its Hall star/empty-target form, pay the missing source after
compression, eliminate root full-pool capture, close GG, or prove
four-agent/general additive EFX.

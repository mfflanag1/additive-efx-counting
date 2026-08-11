# q-closing-source residual-reassignment lemma

**Date:** 2026-08-11

**Status:** proved special case, superseded by the universal closing-source
deletion-return residual-completion lemma

## Source-collision state

Use one of the six stable anchored pivots in which `q` is the old decorated
response source into owner hole `t`.  Before the pivot, the Hamiltonian path
assigns q an old base-common-safe desired core `A_q`.  The permanent incoming
anchor into target q selects

\[
 C_q\subseteq Y_q,
 \qquad
 R_q=Y_q\setminus C_q.                            \tag{1}
\]

The closing decorated core is

\[
 D\subseteq Y_t,
\]

and is current-safe at the paid state:

\[
 \tau_h(D)\le v_h(Y_h)\qquad(h\in N).             \tag{2}
\]

The target owner `t` holds an old path core `A_t`; writing
`R_t=Y_t-D`, the sole-target-owner separator is

\[
 v_t(A_t+R_t)<\tau_t(D).                           \tag{3}
\]

## Return a deletion remainder to the hole owner

Let `g` be a least-t good of `D` and put

\[
 P=D-g.
\]

Then (3) gives

\[
 v_t(P)=\tau_t(D)>v_t(A_t+R_t)>v_t(X_t).          \tag{4}
\]

Do not execute the closing edge `q -> t:D`.  Give `P` to `t` and retain q's
old path core `A_q`.  The target `P` is a strict subbundle of the current-
safe core `D`, so

\[
 \tau_h(P)\le\tau_h(D)                             \tag{5}
\]

for every observer.  Every nonowner `h notin {t,q}` keeps the residual or
self-response compensation already supplied by the mixed-margin nonowner
lemma.  A compensation paying the debt of `D` automatically pays the weakly
smaller debt of `P`; a failed compensation has already produced PI, support
growth, or response augmentation.

## The former source becomes an ordinary observer

After `D` is returned, q no longer receives the decorated target and must be
checked as an observer.  Give q the released residual `R_q` beside its old
assigned core.

### Residual pays

If

\[
 v_q(A_q+R_q)\ge\tau_q(P),                         \tag{6}
\]

q is paid.  Together with (4) and the already paid nonowner rows, every owner
is strictly above the globally maximal base.  The old cores remain pairwise
disjoint, `P` lies in the previously unmatched hole target, and every
residual excludes the incoming core selected from its own target.  Hence the
candidate bundles are physically disjoint.

If all enlarged targets are safe, the candidate is a partial EFX Pareto—and
therefore lexicographic—improvement.  Any unsafe enlarged target gives a
globally minimal current response.  Because the good `g` is absent from every
allocated target while `g in D`, this response cannot be the same physical
decorated core `D`; it changes the core/target support, invokes an already
recorded hole-pivot/PI component, or is permanent response augmentation.
The unused packet is handled, when necessary, by arbitrary-charity collapse.

### Residual fails

Otherwise, (2),(5), and (1) give

\[
 v_q(A_q)+v_q(R_q)
 <\tau_q(P)
 \le\tau_q(D)
 \le v_q(C_q)+v_q(R_q).
\]

Cancellation yields

\[
 v_q(C_q)>v_q(A_q)>v_q(X_q).                      \tag{7}
\]

The incoming anchor core `C_q` is base-common-safe, so (7) is an exact
self-response by q into its own physical target.  A new core/release label is
permanent augmentation; an old internally supplied self-edge is PI; and an
unreleased packet grows the physical component.  At full-owner saturation a
changed full signed label is again augmentation.  Thus residual failure is a
certified progress outcome, not a recurring q-source payment deficit.

## Path exhaustiveness

In all six q-source anchor cycles, q has the incoming edge `r -> q` and a
distinct old outgoing path edge: four point to an external owner target and
two point to charity.  The reassignment above therefore exists in every
cycle length two, three, and four.  No q-source anchored pivot survives.

## Verification and boundary

[`q_closing_source_residual_reassignment_audit.json`](q_closing_source_residual_reassignment_audit.json)
checks the six path positions, physical disjointness of the reassigned path
cores/residuals, target-owner payment, threshold monotonicity under deletion,
and the residual-failure cancellation in exact arithmetic.

This lemma eliminates the q-source role collision.  It does not discharge
the non-q-source donor/rank-two continuation, prove termination of every
unsafe enlarged-target response, produce a globally maximal countermodel,
close GG, or prove four-agent/general additive EFX.

The same argument applies to every nonself closing source, not only q.  The
superseding result is
[`CLOSING_SOURCE_DELETION_RETURN_RESIDUAL_COMPLETION_LEMMA_20260811.md`](CLOSING_SOURCE_DELETION_RETURN_RESIDUAL_COMPLETION_LEMMA_20260811.md).

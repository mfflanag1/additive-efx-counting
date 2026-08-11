# Paid-splice observer-failure current-response lemma

**Date:** 2026-08-11

**Status:** cap-free conversion of every failed observer-surplus inequality
into a current-improving, surplus-budgeted response; persistence requires
retaining the physical observer-compensation packets

## Paid splice and failed safety

Let `X` be an EFX-with-charity allocation and let `Y` be any complete splice
candidate satisfying

\[
 v_i(Y_i)\ge v_i(X_i)\qquad(i\in N).               \tag{1}
\]

Suppose `Y` is not EFX.  Then some observer `i` and target `j!=i` satisfy

\[
 v_i(Y_i)<\tau_i(Y_j).                             \tag{2}
\]

Equivalently, the observer-surplus budget fails:

\[
 \tau_i(Y_j)-v_i(X_i)>
 v_i(Y_i)-v_i(X_i).                                \tag{3}
\]

Thus failure after the four-owner payment selector is not an independent
kind of separator: it is strict envy relative to the **current** paid
allocation.

## Globally minimal current response

Let `F` be the finite family of all pairs `(h,D)` for which `D` is a subset
of a failed changed target and

\[
 v_h(D)>v_h(Y_h).                                  \tag{4}
\]

The family is nonempty.  Indeed, if `g` is a least-`i` good of the target in
(2), then `D=Y_j-g` satisfies (4).

Choose a member `(s,D)` whose support `D` is inclusion-minimal over the
supports appearing in `F`.  Then

\[
 v_s(D)>v_s(Y_s)\ge v_s(X_s),                     \tag{5}

\]

and for every owner `h` and every `g in D`,

\[
 v_h(D-g)\le v_h(Y_h).                             \tag{6}

\]

Otherwise `(h,D-g)` would be a member of `F` with strictly smaller support.
Consequently `D` is EFX-safe against the entire current paid allocation:

\[
 \tau_h(D)\le v_h(Y_h)\qquad(h\in N).             \tag{7}

\]

Equation (7) does **not** imply common safety relative to `X`: the direction
in (1) is the wrong way for that inference.  Instead put

\[
 \Delta_h=v_h(Y_h)-v_h(X_h)\ge0,
 \qquad
 \beta_h(D)=\bigl(\tau_h(D)-v_h(X_h)\bigr)_+.      \tag{8}
\]

Then (7) gives the exact surplus budget

\[
 \beta_h(D)\le\Delta_h\qquad(h\in N).             \tag{9}

\]

Thus `D` is a surplus-budgeted response target in the sense of the connected-
component endpoint theorem.  Equation (5) is stronger than an ordinary base
response on the source row, but other observers may need to retain the
physical gains realizing `Delta_h`.

## Persistent response consequence

If every `beta_h(D)=0`, record the ordinary exact physical response triple

\[
 (s,\operatorname{supp}(Y_j),D).                  \tag{10}

\]

For each owner write the canonical signed physical transfer relative to the
base as

\[
 I_h=Y_h\setminus X_h,
 \qquad O_h=X_h\setminus Y_h,
 \qquad \Delta_h=v_h(I_h)-v_h(O_h).                \tag{11}
\]

For recurrence, the persistent object must use the **full decorated
response**

\[
 (s,\operatorname{supp}(Y_j),D;
   (I_h,O_h)_{h\in N}),                            \tag{12}

\]

where the positive-debt rows certify net gain at least `beta_h(D)` and the
zero-debt rows make the physical allocation reconstructible.  Recording
only the edge `s -> j:D`, or only the positive-debt rows, would be unsound:
a later reset could change a zero-debt owner's bundle or undo part of a
compensation transfer without changing the coarse response graph.

Use (10) for the ordinary response relation when every `beta_h(D)=0`, but
attach the full signed state (12) whenever exact physical recurrence is
tested.  In the positive-debt case the failed observer has exposed the
smallest missing packet operation: the response must retain its signed
compensation transfers.
At a fixed returning `(hole, paid anchor, consumed support)` state, exactly
one of the following occurs.

1. The applicable ordinary or decorated record has not occurred.  Adjoining
   it is a permanent response augmentation.
2. The record has occurred, but `s` now
   holds a different bundle.  Recapture
   by `D` strictly raises the same-owner current utility from `v_s(Y_s)` to
   `v_s(D)` before any reset.  The paid-anchor current-wall and support-reset
   lemmas then give fixed-state source progress, fresh anchor consumption,
   or captured payment margin.
3. The exact source, target support, desired core, and the complete signed
   physical state recur.  The allocation, charity, moved-packet graph, and
   response/release labels are then fixed by reconstruction.  This is the
   explicit repeated-support connected-splice terminal: the released-core
   packet walk must be closed as a release-compatible component.

There are finitely many exact decorated physical responses on a finite ground
set.  Hence observer failure cannot generate an untyped infinite family.  It
strictly augments the ordinary relation, adds a named compensation packet to
the connected operation, increases a current same-owner bundle value,
consumes support, captures margin, or exposes an exact repeated decorated
response.

## Consequence for the GG splice program

The universal repeated-support theorem no longer needs to prove observer
safety directly for every proposed packet split.  It may maximize the paid
four-owner selector first.  A failed safety inequality automatically yields
the current-safe core (5)--(9) and names every observer compensation that
must remain attached.  Only recurrence of the exact decorated physical
response (12) reaches the final connected-return gate.

This removes “observer-surplus failure” as a free-standing scalar branch.
The remaining theorem is physical: show that the response core, released
packets, and its named signed transfers between two occurrences of (12)
form one release-compatible component, or produce a full globally maximal GG
countermodel.

## Verification and boundary

[`paid_splice_observer_failure_current_response_audit.json`](paid_splice_observer_failure_current_response_audit.json)
checks the failed-budget equivalence, nonempty least-good witness, strict
current response, exact surplus-budget implication, the failure of the
invalid current-safe-to-base-safe inference, and the decorated-response
trichotomy.

This lemma does not prove that an old decorated response closes as a
connected component, force the decorated signed transfers to lie in one
connected supplier component, establish a full globally
maximal GG countermodel, close GG, or prove four-agent/general additive EFX.

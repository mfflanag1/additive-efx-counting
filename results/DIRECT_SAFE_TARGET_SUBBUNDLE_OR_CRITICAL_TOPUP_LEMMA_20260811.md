# Direct-safe target subbundle-or-critical-top-up lemma

**Date:** 2026-08-11

**Status:** cap-free dominant repair of the decorated target; exact recurrent
critical top-up substitution remains open

## Sole-wall paid state

Let `Y` be the exact paid state before assigning the decorated response core.
Assume every owner target other than `Y_t` is EFX-safe at `Y`; this is the
one-wall normal form produced by paid-input compression.  Define the target
owner's priority/direct floor

\[
 F_t=\max\left\{\rho_t,
                 \max_{j\ne t}\tau_t(Y_j)\right\},                 \tag{1}
\]

where `rho_t=v_t(X_t)` if `t` must remain above base for the fixed
lexicographic prefix, and otherwise `rho_t` is its priority-valid direct
floor.  The family

\[
 \mathcal Q=\{Q\subseteq Y_t:v_t(Q)\ge F_t\}       \tag{2}
\]

is nonempty because `Y_t in mathcal Q`.  Choose an inclusion-minimal member
`Q*`, with a deterministic physical tie-break.

## Safe target branch

If

\[
 \tau_h(Q^*)\le v_h(Y_h)\qquad(h\ne t),           \tag{3}
\]

keep every other owner at `Y_h`, give `Q*` to `t`, and leave `Y_t-Q*`
unallocated.  Equation (1) makes `t` directly safe against every unchanged
target and preserves the priority prefix.  Equation (3) makes every other
owner safe against the only changed target.  Hence the result is a partial
EFX lexicographic improvement of the globally maximal base.

If a charity-dominance invariant is required, the arbitrary-charity-packet
collapse either makes the enlarged charity safe, produces the same endpoint,
or yields a new current response/progress event.  Thus disposal of
`Y_t-Q*` is not a separate obstruction.

## Unsafe target branch

If (3) fails, globally minimize the support of a pair `(h,E)` with

\[
 E\subseteq Q^*,
 \qquad v_h(E)>v_h(Y_h).                           \tag{4}

The family is nonempty by deleting a least-`h` good from the strong-envy
witness.  Global support minimality gives

\[
 \tau_a(E)\le v_a(Y_a)qquad(a\in N),             \tag{5}

so `E` is an exact current-safe decorated response.  A new source, support,
core, signed state, or release label is permanent augmentation.

Suppose instead that the exact old decorated response `D` recurs, so
`E=D subseteq Q*`.  If `D` itself belongs to `mathcal Q`, inclusion
minimality of `Q*` forces `Q*=D`, and (5) contradicts the unsafe branch.
Therefore

\[
 v_t(D)<F_t,
 \qquad K=Q^*\setminus D\ne\varnothing.           \tag{6}

Moreover every good of `Q*` is target-owner critical:

\[
 v_t(Q^*-g)<F_tqquad(g\in Q^*),                  \tag{7}

because `Q*` is inclusion-minimal in (2).

The exact recurrent terminal is consequently not an arbitrary mixed debt.
It consists of a current-safe old response `D` plus a nonempty physical
top-up packet `K` that is necessary to pay/directly protect target owner `t`,
while `Q*=D+K` creates a current wall.  The next operation must substitute
for `K` from the recorded signed-transfer component, compensate its blocker,
change the source/root, or replace `D`.

## Verification and boundary

[`direct_safe_target_subbundle_or_critical_topup_audit.json`](direct_safe_target_subbundle_or_critical_topup_audit.json)
checks family nonemptiness, the safe-branch EFX implications, response
minimality, nonempty recurrent top-up, and every-good criticality symbolically
and by exhaustive finite-set logic.

This lemma does not supply a substitute for `K`, pay its blocker, eliminate
the exact recurrent critical-top-up state, produce a globally maximal
countermodel, close GG, or prove four-agent/general additive EFX.

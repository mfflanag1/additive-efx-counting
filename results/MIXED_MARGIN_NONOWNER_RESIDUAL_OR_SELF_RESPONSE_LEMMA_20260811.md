# Mixed-margin nonowner residual-or-self-response lemma

**Date:** 2026-08-11

**Status:** cap-free closure of every underfunded observer except the owner of
the decorated target; that owner requires complement return

## Path-local decomposition

Work at one exact full signed-transfer state.  The PI-free rank-four matching
is the Hamiltonian path

\[
 h_0\longrightarrow h_1\longrightarrow h_2
 \longrightarrow h_3\longrightarrow c,           \tag{1}
\]

and one decorated response assigns a current-safe desired core `D subseteq
Y_t` to its source `s`, where `t` is the owner of the decorated physical
target.  Every other selected core is an old base-common-safe core.

Let `h != t,s` be an observer whose assigned old core `A_h` does not cover
the debt of `D`:

\[
 v_h(A_h)<\tau_h(D)\le v_h(Y_h).                  \tag{2}
\]

The matching edge entering target `h` selects an old core `C_h subseteq
Y_h`.  Put

\[
 R_h=Y_h\setminus C_h.                            \tag{3}
\]

The packet `R_h` is physically released by that incoming path edge.

## Exact dichotomy

### Residual pays

If

\[
 v_h(A_h+R_h)\ge\tau_h(D),                        \tag{4}
\]

give `R_h` to `h`.  This repairs row `h` without lowering any owner and uses
a packet already released on the same path component.  The enlarged target
`A_h+R_h` is the only new owner-target safety risk.  If it is safe, the debt
is closed; if it is unsafe, globally minimal current-response extraction
gives an ordinary/full-decorated response augmentation or current progress.

### Residual fails

Otherwise, using `Y_h=C_h dotunion R_h`, (2) gives

\[
 v_h(A_h)+v_h(R_h)<\tau_h(D)
 \le v_h(C_h)+v_h(R_h),                           \tag{5}
\]

and therefore

\[
 v_h(C_h)>v_h(A_h)>v_h(X_h).                      \tag{6}
\]

Because `C_h` is base-common-safe, (6) is an exact response by `h` into its
own physical target.  A new core or release label is permanent response
augmentation.  An old internally supplied label is a generalized self-PI
edge.  An unreleased incoming packet names an outside supplier and strictly
grows the connected physical component; at full-owner saturation, a changed
release label is again augmentation.

Thus a nonowner of `D` cannot remain an untyped underfunded observer.

## Boundary cases

The decorated source `s` does not observe `D` as another owner's target once
it receives `D`, so it is not a debt observer for this comparison.  The case
`h=t` is different because the edge entering `Y_t` is the decorated edge
itself, so `C_t=D` is not base-common-safe.  It is handled by the decorated-
target-owner complement-return selector.

## Verification and boundary

[`mixed_margin_nonowner_residual_or_self_response_audit.json`](mixed_margin_nonowner_residual_or_self_response_audit.json)
checks the residual-payment branch and proves (5)--(6) symbolically.

This lemma does not close the decorated target owner's debt, prove that every
new enlarged target is immediately safe, resolve the final complement-return
separator, close GG, or prove four-agent/general additive EFX.

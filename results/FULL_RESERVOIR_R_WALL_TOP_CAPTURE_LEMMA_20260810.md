# Full-reservoir R-wall top-capture lemma

**Date:** 2026-08-10

**Status:** cap-free analytic localization; the strict top-core branch remains
open

## Setting

Use an R-exhausted leaf of the released-owner compensation chain.  Thus an
external response core `K subseteq X_q` is selected, with

\[
O=X_q\setminus K,
\]

and a payment packet `P subseteq T_r` satisfies the full-reservoir wall

\[
v_r(O+X_a)<v_r(P). \tag{1}

\]

Write the mutual bundle as

\[
X_q=T_q\mathbin{\dot\cup}B_q

\]

and split the response core into

\[
K_T=K\cap T_q,
\qquad
K_B=K\cap B_q. \tag{2}

\]

The flower gives the common-safe desired root bundle `T_q+f` for `r`, so

\[
v_r(T_q+f)>v_r(T_r+B_r). \tag{3}

\]

Global maximality and the early-root charity rotation give

\[
v_r(B_r)\ge v_r(f). \tag{4}

\]

## Top-capture theorem

Every full-reservoir R-wall forces

\[
v_r(K_T)>v_r(B_q\setminus K_B)+v_r(X_a). \tag{5}

\]

In particular `K_T` is nonempty.  Therefore an R-wall is impossible when
the external response core is contained entirely in the later owner's
bottom packet `B_q`.

## Proof

Since `P subseteq T_r`, (1) implies

\[
v_r(T_r)>v_r(O)+v_r(X_a). \tag{6}

\]

Combining (3) and (6) gives

\[
v_r(T_q)+v_r(f)
>v_r(O)+v_r(X_a)+v_r(B_r). \tag{7}

\]

But

\[
O=(T_q\setminus K_T)+(B_q\setminus K_B).

\]

Cancel `T_q\setminus K_T` from (7):

\[
v_r(K_T)+v_r(f)
>v_r(B_q\setminus K_B)+v_r(X_a)+v_r(B_r). \tag{8}

\]

Finally (4) turns (8) into (5).  Positivity makes the right side of (5)
strictly positive, so `K_T` cannot be empty. \(\square\)

## Consequences for the adaptive bridge

The compensation architecture now has the following exhaustive signed
leaves.

1. A successful repair gives the three-owner release-compatible component.
2. Q-exhaustion changes the root to `q` and enters the finite sink-
   augmentation chain.
3. R-exhaustion can survive only when the external desired response retains
   a nonempty top core `K_T` satisfying the strong capture inequality (5).

All current strict-capture adversaries use a bottom-only core and therefore
cannot realize branch 3.  The next root/order operation need only address a
top packet that `r` values above the omitted bottom packet plus the entire
external bundle; it no longer needs to handle an arbitrary response core.

The scalar implication replays in
[`full_reservoir_r_wall_top_capture_audit.json`](full_reservoir_r_wall_top_capture_audit.json).

## Claim boundary

This lemma eliminates full-reservoir R-walls for bottom-only response cores
and sharply orients every survivor.  It does not eliminate the strict top-core inequality
(5), select the final root/order flip in that branch,
eliminate all-owner Hall defects, close the `GG` flower, or prove four-agent
additive EFX.

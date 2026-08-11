# Q-exhaustion root-switch lemma

**Date:** 2026-08-10

**Status:** cap-free analytic conversion of the Q-wall into a transfer-tree
component; its open/Hall response boundary remains

## Statement

Use a Q-exhausted leaf of the alternating payment-compensation chain.  Thus

\[
O=X_q\setminus K,
\qquad
\Delta_a=v_q(K)-v_q(X_a),
\]

and packets `P subseteq T_r`, `H subseteq O` satisfy

\[
v_q(T_r)\le \Delta_a+v_q(H). \tag{1}
\]

Put

\[
E=O\setminus H. \tag{2}
\]

Then

\[
v_q(f)>v_q(E)+v_q(X_a). \tag{3}

Consequently `q` can be made the charity root by replacing `E` with `f`:

\[
Z_q=X_q\setminus E+f=K+H+f. \tag{4}
\]

If `E` is nonempty, give it to the terminal external owner:

\[
Z_a=X_a+E. \tag{5}
\]

Fix `r` and the other external owner.  If `E` is empty, simply fix `a` as
well.  In either case `Z` is a complete allocation, `r` is unchanged, and
`q` strictly improves.  For nonempty `E`, owner `a` also strictly improves
by positivity.

## Proof of the root-switch inequality

The flower bundle `T_r+f` is strictly desired by `q`, so

\[
v_q(T_r)+v_q(f)>v_q(X_q)
=v_q(K)+v_q(H)+v_q(E). \tag{6}

Equation (1) is

\[
v_q(T_r)\le v_q(K)-v_q(X_a)+v_q(H). \tag{7}

Subtracting (7) from (6) gives exactly (3).  In particular
`v_q(f)>v_q(E)`, which proves that (4) strictly improves `q`.

The stronger margin in (3) is important: the new charity-root operation
does not merely clear the selected packet; its `q`-gain exceeds `q`'s value
for the entire terminal external bundle.

## Response-Hall composition

For nonempty `E`, equations (4)--(5) form the one-edge charity-rooted transfer tree

\[
q\longrightarrow a:E.
\]

Its root target has incoming `{f}` and releases `E`; its leaf target has
incoming `E`.  For empty `E` the tree consists only of root `q`.  Therefore
the charity-rooted transfer-tree theorem applies:

1. if `Z` is EFX, it is the required complete allocation with `r` fixed and
   `q` strictly better;
2. any internal response SDR is a release-compatible PI edge set;
3. otherwise a response source outside the current tree grows the owner
   component, or Hall's theorem names the exact deficient target set.

On the hardened PI-free flower profile, (4) is exactly the `q` bundle in
the minimum radius-four EFX escape.  The two-owner root switch is blocked,
but its leaf response exposes the other external owner; growing the tree
produces the observed path `q -> c -> s`.  This is adversarial evidence for
the composition, not a cap-free closure of its Hall branch.

The scalar implication and one-edge support replay in
[`q_exhaustion_root_switch_audit.json`](q_exhaustion_root_switch_audit.json).

## Claim boundary

This lemma eliminates Q-exhaustion as an unnamed compensation failure and
turns it into a canonical charity-rooted component.  It does not prove that
the root switch is EFX, eliminate its open source or Hall defect, close the
R-exhausted branch, close the `GG` flower, or prove four-agent additive EFX.

# Joint-packet maximal lex-donation frontier lemma

**Date:** 2026-08-11

**Status:** cap-free conversion of the canonical joint packet into a
connected lexicographic transfer component; blocker termination remains open

## Joint packet and maximal donation

Let `(X,{f})` be the base positive-additive EFX-with-charity state.  Let `r`
precede `q` in the fixed priority, and let

\[
 \varnothing\ne K\subseteq X_q
\]

be the joint-critical packet produced by the canonical root-response
selector.  Choose, with deterministic tie-breaking, an inclusion-maximal
packet

\[
 G\subseteq X_r
\]

subject to both

\[
 v_r(G)<v_r(K)                                      \tag{1}
\]

and

\[
 v_r(X_r\setminus G)+v_r(K)
 \ge v_r(f)+v_r(G).                                 \tag{2}
\]

The family is nonempty because `G=empty` is feasible: base charity
dominance gives `v_r(X_r)>=v_r(f)`, and `K` has positive value.  For every
unused good `g in X_r\setminus G`, maximality and nondegeneracy give at
least one of

\[
 v_r(G+g)>v_r(K),                                   \tag{3}
\]

or

\[
 v_r(X_r\setminus(G+g))+v_r(K)
 <v_r(f)+v_r(G+g).                                  \tag{4}
\]

Thus every unused root good is individually critical for preserving either
the root's gain or her charity dominance.

## Connected lexicographic transfer

Form

\[
 Y_r=(X_r\setminus G)+K,
 \qquad Y_q=X_q\setminus K,
 \qquad Y_c=X_c,
 \qquad Y_s=X_s,
 \qquad P_Y=\{f\}+G.                               \tag{3}
\]

The transfer multigraph contains the connected edge

\[
 q\longrightarrow r:K.
\]

When `G` is nonempty, it extends that same component by

\[
 r\longrightarrow\mathrm{charity}:G.
\]

When `G` is empty, the component is simply the owner edge `q -> r`; in that
case no new charity wall can occur because the charity remains `{f}`.

Equation (1) gives

\[
 v_r(Y_r)-v_r(X_r)=v_r(K)-v_r(G)>0.                 \tag{5}
\]

Every owner preceding `r` is unchanged and `r` strictly improves.  Hence an
EFX instance of (3) is a strict global lexicographic improvement even though
the later donor `q` may lose and charity cardinality may grow.

## Exhaustive blocker localization

Equation (2) makes the root dominate the new charity by construction.  If
(3) is not EFX with charity, every failure has one of three forms.

1. **Donor wall.** Owner `q`, who loses `K`, fails an owner-target EFX
   comparison or charity dominance.
2. **External root-target wall.** Some `i in {c,s}` strongly envies
   `(X_r\setminus G)+K`.  Since the observer is unchanged and base EFX
   holds against `X_r`, this forces the exact strict threshold polarity
   \[
   \tau_i((X_r\setminus G)+K)>\tau_i(X_r).          \tag{6}
   \]
   A globally minimal desired subset of the changed root target supplies a
   named common-safe response core.
3. **External charity wall.** Some `i in {c,s}` envies `f+G`.  Base charity
   dominance gives
   \[
   v_i(G)>v_i(X_i)-v_i(f)\ge0.                      \tag{7}
   \]
   Every globally minimal desired subset of `f+G` must consume a good of
   `G`, because no subset of `{f}` alone is desired at the base.

No other failure is possible.  The root improves, remains safe against
every unchanged target and the shrunken `q` target, and satisfies charity
dominance by (2).  An external owner is unchanged, every external target is
unchanged, and the `q` target only shrinks; hence her only new comparisons
are the root target and charity.  All failures of the losing donor are
deliberately retained in branch 1.

## Potential consequence

At the canonical root-response terminal, (3) is the first connected
lexicographic component and (3)--(4) are its local maximality certificate.  A
charity response adds a new owner to the same physical transfer component;
a root-target response enters the response/Hall augmentation; and a donor
wall enters the sacrificed-owner compression machinery.  The packet size is
unrestricted, and no bounded transfer radius is used.

The selected frontier cannot be enlarged by one root good without losing
the lexicographic sign or root charity dominance.  A valid global
termination proof must therefore either augment through one of the named
blocker targets or derive a packet exchange reversing (3)--(4); merely
trying larger donations is exhausted.

## Verification and claim boundary

[`joint_packet_maximal_lex_donation_frontier_audit.json`](joint_packet_maximal_lex_donation_frontier_audit.json)
checks nonemptiness of the constrained frontier, root gain and charity
dominance, propagation of inclusion maximality, and the external blocker
polarities under Z3 5.0.0.

This lemma converts the joint packet into a canonical connected
lexicographic transfer and classifies every blocker.  It does not pay every
donor wall, prove that each named response augments to EFX/PI, terminate the
connected component, close `GG`, or prove four-agent/general additive EFX.

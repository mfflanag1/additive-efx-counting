# Flower rank-one root-monopoly handoff lemma

**Date:** 2026-08-11

**Status:** cap-free generic rank-one handoff; in the `GG` flower the
external-bottom-edge anchor excludes the root-monopoly branch

## Live flower target

Use the `GG` flower decomposition

\[
 X_r=T_r\mathbin{\dot\cup}B_r,
 \qquad
 X_q=T_q\mathbin{\dot\cup}B_q,
\]

and the mutual desired cores `T_q+f` for `r` and `T_r+f` for `q`.

If

\[
 v_q(f)>v_q(B_q),                                    \tag{1}
\]

the standard packet-for-charity replacement gives `q` the common-safe
bundle `T_q+f`, keeps `r` at `X_r`, and leaves `B_q` in charity.  It is an
EFX flexible improvement.  Hence every live survivor satisfies

\[
 v_q(f)\le v_q(B_q).                                 \tag{2}


The other mutual edge gives

\[
 v_q(T_r+f)>v_q(T_q+B_q).
\]

Combining this with (2) yields

\[
 v_q(T_r)>v_q(T_q),
 \qquad
 v_q(U)>v_q(X_q),
 \quad U:=T_r+B_q.                                   \tag{3}

Thus the rank-one state always has a second disjoint desired target `U` in
addition to the anchored root core `A=T_q+f`.

## Response-matching dichotomy

Let `C_U` be the nonempty set of base-response sources for `U`, with one
common-safe desired response core selected for each source.  The root `r`
is a response source for the common-safe target `A`.

If `C_U` contains some source `a != r`, select the disjoint cores

\[
 A\subseteq T_q+f,
 \qquad D_a\subseteq U.                              \tag{4}

They give a rank-two response matching.  Keep these two cores and pool all
other goods between the other two owners.  The two-hole cut-and-choose
selector and exact 2-by-2 Hall normal form apply.  Therefore this branch
gives an EFX lex improvement, a release-compatible PI component, or the
already named source-inactive two-hole boundary.  It is not a rank-one
terminal.

The only rank-one response defect is consequently

\[
 C_U=\{r\}.                                           \tag{5}


## Root-monopoly support

Let `D_r subseteq U` be the root's common-safe desired response in (5):

\[
 v_r(D_r)>v_r(X_r).                                  \tag{6}

It must capture a nonempty part of `B_q`.  Indeed, if
`D_r\cap B_q` were empty, then `D_r subseteq T_r`, and positivity would give

\[
 v_r(D_r)\le v_r(T_r)<v_r(T_r+B_r)=v_r(X_r),
\]

contradicting (6).  Hence

\[
 K_B:=D_r\cap B_q\ne\varnothing.                     \tag{7}

Write `K_T=D_r\cap T_r`.  The exact terminal target is

\[
 D_r=K_T+K_B,                                        \tag{8}

with `K_B` a named captured packet of the later mutual owner's bottom.
The remaining goods of `U` are released inside the same owner union.

Thus a rank-one response relation cannot end in an arbitrary three-agent
external-observer selector.  It either regains rank two or exposes the
root-monopoly bottom-capture dependency (7)--(8), which must be compensated
from `A`, the residual pool, or an external owner component.

## Verification and claim boundary

[`flower_rank_one_root_monopoly_handoff_audit.json`](flower_rank_one_root_monopoly_handoff_audit.json)
checks the live `q`-target inequality, the two-target matching dichotomy,
disjoint support, and the forced nonempty bottom capture under Z3 5.0.0 and
4.15.3.

This lemma eliminates a generic rank-one/three-hole existence problem from
the flower bridge.  The separate external-bottom-edge anchor supplies a
nonroot response to `U` in `GG`, so the abstract monopoly branch cannot
occur there.  These lemmas do not terminate a return to the two-hole
source-inactive boundary, close `GG`, or prove four-agent/general additive
EFX.

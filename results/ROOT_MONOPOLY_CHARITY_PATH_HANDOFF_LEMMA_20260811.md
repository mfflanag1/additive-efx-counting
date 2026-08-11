# Root-monopoly charity-path handoff lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of the complete-path root-monopoly terminal;
the root-anchored sacrificed-`q` Hall reset remains open

## Root-monopoly target

Use the root-monopoly branch of the charity-completed path response
boundary.  Its permanent root anchor is

\[
 D_r=T_q+f,
\]

and maximum-matching compression with that edge leaves the auxiliary target

\[
 U=X_r+B_q.                                          \tag{1}
\]

Suppose the only response source for `U` is the root, with a common-safe
desired response core

\[
 D\subseteq U,
 \qquad v_r(D)>v_r(X_r).                            \tag{2}
\]

Decompose its support as

\[
 C=D\cap X_r,
 \qquad K=D\cap B_q,
 \qquad G=X_r\setminus C.                          \tag{3}

Then `K` is nonempty.  Otherwise `D subseteq X_r`, contradicting (2).
Moreover (2) is exactly

\[
 v_r(C)+v_r(K)>v_r(C)+v_r(G),
\]

and therefore

\[
 v_r(K)>v_r(G).                                     \tag{4}

Thus the monopolizing root response itself selects a root-affordable packet
`G`; no second bilateral search is required.

## Canonical complete path

Choose either external owner `a` when `G` is nonempty and define

\[
 Y_q=(X_q\setminus K)+f,
 \qquad Y_r=(X_r\setminus G)+K=D,                   \tag{5}
\]

and

\[
 Y_a=X_a+G                                           \tag{6}
\]

when `G` is nonempty.  Fix the other external bundle and leave no charity.
When `G` is empty, omit (6).  The bundles are complete and disjoint because
they apply exactly the packet path

\[
 \mathrm{charity}\xrightarrow{f}q
 \xrightarrow{K}r
 \xrightarrow{G}a.                                 \tag{7}

The root receives the desired core `D` and strictly improves.  The external
sink, when present, strictly improves.  Owner `q` has exact change

\[
 v_q(Y_q)-v_q(X_q)=v_q(f)-v_q(K).                  \tag{8}

Hence `q` is either paid or is the unique possibly sacrificed owner.  In
both cases every EFX instance of (5)--(6) is a strict global lexicographic
improvement because the earlier root improves.

## Permanent anchor and response handoff

Since `K subseteq B_q`, the changed `q` target still contains

\[
 T_q+f\subseteq (X_q\setminus K)+f.                \tag{9}

Thus the permanent response edge `r -> q` survives and releases all of
`B_q`, including the packet `K` entering the changed root target.  The
packet `G` entering the sink is released by the root target, and `f` is
supplied by charity.  Every incoming path packet is therefore internally
supplied.

Consequently the complete-path response theorem applies verbatim:

1. an EFX endpoint contradicts global lexicographic maximality;
2. an internal response SDR is a release-compatible generalized PI
   component;
3. an outside response source strictly grows the owner union; and
4. every remaining maximum-matching obstruction is the already named
   root-anchored residual/Hall compression, with `q` sacrifice-eligible when
   (8) is negative.

The former root-monopoly pair is therefore not an additional terminal.  It
canonically maps into the same complete connected path and the same
sacrificed-`q` Hall boundary as the joint-packet branch.

## Claim boundary

This lemma eliminates the complete-path root-monopoly pair without an item
cap.  It does not terminate the resulting root-anchored sacrificed-`q`
compression/recapture reset, prove monotonicity of the retained-support and
response-rank potential, close `GG`, or prove four-agent/general additive
EFX.

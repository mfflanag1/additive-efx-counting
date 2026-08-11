# Root-critical alternating-frontier lemma

**Date:** 2026-08-11

**Status:** cap-free finite termination of the root-critical compensator
chain; the resulting top-reset/captured-bottom recurrence remains open

## Setting

Use the failed root-preserving selector and the notation of the
root-critical compensator dichotomy:

\[
 A\mathbin{\dot\cup}W=H\mathbin{\dot\cup}L,
 \qquad
 \delta=v_r(H)-v_r(A)=v_r(W)-v_r(L)\ge0.             \tag{1}
\]

The root core satisfies `v_r(A)>v_r(W)`.  The selected partition maximizes
`v_d(L)` subject to `v_r(H)>=v_r(A)`.  If `g` is the least-`d` good of `H`,
selector failure supplies

\[
 v_d(H-g)>v_d(L),
 \qquad
 v_r(g)>\delta.                                      \tag{2}
\]

## Alternating packet growth

Start with

\[
 R_0=\{g\}\subseteq H,
 \qquad S_{-1}=\varnothing\subseteq L.
\]

Then `v_d(R_0)>v_d(S_{-1})` by positivity and
`v_r(R_0)>v_r(S_{-1})+delta` by (2).  Given
`R_t,S_{t-1}` with these two strict inequalities, do the following.

1. If even `L` cannot compensate the root for `R_t`, namely

   \[
   v_r(L)<v_r(R_t)-\delta,                            \tag{3}
   \]

   stop.
2. Otherwise choose an inclusion-minimal `S_t` satisfying

   \[
   S_{t-1}\subseteq S_t\subseteq L,
   \qquad
   v_r(S_t)\ge v_r(R_t)-\delta.                      \tag{4}
   \]

   Exchanging `R_t` and `S_t` preserves the root constraint.  Selector
   maximality therefore forces

   \[
   v_d(S_t)\ge v_d(R_t),                             \tag{5}
   \]

   and nondegeneracy makes the inequality strict.
3. Since `R_t` contains `g`, equation (2) gives

   \[
   v_d(H)>v_d(L)\ge v_d(S_t).
   \]

   Choose an inclusion-minimal strict extension

   \[
   R_t\subsetneq R_{t+1}\subseteq H,
   \qquad
   v_d(R_{t+1})>v_d(S_t).                            \tag{6}
   \]

The old `S_t` cannot already satisfy (4) for `R_{t+1}`: if it did,
maximality would give `v_d(S_t)>=v_d(R_{t+1})`, contradicting (6).
Consequently every successful round strictly enlarges both packet sets:

\[
 R_0\subsetneq R_1\subsetneq\cdots\subseteq H,
 \qquad
 S_0\subsetneq S_1\subsetneq\cdots\subseteq L.      \tag{7}
\]

## Finite terminal support certificate

The process terminates after at most `|H|+|L|` strict packet additions.
Indeed, step 3 never exhausts before `R_t=H`, while at `R_t=H` condition
(3) must hold because

\[
 v_r(H)-\delta=v_r(A)>v_r(W)\ge v_r(L).              \tag{8}
\]

At the terminal packet `R`, (3) and (1) give

\[
 v_r(R)>v_r(L)+\delta=v_r(W).                        \tag{9}
\]

Split its support according to the old pool:

\[
 R_A=R\cap A,
 \qquad R_W=R\cap W.
\]

Cancelling the common packet `R_W` from (9) yields

\[
 v_r(R_A)>v_r(W\setminus R_W).                       \tag{10}
\]

In particular `R_A` is nonempty.  Thus the entire compensator chain ends
with a packet in the old root core that dominates the exact unrecruited
complement of the old residual.

## Flower routing

For `A=T_q+f`, equation (10) has two forms.

1. If `R_A\cap T_q` is nonempty, any nonempty top subpacket enters the
   top-core root exchange and its residual-reset continuation.
2. Otherwise `R_A={f}` and

   \[
   v_r(f)>v_r(W\setminus R_W).                       \tag{11}
   \]

   With `v_r(B_r)>=v_r(f)`, the packet
   `B_r\setminus(W\setminus R_W)` is nonempty.  This is the same
   captured-bottom handoff as before, now against a weakly smaller residual
   support.  If `R_W` is nonempty, the support has strictly decreased; if it
   is empty, (11) is the original f-only captured-bottom polarity.

Hence root-criticality cannot generate an infinite compensator chain.  It
terminates cap-free in a top exchange/reset or a captured-bottom dependency,
and the f-only branch records strict residual-support descent whenever the
chain recruited an old-residual good.

## Verification and claim boundary

[`root_critical_alternating_frontier_audit.json`](root_critical_alternating_frontier_audit.json)
checks the compensation exchange, the two forced alternating inequalities,
strict packet growth, terminality at the full root cell, and the terminal
support cancellation under Z3 5.0.0 and 4.15.3.

This lemma terminates the root-critical compensator chain.  It does not
prove that every subsequent top reset preserves a global potential, close
the captured-bottom owner handoff, eliminate the nonroot empty-target
recurrence, close `GG`, or prove four-agent/general additive EFX.

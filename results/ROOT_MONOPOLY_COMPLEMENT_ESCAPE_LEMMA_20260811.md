# Root-monopoly complement-escape lemma

**Date:** 2026-08-11

**Status:** cap-free termination of repeated root monopoly; the terminal
two-row bottom-capture polarity remains open

## Setting

Use the root-monopoly branch of the flower rank-one handoff.  Put

\[
 U=T_r+B_q,
\]

and let the root's common-safe desired response be

\[
 D=K_T+K_B,
 \qquad K_T\subseteq T_r,
 \quad \varnothing\ne K_B\subseteq B_q.             \tag{1}
\]

Thus

\[
 v_r(D)>v_r(X_r)=v_r(T_r+B_r).                       \tag{2}


Let

\[
 O=U\setminus D=(T_r\setminus K_T)+(B_q\setminus K_B). \tag{3}

## Root-row capture

Cancelling `K_T` from (2) gives the strict packet inequality

\[
 v_r(K_B)>
 v_r(T_r\setminus K_T)+v_r(B_r)>v_r(B_r).           \tag{4}

Thus even a partial bottom capture is quantitatively strong: the captured
`B_q` packet pays for the root's whole bottom and every omitted root-top
good.

## The root cannot monopolize the complement

Base EFX against `X_q=T_q+B_q` and nonempty `T_q` give

\[
 v_r(B_q)\le \tau_r(X_q)\le v_r(X_r).               \tag{5}

Positivity also gives `v_r(T_r)<v_r(X_r)`.  Therefore

\[
 v_r(U)=v_r(T_r)+v_r(B_q)<2v_r(X_r).                 \tag{6}

Suppose `q` still desires the complement:

\[
 v_q(O)>v_q(X_q).                                    \tag{7}

Choose any common-safe desired response core `E subseteq O`.  Its source
cannot be `r`.  Otherwise `D,E` would be disjoint and both worth more than
`X_r` to the root, forcing

\[
 v_r(U)\ge v_r(D)+v_r(E)>2v_r(X_r),

contradicting (6).  Hence (7) exposes a nonroot response source and restores
a rank-two response matching with the anchored root core.

## Terminal complement polarity

If (7) fails, use the live target inequality

\[
 v_q(U)-v_q(X_q)=v_q(T_r)-v_q(T_q)>0.

Since `U=D+O`, failure of (7) yields

\[
 v_q(D)
 \ge v_q(U)-v_q(X_q)
 =v_q(T_r)-v_q(T_q)>0.                               \tag{8}

Thus repeated root monopoly terminates after one complement check.  Either
a nonroot source restores rank two, or the same response core satisfies the
two-row certificate (4),(8): its `B_q` part dominates the root's omitted
base support, while the full core captures all of `q`'s strict top-surplus
margin.

This is the exact bottom-capture packet that the next compensation or Hall
augmentation must follow.

## Verification and claim boundary

[`root_monopoly_complement_escape_audit.json`](root_monopoly_complement_escape_audit.json)
checks the root-row cancellation, the base-EFX two-core exclusion, the
forced nonroot complement source, and the terminal `q`-surplus capture under
Z3 5.0.0 and 4.15.3.

This lemma terminates repeated rank-one root monopoly.  It does not convert
the terminal two-row packet into an EFX allocation or PI component,
terminate its compensation handoff, close `GG`, or prove four-agent/general
additive EFX.

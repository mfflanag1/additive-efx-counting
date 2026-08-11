# q-donor blockade captured-margin handoff lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of the protected-`q` donor blockade as an
independent third-owner terminal; the floater-consuming continuation and
repeated retained-bottom Hall gate remain open

## Protected donor choice

Use the third-owner root-replacement fork with donor `b=q` and choose as its
donor core the known protected split-support response

\[
 D=D(U)=(T_r\setminus U)+f,
 \qquad \mu_q=v_q(D)-v_q(X_q)>0.                   \tag{1}
\]

For `K subseteq D` and `G subseteq R\setminus C`, root feasibility is

\[
 v_r(K)-v_r(G)\ge\delta_r.                         \tag{2}
\]

After the correction that a weakly paid donor is sufficient, fork success
is exactly

\[
 v_q(K)-v_q(G)\le\mu_q.                            \tag{3}
\]

Indeed the captured source is restored strictly, so equality in (3) already
gives the strict lexicographic gain required by the surplus-budget endpoint.

## Strict blockade implies captured margin

Suppose the root-feasible family is nonempty but every feasible pair fails
(3).  Select any feasible `(K,G)`.  Then

\[
 v_q(K)-v_q(G)>\mu_q.                              \tag{4}
\]

Positivity gives `v_q(G)>=0`, hence

\[
 v_q(K)>\mu_q>0.                                   \tag{5}
\]

Thus `K` is nonempty and, by itself, captures the entire remaining protected
`q` response margin.  The donor blockade is therefore not a new residual or
Hall state.  It enters one of the two already named physical handoffs.

1. If `f notin K`, then `K subseteq T_r\setminus U`.  Updating
   `U'=U union K` strictly enlarges retained top support and makes
   `v_q(D(U'))<v_q(X_q)`.  Invoke the captured-`q`-margin anchored residual
   rotation.
2. If `f in K`, the packet consumes the unique floater.  Invoke the
   floater-consuming reset source trichotomy.  Any top part
   `K\setminus{f}` is recorded in `U` before that handoff.

There is no zero-loss exception.  If `delta_r<=0`, the empty pair is root
feasible and satisfies (3), because `mu_q>0`.  Hence a strict blockade also
forces

\[
 \delta_r>0,                                       \tag{6}
\]

which is precisely the root-critical polarity expected at the handoff.

## Consequence

For the protected-`q` donor, the third-owner selector now has only two live
outcomes: a weakly paid connected fork, or aggregate root concentration.
The former proceeds to the surplus-budget/response-augmentation check; the
strict donor blockade is absorbed by retained-top growth, captured-margin
rotation, or the floater-source trichotomy.  It cannot recur as an unchanged
fixed-support `q` residual state.

## Verification and boundary

[`q_donor_blockade_captured_margin_handoff_audit.json`](q_donor_blockade_captured_margin_handoff_audit.json)
checks the weak-payment boundary, strict captured-margin implication,
nonemptiness of `K`, strict root gap, and the floater/top support split in
exact linear arithmetic.

This lemma does not prove that every third-owner donor can be chosen as `q`,
discharge the surplus-budget inequalities of a successful fork, terminate
the floater-consuming handoff, close a repeated retained-bottom Hall state,
close `GG`, or prove four-agent/general additive EFX.

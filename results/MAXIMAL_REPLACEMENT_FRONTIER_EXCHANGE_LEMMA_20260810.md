# Maximal replacement-frontier exchange lemma

**Date:** 2026-08-10

**Status:** cap-free analytic selector invariant; compensation and the final
external Hall deficiency remain open

## Setting

Let `(X,{f})` be a positive, nondegenerate additive EFX allocation with
unenvied charity.  Assume the flower selector supplies a good `g in X_q`
with

\[
v_q(g)<v_q(f).
\]

Among all nonempty packets `R subsetneq X_q` satisfying

\[
v_q(R)<v_q(f), \tag{1}
\]

choose one maximizing `v_q(R)`.  This is a global packet choice, not an
inclusion-maximal continuation of a predetermined singleton.  Put

\[
C=X_q\setminus R,
\qquad
\sigma=v_q(f)-v_q(R)>0. \tag{2}
\]

The family in (1) is nonempty by the selector.  It is finite, so `R`
exists.  Charity dominance gives `v_q(X_q)>v_q(f)`, hence every maximizing
packet is proper.

## Frontier-crossing theorem

Every nonempty packet `S subseteq C` satisfies

\[
v_q(S)>\sigma. \tag{3}
\]

Indeed, `R+S` has value strictly larger than `R`.  If it is a proper subset
of `X_q` and had value below `f`, it would contradict maximality of `R`.
Equality with `f` is excluded by nondegeneracy.  If `R+S=X_q`, charity
dominance gives the same strict conclusion.

More generally, let `U subseteq R` and let nonempty `V subseteq C`.  If
`R-U+V` is a proper subset of `X_q` and

\[
v_q(V)>v_q(U), \tag{4}
\]

then the improvement crosses the whole frontier slack:

\[
v_q(V)-v_q(U)>\sigma. \tag{5}
\]

Otherwise `R-U+V` would be an eligible packet worth more than `R`.
Thus no exchange from the selected side to the residual side can improve
`q` by an amount in the forbidden band `(0,sigma]`.  In particular, for
every `u in R` and `h in C`,

\[
v_q(h)>v_q(u)
\quad\Longrightarrow\quad
v_q(h)>v_q(u)+\sigma. \tag{6}
\]

This strict exchange gap is the useful content of choosing a value-maximal
frontier rather than merely an inclusion-maximal packet.

## Consequence for a surviving external response

Apply the packet-replacement complement-return lemma to the target

\[
C+f.
\]

Suppose an external source `a` survives all direct and complement returns,
with desired response

\[
A=K+f,
\qquad
\varnothing\ne K\subseteq C.
\]

The strict core-capture interval gives

\[
v_q(X_a)<v_q(K)<v_q(X_q)-v_q(f). \tag{7}
\]

Writing `D=C\setminus K`, equations (2) and (7) imply

\[
D\ne\varnothing,
\qquad
v_q(D)>\sigma. \tag{8}
\]

Consequently the whole released complement

\[
O_q=X_q\setminus K=R+D
\]

strictly crosses the charity threshold:

\[
v_q(R)<v_q(f)<v_q(O_q). \tag{9}
\]

Every individual good of `D` already crosses the residual slack.  Hence a
surviving blocker cannot be modeled as an arbitrarily small perturbation of
the chosen replacement: it leaves a nonempty, threshold-crossing pivot on
the released side.

## Interaction with the paid root flip

The complement-return lemma supplies `P subseteq T_r` with

\[
v_q(P)>\Delta_a,
\qquad
\Delta_a=v_q(K)-v_q(X_a)>0.
\]

The canonical root flip closes if some `H subseteq O_q` satisfies

\[
v_r(H)\ge v_r(P),
\qquad
v_q(P)>\Delta_a+v_q(H). \tag{10}
\]

The frontier theorem does **not** assert (10): (3)--(6) constrain only
`q`'s row, whereas (10) is a genuinely two-row indivisible exchange.  Its
role is instead to give a strict discrete potential for an adaptive
continuation.  Any attempted evolution of `R` that improves its `q`-value
must jump across `f`; any continuation that stays below `f` must weakly
decrease the selected frontier value.  A finite component proof may
therefore orient every replacement change by the pair

\[
(v_q(R),\ \text{number of represented response owners}), \tag{11}
\]

with external-owner growth ordered before a decrease of the frontier.

The seven frozen flower profiles provide an adversarial check rather than
a proof.  Their raw unperturbed rational representatives may lie on an
equality boundary, so the census tests the weak crossing form before the
nondegenerate perturbation; every displayed external response either has a
`q` return or admits (10).  The stronger live-polarity bounded
profile considered during proof mining has one uncompensated capture, but
its return target exposes the other external owner; this confirms that
external augmentation, not a universal compensation assertion, is needed.

The scalar implications replay in
[`maximal_replacement_frontier_exchange_audit.json`](maximal_replacement_frontier_exchange_audit.json),
and the frozen-profile census is
[`maximal_replacement_frontier_profile_census.json`](maximal_replacement_frontier_profile_census.json).

## Claim boundary

This lemma proves a cap-free global selector and a strict exchange-gap
potential.  It does not prove the two-row compensation system (10), show
that every exposed external source increases the potential (11), eliminate
the final Hall defect, close the `GG` flower, or prove four-agent additive
EFX.

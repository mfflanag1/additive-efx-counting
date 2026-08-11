# Top-core root-exchange lemma

**Date:** 2026-08-10

**Status:** cap-free analytic root/order flip; one critical reverse-order
wall remains

## Setting

Use the surviving full-reservoir R-wall.  The top-capture lemma supplies a
nonempty packet

\[
K_T=K\cap T_q

\]

satisfying

\[
v_r(K_T)>v_r(B_q\setminus K_B)+v_r(X_a). \tag{1}

\]

The flower also gives

\[
v_q(T_r+f)>v_q(X_q)>v_q(K_T). \tag{2}

\]

## Minimal return packet

By (2), choose an inclusion-minimal packet `P' subseteq T_r` such that

\[
v_q(P')+v_q(f)>v_q(K_T). \tag{3}

\]

The packet may be empty if `q(f)>q(K_T)`; otherwise it is nonempty and every
good is payment-critical:

\[
v_q(P'\setminus\{p\})+v_q(f)<v_q(K_T)
\qquad(p\in P'). \tag{4}

\]

Strictness in (4) uses nondegeneracy.

## Root exchange

Transfer `K_T` from `q` to `r`, give `f` to `q`, and return `P'` from `r`
to `q`:

\[
Y_q=(X_q\setminus K_T)+P'+f,

\]

\[
Y_r=(X_r\setminus P')+K_T, \tag{5}

\]

fixing both external owners.  This is a complete allocation.  Agent `q`
strictly improves by (3).  If

\[
v_r(K_T)\ge v_r(P'), \tag{6}

\]

then `r` is weakly nonworse and (5) is the required later-owner component.
If (5) is EFX it closes directly; its two response targets have labels

| target | incoming | release |
|---|---|---|
| `q` | `P'+f` | `K_T` |
| `r` | `K_T` | `P'` |

so every internal response SDR is a release-compatible PI edge set.

## Exact survivor order

Failure of (6) is strict by nondegeneracy:

\[
v_r(P')>v_r(K_T). \tag{7}

\]

Together with (1), the only surviving R-wall therefore satisfies

\[
v_r(P')>v_r(K_T)>
v_r(B_q\setminus K_B)+v_r(X_a), \tag{8}

\]

while (3)--(4) say that `P'` is a deletion-minimal payment for `K_T` in
`q`'s row.  Thus the residual is no longer an arbitrary top-core response:
it is a two-row critical exchange with a strict reverse order in `r`'s row.

The scalar selector and support replay in
[`top_core_root_exchange_audit.json`](top_core_root_exchange_audit.json).

## Claim boundary

This lemma closes every top-core R-wall satisfying (6) and reduces all
others to the critical reverse order (8).  It does not eliminate (8), prove
that every blocked exchange response augments to an SDR, eliminate the
all-owner Hall branch, close the `GG` flower, or prove four-agent additive
EFX.

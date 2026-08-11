# Dual-pool minimal core-extraction lemma

**Date:** 2026-08-11

**Status:** cap-free conversion of the aggregate dual-pool deficit; terminal
source-capture compensation remains open

## Setting

Use the dual flower cores

\[
 D_q=T_r+f,
 \qquad A_a\subseteq T_q+B_r,
\]

with distinct sources `q` and `a in {c,s}`, and let

\[
 P=\left(\mathop{\dot\bigcup}_{i\in N}X_i+f\right)
   \setminus(D_q\mathbin{\dot\cup}A_a).
\]

Assume the dual-pool deficit from the root-paid selector:

\[
 v_r(P)<v_r(X_r).                                    \tag{1}
\]

## Minimal extraction

Because `P+D_q+A_a` is the union of all base bundles and `f`, and valuations
are positive, there is a nonempty
packet

\[
 C=C_q\mathbin{\dot\cup}C_a,
 \qquad C_q\subseteq D_q,
 \quad C_a\subseteq A_a,                             \tag{2}
\]

such that

\[
 v_r(P+C)\ge v_r(X_r).                               \tag{3}

Choose `C` inclusion-minimal.  For every `g in C`,

\[
 v_r(P+C-g)<v_r(X_r).                                \tag{4}

Writing

\[
 \Delta=v_r(X_r)-v_r(P)>0,
\]

equations (3)--(4) are equivalently

\[
 v_r(C)\ge\Delta,
 \qquad
 v_r(g)>v_r(C)-\Delta\quad(g\in C).                 \tag{5}

Thus the aggregate deficit always exposes a finite, item-critical packet
inside the two dual cores; it cannot recur as an unnamed scalar wall.

## Source-payment trichotomy

Put

\[
 D'_q=D_q\setminus C_q,
 \qquad A'_a=A_a\setminus C_a.                       \tag{6}

Deleting goods preserves common safety: for every nonempty proper subset
`S subset A`, positivity gives
`tau_i(S)<=v_i(S)<=v_i(A)-min_{g in A}v_i(g)=tau_i(A)`; the empty and
unchanged cases are immediate.  If

\[
 v_q(D'_q)>v_q(X_q),
 \qquad v_a(A'_a)>v_a(X_a),                          \tag{7}

both reduced cores remain valid disjoint desired cores.  Their complement
is exactly `P+C`, which pays the earlier root by (3).  The dual-anchor
root-paid selector therefore applies with `D'_q,A'_a`: it yields an EFX
flower improvement, a release-compatible response/Hall boundary, or an
item-named root-critical certificate.

If (7) fails, one of the extracted packets captures the corresponding
source's whole strict response margin.  Explicitly, with

\[
 \mu_q=v_q(D_q)-v_q(X_q)>0,
 \qquad \mu_a=v_a(A_a)-v_a(X_a)>0,                  \tag{8}

failure gives

\[
 v_q(C_q)\ge\mu_q                                   \tag{9}

or

\[
 v_a(C_a)\ge\mu_a.                                  \tag{10}

The alternatives are exhaustive and may both hold.  Equations (5), (9),
and (10) attach the same physical extraction packet to the root-payment row
and to at least one displaced source row.  This is the exact two-row packet
that the next compensation or owner-transfer component must follow.

## Full-capture form

In the full-`X_q` capture normal form, write

\[
 A_a=T_q+H,
 \qquad \varnothing\ne H\subseteq B_r.
\]

Then

\[
 P=(B_r\setminus H)+B_q+X_c+X_s,
\]

and (1) cancels to the sharper support certificate

\[
 v_r(T_r+H)>v_r(B_q+X_c+X_s).                       \tag{11}

Hence the failed dual reset is exactly a root-top/captured-bottom payment
problem.  Any repair must either remove a packet from `T_r+f`, remove a
packet from `T_q+H`, or abandon one of the two dual response sources; (2)--
(10) classify these possibilities without fixing a packet size.

## Verification and claim boundary

[`dual_pool_minimal_core_extraction_audit.json`](dual_pool_minimal_core_extraction_audit.json)
checks existence at the full dual union, minimality, both critical-value
rewrites, the source-margin alternatives, and the full-capture cancellation.

This lemma converts every aggregate dual-pool deficit into either a
root-payable reduced-core selector or a named two-row captured packet.  It
does not compensate a source satisfying (9) or (10), terminate a later
root-critical/reset recurrence, close `GG`, or prove four-agent/general
additive EFX.

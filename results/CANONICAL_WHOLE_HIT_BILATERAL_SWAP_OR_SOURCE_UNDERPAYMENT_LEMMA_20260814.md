# Canonical whole-hit bilateral swap or source-underpayment lemma

**Date:** 2026-08-14

**Status:** cap-free current-response reduction inside the actual canonical
ledger-free state; base-floor responses and exact normalization-bypass
recurrence remain open

## Actual-state input

Let `Z` be the canonical ledger-free realization of an exact
`T_{L,times}^*` collision, and let the named retired packet `K` remain with
its recorded current holder `h`. Write

\[
 Z_h=K\mathbin{\dot\cup}H.                       \tag{1}
\]

Suppose an EFX wall at `Z` extracts a globally minimum **current** response
`D` with source `t` and target `h`, and suppose the response hits the whole
packet:

\[
 K\subseteq D\subseteq Z_h,
 \qquad v_t(D)>v_t(Z_t).                         \tag{2}
\]

Current means that the source benchmark is its actual utility at `Z`, not a
lower base or sacrifice floor.

## Whole-hit localization

Because canonical cancellation leaves all of `K` in the single holder
target, any single-target response containing all of `K` must target `h`.
Its source cannot be `h`: a subset of `Z_h` cannot be strictly preferred by
`h` to `Z_h` under positive additivity.

The response is proper. Indeed, the EFX wall gives a good `g in Z_h` with

\[
 v_t(Z_h-g)>v_t(Z_t),                            \tag{3}
\]

so global minimum-cardinality extraction cannot select the whole `Z_h`.
Consequently

\[
 L=Z_h\setminus D
\]

is nonempty and ledger-free, and for `D`'s whole-hit branch

\[
 \varnothing\ne L\subseteq H,
 \qquad D=K\mathbin{\dot\cup}(H\setminus L).    \tag{4}
\]

In particular, a holder target equal to `K` admits no whole-hit current
response.

Minimum-cardinality extraction also makes every good of `D` critical in the
source row. If

\[
 m_t=v_t(D)-v_t(Z_t)>0,
\]

then

\[
 v_t(g)\ge m_t\quad(g\in D),                    \tag{5}
\]

including every retired atom `g in K`.

## Supplier-closed bilateral test

Exchange the response and source bundle while leaving the holder residual in
place:

\[
 Z'_t=D,
 \qquad Z'_h=L\mathbin{\dot\cup}Z_t,            \tag{6}
\]

and leave every other target and charity unchanged. This is a physical
two-owner exchange: `h` supplies `D`, `t` supplies `Z_t`, and `L` never
moves. The source strictly improves. The holder is weakly nonworse exactly
when

\[
 v_h(Z_t)\ge v_h(D).                             \tag{7}
\]

When (7) holds, all assigned utilities weakly increase and the response
target `D` is current-safe. Therefore the only possible new EFX walls are
against the new holder target `L+Z_t`. That target is disjoint from `K`, so
every response extracted from a new wall is ledger-free. The admitted
bilateral exchange consequently yields one of:

1. an EFX allocation Pareto-above `Z`, preserving whatever strict
   fixed-priority certificate the canonical candidate carries relative to
   the globally maximal base;
2. a genuinely new ledger-free signed response/state coordinate; or
3. the already typed exact normalization-bypass recurrence.

It never returns a whole-`K` collision in the same step.

If (7) fails, the exact remaining charge is

\[
 v_h(Z_t)<v_h(D).                                \tag{8}
\]

Thus a current whole-hit recurrence can survive the direct physical swap
only when the response source's entire current bundle is worth less to the
holder than the desired response it receives. This is a named cross-row
source-underpayment separator, sharper than an anonymous missing
compensation packet.

## Claim boundary

This lemma uses the actual canonical state and the already permitted
bilateral exchange, so it does not rely on the counterfactual global donation
candidates. It proves localization (4), source criticality (5), and the
swap/underpayment dichotomy (7)--(8). It does not eliminate (8), turn a
base-floor-safe core into a current response, terminate an exact repeated
ledger-free normalization bypass, close `T_{L,times}^*`, or prove
four-agent/general EFX.

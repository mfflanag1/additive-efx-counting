# Universal full-owner charity-exchange extraction theorem

**Date:** 2026-08-12

**Status:** cap-free closure of the exact saturated four-owner decorated-
response/base-margin separator; conditional on the named GG separator and
response-continuation premises below

## Saturated terminal

Let `(X,Q)` be a positive additive four-owner EFX-with-charity allocation,
chosen globally lexicographically maximal in the fixed GG priority order.
Assume the exact full-owner terminal of the
[`FOUR_OWNER_DECORATED_COMPONENT_EXHAUSTION_LEMMA_20260811.md`](FOUR_OWNER_DECORATED_COMPONENT_EXHAUSTION_LEMMA_20260811.md):

1. a nonself, current-safe desired response `D subseteq Y_t` into an owner
   hole `t` is fixed together with its complete signed transfer record;
2. all four owners occur in the physical response component;
3. the component-wide base-margin separator holds for every debt-removing
   packet and every redistribution of the represented pool;
4. the sacrificed source's direct EFX and charity-safety alternative fails;
   and
5. exact response records, physical supports, owner coverage, and current
   utilities within a fixed record are saturated.

Here saturation means that none of the following is available: a new full
decorated response record, strict physical support/component growth, a
release-compatible PI or self-response component, or strict same-record
current-utility progress.  This explicit terminal condition is essential;
omitting any one of these exclusions recovers only a continuation theorem.

## Canonical Hamiltonian representation

By the rank-four five-target matching classification, every PI-free survivor
has a Hamiltonian owner-to-charity path

\[
 h_0=t\longrightarrow h_1\longrightarrow h_2
 \longrightarrow h_3\longrightarrow c.           \tag{1}
\]

Write `A_i` for the core assigned by owner `i` to its successor target,
`R_i` for the residual of target `i` after deleting its incoming core, and

\[
  Y_t=D\mathbin{\dot\cup}R_t.
\]

The response source is some `s=h_k`, `k in {1,2,3}`.  It cannot be `t`,
because positivity prevents a proper subset of `Y_t` from being strictly
preferred by `t` to `Y_t`.

Choose a least-`t` good `g in D` and put `P=D-g`.  Before any charity repair,
form

\[
 Z_t=P,
 \qquad Z_i=A_i\mathbin{\dot\cup}R_i\quad(i\ne t), \tag{2}
\]

with provisional charity

\[
 Q'=A_t\mathbin{\dot\cup}\{g\}\mathbin{\dot\cup}R_t
     \mathbin{\dot\cup}R_c.                       \tag{3}
\]

Equations (2)--(3) are a partition of exactly the old goods.  Relative to
the paid path state, their nontrivial supplier edges include

\[
 c\to h_3\to h_2\to h_1\to c,
 \qquad h_0\to c.                                 \tag{4}
\]

Thus the construction is one connected charity-exchange component and is
genuinely cyclic.  Charity both donates `A_{h_3}` and receives replacement
packets.  Packet sizes are unrestricted.

## Payment and safety

The target separator and least-good deletion give

\[
 v_t(P)=\tau_t(D)>v_t(A_t+R_t)>v_t(X_t).          \tag{5}
\]

For every owner other than `t` and the closing source, failure to pay against
`D` would give the mixed-margin self-response/progress exit.  Saturation
excludes that exit, so `A_i+R_i` pays against `D`, and therefore also against
`P` by deletion monotonicity.

For the closing source `s`, either

\[
 v_s(A_s+R_s)\ge\tau_s(P),                        \tag{6}
\]

or current safety of `D` implies

\[
 v_s(C_s)>v_s(A_s)>v_s(X_s),                      \tag{7}
\]

which is a self-response/progress exit.  Saturation excludes (7), hence (6)
holds.  All four owners are therefore strictly above their GG base and paid
against the returned target `P`.

If an owner target in (2) is unsafe, current-minimal extraction gives either
a new decorated record, PI/self-response, support growth, or strict
same-record progress.  All are excluded at the saturated terminal.  Hence
every owner target is safe.

If `Q'` is safe, (2)--(3) are already EFX with charity.  If `Q'` is unsafe,
the arbitrary-packet blocker collapse gives the whole packet to a blocker
and parks one blocker good.  This strictly improves that owner and reduces
charity to a singleton.  The finite singleton-charity exchange walk ends in
EFX or one of the same four saturated progress exits.  The latter are
excluded.  Consequently the walk must end in an EFX-with-charity allocation
strictly lexicographically above `(X,Q)`.

At the EFX endpoint, put

\[
 \Delta_i=v_i(Z_i)-v_i(X_i)\ge0.
\]

The owner-target and charity inequalities imply, for every changed observer,

\[
 \tau_i(Z_j)-v_i(X_i)\le\Delta_i,
 \qquad v_i(Q')-v_i(X_i)\le\Delta_i.             \tag{8}
\]

Thus the final packets satisfy every owner-payment, observer-surplus,
charity-safety, and lexicographic-improvement inequality of the
surplus-budgeted charity-exchange endpoint theorem.

## Theorem

There is no positive additive rational or real countermodel to the exact
saturated full-owner decorated-response/base-margin separator together with
the complete GG continuation premises above.  Every such terminal extracts
an EFX lexicographic improvement supported by a connected charity-exchange
component; before optional blocker repair, the canonical component is the
cyclic graph (4).  Therefore the putative saturated terminal contradicts
global lexicographic maximality.

The argument is cap-free: it uses four owners, but no bound on goods, packet
cardinalities, values, or moved-good radius.  Cycles and replacement packets
received by charity are explicitly permitted and used.

## Independent verification and exact boundary

[`audit_universal_full_owner_charity_exchange_extraction.py`](../tracks/parkability/audit_universal_full_owner_charity_exchange_extraction.py)
is a standalone encoding.  It does not import a prior selector.  It
enumerates all 24 Hamiltonian paths and 72 nonself response sources,
constructs the physical atom partition (2)--(3), verifies conservation,
connectedness and the charity cycle, and independently checks the payment,
surplus-budget, and saturated-outcome implications in QF_LRA/Boolean logic.
The resulting exact manifest is
[`universal_full_owner_charity_exchange_extraction_audit.json`](universal_full_owner_charity_exchange_extraction_audit.json).

This theorem closes **the declared saturated full-owner separator**.  It
does not prove that every other GG/Hall branch reaches this separator, close
the outstanding fixed-`U` retained-support recurrence, prove the full GG
theorem, or prove four-agent/general additive EFX.  Those statements remain
strictly outside the claim.

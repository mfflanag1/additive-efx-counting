# Supplier saturation does not force mixed-cycle observer payment

**Date:** 2026-08-13

**Status:** exact cap-free refutation of the generic payment implication;
the globally recurrent GG strengthening remains open

## Frozen implication

The post-recruitment manuscripts use the following data before invoking the
remaining observer-payment step.

1. Four owners lie on a directed cycle of pairwise-disjoint selected cores.
2. One or more cores are current-desired/current-safe (decorated), while the
   remaining cores are base-desired/base-common-safe (old).
3. Every core and incoming packet is supplied by an owner on the cycle, so
   the cycle is physically release-compatible.
4. Each old source may receive its outgoing core together with residual goods
   released from its own current target.
5. The permanent old edge `r -> q` remains selected and its core is retained
   by the root.

The generic implication under audit is that supplier saturation plus these
response inequalities forces the residual-completed cycle to pay every
observer debt.  It is false.

## Exact anchored countermodel

Use the owner order

\[
 r\longrightarrow q\longrightarrow a\longrightarrow b
 \longrightarrow r.                              \tag{1}
\]

The selected cores are

\[
 K_r\subseteq Y_q,\quad D=\{d_1,d_2\}\subseteq Y_a,
 \quad K_a\subseteq Y_b,\quad K_b\subseteq Y_r.  \tag{2}
\]

`K_r`, `K_a`, and `K_b` are old singleton cores.  `D` is the unique
decorated core and is sourced by `q`.  Write

\[
 Y_i=C_i\mathbin{\dot\cup}R_i                    \tag{3}
\]

for the incoming core and a positive singleton residual at every target.
All base floors are 10.  The audit records a positive rational valuation
table with the following decisive entries:

\[
 v_q(D)=13>v_q(Y_q)=12,                           \tag{4}
\]

and

\[
 \tau_a(D)=12\le v_a(Y_a)=13.1.                  \tag{5}
\]

Thus `D` is current-desired by `q` and current-safe for every observer.
Every old singleton core is base-desired by its source and automatically
base-common-safe.

Rotate the cores around (1), retaining the permanent anchor `K_r` with the
root.  The blocked old source `a` receives `K_a`.  Even if `a` receives the
complete residual pool

\[
 \mathcal R=R_r\mathbin{\dot\cup}R_q
             \mathbin{\dot\cup}R_a
             \mathbin{\dot\cup}R_b,
\]

the audit has

\[
 v_a(K_a+\mathcal R)=11.4<12=\tau_a(D).          \tag{6}
\]

Consequently no allocation of residual goods can pay row `a` while the four
selected cores are kept intact.  In the natural residual-return allocation,
`a` is even further below the deletion threshold of `D+R_q`, so that
allocation is not EFX.

All selected supports lie in targets owned by members of (1); hence the
supplier closure is already all four owners.  The permanent root anchor is
not cut, released, or duplicated.  Supplier saturation therefore proves
physical availability but not observer payment.

## Exact surviving separator

The failure is localized at the head of a decorated edge.  In row `a`,

\[
 v_a(D)>v_a(K_a),                                 \tag{7}
\]

as follows generally by cancelling `R_a` from

\[
 v_a(K_a+R_a)<\tau_a(T)\le v_a(D+R_a).
\]

Unlike an old incoming core, `D` need not be base-common-safe, so (7) does
not produce the old-core self-response used for nondecorated heads.  The
smallest operation missing from the generic theorem is therefore a
**decorated-head exchange**: split or replace `D`, change its source, or
bring in another selected core while preserving the decorated source's
strict current floor.

## Consequence for the GG program

The generic supplier-saturated observer-payment theorem is refuted.  A valid
replacement must use an additional flower/GG maximality inequality that
rules out (6), or explicitly include a decorated-head exchange operation.
The same correction applies to the anchor-source branch: `R_q` alone is not
the complete physical compensation family; the relevant first selector is
the complete signed residual pool, as proved in
[`ROOT_SOURCED_COMPLETE_SIGNED_RESIDUAL_COMPENSATION_LEMMA_20260813.md`](ROOT_SOURCED_COMPLETE_SIGNED_RESIDUAL_COMPENSATION_LEMMA_20260813.md).

## Claim boundary

The countermodel exactly satisfies the stated mixed response, current/base
safety, physical cycle, supplier-saturation, residual-return, and permanent
anchor premises.  It refutes the implication from those premises to
observer payment.  It is not asserted to be an exact recurrent state of the
full GG algorithm, a globally lexicographically maximal EFX base, or a
counterexample to four-agent additive EFX.  Those stronger hypotheses may
still force a decorated-head exchange and are the remaining live route.

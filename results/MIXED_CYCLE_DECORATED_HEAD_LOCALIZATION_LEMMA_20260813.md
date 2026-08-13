# Mixed-cycle decorated-head localization lemma

**Date:** 2026-08-13

**Status:** cap-free localization of every terminal observer-payment failure
to at most two decorated-to-old boundaries

## Mixed cycle

Let the four owners lie on a supplier-saturated directed cycle.  For owner
`i`, let `O_i` be her outgoing selected core, let `C_i` be the incoming core
contained in her current target, and write

\[
 Y_i=C_i\mathbin{\dot\cup}R_i.                  \tag{1}
\]

Each selected core is exactly one of the following.

- **Old:** `v_i(O_i)>v_i(X_i)` and `O_i` is base-common-safe.
- **Decorated:** `v_i(O_i)>v_i(Y_i)` and `O_i` is current-safe.

Give each source the residual-completed outgoing bundle

\[
 Z_i=O_i\mathbin{\dot\cup}R_i.                  \tag{2}
\]

Let `T` be any allocated current-safe special target, so

\[
 \tau_i(T)\le v_i(Y_i).                         \tag{3}
\]

## Localization

Suppose row `i` is underfunded against `T`:

\[
 v_i(Z_i)<\tau_i(T).                             \tag{4}
\]

Then `O_i` cannot be decorated, because in that case

\[
 v_i(Z_i)\ge v_i(O_i)>v_i(Y_i)\ge\tau_i(T),
\]

contradicting (4). Hence the outgoing edge at `i` is old.

Using (1), (3), and (4), cancellation gives

\[
 v_i(O_i)+v_i(R_i)
 <\tau_i(T)
 \le v_i(C_i)+v_i(R_i),
\]

and therefore

\[
 v_i(C_i)>v_i(O_i)>v_i(X_i).                    \tag{5}
\]

If `C_i` were old, it would be a base-common-safe desired core sourced by
`i` into her own current target.  This is the existing self-response branch:
a new source/core label, matching pivot, internally supplied PI edge, or
strict support transition.  Consequently, after those ordinary progress
outcomes are excluded by exact response saturation, `C_i` must be decorated.

Thus every terminal blocker is exactly a vertex whose incoming edge is
decorated and whose outgoing edge is old—a **decorated head**.

## Four-cycle consequence

Encode the four cycle edges cyclically by `D` and `O`.  The mixed case has
between one and three decorated edges. Decorated heads are precisely the
cyclic transitions

\[
 D\longrightarrow O.                            \tag{6}
\]

Every nonconstant binary four-cycle has at most two such transitions.
More precisely:

- one decorated edge gives one head;
- two adjacent decorated edges give one head;
- two alternating decorated edges give two heads; and
- three decorated edges give one head.

The permanent root edge `r -> q` is old, so the same bound applies to every
anchored mixed cycle.  Supplier-saturated observer payment is therefore not
a four-row problem.  After standard response/pivot progress is removed, it
is a one-head exchange except in the unique alternating `D,O,D,O` topology,
where it is a coupled two-head exchange.

## Relation to the exact falsifier

The countermodel in
[`SUPPLIER_SATURATION_DOES_NOT_FORCE_MIXED_CYCLE_PAYMENT_20260813.md`](SUPPLIER_SATURATION_DOES_NOT_FORCE_MIXED_CYCLE_PAYMENT_20260813.md)
has one decorated edge `q -> a`, followed by the old edge `a -> b`; its sole
blocked row is exactly the decorated head `a`.  It therefore shows that the
one-head case is genuine, not merely an artifact of the proof.

For a root-sourced overlap while retaining the permanent anchor, residual
accounting must additionally use the complete pool in
[`ROOT_SOURCED_COMPLETE_SIGNED_RESIDUAL_COMPENSATION_LEMMA_20260813.md`](ROOT_SOURCED_COMPLETE_SIGNED_RESIDUAL_COMPENSATION_LEMMA_20260813.md).

## Claim boundary

This lemma proves the scalar localization, the old-incoming self-response,
and the exact at-most-two cyclic count without an item or value cap. It does
not force the one-head or alternating two-head exchange, prove that an old
self-response always terminates an exact GG recurrence, eliminate full-pool
capture, close GG, or prove four-agent/general additive EFX.

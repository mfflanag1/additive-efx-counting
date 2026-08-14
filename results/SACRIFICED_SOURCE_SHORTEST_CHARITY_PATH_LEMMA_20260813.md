# Sacrificed-source shortest charity-path lemma

**Date:** 2026-08-13

**Status:** cap-free functional payment skeleton for both exact response
forms; one endpoint margin and observer safety remain

## Correct path orientation

In either corrected exact response form, begin at the sacrificed owner `d`
and follow a simple directed response path until the last paid owner `h`.
Reverse only that path's response cores and give singleton charity `{p}` to
`h`.  Every owner outside the path keeps its complete paid support bundle.

This differs essentially from completing a Hamiltonian path through every
owner: an already-paid off-path source need not receive a response core, and
`d` need not release its residual after being repaired.

## Two-cycle form R2

The two available response paths from `d` are

\[
 d\to r\to q,
 \qquad d\to q\to r.                              \tag{1}
\]

Their reverse transfer paths are

\[
 \mathrm{charity}\to q\to r\to d,
 \qquad \mathrm{charity}\to r\to q\to d.         \tag{2}
\]

Each uses three support edges.  Owner `s` keeps all of `Y_s`; `d` keeps all
of `W` and receives its desired core.  The internal path source and `d` are
strictly paid, and `s` remains paid.  Only endpoint `h in {q,r}` can lose
payment.

## Three-cycle form R3

The two paths from `d` are

\[
 d\to r\to q\to s,
 \qquad d\to q\to s\to r.                        \tag{3}
\]

Their reverse transfer paths are

\[
 \mathrm{charity}\to s\to q\to r\to d,
 \qquad \mathrm{charity}\to r\to s\to q\to d.   \tag{4}
\]

Each uses four support edges.  All three nonendpoint path sources receive
desired cores and are strictly paid.  Again only endpoint `h in {s,r}` can
lose payment.

## Exact endpoint separator

Let `C_h` be the response core removed from endpoint `h`, and let

\[
 \Delta_h=v_h(Y_h)-v_h(X_h)\ge0.
\]

The endpoint keeps every other current good and receives `p`, so its exact
base margin is

\[
 m_h=\Delta_h-v_h(C_h)+v_h(p).                    \tag{5}
\]

Endpoint payment fails exactly when

\[
 v_h(C_h)>\Delta_h+v_h(p).                        \tag{6}
\]

Thus a weakly paid functional candidate exists unless both available
shortest paths suffer endpoint capture.  At saturation, simultaneous capture
must be converted into retained-support growth, response replacement, a
release-compatible component, or another paid functional topology.

If the candidate is paid but not EFX, the paid-splice observer-failure lemma
turns the failure into a complete decorated current response.  The remaining
gate is therefore exact repeated-component extraction, not arbitrary direct
verification of all observer inequalities.

## Verification and boundary

[`audit_sacrificed_source_shortest_charity_path.py`](../tracks/parkability/audit_sacrificed_source_shortest_charity_path.py)
constructs all four paths for arbitrary symbolic packet atoms, verifies
conservation, functionality, the edge bounds, preservation of off-path
bundles, strict payment of nonendpoints, and the endpoint identity in exact
QF-LRA.

This lemma does not reverse simultaneous endpoint capture, prove observer
safety, prove a paid functional candidate exists in every saturated state,
or close the four-edge theorem.

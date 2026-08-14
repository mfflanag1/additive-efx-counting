# Two-survivor Hamiltonian charity-path selector lemma

**Date:** 2026-08-13

**Status:** cap-free four-edge support and three-owner payment closure; one
endpoint margin plus observer safety remains

**Boundary update:** this path family is not exhaustive. Exact rational
profiles in both survivor forms defeat the union of all named response-
derived topologies; see
`TWO_SURVIVOR_NAMED_TOPOLOGY_SELECTOR_REFUTATION_20260813.md`.

## Four physical paths

For the two-cycle response form, both response paths

\[
 s\to d\to r\to q,
 \qquad s\to d\to q\to r                         \tag{1}
\]

exist. For the three-cycle response form, both

\[
 d\to r\to q\to s,
 \qquad d\to q\to s\to r                         \tag{2}
\]

exist. Each path visits every owner exactly once and uses three of the five
live response edges.

Reverse the three path cores and give the singleton charity token to the
path endpoint. This produces respectively the support-transfer path

\[
 \text{charity}\to h\to i_2\to i_1\to i_0,       \tag{3}
\]

where `h` is the response-path endpoint. It conserves every good, empties
charity, and uses exactly four support-provenance edges. Core and residual
packet sizes are unrestricted.

## Payment

The three nonendpoint response sources receive their desired cores and are
strictly above base. Only endpoint `h` can be unpaid. If `C_h` is the path
core removed from its current bundle, its exact final base margin is

\[
 m_h=\Delta_h-v_h(C_h)+v_h(p),
 \qquad \Delta_h=v_h(Y_h)-v_h(X_h).               \tag{4}
\]

Thus endpoint failure is the strict capture inequality

\[
 v_h(C_h)>\Delta_h+v_h(p).                        \tag{5}
\]

The two endpoint choices are `{q,r}` for the two-cycle form and `{s,r}` for
the three-cycle form.

## Remaining implication

At exact saturation, prove that at least one endpoint candidate has
nonnegative margin and that every enlarged target is observer-safe. If both
endpoint candidates fail, their two strict capture inequalities (5) occur on
the paid response cycle. The intended contradiction is then one of:

1. a release-compatible PI cycle;
2. a new self/decorated response;
3. strict signed support/component growth; or
4. replacement of a captured core by a disjoint response packet.

This is a two-choice scalar gate, not an arbitrary graph search.

## Verification and boundary

[`audit_two_survivor_charity_path_selector.py`](../tracks/parkability/audit_two_survivor_charity_path_selector.py)
independently builds all four paths, verifies exact atom conservation and the
four-edge count, and proves the payment identity and capture implication in
QF-LRA.

The lemma does not eliminate simultaneous endpoint capture or prove final
observer safety, so the universal four-edge theorem remains open.

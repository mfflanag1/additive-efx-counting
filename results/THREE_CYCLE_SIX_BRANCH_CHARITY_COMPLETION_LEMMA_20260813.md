# Three-cycle six-branch charity-completion lemma

**Date:** 2026-08-13

**Status:** cap-free six-branch support and three-owner payment normal form;
simultaneous endpoint/observer failure remains

**Boundary update:** these six branches are not exhaustive. Their complete
topology union is refuted as a universal selector in
`TWO_SURVIVOR_NAMED_TOPOLOGY_SELECTOR_REFUTATION_20260813.md`.

## Six branches

In the three-cycle survivor, the paid response cycle is

\[
 r\to q\to s\to r,                                \tag{1}
\]

and `d` responds into each of `r,q`. Choose one of those two d-targets and
omit one of the three cycle responses. Reverse the other two cycle cores,
give the chosen d-core to `d`, and give singleton charity to the omitted
cycle source.

Every branch has exactly four support edges:

\[
 2\text{ cycle edges}+1\text{ d edge}+1\text{ charity edge}. \tag{2}
\]

All goods are conserved and packet cardinalities are unrestricted. The two
selected cycle sources and `d` are strictly paid by desired cores. Only the
omitted paid-cycle source can be unpaid.

For two of the six branches, the cycle core physically sharing the d-target
is precisely the omitted response, so no shared-target disjointness premise
is needed. The other four branches use the ordinary disjoint-or-capture gate.

## Exact endpoint separator

If omitted source `h` supplies packets of h-value `L_h`, its final margin is

\[
 m_h=\Delta_h-L_h+v_h(p).                         \tag{3}
\]

Failure is exactly

\[
 L_h>\Delta_h+v_h(p).                             \tag{4}
\]

Thus the three-cycle form is reduced to six named scalar/overlap choices.
At saturation, an unsafe enlarged target yields a new response or support
record. The remaining proof must show that all six instances of (4), plus
the four relevant overlap-capture inequalities, cannot hold simultaneously
without PI, rank/support growth, or response replacement.

## Verification and boundary

[`audit_three_cycle_six_branch_charity_completion.py`](../tracks/parkability/audit_three_cycle_six_branch_charity_completion.py)
constructs all six branches, checks exact support conservation and edge
counts, and verifies payment and capture identities in QF-LRA.

It does not eliminate simultaneous failure of all six endpoint/observer
budgets and therefore does not finish the universal theorem.

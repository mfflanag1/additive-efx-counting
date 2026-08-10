# BCFF composition audit for the length-three escape theorem

**Date:** 2026-08-09

**Conclusion:** every hypothesis of the cap-free reservoir-order theorem is
derived inside the length-three branch of the BCFF exactly-two-
nonsingleton reduction

| Required premise | Derivation in the BCFF state | Hidden assumption? |
|---|---|---|
| One charity good `f` and partial EFX base | The contradiction state selected through BCFF Lemma 2.4 | No |
| Global lexicographic maximality | Choose a maximum under the fixed BCFF domination order | No transfer between orders |
| PI-free champion graph | BCFF Lemma 3.5 turns every PI cycle into a Pareto-improving EFX allocation | No |
| Two genuine edges entering the large bundles | Every vertex has an incoming `f`-champion; a selected simple cycle has at least two genuine edges and no genuine edge enters a singleton | No exact-graph assumption |
| Length-three normal form `p -f-> r -f-> q -> p` | Relabel the consecutive-genuine length-three selected cycle | No chordlessness assumption |
| External edge `a -> s` | A globally maximal singleton must be envied, or its owner absorbs `f` EFX | All three sources `a in {p,r,q}` retained |
| Nonempty `T_r,B_r,T_q,B_q` | Empty top contradicts charity dominance; empty bottom forces a self-`f`-champion via BCFF Observation 2.10 | No genericity assumption |
| Common safety of `D_p,D_r` | They are the desired sets of the two selected champions | By definition |
| `p,q` do not envy `X_r` | Either envy edge closes a basic PI cycle through `r -f-> q` and `q -> p` | No exclusion of unrelated edges |
| Positive/nondegenerate values | Standard respecting perturbation in BCFF Lemma A.1 | Removed again at the end |

## Order and source completeness

For each of the three external sources, the 24 priority orders partition
into twelve with `q` before `r` and twelve with `r` before `q`.

- The first half uses `D_p` and `W=X_q+B_r` at threshold `tau_r(D_p)`.
- The second half uses `D_r` and `U=X_r+B_q` at threshold `tau_q(D_r)`.

The low branch of the second orientation has only `r`- and `s`-sources.
For a desired `A subseteq X_r+B_q`, put \(H=A\cap B_q\) and
\(S=X_r\setminus A\). If `H` is empty, a `p`- or `q`-source contradicts
the no-envy row above. If `H` is nonempty, the `(H|S)` edge into `r`
closes a PI cycle with `r -f-> q`; that selected edge releases
`H subseteq B_q`. This covers extra champion edges rather than assuming
they are absent.

The 24 aggregate source/orientation implications are independently checked
in
[`length_three_reservoir_order_packet_audit.json`](length_three_reservoir_order_packet_audit.json).
The order partition is regression-tested in
[`test_length_three_capfree_order_coverage.py`](../tracks/parkability/test_length_three_capfree_order_coverage.py).

## Exact claim boundary

This audit establishes that the reservoir-order theorem plugs into the
BCFF **length-three branch** without additional premises. It does not use
or prove the length-two, adjacent-large, or alternating branches, and it
does not address BCFF states with three or four nonsingleton bundles.

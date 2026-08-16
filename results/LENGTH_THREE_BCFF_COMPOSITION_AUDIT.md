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
| Positive/nondegenerate values | Nondegeneracy from the BCFF Lemma A.1 respecting witness; positivity from A.1's nondegeneracy **plus the paper's standing monotonicity**. The witness A.1 guarantees is *cancelable*, not necessarily additive; the additive respecting nondegenerate perturbation actually run here is folklore (Chaudhury et al.), not A.1 | Only the final EFX allocation is carried back to the original profile — see the A.1 note in the inventory below |

*BCFF-audit repair 2026-08-16.*  The BCFF-sourced rows above are marked
"No" in the sense that they introduce no *hidden* assumption; they are
nonetheless external imports, and the newer sibling audits mark them
**EXTERNAL-TRUSTED**.  The inventory added below brings this table into that
format.

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

## EXTERNAL-TRUSTED inventory

*BCFF-audit repair 2026-08-16* — added to match
[`ALTERNATING_BCFF_COMPOSITION_AUDIT.md`](ALTERNATING_BCFF_COMPOSITION_AUDIT.md)
and
[`ADJACENT_BCFF_COMPOSITION_AUDIT.md`](ADJACENT_BCFF_COMPOSITION_AUDIT.md).
Not reproduced in this repository; checked against the arXiv e-print by
[`BCFF_IMPORT_AUDIT_20260816.md`](BCFF_IMPORT_AUDIT_20260816.md), which found
the surface faithful.  A human referee check is still wanted.

**Citation pin.**  All numbering here follows the **arXiv full build** of
[arXiv:2102.10654](https://arxiv.org/abs/2102.10654) (`\fulltrue`); v1
(2021-02-21) and v2 (2021-02-28) have identical Section 2 and Section 3
environment sequences, so the pin is "arXiv full version, v1 = v2".  The
AAAI-22 short build drops Definition 2.2, Example 2.5 and Definition 2.7 and
renumbers Section 2: under it "Lemma 2.4" is a Definition, "Definitions
2.6--2.7" are Observations, and **Observation 2.10 does not exist**.  Every
Section-2 citation below is coherent only under the full arXiv build.

| BCFF statement | Used for | Where |
|---|---|---|
| Lemma 2.4 | Existence/selection of the one-charity partial EFX contradiction state | Row "One charity good `f` and partial EFX base" |
| Definitions 2.6--2.7 | Champion, desired set, common safety.  Caveat: the primitive "most envious of `S`" lives in unnumbered prose (its definition environment is commented out in both builds), so this is the best available citation, not complete provenance | Row "Common safety of `D_p,D_r`" |
| **Observation 2.8** ("Every agent `i` has a champion with respect to `g`") | Every allocated bundle has an incoming `f`-champion | Row "Two genuine edges entering the large bundles", which asserts it with "Hidden assumption? No" (*added 2026-08-16*; it is not derivable from any other listed item) |
| Observation 2.10 | Empty bottom forces a self-`f`-champion | Row "Nonempty `T_r,B_r,T_q,B_q`" |
| Definitions 3.1, 3.2 and 3.4 (3.3 is an Example) and Lemma 3.5 | PI cycles yield Pareto-improving EFX allocations | Row "PI-free champion graph" and the low-branch PI routing |
| Lemma A.1 | A nondegenerate **cancelable** respecting witness `v'`, plus the one-directional transfer `EFX(v') => EFX(v)` — see the note below | Row "Positive/nondegenerate values" |

**What Lemma A.1 does and does not supply.**

1. **Not additivity.**  A.1 produces a *cancelable* respecting witness, not
   necessarily an additive one.  Additive respecting nondegenerate
   perturbations exist, but that is folklore (Chaudhury et al.), **not** BCFF
   Lemma A.1.
2. **Not positivity.**  A.1 says nothing about positivity.  The strict
   positivity used here is A.1's nondegeneracy together with the paper's
   standing monotonicity assumption; cite it as "A.1 + standing
   monotonicity", never as A.1 alone.
3. **Not a round trip.**  The transfer is one-directional and carries only
   the final EFX allocation back to the original profile.  It does **not**
   carry lexicographic maximality, the one-charity normal form, or the
   champion graph — all of which are defined *inside* the perturbed profile,
   which is exactly why the argument is legitimate.  The correct in-corpus
   statement of this is `ONE_LARGE_CHAMPION_CLOSURE_REDUCTION.md`, lines
   276--281; that file is on `codex/efx-breakthrough-next-20260802`, see gap
   G5.

Related wording to fix outside this audit: the "Nonnegative and tie wrapper"
of
[`LENGTH_THREE_GLOBAL_LEX_TARGET.md`](LENGTH_THREE_GLOBAL_LEX_TARGET.md)
(lines 2848--2850) still describes A.1 as supplying a *nondegenerate additive*
profile.  That proof body was deliberately left untouched in this repair
round; the flag is recorded here instead.

**Not used by the length-three branch:** BCFF Theorem 3.16 and Definition
3.9.  Only the length-two case theorem invokes them.

## Exact claim boundary

This audit establishes that the reservoir-order theorem plugs into the
BCFF **length-three branch** without additional premises. It does not use
or prove the length-two, adjacent-large, or alternating branches, and it
does not address BCFF states with three or four nonsingleton bundles.

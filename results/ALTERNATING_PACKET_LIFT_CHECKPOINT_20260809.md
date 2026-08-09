# Alternating packet-lift checkpoint

**Date:** 2026-08-09
**Status:** active cap-free conversion; no general alternating theorem yet

> **Update.**  The later anchored-or-any-desired lift for `(p,s,q,r)` and
> `(s,p,r,q)` is exactly refuted in an eight-good split cell; see
> [`ALTERNATING_PSQR_EXTENSION_GATE.md`](ALTERNATING_PSQR_EXTENSION_GATE.md).
> This does not refute the broader alternating escape, because both profiles
> retain many unrestricted EFX improvements.

**Encoding correction:** the original eleven-good split-packet search sorted
the two goods in every packet independently in every valuation row.  A global
relabeling justifies sorting one reference row, not all four; the original
UNSAT searches therefore covered only a within-packet comonotone subcell.
The implementation now sorts only `p`'s row.  SAT profiles and the analytic
root-flip lemma remain valid.  No old split-packet UNSAT status is used as a
broader theorem without a fresh replay under the corrected encoding.

## New durable result

The
[`easy-priority escape lemma`](ALTERNATING_EASY_PRIORITY_ESCAPE_LEMMA.md)
analytically closes 16 of the 24 priority-role orders for arbitrary bundle
sizes. It needs only the two ordinary envy edges and the fact that `p,s`
own singleton bundles. The construction discards the large packets and
gives every agent at most one good, making EFX automatic.

The live alternating gate was initially reduced to eight orders beginning
with a singleton owner whose good cannot be transferred to its incoming
envier.  The cap-free
[`root-flip lemma`](ALTERNATING_ROOT_FLIP_LEMMA.md) now closes two more,
`(p,q,r,s)` and `(s,r,q,p)`, leaving six.

## Exact atomic result

The seven-good `2+2+1+1` atom closes all eight hard orders as well. The
largest deletion-minimal rival menu has five allocations. This is frozen in
[`alternating_global_lex_atomic_core_audit.json`](alternating_global_lex_atomic_core_audit.json).

## Whole-packet relaxation

Each top/bottom packet was summarized by its total value and its maximum
value after deleting one internal good. This exactly checks EFX for
reallocations that keep all four packets intact. A shared-cardinality
constraint makes every abstract packet either a singleton in all valuation
rows or a realizable two-good packet in all rows.

For hard order `(p,s,r,q)`, the whole-packet relaxation has a globally
lex-maximal SAT model. Expanding each packet into two goods exposes extra
basic champion chords and self-champions. Therefore it is not a valid
alternating obstruction and does not refute the escape lemma. It proves
that totals plus maximum-deletion remainders do not encode enough of the
champion topology.

## Exact split-packet search

The next rung uses 11 actual goods: two goods in each of
\(T_r,B_r,T_q,B_q\), plus `x,y,f`. It enforces:

- strict base EFX and charity dominance;
- the exact ordinary envy graph;
- the selected alternating desired blocks;
- absence of every basic champion chord over all target subsets;
- absence of all four compatible generalized families over every internal
  incoming subset and target release;
- global lexicographic maximality against symbolically discovered actual
  EFX allocations.

For order `(p,s,r,q)`, every completed original master model had a concrete
EFX lexicographic escape. Z3 first returned `unknown` with 524 blockers.
cvc5 then solved that same master SAT, and an independent exact audit found
64 further EFX lexicographic dominators of its model. The durable pool now
contains 588 rivals. With all 588 blockers, Z3 returned `unknown` at 120
seconds and cvc5 returned `unknown (TIMEOUT)` at 300 seconds. This is a
comonotone-subcell search trace, not an UNSAT result or a complete corrected
cell.

Artifacts:

- [`alternating_split_packet_0213_pool.json`](alternating_split_packet_0213_pool.json)
- [`alternating_split_packet_0213_session1.json`](alternating_split_packet_0213_session1.json)
- [`alternating_split_packet_0213_cvc5_524_model_audit.json`](alternating_split_packet_0213_cvc5_524_model_audit.json)
- [`run_alternating_split_packet_cegar.py`](../tracks/parkability/run_alternating_split_packet_cegar.py)

## Threshold-target correction

The proposed two-slot threshold Hall target is exactly false.  A frozen
strictly positive and subset-nondegenerate profile satisfies the complete
alternating structural cell but has no qualifying block among all 63
nonempty residual subsets.  The exact boundary and replay data are in
[`threshold_two_slot_refutation_audit.json`](threshold_two_slot_refutation_audit.json).
This refutes only the one-whole-block construction, not the alternating
escape.  The same profile has many lexicographically improving EFX rivals
that repartition goods among three agents.

## Next actions

1. Lift the three-rival atomic core for `(p,q,s,r)`.  The root-flip lemma
   already supplies two of its branches; the missing branch augments or
   reroutes a bottom packet to improve `q` before `s,r`.
2. Apply half-turn symmetry to `(s,r,p,q)`.
3. Then treat the two four-rival symmetry pairs rooted at priority prefix
   `(p,s)` / `(s,p)`.
4. Use exact split-packet solving only to falsify each proposed cap-free
   menu before attempting its proof.  Do not resume blind growth of the
   588-rival global master.

The preserved-root three-agent target was itself too strong: exact atomic
countermodels refute it in six hard orders.  The repaired
[`anchored-or-promoted target`](ALTERNATING_ANCHORED_OR_PROMOTED_TARGET.md)
keeps both necessary branches.  For `(p,q,r,s)`, its eleven-good decision
collapsed from 576 learned rivals to a deletion-minimal two-rival core and
then to the cap-free root-flip proof.

The breakthrough boundary is unchanged: even a complete 11-good exclusion
is only a lemma-discovery rung. The required result is a proof for arbitrary
packet sizes.

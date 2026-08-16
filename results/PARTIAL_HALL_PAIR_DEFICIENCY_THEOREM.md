# Pair-deficiency theorem for the canonical radius-one cell

## Exact statement

Fix four agents, nine goods, the partial allocation

\[
X=(\{6,7\},\{1,2,3\},\{0,4\},\{5\}),\qquad f=8,
\]

and strictly positive additive valuations. Suppose $X$ is EFX and
$v_i(X_i)\ge v_i(f)$ for every agent. Consider the 91 bundle partitions
obtained by assigning $f$ and moving at most one previously allocated good
between bundle labels.

If every one of these partitions has no EFX perfect matching, then at least
one partition has two agents whose combined EFX-acceptability neighborhood
has size one.

Equivalently, an eligible radius-one Hall obstruction in this fixed cell
cannot have all its minimal deficient sets of sizes three and four.

## Certification

The exact QF_LRA decision artifact is
[`partial_hall_pair_deficiency_gate.json`](partial_hall_pair_deficiency_gate.json),
with frozen formula
[`partial_hall_pair_deficiency_gate.smt2`](partial_hall_pair_deficiency_gate.smt2).
Z3 returns `unsat`; after syntax-only normalization, cvc5 1.3.4 independently
returns `unsat` in 18.7 seconds.

The encoding uses:

1. row normalization and strict positivity;
2. the base EFX and floater-dominance inequalities;
3. exact EFX-acceptability edges for each candidate partition;
4. the 52 possible Hall witnesses of sizes two, three, and four; and
5. the negation of every size-two witness.

The reduction from failed perfect matchings to Hall witnesses is independently
checked by
[`partial_hall_witness_encoding_audit.json`](partial_hall_witness_encoding_audit.json).
The omission of singleton deficient sets follows from the cap-free
[maximum-bundle neighbor lemma](PARTIAL_HALL_NONEMPTY_NEIGHBOR_LEMMA.md).

A bounded deletion pass reduced the tracked proof from 74 to 36 high-level
constraints: four row-nonnegativity assumptions, nine base-eligibility walls,
six blocked-partition assertions, and seventeen assertions excluding a pair
defect. Only 20 of the 91 candidate partitions remain. The compact replay is
[`partial_hall_pair_deficiency_compact_core.smt2`](partial_hall_pair_deficiency_compact_core.smt2)
(202 KiB, SHA-256
`e82f1380af9c09e974517bf5ff51ca4cc6c0fb05723861ff45a0b8d575d3ec6f`).
Z3 and cvc5 both return `unsat` on this core. The bounded core is not claimed
deletion-irreducible: 34 attempted deletions reached their five-second limit.

## Claim boundary and next conversion

This is a structural theorem for one fixed bundle shape and good count. It
does not prove the radius-five potential lemma or complete EFX existence.
The high-leverage next lemma is now narrower: show that a two-agent,
one-neighbor obstruction across a suitable one-good move yields either an EFX
completion or an eligible improving exchange. The compact 20-partition core
identifies the current proof support; further human compression remains.

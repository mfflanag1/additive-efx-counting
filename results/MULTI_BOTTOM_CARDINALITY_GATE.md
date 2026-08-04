# Multi-bottom cardinality gate

## Result

The bad-source champion branch of a four-agent one-charity Hall obstruction
cannot be reduced to singleton discard by a local argument. Exact
positive-additive \((4,8)\) witnesses establish all of the following:

1. a full identity/unique-defect obstruction can have a bad-to-host champion
   whose every desired bundle retains the floater and discards at least two
   host goods;
2. such a state need not have an eligible positive-\(\Theta\) one-good owner
   transfer;
3. redistributing the obstructing host's bundle and inserting the floater
   into that same host need not complete EFX;
4. even redistributing that bundle, choosing any insertion host, and allowing
   all 24 bundle matchings need not complete EFX; and
5. adding every eligible one-good-per-owner Pareto exchange cycle and every
   improving owner-minimum/charity swap still leaves an exact locally
   saturated obstruction.

Items 4 and 5 were produced by exact QF_LRA formulas in the canonical
\(3+2+1+1\) partial-bundle cell and replayed literally using positive integer
valuation matrices. The first formula obstructs all 175 host-redistribution
partitions. The second additionally saturates 87 owner-Pareto exchange-cycle
candidates and seven owner-minimum/charity swaps.

## What the residual actually requires

The nearest strict \((\Theta,U)\) escape from the final saturated witness has
label distance three. It exchanges the two-good bundle of one owner with a
singleton bundle of another owner. The two-owner transfer component moves
three goods, raises \(\Theta\) by

\[
\frac{28099}{195720},
\]

improves one affected owner by \(2897\), and reduces the other affected
owner's utility by \(1141\). It leaves one residual insertion defect, rather
than absorbing immediately. Hence neither Pareto maximality nor bounded
host-only completion controls this gate. A valid proof must permit a
non-Pareto positive-threshold component and then propagate its remaining Hall
wall.

Across the seven exact adverse profiles currently frozen, every nearest
strict extremal escape is one connected transfer component. Their minimum
label distances range from one to three. This is recorded in
[`unique_defect_adverse_branch_escape_audit.json`](unique_defect_adverse_branch_escape_audit.json).

## Live breakthrough target

At the selected \((\Theta,U,\Lambda)\) state, start with the positive
component exposed by the bad-source or host-interference wall. Repeatedly add
the owner component named by a crossing EFX/Hall wall. Prove that, for four
owners, either:

1. the union becomes eligible while retaining positive normalized threshold
   gain;
2. it becomes threshold-neutral and strictly improves the owner-utility or
   Hall tie-break; or
3. a repeated owner yields a strict signed inequality cycle whose normalized
   sum is impossible.

The exact local-menu counterexample shows why the union must allow unequal
bundle cardinalities and utility loss at intermediate owners. The existing
transfer-component hybrid wall lemma supplies component additivity and the
strict crossing polarity; the missing statement is preservation of enough
positive gain during dependency closure.

## Targeted global-extremum CEGAR

The canonical \(3+2+1+1\) selected-desired cell is now encoded directly as
an exact QF_LRA CEGAR problem. Each refinement cut says that a concrete
one-charity state cannot be both eligible and strictly better than the adverse
base under \((\Theta,U)\). Unlike the retired local menus, these cuts allow
arbitrary goods, owners, and connected-component shapes.

Five bounded iterations installed 40 exact extremal cuts. The improvement
counts in the successive concrete models were \(169,63,219,108,107\). At
pool size 40, a fresh two-minute master solve returned `unknown` with reason
`timeout`; it did not establish satisfiability or unsatisfiability. The pool,
result, and 2.8 MB SMT2 formula are resumable:

- [`unique_defect_extremal_cell_cegar_pool.json`](unique_defect_extremal_cell_cegar_pool.json)
- [`unique_defect_extremal_cell_cegar_result.json`](unique_defect_extremal_cell_cegar_result.json)
- [`unique_defect_extremal_cell_cegar.smt2`](unique_defect_extremal_cell_cegar.smt2)

`CELL_UNSAT` would prove this canonical cell only; a satisfiable model with no
better eligible state would be an exact counterexample to the proposed
\((\Theta,U)\) selector. The current timeout is neither result.

## Claim boundary

The counterexamples, their exhaustive local menus, and their nearest escape
components are exactly replayed. The dependency-closure alternative above is
not proved. Consequently this gate does not resolve four-agent or general
additive EFX.

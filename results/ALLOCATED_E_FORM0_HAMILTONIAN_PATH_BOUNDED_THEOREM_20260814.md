# Allocated-E form-0 Hamiltonian-path bounded theorem

**Date:** 2026-08-14

**Status:** exact twelve-atom theorem with a 70-cut replay core; the cap-free
path-partition lift remains open

## Exact bounded cell

Use the twelve-atom allocated-E form-0 master from
`run_allocated_e_capture_rank_three_cegar.py`.  It includes positive additive
valuations, normalized base EFX, the selected rank-three cores, the exact
form-0 response relation, ordinary PI exclusion, generalized self-PI
exclusion, anchored and pairwise closed-core exclusions, and the exact
rank-three full-capture premises declared by that master.

The physical current support partition is

\[
\begin{array}{c|ccccc}
\text{supplier}&r&q&d&s&\text{charity}\\ \hline
\text{goods}&a_0,a_1,h&j,k,q_0&m,g_q,g_r&\ell,e&p.
\end{array}
\]

Consider only complete allocations whose nontrivial supplier-recipient
pairs are exactly

\[
 \text{charity}\to r\to q\to d\to s.             \tag{1}
\]

Thus every ordinary supplier's three goods either remain or move one step
along (1), with at least one good using each owner edge; `s` retains its two
goods and `p` goes to `r`.  There are exactly

\[
                         7^3=343                 \tag{2}
\]

such allocations.

## Bounded theorem

Every valuation profile in the exact form-0 master that is free of a closed
generalized PI core family admits a complete EFX allocation among the 343
Hamiltonian-path allocations (1).

Equivalently, negating EFX for all 343 allocations makes the form-0 master
UNSAT after generalized PI families are excluded.

## Exact decision and replay

The primary CEGAR run produced 15 successive SAT profiles.  Every one
contained at least one exact closed generalized-PI core family.  Batched
separation added 21,934 distinct PI cuts; the sixteenth master check was
UNSAT.  Total decision time was 933.8 seconds under Z3 4.15.3.

The tracked replay reduced those 21,934 cuts to a 70-cut UNSAT core.  A fresh
master containing only the 343 path negations and those 70 PI cuts is again
UNSAT.  A separate solver-independent combinatorial audit checks each of the
70 witnesses for distinct cycle owners, pairwise-disjoint cores, base-owner
closure, exact incoming/released packets, and release coverage.

Artifacts:

- `allocated_e_form0_hamiltonian_path_cegar.json.gz`: compressed complete
  primary trace (decompress before passing it to the core extractor);
- `allocated_e_form0_hamiltonian_path_unsat_core.json`: 70-cut replay core;
- `allocated_e_form0_hamiltonian_path_core_audit.json`: independent witness
  semantics audit.

## Analytic signal

The surviving topology is not an arbitrary solver artifact.  It is the
reverse of the Hamiltonian owner-to-charity path in the universal full-owner
extraction theorem.  In this bounded cell, every supplier needs only one
forward recipient, and each owner's packet choice is a binary stay-or-forward
cut.  The cap-free lift is therefore the following explicit problem:

> Along `charity -> r -> q -> d -> s`, choose one forward packet from each of
> the three current supplier bundles so that the resulting complete
> allocation is EFX, or show that failure of every such triple of cuts yields
> a closed generalized-PI family or the exact full-owner base-margin
> separator.

This is substantially narrower than arbitrary packet graphs and aligns with
the critical-anchor uncrossing packet: its stay/forward choice is the first
cut on (1).

## Claim boundary

This is an exhaustive bounded-atom theorem, not a cap-free theorem.  The
primary decision and 70-cut replay share the same algebraic master encoding;
only the path generator and PI-witness semantics have independent
combinatorial audits.  The result does not prove the analogous form-2 cell,
the universal Hamiltonian path-partition lemma, the complete fixed-U target,
four-agent EFX, or general additive EFX.

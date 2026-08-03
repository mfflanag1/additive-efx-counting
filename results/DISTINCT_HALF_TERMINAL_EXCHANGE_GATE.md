# Terminal-to-Eight-Orbit Exchange Gate

**Status:** dual-verified cap-5 theorem; unrestricted implication refuted  
**Scope:** four agents, nine goods, positive-integer values at most 5, strict
common favorite, universal owner-threshold failure, four distinct
half-favorite representatives; no Hall-cell condition is assumed  
**Not claimed:** a cap-free exchange lemma, a new value-cap existence range,
or a proof of general additive EFX

## Basic idea

The eight-orbit family contains the 780 balanced favorite-pair partitions
whose triple does not consist of three representative goods. The 60 states
outside that family form two terminal partition orbits:

\[
R=((0,1),(2,3,4),(5,6),(7,8)),\qquad
U=((0,5),(1,2,3),(4,6),(7,8)).
\]

Here (0) is the common favorite, (1,\ldots,4) are the four distinct
half-favorite representatives, and (5,\ldots,8) are the unrepresented
goods. A single edge in the state graph exchanges one good between two
bundles. From either terminal state, exactly 138 eight-orbit states lie
within two edges. The question is whether EFX at a terminal state forces
EFX at one of those nearby states.

The one-edge version is false: exact positive-real profiles in both terminal
orbits retain terminal EFX but have no one-swap repair. The radius-two
version survives through cap 5 but is false by cap 20.

## Bounded theorem

> Let every value be an integer in \(\{1,\ldots,5\}\), and impose the
> residual-branch assumptions above. If either terminal partition supports
> a complete EFX allocation, then an eight-orbit favorite-pair partition at
> graph distance at most two from that terminal partition also supports a
> complete EFX allocation.

The statement is nonvacuous. The audit contains a cap-5 profile satisfying
the entire branch and the first canonical (R)-matching cell. Literal
replay finds 96 radius-two eight-orbit repairs and 592 favorite-pair repairs
in total.

## Exhaustive symmetry reduction

Simultaneously permuting agents and their four representative goods, while
independently permuting the four unrepresented goods, leaves the normalized
branch invariant. The stabilizer of (R) has size 48 and divides its 24
possible agent-to-bundle matchings into orbits of sizes 6, 6, and 12. The
stabilizer of (U) has size 12 and divides the matchings into four orbits of
size 6. Thus seven canonical terminal/matching cells cover every possible
terminal EFX matching.

For each cell, two separately constructed finite-domain formulas are
infeasible:

| terminal | matching orbit | CP-SAT | Z3 QF_LIA | radius-two targets |
|---|---:|---|---|---:|
| R | 0 | infeasible | unsat | 138 |
| R | 1 | infeasible | unsat | 138 |
| R | 2 | infeasible | unsat | 138 |
| U | 0 | infeasible | unsat | 138 |
| U | 1 | infeasible | unsat | 138 |
| U | 2 | infeasible | unsat | 138 |
| U | 3 | infeasible | unsat | 138 |

The CP-SAT encoding and the Z3 integer-linear encoding independently impose
the structural branch, fix the stated terminal EFX matching, and obstruct
all 138 target partitions. No full-Hall-cell condition appears in either
formula. The deterministic audit
recomputes the symmetry census and target hashes, checks all fourteen solver
records, and hash-pins every exported protobuf and SMT formula.

## What this changes

This result does not extend the already certified finite existence ladder:
the stronger full-cell dichotomy is already closed through cap 6. Its value
is proof mining. It says that cap-5 terminal EFX itself forces a local route
back into the 780-state eight-orbit family within two moves, whether or not
a full Hall cell exists. That is evidence for a concise exchange argument,
but finite caps are not monotone evidence toward arbitrary real valuations.

## Sharp failure beyond cap 5

The unrestricted radius-two implication is false, even together with the
full no-Hall-cell premise. A cap-20 profile in the first canonical
(R)-matching cell is

\[
\begin{pmatrix}
17&13&15&15&15&16&1&16&11\\
17&3&14&15&15&9&7&11&9\\
20&1&16&16&15&17&15&6&19\\
19&5&13&13&14&5&18&16&14
\end{pmatrix}.
\]

Independent literal replay verifies:

- the strict common-favorite, universal-threshold, and distinct-
  representative branch assumptions;
- EFX of the canonical terminal matching;
- no full favorite-triple Hall cell among all 28 low pairs;
- zero EFX repairs among all 138 eight-orbit states at distance at most two;
- 336 favorite-pair EFX partitions elsewhere, of which 290 lie in the
  eight-orbit family; and
- 1,439 labeled complete EFX allocations.

The nearest eight-orbit repairs are at distance three: 152 occur there and
another 138 at distance four. Thus the profile refutes only the local
selector, not the global eight-orbit-or-full-Hall dichotomy and certainly not
EFX existence.

The optimizer did not assume the absence of every Hall cell; it explicitly
forbade only cell (\{1,2\}). The decoded integer profile was then replayed
over all 28 cells and found to have none. Its obstruction objective reached
the exact bound 138, so the zero target count is a solver-certified optimum,
while the semantic audit is independent of that objective encoding.

The earlier partner split remains useful postmortem evidence. Exact
no-full-cell profiles separately block all 66 same-partner states or all 72
changed-partner states. The new profile blocks their union. Local exchange
within two moves is therefore retired; the live target returns to the global
780-state eight-orbit selector or a direct full-cell argument.

## Trust boundary

The bounded theorem is computer-assisted and has no independently checkable UNSAT
proof object. Confidence comes from agreement of two different encodings,
complete symmetry coverage, semantic reconstruction of the target family,
and hash-pinned formula artifacts. `UNKNOWN` results are excluded from the
theorem. The finite cap is essential. The cap-20 refutation is a positive
integer model and is therefore easier to check than an UNSAT claim.

The primary artifact is the
[terminal-exchange audit](efx49_distinct_half_terminal_exchange_gate_audit.json).
Its executable replay is
[`audit_distinct_half_terminal_exchange_gate.py`](../tracks/parkability/audit_distinct_half_terminal_exchange_gate.py).
The decisive profile and optimization record are
[the cap-20 radius-two refutation](efx49_distinct_half_terminal_radius2_R_m0_cpsat_cap20_forbid_cell12_optimize_session1.json).
The broader orbit context is in the
[six/eight-orbit gate](DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md).

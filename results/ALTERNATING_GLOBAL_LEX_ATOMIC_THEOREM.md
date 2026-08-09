# Alternating global-lex atomic exclusion

**Status:** exact QF_LRA theorem for the strict seven-good atom; analytic
packet lift open
**Scope:** positive additive valuations, bundle shape `2+2+1+1`, one charity
good, exact alternating chordless champion topology
**Boundary:** excludes global lexicographic maximality for all 24 priority
orders; it does not yet cover multi-good top or bottom packets

## Statement

Order the agents as `p,r,s,q` and the goods as

\[
t_r,b_r,t_q,b_q,x,y,f.
\]

Consider the partial allocation

\[
X_p=\{x\},\quad X_r=\{t_r,b_r\},\quad
X_s=\{y\},\quad X_q=\{t_q,b_q\},
\]

with `f` unallocated. Assume:

1. the allocation is strictly EFX and every owner strictly prefers her
   bundle to `f`;
2. the exact ordinary envy graph is `r -> s`, `q -> p`;
3. the exact basic `f`-champion graph is the alternating cycle

   \[
   p\xrightarrow f r\longrightarrow s
   \xrightarrow f q\longrightarrow p,
   \]

   where `p` has desired set \(\{t_r,f\}\), `r` has \(\{y\}\), `s`
   has \(\{t_q,f\}\), and `q` has \(\{x\}\); alternate proper desired
   sets on the same edge are allowed, while full-target desired sets are
   excluded by nonabsorption;
4. all four compatible generalized cross-bottom source families are absent,
   using the exact most-envious-subset definition for every incoming subset
   and every target release.

> **Atomic exclusion theorem.** For every permutation of the four agents,
> this partial allocation is not globally lexicographically maximal among
> all partial EFX allocations.

The quantifier over rivals includes all \(5^7=78{,}125\) assignments of a
good to one of four agents or to charity. Rivals may leave any number of
goods unallocated.

## Exact certificate

For every priority order, a finite menu of rival allocations is frozen in
[`alternating_global_lex_atomic_core_audit.json`](alternating_global_lex_atomic_core_audit.json).
The structural premises together with the assertion that every allocation
in the menu either fails EFX or fails to lexicographically improve are
QF_LRA-UNSAT.

- all 24 priority orders are UNSAT;
- 16 orders require only one rival allocation;
- the remaining eight require between two and five rivals;
- the maximum core size is five;
- every core is deletion-minimal with respect to its rival menu.

The replay uses exact rational arithmetic in Z3 5.0.0. The frozen audit does
not depend on a CEGAR search trace: it rebuilds the structural formula,
checks every core, removes each rival in turn, and verifies that every
single deletion restores satisfiability.

## The one-rival mechanism

The simplest certificate is already analytic. For priority order
`p,r,s,q`, use

\[
X'_p=\{x\},\quad X'_r=\{y\},\quad
X'_s=\{f\},\quad X'_q=\{t_q\},
\]

and discard the other goods. Every allocated bundle is a singleton, so the
allocation is automatically EFX. Agent `p` is unchanged and `r` strictly
improves because `r -> s` is an envy edge. The same singleton-collapse
idea proves the other 15 one-rival orders after relabelling or choosing the
first applicable envy edge.

The eight hard orders begin with a singleton owner whose singleton cannot
be transferred without lowering the first priority coordinate. Their
two-to-five-allocation cores use the absent champion families to force at
least one safe pooling or splitting alternative. Converting those eight
cores into a concise inequality case lemma is the next analytic task.

## Why this advances the breakthrough route

The earlier profile `V*` showed that Pareto maximality cannot close the
alternating cycle. This theorem proves that the obstruction disappears once
true global lexicographic maximality is imposed in the smallest exact atom.
Thus the priority-sensitive route survives its first complete adversarial
test and produces small proof menus rather than a countermodel.

The remaining issue is not the number of priority orders. It is the packet
lift. In an arbitrary instance, \(T_r,B_r,T_q,B_q\) may contain several
goods. Treating each as one atomic good is insufficient because EFX must be
checked after deleting each individual good from a new bundle. The desired
cap-free lemma must replace atomic singleton safety with BCFF
most-envious-set safety or select terminal subpackets whose every
one-good deletion is controlled.

> **Packet-lift target.** Each rival menu used in the eight hard atomic
> orders can be replaced by a bounded menu of reallocations of desired
> blocks and incoming-clean subpackets, one of which is EFX and
> lexicographically improves the base.

Proving that target closes the separated length-four alternating residue.
The same packet-safety invariant is then the natural candidate for the
length-three and adjacent length-four residues.

## Reproduction

```bash
PYTHONPATH=/private/tmp/efx-python-deps \
python3 tracks/parkability/audit_alternating_global_lex_atomic_core.py \
  --output /private/tmp/alternating-global-lex-atomic.json
cmp results/alternating_global_lex_atomic_core_audit.json \
  /private/tmp/alternating-global-lex-atomic.json
```

Search implementation:
[`run_alternating_global_lex_cegar.py`](../tracks/parkability/run_alternating_global_lex_cegar.py).

Frozen-core audit:
[`audit_alternating_global_lex_atomic_core.py`](../tracks/parkability/audit_alternating_global_lex_atomic_core.py).

## Primary source

Berger, Cohen, Feldman, and Fiat,
[*Almost Full EFX Exists for Four Agents (and Beyond)*](https://arxiv.org/abs/2102.10654),
Definitions 2.6--2.7 and 3.1--3.4 and Lemma 3.5.

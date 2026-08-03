# Owner-minimum Hall-pair extraction theorem

**Status:** exact machine-assisted theorem, independently replayed by Z3 and
cvc5; arbitrary positive-additive values and arbitrary bundle sizes.

## Theorem

Let

\[
X=(X_0,X_1,X_2,X_3;f)
\]

be an EFX allocation of all but one good under strictly positive additive
valuations, with

\[
v_i(X_i)\ge v_i(f)\qquad(i=0,1,2,3).
\]

For each bundle $X_s$, select a good

\[
g_s\in\arg\min_{g\in X_s}v_s(g).
\]

Consider the following complete bundle partitions, followed in every case by
an arbitrary matching of agents to bundle labels:

1. insert $f$ into any host bundle $X_h$; or
2. insert $f$ into any host $X_h$, move $g_s$ from any source $X_s$ to any
   destination $X_d$ with $d\ne s$, and retain the candidate only if all four
   bundles are nonempty.

Then either some candidate has an EFX perfect matching, or some candidate's
EFX-acceptability graph contains two agents whose combined neighborhood is a
single bundle.

For a nonsingleton source, host and source vary independently. For a singleton
source, nonemptiness permits evacuation only when $h=s$, leaving $\{f\}$ at
the source label. Ties in the choice of $g_s$ are allowed. There is no bound on
the number of goods or on valuation magnitudes.

## Exact reduction

For every observer $i$ and nonsingleton bundle $X_j$, decompose

\[
X_j=\{g_j\}\mathbin{\dot\cup}R_j
\]

and retain only

\[
a_{ij}=v_i(g_j),\qquad r_{ij}=v_i(R_j),\qquad
q_{ij}=\min_{g\in R_j}v_i(g),\qquad F_i=v_i(f).
\]

For a singleton bundle, retain only $a_{ij}$. These statistics determine every
EFX threshold exactly, because for any nonempty additive bundle $B$,

\[
\max_{g\in B}v_i(B\setminus\{g\})
=v_i(B)-\min_{g\in B}v_i(g).
\]

The QF_LRA encoding imposes positivity, row normalization, base EFX, floater
nonenvy, and $a_{ss}\le q_{ss}$ for every nonsingleton source. It then defines
every acceptability edge for all selected candidates. A counterexample would
make all 24 agent--bundle permutations fail in every graph while also
excluding every two-agent/one-neighbor Hall witness.

The encoding relaxes remainder realizability: it requires only
$r_{ij}\ge q_{ij}>0$, although an actual multi-good remainder obeys additional
constraints. Therefore UNSAT of this larger domain is sound for every actual
additive instance.

## Certification

The generator is
[`decide_partial_hall_host_minimum_extraction.py`](../tracks/parkability/decide_partial_hall_host_minimum_extraction.py).
Sixteen frozen formulas cover every subset of singleton bundle labels. Z3
returns `unsat` on all sixteen. Simultaneous permutation of agent and bundle
labels makes patterns with the same number of singletons isomorphic, so the
five masks $0,1,3,7,15$ represent all possible singleton counts. cvc5 1.3.4
independently returns `unsat` on all five representative formulas.

The main nonsingleton formula is
[`partial_hall_owner_minimum_ties_extraction_aggregate.smt2`](partial_hall_owner_minimum_ties_extraction_aggregate.smt2),
SHA-256
`6796327819fc8690886b256ac5819067d01c319579082da12d7481b4c472d008`.
The all-singleton representative is
[`partial_hall_owner_minimum_ties_singletons_15.smt2`](partial_hall_owner_minimum_ties_singletons_15.smt2),
SHA-256
`47b9752619003e69a6a0fc391b7d66362055f89e8e3be93881ac47b61f3011ab`.
The complete hash and status ledger is
[`partial_hall_owner_minimum_extraction_theorem_audit.json`](partial_hall_owner_minimum_extraction_theorem_audit.json).

## Sharpness of the move family

Two exact positive instances rule out tempting simplifications:

- direct insertion alone fails on a $4\times9$ instance; and
- direct insertion plus only host-source owner-minimum replacements fails on
  a $4\times13$ instance with unique owner minima.

In the second instance, inserting $f$ into bundle 1 while transferring owner
0's minimum good from source 0 to destination 2 yields an EFX matching. Thus
the theorem's independent host and source roles are not merely an encoding
convenience.

## Breakthrough boundary

This closes the arbitrary-bundle **pair-extraction gate** for four agents. It
does not close the **pair-trap conversion gate**. When the theorem returns a
two-agent/one-neighbor obstruction rather than a completion, one must still
construct another eligible one-floater EFX allocation with strictly larger
selector value. Proving that exchange contradiction is the remaining central
step toward converting the known almost-complete four-agent result into
complete EFX.

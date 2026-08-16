# Exact Refutation of Partial-EFX Maximum-Nash Direct Completion

**Status:** exact, exhaustive counterexample to the selector  
**Domain:** four agents, nine goods, strictly positive additive valuations  
**Claim boundary:** the profile has 83 complete EFX allocations; it is not an
additive-EFX counterexample

## Refuted statement

Let \(\mathcal E(V)\) be the partial EFX allocations \((X,f)\) with exactly
one unallocated good (f) and

\[
v_i(X_i)\ge v_i(f)\qquad\text{for every agent }i.
\]

The proposed completion rule selected a state maximizing

\[
\prod_{i=0}^3 v_i(X_i)
\]

and conjectured that some maximizer permits direct insertion of its floater.
The following profile has a unique maximizer and that maximizer is blocked at
all four hosts.

## Counterexample

The valuation matrix is

\[
\begin{pmatrix}
1&2&299&368&1&32&6209&3578&261\\
16385&4098&24580&5682&9&34848&29710&772&2187\\
10241&53&18436&7065&20564&1625&29760&77&5874\\
371&541&1249&144&17887&20512&19152&150&2969
\end{pmatrix}.
\]

Good 8 is unallocated, and the owner vector for goods (0,ldots,8) is

\[
(2,1,1,1,2,3,0,0,-).
\]

Thus the bundles are

\[
X_0=\{6,7\},\quad X_1=\{1,2,3\},\quad
X_2=\{0,4\},\quad X_3=\{5\},
\]

with own utilities

\[
(9787,34360,30805,20512).
\]

Their product is

\[
212486804036051200.
\]

Exact enumeration finds 290 eligible one-floater states and 285 distinct
utility vectors. The displayed state is the unique product maximizer. The
second-largest product is (205476190869242880), leaving the strict gap

\[
7010613166808320.
\]

## Why insertion fails

The state is not near the boundary of eligibility: its minimum EFX slack is
1,045, and its four floater-nonenvy slacks are

\[
(9526,32173,24931,17543).
\]

Nevertheless every host has a strict insertion witness:

| host | observing agent | removed good | insertion slack |
|---:|---:|---:|---:|
| 0 | 2 | 7 | -4829 |
| 0 | 3 | 7 | -1609 |
| 1 | 2 | 1 | -570 |
| 2 | 3 | 0 | -344 |
| 3 | 1 | 8 | -488 |

One negative witness is enough to block a host. All four hosts are therefore
blocked.

## Exhaustive verification

The permanent audit examines all

\[
9\cdot4^8=589824
\]

one-floater assignments with a literal implementation of EFX, floater
nonenvy, insertion, and integer utility products. It then independently
reconstructs the same 290 eligible states using the repository's core
iterator and a separate vectorized subset-sum implementation. All three
implementations identify the same unique blocked maximum.

A second exhaustive census examines all

\[
4^9=262144
\]

complete assignments. Independent literal and core iterators both find 83
complete EFX allocations. Their canonical allocation-list hash is
`763cdc3b10f19f8de13cb3adf735c179171ce67eafa9219e332ad0bfc9f3dff0`.

The audit also stores all 290 eligible partial states in decreasing product
order, so the maximality claim can be inspected directly rather than inferred
from a solver verdict.

## Meaning for the general problem

This closes the maximum-Nash **direct-insertion** proof route. It does not
close the general additive-EFX problem: the same profile explicitly has
complete EFX allocations. The cap-free safe-exchange, bundle-cycle, source-
host, and substitution-path lemmas remain true, but they cannot collectively
force insertion at a maximum-Nash partial state.

The counterexample is still structurally informative. Its maximum has nearby
lower-product eligible states that permit insertion, so a completion proof
may need a controlled descent or a selector based on reachability rather than
static welfare maximality. A one-transfer repair was tested next and is also
empirically refuted, but that secondary endpoint is not part of this promoted
claim until it receives the same independent audit.

## Reproduction

The fixed input is
[partial_nash_completion_refutation_profile.json](partial_nash_completion_refutation_profile.json),
the exhaustive output is
[partial_nash_completion_refutation_audit.json](partial_nash_completion_refutation_audit.json),
and the deterministic discovery provenance is
[partial_nash_gap_anneal_seed211.json](partial_nash_gap_anneal_seed211.json).

Frozen SHA-256 values:

- profile: `928029ffcd6d4171e1733999fe6f6f0abf0d0d5ab6ffe1c7c0a3702215155981`;
- exhaustive audit: `20f8804f932534242b196db6acbbca6d3c0434563ef3cdfed910e2babd412df6`;
- discovery provenance: `c70870d3965621d5b60044ebd3adf7a2058af9a6c2446b414ef5790c6a867211`;
- refreshed corpus scan: `56cb55c30be0fbc8f97f4c4ce034499993eb38e063b470a13d4f56e5a0471e38`.

Rebuild and byte-compare the audit with:

```bash
make verify-partial-nash-completion-refutation
```

# Cap-free Hall-pair extraction target

**Status (2026-08-02): superseded by a proved theorem.** The arbitrary-bundle
statement is established in the stronger bounded owner-minimum form; see the
[owner-minimum Hall-pair extraction theorem](PARTIAL_HALL_OWNER_MINIMUM_EXTRACTION_THEOREM.md).
This file retains the evidence and proof agenda that led to the theorem.

## Conjectured lemma

Let

\[
X=(X_0,X_1,X_2,X_3;f)
\]

be an EFX allocation of all but one good under strictly positive additive
valuations, and suppose

\[
v_i(X_i)\geq v_i(f)\qquad(i=0,1,2,3).
\]

Form every complete partition obtained by:

1. inserting $f$ into one bundle;
2. optionally transferring one previously allocated good between two bundle
   labels; and
3. allowing an arbitrary matching of agents to the resulting four bundles.

Then either one of these partitions admits an EFX perfect matching, or at
least one of their EFX-acceptability graphs contains two agents whose combined
neighborhood consists of a single bundle.

The statement quantifies over arbitrary finite bundles. It has no bound on the
number or magnitude of goods.

### Proved bounded move family

For each source bundle $X_s$, select a good minimizing its value to its current
owner $s$. The theorem proves that direct insertion and transfers of these
owner-minimum goods suffice. This reduces the move family to at most four
distinguished old goods, independently of the total number of goods. Ties and
singleton bundles are included.

## Why this is the correct breakthrough gate

Hall's theorem says that every failed matching has a deficient set. The
cap-free maximum-bundle-neighbor lemma excludes deficient singletons. With
four agents, the remaining obstruction types are therefore

\[
2\to1,\qquad 3\to1,\qquad 3\to2,\qquad
4\to1,\qquad 4\to2,\qquad 4\to3.
\]

The now-proved theorem says that varying the floater host and one selected transfer always
converts one of the larger obstruction types into $2\to1$. That is exactly the
pair trap needed by the cap-free star-localization and exchange lemmas. A
proof would clear pair-extraction gate 1 in the
[breakthrough alignment audit](EFX_BREAKTHROUGH_ALIGNMENT_AUDIT_20260802.md).
It would not by itself prove complete EFX: the pair trap must still be
converted into a strictly better eligible partial allocation.

The cap-free
[diagonal-or-host lemma](PARTIAL_HALL_DIAGONAL_OR_HOST_LEMMA.md) supplies the
first universal restriction: after direct insertion into host $h$, every row
contains its diagonal or column $h$. If a diagonal disappears, column $h$
must appear. The direct counterexample shows that this restriction alone still
permits $3\to2$ and $4\to3$ defects, so the owner-minimum transfer must supply
the next monotonicity step.

## Exact finite evidence

The search program is
[`search_partial_hall_pair_extraction.py`](../tracks/parkability/search_partial_hall_pair_extraction.py).
For each valuation profile it exhaustively enumerates every eligible
one-floater EFX state, every floater host, every optional old-good transfer,
the exact EFX-acceptability graph, and every perfect matching and Hall witness.

The main audit
[`partial_hall_pair_extraction_corpus134.json`](partial_hall_pair_extraction_corpus134.json)
has SHA-256
`68767f28f9c180119b5060decc338a1b3674e59e92301018d6e43a4fa23583c2`.
Across 134 positive-additive $4\times9$ profiles it checks:

- 128,131 eligible one-floater EFX states;
- 11,988,061 generated radius-one candidate partitions;
- 127,457 states with an EFX completion in that move family; and
- 674 states with no such completion, every one of which has a $2\to1$ Hall
  witness.

No counterexample was found. All five possible positive bundle-size shapes
for eight allocated goods occur:

| Sorted bundle sizes | Eligible states |
|---|---:|
| $1,1,1,5$ | 28 |
| $1,1,2,4$ | 3,390 |
| $1,1,3,3$ | 2,315 |
| $1,2,2,3$ | 80,177 |
| $2,2,2,2$ | 42,221 |

Separate exact audits of the tight witnesses at $(4,7)$, $(4,8)$, $(4,9)$,
and $(4,10)$ also find no counterexample. The tight $(4,8)$ witness supplies
12 genuinely blocked states, all with the required pair witness; the other
three tight profiles complete within radius one.

These are exhaustive statements about the named integer profiles, not a proof
over real valuations.

The same audit separately tests the owner-minimum move family on every state:
127,081 states complete and the remaining 1,050 expose a pair trap. No
owner-minimum-family counterexample occurs. The pair count is larger than 674
because 376 states complete using some unrestricted transfer but do not
complete using the smaller selected family; they still expose a pair there.

## Exact limit of direct insertion

Direct insertion alone is insufficient. The positive integer profile
[`partial_hall_direct_pair_extraction_counterexample.json`](partial_hall_direct_pair_extraction_counterexample.json)
has four two-good base bundles and one floater. Its exact independent
[audit](partial_hall_direct_pair_extraction_counterexample_audit.json) verifies
that the base is eligible EFX, all four direct-insertion graphs lack a perfect
matching, and none contains two agents whose sole neighbor is the host. Moving
owner 0's least-valued good from bundle 0 to bundle 1 while inserting the
floater into bundle 0 yields an EFX matching. Thus one-good transfer is not an
encoding convenience; it is logically necessary for this proof route. The
counterexample does not refute the owner-minimum or unrestricted radius-one
conjectures, and it is not an EFX counterexample.

## Proof agenda

Assume no candidate partition has a perfect matching and no candidate graph
has a $2\to1$ defect. For each floater host, choose an inclusion-minimal Hall
witness. It has size three or four. The intended proof has three reductions:

1. use the host owner's guaranteed edge to the enlarged host bundle and the
   maximum-bundle-neighbor lemma to restrict which bundle labels can occur in
   a minimal $3\to2$ or $4\to3$ witness;
2. transfer an owner-minimum good from a bundle in the witness neighborhood
   to a bundle outside it, and apply star localization to show that unchanged
   acceptance edges can disappear only through the enlarged host; and
3. compare two host choices. If the large deficient set persists, its
   neighborhoods must cross in a way that either yields a perfect matching or
   leaves two rows with the same sole neighbor.

The next formal artifact should encode these reductions at the level of
abstract acceptance graphs plus the monotonicity constraints induced by one
transfer. A pure enumeration of graph families is useful only if every graph
transition is justified by an additive/EFX monotonicity lemma.

## Short replay

```bash
python tracks/parkability/search_partial_hall_pair_extraction.py \
  results/partial_hall_two_positive_reroute_corpus_search.json \
  --output /tmp/partial_hall_pair_extraction_replay.json
```

The output must report `claim_survives_tested_profiles: true`, 134 profiles,
128,131 tested states, 674 blocked states with pair extraction, and zero
counterexamples.

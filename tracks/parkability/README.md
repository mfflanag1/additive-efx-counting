# Parkable deletion at \((4,8)\)

- **Status:** exhaustive exact-LRA closure candidate; not yet an
  independently proof-checked theorem.
- **Target:** decide whether every positive additive \(4\times8\) matrix has a
  deletion, an EFX\(_0\) allocation of the remaining seven goods, and a host
  to which the deleted good can be parked while preserving EFX\(_0\).
- **Equivalence:** the Threshold-Cycle Normal Form Theorem proves that, for
  positive valuations with \(m\ge n\), a complete EFX\(_0\) allocation
  exists if and only if a parkable-deletion triple exists. A zero-triple
  matrix would therefore be a genuine additive-EFX counterexample. A bounded
  master UNSAT is still only solver evidence until its terminal formula and
  proof are independently certified.

The current eight-cell exact-LRA closure candidate, its analytic coverage
argument, formula hashes, and proof-checking boundary are recorded in
[`results/EFX_4X8_LRA_CERTIFICATE.md`](../../results/EFX_4X8_LRA_CERTIFICATE.md).

This directory is a fresh implementation. It does not import the historical
`park_hunt.py` or `cegar.py` masters. Those search complete EFX allocations
directly; the normal-form theorem now proves that their target property and
zero parkability are equivalent, although their other reductions and
certification boundaries still require separate auditing.

## Exact semantics

A triple is \(t=(f,a,h)\), where good \(f\) is absent from the base assignment
\(a\), and host \(h\) receives it. Write \(B_j\) for agent \(j\)'s base
bundle. The triple is valid exactly when the base is EFX\(_0\) and

\[
  v_k(B_k)\ge
  v_k(B_h)+v_k(f)-\min_{g\in B_h\cup\{f\}}v_k(g)
  \qquad(k\ne h).
\]

The exact evaluator scans all

\[
  8\cdot4^7=131{,}072
\]

labeled deletion assignments, retains every EFX\(_0\) base, and checks all
four hosts. Triple JSON uses `null` exactly at the deleted good:

```json
{
  "floater": 3,
  "base_owner": [1, 1, 0, null, 3, 2, 2, 2],
  "host": 0
}
```

Equivalently, a triple is a complete EFX\(_0\) allocation with one
owner-removable good. The exact owner-slack identity and its deletion-rigidity
reformulation are proved in
[`results/REVERSE_PARKING_LEMMA.md`](../../results/REVERSE_PARKING_LEMMA.md).
That note also proves the Threshold-Cycle Normal Form Theorem: rotate bundles
along cycles of strictly improving maximum EFX thresholds until some owner's
own bundle is threshold-maximal, at which point its least good is removable.
`core.threshold_cycle_normal_form` implements and checks the construction.

`core.py` evaluates subset thresholds. `independent.py` separately expands
every removed-good inequality and enumerates the same triples in both
base-first and completion-first order.

## Commands

Use the repository's Python 3.10 environment after installing
`requirements.txt`.

```sh
make verify-parkability PYTHON=python3.10

python3.10 tracks/parkability/evaluate.py results/tb4.json \
  --output /tmp/tb4-parkability.json \
  --details /tmp/tb4-efx-bases.jsonl
```

The basin-1 control currently has 167 EFX deletion bases, 6 parkable triples,
and 4 distinct complete EFX\(_0\) allocations. The extra two triples are
alternative deletion certificates for an already counted completion. When
`--details` is used, the landscape JSON records the JSONL path, record count,
and SHA-256 digest.

A one-point-box CEGAR smoke test is:

```sh
python3.10 tracks/parkability/run_cegar.py \
  --K 1 \
  --pool /tmp/parkability-k1-pool.json \
  --trace /tmp/parkability-k1-trace.jsonl \
  --result /tmp/parkability-k1-result.json
```

`run_lra_cegar.py` searches the entire positive-real domain with exact
rational linear arithmetic. It excludes matrices with a universal-minimum
good using the proved reduction: delete that good, take a seven-good EFX
allocation, eliminate envy cycles without losing EFX, and park the good at a
source. Thus an LRA `UNSAT_CANDIDATE`, combined with that reduction, would
cover all positive valuations rather than a bounded integer box. The emitted
SMT-LIB formula still requires independent proof checking before promotion.

```sh
python3.10 tracks/parkability/run_lra_cegar.py \
  --add 128 \
  --include-one-nonsingleton \
  --pool /tmp/parkability-lra-pool.json \
  --trace /tmp/parkability-lra-trace.jsonl \
  --result /tmp/parkability-lra-result.json \
  --smt2 /tmp/parkability-lra.smt2
```

`run_efx_lra_cegar.py` uses the normal-form equivalence to negate complete
allocations directly. Its full positive \((4,8)\) universe has 40,824 onto
allocations rather than 524,288 labeled parking triples. Historical raw
allocation lists can be imported with repeatable `--allocation-pool` options;
parking pools can be converted with `--triple-pool`.

```sh
python3.10 tracks/parkability/run_efx_lra_cegar.py \
  --pool /tmp/complete-efx-pool.json \
  --allocation-pool results/z3_pool.json \
  --symmetry double_lex \
  --exclude-peelable \
  --require-pairwise-distinct-rows \
  --trace /tmp/complete-efx-trace.jsonl \
  --result /tmp/complete-efx-result.json \
  --smt2 /tmp/complete-efx.smt2
```

The two optional residual cuts compose with proved safe cases: a peelable
singleton reduces to the three-agent theorem, and repeated normalized rows
reduce to the theorem for at most three valuation types. Omitting both flags
leaves only the always-enabled universal-minimum reduction. A solver-reported
UNSAT remains a candidate until the exported formula receives independent
proof checking.

At \(m=2n\), `--require-favorite-hall-deficiency` adds another proved case
split. If the agents can be matched to distinct favorite goods, assigning
each matched favorite with one arbitrary leftover good is an EFX allocation:
an observer's own pair is worth at least its favorite, and every target
pair's one-good-removed threshold is worth at most that favorite.

Because EFX nonexistence is an open condition, a counterexample may be
perturbed to have a unique favorite in every row. Up to relabeling, a
Hall-deficient unique-favorite profile has one of four multiplicity patterns.
The partition runner can search a canonical strict cell, for example:

```sh
python3.10 tracks/parkability/run_partition_lra.py \
  --favorite-pattern 0,0,1,2 \
  --favorite-pattern-stabilizer \
  --result /tmp/partition-211-result.json \
  --smt2 /tmp/partition-211.smt2
```

`anneal_efx.py` is a heuristic companion that minimizes the exact complete-EFX
count. It uses the vectorized evaluator but performs definition-literal audits
before reporting any zero candidate.

`anneal_efx_family.py` minimizes a specified union of complete-EFX shapes
and singleton-good branches. It preserves an optional strict
common-favorite cell and independently replays any zero-family endpoint.
The common-favorite \(4\times9\) campaign uses shape code `3222` together
with singleton good 0.

`run_partition_lra.py` expresses the same terminal question through the 1,701
unlabeled nonempty bundle partitions. For each partition it builds the
agent--bundle EFX-feasibility graph and requires that graph to have no perfect
matching. Both the direct 24-matching-clause encoding and an independent
Hall-witness encoding are available.

```sh
python3.10 tracks/parkability/run_partition_lra.py \
  --symmetry double_lex \
  --exclude-peelable \
  --require-pairwise-distinct-rows \
  --obstruction-encoding hall_selectors \
  --result /tmp/partition-lra-result.json \
  --smt2 /tmp/partition-lra.smt2
```

The target \(K=4\) campaign is launched through `durable_campaign.py`, which
fixes the sound configuration, holds a whole-session file lock, requires a
clean source commit, and archives hash-chained before/after pool snapshots:

```sh
python3.10 tracks/parkability/durable_campaign.py run \
  --root /absolute/external/path/parkability/k4-none \
  --python /absolute/path/to/python3.10

python3.10 tracks/parkability/durable_campaign.py status \
  --root /absolute/external/path/parkability/k4-none
```

`run` also resumes an inconclusive or interrupted campaign by allocating a
new immutable session directory. It refuses concurrent access, configuration
drift, archive corruption, source drift, and resumption after a terminal
status. SIGINT and SIGTERM are forwarded to the child process group while the
supervisor retains the lock and records the outcome. The child inherits the
lock descriptor, so a supervisor hard-kill cannot permit concurrent pool
access; after the child exits, the next `run` seals the incomplete ledger
before resuming.

The raw runner remains useful for smoke tests. Its default master is
symmetry-free. `--symmetry double_lex` is available as a separate,
non-strict row/column permutation symmetry mode; the selected mode is bound
into the pool schema and result.

## Bounded-integer partition and rank-gap workbench

`run_integer_partition_cegar.py` uses exact integer variables and
bidirectionally reified comparison literals. Repeat `--partition-shape` or
`--partition-singleton-good` to restrict the allocation universe to a union
of shapes and singleton branches. It can also restrict each row to distinct
item values. `--second-favorite-pattern` with
`--ranking-prefix-stabilizer` gives a sound top-two ranking cell.
`--require-singleton-threshold-failure-good` directly encodes universal
failure of the selected singleton owner's threshold over every residual
partition, without adding resident Hall constraints. For example, the
common-favorite balanced-or-singleton cell is:

```sh
python3.10 tracks/parkability/run_integer_partition_cegar.py \
  --n 4 --m 9 --upper 12 \
  --pool /tmp/rank-gap-pool.json \
  --seed-pool results/efx49_borda_shape3222_favorites4_pool.json \
  --result /tmp/rank-gap-result.json \
  --proto /tmp/rank-gap-model.pb \
  --require-distinct-item-values \
  --favorite-pattern 0,0,0,0 \
  --favorite-pattern-stabilizer \
  --partition-shape 3,2,2,2 \
  --partition-singleton-good 0
```

The Borda shape theorem closes all five favorite orbits at cap 9 with both
matching-clause and Hall-selector encodings. The same shape is
matching-clause closed through cap 11. At cap 12 it fails: the frozen
common-favorite profile has no \(3+2+2+2\) EFX allocation but has 838
complete EFX allocations of singleton-containing shapes. Reproduce both the
literal allocation census and the independent partition-graph census with:

```sh
python3.10 tracks/parkability/audit_rank_gap_boundary.py \
  --output /tmp/rank-gap-boundary.json
```

See
[`../../results/RANK_GAP_EFX_4X9.md`](../../results/RANK_GAP_EFX_4X9.md).
The ten-cell dual-encoding manifest is
[`../../results/efx49_rankgap12_dual_encoding_audit.json`](../../results/efx49_rankgap12_dual_encoding_audit.json).

At cap 13, repeat `--partition-singleton-good` to admit any designated
favorite singleton. The \(3+1\) and \(2+2\) cells require goods 0 and 1;
the common-favorite cell requires good 0. All five matching cells and all
five Hall-selector cells close; the hard common-favorite orbit uses a
hash-identical sparse pool of 446 partitions in both encodings.
See
[`../../results/efx49_rankgap13_theorem_audit.json`](../../results/efx49_rankgap13_theorem_audit.json).

The unrestricted-real boundary, the 18-allocation heuristic endpoint, and
the falsification of the narrower balanced-or-\(6+1+1+1\) cover are audited
by:

```sh
python3.10 tracks/parkability/audit_common_favorite_boundaries.py \
  --results-dir results \
  --output /tmp/common-favorite-boundaries.json
```

## Adaptive-priority completion workbench

`run_adaptive_priority_cegar.py` derives the unique lexicographic maximum
for every agent order from a \(4\times9\) seed, fixes those candidate
identities, requires every distinct candidate to be EFX, floater-nonenvying,
and blocked, and learns every eligible lexicographically nonlower rival.
`UNSAT_FIXED_CANDIDATE_CELL` closes only that candidate cell.

```sh
python3.10 tracks/parkability/run_adaptive_priority_cegar.py \
  --seed results/lexmax_all_orders_seed93_exact_replay.json \
  --pool /tmp/adaptive-pool.json \
  --result /tmp/adaptive-result.json \
  --smt2 /tmp/adaptive.smt2
```

`shrink_adaptive_priority_core.py` extracts a deletion-minimal joint core of
candidate states and rival clauses. The first compact cell exposed the
forced singleton-swap handoff. Its weak-EFX symbolic reconstruction is
audited by:

```sh
python3.10 tracks/parkability/audit_forced_singleton_swap_lemma.py
```

The corresponding human proof is
[`../../results/FORCED_SINGLETON_SWAP_LEMMA.md`](../../results/FORCED_SINGLETON_SWAP_LEMMA.md).

## CEGAR soundness

For a pooled triple, the master requires at least one strict reversal of:

1. a removed-good EFX inequality in its seven-good base; or
2. a removed-good EFX inequality directed at the enlarged host bundle.

Over integer values, each reversal is `lhs + 1 <= rhs`. One-way reified
Booleans plus one `BoolOr` are exact after projection: a satisfying model
contains an actual violation, and every invalid triple has a violation that
can witness the disjunction. There are no distinct-row, valuation-type,
global-minimum, dominant-good, shape, normalization, or heuristic cuts.

Terminal statuses are deliberately conservative:

| Status | Meaning |
|---|---|
| `ZERO_PARKABLE_TRIPLES` | A matrix was exhaustively confirmed by both independent enumeration orders. By the Threshold-Cycle Normal Form Theorem, this is a genuine complete-EFX counterexample; the independently recorded complete count must be zero. |
| `UNSAT_CANDIDATE` | CP-SAT reports that the bounded master is infeasible. This is not promoted to a theorem without an independent terminal encoding and checked proof. |
| `MASTER_UNKNOWN` | The master timed out or returned another inconclusive status. |
| `ITERATION_LIMIT` | A valid resumable pool was written, but the requested iteration cap was reached. |

The independent terminal encoder, cold replay, pinned proof generation,
DRAT verification, and final `CERTIFIED_UNSAT` promotion are specified in
[TERMINAL_CERTIFICATION.md](TERMINAL_CERTIFICATION.md).

Run products belong under `results/parkability/` during discovery. Only
terminal, independently archived evidence should be promoted under `repro/`.

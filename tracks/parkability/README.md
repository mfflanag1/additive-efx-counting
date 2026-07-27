# Parkable deletion at \((4,8)\)

- **Status:** research workbench; no bounded \(K=4\) result is claimed.
- **Target:** decide whether every positive additive \(4\times8\) matrix has a
  deletion, an EFX\(_0\) allocation of the remaining seven goods, and a host
  to which the deleted good can be parked while preserving EFX\(_0\).
- **Claim boundary:** zero such triples refutes this completion route but does
  not by itself decide additive EFX existence; the full EFX count is therefore
  recorded separately. A bounded master UNSAT is solver evidence until its
  terminal formula and proof are independently certified.

This directory is a fresh implementation. It does not import the historical
`park_hunt.py` or `cegar.py` masters: those search for complete EFX
counterexamples and use reductions that have not been proved for the stronger
zero-parkability property.

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
| `ZERO_PARKABLE_TRIPLES` | A matrix was exhaustively confirmed by both independent enumeration orders. This exactly refutes the route for that matrix; its separately recorded complete EFX count determines whether EFX still exists there. |
| `UNSAT_CANDIDATE` | CP-SAT reports that the bounded master is infeasible. This is not promoted to a theorem without an independent terminal encoding and checked proof. |
| `MASTER_UNKNOWN` | The master timed out or returned another inconclusive status. |
| `ITERATION_LIMIT` | A valid resumable pool was written, but the requested iteration cap was reached. |

The independent terminal encoder, cold replay, pinned proof generation,
DRAT verification, and final `CERTIFIED_UNSAT` promotion are specified in
[TERMINAL_CERTIFICATION.md](TERMINAL_CERTIFICATION.md).

Run products belong under `results/parkability/` during discovery. Only
terminal, independently archived evidence should be promoted under `repro/`.

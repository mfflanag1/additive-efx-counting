# Terminal certification

The discovery master is CP-SAT. The terminal master is a separate
symmetry-free CNF implementation that imports none of the CP-SAT master,
landscape evaluator, or CEGAR runner. A CP-SAT `UNSAT_CANDIDATE` is not a
theorem; promotion requires the complete chain below.

## Independent formula

For a pooled triple \(t=(f,a,h)\), let \(B_j\) be agent \(j\)'s base bundle
and \(E_h=B_h\cup\{f\}\). The triple is invalid exactly when at least one
strict reversal holds:

\[
v_i(B_i)<v_i(B_j\setminus\{r\})
\quad(i\ne j,\ r\in B_j),
\]

or

\[
v_i(B_i)<v_i(E_h\setminus\{r\})
\quad(i\ne h,\ r\in E_h).
\]

The first family says the base is not EFX\(_0\); the second says parking at
the selected host fails. Thus, for pool \(T\), the terminal formula is

\[
F_T=\operatorname{Domain}(V)\land
\bigwedge_{t\in T}\operatorname{Invalid}_t(V).
\]

`UNSAT(F_T)` means every matrix in the bounded value box validates at least
one pooled triple. The discovery trace and the method used to find the pool
are not premises of this implication.

For \(v_i(g)\in\{1,\ldots,K\}\), the encoder uses monotone threshold bits
\(x_{i,g,q}=[v_i(g)\ge q]\), \(q=2,\ldots,K\). If an observer's own bundle
has size \(a\) and the target remainder has size \(b\), the strict reversal
is equivalent to

\[
\sum_{g\in R,q}x_{i,g,q}+
\sum_{g\in B_i,q}\neg x_{i,g,q}
\ge Ka-b+1.
\]

Each possible reversal receives a one-way guarded sequential counter. The
outer disjunction selects one real reversal. Fresh counter auxiliaries make
this encoding exact after projection.

## Promotion chain

| Stage | Required status | Meaning |
|---|---|---|
| CP-SAT CEGAR | `UNSAT_CANDIDATE` | Discovery solver could not find another matrix. |
| Independent CNF | `UNSAT_SOLVER_RESULT` | Separate threshold encoder and direct solver agree. |
| Cold DIMACS replay | `UNSAT_SOLVER_RESULT` | Frozen bytes solve UNSAT without rebuilding. |
| CaDiCaL | `UNSAT_PROOF_GENERATED` | Pinned solver emitted binary DRAT. |
| drat-trim | `VERIFIED_DRAT` | A pinned, hashed checker accepted the proof. |
| Finalizer | `CERTIFIED_UNSAT` | Pool, sources, CNF, proof, records, and tools form one hash-checked chain. |

The final status certifies only the bounded parkable-deletion statement. It
does not decide unrestricted additive EFX existence.

## Pipeline

The first certified run must use a pool whose schema records
`"symmetry": "none"`.

```sh
python3.10 tracks/parkability/terminal_cnf.py \
  --pool POOL.json \
  --export terminal.cnf \
  --result-out terminal-result.json \
  --solver cadical195 \
  --timeout-seconds 10800 \
  --expect unsat

python3.10 tracks/parkability/replay_terminal_cnf.py \
  --dimacs terminal.cnf \
  --expect-sha256 DIMACS_SHA256 \
  --result-out replay-result.json \
  --solver cadical195 \
  --timeout-seconds 10800 \
  --expect unsat
```

Proof generation is pinned to CaDiCaL 1.9.5 commit
`146207318796f094dcded87349a64f0c6927309e`:

```sh
python3.10 tracks/parkability/generate_terminal_drat.py \
  --dimacs terminal.cnf \
  --terminal-result terminal-result.json \
  --proof-out proof.binary.drat \
  --log-out cadical.log \
  --result-out proof-generation.json \
  --cadical /path/to/cadical \
  --cadical-source /path/to/cadical/source \
  --expect-cadical-sha256 CADICAL_EXECUTABLE_SHA256 \
  --expect UNSAT_PROOF_GENERATED
```

Proof checking is pinned to drat-trim commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The checker executes a private
byte-identical snapshot and is hashed before and after use:

```sh
python3.10 tracks/parkability/verify_terminal_drat.py \
  --dimacs terminal.cnf \
  --terminal-result terminal-result.json \
  --proof proof.binary.drat \
  --result-out proof-check.json \
  --checker /path/to/drat-trim \
  --expect-checker-sha256 DRAT_TRIM_EXECUTABLE_SHA256 \
  --binary
```

For a compressed proof, pass `proof.binary.drat.xz`; the verifier records
both compressed and uncompressed hashes. The finalizer accepts either form:

```sh
python3.10 tracks/parkability/certify_terminal.py \
  --pool POOL.json \
  --terminal-result terminal-result.json \
  --dimacs terminal.cnf \
  --replay-result replay-result.json \
  --proof-generation proof-generation.json \
  --proof proof.binary.drat \
  --proof-check proof-check.json \
  --certificate-out CERTIFICATE.json \
  --cadical /path/to/cadical \
  --cadical-source /path/to/cadical/source \
  --drat-trim /path/to/drat-trim \
  --drat-trim-source /path/to/drat-trim/source
```

The finalizer refuses uncommitted changes to any claim-bearing pipeline
source. It also rebuilds the DIMACS byte-for-byte from the pool, rebuilds
drat-trim byte-for-byte from the pinned C source and recorded compiler, and
runs the proof checker again itself. `CERTIFIED_UNSAT` therefore does not
depend on trusting the earlier proof-check JSON record.

## Calibration

The pipeline has been exercised on the symmetry-free \(K=2\), \(4\times8\)
terminal pool:

- 160 pooled triples;
- 4,646 CNF variables and 6,070 clauses;
- DIMACS SHA-256
  `fa7d72120474524f18bf2681c0cfbb7bd863ec01cbc1238d3b980f84f3f701ac`;
- 12,890-byte binary DRAT proof, SHA-256
  `b87866ecae02455b02c8b007275880d4019333d8e37a33da95756bed3f50776e`;
- drat-trim result: `VERIFIED`, with 13 of 511 lemmas in the core, 218
  resolution steps, and zero RAT lemmas in the core.

This is a calibration of the certification machinery, not the target
\(K=4\) result.

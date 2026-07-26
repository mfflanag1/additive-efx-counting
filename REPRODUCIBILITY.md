# Reproducibility

All commands below are run from the repository root. The audited environment
used Python 3.10.14. Pinned Python dependencies are:

- `numpy==2.2.6`
- `ortools==9.15.6755`
- `python-sat==1.9.dev7`
- `z3-solver==5.0.0.0`

Install them in an isolated environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Paper claims

Run the read-only paper verification target:

```sh
make verify-paper
```

This performs:

```sh
python3 repro/counting_witnesses/verify_all.py
python3 artifacts/generalized_parking/verify_certificates.py
python3 repro/countcegar_k4/test_sat_differential.py \
  --result-out /tmp/additive-efx-counting-verify/sat-differential.json
python3 repro/countcegar_k4/test_slot_boundary.py \
  --result-out /tmp/additive-efx-counting-verify/slot-boundary.json
python3 repro/countcegar_k4/verify_drat.py --hash-only
```

The first two commands exhaustively enumerate the relevant allocation spaces.
The two K4 regressions test the CNF identity, symmetry utilities, deterministic
export, and the fixed-instance three-slot boundary. `--hash-only` checks the
archived CNF/proof integrity but does not establish the logical validity of the
DRAT proof.

Full DRAT verification requires a locally built checker at the exact revision
recorded in the certificate:

```sh
python3 repro/countcegar_k4/verify_drat.py \
  --checker /absolute/path/to/drat-trim
```

The pinned checker is `drat-trim` commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The producing solver was CaDiCaL
1.9.5, tag `rel-1.9.5`, commit
`146207318796f094dcded87349a64f0c6927309e`.

Re-solving the frozen CNF is optional and can be expensive:

```sh
python3 repro/countcegar_k4/replay_sat.py \
  --dimacs results/countcegar_K4_sat.cnf \
  --expect-sha256 ccc2aa45a5710d967a166abf7bc56a2026c517f4157730872b99524027baa166 \
  --solver cadical195 \
  --timeout-seconds 10800 \
  --expect unsat \
  --result-out /tmp/additive-efx-counting-verify/sat-replay.json
```

The K4 trust boundary is the mathematical slot-soundness argument, the
auditable CNF translation, and the correctness of the proof checker. There is
no proof-assistant formalization.

## Audited work outside the paper

Run:

```sh
make verify-audit
```

This checks:

```sh
python3 repro/countcegar_real/test_countcegar_real.py
python3 repro/countcegar_real/validate_manifest.py
python3 artifacts/efx_chambers/verify_radii.py
python3 artifacts/efx_chambers/verify_radii_exact.py
python3 artifacts/multifloater_parking/verify_small.py
python3 supplement/test_build_release.py
```

The exact-real validator checks all 38 pinned files, reconstructs seven trace
branches, independently recounts every retained candidate, validates 80
refinements, and verifies the checkpoint lineage. Both terminal exact-real
masters are checkpoints: the last checked masters were SAT and their post-cut
exports were not checked. Nothing in this command promotes them to theorems.

The two chamber verifiers independently check all 11,860,961 labeled
allocations and the rational radius certificates. The multi-floater regression
exhausts its stated small parameter boxes.

## Paper build

With a TeX distribution containing `latexmk`:

```sh
make paper
```

The committed PDF is the review copy. `paper/main.tex` still contains an
author-metadata placeholder that must be resolved before external submission.

## Deterministic supplement

The paper supplement deliberately contains only the paper claims. Exact-real,
chamber, and multi-floater files are excluded.

Build from a clean commit, with both outputs outside the repository:

```sh
python3 supplement/build_release.py build \
  --archive /absolute/output/efx-paper-supplement.tar.xz \
  --manifest /absolute/output/efx-paper-supplement.manifest.json
```

Verify without extracting:

```sh
python3 supplement/build_release.py verify \
  --archive /absolute/output/efx-paper-supplement.tar.xz \
  --manifest /absolute/output/efx-paper-supplement.manifest.json
```

The default builder refuses modified, untracked, missing, or index-mismatched
selected files and binds one immutable byte snapshot to both the initial Git
index and the archive. `--allow-dirty` is for development tests only.

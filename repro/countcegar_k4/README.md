# K=4 counting-CEGAR reproducibility package

This directory reconstructs and independently checks the bounded statement

> Every additive `4 x 7` valuation matrix with entries in `{1,2,3,4}` has at
> least four EFX0 allocations.

It does not alter or silently complete the historical run artifacts.

## Historical-artifact audit

The committed result `results/countcegar_K4.json` reports an UNSAT master with
pool size 1,295 after iteration 260. The committed log reports the same terminal
line. However, `results/countpool_K4.json` is the most recent periodic
checkpoint, written after iteration 250: it has 1,250 entries, of which 1,134
are distinct. The historical script saved the pool only every ten successful
iterations and did not save it on UNSAT. The log did not record candidate
valuations or added allocations. Consequently, the exact 45 final entries of
the historical terminal master cannot be recovered from the retained
artifacts.

The source and artifacts first appear together in Git commit
`a9c88411593cefe464a0731cd15bc1d03ae97d31`. This is provenance for the
archived bundle, not proof that the run used byte-for-byte identical source:
the source file's filesystem modification time postdates the result, and the
run itself recorded neither a source hash nor a package version. The historical
command is inferred from the script's CLI:

```sh
python countcegar.py --K 4
```

`MANIFEST.json` records the archival hashes and the reconstructed terminal
master's hashes, versions, and exact checking commands.

## Reconstruction

Install the three pinned solver interfaces into an isolated environment, then run
from the repository root:

```sh
python -m pip install -r repro/countcegar_k4/requirements.txt
python repro/countcegar_k4/reconstruct.py
```

The reconstruction starts from the historical checkpoint, removes logically
redundant duplicate allocations, and resumes counting-CEGAR. It writes the pool
atomically after every successful master call and appends every candidate and
new cut to `results/countcegar_K4_reconstruction.jsonl`. A terminal UNSAT pool
is therefore complete even if the process is later interrupted. Six CP-SAT
workers match the historical script but are not guaranteed to choose identical
models; the reconstructed pool determines an alternative complete terminal
master for the same claim, not a recovery of the missing historical cuts.

The retained fresh run used
`python repro/countcegar_k4/reconstruct.py --workers 6 --random-seed 1 --add 16`.
It returned UNSAT on round 8 after 1,060.725 seconds. Its terminal pool contains
1,240 distinct allocations and has SHA-256
`af85029ca3ec3527e60bffc516d2ef5ec9bfc1e82fbaeeb3e521f8c1f3d38e28`.
`results/countcegar_K4_reconstruction_run.json` preserves that run record;
`results/countcegar_K4_reconstructed.json` records the subsequent check of the
frozen pool together with the exact solver-export hashes. That one-call export
replay returned UNSAT after 286.056 seconds.

On terminal UNSAT, the reconstruction also writes the exact reconstructed
`CpModelProto`, `CpSolverResponse`, and human-readable response statistics as
text protobuf/text files. These preserve the solver input and response; they
are not a formal UNSAT proof.

## Independent master check and SMT-LIB2 export

`check_z3.py` does not import the CP-SAT master builder, `countcegar.py`,
`cegar.py`, or the exhaustive slave. Its default checker uses finite-domain
one-hot variables and pseudo-Boolean inequalities rather than the integer
CP-SAT encoding. It also eliminates the three interchangeable slot vectors
using the equivalent condition that at most three distinct pooled allocations
may remain EFX0. The loader removes duplicate pool entries before imposing that
cardinality bound. The default formulation directly encodes in Z3:

- finite-domain one-hot valuation variables representing `[1,4]`;
- row and column DoubleLex symmetry representatives;
- the EFX0 predicate for every distinct pooled allocation; and
- the cardinality bound that at most three distinct pooled allocations
  remain EFX0.

With `--formulation slots`, the checker instead encodes three one-hot
allocation slots and, for each pooled allocation, the literal disjunction of a
strong-envy witness or equality to one slot.

Run it and export the exact checked formula as SMT-LIB2:

```sh
python repro/countcegar_k4/check_z3.py \
  --pool results/countpool_K4_complete.json \
  --timeout-ms 10800000 \
  --threads 4 \
  --expect unsat \
  --export results/countcegar_K4_complete.smt2 \
  --result-out results/countcegar_K4_z3.json
```

For an optional replay through the command-line executable:

```sh
z3 -T:10800 sat.threads=4 -smt2 results/countcegar_K4_complete.smt2
```

A completed solve would need to return `unsat` to corroborate the bounded
result. The retained Python run reached its three-hour cap and returned
`UNKNOWN` with reason `timeout`, so no Z3 verdict is used as evidence in the
paper. The command-line replay repeats the same Z3 encoding and is not a
separate manifest gate. The SMT-LIB2 file remains a standalone, inspectable Z3
interchange artifact; it does not rely on Python source when passed to the Z3
command-line executable. Use `--encoding lia` to export a standards-oriented
QF_LIA version instead of the faster pseudo-Boolean version. Use
`--formulation slots` to retain the literal slot vectors instead of the
equivalent cardinality formulation.

## Independent CNF literal-slot check

`check_sat.py` is a second independent literal-slot implementation. It imports
neither the CP-SAT nor Z3 builders. Each valuation is represented by monotone
threshold literals
`v = 1 + [v >= 2] + [v >= 3] + [v >= 4]`; row and column DoubleLex comparisons
are encoded exactly in CNF; and each of the three allocation slots has a
four-owner one-hot domain. For a removable good with an observer bundle of size
`a` and a target remainder of size `b`, strong envy is the guarded cardinality
constraint

```text
target threshold literals + complemented own threshold literals
    >= 4a - b + 1.
```

Those constraints use `python-sat`'s sequential-counter `CardEnc`. The pool
loader validates every owner strictly, preserves the first occurrence of each
allocation, and reports both the source-file and deduplicated-pool hashes.

Before running the complete pool, execute the differential regression:

```sh
python repro/countcegar_k4/test_sat_differential.py
```

It exhaustively checks the threshold strong-envy identity over all feasible
bundle-size/value multisets, checks every length-two lexicographic comparison,
checks strict pool deduplication and deterministic DIMACS output, and compares
fixed-master SAT/UNSAT results with the direct EFX0 definition and all four Z3
formulations (LIA/PB crossed with slots/cardinality).

Export and solve the complete CNF with the pinned CaDiCaL 1.9.5 binding:

```sh
python repro/countcegar_k4/check_sat.py \
  --pool results/countpool_K4_complete.json \
  --solver cadical195 \
  --timeout-seconds 10800 \
  --expect unsat \
  --export results/countcegar_K4_sat.cnf \
  --result-out results/countcegar_K4_sat.json
```

Replay the exported file without rebuilding the master:

```sh
python repro/countcegar_k4/replay_sat.py \
  --dimacs results/countcegar_K4_sat.cnf \
  --expect-sha256 ccc2aa45a5710d967a166abf7bc56a2026c517f4157730872b99524027baa166 \
  --solver cadical195 \
  --timeout-seconds 10800 \
  --expect unsat \
  --result-out results/countcegar_K4_sat_replay.json
```

The retained builder-fed run and cold replay both returned UNSAT. The formula
has 282,029 variables and 600,624 clauses, occupies 13,684,928 bytes, and has
SHA-256
`ccc2aa45a5710d967a166abf7bc56a2026c517f4157730872b99524027baa166`.
Their recorded solve times are 68.048 and 67.760 wall-clock seconds,
respectively, and their CaDiCaL counters agree exactly.

## Archived proof certificate

Official CaDiCaL 1.9.5 was also run directly on the frozen DIMACS with binary
DRAT tracing enabled. It returned UNSAT and wrote a 134,426,255-byte proof.
Official `drat-trim` independently verified the proof: its core contains
259,081 original clauses and 645,356 lemmas, checked by 28,212,699 resolution
steps, with zero RAT lemmas in the core.

The proof is archived as
`certificates/countcegar_K4_sat.cadical-1.9.5.binary.drat.xz`. Its compressed
size is 38,753,120 bytes and its SHA-256 is
`ddcad227664410e4e3552bd774ea369888dae4e56093a3016a4ce880eb549977`.
The uncompressed proof has SHA-256
`710c51bd36addd3d1ea73c14d902d2b1d9aba23cafcd4874ef1d21daf2779a5b`.
`certificates/DRAT_CERTIFICATE.json` records both tool commits, commands,
hashes, counters, timings, and archived logs.

The recorded tool revisions are:

- official CaDiCaL tag `rel-1.9.5`, commit
  `146207318796f094dcded87349a64f0c6927309e`;
- official `drat-trim`, commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

After building that `drat-trim` revision, verify the compressed certificate
from the repository root:

```sh
python repro/countcegar_k4/verify_drat.py \
  --checker /path/to/drat-trim
```

The wrapper verifies the CNF and compressed-file hashes, decompresses into a
temporary directory, checks the uncompressed size and hash, and invokes
`drat-trim` with `-i`, its binary-proof input flag. For a quick archive
integrity check that deliberately does not verify the logical proof, run:

```sh
python repro/countcegar_k4/verify_drat.py --hash-only
```

`kissat404` is also available through `--solver`. These PySAT bindings do not
provide safe asynchronous wall-clock interruption for either backend, so a
nonzero timeout runs the solver in an isolated child process and terminates
only that process at the deadline. The differential regression requires both a
successful real-backend child and detection of a synthetic exit-code-17 crash
within two seconds; it also detects a synthetic deadline with the expected
timeout reason within two seconds and records the exact checker-source hashes.
The uncompressed DIMACS file is the exact, hashed solver input. The earlier
JSON files preserve run metadata and solver verdicts; the separately archived
DRAT trace is the machine-checkable UNSAT certificate.

The fixed-instance slot boundary has its own executable regression:

```sh
python repro/countcegar_k4/test_slot_boundary.py
```

It exhaustively enumerates the retained `t47.json` valuation, checks that its
four EFX0 allocations are distinct, and expects fixed-master statuses SAT for
an empty pool, SAT for three pooled allocations, and UNSAT for all four.

After the terminal CP-SAT and direct-SAT checks, the manifest generator refuses
to run unless both claim-bearing verdicts, all recorded hashes, the CNF
differential regression, and the boundary test are consistent. It accepts the
retained Z3 record only as either a hash-consistent UNSAT result or the
hash-consistent timeout-UNKNOWN attempt reported above; the latter is explicitly
marked as non-evidence. The generator also parses the model and response
protobufs and requires an
`INFEASIBLE` response, rebuilds byte-identical CP-SAT, SMT-LIB2, and DIMACS
inputs from the current source plus terminal pool, and exactly replays all
seven SAT trace rounds from the deduplicated historical checkpoint:

```sh
python repro/countcegar_k4/make_manifest.py
```

UNSAT of this master is sufficient because a valuation with at most three EFX0
allocations could place all of them in the three slots. Every pooled allocation
would then either fail EFX0 or equal a slot, producing a master model. The
double-lex constraints only choose a row/column permutation representative, and
the number of EFX0 allocations is invariant under those permutations. The
DRAT certificate removes trust in CaDiCaL's UNSAT verdict, but the semantic
conclusion still depends on the independently auditable CNF translation and a
correct proof checker.

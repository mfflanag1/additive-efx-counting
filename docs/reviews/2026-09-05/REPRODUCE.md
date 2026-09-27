# Counting: staged reproduction

Run from this directory. Python 3.13 was used for dependency-bearing checks. Original package pins are in `repro/countcegar_k4/requirements.txt`; fresh replay versions are recorded in the check logs. A working convenience command using `uv` is:

```sh
uv run --with numpy --with python-sat --with z3-solver --with ortools python repro/counting_witnesses/verify_all.py
uv run --with numpy python artifacts/generalized_parking/verify_certificates.py
uv run --with numpy --with python-sat --with z3-solver --with ortools python repro/countcegar_k4/test_sat_differential.py --result-out /tmp/efx-counting-sat-differential.json
uv run --with numpy --with python-sat --with z3-solver --with ortools python repro/countcegar_k4/test_slot_boundary.py --result-out /tmp/efx-counting-slot-boundary.json
```

The witness run checks 11,860,961 allocations per implementation across six inputs. Exact timings depend on hardware. The differential and boundary tests exercise both SAT and UNSAT outcomes and reject malformed/repeated allocations where appropriate; they are not themselves the full finite-box proof.

The shortest full logical replay of the retained counting CNF proof, once a C compiler is available, is:

```sh
cc -O2 -o /tmp/efx-review-drat-trim review-tools/drat-trim.c
python3 repro/countcegar_k4/verify_drat.py --checker /tmp/efx-review-drat-trim
```

The source and license for the freshly used checker are enclosed. The wrapper first checks all archived CNF/proof hashes, decompresses the retained proof, then requires a zero checker exit and `s VERIFIED`. Temporary decompression needs about 135 MB, in addition to working memory. This is not a verified compiler or formalized proof checker. `--hash-only` is an integrity test, not a proof replay.

For a new independently encoded master, see `repro/countcegar_k4/README.md` and its SAT/CP-SAT replay commands. These are slower than checking the archived certificate and are not required merely to read the paper.

Build the review paper:

```sh
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error paper/main.tex
```

`SOURCE_INVENTORY.json` hashes the original source blobs. Use the new `REVIEW_MANIFEST.json` to authenticate this revised paper and distributed evidence. Running `supplement/build_release.py` here is not supported: this selected copy is not a clean Git checkout of the original release.

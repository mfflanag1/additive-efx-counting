# Fresh verification and trust boundary — 27 September 2026

Performed on the isolated audit worktree based on main
`b3eb183d2375c3b98ec0196bbcc06207b1d85a86`, plus an exact F4 snapshot.
No research solver continuation was launched. These commands terminated.

| Check | Fresh result |
|---|---|
| `make verify-paper` | PASS, 118.48 seconds: six counts over 11,860,961 labeled allocations per implementation, seven generalized-parking certificates, SAT differential controls, slot boundary, archived DRAT hash/decompression check. |
| Full `verify_drat.py` with freshly built pinned drat-trim | VERIFIED, 76.05 seconds, checker exit 0. Not merely a hash check. |
| F4 `pytest -q tracks/parkability/test_fixed_u_f4.py` at 712a40e | 4 passed in 105.92 seconds, including exact four-edge obstruction/five-edge completion calibration. |
| Counting manuscript | LaTeX build succeeds, 10 pages; no overfull/underfull boxes or LaTeX warnings in final log. |

Logs, machine-readable results and exact command arguments are in `checks/`.
The environment was Python 3.13.5 via uv with NumPy, python-sat, z3-solver,
OR-Tools and pytest. Absolute interpreter paths in the logs are temporary runtime
paths, not reproduction requirements. Portable commands from a clean checkout:

```sh
python -m pip install -r requirements.txt
make verify-paper
cc -O2 docs/reviews/2026-09-05/review-tools/drat-trim.c -o /tmp/efx-drat-trim
python repro/countcegar_k4/verify_drat.py --checker /tmp/efx-drat-trim --timeout-seconds 600
```

For F4, create a separate worktree at `712a40e` and install z3-solver/pytest/NumPy;
do not switch the publication worktree or infer a theorem from an unrelated branch.

## Exact proof identity

- CNF SHA-256: `ccc2aa45a5710d967a166abf7bc56a2026c517f4157730872b99524027baa166`.
- Compressed proof: `ddcad227664410e4e3552bd774ea369888dae4e56093a3016a4ce880eb549977`.
- Uncompressed proof: `710c51bd36addd3d1ea73c14d902d2b1d9aba23cafcd4874ef1d21daf2779a5b`, 134,426,255 bytes.

## Not freshly verified here

The complete historical goods archive, all 408 F4 profiles, every bounded theorem,
every two-nonsingleton proof case, global admission and a cap-free closure theorem
were not re-proved. The focused tests do not discharge those obligations. The
counting DRAT result is only as sound as the CNF-to-mathematics encoding and proof
checker. The full historical `make verify-parkability` suite is separate from these
focused checks; its optional local replay was stopped at the user's request to
finish promptly. No complete pass is claimed. GitHub CI status is separate.

The adjacent chores update has its own fresh checks and limits at
`counterexample-hunt/efx2/review/2026-09-27/VERIFICATION.md`.

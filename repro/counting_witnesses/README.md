# Exact count-\(n\) witness reproduction

This package runs the paper's two pure-Python exact verifiers and its separate
NumPy-vectorized counter on one matrix for each of the six reported cells.
`instances.json` fixes every source and verifier by SHA-256 and records the
expected count.

From the repository root, run:

```sh
python3 -m pip install -r repro/counting_witnesses/requirements.txt
python3 repro/counting_witnesses/verify_all.py \
  --output repro/counting_witnesses/last_run.json
```

Each implementation enumerates all \(n^m\) complete labeled allocations. The
two pure-Python implementations use different enumeration and bundle-checking
strategies. The vectorized implementation supplies a third independent
execution path. Because every matrix entry is positive, the EFX\(_0\) and
positive-good EFX counts must also agree; the runner checks this equality.

The expected result is:

```text
PASS n4_m7 (4,7): count=4 across 16,384 allocations
PASS n5_m8 (5,8): count=5 across 390,625 allocations
PASS n6_m9 (6,9): count=6 across 10,077,696 allocations
PASS n4_m8 (4,8): count=4 across 65,536 allocations
PASS n4_m9 (4,9): count=4 across 262,144 allocations
PASS n4_m10 (4,10): count=4 across 1,048,576 allocations
PASS all 6 count-n witness checks
```

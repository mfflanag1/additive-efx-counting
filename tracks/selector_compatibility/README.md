# Restricted-selector compatibility checkpoint

The conventional proof is in
[the research packet](../../docs/global-admission/RESTRICTED_SELECTOR_COMPATIBILITY_20261016.md).
Its load-bearing published input is BCFF, arXiv:2102.10654v2, Theorem 5.1.
The scripts below are exact finite calibrations and certificate checkers, not
formalizations of that published proof.

From the repository root, using Python 3.10 or later:

```sh
python3 -m unittest discover -s tests -p 'test_selector_compatibility*.py' -v
python3 tracks/selector_compatibility/independent_enumerator.py results/lexmax_partial_counterexample_4x9.json
python3 tracks/selector_compatibility/verify_trace.py results/selector_compatibility_discard_repair_20261016.json
python3 tracks/selector_compatibility/verify_trace.py results/selector_compatibility_pool_repair_20261016.json
python3 tracks/selector_compatibility/verify_trace.py results/selector_compatibility_complete_loss_20261016.json
```

No solver or third-party library is required. The enumerator visits all 5^m
physical assignments, has a default ten-good guard, and fixes priority 0,1,2,3.
It reports all-partial, safe-partial, safe-at-most-one-charity, exactly-one-safe,
and complete maxima separately. It does not assume that the supplied candidate
is maximal. Rational inputs are scaled to exact integers. The frozen nine-good
output is `results/selector_compatibility_4x9_exact_audit_20261016.json`.

The trace checker uses direct Fraction arithmetic and does not import the
enumerator or any historical EFX helper. Its default domain is the positive,
bundle-nondegenerate four-agent profile in the theorem. Priorities remain fixed
throughout a trace. A BCFF-labeled step is verified as a physical EFX lex
improvement from a state with at least two unallocated goods; the checker does
not certify which case of the BCFF construction generated that step.
The trace checker defaults to at most sixteen goods before exponential
nondegeneracy checks; `--max-goods` explicitly overrides this runtime guard.
These computational limits do not limit the conventional theorem.

## What the three physical traces demonstrate

1. **Discard/repair, seven goods.** A valid singletonization endpoint improves
   first-priority utility from 2051 to 5152 but leaves three unsafe charity goods.
   A verified EFX improvement returns to S (indeed to a complete allocation).
   This tests the endpoint interface; it is not advertised as an example
   satisfying every antecedent of an alternating champion-cycle theorem.
2. **Pool repair, five goods.** A singletonization leaves one envied charity good;
   the minimum-envied-subset replacement restores safe charity and improves lex.
3. **Complete utility loss, nine goods.** The archived example completes with
   first-priority utility 6464 rather than 10432. This is a valid complete exit,
   not a lexicographic contradiction. The valuation matrix is historical, not a
   newly discovered counterexample.

Malformed physical assignments, missing goods, non-EFX endpoints, non-strict
partial exits, priority changes, and continued traces after reaching S are
rejected. Passing finite tests is not a universal theorem; the conventional
proof supplies that part, with its published dependency explicit.

# Physical admission: exact local verifiers

This track derives and checks the physical entry for A1; it does not prove the
fixed-U admission theorem. See [the proof and exact boundary](../../docs/global-admission/PHYSICAL_ADMISSION_A1_20261016.md)
and [verification/review record](../../docs/global-admission/PHYSICAL_ADMISSION_A1_VERIFICATION_20261016.md).
The continuation [physical cycle release](../../docs/global-admission/PHYSICAL_CYCLE_RELEASE_20261016.md)
derives priority-improving probes, one-run residual returns, and original-floor
observer/Hall consequences. Its [verification record](../../docs/global-admission/PHYSICAL_CYCLE_RELEASE_VERIFICATION_20261016.md)
separates these conventional lemmas from the bounded executable checks.

From the repository root, standard-library Python only:

```sh
python3 -m unittest discover -s tests -p 'test_physical_admission_*.py'
python3 -m unittest discover -s tests -p 'test_selector_compatibility_*.py'
python3 tracks/physical_admission/extract_champion_cores.py results/selector_compatibility_4x9_exact_audit_20261016.json --archive
python3 tracks/physical_admission/verify_cycle_release.py results/selector_compatibility_4x9_exact_audit_20261016.json --archive
python3 tracks/physical_admission/verify_state_separation.py --archive docs/global-admission/references/a1_source/fixed_u_twelve_atom_four_edge_residuals_20260826.json
```

Expected: 60 physical-admission tests (including 21 cycle-release tests), 48 A0
regression tests. CLI reports are deterministic and match
`results/physical_admission_champion_cores_20261016.json`,
`results/physical_cycle_release_20261016.json`, and
`results/physical_admission_state_separation_20261016.json`, respectively.

`extract_champion_cores.py` takes original-good values/ownership, checks EFX and safe
singleton charity, exhausts all minimal envied cores and decorated simple cycles,
and independently rechecks each disjoint-cycle exchange. It does not check global
maximality. Its CLI is bounded by explicit `--max-goods` and
`--max-decorated-cycles`; hitting either rejects the input, not an UNSAT theorem.

`verify_state_separation.py` takes named roles as disjoint nonempty physical packets,
checks the literal base, exhibits every normalized role bound and root-wall failure,
and reconstructs signed transfers including charity. `--profile PATH` accepts the
schema documented in the source; `--require-root-wall` makes that wall mandatory.
Without an input it runs a base-only calibration. Its archived mode checks only
the stated physical predicates, not historical solver claims or all master premises.

These loaders reject inexact Python float values and malformed physical records. The core
loader accepts JSON decimals as exact Fractions; the state loader deliberately
accepts only integer JSON numbers or exact rational strings. Both reject duplicate
object keys and nonfinite tokens. Frozen historical driver files under references
are audit sources, not dependencies imported by these verifiers.

`verify_cycle_release.py` reuses the exhaustive core/cycle enumerator, but computes
physical ownership, all EFX deletions and utilities independently with Fractions.
It selects the canonical cycle before checking applicability; it never skips a
shorter unfavorable cycle. Release and residual-return winner rules are distinct.
Two ordinary runs give `mechanism_not_guaranteed`. A finite successful audit does
not verify global maximality, no-complete-EFX, all-G Hall consequences, or universal
admission; the JSON records these boundaries explicitly.

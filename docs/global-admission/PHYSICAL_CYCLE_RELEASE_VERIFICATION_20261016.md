# Physical cycle release: verification and handoff

16 October 2026. Branch `codex/efx-physical-admission-20261016`, continuing committed
checkpoint `2930168d96740b05ec41d4b71fae9f0b3d9c33c0`.

## Result and exact boundary

[The conventional proof](PHYSICAL_CYCLE_RELEASE_20261016.md) derives physical states
from the original selected allocation O, not from an assumed numerical BASE:

1. Canonical full-graph cycle: no internal non-successor champion edges, no ordinary
   envy parallel to a chosen G edge, and original-owner residual payment bounds.
2. Charity release: k G edges yield a priority-improving physical probe with k-1
   underpaid owners; each deficit is strictly between zero and that owner's value
   of p in the nondegenerate scope. Every EFX failure is witnessed by an underpaid
   owner, and its shortfall is at most that deficit. In particular k=2 derives a
   one-underpaid support state, without assuming a GG two-cycle or a role layout.
3. Residual return: at most one ordinary run yields a complete physical probe that
   strictly improves every cycle owner. All EFX failures target enlarged incoming-G
   junction bundles, including the winner's p-augmented junction when applicable.
4. All-G cycles: at least two cross-pools have foreign-observer old-floor failures;
   a minimal physical agent-side Hall witness exists with the stated deficiency,
   without assuming matching rank three. The GG external-core fact follows directly.

These are internally reviewed conditional lemmas. No publication novelty priority
is asserted for champion-cycle, BCFF or Hall ingredients. They do not establish
A1's full fixed-U layout, ADMIT4, four-agent existence, or general additive EFX.
The all-G universal statements are justified by their conventional arguments;
the finite probe program does not purport to certify those universal arguments.

## Exact physical calibration

Input: the frozen nine-good global-selector audit at the SHA below. Exhaustive local
core enumeration retains 32 subsets, four minimal cores, six champion edges and one
decorated cycle, 1->3->2->1. Both priority-compatible release winners are checked.

| construction | winner | new own utilities | unique EFX shortfall |
|---|---|---|---|
| release | 2 | 10432, 34848, 33036, 18448 | observer 3, target 0, delete good 7: 1072 |
| release | 3 | 10432, 34848, 26636, 22800 | observer 2, target 0, delete good 7: 3124 |
| residual return | 3 | 10432, 38946, 36877, 22800 | observer 1, target 2, delete good 3: 2019 |

The release raw deficits are 2064 and 4101, distinct from the EFX shortfalls.
All three constructions improve original priority but fail EFX. The return is
complete and Pareto-improving but still fails EFX. It is not a legal terminal exit.
The same instance has 103 complete EFX allocations, so it is not a counterexample
to EFX or to admission under a no-complete-EFX premise.

This refutes two unconditional shortcuts at the selected global state: all release
blockers being inside the cycle, and ordinary/G edges being transitively contractible
as augmented champion edges. It does not defeat every possible physical repair.

The global-maximality/nondegeneracy facts and counts of all partial/complete EFX
allocations are imported from the earlier hashed exhaustive audit, not rerun here.
That earlier computation examined 5^9 = 1,953,125 physical ownership assignments.
The new program does not trust global/complete-exit assertions in its input JSON.

## Fresh checks

- 60 physical-admission tests passed, including 21 new release/return tests.
- 48 selector-compatibility regression tests passed: 108 tests in total.
- Two separately launched probe CLI runs were byte-identical; a third streaming
  hash agrees with the persisted result. The test suite also compares CLI output
  with that result file.
- Every physical-good deletion and own utility is checked with exact Fractions.
  The test oracle independently reconstructs goods, values and all inequalities.
- Negative controls: wrong source/target orientation, forged core metadata,
  nonphysical goods, duplicate or malformed ownership, unsafe cores, ties/zero
  deficits, omitted p-junction comparisons, and enumeration-limit rejection.
- Positive control: a local nonmaximal EFX state has a genuine improving EFX release;
  the program does not force every probe to fail or falsely infer global maximality.
- All decorated cycles are enumerated before canonical selection. Applicability
  failures are reported, not skipped in favor of a favorable longer cycle.
- The alternating GEGE case returns `mechanism_not_guaranteed` for residual return.
  It is not promoted to a negative theorem about other possible mechanisms.

The core/cycle enumerator is reused from the prior reviewed checkpoint. Ownership,
EFX comparisons and utilities in the probe layer are independently recomputed;
this is not a fully separate implementation of the entire global-selection proof.

## Replay from repository root

Standard-library Python only; no solver or network required:

```sh
python3 -m unittest discover -s tests -p 'test_physical_admission_*.py'
python3 -m unittest discover -s tests -p 'test_selector_compatibility_*.py'
python3 tracks/physical_admission/verify_cycle_release.py results/selector_compatibility_4x9_exact_audit_20261016.json --archive | cmp - results/physical_cycle_release_20261016.json
git diff --check
```

The shortest numerical replay is the third command (exit 0 with no output).
This does not rerun the original exhaustive global-selector census.

## Review and cross-model adjudication

- [Independent proposal plus opposite-model QA](PHYSICAL_CYCLE_RELEASE_CROSS_MODEL_RECORD_20261016.md):
  Fable research `20261016-143119-d0493cd6`, Codex QA `qa-71f7e1f6ea`.
  QA verdict `revise`. Root adjudication: **reject the raw candidate as written**,
  while retaining the independently verified one-run construction with corrections.
  Specifically, its pure-G p-assigned extension omitted the enlarged p-junction
  wall, and its two-run discussion was not a precise lemma. Both were verified
  against literal ownership formulas. The accepted proof includes the enlarged
  junction and explicitly leaves two-run return untreated. This record is the
  adjudication evidence, with approximately eight minutes of corrective rework.
- [Hostile review of the corrected proof](PHYSICAL_CYCLE_RELEASE_HOSTILE_REVIEW_20261016.md):
  separate Fable review `20261016-144241-28149f1b`, no substantive mathematical
  defect found in the reviewed scope. Clarified charity domain and the source of
  self-edge exclusion. No code executed by that reviewer.
- Native independent code review: no blocking finding; 21 focused tests and 12
  additional exact probe comparisons passed. Its suggested augmented-winner
  regression was added and passed.
- BCFF source correspondence was checked separately against the primary PDF,
  section 2.3, Definition 3.9, Lemmas 3.13–3.14 and Theorem 3.16. Mixed cycles are
  not covered by that all-G import. No new source-based existence claim is made.

These are internal cross-model/code reviews, not a specialist referee report,
formal proof-assistant verification, or independent global-exhaustion rerun.

## SHA-256 pins

```text
4fa9952c5d3c0a11251be646c1cf6e81cc46428df7ddbd7c337aab92574350cb  docs/global-admission/PHYSICAL_CYCLE_RELEASE_20261016.md
d57f005f3cf46d3f385eb6a8c72b6f43e9cdd1360e2a9868701fa3854fb39449  tracks/physical_admission/verify_cycle_release.py
ef3d078b1dc89ac014fba8c8aca59bebce07b399ffe20a685863b716199a19e2  tests/test_physical_admission_cycle_release.py
28c1eb437988d09f4eec076fda3ccd817edb92c5da7aefbf9a13dc54eee9fcb8  results/physical_cycle_release_20261016.json
b1a3f78be72370ea0d9518b4b9c2e5de43c5b9201350a05693714461724ae9b8  results/selector_compatibility_4x9_exact_audit_20261016.json
6a01a6de53d2691638d7298d45446533da1c774402de19c49de9968d9b2ce7a2  results/physical_admission_champion_cores_20261016.json
979fb0c644151d461c180dd9e3b746f2e1b1f650fdc3742b1ba831e92e337066  docs/global-admission/PHYSICAL_CYCLE_RELEASE_HOSTILE_REVIEW_20261016.md
43bb4dc393ed8549287787481f412d789f4575d69695dc34dc2e5d6eeb3b8a08  docs/global-admission/PHYSICAL_CYCLE_RELEASE_CROSS_MODEL_RECORD_20261016.md
```

## Next exact target

Prove or refute a physical repair/complete-exit dichotomy for the derived two-G
release state that covers both external fixed-bundle walls and return-induced
junction walls. Every partial exit must preserve original floors sufficiently to
improve the original priority and satisfy EFX; a complete exit may lower utilities.
Track original O thresholds through every rebasing. Do not import twelve-role
closure before deriving that layout and its complete predicate list. Three/four-G
and alternating-cycle branches remain separate coverage obligations.

The checkpoint ends without a new solver campaign or an unresolved background
computation. The next work should attack this missing implication, not add a fixed
menu and declare sampled success to be admission.

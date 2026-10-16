# Verification and hostile-review checkpoint — 16 October 2026

## Mathematical result and claim boundary

Accepted argument: for four positive, additive, bundle-nondegenerate agents and
one fixed priority, every partial EFX allocation can be lex-nondecreasingly
repaired to safe charity of size at most one. Restricted maxima are therefore
unrestricted partial-EFX maxima. The repair uses BCFF Theorem 5.1 plus the
minimum-envied-subset pool replacement and finite strict lexicographic ascent.

This closes A0, not ADMIT4, fixed-U physical extraction, response coverage, local
closure, or general EFX. It is an integration corollary of published work, not
a novel existence result. BCFF's case analysis remains external-trusted. The
trace verifier checks concrete witnesses, not that case analysis. A generic
perturbation does not justify fixed-initial-state repair for tied valuations.

## Actual checks run by the coordinator

- Independently read the primary v2 paper's Definition 2.3 and Lemma 2.4 proof
  (printed page 6), Theorem 5.1 (page 13), and fixed-VIP roadmap (page 14).
  Confirmed arbitrary fixed order, every starting EFX state with at least two
  charity goods, and no requirement that the pool decrease in one step.
- Checked the pool-replacement argument directly: physical conservation,
  minimal-cardinality deletion inequalities for every observer, unchanged
  bundles, recipient improvement, and preserved EFX.
- Independently inspected both new exact implementations. One uses scaled
  integer subset tables and enumerates all assignments; the other uses direct
  Fraction deletion arithmetic and validates supplied traces. They do not import
  each other's predicates or the historical parkability helpers.
- Ran `python3 -m unittest discover -s tests -p 'test_selector_compatibility*.py'`:
  **48 tests passed** (11 enumeration, 37 trace). Expected rejection cases are
  tested explicitly. Tests include arbitrary fixed priority transport, complete
  utility loss, complete non-EFX rejection, non-strict step rejection, malformed
  physical data, unsafe intermediate pools, and nondegeneracy guards.
- Ran the independent enumerator on the archived nine-good profile twice.
  Output was byte-identical to the committed report, SHA-256
  `b1a3f78be72370ea0d9518b4b9c2e5de43c5b9201350a05693714461724ae9b8`.
- Ran the three supplied physical trace certificates with the separate verifier;
  all accepted in the default nondegenerate scope.
- Ran the historical `tracks/parkability/audit_lexmax_counterexample.py` using
  `uv run --with numpy python`: PASS, including direct-insertion failure,
  322 eligible one-charity states, 103 complete EFX states, nondegeneracy, and
  the 24-priority-order insertion census. This is a separate code path.

## Exact nine-good calibration

All **1,953,125 = 5^9** original-good assignments were visited.

| Domain | EFX state count | Maximum utility tuple (priority 0,1,2,3) |
|---|---:|---|
| All partial EFX, no charity restriction | 10,929 | (10432,32782,30737,20512) |
| Partial EFX with safe whole charity | 864 | same |
| Safe charity of size at most one, INCLUDING complete | 425 | same |
| Safe charity of size exactly one | 322 | same |
| Complete EFX | 103 | (6464,32910,30737,20512) |

Each listed maximum is unique. There is no out-of-class improvement over the
archived restricted maximum. The complete EFX examples establish why a terminal
complete exit need not improve the selector's utility. These finite facts
calibrate the conventional theorem; they are not its proof.

## Independent mathematical reviews

1. **Independent Codex source audit:** the explorer re-read the primary theorem,
   checked the fixed-VIP transport, and re-derived the repair and selector-equality
   arguments. It withdrew its preliminary missing-repair suspicion after checking
   the stronger published theorem. No theorem-level defect remained in scope.
2. **Fable primary-source audit:** run
   `20261016-130401-74455774`, category `mathematical-proof`, engine auto selected
   Fable 5.1. Result: SOUND conditional on BCFF's published theorem. It checked
   the statements, hypotheses and priority transport, not the entire case proof.
3. **Opposite-model QA:** Codex QA `qa-4681243af1` accepted that source audit and
   independently confirmed the logical links. This was source/mathematical QA,
   not an execution of our new verifiers.

Coordinator verification is the source inspection, explicit argument, and actual
runs listed above—not the agreement of model verdicts. The Fable finding that
the August import audit already cited Theorem 5.1 was checked and incorporated:
the correction concerns the later September A0 framing, not that earlier import.
No independent human specialist review or Lean/formal proof is claimed.

Local full review record:
`~/.local/state/cross-model/efx-audit-20260927-9080c6f5d94b/20261016-130401-74455774/`.
Portable record is this summary, the exact sources, and the reproducible checks;
the full external review transcript is not required for reproduction.

Independent code snapshot review and its checked dispositions are in
[the code-review record](SELECTOR_COMPATIBILITY_CODE_REVIEW_20261016.md).

## Reproduction and source provenance

See [the five short commands](../../tracks/selector_compatibility/README.md).
`results/selector_compatibility_source_manifest_20261016.json` freezes twelve
historical transition/import files by commit, Git blob and SHA-256. Historical
source claims are dependencies, not silently re-proved by the compatibility
corollary. The retired non-EFX floor reset remains excluded.

The next mathematical target is A1: a complete physical extraction from the
selected original state into the proposed fixed-U roles, with the precise
selected/base/support-state identity and every branch accounted for. There is
no reason to continue searching for a counterexample to the now-sourced A0 lemma
in its declared scope.

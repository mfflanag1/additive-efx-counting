# Threshold--Hall checkpoint (2026-08-02)

This is the focused publication checkpoint for the four-agent threshold--Hall
route.  It freezes one proved structural reduction, one open conversion target,
the exact finite evidence motivating that target, and the source used to audit
the evidence.

## Headline and exact boundary

The proved result is the **owner-minimum Hall-pair extraction theorem**:
starting from an eligible four-agent one-floater EFX allocation, direct
insertion and owner-minimum transfers either produce an EFX-perfect-matching
candidate or expose a two-agent/one-neighbor Hall obstruction.  The theorem is
cap-free and is certified by independently checked QF_LRA instances.

The open target is the **threshold-plateau cycle conversion lemma**.  For the
normalized owner-threshold potential

\[
\Theta(X,f)=\sum_i\frac{v_i(X_i)-\min_{g\in X_i}v_i(g)}{v_i(M)},
\]

the stored-profile corpus contains a Hall-completing global maximizer in every
one of 237 distinct positive four-agent profiles with 7--10 goods.  A fixed
minimum-utility tie-break fails on 46 profiles.  Across all 4,847 blocked
states selected by that tie-break, an exact audit reaches a completing state
on the same maximum plateau by at most two threshold-neutral floater swaps,
each strictly improving the recorded Hall margin; 4,843 transitions are
literal owner-minimum-slot cycles and the remaining four are tied-value
variants.

These corpus statements are finite computational evidence, not universal
theorems.  **Neither complete EFX for four additive agents nor general
additive EFX is resolved by this checkpoint.**  The missing analytic step is
to convert every extracted two-agent/one-neighbor Hall trap into either a
strict increase of \(\Theta\) or a threshold-neutral slot cycle that strictly
improves a finite Hall-defect order while preserving all eligibility
inequalities.

## Review path

1. Read `PARTIAL_HALL_OWNER_MINIMUM_EXTRACTION_THEOREM.md` for the proved gate.
2. Read `PARTIAL_THRESHOLD_PLATEAU_CYCLE_TARGET.md` for the exact proposed
   conversion lemma and the arbitrary-agent extension boundary.
3. Inspect `partial_hall_threshold_existential_full_corpus_scan.json` for the
   237-profile existential selector census.
4. Inspect `partial_hall_threshold_minimum_full_corpus_scan.json` for the 46
   fixed-tie-break failures.
5. Inspect `partial_hall_threshold_plateau_completion_analysis.json` for the
   complete 4,847-state transition census.

The two large JSON files are intentionally retained: they are exact audit
records, not transient solver traces.  The 44 compact source JSON records
referenced by the 46 failing profiles are also retained so the plateau replay
is self-contained.  Annealing traces, temporary solver pools, interrupted
scans, and unrelated EFX campaign artifacts are excluded.

## Replays

The plateau census can be regenerated exactly from its frozen source scan:

```bash
python tracks/parkability/analyze_threshold_plateau_completion.py \
  --source results/partial_hall_threshold_minimum_full_corpus_scan.json \
  --output /tmp/threshold-hall-plateau-replay.json
cmp results/partial_hall_threshold_plateau_completion_analysis.json \
  /tmp/threshold-hall-plateau-replay.json
```

The focused worktree regression gate used before publication is:

```bash
pytest -q \
  tracks/parkability/test_parkability.py \
  tracks/parkability/test_threshold_hall_checkpoint.py
```

At freeze time this reports 31 passing tests: the parent research snapshot's
30-test suite plus one focused threshold--Hall checkpoint test.  The complete
stored corpus that fed the 237-profile scan belongs to the broader research
worktree; this focused branch freezes the scan output, the 46-profile
counterexample payload used by the plateau replay, and all code needed for that
replay.  It does not claim that the heterogeneous 1,948-file discovery corpus
is independently frozen here.

## Frozen artifact hashes

- `partial_hall_threshold_existential_full_corpus_scan.json`:
  `dcf48b99b6a6a6f38519f58de8ded072a1bbd51515a63491fdc8c9e610da7ee7`
- `partial_hall_threshold_minimum_full_corpus_scan.json`:
  `2344e4ce61e7a7337aa33ef9db0af5a12a184133aa6a1aed9aa7af11c4f0fa25`
- `partial_hall_threshold_plateau_completion_analysis.json`:
  `f1aed59eb64405d0eaef0c80e44c408af0810e3176e3b5f627f61bf912e20ffd`

The plateau artifact records the minimum-tie-break scan hash internally and
the value agrees with the second hash above.

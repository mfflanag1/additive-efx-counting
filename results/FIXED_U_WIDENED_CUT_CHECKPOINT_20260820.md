# Fixed-U widened chart cut checkpoint

**Date:** 2026-08-20  
**Branch:** `codex/efx-fixed-u-resume-20260820`  
**Parent:** `cc/efx-idwitness-20260816` at `ef67d89`

## Corrected starting point

This checkpoint adopts `HANDOFF_FROM_CC_20260817.md` and the identity-aware
corpus as authoritative. In particular:

- the old one-minimum-split obstruction is a selector artifact;
- the banked population is `111` distinct profiles over `211` rounds, or
  `113` including terminal profiles—not `173`;
- the earlier “22-good / 1/696” sentence conflated two profiles;
- Theorem 1 of `IDENTITY_AWARE_SLACK_TWO_20260816.md` is the valid
  realization-free reduction; and
- the only live chart failure shape is a profile for which every four-edge EFX
  allocation must split a wild role.

No result here concerns the now-scooped standalone `(4,8)` theorem.

## Durable cut migration

The widened driver previously checkpointed source profiles and split-set
statistics, but not the allocations for all `8^k` pattern vectors. Its cuts
therefore could not be replayed without rerunning the oracle. This is repaired.

Every accepted cut is appended to a JSONL ledger containing the complete
certificate, source totals and minima, split set, branch, pattern count, and a
SHA-256 digest. Before the summary advances, the ledger append is flushed and
`fsync`ed. On resume, every record is hash-audited, coverage-audited, and
rechecked in exact rational arithmetic. A ledger ahead of the JSON summary is
authoritative. Torn lines, duplicate or missing iterations, altered payloads,
incomplete pattern products, and failed EFX allocations are rejected.

The pre-ledger snapshot migrated successfully:

```text
rounds       191
whole-role   188
one split      3
ledger lines 191
```

The resumed run added three further whole-role certificates and then the
master returned `UNKNOWN` (`canceled`) at its 120-second timeout:

```text
rounds       194
whole-role   191
one split      3
obstructions   0
ledger lines 194
```

Thus the run passed its former freeze, preserved every new cut, and found no
wild-and-forced obstruction. This is evidence only. The chart theorem needs
master `UNSAT`; a negative shape needs the widest oracle itself to return
`UNSAT_NO_TAME_SPLIT_ALLOCATION`.

## Verification

```bash
pytest -q \
  tracks/parkability/test_fixed_u_multi_split_chart.py \
  tracks/parkability/test_fixed_u_tame_menu_chart.py
```

Recorded result: `49 passed in 0.43s`.

The new tests cover record round-trip, digest tampering, torn-line rejection,
and recovery when a durable ledger entry is ahead of the summary. Existing
tests enforce the full `8^k` product and prohibit search limits from borrowing
obstruction language.

## Replay

```bash
python -m tracks.parkability.run_fixed_u_multi_split_chart_theorem \
  --form-index 2 \
  --resume results/fixed_u_multi_split_chart_resume_20260820.json \
  --cut-ledger results/fixed_u_multi_split_chart_cuts_20260820.jsonl \
  --output results/fixed_u_multi_split_chart_resume_20260820.json \
  --maximum-rounds 400 --timeout-seconds 120 \
  --pattern-budget 20000 --random-seed 0
```

The CLI now requires `--cut-ledger`; a long chart run cannot silently revert
to the nonreplayable mode.

## Analytic status

Lemma D remains the only premise-level allocation-wide constraint:

> Every EFX allocation gives `d` a role outside `W`, or separates `a0` from
> `a1`.

A first strengthening is false at the current cut frontier. Even after
excluding all 189 then-banked whole-role certificates, the master is SAT when
every role in `{gq,m,l,a0,a1}` is simultaneously wild. Therefore the theorem
cannot follow merely by showing that one empirically forced role is tame. The
missing statement must combine wildness with the geometry making a role
forced.

The 194-cut master times out before another model. Extending the same CEGAR has
sharply declining value. The next computational move is a normal form for the
absent-response disjunctions and EFX cuts that shrinks the 96-rational-variable
master. The next analytic target is:

> If a named role is wild and every within-budget EFX allocation splits it,
> then the form-2 wall admits rank four, a forbidden response edge, or a
> whole-role four-edge exchange.

Each conclusion is terminal in the frozen chart. No direction is yet proved.

## Claim boundary

Proved here: crash-safe, independently re-audited replay of all 194 widened
chart certificates, and three additional exact adversarial profiles closed
after the handoff.

Not proved: termination of the 194-cut master; the wild-and-forced implication;
the form-2 tame covering-menu theorem; coverage of every saturated root-facing
rank-three fixed-`U` state by form 2; or the active universal theorem.


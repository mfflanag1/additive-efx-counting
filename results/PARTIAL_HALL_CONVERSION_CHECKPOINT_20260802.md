# Partial Hall conversion checkpoint — 2026-08-02

## Proven boundary

The cap-free four-agent owner-minimum Hall-pair extraction theorem is proved:
every eligible one-floater EFX allocation either completes after direct
insertion or one chosen owner-minimum transfer, or one selected candidate has
a two-agent/one-neighbor Hall witness. The theorem includes arbitrary bundle
sizes, singleton bundles, and ties. Its 16 Z3 cases and five independent cvc5
symmetry representatives replay with:

```bash
make verify-partial-hall-pair-extraction
```

This does not prove conversion of the pair trap or complete EFX.

## Conversion boundary

The first feasible hard orbit is

```text
candidate (host=0, source=0, destination=1),
trapped agents {0,1}, sole neighbor 1.
```

The strengthened exact-two-goods conversion menu contains:

- 16 owner-minimum substitution partitions;
- all 24 ordinary one-good transfers;
- 12 swaps between bundle 3 and bundles 0, 1, and 2; and
- the two mined three-cycles `(0,0,2,0,3,0)` and
  `(0,1,2,0,3,0)`.

Local exact models show that swaps, transfers, and cycles are successively
necessary. The next surviving topology is a floater-coupled augmenting path,
which aligns this route with the connected-exchange and
transfer-component dependency-cycle lemmas.

## Tie correction

The cap-80 artifact
[`partial_hall_owner_minimum_connected_menu_hall_r00_o01_k80_resume_cegar.json`](partial_hall_owner_minimum_connected_menu_hall_r00_o01_k80_resume_cegar.json)
is **not** a counterexample to the full owner-minimum family. Its exact profile
has tied owner minima. The independent audit finds one EFX completion after
moving an alternate tied minimum:

[`partial_hall_owner_minimum_connected_menu_k80_counterexample_base_audit.json`](partial_hall_owner_minimum_connected_menu_k80_counterexample_base_audit.json).

Retain this artifact only as evidence that a symbolic chosen-minimum encoding
must either enumerate every tied minimum or enforce uniqueness.

## Clean stopping state

The repaired master enforces unique selected owner minima. At cap 80, Hall
orbit 1 and trap-witness branches 0 and 2 time out with the 91-blocker seed.
Branch 1 finds an intermediate obstruction, learns two further swap blockers,
and then times out/cancels. The durable 93-blocker checkpoint is:

[`partial_hall_owner_minimum_connected_menu_hall_strict_r00_o01_k80_t1_cegar.json`](partial_hall_owner_minimum_connected_menu_hall_strict_r00_o01_k80_t1_cegar.json).

Its status is `UNKNOWN`, not SAT or UNSAT. No campaign process is active.

## Highest-leverage continuation

The analytic target is to start a connected augmenting exchange from the
designated pair trap. If every positive exchange component fails EFX, the
cap-free dependency-cycle lemma supplies a directed cycle of cross-component
walls. The missing step is a weighted sum of those wall inequalities that
either yields an eligible improving component or contradicts normalized-
utilitarian maximality.

If computation is resumed first, use the 93-blocker branch-1 artifact as the
seed and retain strict owner minima:

```bash
python tracks/parkability/decide_partial_hall_owner_minimum_substitution_conversion.py \
  --remainder-multi-mask 0 --pair-orbit-index 1 --trap-witness-prefix 1 \
  --hall-witness-encoding --strict-owner-minima --integer-cap 80 \
  --include-one-good-transfers \
  --cycle-spec 0,0,2,0,3,0 --cycle-spec 0,1,2,0,3,0 \
  --include-pairwise-swaps \
  --swap-spec 0,0,3,0 --swap-spec 0,0,3,1 \
  --swap-spec 0,1,3,0 --swap-spec 0,1,3,1 \
  --swap-spec 1,0,3,0 --swap-spec 1,0,3,1 \
  --swap-spec 1,1,3,0 --swap-spec 1,1,3,1 \
  --swap-spec 2,0,3,0 --swap-spec 2,0,3,1 \
  --swap-spec 2,1,3,0 --swap-spec 2,1,3,1 \
  --cegar-batch 32 --max-iterations 200 \
  --seed-blocker-file results/partial_hall_owner_minimum_connected_menu_hall_strict_r00_o01_k80_t1_cegar.json \
  --output results/partial_hall_owner_minimum_connected_menu_hall_strict_r00_o01_k80_t1_resume2_cegar.json \
  --smt2 results/partial_hall_owner_minimum_connected_menu_hall_strict_r00_o01_k80_t1_resume2_cegar.smt2 \
  --timeout-seconds 300
```

The computation is secondary to the weighted dependency-cycle proof.

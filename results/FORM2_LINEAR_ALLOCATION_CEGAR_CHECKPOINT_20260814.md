# Form-2 linear-allocation CEGAR checkpoint

**Date:** 2026-08-14

**Status:** reproducible 33-model bounded census; no four-edge obstruction
found and no bounded or cap-free theorem proved

## Exact encoding improvement

For a complete allocation `Z`, additive EFX can be written without a
piecewise minimum:

```text
v_i(Z_i) >= v_i(Z_j minus g)
for every i != j and every g in Z_j.
```

This is exactly equivalent to the usual least-good tail inequality. The new
driver uses these direct linear deletion inequalities in every allocation
cut, avoiding thousands of repeated nested `If` expressions. A separate
QF-LRA regression proves equivalence to the old tail encoding for target
sizes 1 through 12.

## Reproducible two-stage run

The corrected exact-response form-2 twelve-atom master was run in two
declared stages. Each adversarial valuation was separated by up to eight
topology-diverse complete EFX allocations using at most four frozen-support
supplier/recipient pairs.

- Stage 1: 20 rounds, 160 cuts, `ITERATION_LIMIT`.
- Stage 2: 13 rounds, 104 fresh cuts after replaying stage 1,
  `ITERATION_LIMIT`.
- Combined: 33 exact rational models and 264 distinct allocation cuts.

Every model admitted at least one complete EFX allocation within the edge
bound. The minimum edge histogram was

```text
2 edges:  7 models
3 edges: 19 models
4 edges:  7 models.
```

The number of complete four-edge EFX allocations per model ranged from 14
to 196, spread across 8 to 54 transfer topologies. The 264 selected
witnesses used 141 distinct topologies, so the evidence does not support one
small universal fixed-topology menu.

## Structural signal

Across all 33 bounded models, the inclusion-minimal exact-response cores had
three invariant whole-target patterns:

```text
r -> q : the complete Q target
d -> q : the complete Q target
q -> s : the complete E target.
```

The most frequent selected topology, appearing in 11 rounds, was the
functional charity path

```text
charity -> r -> s -> q -> d.
```

This is the path already isolated analytically by the sacrificed-source
shortest-charity-path lemma. Its only payment obstruction is capture of the
root endpoint margin by the outgoing `s`-response core. The census therefore
supports the existing analytic target—reverse endpoint/shared-target capture
using the signed saturation ledger—rather than another topology expansion.

The invariant whole-target pattern is specific to this twelve-atom cell. It
must not be promoted to a cap-free claim about arbitrary physical response
cores.

## Claim boundary and next step

Proved: equivalence of the ITE-free EFX encoding and exact replay of the
33-model census. Not proved: termination of the bounded CEGAR, bounded
UNSAT, a bounded countermodel, the cap-free fixed-`U` theorem, or additive
EFX.

Do not continue by merely increasing the round limit. The next analytic
target is the simultaneous terminal packet system: combine the root
endpoint-critical packet, the shared-target overlap-critical packet, and
their frozen supplier labels with the full signed `X -> Y -> Z` margins.
Either obtain a release-compatible generalized-PI/component exit or encode
a full-premise positive-rational countermodel.

## Authoritative files

- `results/exact_response_empty_seed.json`
- `results/exact_response_form2_linear_allocation_cegar_fresh_v2_20260814.json`
- `results/exact_response_form2_linear_allocation_cegar_stage2_v2_20260814.json`
- `results/exact_response_form2_linear_cegar_checkpoint_analysis.json`
- `tracks/parkability/run_exact_response_linear_allocation_cegar.py`
- `tracks/parkability/analyze_exact_response_linear_cegar_checkpoint.py`
- `tracks/parkability/test_exact_response_linear_allocation_cegar.py`
- `tracks/parkability/test_exact_response_linear_cegar_checkpoint.py`

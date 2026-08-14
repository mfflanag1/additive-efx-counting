# Cap-free physical-minimum role-union checkpoint (2026-08-14)

## Outcome

This checkpoint does **not** prove or refute the active fixed-`U` theorem.
It replaces the earlier twelve-atom tail surrogate by an exact cap-free
description of the total and least-good value of each of the twelve named
roles.  In the exact response form-2 chart it finds a positive-rational
physical profile with no complete EFX allocation obtained by moving whole
named roles along at most four frozen-support supplier/recipient pairs.
Therefore a universal proof cannot finish by treating the named roles as
indivisible packets.  It must split at least one role, use a signed
PI/component/progress exit, or exploit premises absent from this chart.

This is a refutation of a **whole-role selector**, not a counterexample to
complete EFX and not a refutation of the active theorem, which permits
arbitrary subpackets.

## Exact abstraction

For every named role `g` and observer `i`, the model has its total value
`T[g,i]` and least physical-good value `M[g,i]`.  A common physical role is
constrained to be either:

1. a singleton for every observer: `M[g,i] = T[g,i]`; or
2. a multi-good packet for every observer: `2 M[g,i] <= T[g,i]`.

This is cap-free and exactly realizable: the second case needs only two
physical goods, valued `M[g,i]` and `T[g,i]-M[g,i]` by observer `i`.
Consequently the EFX tail of a union of roles is exactly its total value minus
the smallest participating role minimum.

An initial weaker run imposed only `0 < M <= T`.  Its obstruction models had
cells with `M < T < 2M`, revealing that the relaxation was physically
spurious.  Those runs were overwritten; schema v2 includes the common
singleton/multi-good disjunction and a regression test for this correction.

## Bounded results

- Exact response form 0: ten CEGAR rounds, 63 whole-role allocations blocked,
  `ITERATION_LIMIT`.  This is evidence only.
- Exact response form 2: a physically realizable obstruction after three
  rounds, with nine whole-role allocations blocked by accumulated cuts and no
  remaining complete EFX whole-role allocation in the exhaustive at-most-four
  support-edge menu for the terminal model.
- The allocation oracle enumerates the full declared whole-role menu; it is
  not a hand-selected topology family.

The form-2 terminal model is a reusable adversarial target for the next proof
step: identify the smallest within-role split that repairs it, and translate
that split into the terminal-path two-packet selector or a signed progress
certificate.

## Verification

Shortest command:

```bash
pytest -q tracks/parkability/test_exact_response_physical_minimum_cegar.py
```

Recorded result: `3 passed in 1.10s`.

The tests prove direct-deletion/least-role-tail equivalence for target sizes
1 through 12, confirm both exact-response masters are satisfiable, and exclude
the physically impossible `M < T < 2M` gap.

Replay commands:

```bash
python -m tracks.parkability.run_exact_response_physical_minimum_cegar \
  --output results/exact_response_form0_physical_minimum_cegar_checkpoint_20260814.json \
  --form-index 0 --maximum-rounds 10 --timeout-seconds 30 \
  --cuts-per-round 8 --random-seed 8140
python -m tracks.parkability.run_exact_response_physical_minimum_cegar \
  --output results/exact_response_form2_physical_minimum_cegar_checkpoint_20260814.json \
  --form-index 2 --maximum-rounds 10 --timeout-seconds 30 \
  --cuts-per-round 8 --random-seed 8142
```

SHA-256 at freeze:

```text
73d7d529ed3553bf0736fec30675cef642e3b63e1b8eeb3f333a187160cd1a14  tracks/parkability/run_exact_response_physical_minimum_cegar.py
8a945231c9c72f04f94d99f97cad0c4deed2618935384400f84052ba59b4f373  tracks/parkability/test_exact_response_physical_minimum_cegar.py
2f1fe1dade8bafe2316feaa0fea460866b4bdc4d6cd2d03702cacfee6274686f  results/exact_response_form0_physical_minimum_cegar_checkpoint_20260814.json
e396f24dfb60f0ea796e6dea46962a3ac4eb3794ee6e6e87932f9fa94eff6963  results/exact_response_form2_physical_minimum_cegar_checkpoint_20260814.json
```

## Exact remaining boundary

Still unproved:

1. conversion from the current-holder packet selectors to at most four
   frozen-`Y` supplier/recipient pairs when arbitrary subpackets are allowed;
2. observer EFX safety after those splits;
3. closure of the decorated-response recurrence by generalized PI,
   component extraction, or strict lexicographic progress; and
4. coverage from the two exact twelve-role response charts to every saturated
   root-facing rank-three fixed-`U` state.

No statement here resolves four-agent or general additive EFX.

## Best next move

Use the form-2 terminal obstruction as a separation oracle over within-role
splits.  Find a minimum-cardinality split repair and classify it by the three
terminal charity placements.  The desired theorem is that every such repair
either uses at most four frozen supplier pairs or forces one of the signed
PI/component/progress exits.  Avoid extending the whole-role CEGAR: form 2
has now proved that search space insufficient.

## External review still needed

Before citing even the selector refutation, an independent reviewer should:

1. rebuild the form-2 premise ledger without importing the master builder;
2. independently enumerate the whole-role four-edge menu and evaluate EFX;
3. verify simultaneous realizability of every role's totals/minima as common
   physical goods; and
4. audit whether the exact-response chart contains every intended saturation
   premise and no circular continuation exclusion.


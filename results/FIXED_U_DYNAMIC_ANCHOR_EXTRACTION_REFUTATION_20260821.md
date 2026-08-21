# Dynamic anchor-extraction theorem: exact refutation

**Date:** 2026-08-21
**Status:** exact positive-rational countermodel to the proposed dynamic-anchor
theorem; independently encoded; complete EFX not refuted

## Headline

The dynamic anchor-extraction theorem is false for the complete declared
exact-response form-2 physical-minimum master.

There exists an admissible positive-rational totals/minima profile such that:

1. no complete whole-role EFX allocation uses at most four support edges; and
2. for every non-singleton role `H`, every anchor observer, every pair of
   distinct recipients, and every allocation of all other roles whole, the
   rule “send any anchor-minimum `H` good to the first recipient and `H-g` to
   the second” fails for some permitted physical realization.

This is **not** an EFX counterexample. Its canonical physical realization has
a complete four-edge EFX allocation splitting only `a1`, and a verified
64-pattern tame menu splitting `{a1,h}` closes every realization.

## Exhaustive one-anchor normal form

Let `x_i` be observer `i`'s value for the selected anchor good of role `H`.
The exact universal-realization check is finite:

- At cardinality two, `x_i` is either `M_i` or `T_i-M_i`; the anchor row is
  fixed to `M_i`, and the complement deletion value is `T_i-x_i`.
- At cardinality at least three, feasible selected coordinates fill
  `[M_i,T_i-2M_i]`; every EFX slack is affine, so only its two endpoints need
  checking, while a complement deletion can attain `M_i`.
- Cardinalities four and above only shrink that interval and create no new
  inequality.

Thus the oracle exactly enumerates all roles, anchors, recipients, whole-role
assignments, four-edge topologies, two-good witness sides, and higher-cardinality
endpoint cases. It is neither a sampled census nor the stronger sufficient box
relaxation used in the earlier terminal proof.

## Calibration and CEGAR result

The generic oracle first passed all required calibration gates:

```text
retained form-2 profiles       205
closed whole-role              200
closed by dynamic anchor         5
terminal selectors recovered     2
```

The universal CEGAR deduplicated these to 192 symbolic candidates, added seven
fresh exact candidates, and then returned
`SAT_DYNAMIC_ANCHOR_OBSTRUCTION`. The terminal profile is frozen in
`fixed_u_dynamic_anchor_cegar_20260821.json`; its seven cuts are preserved in
the fsynced JSONL ledger.

## Independent audit

A separately written verifier uses integer owner variables rather than the
primary Boolean piece-placement encoding. It derives support edges directly
from owner equalities and independently enforces every exact endpoint EFX
inequality.

Recorded verdict:

```text
complete form-2 master replay                 SAT
whole-role four-edge oracle                 UNSAT
applicable role/anchor lanes                    40
all 40 independent lane decisions           UNSAT
canonical physical split cap 0              UNSAT
canonical physical split cap 1                SAT
minimum canonical split roles                 a1
```

Therefore the countermodel refutes the exact dynamic-anchor statement, while
the unrestricted physical gate explicitly prevents promotion to an EFX
counterexample.

## The first minimal correction—and its boundary

The obstruction's complete realization-free repair is a tame side-pattern
menu splitting roles `{a1,h}`. It contains all `8^2=64` witness-side patterns,
and every allocation is rechecked exactly. This identifies what one universal
anchor loses: different cross-observer minimum identities require different
allocations.

The natural corrected conjecture

> every form-2 profile has a tame side-pattern menu or a dynamic anchor

was then tested against the complete master. It is also false. Starting from
205 prior menu cuts and ten anchor cuts, the corrected CEGAR installed 81
fresh audited cuts—including a genuinely necessary `a0/q` anchor—before
reaching a profile with both:

```text
widest tame-family oracle       UNSAT_NO_TAME_SPLIT_ALLOCATION
dynamic-anchor oracle           UNSAT
```

Again this is not an EFX counterexample: its canonical physical realization
has a four-edge repair splitting only tame role `gq`. Attempting the next
smallest fixed correction—condition on the eight `gq` witness patterns and
permit one additional cap-free anchor—still leaves exact pattern `gq:0001`
uncovered after every role/observer anchor lane is exhausted.

The live missing mechanism is therefore genuinely conditional and
multi-packet: the anchor role or split topology must change with the tame
witness pattern, or two physical split roles must be coordinated.

## Premise implication audit

The following parts are consequences of definitions or encoded premises:

- prescribed minima are attained by physical goods;
- a common multi-good role satisfies `T_i >= 2M_i` in every row;
- whole-role bundle totals and deletion floors compress exactly to `(T,M)`;
- the owner-cycle, base-EFX, PI-free, exact-response, saturation, and source
  conditions are all present in the replayed form-2 master; and
- every accepted topology has at most four support edges.

What does **not** follow is the existential conjunction of affine anchor EFX
bounds for any single role/observer/topology. The independently replayed
countermodel satisfies the complete encoded premise system while defeating
all 40 applicable role/anchor lanes and the entire whole-role allocation
universe. It is therefore one explicit simultaneous countermodel to every
fixed one-anchor conclusion, not merely a negative statistic from prior
profiles.

No stronger semantic GG premise absent from the declared master is claimed to
be refuted.

## Reproduction

```bash
python -m tracks.parkability.run_fixed_u_dynamic_anchor_cegar \
  --seed results/fixed_u_dynamic_anchor_profile_calibration_20260821.json \
  --ledger results/fixed_u_dynamic_anchor_cuts_20260821.jsonl \
  --output results/fixed_u_dynamic_anchor_cegar_20260821.json \
  --maximum-rounds 500 --master-timeout-seconds 300 \
  --oracle-timeout-seconds 30 --edge-cap 4 --random-seed 821 --master-mode smt

python -m tracks.parkability.audit_fixed_u_dynamic_anchor_obstruction \
  --profile results/fixed_u_dynamic_anchor_cegar_20260821.json \
  --physical-decision results/fixed_u_dynamic_anchor_obstruction_canonical_physical_decision_20260821.json \
  --output results/fixed_u_dynamic_anchor_obstruction_independent_audit_20260821.json

pytest -q tracks/parkability/test_fixed_u_dynamic_anchor_extraction.py
```

Frozen principal artifact hashes:

```text
2255c2cf4ba3537097d510ddb2972645405f78329dc0cbccd02570400901df4a  results/fixed_u_dynamic_anchor_cegar_20260821.json
39e518d9b004f430fbc88c9263da5734acefae91a30ade559cb6f79e4511b94b  results/fixed_u_dynamic_anchor_cuts_20260821.jsonl
8882871dbfc0b9469b695dd7416df8cdea59357ac0043bdb85cef5638c9c2869  results/fixed_u_dynamic_anchor_obstruction_independent_audit_20260821.json
c62c194be38f69463546feeae8ef28b989624520e6832cf66af1f7e42f3cc5f7  results/fixed_u_dynamic_anchor_obstruction_tame_menu_20260821.json
995077adf48c0e6fe57f770489de4aebfdb6ec4872991e8063438f4517e5056c  results/fixed_u_tame_or_anchor_cegar_20260821.json
d2c8cf5a310e53d695e528c11dc4a2defa916b1c8f0fccf6b5859106f5653147  results/fixed_u_tame_or_anchor_cuts_20260821.jsonl
```

## Exact remaining boundary

Proved false:

1. the universal dynamic one-anchor theorem;
2. the universal tame-menu-or-one-anchor correction; and
3. on the second obstruction, the fixed `gq`-pattern plus one-extra-anchor
   correction.

Not refuted:

1. the four-edge EFX conclusion for either concrete profile;
2. a pattern-dependent mixed menu whose anchor choice varies by witness side;
3. a two-anchor or two-wild-split realization-free theorem;
4. the universal fixed-`U` theorem; or
5. general additive EFX.

The next exact target is a **pattern-dependent mixed-menu theorem**: allow each
tame witness-side cell to choose its own anchor role/observer/topology, and if
that fails, require an unrestricted two-split-role certificate before widening
again.

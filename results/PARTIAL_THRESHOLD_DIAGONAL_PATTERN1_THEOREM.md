# Diagonal pattern 1 global-improvement theorem

## Theorem

Consider positive additive valuations for four agents and nine goods.  Fix the
canonical eligible partial allocation

\[
01\mid23\mid45\mid67;\qquad f=8,
\]

with strict owner minima \(1,3,5,7\).  For the four completions obtained by
inserting good 8 into hosts \(0,1,2,3\), require the deficient observer pairs

\[
\{0,3\},\quad\{0,1\},\quad\{1,2\},\quad\{2,3\}
\]

to see exactly their corresponding host bundle.  Fix the 24 remaining
off-host edge values to the recorded boundary profile.  Order the eight free
host-edge values as

\[
(0,1),(0,2),(1,2),(1,3),(2,0),(2,3),(3,0),(3,1)
\]

and set their bit pattern to 1: the first edge is present and the other seven
are absent.

Then the canonical partial allocation cannot simultaneously be a global
maximum of normalized owner-threshold potential and have every eligible
fixed-core token permutation fail EFX completion.  Equivalently, at a global
threshold maximum in this edge cell, some eligible permutation of tokens
\(1,3,5,7,8\) over fixed cores \(0,2,4,6\) admits an EFX completion.

## Exact certificate

The exact rational CEGAR certificate is UNSAT with:

- 65 global-maximality cuts;
- 116 individual EFX-completion matching blockers;
- 50 cumulative adversarial iterations; and
- no solver timeout or unknown result.

A fresh staged reconstruction independently reproduced the complete ordered
cut pools and the UNSAT verdict in 374.16 seconds.  A one-shot Z3 replay and
an independent cvc5 replay each timed out at 600 seconds without a verdict;
they are recorded as UNKNOWN and are not counted as confirmations.

Every global cut has the form

\[
\operatorname{eligible}(Y)\Longrightarrow
\Theta(Y)\leq\Theta(X).
\]

The Hall-completable annotations record the valuation at which a cut was
discovered; they are not used in the final formula.  Every individual
completion blocker is guarded by eligibility of its token state and negates
one exact host/permutation EFX matching.

All 65 global witnesses are connected transfers from the canonical base.  Of
these, 18 have owner distance two, 28 distance three, and 19 distance four.
At distance four, four witnesses use a connected three-owner transfer graph
and 15 use all four owners.

The Hall-selector and explicit-matching encodings have also been compared
against literal perfect-matching enumeration on all 480 host completions of
each of two audit profiles.  All 960 checks agree exactly.

## Why this is useful

The earlier four-host theorem fixed all 64 edge truth values.  This theorem
changes one of the eight diagonal host-edge values while retaining only the
source's 24 off-host values, so it proves that the global-improvement mechanism
survives a genuine edge-cell perturbation.  The proof pool also supplies a
short, connected menu for analytic extraction: no witness moves more than four
goods, and no witness splits into independent transfer components.

## Claim boundary

This is one exact diagonal pattern out of 256 in one fixed off-host edge
profile.  It does not prove the entire eight-switch subcell, the cyclic
pair-Hall cell, arbitrary-core four-agent EFX, or general EFX.  In particular,
pattern 2 remains computationally unresolved, and the 24 off-host edge
equalities have not been derived from pair-Hall blockage.

## Reproduction

Certificate:

`results/minimum_slot_orbit_diagonal_pattern1_global_witness_cegar_session3.json`

SHA-256: `c323d04cd29e504bf323208ca88ea09525d8f6e4e98cd6533250180403df9213`.

Fresh staged replay:

`results/minimum_slot_orbit_diagonal_pattern1_global_witness_cegar_staged_replay.json`

SHA-256: `efe0a6f9981b02bf68b81e21ae02c5c8421b0e60889fa31823e3638b33522bb9`.

Replay audit:

`results/minimum_slot_orbit_diagonal_pattern1_global_witness_cegar_replay_audit.json`

SHA-256: `d1a3b7e83491712f3b781437a2c4d792d6d68cfb4bd8e0bec8b78b0ef9d48ec0`.

Component audit:

`results/minimum_slot_orbit_diagonal_pattern1_global_witness_cegar_component_audit.json`

SHA-256: `0aa3c8d908552f7902bfe13983a7c1d861c2136ffbffae322290943f1c458a88`.

Replay command:

```sh
python tracks/parkability/run_minimum_slot_orbit_cegar.py \
  --timeout-seconds 300 --max-iterations 100 \
  --seed results/minimum_slot_orbit_diagonal_pattern1_global_witness_cegar_session1.json \
  --relabeling-mode cyclic --completion-batch-size 8 \
  --completion-cut-mode witness --global-witness-mode hall_insertable \
  --base-host-pair-hall-cycle \
  --base-host-offhost-edge-cell-source \
    results/minimum_slot_orbit_hall_state_nearest_cegar_session2_orbit_blocked_seed.json \
  --base-host-diagonal-pattern 1 \
  --output /tmp/minimum-slot-diagonal-pattern1-staged-replay.json
```

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

## Cyclic corollary

The fixed 24-bit off-host edge profile is invariant under simultaneous cyclic
relabeling of agents, cores, tokens, hosts, and assigned bundles.  Under one
cyclic shift, diagonal bit positions are permuted as

\[
0\to2\to5\to6\to0,
\]

so the theorem transfers without another solver assumption to diagonal
patterns

\[
\{1,4,32,64\}.
\]

The original exact host-edge theorem covers pattern 0.  Hence five exact
diagonal profiles in this fixed off-host subcell are now closed.  The other
single-bit orbit is \(\{2,8,16,128\}\); none of those four cells is proved by
this symmetry argument.

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

## Preferred 52-cut finite-menu core

A separately tracked exact run returned UNSAT with 77 global cuts and 73
matching blockers.  Z3's raw UNSAT core retains only:

- 49 global-improvement cuts; and
- 27 individual completion-matching blockers.

Repeated tracked extraction and Z3 core minimization reduce that certificate
to 52 guarded consequences: 27 global-improvement cuts and 25 individual
completion blockers.  A fresh standalone, untracked reconstruction returns
UNSAT in 98.91 seconds.  QF_LRA-specialized Z3 returns UNSAT in 90.99 seconds,
and independently parsed cvc5 1.3.4 returns UNSAT in 128.23 seconds.  A
dual-replay audit checks the cut lists, raw and normalized SMT-LIB hashes, and
all three verdicts.

The replay now expands every EFX maximum comparison into its literal pairwise
inequalities.  This is logically equivalent and gives a cleaner analytic
object.  It also exposes an important export guard: tracked assertions are
never emitted as standalone SMT-LIB because their tracker literals would not
otherwise be forced.

All 27 retained global witnesses are connected.  They split exactly into 12
two-owner swaps and 15 four-owner cycles; no three-owner transfer remains.
Across the four cyclically related pattern cells, the core has eight exchange
templates and 15 completion-failure templates.  The exact finite-menu
alternative and its human-proof target are stated in
`PARTIAL_THRESHOLD_DIAGONAL_FINITE_MENU_LEMMA.md`.  The 52-cut core is
solver-minimized but has not been independently proved inclusion-minimal.

## Why this is useful

The earlier four-host theorem fixed all 64 edge truth values.  This theorem
changes one of the eight diagonal host-edge values while retaining only the
source's 24 off-host values, so it proves that the global-improvement mechanism
survives a genuine edge-cell perturbation.  The proof pool also supplies a
short, connected menu for analytic extraction: no witness moves more than four
goods, and no witness splits into independent transfer components.

## Claim boundary

This is one cyclic orbit of four exact diagonal patterns out of 256 in one
fixed off-host edge profile.  It does not prove the entire eight-switch
subcell, the cyclic pair-Hall cell, arbitrary-core four-agent EFX, or general
EFX.  Pattern 2 and its cyclic orbit are now closed by the separate theorem in
`PARTIAL_THRESHOLD_DIAGONAL_PATTERN2_THEOREM.md`; multi-bit patterns remain
unclassified, and the 24 off-host edge equalities have not been derived from
pair-Hall blockage.

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

Cyclic-symmetry audit:

`results/minimum_slot_orbit_diagonal_pattern1_symmetry_audit.json`

SHA-256: `6bbe358207bcc03132f5f5ffa3c8e58b8726a64f7312712a90f09bae18e744fa`.

Tracked core derivation:

`results/minimum_slot_orbit_diagonal_pattern1_global_witness_cegar_core_session1.json`

SHA-256: `f652b998c94544f9b7e17b2cd86de21cd7eb450138e84921689ec31d7d10e395`.

Extracted 76-cut pool:

`results/minimum_slot_orbit_diagonal_pattern1_unsat_core_pool.json`

SHA-256: `ca2f8a86151a1a37456b5473acaa4d8d25d9aeb7ad5d982f9e0173b97b6ed000`.

Fresh one-check core replay:

`results/minimum_slot_orbit_diagonal_pattern1_unsat_core_replay.json`

SHA-256: `c40d037a3680b0e7f46f2aff0482c62f55bb210dd67222466cc9146fd5cabde7`.

Core replay audit:

`results/minimum_slot_orbit_diagonal_pattern1_unsat_core_replay_audit.json`

SHA-256: `135dbc713348ea3a8694ba652ab8066d9f37ef83f7d9b88190a6978efa148d0d`.

Core component and quotient audits:

- `results/minimum_slot_orbit_diagonal_pattern1_unsat_core_component_audit.json`,
  SHA-256 `9486d9b83b73ad6a6c7a7b09b6ef4f8a0e6d395530ebfd9eb3c11472be33004f`;
  and
- `results/minimum_slot_orbit_diagonal_pattern1_unsat_core_quotient_audit.json`,
  SHA-256 `4394b3735d4655581963d8ca0585942e3b539f7595996310672b898a05d5329f`.

Independent replay bundle:

- `results/minimum_slot_orbit_diagonal_pattern1_unsat_core_qflra_replay.json`,
  SHA-256 `305db5a8ddfe8a11db87cece15af66f091054a950c34015a515cc3e6d2378d63`;
- `results/minimum_slot_orbit_diagonal_pattern1_unsat_core.cvc5.json`,
  SHA-256 `68906b86c7118fdf6af574535db2223e52c3d003490209900b37379d30e5bef8`;
- `results/minimum_slot_orbit_diagonal_pattern1_unsat_core.normalization.json`,
  SHA-256 `9ad49e0cd65a73daf014e6744eba883506d0c40389650de237999b62ce186442`;
  and
- `results/minimum_slot_orbit_diagonal_pattern1_unsat_core_dual_replay_audit.json`,
  SHA-256 `aee629a43e9ad83f628caa0cad12d9ebc699e9f0cb9a44abd0eb5f7137d2418b`.

Preferred 52-cut bundle:

- `results/minimum_slot_orbit_diagonal_pattern1_unsat_core_pool_v5.json`,
  SHA-256 `31195d09b7587d74b43e818aa08bbe8727973917b839ef73de50b4b3a66f59dc`;
- `results/minimum_slot_orbit_diagonal_pattern1_unsat_core_untracked_replay_v5.json`,
  SHA-256 `7b4cbbd0f19f21f89e6dfecce4af600c6f85ee5640058ea5662d4352a6b2479b`;
- `results/minimum_slot_orbit_diagonal_pattern1_unsat_core_untracked_replay_audit_v5.json`,
  SHA-256 `d643a4de8ac4c2a992b46dd132bbc806c2f37ad6d4008be944fc220ddae3ba49`;
- `results/minimum_slot_orbit_diagonal_pattern1_unsat_core_component_audit_v5.json`,
  SHA-256 `66a6eec6a27b6c1dbdc5c781d677210b2097a9ca2bdae291d987e0a2ff8aa1f6`;
- `results/minimum_slot_orbit_diagonal_pattern1_unsat_core_quotient_audit_v5.json`,
  SHA-256 `048a93959fa5aa561614e1b564264fc66fa2520b973d1386c5d578611640d8ae`;
- `results/minimum_slot_orbit_diagonal_pattern1_unsat_core_v5_untracked.normalized.smt2`,
  SHA-256 `b5a9ddc5ab1b0aab5ebbb13f1abbe43ab3cf964e993eb3a20830a86df02cb372`;
- `results/minimum_slot_orbit_diagonal_pattern1_unsat_core_v5_untracked.cvc5.json`,
  SHA-256 `ba04d58b04437b65f40dbf90014fe551edf1f89a964385d845def76e180d4c80`;
  and
- `results/minimum_slot_orbit_diagonal_pattern1_unsat_core_dual_replay_audit_v5.json`,
  SHA-256 `bf97a9b5a064517abf70b474df684e639397b28a39af814e0c9cb40fce589cb4`.

Preferred replay command:

```sh
python tracks/parkability/run_minimum_slot_orbit_cegar.py \
  --timeout-seconds 300 --max-iterations 1 \
  --seed results/minimum_slot_orbit_diagonal_pattern1_unsat_core_pool_v5.json \
  --relabeling-mode none --completion-batch-size 8 \
  --completion-cut-mode witness --global-witness-mode hall_insertable \
  --base-host-pair-hall-cycle \
  --base-host-offhost-edge-cell-source \
    results/minimum_slot_orbit_hall_state_nearest_cegar_session2_orbit_blocked_seed.json \
  --base-host-diagonal-pattern 1 \
  --output /tmp/minimum-slot-diagonal-pattern1-core-replay.json
```

Full staged reconstruction command:

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

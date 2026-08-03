# Diagonal finite exchange-menu lemma

## Exact lemma

Use the canonical pair base

\[
B=01\mid23\mid45\mid67;\qquad f=8
\]

and all hypotheses of diagonal pattern 1 in
`PARTIAL_THRESHOLD_DIAGONAL_PATTERN1_THEOREM.md`: positive normalized additive
valuations, eligibility of \(B\), strict owner minima \(1,3,5,7\), the cyclic
pair-Hall witnesses, the fixed 24 off-host edges, and diagonal bit pattern 1.

There are explicit finite menus \(G\) and \(C\), stored in
`minimum_slot_orbit_diagonal_pattern1_unsat_core_pool_v5.json`, with:

- 27 connected exchange allocations in \(G\); and
- 25 specified token-state/host/matching completions in \(C\).

Assume also the minimum-slot plateau consequence: whenever a permutation of
tokens \(1,3,5,7,8\) over cores \(0,2,4,6\) is eligible, every incoming owner
token is weakly below that owner's core good.  Then at least one of the
following holds:

1. a specified member of \(C\) has an eligible token state and its specified
   complete allocation is EFX; or
2. a member \(Y\in G\) is eligible and
   \(\Theta(Y)>\Theta(B)\).

Consequently, if \(B\) globally maximizes normalized owner-threshold
potential, one of the 25 specified completions is EFX.  Global maximality
implies the plateau consequence by the minimum-slot permutation lemma and
rules out the second alternative.

## Exchange structure

All 27 members of \(G\) are balanced two-good allocations obtained from \(B\)
by one connected directed transfer cycle.  They split into:

- 12 two-owner swaps;
- 15 four-owner cycles.

Write \(a_i=2i\) for the core good and \(b_i=2i+1\) for the owner-minimum
token.  Quotienting the four cyclically related pattern cells gives eight exchange
types:

- three adjacent-swap types;
- five backward four-cycle types.

For the canonical representatives, the directed cycles move goods toward the
previous owner.  The four-cycle menu uses

\[
(b_0,a_1,a_2,a_3),
(b_0,a_1,a_2,b_3),
(b_0,a_1,b_2,a_3),
(b_0,a_1,b_2,b_3),
(a_0,a_1,a_2,a_3).
\]

This is the concrete cancellation pattern to target in a human proof: failed
specified completions should force a strict positive sum around one of these
cycles, while eligibility makes that cycle admissible.

## Exact proof and interpretation

For every \(Y\in G\), negate alternative 2 by imposing

\[
Y\text{ eligible}\Longrightarrow\Theta(Y)\leq\Theta(B).
\]

For every member of \(C\), negate alternative 1 by imposing that eligibility
of its token state implies failure of at least one observer's assigned EFX
inequality.  Together with the fixed cell and plateau hypotheses, these 52
guarded consequences are exactly UNSAT over the rationals.

The completion failures can be written without a maximum operator:

\[
v_i(A_{\pi(i)})<
\max_{j\ne\pi(i)}\tau_i(A_j)
\quad\Longleftrightarrow\quad
\bigvee_{j\ne\pi(i)}
v_i(A_{\pi(i)})<\tau_i(A_j).
\]

Likewise, each EFX edge is the conjunction of its three literal pairwise
threshold inequalities.  This direct form is now used by the replay code and
is the preferred starting point for an inequality proof.

## Analytic conversion target

For a directed exchange cycle in which owner \(i\) sends one of
\(\{a_i,b_i\}\), let \(r_i\) be its retained good and \(q_i\) its incoming
good.  Its exact threshold-potential change is

\[
\Delta=
\sum_i\left(
\max\{v_i(r_i),v_i(q_i)\}-v_i(a_i)
\right).
\]

If an owner sends \(b_i\), it retains \(a_i\), so its summand is nonnegative.
Only owners sending their core \(a_i\) can contribute a loss.  The remaining
human-proof task in this cell is therefore sharply defined: use the literal
failure inequalities from the 25 completion menu to show that one of the eight
cycle types is eligible and that its nonnegative token-sender gains strictly
exceed its core-sender losses.

## Claim boundary

This is an exact finite-menu lemma for one fixed off-host edge profile and one
diagonal-pattern orbit.  Its present proof is solver-certified, not yet a
shorthand proof.  The cyclic quotient organizes corresponding cuts across
four related pattern cells; it does not make a single representative imply
all cuts inside pattern 1.  The lemma does not remove the fixed off-host
edges, settle the other single-bit orbit, cover arbitrary four-agent cores,
or prove general EFX.

## Reproduction

- Core pool: `minimum_slot_orbit_diagonal_pattern1_unsat_core_pool_v5.json`,
  SHA-256 `31195d09b7587d74b43e818aa08bbe8727973917b839ef73de50b4b3a66f59dc`.
- Standalone replay audit:
  `minimum_slot_orbit_diagonal_pattern1_unsat_core_untracked_replay_audit_v5.json`,
  SHA-256 `d643a4de8ac4c2a992b46dd132bbc806c2f37ad6d4008be944fc220ddae3ba49`.
- Exchange-component audit:
  `minimum_slot_orbit_diagonal_pattern1_unsat_core_component_audit_v5.json`,
  SHA-256 `66a6eec6a27b6c1dbdc5c781d677210b2097a9ca2bdae291d987e0a2ff8aa1f6`.
- Cyclic quotient audit:
  `minimum_slot_orbit_diagonal_pattern1_unsat_core_quotient_audit_v5.json`,
  SHA-256 `048a93959fa5aa561614e1b564264fc66fa2520b973d1386c5d578611640d8ae`.
- Dual-solver audit:
  `minimum_slot_orbit_diagonal_pattern1_unsat_core_dual_replay_audit_v5.json`,
  SHA-256 `bf97a9b5a064517abf70b474df684e639397b28a39af814e0c9cb40fce589cb4`.

Shortest standalone replay:

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
  --output /tmp/minimum-slot-diagonal-pattern1-core-v5-replay.json
```

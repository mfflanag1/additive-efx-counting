# Rooted three-good transfer refutation

**Date:** 2026-08-10

**Status:** exact bounded refutation of the selected-replacement-rooted
strengthening; unrestricted connected radius three remains open

## Refuted strengthening

In the representative two-atom full-capture flower cell, let `q` be the
later mutual-cycle owner and let `g in X_q` satisfy `v_q(f)>v_q(g)`, as
guaranteed cap-free by the later-owner selector lemma.  Consider every
connected redistribution of at most three goods that contains both moves

\[
f:\mathrm{charity}\to q,
\qquad
g:q\to\mathrm{charity}.
\]

It is false that one of these rooted transfers must preserve `r`, strictly
improve `q`, and maintain EFX with charity.

## Exact countermodel

The symbolic full-capture master blocks all 78 structurally feasible rooted
allocations and remains SAT.  In the resulting positive-additive valuation,
the nearest unrestricted flexible endpoint moves only two goods, but bypasses
the selected replacement entirely.  Its transfer signature is

\[
c\to q,
\qquad
q\to c.
\]

Thus the obstruction is not transfer radius or connectedness.  It is the
attempt to force every repair to contain the analytically selected
`f`-for-`g` move.

## Consequence for the breakthrough target

The mechanism-independent lemma must quantify over all connected
redistributions directly.  It cannot first select the charity replacement
and then prove that one additional incident move repairs it.  Bilateral
swaps, owner paths, and directed owner cycles are genuine alternative
mechanisms, not merely response edges attached to the selected replacement.

The unrestricted radius-three decision contains 6,738 candidates after
exact positivity reductions.  A direct QF_LRA run was interrupted cleanly
as `unknown`; neither a countermodel nor an UNSAT result is claimed for that
larger statement.

## Verification

The source model is
[`flexible_later_owner_rooted_connected_transfer_refutation.json`](flexible_later_owner_rooted_connected_transfer_refutation.json).
The exact-Fraction replay
[`flexible_later_owner_rooted_connected_transfer_refutation_audit.json`](flexible_later_owner_rooted_connected_transfer_refutation_audit.json)
checks the flower axioms, all common-safe-cover failures, all 78 rooted
allocations, and the displayed two-good escape.

Z3 4.15.3 and 5.0.0 independently return SAT models for the same 78-candidate
gate.  Their rational models are not byte-identical, but both pass the same
solver-free exact-Fraction audit and expose the same bilateral-swap escape
signature.

Replay with:

```sh
python tracks/parkability/audit_flexible_later_owner_rooted_connected_transfer_refutation.py \
  --source results/flexible_later_owner_rooted_connected_transfer_refutation.json \
  --output /tmp/rooted-connected-transfer-audit.json
cmp results/flexible_later_owner_rooted_connected_transfer_refutation_audit.json \
  /tmp/rooted-connected-transfer-audit.json
```

This is a bounded proof-mining refutation.  It does not refute the
unrestricted connected-radius-three lemma, the cap-free flower theorem, or
existence of EFX allocations.

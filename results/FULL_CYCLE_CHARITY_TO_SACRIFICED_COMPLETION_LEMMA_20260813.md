# Full-cycle charity-to-sacrificed completion lemma

**Date:** 2026-08-13

**Status:** cap-free all-non-d payment closure for both response forms; one
sacrificed-owner deficit remains

**Boundary update:** this is a conditional endpoint, not an exhaustive
selector. Its topologies are included in the exact refuted family documented
in `TWO_SURVIVOR_NAMED_TOPOLOGY_SELECTOR_REFUTATION_20260813.md`.

**R2 simplification:** the transfer `d -> s` is unnecessary because `s` is
already paid.  The sharper construction in
`PAID_CYCLE_CHARITY_TO_SACRIFICED_LEMMA_20260813.md` retains `s`, uses only
three edges, and leaves the bare `v_d(W)+v_d(p)-v_d(X_d)` margin in both
response forms.

## Two-cycle endpoint

Rotate the `r <-> q` response cores, give `s` its desired core from `Y_d`,
and give singleton charity to `d`. The transfer edges are

\[
 q\to r,\quad r\to q,\quad d\to s,
 \quad\text{charity}\to d.                        \tag{1}
\]

Owners `r,q,s` are strictly paid. If `C_s subseteq Y_d` is the core sent to
`s`, d's exact margin is

\[
 m_d=\Delta_d-v_d(C_s)+v_d(p).                    \tag{2}
\]

## Three-cycle endpoint

Rotate the entire paid `r -> q -> s -> r` cycle and give singleton charity
to `d`. This again uses four edges. Owners `r,q,s` are strictly paid and d
keeps all of `W`, so

\[
 m_d=\Delta_d+v_d(p)
     =v_d(W)+v_d(p)-v_d(X_d).                     \tag{3}

Failure is the bare residual deficit

\[
 v_d(W)+v_d(p)<v_d(X_d).                          \tag{4}

## Consequence

Together with the represented-owner endpoint branches, the universal gate
has now separated into explicit scalar failures. In the two-cycle form, the
d-endpoint failure is a lost-W-core capture. In the three-cycle form it is
exactly (4). Any unsafe enlarged target remains a saturated response/support
exit rather than a new topology case.

## Verification and boundary

[`audit_full_cycle_charity_to_sacrificed_completion.py`](../tracks/parkability/audit_full_cycle_charity_to_sacrificed_completion.py)
independently checks both constructions, conservation, the four-edge bound,
and all payment/capture identities in QF-LRA.

It does not prove d's margin is nonnegative or establish final observer
safety, so it does not finish the universal theorem.

# Seven-endpoint payment-strengthening no-go

**Date:** 2026-08-14

**Status:** corrected minimized-core shortcut no-go; every profile has another
generalized PI, so the fully PI-free payment question remains open

The minimized 425-clause seven-endpoint certificate cannot by itself be
strengthened merely by requiring that its EFX endpoint preserve enough
base-owner floors. Exact positive-rational profiles satisfying that reduced
exclusion core show all of the following.

1. No endpoint need be both EFX and all-owner-paid.
2. No endpoint need be EFX while paying the fixed owners `r,q,s` (allowing
   only `d` to be the payment hole).
3. No endpoint need be EFX with at most one payment hole.
4. No endpoint need be EFX with at most two payment holes.

The fourth profile has `Z5` EFX while `r,q,d` are all slightly below their
base floors; only `s` is paid. However, the full generalized-PI oracle finds
another closed disjoint-core family in every one of the four profiles. They
therefore do **not** refute the stronger statement restricted to fully
generalized-PI-free states. They prove only that the 425-clause minimized core
omits information needed for such a payment strengthening.

Sources:

- `allocated_e_form2_seven_endpoint_paid_strengthening.json`;
- `allocated_e_form2_seven_endpoint_d_hole_strengthening.json`;
- `allocated_e_form2_seven_endpoint_single_hole_strengthening.json`;
- `allocated_e_form2_seven_endpoint_two_hole_strengthening.json`.

Each is replayed by
`tracks/parkability/audit_allocated_e_paid_strengthening_counterprofile.py`
using exact `Fraction` arithmetic for every PI clause, endpoint EFX test, and
payment count, plus a fixed-profile replay of the complete master and a full
generalized-PI census. The ongoing decisive test uses the complete 46,683-cut
PI pool rather than the minimized core.

## Claim boundary

These witnesses refute only derivation of the listed payment strengthenings
from the minimized 425-clause core. They do not refute those strengthenings
under full generalized-PI-freeness, complete EFX, four-agent EFX, or general
EFX.

# Root singleton supplier-star floor-reset closure theorem

**Referee downgrade (2026-08-16).** Independent adversarial referee round
returned **GAP FOUND** on this closure: S3 (registry admissibility of the
controlled floor reset) is asserted, not derived; S4 (a well-founded descent
coordinate) is not addressed; the claimed progress form is excluded by the
frozen contracts `AUG14_COLLISION_CANDIDATE_TRANSITION_ADMISSIBILITY_AUDIT
_20260814.md:44-49` and `RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT
_20260813.md:102-103`; and the supporting audit scripts verify provenance,
not content. The nonroot-holder branch is unaffected. Status is downgraded to
**conditionally closed on admissibility of the controlled floor reset**. Do
not quote externally. Full report:
[`TLX_CLOSURE_REFEREE_REPORT_20260816.md`](TLX_CLOSURE_REFEREE_REPORT_20260816.md).

**Model-check update (2026-08-16, later same day).** The successor-state model
checker (`TLX_SUCCESSOR_MODEL_CHECK_20260816.md`, 233,030 instances / 35.9M
successor configurations) CONFIRMS referee findings G2, G3 and G7 with
concrete witnesses, and additionally REFUTES closure equation (5) outright
under its own minimisation quantifier (the singleton target `{k}` is desired
by any emptied owner, so `D={k}` is a legal globally minimum response with
`D∩K ⊄ K−k`; the closure needs `D ⊆ G−k` as an explicit hypothesis).
Sharpest finding: the packet coordinate descends on EXACTLY the `L_α = K`
slice (1,803,708/1,803,708) and NEVER off it (0/34,072,500), where the
contract's other declared coordinate (hitting multiplicity) strictly
INCREASES. Honest status: **closed on the `L_α = K` slice, open otherwise;
route recommended for retirement** — the sole repair would be proving
`L_α = K` in the root-holder branch, and the nonroot branch's own claim
boundary disclaims the same slice from the opposite side. Verdicts are
conditional on witness reachability (the checker searches a superset of
genuine `T_{L,×}^*` states; see simplification S1 in the model-check report).

**Date:** 2026-08-14

**Status (superseded 2026-08-16, see referee downgrade above):** cap-free
closure of every root-held retired-packet collision under
the frozen anchored `GG` import

## Exact root-holder input

Let an exact `T_{L,times}^*` state have the protected first-priority root `r`
as current holder of the named nonempty retired packet `K`. Retain the
globally maximal EFX base `X`, put `x=v_r(X_r)`, and let

\[
 O=G\setminus X_r.
\]

The frozen physical anchor label retains the old common-safe desired root
core

\[
 A=T_q+f\subseteq O,
 \qquad v_r(A)>x.                                \tag{1}
\]

The selected top packet `T_q` is nonempty, so `A` contains at least two
goods. No criticality, current-root minimality, recipient margin, or
historical return premise is needed below.

## Every singleton supplier star is root-strict

Choose any `k in K`. Consider the root target `G-k`. Its margin over the
base is

\[
 v_r(G-k)-x=v_r(O)-v_r(k).                      \tag{2}
\]

This margin is strictly positive in both support cases.

1. If `k in X_r`, positivity gives `v_r(k)<=x`, while (1) gives
   `v_r(O)>=v_r(A)>x`. Hence `v_r(O)>v_r(k)`.
2. If `k in O`, then `O-k` is nonempty. If `k notin A`, it still contains
   `A`; if `k in A`, it contains the nonempty packet `A-k`. Positivity gives
   `v_r(O)-v_r(k)=v_r(O-k)>0`.

Therefore

\[
 v_r(G-k)>x                                      \tag{3}
\]

for every possible retired atom `k`, including an atom of the critical old
anchor.

## Controlled reset allocation

Let `u != r` be the named nonroot sacrifice row. Form the complete physical
allocation

\[
 Y_r=G-k,
 \qquad Y_u=\{k\},
 \qquad Y_j=\varnothing\quad(j\notin\{r,u\}),   \tag{4}
\]

with empty charity. Every good entering the root is supplied by its actual
current holder, and the root supplies `k`. Every other retirement collision
and the new physical root-support label is appended to the signed record; no
PI edge or historical reversal is inferred.

Apply the strict first-priority floor-reset theorem at (4). Reset each
current auxiliary floor to the utility of the displayed assigned bundle,
retain the immutable base certificate and all physical labels, and recompute
every EFX comparison. This is the controlled reset missing from the earlier
global supplier-star proof. The reset itself is not counted as progress;
progress below is the strict packet-intersection change.

## Exhaustive EFX boundary and packet reduction

If (4) is EFX, (3) contradicts global fixed-priority maximality. Suppose it
is not EFX. Empty targets cannot be strongly envied. The singleton target
`{k}` cannot be strongly envied because deleting its only good leaves the
empty bundle. Thus every EFX wall is against `G-k`.

Choose a globally minimum desired response `D subseteq G-k` at the actual
allocation. The floor-reset theorem makes `D` a safe exact response. Its
retired intersection satisfies

\[
 D\cap K\subseteq K-k\subsetneq K.              \tag{5}
\]

Hence the adopted allocation/response has strictly smaller collision
hitting support. A simultaneously exposed second retirement label is kept
in the signed record, but cannot put `k` into `D`; restoring the old whole
`K` hit would require a separately recorded later collision.

This is outcome 4 of the charge-or-anchor contract. It does not rely on the
invalid claim that the old nonroot floors survived (4).

## Typed branches

- **Strict capture:** (3)--(5) use no recipient surplus or holder
  compensation inequality.
- **Equality-critical payment:** neither recipient equality nor root
  equality survives; the root is strict by physical support and positivity.
- **Base-floor debt:** all later floors are explicitly reset at (4), while
  the immutable first-priority root certificate remains strict.
- **Release compatibility:** (4) is a complete current-holder supplier star,
  not a PI claim. Every moved good has one supplier and one destination.
- **Normalization bypass:** the actual named packet and bypass response
  record enter the same support reduction (5); no canonical historical
  return is used.

## Consequence

The nonroot-holder branch is closed by the desire-free safe-envelope descent.
The present theorem closes the exhaustive root-holder branch. Consequently
the retired-packet charge-or-anchor-exchange theorem is proved for the full
collision subtype `T_{L,times}^*`.

## Claim boundary

This theorem closes `T_{L,times}^*` under the frozen anchored `GG` import. It
does not close the parked-support subtype `T_{L,perp}^*`, the empty-ledger
subtype `T_0^*`, the full `GG` class, the other selected-cycle classes,
four-agent EFX, or general additive EFX. The new controlled-reset operation
and this composition require independent statement/encoding audit and
external expert review before publication-level promotion.

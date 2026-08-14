# Current-wall charity-retarget-or-unanimous-capture lemma

**Date:** 2026-08-13

**Status:** cap-free second endpoint for the R3 current-wall capture; final
two-row polarity/observer safety remains

## Terminal state

Use the nonsingleton current-wall backward-hole terminal. Let `D` be the
current-safe root core assigned toward `d`, and let `H subseteq D` be the
packet retained by physical root owner `r`. Write `B` for every other good
in `r`'s terminal bundle. The original terminal bundles are

\[
 Z_d=W+(D\setminus H)+P,
 \qquad Z_r=B+H.                                  \tag{1}
\]

Assume `r` is paid and `d` is not:

\[
 v_r(B+H)\ge F_r,
 \qquad v_d(W+D-H+P)<F_d.                         \tag{2}
\]

The half-floor lift also gives

\[
                         v_d(W+D)>F_d.            \tag{3}

## Charity retarget

Send the retained packet `H` to `d` along the already present root-to-`d`
pair and retarget charity `P` from `d` to `r`. The only changed bundles are

\[
 Z'_d=W+D,
 \qquad Z'_r=B+P.                                 \tag{4}

Conservation is exact. The owner-transfer graph is unchanged—the packet on
`r->d` is merely enlarged from `D-H` to `D`—and the single charity edge
changes recipient from `d` to `r`. Thus the operation remains within the
same three owner pairs plus one charity pair.

By (3), `d` is strictly base-paid in (4). Therefore exactly one of the
following occurs.

1. **Retargeted payment:** `v_r(B+P)>=F_r`. Then every owner is paid in the
   retargeted four-edge candidate.
2. **Unanimous retained-packet capture:** `v_r(B+P)<F_r`. Combining this
   with (2) gives

   \[
   v_r(H)>v_r(P).                                 \tag{5}
   \]

   Combining (2) with (3) gives independently

   \[
   v_d(H)>v_d(P).                                 \tag{6}
   \]

Hence failure of the retargeted endpoint forces both owners incident to the
root/charity exchange to rank the retained packet strictly above charity.

## Exact remaining boundary

The four-edge owner-payment problem in the nonsingleton current-wall branch
is now reduced from an arbitrary mixed margin to the explicit two-row
polarity (5)--(6). The retained packet is also full-value base-safe because
`H subseteq D` and the half-floor core has that property for every
non-source observer (and value at most `F_d` in the source row).

The lemma does not prove observer safety of either complete candidate or
show that unanimous dominance alone yields generalized PI. The next proof
must combine (5)--(6) with the base provenance of `H`, the owner receiving
the displaced response core, and saturation of charity-blocker responses.

[`audit_current_wall_charity_retarget_or_unanimous_capture.py`](../tracks/parkability/audit_current_wall_charity_retarget_or_unanimous_capture.py)
independently verifies conservation, edge-count preservation, retargeted
payment, and both strict polarity implications.

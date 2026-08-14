# Endpoint-6 two-probe `H`-relay closure theorem

**Dependency correction (2026-08-14):** the imported claim that all
`T_{L,times}^*` states are closed has an uncovered nonroot-holder
normalization-bypass case when the repeated ledger-free response avoids
`H`; see `NONROOT_NORMALIZATION_BYPASS_COLLISION_GAP_20260814.md`.  This
document proves the two-probe reduction and exact collision premise map, but
does not currently prove that one probe is EFX unless that missing branch is
closed or a local argument forces the normalized response to hit `H`.

**Date:** 2026-08-14

**Status:** cap-free reduction of the endpoint-6 recurrent branch to the
unproved nonroot normalization-bypass subtype; the paid/sacrificed relay
admission is separately proved

## Two explicit probes

At the physical endpoint-6 support state

\[
Y=(A+H,Q,W,E;P),                                 \tag{1}
\]

test, in order,

\[
\begin{aligned}
C_d&=(A,Q,H+L+W,(E-L)+P),\\
C_s&=(A,Q,L+W,H+(E-L)+P).
\end{aligned}                                    \tag{2}
\]

Both are complete.  Relative to (1), their support edges are

\[
\begin{array}{c|c}
C_d&c\to s,\ r\to d,\ s\to d,\\
C_s&c\to s,\ r\to s,\ s\to d.
\end{array}                                      \tag{3}
\]

Thus either EFX endpoint uses exactly three edges, below the requested
four-edge bound.  Relative to `C_d`, the second probe changes only the holder
of `H`:

\[
H:d\longrightarrow s.                            \tag{4}
\]

## Admission and payment

The endpoint-6 hard premises force all four owners to be base-paid at `C_d`.
They force `r,q,s` to be base-paid at `C_s`; only `d` may be below base.
The root receives the same strict packet `A` in both probes.  Therefore:

- `C_d` is an all-paid candidate in the fixed-`U` paid-candidate phase;
- `C_s` is a priority-valid one-sacrificed-owner candidate in the
  sacrificed-hole phase; and
- neither probe assumes its own EFX conclusion.

These are the two admission classes explicitly retained by the frozen
fixed-`U` continuation.  The second is independently established by
`SACRIFICED_H_RELAY_ADMISSION_LEMMA_20260814.md`: if `d` becomes unpaid,
`H` strictly captures its whole base-floor deficit; otherwise `C_s` is
all-owner-paid.  Adding the deterministic order `C_d` then `C_s` is finite
and noncircular: saturation excludes a first unseen probe as strict history
progress.

## Relay argument

If `C_d` is EFX, stop.  Otherwise its all-paid failure yields the exact
current-safe decorated response recorded in the all-paid whole-`H` lemma.
The transition `Y -> C_d` removes the nonempty physical packet `H` from the
protected root and pays its new holder `d`; record `H` in the monotone
retired-support ledger.

Now test `C_s` from that signed state.  Equation (4) attempts to consume the
same retired packet under the same root/anchor label.  The canonical
ledger-free normalization cancels precisely the transfer (4).  Because the
two probes differ nowhere else, the normalized allocation is exactly

\[
C_s^-=C_d.                                       \tag{5}
\]

Thus the normalized EFX test is not an unclassified new allocation: it is
the already failed all-paid probe together with its exact current-safe
decorated response.  If `C_s` itself is EFX, stop.  Otherwise one of the
following exact failures is recorded:

1. `d` fails its protected/base floor after releasing `H`;
2. an EFX comparison fails at the tested complete allocation;
3. a required release/normalization comparison fails; or
4. the resulting response is a new signed record, which is strict finite
   history progress until its first exact repeat.

At a saturated repeat, equation (5) gives the normalization-bypass collision
certificate directly.  Cases 1--3, and case 4 after its first occurrence,
are therefore in `T_{L,times}^*`: the packet, retirement supplier, current
holder, recipient, floors, candidate support, failed normalized test, exact
repeated response, and physical label are all explicit.  This is not the
parked subtype because the second active probe itself intersects `H`.

The companion collision theorem at commit
`34709c9ce22dbde23a5fa381a2ccea7898dfe1ca` excludes every saturated
`T_{L,times}^*` state by controlled floor reset.  Hence, subject to semantic
acceptance of that imported theorem, `C_s` cannot
fail at the saturated endpoint-6 record.  One of `C_d,C_s` is therefore a
complete physical EFX allocation through three packet-transfer edges.

## Consequence and remaining global boundary

This closes the endpoint-6 `Z6` recurrent face that survived root-fixed
exhaustion.  It also eliminates the parked-support escape for this face:
`C_s` is an always-declared active selector that explicitly reactivates the
parked packet `H`.

It does **not** by itself prove the full active fixed-`U` objective.  Promotion
requires a dependency audit showing that every saturated root-facing
rank-three state either reaches this exact endpoint-6 chart, reaches an
already closed `Z1--Z4`/PI/progress branch, or supplies a separately valid
complete EFX endpoint.  It also requires external review of the imported
controlled floor reset and its composition with the separately proved
same-label relay admission.

## Verification

`audit_endpoint6_two_probe_h_relay_closure.py` independently verifies packet
conservation, the two three-edge support graphs, the one-edge relay (4), the
payment rows in the exact endpoint-6 decision, the nonempty-ledger/collision
classification, and the imported theorem identity.

Claimed here: conditional endpoint-6 closure with a complete three-edge EFX
endpoint.  Not yet claimed: unconditional universal fixed-`U` closure,
four-agent additive EFX, or general additive EFX.

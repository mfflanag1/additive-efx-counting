# Endpoint-6 two-probe to `T_{L,times}^*`: premise audit

**Date:** 2026-08-14

**Verdict:** every data premise of the collision contract has an explicit
endpoint-6 witness; relay admission is proved locally, while placement in
the frozen global composition remains external-review critical

## Premise-by-premise map

| Collision-contract datum | Endpoint-6 witness | Status |
|---|---|---|
| globally maximal EFX-with-charity base | frozen saturated fixed-`U` premise | imported |
| first-priority protected root and permanent anchor | root `r`, permanent packet `A` | unchanged in both probes |
| nonempty retired packet | physical packet `H` | nonempty by the packet chart |
| retirement supplier and first holder | `r -> d:H` in `Y -> C_d` | exact |
| retirement-time floor snapshot | all four owners are base-paid at `C_d`; `r` is strict | exact payment decision |
| actual failed tested state | non-EFX `C_d` | branch assumption |
| response at normalized state | globally minimal current-safe/current-desired `D subseteq H+L+W` | cap-free extraction |
| later colliding selector | `C_s` | explicit complete allocation |
| current holder and recipient | `d -> s:H` from `C_d` to `C_s` | exact |
| same physical anchor label | both probes retain root packet `A` and orientation | exact in the chart |
| canonical cancellation | cancel `d -> s:H` | gives `C_s^-=C_d` identically |
| failed normalized EFX test | `C_d` is the already failed probe | exact |
| repeated normalized response | the full signed `C_d,D` record at saturation | exact-repeat premise |
| floor/observer/release separator | `C_s` has only possible base hole `d`; any EFX/release failure is recorded | exact typed split |
| rank-deficient GG state | saturated root-facing rank-three fixed-`U` input | imported |
| finite-history condition | the two probes and their full signed records are fixed | finite |

The collision is specifically the normalization-bypass clause of
`T_{L,times}^*`.  It does not require the new response extracted at `C_s` to
meet `H`: the original selector meets `H`, cancellation restores the already
failed `C_d`, and the exact ledger-free response repeats.

## Relay admission

The ledger contract permits an insertion only together with adoption of an
actual extracted/tested response coordinate.  The paid-splice theorem gives
exactly such a coordinate when `C_d` fails: the complete signed allocation,
source, target, core, residual, observer surplus, and supplier edges are all
recorded.  Since `H` leaves the root and its new holder `d` is paid, this is
the natural `G8` retirement insertion.

The previously open question was:

> Does the frozen `G0--G10` transition language admit the fixed second probe
> `C_s` after recording the failed paid probe `C_d`, even though `C_s` may
> leave `d` below base?

`SACRIFICED_H_RELAY_ADMISSION_LEMMA_20260814.md` answers **yes** at the exact
local interface:

1. `r` remains strictly above base and `q,s` remain paid, so `d` is the
   unique sacrifice-eligible last-priority hole;
2. the fixed-`U` candidate phase explicitly includes paid and
   priority-valid sacrificed-hole candidates;
3. the global ledger contract says no selector is forbidden merely because
   it consumes retired support—its canonical cancellation must instead be
   tested; and
4. cancellation here is unusually exact: it restores `C_d` without changing
   any other packet or floor.

If `d` falls below base, exact subtraction proves that `H` strictly captures
the whole deficit from its earlier paid state; if `d` remains paid, the
ordinary paid-splice theorem applies.  This is independently QF_LRA-audited.

The remaining external-review question is compositional: confirm that the
frozen global proof graph imports this proved one-edge operation

\[
(A,Q,H+L+W,X_s)\longrightarrow(A,Q,L+W,H+X_s),
\]

with root and protected owner fixed.  No valuation search or packet-size
bound is used.

## Claim boundary

This audit establishes statement fidelity between the endpoint-6 data and
every typed collision field.  It does not substitute for external semantic
review of the transition language, independently reprove the collision
closure theorem, or certify the full fixed-`U` dependency graph.

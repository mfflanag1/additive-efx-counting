# Five-core-endpoint root-retention ledger lemma

**Date:** 2026-08-14

**Status:** cap-free exact supplier/edge reduction for the five endpoints in
the sharp `q,s`-payment proof core

## Input

Use the physical packet interpretation of the allocated-`E` form-2 cell.  The
current support allocation is

\[
Y=(A+H,\ Q,\ W,\ E;\ P),                       \tag{1}
\]

in owner order `(r,q,d,s; charity)`.  The protected root bundle `A+H` is
strict at the current fixed-`U` record.  The compact `q,s`-paid proof core
uses exactly endpoints `Z1,Z2,Z3,Z4,Z6`.

For a selected endpoint, retain the current root bundle `A+H`.  Remove from
the selected nonroot target every packet recaptured by the root.  If the
selected root target contains `M` (only `Z6`), release `M` to `q`.  This gives
the following exact complete allocations.

| Selected endpoint | Root-retained allocation `(r,q,d,s)` | Moved supplier edges from `Y` | Only newly debited nonroot owner |
|---|---|---|---|
| `Z1` | `(A+H,Q,W+P,E)` | `charity->d` | `d` loses `H` |
| `Z2` | `(A+H,Q,L+W,(E-L)+P)` | `s->d, charity->s` | `d` loses `H` |
| `Z3` | `(A+H,Q,L+W,(E-L)+P)` | `s->d, charity->s` | none: `(E-L)+P=X_s` |
| `Z4` | `(A+H,Q,W+P,E)` | `charity->d` | `d` loses `A-a0` and `H` |
| `Z6` | `(A+H,(Q-J)+P+M,J+(W-M),E)` | `q->d, d->q, charity->q` | `q` loses `A-a0` and `H`, gains `M` |

Every row is complete and uses at most three directed supplier-to-recipient
edges.  Packet cardinalities are unrestricted.

## Exact debt accounting

The root is paid strictly in every row because its bundle is exactly `Y_r`.
Every owner whose target is unchanged from the selected endpoint preserves
her endpoint utility.  Therefore:

1. for `Z1,Z2,Z4`, the only possible newly created payment hole is `d`;
2. for `Z3`, `s` loses `H` from the endpoint but returns exactly to her base
   bundle `(E-L)+P=X_s`, so no new hole is created; and
3. for `Z6`, the only possible new hole is `q`, again in addition to a
   pre-existing endpoint hole at `d`.

The exact new-creditor margins are

\[
\begin{aligned}
v_d(W+P)-v_d(H+W+P)&=-v_d(H) &&(Z1),\\
v_d(L+W)-v_d(H+L+W)&=-v_d(H) &&(Z2),\\
v_s((E-L)+P)-v_s(H+(E-L)+P)&=-v_s(H) &&(Z3),\\
v_d(W+P)-v_d((A-a0)+H+W+P)&=-v_d((A-a0)+H) &&(Z4),\\
v_q((Q-J)+P+M)-v_q((A-a0)+H+(Q-J)+P)
 &=v_q(M)-v_q((A-a0)+H) &&(Z6).
\end{aligned}                                    \tag{2}
\]

Thus the generic root/sacrifice two-debt interface splits into two typed
physical cases:

- a sole `d`-row current wall (`Z1,Z2,Z3,Z4`); or
- a `{d,q}` two-creditor row with the explicit compensation packet `M`
  (`Z6`).

One support edge remains unused even in the last row.  Any compatible
response/charity repair using that remaining edge stays within the requested
four-edge budget.

## Saturation interface

If a root-retained row is complete physical EFX, it proves the requested
conclusion immediately.  Otherwise a failed observer who remains at or above
base exposes an ordinary base response by global minimum extraction.  After
that saturated exit is excluded, only the debt rows listed above can remain.

Consequently the unresolved supplier theorem is no longer an arbitrary
two-family Hall problem.  It is the disjunction of:

1. closing the already mandatory current-only `d` wall with one spare edge;
2. proving that `M` pays or reroutes the `Z6` `{d,q}` row, or that failure
   activates the recorded `q->d`, `d->q` two-cycle.

The `Z3` payment claim is unconditional in the declared cell: `(E-L)+P` is
literally the normalized base bundle of `s`.  Conversely the `Z6` new
`q`-debt is genuine.  An exact PI-CEGAR added 78 missing generalized-PI cuts
and terminated at a positive-rational PI-free profile satisfying endpoint-6
EFX and `q,s` endpoint payment while the root-retained `q` bundle is below
base.  Thus the final `Z6` inequality cannot be removed by generic PI-freeness.

## Claim boundary

Proved: exact completeness, supplier edges, root retention, changed-owner
sets, and margin identities for all five proof-core endpoints, without a
packet-size cap.

Not proved: EFX of a root-retained row, closure of its remaining one-/two-row
response, admissibility of an additional repair edge at the identical
saturated record, the universal fixed-`U` theorem, or general EFX.

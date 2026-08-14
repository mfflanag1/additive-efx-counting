# Global retired-root-support ledger composition theorem

**Date:** 2026-08-13

**Status:** cap-free composition of the retired-support ledger through the
`G0--G10` architecture; the exact surviving class is typed `T_L^*`, not GG
closure

**Subsequent audit correction (2026-08-14):** an attempted elimination of
`T_{L,times}^*` remains conditional because its root supplier-star operation
does not yet preserve declared nonroot floors.  Thus this theorem's full
typed output `T^dagger=T_0^* dot-union T_L^*` remains the current frontier.
See `ROOT_GLOBAL_SUPPLIER_STAR_FLOOR_ADMISSIBILITY_GAP_20260814.md`.

## Theorem

Use the frozen augmented-state contract and the existing `G0--G10` proof
graph, beginning at the globally maximal base. Before the first
permanent-anchor peel, `L` is empty and every original transition is
unchanged; an exact original `T*` recurrence is labeled `T_0^*`. After the
first peel, append every retirement and every attempted later consumption to
the exact signed state and perform the canonical ledger audit below.

Then every transition has at least one of the following outcomes:

1. an explicit EFX allocation lexicographically above the globally maximal
   base;
2. a release-compatible PI cycle;
3. strict growth of the retirement ledger, or an actual strict change of the
   selected response, complete signed allocation, retained support,
   owner-component prefix, or an existing fixed-family finite utility vector,
   with its collision/state provenance recorded so that it cannot recur at
   fixed earlier coordinates;
4. a valid root/anchor exchange or reselection with a permanently new exact
   label; or
5. an exact state in
   `T^dagger=T_0^* dot-union T_L^*`: either the pre-ledger exact `T_0^*`
   recurrence, a parked-support `T_{L,perp}^*` recurrence whose complete
   active selector/release pool avoids nonempty `L`, or a collision
   `T_{L,times}^*` state carrying a named retired packet, its retirement
   supplier and current holder, and either a repeated retired-hitting
   response, a repeated normalization-bypass response, or an
   equality-critical/base-floor separator for which no typed handoff is
   admissible, together with rank deficiency or the explicit
   observer-payment/release wall. Here
   `T_L^*=T_{L,perp}^* dot-union T_{L,times}^*`.

In particular, no retired good is executed as a required input of a later
selector under the same anchor label. A later preference or proposed cell
may still mention the good, but canonical cancellation diverts that attempt
to a ledger-free selector, a closing outcome, strict permanent finite
progress, or `T_L^*`; it does not execute the same-label restoration.

## Canonical audit of one transition

Let `Z` be the candidate constructed by the original transition and let
`K` be the set of goods in the current **physical** label's retired support
`L_alpha` that `Z`
would move away from their current holders.

### A. No collision

If `K` is empty, execute the original proved transition. Its old
EFX/PI/progress/continuation classification is unchanged. If it reaches an
exact `T*` recurrence while `L` is empty, record `T_0^*`. If `L` is nonempty,
audit the complete active selector/release pool, not only the chosen move. A
member that meets `L_alpha` is processed by B--D. If every member is
disjoint, all retired goods stay with their recorded holders and the exact
recurrence is the parked-support subtype `T_{L,perp}^*`. Thus a collision-free
post-ledger terminal is not omitted.

### B. Ledger-free realization

Otherwise form `Z^-` by cancelling every transfer of a good in `K`: leave
that good with its current holder and perform every other transfer of `Z`.
This operation is physical and conserves every good. Relative to `Z`, a
current holder regains outgoing retired goods but may also lose retired goods
that `Z` would have transferred in. Likewise, an intended recipient can lose
assigned utility even while remaining above its typed floor. Therefore the
proof recomputes **every** owner-target and owner-charity comparison at `Z^-`; it does not
localize new walls to one enlarged target.

If every typed protected floor survives and `Z^-` is EFX, the preserved
strict-priority floor makes it a lexicographic contradiction. If floors
survive but any comparison fails, globally minimum extraction at the actual
allocation `Z^-` gives a genuinely current-safe response. It either avoids
the ledger or meets it and enters the collision normalization lemma. A new
response coordinate is finite progress; an exact ledger-free response/state
repeat is the normalization-bypass `T_L^*` variant because the original
selector still collided with the named nonempty packet and its normalized
EFX test failed. No wall or changed observer utility is discarded.

### C. Failed recipient floor

If a recipient `s` loses her required floor, use her original cell `A` and
the removed part `K_s=A intersect K`. Then

\[
 v_s(K_s)\ge v_s(A)-F_s.                         \tag{1}
\]

When `v_s(A)>F_s`, the retired packet captures a positive margin and global
protected-floor-minimal extraction applies within the strict failed cells. A
ledger-free core gives an alternative current-response or priority-valid
base-floor handoff. A root core in the enlarged-root state invokes
peel/reselect. A core hitting retired support either adds a new exact
collision/state record or reaches `T_L^*` at exact repetition.

When `v_s(A)=F_s`, positivity makes the removed packet equality-critical:
`v_s(A-K_s)<F_s`. A nonroot sacrifice handoff is tested only when its exact
earlier-priority and physical premises hold. A root candidate is used only
when the root remains strictly above base, or a separately valid safe anchor
exchange applies. An EFX test closes; otherwise an executed admissible test
supplies a genuine response coordinate. If no such typed operation is
admissible, the equality cell, packet provenance, and failed normalized floor
enter the equality-critical `T_L^*` variant immediately. No nonexistent
strict response or universally available sacrifice handoff is inferred.

### D. Release compatibility

Cancellation never declares a retired packet supplied. Every retained good
keeps its current holder and signed provenance. Any proposed PI edge set is
closed under the recorded suppliers before PI is invoked. An outside
supplier strictly grows the four-owner component; at full owner closure, an
exact repeated edge set is checked by the existing hole-pivot/cycle theorem.

## Why the progress is global

The permanent history is ordered by inclusion:

\[
 (L,\mathcal C,\mathcal R,\mathcal A),            \tag{2}
\]

where `mathcal A` is the set of physical root/anchor labels already entered;
floor changes do not manufacture new labels. Each set
is finite:

- goods and packet supports are subsets of a finite ground set;
- allocations include charity and hence form a finite family;
- matchings, holes, suppliers, and source/target labels are finite;
- every typed floor is the value or threshold of a bundle in a fixed row.

A changed collision is recorded only together with adoption of its actual
extracted/tested response; a changed state or anchor is likewise executed
before being recorded. Therefore a log insertion alone is never progress,
and the associated physical response/allocation/label change cannot be
reported a second time at fixed earlier coordinates.
When no insertion is possible, the complete augmented record repeats and is
exactly the `T_L^*` outcome. This uses full signed reconstruction; it does not
order unrelated scalar residuals.

## Transition-by-transition composition

| State | Ledger-normalized outcome |
|---|---|
| `G0` | entry has empty ledger; original globally maximal flower; an exact pre-peel terminal is typed `T_0^*` |
| `G1` | top/floater reset, or collision normalization; old retained-support growth remains monotone |
| `G2` | ledger-free minimal response or retired-hitting response record |
| `G3` | connected root transfer with cancelled retired packets; failed payment enters protected-floor extraction |
| `G4` | normalize each matching core; first failed core is the collision witness; rank-four exact repeats use the hole cycle |
| `G5` | source-inactive/two-hole repair, or typed base-floor collision separator |
| `G6` | normalized fork; outside supplier grows owner closure, saturated repetition enters `T_L^*` |
| `G7` | component-wide return selector over ledger-free packets; failure supplies (1) and its typed separator |
| `G8` | append `L`, collision, and label provenance to the exact signed state; executed coordinate changes are strict, repeats exact |
| `G9` | normalize path cores/releases; a supplied cycle is PI, otherwise supplier/collision progress or `T_L^*` |
| `G10` | root-high response reselects; root-low response grows `L`; every later return is audited by B--D |

Orientation reset, recapture, hole pivot, two-hole normalization, paid-anchor
reset, root flip, anchor exchange, and enlarged-root return are instances of
B--D. Their old
fixed-support coordinates are retained, not replaced by the ledger.

## Exact surviving class and proof graph

The global surviving class is

\[
T^\dagger=T_0^*\mathbin{\dot\cup}T_L^*,
\]

where `T_0^*` is an exact generic `T*` recurrence with empty ledger and

\[
T_L^*=T_{L,\perp}^*\mathbin{\dot\cup}T_{L,\times}^*.
\]

The parked-support subtype `T_{L,perp}^*` has nonempty `L` and a complete
active selector/release pool disjoint from it. The collision subtype is the
more structured class below.

The post-ledger open node is

> **`T_{L,times}^*`: retired-packet saturated splice.** The complete signed state,
> typed floors, physical root/anchor label, retirement and collision histories repeat;
> the canonical ledger-free realization of the active selector fails a floor,
> EFX comparison, or release test; and a globally minimal protected-floor
> core hits a named nonempty retired packet, a ledger-free response repeats
> after normalization, or an equality-critical/base-floor typed handoff is
> unavailable. If all
> selected edges are current responses, response rank is below four;
> otherwise the state carries the explicit base-floor observer-payment or
> release separator.

The other post-ledger subtype `T_{L,perp}^*` carries nonempty retired support,
exact current holders, and complete selector-pool avoidance. Both are more
structured than an untyped generic `T*` record. Empty-ledger rank-deficient
`T*` instances are not in `T_L^*`.

The updated local graph is

```text
G0 -> ... -> G10
                | root-high
                +-> anchor reselection (outcome 4)
                | root-low
                +-> grow L (outcome 3)
                        |
              ledger-normalize every return
                 /       |          \
              EFX/PI  finite record  T_{L,times}^*
```

A post-ledger exact recurrence whose whole active pool avoids `L` enters
`T_{L,perp}^*` from the collision-free branch.

The base-to-peel prefix has the unchanged additional exit `T_0^*`. Thus the
global graph has the single typed union terminal `T^dagger`, with its empty-
and nonempty-ledger components explicitly separated.

## Claim boundary

This theorem proves the global bookkeeping, selector-normalization, physical
conservation, typed-floor routing, no-silent-reuse property, and the exact
global `T^dagger` terminal for the current `G0--G10` architecture. It does not pay
the rank-deficient/base-floor separator inside `T_L^*`, close generic
empty-ledger `T*`, validate the original BCFF-to-GG import beyond the premises
already frozen by the referee composition, close GG, or prove four-agent /
general additive EFX.

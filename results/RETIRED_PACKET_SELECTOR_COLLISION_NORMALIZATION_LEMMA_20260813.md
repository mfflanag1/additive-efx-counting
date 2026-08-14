# Retired-packet selector-collision normalization lemma

**Date:** 2026-08-13

**Status:** cap-free reduction of every unavailable ledger-free selector to
a ledger-free protected-floor core, strict signed collision progress, a root
operation, or the retired-packet `T_L^*` subclass

## Exact selector collision

Fix one augmented GG state with protected floor vector `F`.  An original
admissible transition gives some recipient `s` a physical packet `A` and
requires

\[
 v_s(A)\ge F_s.                                   \tag{1}
\]

The packet may be a selected core, a compensation cell, a retained target,
or a union of signed packets from a connected supplier component.  Let

\[
 K=A\cap L_\alpha,                                \tag{2}
\]

where `L_alpha` includes every good ever retired under the same physical
root/anchor/supplier/orientation label, regardless of later floor changes.

If `K` is empty there is no collision.  Suppose `K` is nonempty and the
ledger-free packet fails:

\[
 v_s(A-K)\le F_s.                                 \tag{3}
\]

If (1) is strict, additivity gives the exact capture

\[
 v_s(K)\ge v_s(A)-F_s>0.                         \tag{4}
\]

If (1) is equality, positivity instead gives

\[
 v_s(A-K)=F_s-v_s(K)<F_s.                        \tag{4e}
\]

This is an **equality-critical retired packet**. It need not contain a core
strictly desired over `F_s`, so it is not silently promoted to a response.
If `s` is nonroot and the exact premises of an existing priority-valid
sacrifice handoff hold, test the normalized allocation with `s` as the
explicitly sacrificed later owner. An EFX candidate closes; otherwise
globally minimum extraction at that actual allocation supplies a genuine
response coordinate. If `s` is the first-priority root, use a normalized
candidate only when the root remains strictly above base; an independently
valid safe root core may instead use the existing root/anchor exchange. When
neither typed operation is admissible, (4e), the original colliding cell,
and the failed normalized floor form the equality-critical `T_L^*` variant
immediately. No specialized handoff is invoked outside its premises, and no
certificate alone is called progress.

## Global floor-minimal extraction

First process every equality-critical failed cell through the admissibility
test above. An actually executed sacrifice/root operation changes the
response/allocation/anchor coordinate. If no such operation is admissible,
the exact equality-critical cell enters typed `T_L^*` immediately; merely
recording the failed test is not progress.

For every remaining strict failed recipient `i`, let `A_i` be that recipient's complete cell
in the original transition. Among every active failed recipient `i` and every
subset `D subseteq A_i` satisfying

\[
 v_i(D)>F_i,                                      \tag{5}
\]

choose an agent/subset pair of globally minimum cardinality, with fixed
physical tie-breaking. The family is nonempty by strict (1). Keeping `D` inside one
original candidate cell preserves its exact signed supplier set; the proof
does not manufacture a new cross-cell packet.

The selected `D` is safe relative to `F`: if an observer `j` had
`tau_j(D)>F_j`, deleting a least-`j` good would give a strictly smaller
subset desired over `F_j`, contradicting global minimality.  Every good of
`D` is critical in its source row.

This is current safety only for rows with `F_j=v_j(Y_j)`. If `F_j` is a
lower base or priority-valid sacrifice floor, `D` is merely
**protected-floor-safe**. The signed state retains which rows use which kind
of floor; no base-paid core is silently promoted to a current response.

Exactly one of the following applies.

### 1. Ledger-free protected core

If

\[
 D\cap L_\alpha=\varnothing,                     \tag{6}
\]

then `D` is a protected-floor-safe desired core using no retired support. If
its source floor is current utility, it is a genuine current response. If
its floor is lower, assign it only when the exact premises of an existing
priority-valid base-floor handoff hold, retaining the earlier strict root
gain and every row's floor type; otherwise the failed typed payment is the
base-floor separator in `T_L^*`. A genuinely new core/target/release label is
permanent finite signed-state progress. If the ledger-free response and the
complete augmented state already repeat, the original nonempty collision
packet together with the failed normalized selector gives the
**normalization-bypass** variant of `T_L^*`; the proof does not send the same
response around the graph again.

### 2. Root collision

If the source of `D` is the current root and the enlarged-root surplus
premises hold, apply the permanent-anchor peel-or-reselect dichotomy.  A
root-high `D` is a valid current-phase anchor reselection.  A root-low `D` is
paid by the old-anchor surplus and strictly grows the retirement ledger.

Outside that enlarged-root interface, a root-sourced `D` remains a labeled
root collision; it is not silently imported into the peel theorem.

### 3. Retired response with fresh record

Suppose `D` meets `L_alpha`.  Attach to its exact response record:

- `K_D=D intersect L_alpha`;
- every retirement event and current holder of `K_D`;
- the supplier set of every other signed packet of `D`;
- the protected floor vector and current anchor label; and
- the matching/hole state in which `D` is selected.

If this collision record is new, adopt the corresponding globally extracted
or tested response and permanently add its collision provenance to
`mathcal C`. Thus the complete response coordinate changes; the proof does
not claim progress merely because a visit was logged. This is strict finite
signed-state progress. Finiteness follows from the finite
ground set, allocations, owner labels, packet subsets, matchings, and floor
values induced by bundles.

### 4. Old collision at a changed complete state

If the collision label is old but the complete augmented state is new,
execute the admissible response/root/anchor coordinate change and permanently
add the resulting complete record to `mathcal R`. Full signed
reconstruction makes this an actual new allocation/charity/support state,
not a scalar relabeling.  Again the coordinate has finite range.

### 5. Exact retired-packet recurrence

If both the collision/response record and complete augmented state repeat,
the state has all data required for `T_L^*`: a nonempty retired packet with
original supplier and current holder, a fixed typed floor vector, failure of
the canonical ledger-free realization, and a retired-hitting or
normalization-bypass repeated response. The equality-critical variant may
enter earlier when its specialized sacrifice/root operation is not
admissible; it does not invent a repeated current response.

When every selected edge is a current response and rank is four, the existing
exact-state hole-pivot theorem either gives a release-compatible cycle or
changes a physical edge/hole record, returning to branches 3--4. If some
edge is only base-floor desired, or comes from the equality-critical
sacrifice/root test, its typed observer debt remains an explicit separator.
Thus the surviving `T_L^*` state is rank deficient or has an
explicit base-floor observer-payment/release separator. It is a proper
subclass of generic `T*` because `K_D` is required to be nonempty; generic
empty-ledger `T*` records remain outside it.

## New root or anchor label

If a retired packet returns only after the root or physical anchor changes,
append the new label to the permanent label history.  A new label is strict
finite progress.  If the label is old but the complete augmented state is
new, branch 4 applies.  If both repeat, branch 5 applies.  Consequently a
root/anchor change cannot be used as an unrecorded restoration at fixed `L`.
Changing only `F` is not a new label and therefore cannot bypass branches
1--5.

## Meaning of “no reuse”

Positive additive valuations do not make a peeled good cease to be desired.
The invariant proved here is therefore **no silent reuse**, not the false
semantic assertion that no later preference can mention the good.  Under the
same anchor label, a later selector either avoids retired support or triggers
one of branches 2--5.  It cannot simply restore the old target and reset the
proof state.

## Claim boundary

This lemma proves protected-floor-safe global extraction, the exact capture
inequality, finite collision/state progress, root-interface routing, and the exact
`T_L^*` recurrence record.  It does not by itself prove that every `G0--G10`
packet family is contained in the declared complete transition pool, pay the
observer separator in rank-deficient `T_L^*`, close generic empty-ledger
`T*`, close GG, or prove four-agent/general additive EFX.

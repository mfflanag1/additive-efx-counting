# Nonroot normalization-bypass collision gap

**Date:** 2026-08-14

**Verdict:** the imported claim that the complete `T_{L,times}^*` subtype is
closed is not established by its cited dependency graph.  Root-held
collisions and common-safe nonroot whole hits are covered; a nonroot-held
normalization bypass whose repeated ledger-free response avoids the retired
packet is not.

## Exact missing case

Let a nonroot holder `h` own a named retired packet `K`.  An active selector
attempts to move `K`; canonical cancellation leaves it at `h` and restores
an allocation `Z`.  Suppose `Z` is non-EFX and its adopted globally minimal
current-safe response is `E`, with

\[
                         E\cap K=\varnothing.     \tag{1}
\]

At exact repetition this is explicitly admitted by clause (d) of the frozen
`T_{L,times}^*` definition: the original selector collides with `K`, while
the ledger-free normalized allocation and response repeat.  The response
itself need not hit `K`.

The two dependencies cited by the Aug-14 resolution do not cover (1):

1. `NONROOT_SAFE_WHOLE_HIT_ENVELOPE_DESCENT_THEOREM_20260814.md` requires a
   common-safe core `D` in the holder target satisfying `K subseteq D`.  Its
   strict nested-envelope argument starts from that containment.
2. `ROOT_SINGLETON_SUPPLIER_STAR_FLOOR_RESET_CLOSURE_THEOREM_20260814.md`
   requires the protected root to be the current holder of `K`.

In (1), the current holder is nonroot and the only repeated response may be
disjoint from `K`.  Neither theorem applies.  Moving `K` to the root in the
counterfactual colliding selector cannot be used to satisfy the second
premise: the frozen ledger contract cancels that transfer and defines the
current holder from the normalized physical allocation.

## Exact local positive-additive witness

The gap is not merely syntactic.  Take a normalized allocation with packets

\[
 Z_r=\{a\},\quad Z_q=\{b,c\},\quad
 Z_h=\{w,p\},\quad Z_s=\{e\},                    \tag{2}
\]

and retired singleton `K={p}` held by `h`.  Give source `s` values

\[
 v_s(e)=1,\qquad v_s(b)=v_s(c)=2,
 \qquad v_s(p)=1/10.                              \tag{3}
\]

Then `s` strongly envies target `q`; a globally minimal desired response can
be the safe singleton `{b}`, which is disjoint from `K`.  Give every other
owner positive value `1/10` for `p` and an own bundle value at least one.
No owner has a desired holder core containing `p` at those current floors.
Separately choose the root value of `a` above its immutable base coordinate.

An active selector returning `p` from `h` to `r` collides with the retired
packet.  Cancelling it restores (2), whose response `{b}` repeats.  This is
the normalization-bypass support pattern, while both cited closure premises
fail.  The witness is a countermodel to the *dependency implication*, not to
the full globally maximal GG theorem.

## Audit failure in the imported certificate

`audit_retired_packet_charge_anchor_resolution_20260814.py` checks the
nonroot dependency only through the status
`ALL_COMMON_SAFE_NONROOT_WHOLE_HITS_TERMINATE`, then sets
`repeated_hitting_or_normalization_bypass_covered=true`.  It does not encode
an implication from a disjoint normalization-bypass response to a
`K`-containing common-safe core, nor does it split the two cases.  The JSON
boolean is therefore documentation, not verification of this branch.

## Consequence for the active fixed-`U` target

The permanent-anchor charity relay reduces the complete target to exactly
this gap.  After moving the permanent anchor to the strict root, stage the
singleton charity at the root, move it to the unmatched owner, and attempt
to return it.  The two complete allocations use only two support-provenance
edges.  If both are non-EFX, the normalized failed response may avoid the
charity singleton, producing (1).

The next theorem is therefore precise:

> In the permanent-anchor charity-relay state, a saturated nonroot-held
> singleton normalization bypass either produces a complete EFX endpoint,
> a release-compatible PI/progress exit, or a common-safe holder core
> containing the singleton (so envelope descent applies).

Alternatively, produce an exact positive-rational full-premise fixed-`U`
countermodel in which every response avoids the singleton and all saturated
exits fail.

## Claim boundary

Proved here: a concrete logical gap in the current proof of complete
`T_{L,times}^*`, with an exact local positive-additive support witness and a
line-by-line dependency mismatch.  Not proved: that `T_{L,times}^*` is
false, a full GG/fixed-`U` countermodel, closure of the normalization bypass,
the active four-edge theorem, or general additive EFX.

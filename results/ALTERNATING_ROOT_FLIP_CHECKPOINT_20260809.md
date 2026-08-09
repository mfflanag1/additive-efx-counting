# Alternating root-flip checkpoint

**Date:** 2026-08-09
**Goal:** complete four-agent additive EFX
**Status:** one new cap-free lemma; general theorem remains open

## New cap-free result

The [`alternating root-flip lemma`](ALTERNATING_ROOT_FLIP_LEMMA.md) proves a
two-allocation dichotomy for arbitrary packet sizes and normalized monotone
valuations.  In the alternating cycle

\[
p\xrightarrow f r\longrightarrow s
\xrightarrow f q\longrightarrow p,
\]

let `D` be any desired set for `p` on \(X_r\cup\{f\}\).  At least one of

\[
(p,r,s,q)=(x,y,D,X_q)
\]

and

\[
(p,r,s,q)=(D,y,X_q,x)
\]

is EFX.  If both failed, `s` would rank a deletion remainder of `X_q`
strictly above `D` and a deletion remainder of `D` strictly above `X_q`, an
impossible strict cycle under monotonicity.

The first allocation preserves `p,q` and improves `r`; the second improves
`p,q,r`.  Hence order `(p,q,r,s)` is closed, as is `(s,r,q,p)` by half-turn
symmetry.  Together with the sixteen easy orders, 18 of 24 alternating
priority-role orders are now closed cap-free.

## Exact discovery and verification

The result came from the eleven-good `(p,q,r,s)` restricted CEGAR:

- eight completed models;
- 576 learned anchored or promoted rivals;
- exact QF_LRA UNSAT;
- an assumption core of three rivals;
- deletion minimization reduced it to two rivals;
- deleting either rival restores SAT.

The independent replay is
[`alternating_root_flip_split_core_audit.json`](alternating_root_flip_split_core_audit.json),
with SHA-256
`27d1bb13567c60ea5cfa69efcf0fa65d20b6939b8f6d01c973771b1920b62146`.
The analytic proof no longer depends on the fixed cell or solver.

The split encoding originally imposed the same within-packet good order in
all four valuation rows.  That was a false comonotonicity restriction.  It
has been corrected to order only `p`'s row, which is a valid global symmetry
break.  The two-rival core above remains exact UNSAT under the corrected
broader formula.

## Necessary correction discovered next

The initial repaired target allowed either:

1. preserve the first singleton owner exactly and find a suffix-improving
   three-agent allocation; or
2. promote that owner to the one desired set selected in the base graph.

Both branches are necessary in the seven-good atom, but the canonical
version is false for split packets.  A strictly positive,
subset-nondegenerate eleven-good `(p,q,s,r)` profile has neither branch.
Its unrestricted EFX escape promotes `p` to the alternate desired set
\(\{tr0,br0,f\}\), while the selected set is \(\{tr0,tr1,f\}\).  The same
offer has six desired subsets.  This is frozen in
[`alternating_anchored_or_promoted_0321_nondegenerate_refutation_audit.json`](alternating_anchored_or_promoted_0321_nondegenerate_refutation_audit.json),
SHA-256
`f64be50d80f41aaee092b1fb4b4b2ef6161471b2399e806d3639c59ad10047c7`.

The correct promoted branch must therefore quantify over **every desired
subset on the champion offer**.

## Current exact boundary

For `(p,q,s,r)`, the original comonotone anchored-or-any-desired CEGAR
completed 17 models and
stored 1,142 exact rivals.  Every completed model had a valid restricted
escape.  The next master returned `unknown/canceled` when the bounded run was
stopped; no claim follows from that status, and the pool is not a decision of
the corrected broader cell.

Pool SHA-256:
`29dd1d15d3acbd5945f8e6e1865d3a60c026c8f4dc515c9a8ce45d01a8764eef`.
Session SHA-256:
`b089a9d6c662c733253b1dc89d0eb55ade821f0fa322469350beb71001b1b380`.

The narrower statement that the anchored branch may force `r` to own
exactly `y` is refuted after 12 models and 707 learned rivals.  Its terminal
model still has many anchored escapes, but all require a different bundle
for `r`.  Therefore the full three-agent repartition is essential.

## Live analytic target

> **Anchored-or-any-desired extension lemma.** Fix the first singleton owner
> and consider all external-observer-safe EFX allocations of the remaining
> three agents.  If the base is suffix-lexicographically maximal in this
> anchored family, then some desired subset on the root champion offer can be
> assigned to the root and extended to a partial EFX allocation.

The root-flip proof supplies the first exchange: failure of the simple
promoted allocation forces an anchored EFX allocation.  For order
`(p,q,s,r)` that allocation may lower `s`, so the missing step is to convert
the failure wall into an improvement of `q` or a nondecreasing replacement
for `s`.  Exact models show this requires genuine repartitioning among all
three active agents; one residual block and a fixed envy return are both
false restrictions.

## Remaining proof ladder

1. Prove the anchored-or-any-desired extension lemma for `(p,q,s,r)` and use
   half-turn symmetry for `(s,r,p,q)`.
2. Close the two priority-prefix pairs beginning `(p,s)` and `(s,p)`.
3. Combine all 24 orders into the cap-free alternating-cycle escape theorem.
4. Reuse its exchange invariant for the length-three and adjacent
   length-four residues, completing the exactly-two-nonsingleton theorem.
5. Prove the packet-flow contraction for three and four nonsingleton bundles.
6. Add the nonnegative/tie wrapper and obtain independent mathematical and
   formal reviews.

The breakthrough boundary is unchanged: the new lemma is real progress, but
complete four-agent additive EFX is not yet proved.

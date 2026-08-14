# Two-hole endpoint physical-failure localization lemma

**Date:** 2026-08-14

**Status:** cap-free analytic consequence of the two-hole endpoint theorem

## Lemma

Let `X` be a base allocation normalized by `v_i(X_i)=1`. Let `Z` be a
complete allocation and let

\[
H=\{i:v_i(Z_i)<1\}.
\]

Assume `|H|<=2`. If `Z` is not physical EFX, then at least one of the
following holds.

1. There is a physical common-safe base-desired core contained in a failed
   target bundle, hence an ordinary base response.
2. Every failed EFX comparison is observed by an owner in `H`; consequently
   all current/base observer debt is localized to at most two owners.

The statement is independent of packet sizes and the number of physical
goods.

## Proof

Take a failed comparison from observer `i` to target `j`, and choose a least
`i`-valued physical good `g in Z_j`. Then

\[
v_i(Z_j-g)>v_i(Z_i).                             \tag{1}
\]

If `i notin H`, the right side is at least one. Thus the finite family

\[
\{(s,D):s\in N,\ D\subseteq Z_j-g,\ v_s(D)>1\}
\]

is nonempty. Choose a pair `(s,D)` with inclusion-minimal support. For every
owner `h` and good `x in D`,

\[
v_h(D-x)\le1,                                    \tag{2}
\]

because otherwise `(h,D-x)` would be a smaller member of the family. Hence
`D` is common-safe relative to every base bundle and is strictly desired by
`s`: it is an ordinary physical base-response core. This is outcome 1.

If outcome 1 does not occur, no failed observer can lie outside `H`. All
failed comparisons are therefore sourced by the at-most-two owners in `H`,
which is outcome 2.

## Application to the allocated-E endpoint

The dual-verified bounded theorem supplies a compressed endpoint `Z_k` with
`|H|<=2`. Physical expansion preserves every owner's utility and hence the
same payment-hole set. Therefore the expanded endpoint is either complete
physical EFX, exposes an ordinary base response, or has every unsafe
comparison concentrated in at most two current/base debt rows.

This is the precise cap-free interface to the companion two-creditor Hall
and base-restoration analysis. It does not assert that the two debt rows are
already supplier-compatible or that their Hall cut closes.

**Sharp role localization update.**  The dual-verified
`q,s`-paid strengthening shows that the selected endpoint may be chosen with
`H subseteq {r,d}`.  Hence, after ordinary base-response augmentation is
excluded, every failed physical comparison is observed by the distinguished
root or sacrificed owner.  The one-hole strengthening has an independently
audited exact PI-free countermodel, so both rows must be retained.

## Claim boundary

Proved: cap-free localization of every physical failure of an at-most-two-
hole endpoint to an ordinary base response or at most two debt observers.

Not proved: elimination of the two-debt Hall cut, repair within four physical
supplier edges, the universal fixed-`U` theorem, four-agent EFX, or general
EFX.

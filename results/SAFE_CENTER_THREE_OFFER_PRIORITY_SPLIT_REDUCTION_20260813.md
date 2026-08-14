# Safe-center three-offer priority-split reduction

**Date:** 2026-08-13

**Status:** cap-free routing of the star to the root-holder price gate or the
existing one-core/three-hole external-star normal form

## Input

Use the safe-center star with center `s`, common-safe whole center bundle
`U_s`, and one common-safe offer `O_h subsetneq U_h` from each leaf
`h in N-{s}`, all strictly desired by `s`.  Let `r` be the first-priority
proof root inherited from the globally maximal base.

## Case I: nonroot center

Suppose `s != r`.  Then the root is one of the three leaves and supplies a
common-safe offer `O_r` desired by `s`.  Test the physical transfer of `O_r`
to `s`.  If the current root bundle is

\[
U_r=H_r\mathbin{\dot\cup}O_r,
\qquad
\sigma_r=v_r(U_r)-F_r,
\]

the exact root-holder release price is

\[
p_r(O_r)=\max\{0,v_r(O_r)-\sigma_r\}.             \tag{1}
\]

Any admissible compensation `J` must satisfy `v_r(J)>=p_r(O_r)`, together
with the typed root/observer safety conditions.  A successful protected
compensation gives two disjoint protected cores—`O_r` for `s` and the paid
root core for `r`—and enters the two-core/two-hole machinery.  Failure of the
complete admissible compensation family is exactly the root-labeled holder-
price separator already isolated in atomic survivor B.  Thus a nonroot-
center star is not a new third separator.

## Case II: root center

Suppose `s=r`.  Choose any offer `O_h`.  It is common-safe and satisfies

\[
v_r(O_h)>v_r(U_r)\ge v_r(X_r).                   \tag{2}
\]

Perform the canonical retired-ledger normalization before releasing the old
root bundle.  Let `K_r` be every retired good that must remain with the root
under the current physical label and put

\[
A_r=O_h\mathbin{\dot\cup}K_r.                    \tag{3}
\]

The root remains strictly above the globally maximal base because
`v_r(A_r)>=v_r(O_h)>v_r(X_r)`.  If `A_r` is not safe at the exact normalized
state, globally minimum response extraction is mandatory.  A response
hitting retired support returns to the proper/whole-packet or root-holder
collision branches; a ledger-free response changes the actual selector and
enters the target-envelope routing.  It may not be skipped by treating `O_h`
alone as the root core.

If `A_r` is safe, let `P` be every remaining good.  By the three-agent
additive EFX theorem, allocate `P` completely and EFX among the three
nonroot owners.  The root is strictly above the globally maximal base, so a
full EFX endpoint is a lexicographic contradiction even if the three-agent
allocation does not preserve their old floors.

All comparisons among the three nonroot owners hold by construction.  Since
`O_h` is common-safe at the old paid state, the only possible new failures
are exactly the six root-star comparisons between the root core and one of
the three hole bundles.  This is the existing one-core/three-hole external-
star normal form.  Its reciprocal signs route to PI, unsafe-core
augmentation, or the named source-inactive loss band; its one-directional
signs retain their existing status.

## Consequence

The safe-center star does not add an unrelated terminal to the collision
proof graph:

- nonroot center -> root-holder price or two-hole response machinery;
- root center -> retired-collision normalization, or EFX / the already-
  certified one-core/three-hole external star when the retained core is safe.

Therefore completing `T_{L,times}^*` now requires the holder-price family
and the inherited external-star signs, with the retired-packet provenance
carried through either route.

## Claim boundary

This is a routing theorem.  It does not prove that root compensation exists,
prove safety of the retired-normalized root core,
eliminate the one-directional/source-inactive signs of the generic external
star, establish that every post-ledger offer has the special original GG
flower anchor used by later flower-specific lemmas, close
`T_{L,times}^*`, or prove four-agent/general EFX.

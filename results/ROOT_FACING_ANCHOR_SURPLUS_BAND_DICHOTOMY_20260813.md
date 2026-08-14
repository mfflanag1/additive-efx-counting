# Root-facing anchor surplus-band dichotomy

**Date:** 2026-08-13

**Status:** cap-free resolution of the root-facing atomic survivor outside
one exact root-surplus loss band

## Exact root-facing state

Let `X` be the globally maximal base, with first-priority root `r`, and put

\[
x=v_r(X_r).
\]

At the root-facing atomic survivor, let the current root target be `H`, with

\[
v_r(H)=x+\delta,
\qquad \delta>0.                                  \tag{1}
\]

Let `D subsetneq H` be a globally minimum current response to `H`, with
source `i`. Then `D` is physically nonempty, current-desired by `i`, and safe
at the exact allocation where it is selected. Put `C=H-D`.

## Exact trichotomy

Exactly one of the following holds.

### 1. Root-high reselection

If

\[
v_r(D)>x,                                         \tag{2}
\]

use the safe packet `D` as the new current-phase root anchor. Its source and
the released complement retain their complete signed provenance. This is a
valid root-preserving anchor reselection; it does not call `D` an old base
anchor.

### 2. Complement-paid controlled release

If

\[
v_r(D)<\delta,                                    \tag{3}
\]

give `D` to its response source and retain `C` at the root. Additivity gives

\[
v_r(C)=x+\delta-v_r(D)>x.                         \tag{4}

Thus the root remains strictly above the base. The source strictly improves,
and `D` is safe by global minimum extraction. The physical root support
shrinks strictly, with the release and any pre-existing walls kept in the
signed record. This is controlled anchor release, not an EFX claim.

### 3. Exact root-surplus loss band

The only remaining case is

\[
\delta\le v_r(D)\le x.                            \tag{5}
\]

Here `D` is not a strict base-improving root anchor, while

\[
v_r(C)=x+\delta-v_r(D)\le x.                     \tag{6}

Consequently neither side of the elementary split can be retained alone by
the first-priority root while keeping a strict lexicographic gain. This is an
exact two-sided root-critical certificate, not an unnamed anchor failure.

The three branches are disjoint and exhaustive. Equality in (3) belongs to
the loss band because (4) must be strict.

## High-surplus corollary

If

\[
v_r(H)>2x,
\]

then `delta>x`, so (5) is impossible. Every globally minimum root-facing
response therefore gives root-high reselection or complement-paid controlled
release.

More generally, the root-facing survivor is eliminated whenever the active
response family contains no packet whose root value lies in the closed band
`[delta,x]`.

## Relationship to retired-packet collision

Atomic survivor B of the retired-packet collision normal form is therefore
closed except when its root-facing minimum response lies in (5). The retired
packet's recipient-row capture does not reverse (5): the loss band is in the
root row. A complete proof must use the retired packet or another released
component to replace the missing root surplus, or show that global GG
maximality excludes the band.

## Claim boundary

This theorem proves the exact root-value trichotomy, safe root-high
reselection, complement-paid controlled release, and the high-surplus
corollary. It does not eliminate the band (5), prove final EFX after the
release, pay pre-existing observer debt, close the whole-packet or
normalization-bypass survivors, close `T_{L,times}^*`, or prove four-agent /
general EFX.


# Flower complement-return augmentation lemma

**Date:** 2026-08-10

**Status:** cap-free analytic strengthening; the deep-capture and internal
Hall-defect branches remain open

## Setting

Use the minimal-payment rotation

\[
W=B_q+L,
\qquad
R=(T_r\setminus L)+B_r,
\]

and let `a in {c,s}` be a most-envious response source for `W`.  Fix one
corresponding common-safe desired bundle `A subseteq W` for `a`.  Unlike the
coarser return construction, retain the whole unused complement `W\A`.
Define

\[
H_a=X_a+R+(W\setminus A). \tag{1}
\]

The three proposed targets are

\[
D_r=T_q+f,
\qquad A,
\qquad H_a.
\]

## Complement-return theorem

Test the following branches in order; the first applicable branch is
exhaustive.

1. **Direct `q` source.** Agent `q` desires `A`.  Then the two targets
   `D_r,A`, with sources `r,q`, form a release-compatible PI edge set.
2. **Complement return.** Agent `q` is a most-envious source for `H_a`.
   Then targets `(r,q,a)` with sources `(r,a,q)` form a
   release-compatible PI edge set.
3. **Named augmentation.** Agent `q` desires `H_a`, but is not a
   most-envious source; a proper desired subset has a source `b != q`.  If
   `b outside {r,q,a}`, the owner component strictly grows.  If
   `b in {r,a}`, the enlarged internal response relation either has an SDR
   and is PI, or Hall's theorem exposes an explicit internal defect.
4. **Complement-low capture.** Agent `q` does not desire `H_a`:
   \[
   v_q(X_a+R+W\setminus A)\le v_q(X_q). \tag{2}
   \]

No packet cardinality is used.

## Release-compatible proof

Regard `A` as a replacement target for slot `q`, rather than retaining the
larger offer `W`.  Its generalized edge has incoming and prescribed-release
sets

\[
I_q=A\cap L,
\qquad
O_q=T_q+(B_q\setminus A). \tag{3}
\]

The root target has

\[
I_r=T_q+f,
\qquad O_r=L+R. \tag{4}
\]

The complement-return target (1), regarded as a replacement for slot `a`,
has

\[
I_a=R+(W\setminus A),
\qquad O_a=\varnothing. \tag{5}

The incoming sets in (3)--(5) are pairwise disjoint.  Every incoming good is
supplied: `f` is initially unallocated; `T_q` and `B_q\A` are released by
the edge into `q`; and `A intersect L`, `L\A`, and `R` are released by the
root edge.  Thus any distinct internal sources for the three targets give a
BCFF PI edge set.

The root target is common-safe and desired by `r`, while `A` is common-safe
and desired by `a`.  If `q` also desires `A`, choose sources `(r,q)` for
targets `(r,q)` and use (3)--(4), proving branch 1.  Otherwise consider
`H_a`.  If it is common-safe and desired by `q`, then `q` is a most-envious
source and `(r,a,q)` proves branch 2.  If it is desired but unsafe, take an
inclusion-minimal desired subset and name one of its sources `b`.  Source
`q` again proves branch 2; every other source gives branch 3.  If `H_a` is
not desired by `q`, (2) is branch 4.  For an internal non-`q` source, inspect
all response sources of the three targets: an SDR is release-compatible by
(3)--(5), while absence of an SDR gives the stated Hall witness. \(\square\)

## Quantitative capture forced by the survivor

Put

\[
b=v_q(X_q),
\qquad
\delta=v_q(W)-b>0,
\qquad
\epsilon_a=b-v_q(X_a+R).
\]

Branch 4 implies

\[
v_q(W\setminus A)\le\epsilon_a,
\qquad
v_q(A)\ge v_q(X_a+R)+\delta. \tag{6}
\]

In the positive nondegenerate convention the inequalities are strict,
because the compared bundles are distinct.  In a PI-free state branch 1 is
also excluded, so common safety of `A` gives `v_q(A)<b`.  Consequently every
surviving complement-low source satisfies the deeper gap

\[
v_q(X_a+R)<b-\delta. \tag{7}
\]

Thus the former low-return alternative is not merely
`v_q(X_a+R)<=b`: the blocker must capture enough of `W` in `q`'s row to
absorb the entire improvement margin `delta`, while the released complement
fits strictly inside the external-return deficit.

## Four-owner termination consequence

Apply the same construction after a named external augmentation.  Only the
other owner in `{c,s}` can be new.  Hence the response chain still cannot
grow indefinitely, but its true terminal inequality is now (2), equivalently
the strict capture system (6)--(7), rather than the earlier coarse
low-return inequality.

The finite set-support and scalar implications replay in
[`flower_complement_return_augmentation_audit.json`](flower_complement_return_augmentation_audit.json).

## Claim boundary

This theorem closes every direct or complement return and forces a strict
deep-capture inequality in every survivor.  It does not yet eliminate that
capture inequality or a closed internal Hall defect, close `GG`, or prove
four-agent additive EFX.

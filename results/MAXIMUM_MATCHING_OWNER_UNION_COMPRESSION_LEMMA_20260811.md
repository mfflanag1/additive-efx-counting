# Maximum-matching owner-union compression lemma

**Date:** 2026-08-11

**Status:** cap-free analytic correction of minimal-defect compression;
residual payment/recapture polarity remains open

## Setting

Let `T` contain every owner target changed by a release-compatible proposed
component `Y`.  Every owner outside `T` keeps her base bundle.  For each
`j in T`, let `C_j` be the nonempty set of response sources relative to the
base EFX allocation `X`.

Choose a maximum matching `mu` of the full target--source relation.  Write

\[
J=\operatorname{dom}(\mu),\qquad
S=\operatorname{im}(\mu),\qquad
V=T\cup S,\qquad M=V\setminus S=T\setminus S. \tag{1}
\]

For each `i in S`, choose a common-safe desired core

\[
A_i\subseteq Y_{\mu^{-1}(i)}. \tag{2}
\]

The cores are pairwise disjoint.  Pool all remaining goods held by owners in
`V`:

\[
P=\left(\mathop{\dot\bigcup}_{v\in V}Y_v\right)
\setminus\left(\mathop{\dot\bigcup}_{i\in S}A_i\right). \tag{3}
\]

Choose any partition `P=dot union_{m in M} P_m`, give `A_i` to source `i`,
give `P_m` to unmatched owner `m`, and fix every owner outside `V`.

## Theorem

The resulting allocation is complete and release-compatible for arbitrary
packet cardinalities.  Every source in `S` strictly improves.  If every
unmatched owner is weakly nonworse, then:

1. no owner can fail EFX against a selected core `A_i`;
2. no owner can fail EFX against a target outside `V`, because that target
   is unchanged from the base allocation and every changed owner is weakly
   nonworse; and
3. every EFX failure is therefore against a residual target `P_m`.

If the compressed allocation is EFX, it is the required lexicographic
improvement.  If its response relation on `V` has an SDR, the selected
response edges are a release-compatible PI component: the desired cores are
disjoint and every other good is released into the residual pool within the
same owner union.

The identity `M=T\setminus S` is important.  When all four owners are active,
`V=T=N`.  Thus a rank-three response relation leaves exactly one residual
owner, a rank-two relation leaves two, and a full rank-four matching is
already a PI response SDR.  No inclusion-minimality assumption is required.

## Why maximum matching is necessary

Compressing only an inclusion-minimal deficient subset can leave a changed
target outside its owner union.  Any pre-existing wall against that target
survives.  This occurs exactly in the hardened weighted-Hall census: the
minimal defect `{c,s}<-{c}` can be paid, but the partial compression still
has walls against the fixed changed root target.  Compressing a maximum
matching of the whole active relation includes that root target and removes
the inherited walls.

## Single-residual recapture

Suppose `M={d}` and put `W=P_d`.  If the compression pays `d`, every wall is
against `W`.  If source `i` responds to `W` with common-safe desired core
`D subseteq W`, replace

\[
A_i,W\quad\text{by}\quad D,\ A_i+(W\setminus D). \tag{4}
\]

This recapture preserves completeness and release support.  Writing

\[
\gamma_d=v_d(W)-v_d(X_d)\ge0,
\]

it preserves payment exactly when

\[
v_d(D)-v_d(A_i)\le\gamma_d. \tag{5}
\]

If `i` lies outside the present owner union, use her released current bundle
in place of `A_i`; then (4) strictly grows `V`.  With four owners, growth is
finite.  Failure of (5) gives the strict terminal polarity

\[
v_d(D)>v_d(A_i)+\gamma_d. \tag{6}

Thus the corrected closure program has exactly three outcomes: EFX,
release-compatible PI, or the named strict recapture polarity (6).  Turning
(6) into a contradiction still requires a flower-specific reverse
inequality or root change.

## Adversarial evidence

The exact maximum-matching/recapture census closes every no-charity boundary
in both nondegenerate hardened models:

- first model: 243 boundaries, 77 immediate SDRs and 166 recapture SDRs;
- radius-two-excluded model: 81 boundaries, 17 immediate SDRs and 64
  recapture SDRs.

The enhanced CEGAR closes the former `sat_no_closure` model with a
maximum-matching compression.  After 21 installed cuts its next master check
reached the solver limit, so this is not a bounded UNSAT theorem.

## Claim boundary

This lemma proves the cap-free support, wall localization, rank/residual
identity, recapture operation, and strict failure polarity.  It does not
prove that every active flower relation has rank at least three, that every
single-residual recapture is payable, or that polarity (6) contradicts the
flower inequalities.  Consequently it does not yet prove the requested
weighted-Hall closure theorem, close `GG`, or prove four-agent/general EFX.

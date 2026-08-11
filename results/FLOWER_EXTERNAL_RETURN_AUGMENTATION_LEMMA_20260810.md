# Flower external return-augmentation lemma

**Date:** 2026-08-10

**Status:** cap-free analytic augmentation step; the low-return and internal
Hall-defect branches remain open

## Setting

Use the minimal-payment rotation and two-root response family.  Let

\[
W=B_q+L,
\qquad
R=(T_r\setminus L)+B_r,
\]

and suppose an external owner `a in {c,s}` is a most-envious response source
for `W`.  Thus the response edge into the evolved `q` target has source `a`,
incoming packet `L`, and prescribed release `T_q`.

## Return-augmentation theorem

Exactly one of the following proof branches is available.

1. **Ordinary return.** Agent `q` desires a subset of `X_a`.  Then the
   ordinary response `q -> a`, together with the root response and
   `a -> q`, is a release-compatible PI edge set.
2. **Low return.** Agent `q` satisfies
   \[
   v_q(X_a+R)\le v_q(X_q). \tag{1}
   \]
3. **Residual return or growth.** There is a nonempty packet `H subseteq R`
   such that either:
   - `q` is a most-envious response source for `X_a+H`, in which case the
     three internal responses close a PI edge set; or
   - a named source `b != q` responds to `X_a+H`.  If `b` is outside
     `{r,q,a}`, the owner component strictly grows.  If `b in {r,a}`, the
     failure is an explicit internal Hall defect rather than an open
     dependency.

The result is independent of `|R|` and does not choose a bounded move radius.

## Proof

If `q` desires a subset of `X_a`, choose an inclusion-minimal desired subset.
It is common-safe and supplies an ordinary edge from `q` into `a`.  On targets
`(r,q,a)`, select sources `(r,a,q)`.  The root edge consumes `T_q+f` and
releases `L+R`; the evolved-`q` edge consumes `L` and releases `T_q`; the
ordinary return consumes nothing.  Every incoming set is therefore supplied,
so the internal SDR is PI.

Suppose no subset of `X_a` is desired by `q`.  If (1) holds, the low-return
branch is established.  Otherwise finiteness gives an inclusion-minimal
nonempty packet `H subseteq R` with

\[
v_q(X_a+H)>v_q(X_q). \tag{2}
\]

If `X_a+H` is common-safe, (2) makes `q` a most-envious response source and
the same SDR `(r,a,q)` closes.  Its incoming sets are now `T_q+f`, `L`, and
`H`; the root releases both `L` and `H`, while the evolved-`q` edge releases
`T_q`.

If `X_a+H` is not common-safe, choose an inclusion-minimal subset of that
offer desired by some agent, and call one of its sources `b`.  This subset is
common-safe and supplies a response edge into `a`.  If `b=q`, the return SDR
again closes.  Otherwise `b` is the named non-`q` response in branch 3.
When the selected desired subset discards all of `H`, the same source gives
the parallel ordinary-envy consequence into `a`; otherwise the response
genuinely consumes a residual packet.  In both cases the next owner or the
internal Hall defect is explicit. \(\square\)

## Termination consequence for four owners

Starting from one external source `a`, a noninternal response can add only
the other external owner.  There is no fifth owner.  Hence repeated use of
the lemma cannot create an unbounded open-source chain.  Every surviving
dependency is reduced after at most one external augmentation to:

1. the low-return inequality (1) for one or both external owners; or
2. a closed Hall-deficient response relation whose missing representative is
   `q`.

These are now the two exact analytic cases required for a root flip.  The
16-partition nondegenerate adversary takes the residual-return branch and
closes with three internal SDRs.

## Verification and claim boundary

Release compatibility of the return SDR is covered by
[`flower_two_root_residual_split_release_audit.json`](flower_two_root_residual_split_release_audit.json),
which checks all 2, 6, and 24 internal response permutations.  The exact
adversarial realization is
[`residual_flower_two_root_partition_census.json`](residual_flower_two_root_partition_census.json).

This lemma proves finite source augmentation, not elimination of the final
low-return/internal-defect cases.  It does not yet close `GG` or prove
four-agent additive EFX.

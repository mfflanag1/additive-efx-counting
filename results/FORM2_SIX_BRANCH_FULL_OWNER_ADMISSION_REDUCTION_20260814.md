# Form-2 six-branch full-owner admission reduction

**Date:** 2026-08-14

**Status:** cap-free spanning-component and minimum-response reduction; the
signed base-margin interface to the full-owner theorem remains to be audited

## Six physical branches

Use the form-2 represented response cycle

\[
 r\to q\to s\to r
\]

and the unmatched owner's responses into `r` and `q`.  Choose one `d`
response, omit one represented-cycle response, reverse the other two, and
send singleton charity `p` to the omitted source.  These are the six branches
of `THREE_CYCLE_SIX_BRANCH_CHARITY_COMPLETION_LEMMA_20260813.md`.

Each branch has exactly four physical supplier pairs:

1. two edges forming a path through the three represented owners;
2. one edge attaching `d` to `r` or `q`; and
3. one edge attaching charity to the omitted represented owner.

Hence every branch graph is a spanning tree on

\[
                    \{\mathrm{charity},r,q,s,d\}. \tag{1}
\]

This is independent of values, packet cardinalities, and the allocation of
retained goods.

## Minimum failed response is common-safe

Suppose one branch pays all four owners but is not EFX.  Among every owner
and every subbundle of every final target that is strictly desired above that
owner's final utility, choose a core `C` of globally minimum cardinality,
with source `i`.

For any observer `k` and any `g in C`,

\[
                         v_k(C-g)\le v_k(Z_k).     \tag{2}
\]

Otherwise `C-g` is a strictly desired smaller core for source `k`, contrary
to the global cardinality choice.  Thus `C` is common-safe at the actual
post-transfer utility vector.  It is a genuine decorated response, not only
an unsafe blocker bundle.

Because the physical transfer support of the branch is already the spanning
tree (1), adjoining the source, target, core, release, and observer labels of
`C` cannot leave an owner outside the decorated component.  Every paid
non-EFX branch therefore enters the **full-owner** decorated-response layer
immediately.  The external-Hall recruitment theorem is unnecessary on this
route.

## Combined dichotomy

Together with `FORM2_SIX_BRANCH_PAYMENT_COMPRESSION_LEMMA_20260814.md`, every
disjoint-core form-2 state satisfies one of the following:

1. one of the six branches is complete EFX through exactly four edges;
2. a paid branch produces a current-common-safe full-owner decorated
   response on a four-edge spanning tree; or
3. all six branches fail owner payment, which is equivalent to

\[
\begin{aligned}
v_r(S)&>\Delta_r+v_r(p),\\
v_q(R)&>\Delta_q+v_q(p),\\
v_s(Q)&>\Delta_s+v_s(p).
\end{aligned}                                      \tag{3}
\]

Shared-target failure remains the previously certified double-margin capture
alternative.

## Exact remaining admission gate

The frozen saturation ledger excludes a new response label, support growth,
release-compatible PI, and strict same-record progress.  To invoke
`UNIVERSAL_FULL_OWNER_CHARITY_EXCHANGE_EXTRACTION_THEOREM_20260812.md` on
outcome 2, one statement-integrity implication still has to be checked:

> If the minimum response at the paid spanning-tree probe repeats an old
> source/core/target/release label, then the probe's signed owner margins and
> complete connected physical pool satisfy the exact component-wide
> base-margin separator and direct-safety hypotheses of the full-owner
> theorem at the same fixed record.

Graph connectivity, owner coverage, core safety, and the four-edge budget no
longer contribute uncertainty.  The unresolved issue is solely this signed
cross-state admission implication, plus elimination of (3) and the
double-margin overlap branch.

## Claim boundary

Proved: all six graphs are four-edge spanning trees; global minimum response
extraction is common-safe at the probe utilities; every paid non-EFX branch
therefore has a full-owner decorated component; and the exact three-outcome
reduction above is cap-free.

Not proved: the signed base-margin admission implication, contradiction of
the supplier-capture system (3), closure of double-margin overlap, the full
fixed-`U` theorem, or general EFX.

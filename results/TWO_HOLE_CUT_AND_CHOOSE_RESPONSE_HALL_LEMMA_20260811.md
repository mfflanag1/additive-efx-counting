# Two-hole cut-and-choose response-Hall lemma

**Date:** 2026-08-11

**Status:** cap-free conversion of non-root J-exhaustion; the root-facing
orientation is handled by the root-preserving selector, while 2-by-2
Hall-deficient termination remains open

## Two-source/two-hole state

Let `p_1,p_2` be represented sources holding pairwise-disjoint common-safe
desired cores `A_1,A_2`.  Let `d,j` be the other two owners and let `P` be
every remaining good.  Thus

\[
A_1\mathbin{\dot\cup}A_2\mathbin{\dot\cup}P
\]

is the complete owner-union pool.  Both represented sources are strictly
above their base utilities.

Choose one hole, say `d`, as divider.  Among all two-way partitions
`P=P_d dot union P_j`, choose one maximizing

\[
\min\{v_d(P_d),v_d(P_j)\}. \tag{1}
\]

Let `j` choose her preferred cell and give the other cell to `d`.

## Cut-and-choose theorem

The resulting partition is EFX for both holes.

For the divider, suppose the lower cell `L` strongly envies the higher cell
`H`.  With `g` a least-valued good of `H`,

\[
v_d(L)<v_d(H-g). \tag{2}
\]

Moving `g` from `H` to `L` makes both new cell values strictly exceed
`v_d(L)`, contradicting the maximin choice (1).  Hence the divider is EFX.
The chooser weakly prefers her selected cell to the other cell, so she is
envy-free and therefore EFX.

## Strict inherited potential

Suppose the pool comes from a one-hole state with old residual `W` and a
core `A` strongly envied by the divider `d`:

\[
v_d(W)<\tau_d(A).
\]

Let `g` be a least-valued good of `A`.  The trial partition

\[
(W+g,\ A-g)
\]

has both cells strictly above `v_d(W)`: positivity gives the first strict
inequality and strong envy gives the second.  Therefore the optimum in (1)
is strictly larger than `v_d(W)`.  Both cells of every maximizing partition
have value at least that optimum, so whichever cell the chooser leaves to
`d` satisfies

\[
v_d(P_d)>v_d(W).                                      \tag{3}
\]

Thus the conversion from a strongly envied one-hole state to two holes is
not potential-neutral.  It strictly increases the old hole's own value.

## Exact wall localization

Give `A_t` to `p_t` and the two cut-and-choose cells to `d,j`.  Then:

1. represented sources cannot fail EFX against either selected core, since
   they are above base and both cores are common-safe;
2. the two holes cannot fail EFX against each other's residual cells by the
   cut-and-choose theorem; and
3. every remaining wall is either a hole against a selected core or a
   represented source against a residual cell.

Thus the arbitrary two-sided compression star becomes a bipartite
two-core/two-residual wall graph.

If the response relation of the four displayed targets has an SDR, the
selected desired subsets are disjoint and every incoming good is supplied
inside the complete owner union, so the SDR is a release-compatible PI
component.  In particular, if the two represented sources can be matched to
the two residual targets and the two holes can be matched to the two core
targets, their union is an SDR.  A PI-free survivor must therefore miss a
matching on at least one side, expose a source-inactive wall, or carry an
inclusion-minimal deficiency-one witness in one of the two 2-by-2 blocks.

## J-exhaustion conversion

At J-exhaustion in the source-inactive repair lemma, the current missing
owner is `d`, the exhausted core source is `j`, and their combined goods are
exactly `A+W`.  Stop requiring `j` to remain represented.  Keep the other
two desired cores fixed and apply the cut-and-choose construction to
`P=A+W` with holes `d,j`.

The source-inactive premise contains `v_d(W)<tau_d(A)`, so (3) applies:
the old hole's cut-and-choose cell is strictly more valuable to her than
the residual she held before J-exhaustion.

If `j != r`, the anchored root `r` remains represented and strictly above
base.  Hence an EFX cut-and-choose endpoint is a valid strict lexicographic
flower improvement even if both holes are below base.  An SDR is PI; every
survivor has the localized 2-by-2 Hall boundary above.  The only
priority-sensitive exception is `j=r`, exactly the previously named
root-facing star.

No item cap is used.  The maximin partition exists because the allocation
set is finite.  When `j=r`, the root-preserving two-hole selector replaces
this unconstrained partition: it preserves `r` above base and yields either
a mutually EFX two-hole partition or an exact root-critical polarity.

## Claim boundary

This lemma removes non-root J-exhaustion as an unstructured unanimous
core-dominance terminal and replaces it by a cap-free two-hole
cut-and-choose response component with a strict inherited potential gain for
the old hole.  Together with the root-preserving selector, priority-valid
conversion now covers every exhausted source.  It does not prove that either 2-by-2
response block has a matching, show that every later compression
preserves that gain, eliminate source-inactive walls created by the
repartition, convert the root-critical polarity into a closing transfer,
close `GG`, or prove four-agent/general additive EFX.

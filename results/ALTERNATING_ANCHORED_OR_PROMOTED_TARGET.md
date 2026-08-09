# Alternating anchored-or-promoted target

**Date:** 2026-08-09
**Status:** all orders closed cap-free by a broader promotion; strict
same-offer refinement exactly refuted
**Scope:** the eight hard priority orders in the alternating two-large cell

## Rooted EFX equivalence

Let `a` own a singleton \(X_a=\{x\}\), and keep that singleton fixed.  Give
disjoint bundles \(Y_i\) to the other three agents, possibly leaving goods
unallocated.  Then \((\{x\},(Y_i)_{i\ne a})\) is EFX if and only if:

1. the three-agent allocation \((Y_i)_{i\ne a}\) is internally EFX; and
2. every active bundle is deletion-safe for `a`:

   \[
   v_a(Y_i\setminus\{g\})\le v_a(x)
   \qquad(i\ne a,\ g\in Y_i).
   \]

Indeed, these are exactly the comparisons among the three active agents and
from `a` to them.  Every comparison from an active agent to `a` is automatic
after deleting the singleton `x`.

This equivalence made a fixed-observer three-agent theorem a natural target.
That target is nevertheless false.

## Exact failure of each one-sided target

In the strict seven-good alternating atom, an **anchored** rival keeps the
first-priority singleton owner's bundle exactly unchanged and never gives
that agent another good.  Exact QF_LRA countermodels have no anchored
lexicographic escape in six of the eight hard orders:

\[
(p,s,q,r),(p,q,r,s),(p,q,s,r),
(s,p,r,q),(s,r,p,q),(s,r,q,p).
\]

Only `(p,s,r,q)` and its half-turn counterpart `(s,p,q,r)` force an anchored
escape in the atom.

A **promoted** rival instead replaces the root singleton by that root's
selected most-envious block: \(T_r\cup\{f\}\) for `p`, or
\(T_q\cup\{f\}\) for `s`.  The root then strictly improves automatically.
This promoted-only statement is also false in the atom for either root, even
when the other three agents may repartition all remaining goods arbitrarily.

Thus neither preserving the root nor fixing its canonical champion block is
a valid universal construction by itself.

## Exact atomic dichotomy

The two constructions are jointly sufficient in the seven-good atom:

> **Atomic anchored-or-promoted dichotomy.** For every one of the eight hard
> priority orders, the alternating structural premises force an EFX
> lexicographic improvement of one of the following two forms:
>
> 1. **anchor:** preserve the first singleton owner's bundle exactly and
>    improve the active three-agent suffix; or
> 2. **promote:** give the first singleton owner its selected top-plus-charity
>    desired block and allocate the remaining goods among the other agents.

This follows from the existing deletion-minimal atomic cores: every rival in
all eight hard-order cores has exactly one of these two root bundles.  Replaying
those restricted menus remains QF_LRA-UNSAT for every hard order.

The dichotomy is strictly sharper than the earlier all-rivals atomic theorem,
and the one-sided countermodels show that both branches are essential.

## Split-packet correction

The canonical two-branch statement is false once packets split.  For order
`(p,q,s,r)`, an exact eleven-good model has neither an anchored escape nor an
EFX escape promoting `p` to the one preselected desired block.  A binary
perturbation makes the model strictly positive and subset-nondegenerate.

The model is not an unrestricted obstruction.  Its EFX lexicographic escape
promotes `p` to a different desired subset of the same offer
\(X_r\cup\{f\}\), mixing one top and one bottom subgood with `f`.  In fact
that offer has six desired subsets in the refuting profile.  The exact audit
is frozen in
[`alternating_anchored_or_promoted_0321_nondegenerate_refutation_audit.json`](alternating_anchored_or_promoted_0321_nondegenerate_refutation_audit.json).

Thus "promoted" must mean promotion to **any** desired subset on the root
champion offer, not only the desired subset chosen when the base champion
graph was recorded.

## Repaired cap-free target

> **Packet anchored-or-promoted target.** In an arbitrary-bundle alternating
> state satisfying the exact champion topology and absence of all compatible
> cross-bottom families, every hard priority order admits either:
>
> - an anchored, external-observer-safe three-agent EFX improvement; or
> - a promoted-root EFX allocation whose root bundle is any desired subset
>   of the same root champion offer.

The promoted branch may repartition all residual packets among the other
three agents.  It must not be restricted to one whole residual block: that
stronger two-slot construction is exactly refuted.

The frozen eleven-good threshold refutation supports both branches rather
than refuting the canonical dichotomy.  It has anchored lexicographic escapes
and 287 EFX allocations with `p`'s selected promoted block fixed.  The newer
`(p,q,s,r)` profile is what forces the any-desired repair.

## Exact status of the repaired target

The first runs in this section used the original all-row packet ordering and
therefore searched a within-packet comonotone subcell.  This does not affect
their SAT refutations.  The root-flip UNSAT core has been replayed after the
symmetry correction and remains UNSAT because its analytic proof never used
the ordering restriction.  The undecided 1,142-rival run is retained only as
proof-mining provenance.

For order `(p,q,r,s)`, the canonical anchored-or-selected run was exact
UNSAT after 576 learned rivals.  Its certificate shrank to two allocations
and yielded the cap-free
[`root-flip lemma`](ALTERNATING_ROOT_FLIP_LEMMA.md).

For order `(p,q,s,r)`, the broader anchored-or-any-desired run learned 1,142
exact rivals through 17 completed models.  The next master returned
`unknown/canceled`; this is neither a theorem nor a refutation.  A narrower
variant that additionally forced the ordinary envier `r` to keep exactly
the singleton `y` is false: its terminal model has no such escape and no
desired promotion, but it has many broader anchored escapes in which `r`
receives a different bundle.

Therefore the live statement must retain the full external-observer-safe
three-agent anchored branch.  Neither a canonical desired set nor a fixed
envy-return bundle is universal.

## Next analytic gate

> **Anchored-or-any-desired extension lemma.** If the base is maximal among
> the EFX allocations that keep the first singleton owner fixed, then some
> desired subset on that owner's champion offer extends to an EFX allocation
> that promotes the owner.

This statement is false. In the eight-good `(1,1,2,1)` packet cell, an
independent exhaustive audit finds no anchored escape and no EFX escape
promoting `p` to any desired subset of `X_r+f`. Its smallest escape instead
promotes `p` to the cross-face desired bundle `B_r+{t_q^0}+B_q` and gives
`q` the complementary `{t_q^1,x}`. See
[`alternating_variable_extension_1121_refutation_audit.json`](alternating_variable_extension_1121_refutation_audit.json).

The cap-free
[`dual-reservoir trichotomy`](ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY.md)
now closes both `(p,s,q,r)` and `(p,q,s,r)`, plus both half-turns, for the
wider lexicographic maximality program.  Its third branch promotes the root
to a desired subset of the opposite reservoir rather than the original
champion offer, so it does not prove the stricter lemma displayed above.
Together with root flip and reservoir exchange, all eight hard orders are
closed.

The strict target is therefore exactly refuted. The broader
opposite-reservoir construction already admits the missing operation and
proves the alternating global-lex theorem, but not complete four-agent EFX.

## Strict-refinement reduction

The later
[`extension-or-handoff reduction`](ALTERNATING_EXTENSION_OR_HANDOFF_REDUCTION.md)
uses failure of both strict branches to prove a desired-set transversal,
common-safety of `B_r+B_q`, two strict threshold inequalities, and a boosted
moving-ceiling handoff reduction. The only surviving cap-free wall is an
`r`-desired subset of `X_r+B_q` that intersects every `p`-desired subset of
`X_r+f`. The exact eight-good profile realizes the failure beyond this gate;
larger blind rival pools are unnecessary.

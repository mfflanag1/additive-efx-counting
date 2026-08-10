# Charity-rooted hub-split obstruction lemma

**Date:** 2026-08-10

**Status:** cap-free analytic branching lemma; hub/partition selection remains
open

## Star operation

Let `(X,{f})` be an EFX allocation with unenvied charity under positive
additive valuations, and suppose every owner bundle used below is nonempty.
Choose a hub owner `h`, a nonempty packet `R subseteq X_h`, and a partition

\[
R=\mathbin{\dot\bigcup}_{k\in L}R_k
\]

into nonempty packets among distinct leaf owners `L subseteq N\{h}`. Form
the complete allocation

\[
Y_h=X_h\setminus R+f,\qquad
Y_k=X_k+R_k\quad(k\in L),
\]

leaving all other owners fixed. Assume

\[
v_h(f)>v_h(R). \tag{1}
\]

Then the hub strictly improves, every leaf strictly improves by positivity,
and every other owner is fixed. Thus `Y` Pareto dominates `X` if it is EFX.

## Exact wall classification

For an observer `i` and owner target `j`, put

\[
s_{ij}=v_i(X_i)-\tau_i(X_j),\qquad
\gamma_i=v_i(Y_i)-v_i(X_i)\ge0.
\]

Only the hub and leaf targets change. Therefore, if `Y` is not EFX, one of
the following exhaustive walls occurs.

### Hub wall

Some observer strongly envies `X_h\R+f`. Since

\[
v_i(Y_i)=v_i(X_i)+\gamma_i\ge v_i(X_i)\ge\tau_i(X_h),
\]

the target threshold strictly increases. The packet-for-charity threshold
polarity then forces

\[
v_i(f)>v_i(R). \tag{2}
\]

Taking a most-envious subset gives a generalized `(f|R)` edge into `h`; if
the desired subset discards `f`, it also gives the parallel ordinary envy
consequence. The edge releases all of `R`, plus any further discard.
If `X_h\R` is empty, the new hub target is the singleton `{f}`, whose EFX
threshold is zero, so a hub wall is impossible.

### Leaf wall

Some observer strongly envies `X_k+R_k`. Let

\[
m_i(X_k)=\min_{g\in X_k}v_i(g),\qquad
m_i(R_k)=\min_{g\in R_k}v_i(g).
\]

The exact threshold charge of inserting the packet is

\[
\kappa_i(k,R_k)
=v_i(R_k)+m_i(X_k)-
  \min\{m_i(X_k),m_i(R_k)\}. \tag{3}
\]

Indeed,

\[
\tau_i(X_k+R_k)-\tau_i(X_k)=\kappa_i(k,R_k).
\]

The wall is therefore possible only if

\[
\kappa_i(k,R_k)>\gamma_i+s_{ik}. \tag{4}
\]

Taking a most-envious subset gives the generalized `(R_k|empty)` edge into
`k`. In BCFF Definition 3.1 the label records the whole offered set `R_k`;
the corresponding discard set may contain goods from either `X_k` or `R_k`.
If the desired subset discards all of `R_k`, it also gives the parallel
ordinary envy consequence into `k`.

If no hub or leaf wall occurs, `Y` is complete EFX and Pareto improves `X`.

## Release compatibility and the Hall remainder

The incoming sets `R_k` of distinct leaf edges are disjoint, and the hub edge
releases all of `R`. The only other possible incoming set is `{f}`, which is
initially unallocated. Consequently, if a selection containing the hub edge
and the chosen leaf edges forms vertex-disjoint directed cycles on its target
owners, those cycles are automatically a BCFF PI edge set: their incoming
sets are disjoint and every one is initially unallocated or released by an
edge in the set. Ordinary envy edges have empty incoming sets and cause no
conflict.

Thus a blocked hub split leaves a sharply defined combinatorial remainder.
A directed wall cycle contradicts global maximality. Otherwise either a
wall source lies outside the current target set and must be added to the
transfer component, or the target-to-source incidence relation has a strict
Hall-deficient subset. A system of distinct representatives alone is not
claimed to be a PI cycle: its sources must close on the same target set.
This is the branching analogue of following one blocker along a path.

For a hub with exactly two leaves, the finite internal-source remainder is
classified in
[`THREE_TARGET_HUB_HALL_CLASSIFICATION_20260810.md`](THREE_TARGET_HUB_HALL_CLASSIFICATION_20260810.md).
The only fully internally blocked family not already containing a PI cycle
through the hub is the leaf-mutual pattern: the leaves block each other, at
least one leaf blocks the hub, and the hub is absent as an internal wall
source.

The scalar implications replay as QF_LRA-UNSAT in
[`charity_rooted_hub_split_obstruction_audit.json`](charity_rooted_hub_split_obstruction_audit.json).

## Flower consequence

After all one-recipient charity packet replacements are blocked, the exact
full-capture gate escapes by precisely this motif: `c` receives `f` and
sends one good to `r` and one to `s`. The lemma now converts every failure of
that motif into a hub edge, a leaf overload edge, an open wall source, or a
strict Hall-deficient wall-source set. The remaining proof obligation is
selecting `h,R`, and its partition from the flower's arbitrary packets so
that neither open-source growth nor Hall deficiency can persist.

## Claim boundary

The wall classification, insertion charge, and conditional PI/component
reduction are cap-free. The lemma does not prove existence of a hub split
satisfying (1), nor eliminate every open-source or Hall-deficient pattern. It
therefore does not close the flower or prove general additive EFX.

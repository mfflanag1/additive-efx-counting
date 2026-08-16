# Root-anchored compression-star lemma

**Date:** 2026-08-11

**Status:** cap-free monotone recapture theorem; the terminal cross-star
orientation remains open


*Convention note 2026-08-16 (`tau`).* This file uses `tau` **without defining it** (inherited), once, in (4). The use is
convention-agnostic: it needs only that `tau_d(A_i)` bounds the one-good deletions
of `A_i`, which both readings supply.

The two forms coincide **only under additivity**: for additive `v`,
`max_{g in Z} v(Z\{g}) = v(Z) - min_{g in Z} v(g)`, but for a merely monotone
cancelable `v` they are different functionals. Composing this file with one that
uses the other form is therefore sound only inside the additive class, where this
rung currently sits. The rung's live conflict —
`FLOWER_MINIMAL_PAYMENT_RESIDUAL_ROTATION_LEMMA_20260810` and
`FLOWER_RESIDUAL_WALL_PAYMENT_POLARITY_LEMMA_20260810` (additive form) against
`CROSS_STAR_HOLE_PIVOT_LEMMA_20260811` (max-deletion) — is recorded at section 8,
item 2 of
[`THREE_NONSINGLETON_CANCELABLE_CONSTRAINT_MAP_20260816.md`](THREE_NONSINGLETON_CANCELABLE_CONSTRAINT_MAP_20260816.md).
Nothing is broken today; the banner exists so the conflict cannot hide when the
rung's proofs are composed. **Labeling only**: no definition and no step in this
file is changed.

## The earlier root is never missing

Apply response compression to an all-owner Hall defect reached from the
two-root residual split. Its root target has the form

\[
Y_r=T_q+f+R_r. \tag{1}
\]

The displayed flower bundle

\[
D_r=T_q+f \tag{2}
\]

is common-safe and strictly desired by `r`, and it is contained in `Y_r`.
Hence `r` is a response source for target `Y_r`: edge `r -> r` may use the
desired core `D_r`. In particular `r` belongs to the response neighborhood
`S` of every all-owner defect.

Therefore the unique missing source `d` is never `r`. Every weighted
compression obstruction is in the sacrifice-eligible branch of the
lex-sacrificed response-compression lemma. If `d` is external, both `r,q`
receive desired cores and improve; if `d=q`, `r` improves before `q` in the
fixed priority.

## Aligned recapture strictly advances

Use a compressed state consisting of common-safe desired cores `A_i` for
`i in S` and residual `W` for missing source `d`. Suppose source `i`
responds to `W` with common-safe desired core

\[
D_i\subseteq W, \tag{3}
\]

and the sacrificed owner `d` strongly envies the **aligned** core `A_i`:

\[
v_d(W)<\tau_d(A_i)<v_d(A_i). \tag{4}
\]

Since `D_i subseteq W`, positivity gives

\[
v_d(D_i)\le v_d(W)<v_d(A_i). \tag{5}
\]

Perform the one-wall recapture

\[
Z'_i=D_i,
\qquad
Z'_d=A_i+(W\setminus D_i), \tag{6}
\]

leaving the other two cores fixed. Source `i` still strictly improves, and
the sacrificed owner's utility changes by

\[
v_d(A_i)-v_d(D_i)>0. \tag{7}
\]

Thus an aligned residual-response/core-wall pair strictly increases the
global recapture potential `v_d(W)`. The new state again has three
common-safe cores and one residual, so the same classification applies.
Because there are finitely many allocations, aligned recaptures cannot occur
indefinitely.

## Maximal cross-star orientation

Choose a state maximizing `v_d(W)` in the finite closure under
priority-valid recaptures. Let `R` be the source indices having a response
core `D_i subseteq W`, and let `L` be the indices whose assigned cores are
strongly envied by `d`. The aligned theorem gives

\[
R\cap L=\varnothing. \tag{8}
\]

Moreover maximality and nondegeneracy force, for every `i in R`,

\[
v_d(D_i)>v_d(A_i); \tag{9}
\]

otherwise (6) would increase the residual potential. For every `j in L`,
strong envy gives `v_d(A_j)>v_d(W)`. Hence every live cross pair obeys the
strict four-level order

\[
v_d(A_j)>v_d(W)\ge v_d(D_i)>v_d(A_i)
\qquad(j\in L, i\in R). \tag{10}
\]

With only three sources, the terminal obstruction is therefore one of the
finite incidence types

\[
(|R|,|L|)\in\{(1,1),(1,2),(2,1)\}, \tag{11}
\]

when both sides are nonempty, together with the two one-sided cases. This
is an incidence classification only, not a fixed item-size search. The next
root/order move needs to reverse (10), merge a cross pair, or eliminate one
of the one-sided cases.

The root support and scalar implications replay in
[`root_anchored_compression_star_audit.json`](root_anchored_compression_star_audit.json).

## Claim boundary

This lemma excludes `r` as the missing source and proves finite termination
of every aligned recapture. It does not eliminate a disjoint cross-star,
prove that both star sides are nonempty, select the final root/order move,
close the `GG` flower, or prove four-agent additive EFX.

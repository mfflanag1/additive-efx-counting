# Flower two-root residual-split response-Hall lemma

**Date:** 2026-08-10

**Status:** cap-free analytic component theorem; partition/payment selection
and open/Hall-deficient termination remain open

## Two-root split

Use the setting and minimal payment packet `L subseteq T_r` from the
minimal-payment residual rotation lemma.  Put

\[
R=(T_r\setminus L)+B_r.
\]

Choose distinct leaves `S subseteq {c,s}` and a disjoint partition

\[
R=R_r\mathbin{\dot\cup}R_0\mathbin{\dot\cup}
\mathop{\dot\bigcup}_{k\in S}R_k,
\]

where each leaf cell `R_k` is nonempty and the root-retained cell `R_r` and
charity cell `R_0` may be empty.  Form

\[
Y_r=T_q+f+R_r,
\qquad
Y_q=B_q+L,
\qquad
Y_k=X_k+R_k\quad(k\in S),
\]

fix every other owner, and leave `R_0` in charity.  Agents `r,q` strictly
improve by the residual-rotation lemma, and every leaf strictly improves by
positivity.  The residual charity is dominated by every owner: for any
`ell in L`, base EFX gives

\[
v_i(X_i)\ge v_i(X_r-\{\ell\})\ge v_i(R_0).
\]

## Response edges

Let `T={r,q} union S`.  For each proposed target `Y_j`, let `C_j` be the set
of all most-envious response sources relative to the base allocation.  Each
intended owner strictly desires her proposed bundle, so `C_j` is nonempty.
The corresponding generalized edges have the following full labels:

| target | incoming set | prescribed release |
|---|---|---|
| `r` | `T_q+f` | `L+(R\setminus R_r)` |
| `q` | `L` | `T_q` |
| leaf `k` | `R_k` | empty |

The label records the entire offered incoming set even when a selected
desired subset discards part of it; such discard only enlarges the release.

## Response-Hall theorem

Restrict each `C_j` to sources in `T`.

1. If the internal response relation has a system of distinct
   representatives, the selected edges form vertex-disjoint directed cycles
   on `T`.
2. Their incoming sets are pairwise disjoint: `T_q+f`, `L`, and the cells
   `R_k` lie in disjoint base/charity packets.
3. Every incoming set is supplied.  The good `f` is initially unallocated;
   the `q`-target edge releases `T_q`; and the `r`-target edge releases
   `L+(R\setminus R_r)`, including `L` and every `R_k`.

Hence the selected cycles are a BCFF Pareto-improvable edge set.  In a
PI-free state an internal SDR is impossible.  Hall's theorem then yields
either a target with only external response sources or an inclusion-minimal
strictly deficient target set.

If the displayed split `Y` is itself EFX, it is already a Pareto improvement.
If it is not, every new failure is against a changed target: all intended
owners weakly improve, unchanged targets remain safe, and the residual
charity is dominated.  Strong-envy wall observers must not be substituted
for the most-envious response sources in the Hall relation.

## Composition with the one-wall rotation

With `S=empty` and `R_r=empty`, the minimal-payment residual rotation proves that the only
possible wall is against `Y_q=B_q+L`.  Adding cells of `R` to its external
blockers is therefore the canonical Hall augmentation.  Each added leaf is
paid by positivity and consumes a packet already released by the `r` edge.
Retaining a cell `R_r` can instead pay a wall witnessed by the root itself;
the enlarged root target is then included in the same response-Hall family.
The process has three legitimate outcomes:

1. an EFX split;
2. an internal response SDR and hence a PI edge set; or
3. an open or Hall-deficient response boundary.

This eliminates the earlier release-support problem: unlike unrelated
bilateral edges, every response incoming packet is supplied by the same
two-root component.

The finite support audit
[`flower_two_root_residual_split_release_audit.json`](flower_two_root_residual_split_release_audit.json)
checks every internal response permutation with zero, one, and two leaves.
The proof itself is for arbitrary positive packet cardinalities.

## Claim boundary

The theorem proves response matching implies release-compatible PI closure
once a residual partition has been selected.  It does not prove that `R`
contains packets large enough to pay every open blocker, eliminate a strict
Hall deficiency, compose the other source/order cells, close `GG`, or prove
four-agent additive EFX.

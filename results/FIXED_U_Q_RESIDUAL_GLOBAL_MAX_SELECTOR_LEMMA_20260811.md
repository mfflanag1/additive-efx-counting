# Fixed-U q-residual global-max selector lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of every nonroot source-inactive `q` wall at
a globally selected fixed-`U` state; root-facing and unsafe-augmentation
branches remain open

## Global selector family

Fix the retained top support `U` and the permanent root anchor

\[
 A_r=T_q+f.                                         \tag{1}
\]

Let `F(U)` be the finite family of complete root-anchored compressed states
with the following properties.

1. `r` holds the common-safe desired core `A_r`; every other represented
   source holds a pairwise-disjoint common-safe desired core.
2. `q` is unrepresented and holds a distinguished residual cell `W`.
3. Every core/residual exchange respects the fixed removed-support condition
   `U`; in particular it never restores a good of `U` to the reduced mutual
   core.
4. `q` has no desired response into any active target.

The family may contain one, two, or three represented cores and any
corresponding number of residual cells.  This is intentional: a nonroot
J-exhaustion may lower response rank while preserving the root anchor.

If `F(U)` is nonempty, choose a state maximizing

\[
 v_q(W).                                             \tag{2}
\]

Use deterministic tie-breaking only after (2).  This is a single-owner
quantity, so it is invariant under independent row scaling and never
compares residual values belonging to different holes.

## Theorem

At the selected state, no source-inactive wall from `q` to a nonroot selected
core can be terminal.  Such a wall yields at least one of:

1. `q` becomes response-active and is represented by an anchor-constrained
   maximum matching;
2. an unsafe-core response augmentation;
3. an EFX lexicographic endpoint or release-compatible PI component; or
4. a contradiction to the maximal choice (2).

Consequently a surviving degree-zero `q` source-inactive wall must be
root-facing.

## Proof

Let `A_j` be a nonroot common-safe desired core held by source `j`, and
suppose `q` strongly envies it while remaining source-inactive:

\[
 v_q(W)<\tau_q(A_j)<v_q(A_j)<v_q(X_q).              \tag{3}
\]

Apply the source-inactive core/residual repair to `A_j+W`.

### Successful repair

At a successful common-safe leaf, `j` still holds a desired core and the new
`q` residual `W'` satisfies

\[
 v_q(W')>v_q(W).                                    \tag{4}

All other selected cores, including (1), are unchanged, and the exchange is
confined to `A_j+W`, so the fixed-`U` condition is preserved.  If `q`
responds to a new active target, the permanent-anchor activity dichotomy
represents her.  If she remains degree zero, the repaired state belongs to
`F(U)`, contradicting (2).  If the repaired core is unsafe, the repair lemma
supplies the named unsafe-core augmentation instead.

### J-exhaustion

At J-exhaustion, stop representing the nonroot source `j`, keep every other
core fixed, and apply two-hole cut-and-choose to `A_j+W`, with `q` as the
divider.  The inherited-potential clause gives the new `q` cell `W'` with

\[
 v_q(W')>v_q(W).                                    \tag{5}

The root anchor remains selected because `j != r`; lowering the number of
represented cores is permitted in `F(U)`.  An EFX endpoint closes by global
lex maximality, and an internal SDR is PI.  Otherwise, if `q` becomes
response-active, anchor-constrained matching represents her.  If she remains
degree zero, the new compressed state again belongs to `F(U)` and (5)
contradicts (2).

These alternatives exhaust successful repair and J-exhaustion.  Therefore a
nonroot source-inactive `q` wall cannot survive at the global selector.
\(\square\)

## Why this avoids the plateau refutation

The historical ledger failed because it allowed the missing owner to change
and only recorded nondecreasing “ever seen” coordinates.  Here the permanent
anchor first ensures that response-active `q` is never sacrificed.  Within
the remaining degree-zero branch, every relevant repair compares `q`'s old
and new cells in the same valuation row and does so strictly.  The selector
is global over all permitted response ranks, so rank descent cannot erase
the gain.

## Remaining boundary

The only source-inactive `q` wall not covered is the root-facing wall against
`A_r=T_q+f`.  Its J-exhaustion cannot release the permanent anchor and is
handled by the root-preserving selector, which may expose the named root-
critical top/floater or captured-bottom polarity.  Unsafe repaired cores and
residual-overlap hitting sets likewise return to their existing augmentation
branches.

This lemma does not eliminate those root-facing or unsafe/hitting-set
branches, prove that every later handoff stays inside `F(U)`, close `GG`, or
prove four-agent/general additive EFX.

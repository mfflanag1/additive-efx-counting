# Paid-anchor current-wall recurrence lemma

**Date:** 2026-08-11

**Status:** cap-free termination of every fixed-hole disjoint recapture by a
same-owner utility vector; only unsafe augmentation or an anchor-driven wall
survives

## Actual wall decomposition

Use a paid-anchor compression with missing owner `d`, represented sources
`S=N\setminus\{d\}`, common-safe desired cores `(A_i)_{i in S}`, and

\[
 W=Y_d\mathbin{\dot\cup}R,
 \qquad v_d(Y_d)\ge v_d(X_d).                      \tag{1}
\]

Suppose represented source `i` actually strongly envies the residual:

\[
 v_i(A_i)<\tau_i(W).                               \tag{2}
\]

This is stronger information than merely having some base-response core in
`W`.

## Disjoint current-improvement

Suppose

\[
 v_i(R)>v_i(A_i).                                  \tag{3}
\]

If `R` is common-safe, replace

\[
 A_i,W
 \quad\text{by}\quad
 R,\ A_i+Y_d.                                      \tag{4}
\]

The hole remains paid because its new residual contains all of `Y_d`.
Source `i` strictly improves relative to the current compressed state by
(3); every other represented source is unchanged. The goods are conserved
and the paid anchor remains intact.

Fix the missing source `d`, anchor support `Y_d`, represented source set `S`,
and the other protected supports. Order `S` deterministically and use

\[
 \Psi=(v_i(A_i))_{i\in S}                           \tag{5}
\]

as a lexicographic vector. Operation (4) changes exactly coordinate `i` and
increases it strictly. Because the ground set is finite, every coordinate
has only finitely many bundle values. Consequently a sequence of common-safe
disjoint current-improvements at fixed `(d,Y_d,S)` cannot recur.

If `R` satisfies (3) but is not common-safe, then `R` is a desired unsafe
target. Globally minimal desired-subset extraction supplies the existing
unsafe response augmentation instead of a recapture.

## Anchor-driven wall

The only remaining case is

\[
 v_i(R)\le v_i(A_i).                               \tag{6}

Let `g` be a least-`i` good of `W`. Expanding (2) gives

\[
 v_i(A_i)<v_i(Y_d)+v_i(R)-v_i(g),
\]

and therefore

\[
 v_i(Y_d)>v_i(A_i)-v_i(R)+v_i(g)\ge v_i(g)>0.      \tag{7}

Thus the wall is quantitatively anchor-driven: the paid pre-compression
target contributes more than the entire current residual deficit plus the
least-good threshold. Any desired response witnessing this wall must either
consume `Y_d` or arise from an unsafe subset already routed above.

## Consequence

At fixed hole and paid anchor, disjoint recapture is no longer a recurrence.
It strictly raises the represented-source vector (5), closes by EFX/PI, or
augments. A reset can revisit the state only by changing the hole/source set,
changing protected support, or consuming the paid anchor under (7). These
are precisely the outer rank/owner/support progress coordinates and the one
remaining anchor-splice operation.

## Verification and boundary

[`paid_anchor_current_wall_recurrence_audit.json`](paid_anchor_current_wall_recurrence_audit.json)
checks support conservation, automatic hole payment, strict single-coordinate
growth, finite-state nonrecurrence, and the anchor-driven inequality (7).

This lemma does not terminate unsafe augmentation after it changes the
response relation, convert every anchor-driven wall into an EFX/PI splice,
close a hole-changing reset, close GG, or prove four-agent/general additive
EFX.

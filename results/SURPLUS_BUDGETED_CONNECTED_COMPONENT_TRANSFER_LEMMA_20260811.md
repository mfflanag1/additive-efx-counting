# Surplus-budgeted connected-component transfer lemma

**Date:** 2026-08-11

**Status:** cap-free global endpoint lemma for arbitrary connected transfer
components; extraction of such a component from every terminal Hall polarity
remains open

## Transfer component and surplus budget

Let `(X,P)` be an EFX-with-charity allocation.  Reallocate finitely many
nonempty, pairwise-disjoint physical packets among owners, allowing the
charity bundle only to donate goods.  Denote the resulting allocation by
`(Y,P')`, where `P' subseteq P`, and let `C` be the nonempty set of owners
whose bundles change.

Join the old supplier of every moved packet to its new recipient.  Assume
that all moved packets form one nontrivial connected component on
`C union {charity}` after isolated vertices are discarded.  Branching,
multiple packets on one edge, and vertices of degree greater than two are
allowed.

For every weakly paid owner define her realized surplus

\[
 \Delta_i=v_i(Y_i)-v_i(X_i)\ge 0.                   \tag{1}
\]

A changed target `Y_j` is **surplus-budgeted for observer `i`** when

\[
 \tau_i(Y_j)-v_i(X_i)\le \Delta_i,                  \tag{2}
\]

or equivalently `tau_i(Y_j)<=v_i(Y_i)`.  External common safety is the
special case in which the left side of (2) is nonpositive, so no realized
surplus is spent.

Let `L subseteq C` be the set of changed owners who are not certified weakly
above their base utility.

## Endpoint theorem

Suppose:

1. every changed target `Y_j` is surplus-budgeted for every observer
   `i notin L` with `i != j`;
2. every owner in `C-L` is weakly paid, while every unchanged owner has
   surplus zero;
3. every owner `i in L` directly satisfies all final comparisons,
   \[
   v_i(Y_i)\ge \tau_i(Y_j)\quad(j\ne i),
   \qquad v_i(Y_i)\ge v_i(P');                       \tag{3}
   \]
4. in the fixed priority, every owner before the first changed owner is
   unchanged and that first changed owner strictly improves.

Then `(Y,P')` is EFX with charity and lexicographically dominates `(X,P)`.
Its moved packets form a single connected transfer component.

## Proof

Fix an observer `i`.  If `i in L`, all comparisons are exactly (3), while
the comparison with her own target is automatic.  Otherwise `i` is either
unchanged or weakly paid and has a nonnegative surplus `Delta_i`.  Against
a changed target belonging to another owner, (2) gives

\[
 v_i(Y_i)=v_i(X_i)+\Delta_i\ge\tau_i(Y_j).           \tag{4}
\]

Against an unchanged target, base EFX and nonnegative surplus give the same
conclusion.  Since `P' subseteq P`, positivity and base charity safety give

\[
 v_i(Y_i)\ge v_i(X_i)\ge v_i(P)\ge v_i(P').         \tag{5}
\]

Thus every EFX and charity comparison holds.  Premise 4 is precisely strict
lexicographic dominance.  Connectedness follows from the packet graph
hypothesis.  No restriction on item count, path length, degree, or packet
size is used.  \(\square\)

## Strict extension of the path lemma

The externally-safe path-transfer lemma is the special case in which the
packet graph is a path, its source is the only member of `L`, and every
other observer spends zero surplus on changed-target safety.  The present
form also covers forks and compensating gains.  Both extensions are
necessary: the hardest currently audited bounded flower profile has no
connected lex endpoint within three moved goods, but has the four-good
connected repair

\[
 \mathrm{charity}\to r,
 \qquad r\to q,
 \qquad r\to c,
 \qquad c\to s.                                     \tag{6}
\]

All four owners strictly improve.  Five observer-target pairs exceed their
old external-safety thresholds, but in every case the overshoot is smaller
than the observer's realized surplus.  Thus (6) is an immediate global-
maximality contradiction even though it is neither a path nor externally
common-safe target by target.  Its exact additive replay is recorded in
[`surplus_budgeted_connected_component_transfer_audit.json`](surplus_budgeted_connected_component_transfer_audit.json).

## Consequence for the fixed-`U` recurrence

A terminal recurrence no longer has to be linearized into a single source-
to-sink path or preserve every base threshold separately.  It is enough to
assemble retained response packets into one connected supplier graph and
show that each owner's net gain pays the total threshold overshoot she
actually faces.  In particular, one physical supplier may compensate two
Hall holes simultaneously, and gains elsewhere in the component may absorb
new target tails.

This changes the live packet-selection target.  The required inequalities
are the observer-indexed slack balances

\[
 v_i(Y_i)-v_i(X_i)
 \ge
 \max_{j\ne i}\bigl(\tau_i(Y_j)-v_i(X_i)\bigr)_+,   \tag{7}
\]

not common safety of every changed target.  Equation (7) is invariant under
independent positive row scaling and therefore avoids the defect in the raw
cross-owner residual potential.

## Claim boundary

This lemma proves the EFX and lexicographic endpoint after the component and
its surplus certificates are supplied.  It does not prove that every
source-inactive or hitting-set polarity supplies those packets, establish
generalized PI-freeness or global lex maximality of the frozen profile,
close `GG`, or prove four-agent/general additive EFX.

# Surplus-budgeted charity-exchange component lemma

**Date:** 2026-08-11

**Status:** cap-free endpoint theorem allowing charity to receive replacement
goods; universal extraction from the full-owner separator remains open

## Exchange component

Let `(X,P)` be an EFX-with-charity allocation.  Reallocate pairwise-disjoint
physical packets among owners and charity to obtain `(Y,P')`, where `P'` is
nonempty but need not be a subset of `P`.  Charity may both donate and
receive.  Assume the moved-packet graph has one nontrivial connected component
on the changed owners together with charity whenever charity changes.

For every changed weakly paid owner put

\[
 \Delta_i=v_i(Y_i)-v_i(X_i)\ge0.                  \tag{1}

\]

Let `L` contain changed owners not certified weakly above base.

## Endpoint theorem

Suppose:

1. every changed owner target `Y_j` is surplus-budgeted for every observer
   `i notin L`, `i!=j`:

   \[
    \tau_i(Y_j)-v_i(X_i)\le\Delta_i;              \tag{2}
   \]

2. the final charity is also surplus-budgeted for every `i notin L`:

   \[
    v_i(P')-v_i(X_i)\le\Delta_i;                  \tag{3}
   \]

3. every `i in L` directly satisfies every final owner-target comparison and
   charity safety:

   \[
    v_i(Y_i)\ge\tau_i(Y_j)\ (j\ne i),
    \qquad v_i(Y_i)\ge v_i(P');                   \tag{4}
   \]

4. every unchanged owner has zero surplus, every owner outside `L` is weakly
   paid, and the first changed owner in the fixed priority strictly improves.

Then `(Y,P')` is EFX with charity and strictly lexicographically dominates
`(X,P)`.  Its packets form one connected charity-exchange component.

## Proof

For `i notin L`, (1)--(2) give

\[
 v_i(Y_i)=v_i(X_i)+\Delta_i\ge\tau_i(Y_j)         \tag{5}

\]

against every changed target.  Base EFX plus nonnegative surplus handles
unchanged targets.  Unlike the donation-only lemma, charity safety no longer
follows from `P' subseteq P`; it follows exactly from (3):

\[
 v_i(Y_i)=v_i(X_i)+\Delta_i\ge v_i(P').           \tag{6}

\]

Owners in `L` satisfy the same comparisons directly by (4).  Thus the final
allocation is EFX with charity.  Premise 4 is strict lexicographic dominance,
and connectedness is the packet-graph premise.  No item, packet, or value cap
is used.  \(\square\)

## Exact necessity

The fixed-U global audit supplies a strict Pareto-improving instance of this
lemma in which

\[
 P=\{f\},\qquad P'=\{bc\_0\}.                     \tag{7}

\]

Its single connected component contains charity and all four owners and has
directed cycles.  No charity-rooted outward tree succeeds on the same profile.
Hence allowing (7) is not cosmetic: it is the smallest operation presently
known to separate the full global premise from the local tree countermodel.

## Verification and boundary

[`surplus_budgeted_charity_exchange_component_audit.json`](surplus_budgeted_charity_exchange_component_audit.json)
checks all owner-target and charity-budget implications symbolically and
links the exact fixed-U witness.

This lemma proves the endpoint once exchange packets and budgets are supplied.
It does not extract them from every repeated full-owner GG separator, prove
the universal connected-splice theorem, close GG, or prove four-agent/general
additive EFX.

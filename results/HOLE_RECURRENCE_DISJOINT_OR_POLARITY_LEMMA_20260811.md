# Hole-recurrence disjoint-or-polarity lemma

**Date:** 2026-08-11

**Status:** cap-free recurrence support theorem; reversal of the terminal
hitting-set polarity remains open

## Simple recurrence

The root-anchored compression never uses `r` as its missing source.  Hence a
first repeated hole contains a simple directed owner cycle of length two or
three among `{q,c,s}`.  Write its required response edges as

\[
 i_0\longrightarrow i_1,
 i_1\longrightarrow i_2,
 \ldots,
 i_{k-1}\longrightarrow i_0,                         \tag{1}
\]

where `k` is two or three.  Edge `i_t -> i_{t+1}` has a finite nonempty
family of common-safe desired cores contained in the corresponding target
packet `T_t`.

Because the edges may have been exposed at different pivot states, cores
chosen from the `T_t` need not be physically disjoint.  This is the only
support issue preventing the owner cycle (1) from immediately being a PI
component.

## Disjoint-core exploration

Process the edges of (1) in cyclic order.  After choosing pairwise-disjoint
cores `D_0,...,D_{t-1}`, put

\[
 H_t=D_0\mathbin{\dot\cup}\cdots\mathbin{\dot\cup}D_{t-1}.
\]

If `T_t-H_t` contains a common-safe desired core for `i_t`, choose an
inclusion-minimal one as `D_t` and continue.  Since the cycle has at most
three edges, the exploration has one of three outcomes after at most three
choices.

### Disjoint completion

All `D_t` are pairwise disjoint.  Every cycle source receives a common-safe
bundle strictly preferred to her base bundle.  Inspect the suppliers of the
physical goods in one fixed release reference state.

If every incoming good is supplied by an owner in the cycle component, the
cores form a release-compatible PI component.  If some incoming good is
supplied outside that component, adjoining its supplier strictly grows the
owner union.  This qualification is essential because the response edges
of a dynamic recurrence may have been exposed in different pivot states;
the target labels alone do not prove common release support.  With four
owners, strict supplier growth can occur only finitely many times.

### First overlap obstruction

For the first failed edge, `T_t-H_t` contains no **common-safe** desired
subset for `i_t`.  If in addition

\[
 v_{i_t}(T_t\setminus H_t)\le v_{i_t}(X_{i_t}),       \tag{2}
\]

then the original edge is live, so
`v_{i_t}(T_t)>v_{i_t}(X_{i_t})`.  Subtraction gives the exact hitting-set
polarity

\[
 v_{i_t}(T_t\cap H_t)
 \ge v_{i_t}(T_t)-v_{i_t}(X_{i_t})>0.                \tag{3}
\]

Thus overlap cannot merely stall the recurrence: the previously used
support captures at least the entire strict target surplus in the blocked
source's valuation row.

If instead the left side of (2) is strictly above base, finiteness supplies
an inclusion-minimal desired subset `D subseteq T_t-H_t`.  It is not
common-safe, or it would have continued the exploration.  Hence some
observer fails a base EFX threshold against `D`; choosing a most-envious
source gives the unsafe-core response augmentation used by the
core/residual repair lemma.  This is a third outcome—component growth—not a
hitting-set polarity.  The distinction is necessary: value above base alone
does not imply common safety.

If the response cores are inclusion-minimal and a particular good `g`
belongs to two of them, that good is critical in each corresponding row:

\[
 v_i(D_i-g)\le v_i(X_i)<v_i(D_i),
 \qquad
 v_i(g)\ge v_i(D_i)-v_i(X_i)>0.                     \tag{4}
\]

Equation (4) is the atomic form of (3).

## Composition consequence

Combine this lemma with the two-by-two response-Hall normal form.  Every
priority-valid lower-dimensional hole recurrence now yields either:

1. a release-compatible PI component;
2. strict owner-union growth from an outside physical supplier;
3. a response augmentation from an unsafe disjoint desired subset;
4. a source-inactive loss band from an empty wall target; or
5. the overlap/hitting-set polarity (3), possibly accompanied by the
   root-critical least-good polarity from the root-preserving selector.

No item bound occurs.  The remaining theorem step is to use minimal payment,
root capture, or global lexicographic maximality to reverse (3).  Merely
observing (3) is not a contradiction because different recurrence edges may
use different valuation rows.

## Claim boundary

This lemma proves disjoint PI closure or strict supplier growth,
unsafe-core augmentation, or an exact strict overlap certificate for every
simple repeated-hole owner cycle.  It does not prove that every dynamic
pivot sequence preserves the same target packets, close the response
relation after owner-union growth, terminate repeated unsafe-core
augmentations, reverse the hitting-set polarity, eliminate a
source-inactive loss band, close `GG`, or prove four-agent/general additive
EFX.

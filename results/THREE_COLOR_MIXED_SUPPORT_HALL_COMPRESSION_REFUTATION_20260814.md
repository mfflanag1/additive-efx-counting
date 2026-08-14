# Three-color mixed-support Hall-compression refutation

**Date:** 2026-08-14

**Status:** exact positive-additive local counterexample; refutes compression
from PI-freeness and common-safe response cores alone, not the full fixed-`U`
theorem

## Three distinct labels

For a good in a response core, distinguish:

1. its base owner in `X`, which controls generalized-PI closure;
2. its frozen physical supplier in `Y`, which controls the theorem's edge
   count; and
3. its target holder in the later response state `Z`.

These labels need not agree.  A support-drainage theorem stated only in base
owners cannot by itself bound frozen-supplier-to-recipient pairs.

## Exact response family

Use owners `0,1,2,3`, with missing response source `0`.  Let the three later
targets `1,2,3` contain pairwise-disjoint cores desired respectively by
sources `2,3,1`:

\[
 D_1=\{x_{01},x_{11}\}\to2,
 \quad D_2=\{x_{02},x_{22}\}\to3,
 \quad D_3=\{x_{03},x_{33}\}\to1.              \tag{1}
\]

Every displayed good is base-owned by owner `0`.  Its first subscript gives
its frozen `Y` supplier, so the supplier sets are

\[
 \sigma(D_1)=\{0,1\},\qquad
 \sigma(D_2)=\{0,2\},\qquad
 \sigma(D_3)=\{0,3\}.                           \tag{2}
\]

Give each named source floor `10` and values `6,5` for the two goods of its
core.  Give it value below `1` for every other displayed good.  Then each
core is strictly desired at value `11`, while every proper subcore has value
at most `6`.  Thus each is inclusion-minimal.  For every other observer, set
both item values in every core to any positive number at most its floor.
The three cores are common-safe.

## PI-freeness of the displayed family

For every nonempty represented source set `W subseteq {1,2,3}`, every chosen
core contains only goods base-owned by `0 notin W`.  Hence no selected
subfamily is closed over its sources, and the closed disjoint-core
characterization produces no generalized PI family from these responses.

This does not assert that a complete ambient instance has no other PI cycle.
It proves that the displayed response-core premises plus their exact base
supports do not force one.

## Physical edge obstruction

Because neither singleton subcore is desired, paying all three represented
sources through these responses requires both supplier components of every
core.  Reversal uses exactly

\[
 \{0\to2,1\to2,
   0\to3,2\to3,
   0\to1,3\to1\},                               \tag{3}
\]

six distinct frozen-supplier pairs before allocating charity.  No selection
of one desired subcore per source can reduce (3), because the full two-good
core is the unique desired subcore in each target.

Therefore the implication

> PI-free disjoint common-safe desired cores for three represented sources
> admit reversal on at most three frozen-supplier pairs

is false.

## Consequence and boundary

Any successful proof of the active theorem must use relations between base
ownership, frozen `Y` provenance, and the later target moves—specifically the
signed fixed-`U` ledgers, support growth, return cancellation, or decorated
recurrence.  Base-support drainage and Hall matching alone cannot establish
the physical edge bound.

Proved: an exact six-good positive-additive local response family with
minimal common-safe cores, no closed represented-source PI subfamily, and a
six-pair mandatory reversal.  Not proved: realization inside all fixed-`U`
premises, absence of other responses/PI cycles, failure of every arbitrary
four-edge EFX allocation, or refutation of the active theorem.

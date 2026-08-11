# Fixed-U global-lex charity-exchange exclusion

**Date:** 2026-08-11

**Status:** exact exclusion of the fixed-U tree countermodel by a connected
cyclic charity-exchange Pareto improvement

## Full global-premise decision

The fixed-U source-margin countermodel proves that the frozen local flower
premises do not force an EFX-improving charity-rooted transfer tree.  To test
whether it could satisfy the actual GG premise, the global audit optimizes
over every assignment of all eighteen goods to the four owners or charity,
subject only to:

1. the final allocation is noncomplete;
2. it is EFX for every observer and target;
3. every owner weakly dominates the final charity bundle; and
4. it lexicographically improves the displayed base in priority
   `(r,q,c,s)`.

This is one exact global allocation decision, not a bounded packet-topology
menu.  Z3 returns `SAT`, and an independent exact-rational replay verifies
the allocation.

## Exact Pareto-improving escape

The base utilities are

\[
 (117,131,192,58)/256
\]

for `(r,q,c,s)`.  The returned noncomplete EFX allocation has utilities

\[
 (137,214,288,59)/256.                             \tag{1}

\]

Thus every owner strictly improves.  The final charity contains the single
good `bc_0`, while the old charity good `f` moves to owner `r`.

The transfer graph moves eight goods and has one nontrivial component on

\[
 \{\mathrm{charity},r,q,c,s\}.                    \tag{2}

\]

It contains directed cycles, including reciprocal transfers between `c,q`
and between `q,s`.  Therefore it is outside every outward charity-rooted tree
enumerated by the local countermodel audit.

## Smallest missing operation

The earlier connected-component endpoint required charity only to donate:

\[
 P'\subseteq P.                                    \tag{3}

\]

The exact escape violates (3): charity donates `f` and receives a replacement
good from `q`.  This exposes the smallest missing packet operation:

> allow a connected surplus-budgeted component to exchange the charity good,
> and charge the final charity bundle against each observer's realized
> surplus just like a changed target.

The accompanying charity-exchange endpoint lemma proves this operation
cap-free.  Hence the strongest current local countermodel does not survive
the full global-lex premise; it points to a cyclic charity exchange rather
than refuting the repeated-support theorem.

## Verification and boundary

[`fixed_u_global_lex_premise_audit.json`](fixed_u_global_lex_premise_audit.json)
contains the exact allocation, utilities, transfer edges, connected component,
and source hashes.  Its replay re-solves the complete allocation formula and
checks the witness with exact `Fraction` arithmetic.

This excludes one exact adversarial profile.  It does not prove that every
full-owner base-margin separator admits a charity exchange, close the
repeated-support theorem, close GG, or prove four-agent/general additive EFX.

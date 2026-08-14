# Global retired-root-support ledger: frozen composition contract

**Date:** 2026-08-13

**Status:** frozen theorem contract; resolved by the global composition
theorem, with typed `T_L^*` left as the declared terminal

## Base and augmented state

Fix the positive, nondegenerate four-agent additive GG instance and its
globally fixed-priority lexicographically maximal partial EFX base `X`.
An augmented state is

\[
 \mathsf S=(Y,P,r,\alpha,F,\Sigma,M,h,\mathcal R,L,\mathcal C),       \tag{1}
\]

where:

- `(Y,P)` is the current allocation and charity;
- `r` is the current proof root;
- `alpha` is the complete **physical** anchor label: root, physical anchor
  support, anchor supplier, and orientation;
- `F` is the separately typed current protected-floor vector;
- `Sigma` is the full signed decoration relative to `X`;
- `M,h,mathcal R` are the selected matching, hole, and complete response /
  release record;
- `L` is a monotone set of labeled retirements
  `(alpha,g,s,F_ret)`, meaning that good `g` was removed from the root target
  under physical label `alpha`, paid to source `s`, and certified against the
  retirement-time floor snapshot `F_ret`; and
- `mathcal C` is the collision-provenance component of the complete response
  record: subsequent attempted consumptions of a retired packet, including
  its holder, recipient, candidate support, and protected floor. Inserting a
  member is accompanied by adopting the corresponding extracted/tested
  response coordinate; it is not an independent visit counter.

The label `alpha` does **not** change merely because the current floor vector
changes. Define

\[
 L_\alpha=\{g:\exists s,F^{\rm ret}\ (α,g,s,F^{\rm ret})\in L\}.
\]

Thus a good remains retired under the same physical anchor label across all
later floor changes. Since the ground set and owner set are finite and every
floor is the value of a bundle in a fixed valuation row, the family of
complete states in (1) is finite.

The ledger never deletes history. A good may move later; that move is not
called an unretirement. It is recorded in `mathcal C`, and its payment and
release compatibility must be proved.

The typed vector `F` distinguishes current, base, threshold, direct-safety,
and strict-priority floors. Every candidate advertised as a possible
lexicographic contradiction includes the earlier strict owner/root floor;
weak payment of later owners is recorded as weak and handled by the
equality-critical branch.

## Admissible transition

An admissible transition is one of the actual operations used by the
`G0--G10` composition: root/orientation reset, minimal-response extraction,
root-sourced connected transfer, anchored response matching, source-inactive
repair, root or bottom fork, paid splice, exact-response saturation,
rank-four path/cycle selection, deletion-return, recapture, hole pivot,
two-hole normalization, anchor exchange, or enlarged-root sacrifice return.

It is not admissible merely because it respects a new ledger convention.
Every source, floor, safety, matching, physical disjointness, and release
premise of the original operation must still hold after ledger normalization.

## Exact target

For every admissible transition from an augmented `G0--G10` state, prove at
least one of:

1. an explicit EFX allocation lexicographically above `X`;
2. a release-compatible PI cycle on pairwise-disjoint desired cores;
3. strict growth of `L` or another declared finite signed-support coordinate
   that cannot be reset at fixed `L`;
4. a valid root/anchor exchange with exact supplier releases and a strict
   finite label transition;
5. entry into the explicitly typed global splice class
   `T^dagger=T_0^* dot-union T_L^*`, where `T_0^*` is an exact generic `T*`
   recurrence reached before any retirement and
   `T_L^*=T_{L,perp}^* dot-union T_{L,times}^*` is the post-ledger class. The
   parked subtype `T_{L,perp}^*` has nonempty retired support disjoint from
   every active selector/release support; the collision subtype
   `T_{L,times}^*` carries a named retired packet, its supplier, and an exact
   payment-capture or response-collision certificate.

The theorem must show selector availability. It may not define a transition
away by forbidding a retired good.

## Ledger collision and the proposed smaller terminal

Suppose an original transition would give candidate packet `A` to source
`s`, with required floor `b_s`, and would consume

\[
 K=A\cap L_\alpha\ne\varnothing.                              \tag{2}
\]

Put `A^-=A-K`. Deletion preserves target safety. If `v_s(A)>b_s`, exactly
one scalar branch holds:

\[
 v_s(A^-)>b_s,                                                   \tag{3}
\]

or

\[
 v_s(K)\ge v_s(A)-b_s>0.                                       \tag{4}
\]

If instead `v_s(A)=b_s`, positivity gives the equality-critical certificate

\[
 v_s(A^-)=b_s-v_s(K)<b_s.                         \tag{5}
\]

It need not produce a desired response and is recorded separately.

Equation (3) is only a candidate normalization: every typed floor and every
owner-target comparison must be recomputed because cancellation can change
both incoming and outgoing retired transfers in one row.
Equation (4) is a **retired-packet capture**, not by itself a closing leaf.

Define `T_0^*` as a generic exact `T*` record with `L` empty. For nonempty
`L`, define the parked-support subtype `T_{L,perp}^*` to require an exact
generic `T*` recurrence in which every member of the complete active
selector/release pool is disjoint from `L_alpha`; all retired goods therefore
remain with their recorded current holders throughout the recurrent move.

Define the collision subtype `T_{L,times}^*` to require, in addition to the
generic exact `T*` record:

1. a nonempty `K` with retirement provenance
   `(alpha,K,s_0,F_ret)` under the same physical label, irrespective of the
   current floor vector;
2. one of four exact collision certificates:
   (a) capture (4) with a repeated retired-hitting response,
   (b) equality-critical certificate (5) when no separately proved
   sacrifice/root handoff applies,
   (c) a repeated response whose support intersects `K`, or
   (d) a repeated ledger-free response extracted from the actual normalized
   allocation after the original selector collided with `K` and failed its
   EFX/release test;
3. full current-holder and supplier labels; and
4. failure of the original canonical ledger-free realization at the same
   protected floors, whether by a floor, EFX-comparison, or release wall.

Put

\[
T_L^*=T_{L,\perp}^*\mathbin{\dot\cup}T_{L,\times}^*.
\]

Each post-ledger subtype is strictly structured: the first certifies a
nonempty inert parked support against the complete selector pool, and the
second carries the exact collision certificate. Generic `T*` records with
empty `L` belong to neither.

The global output class is

\[
 T^\dagger=T_0^*\mathbin{\dot\cup}T_L^*.
\]

It is a proper **certified** subclass of the augmented generic `T*` record
space: a nonempty-ledger generic record belongs only after the complete active
pool is audited and either (i) every selector/release avoids the ledger, or
(ii) a collision carries the packet, provenance, failed canonical
normalization, and typed certificate above. Before the first peel, the ledger
condition is vacuous and an original exact `T*` terminal is recorded as
`T_0^*`; after the peel, only `T_L^*` is allowed.

## Counterexample standard

A refutation must give exact positive-additive data satisfying the complete
GG import, global lexicographic maximality of `X`, full signed provenance,
all transition premises, and a state in which every valid continuation must
reuse retired support while all five outcomes fail. A local scalar capture,
an abstract transition graph, or an existing rational stress witness lacking
global maximality is not a refutation.

## Resolution of the load-bearing gate

The scalar deletion/capture dichotomy is immediate. The physical
**retired-packet return compensation lemma** is resolved by canonical
cancellation plus complete floor/comparison recomputation: when a later
operation needs `K`, it is left with its current holder, and success executes
the normalized transition while failure produces a genuine extracted/tested
response coordinate, a root/anchor operation, or the full `T_L^*` record.
The transition audit composes this routing at every collision row.

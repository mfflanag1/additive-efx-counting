# Allocated-E seven-endpoint bounded dichotomy

**Date:** 2026-08-13

**Status:** dual-verified exact bounded theorem; cap-free reduction now isolates a strict hidden-minimum split

## Exact theorem

For every positive-rational valuation profile in the twelve-atom allocated-`E`
R3 cell encoded by `build_master(2)`, at least one of the following holds:

1. there is a closed pairwise-disjoint family of common-safe desired cores,
   hence a generalized PI; or
2. one of seven explicit complete allocations is EFX.

Use the named support packets

\[
A=\{a_0,a_1\},\ H=\{h\},\ Q=\{j,k,q_0\},\
E=\{l,e\},\ W=\{m,g_q,g_r\},\ P=\{p\}.
\]

The bundle order is `(r,q,d,s)`.

| Endpoint | Complete allocation | Support edges |
|---|---|---|
| `Z1` | `({a0,a1},{j,k,q0},{h,m,gq,gr,p},{l,e})` | `c->d, r->d` |
| `Z2` | `({a0,a1},{j,k,q0},{h,l,m,gq,gr},{e,p})` | `c->s, r->d, s->d` |
| `Z3` | `({a0,a1},{j,k,q0},{l,m,gq,gr},{h,e,p})` | `c->s, r->s, s->d` |
| `Z4` | `({a0},{j,k,q0},{a1,h,m,gq,gr,p},{l,e})` | `c->d, r->d` |
| `Z5` | `({a1,h,k,q0,p},{j,gq,gr},{a0,m},{l,e})` | `c->r, d->q, q->r, r->d` |
| `Z6` | `({a0,m},{a1,h,k,q0,p},{j,gq,gr},{l,e})` | `c->q, d->r, q->d, r->q` |
| `Z7` | `({a0,p},{j,m,gq},{a1,h,k,q0,gr},{l,e})` | `c->r, d->q, q->d, r->d` |

Thus every generalized-PI-free profile in this declared cell has a complete
EFX allocation using at most four support-provenance packet edges.

## Proof record

The exact dynamic producer scanned the complete 93,480-member nonempty-owner
menu and terminated UNSAT after 46,683 generalized-PI cuts and 143 lazy
allocation cuts:

- `allocated_e_form2_all_allocation_atom_cegar.json`, SHA-256
  `a15f0d3b159f2390736b4f32dbc76f592fb01a0db72c2032c90215d867bc8496`.

An independent replay rebuilt desired-core predicates using literal EFX-tail
minima rather than the producer's min-free expansion, used direct allocation
formulas, validated the full resume chain, and again returned UNSAT:

- `allocated_e_form2_all_allocation_unsat_audit.json`, SHA-256
  `01a68dacd8a8ce45dafd1d30689e9edf2be8f18d2132783b8a6a9a4fa37e9106`.

Assumption-core extraction and solver minimization reduced the certificate to
425 PI clauses, 277 desired-core predicates, and the seven allocations above:

- `allocated_e_form2_all_allocation_minimized_unsat_core.json`, SHA-256
  `8c57f349175f4c9c9b68f4e1da8b39ac7b7a8e102f6cdc576382522259575314`.

The minimized core was independently rebuilt with literal tails and direct
allocation formulas and again returned UNSAT:

- `allocated_e_form2_all_allocation_minimized_unsat_core_audit.json`, SHA-256
  `f6377dfd16d39cf3096e0a57f8f98aa1f7d5cd195deaf07a199eeb48b3f46d23`.

The core uses only three- and four-owner PI families: 84 on `{d,q,r}`, 11 on
`{q,r,s}`, 51 on `{d,q,s}`, 49 on `{d,r,s}`, and 230 on all four owners. No
one- or two-owner family is needed.

## Basic interpretation

Whenever an adversary makes all seven endpoints fail EFX, the exact R3
premises force three or four owners to possess mutually disjoint desired
bundles drawn only from their closed owner/charity support. Rotating those
bundles is a generalized PI. Hence a PI-free adversary cannot make all seven
fail. The bounded object is a seven-endpoint disjunction, not one universal
transfer topology.

## Cap-free interface after the EFX-2 packet lemmas

The companion GG analysis proves two facts that can be imported without
assuming its unfinished recurrence theorem:

1. a proper recipient-feasible split physically separates the two parts of a
   contested packet, so a target-local minimum response cannot reassemble the
   whole packet; and
2. when the packet holder is a later sacrifice-eligible owner, holder payment
   is unnecessary—preserving the earlier strict root suffices.

Consequently later-owner multi-good refinements of the seven endpoints route
to strict packet-support reduction, PI/rank progress, or the already isolated
root/protected gate. Only recipient-indivisible packets and root/protected
holders remain load-bearing.

## Exact remaining lemma

> **Seven-endpoint physical-tail/anchor lemma.** In every saturated
> root-facing R3 fixed-`U` state, interpret the twelve symbols above as the
> corresponding named physical packet pieces. If none of `Z1`--`Z7` is
> complete EFX under physical single-good deletion tails, then either:
>
> - a proper recipient-feasible split gives strict collision-support progress
>   (with later-owner sacrifice allowed exactly when priority permits);
> - a root/protected-holder cut converts to a valid anchor change,
>   external-observer-safe exchange, or response-rank progress; or
> - deletion-minimal unsafe witnesses uncross into a closed pairwise-disjoint
>   desired-core family on `{d,q,r}`, `{q,r,s}`, `{d,q,s}`, `{d,r,s}`, or all
>   four owners.

The last alternative is generalized PI. Proving this lemma lifts the bounded
dichotomy to the requested cap-free four-edge theorem.

## Cap-free reduction obtained on 2026-08-14

`CAPFREE_SEVEN_ENDPOINT_OR_HIDDEN_SPLIT_REDUCTION_20260814.md` removes packet
cardinality itself from the open interface.  Combining this bounded theorem
with the physical packet-compression hidden-minimum lemma gives, for arbitrary
finite packet sizes, the exact trichotomy:

1. one of `Z1`--`Z7` expands to complete physical EFX;
2. a compressed desired-core family expands to physical generalized PI; or
3. a failing physical tail exposes a strict least good inside a nonsingleton
   compressed atom, with value below every compressed atom in that bundle.

Thus the remaining cap-free work is conversion of that decorated proper split
through the recipient-deficiency or root/base-restoration hitting cut—not a
bound on the number of goods in the packet.

## Claim boundary

Proved: the seven-endpoint-or-generalized-PI theorem in the exact declared
twelve-atom R3 cell, with two independent UNSAT encodings.

Not proved: conversion of every strict hidden-minimum split through the
root/protected bi-row or base-restoration hitting cut, or the universal
cap-free four-edge complete-EFX theorem.

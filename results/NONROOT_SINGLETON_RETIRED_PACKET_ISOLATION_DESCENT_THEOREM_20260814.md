# Nonroot singleton retired-packet isolation descent theorem

**Date:** 2026-08-14

**Status:** conditional singleton-isolation wall lemma. Singleton safety and
wall localization are exact; adoption of the isolation allocation is not yet
an admissible collision transition.

## Exact singleton state

Let `r` retain a safe root core `A_r` with

\[
v_r(A_r)>v_r(X_r),                               \tag{1}
\]

and let the named retired packet be the singleton

\[
K=\{g\}                                         \tag{2}
\]

with nonroot current holder `h`. Let `s,q` be the other two nonroot owners.
All signed retirement and supplier labels of `g` are retained.

## Isolation allocation

Give `{g}` alone to `h`. Pool every other good not in `A_r` and use the
two-agent additive EFX theorem to partition that pool completely between
`s` and `q` as `P_s,P_q`. Give `A_r` to the root.

The allocation is physical and complete. The singleton target is
automatically common-safe:

\[
\tau_i(\{g\})=v_i(\varnothing)=0
\qquad(i\in N).                                  \tag{3}
\]

The two hole owners are mutually EFX by construction. Consequently every
possible EFX wall is one of:

1. a root-to-hole or hole-to-root wall between `A_r` and `P_s` or `P_q`;
2. a holder wall from `h` to `A_r,P_s`, or `P_q`; or
3. a root wall against a hole bundle.

No owner can have an EFX wall against `{g}`.

## Response routing

- Root-star walls enter the ledger-normalized external-star ascent/root-price
  trichotomy.
- If `h` has a wall against a hole bundle, globally minimum response
  extraction gives a current-safe core inside that K-free hole. Retain it
  with `A_r` and enter the protected two-core/two-hole response-Hall
  boundary.
- If `h` has a wall against `A_r`, its globally minimum response is a proper
  safe subset of the root core and enters root reselection, controlled root
  release, or the bounded root-price branch.
- A supplied desired cycle is PI; a new source/target or outside supplier is
  ordinary finite rank/component progress.

Every extracted response at this test allocation is disjoint from `{g}`.
This proves a conditional selector-pool separation, not yet a decrease of
the active hitting coordinate. The frozen contract requires the allocation
and response to be reached by an admissible operation. An arbitrary
two-agent EFX repartition of the complement is not among the listed
`G0--G10` operations, and its supplier/floor handoff has not been proved.

If the isolation allocation is EFX, (1) gives an immediate lexicographic
contradiction. Otherwise one of the routes above applies.

## Typed branches

- **Strict and equality capture:** the argument never requires a positive
  recipient margin, so both singleton branches are covered.
- **Base-floor debt:** nonroot auxiliary floors may fall; the root remains
  strict. A holder response is retained as an actual decorated core rather
  than called paid.
- **Release:** the singleton stays with its recorded holder, so no release
  of `K` occurs. Every later core retains its own supplier labels.

## Consequence

If the isolation allocation can be implemented by a priority-valid paid
splice, then together with the proper-split theorem every nonroot packet has
either:

- `|K|>=2`, giving a proper packet/rank compression; or
- `|K|=1`, giving singleton isolation and zero hitting multiplicity.

The singleton implementation gate remains open, so this is not presently an
elimination of the nonroot terminal.

## Claim boundary

This lemma proves singleton target safety and exact wall localization at the
displayed isolation allocation. It does not prove a permitted transition to
that allocation, preserve the complement owners' typed floors or supplier
closures, or establish strict collision-hitting descent in the frozen state
graph. It therefore does not eliminate the singleton collision or close
`T_{L,times}^*`.

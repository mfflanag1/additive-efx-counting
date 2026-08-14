# Allocated-E q/s-paid sharp two-debt theorem

**Date:** 2026-08-14

**Status:** dual-verified exact bounded theorem with an independently audited
sharpness countermodel

## Theorem

In the exact twelve-atom allocated-`E` form-2 master, every profile satisfying
all generalized-PI exclusions has one of the seven explicit complete EFX
endpoints at which both represented owners `q` and `s` weakly retain their
normalized base utility:

\[
v_q(Z_q)\ge 1,\qquad v_s(Z_s)\ge 1.
\]

Consequently every payment hole of the selected endpoint belongs to the
distinguished root/sacrifice pair

\[
H(Z)\subseteq\{r,d\}.
\]

The earlier generic statement `|H(Z)|<=2` is therefore not merely a
cardinality bound: the two possible debt rows have canonical GG roles.

## Exact proof record

The producer restores 46,683 valid generalized-PI exclusions and negates all
seven endpoint conjunctions

\[
\operatorname{EFX}(Z_k)\wedge v_q((Z_k)_q)\ge1
                         \wedge v_s((Z_k)_s)\ge1.
\]

The two-hole count is redundant once `q` and `s` are required to be paid, but
is retained in the machine formula to keep the payment interface explicit.
Z3 5.0.0 returns UNSAT.  The producer is
`allocated_e_form2_seven_endpoint_two_hole_qs_paid_full_pi_decision.json`,
SHA-256
`b87c6c94716941f89d07ef0635cf9f09f98cf25426407e7a3ae022d6fcd4c933`.

Assumption-core extraction reduces the proof to 394 PI clauses and five of
the seven endpoints.  The core is
`allocated_e_form2_two_hole_qs_paid_unsat_core.json`, SHA-256
`ecd1f91d4e816479a469440665c2cb14549c9a162b3b31ebe2139b0db148b527`.

An independent replay rebuilds those PI predicates with literal nested
minima, rebuilds EFX with direct single-good-deletion inequalities, and tests
the `q,s` payment rows directly.  With a different random seed it again
returns UNSAT.  The audit record is
`allocated_e_form2_seven_endpoint_two_hole_qs_paid_compact_core_audit.json`,
SHA-256
`e813951632776fc28deba84d32292079a70b019646b373dd705d142ed30db3ef`.

## Sharpness

The conclusion cannot be strengthened to a single payment hole while still
requiring `q` and `s` to be paid.  An exact CEGAR begins with the 46,683
recorded cuts, discovers and excludes sixteen further generalized PI
families, and terminates at a positive-rational profile with:

1. no generalized PI under the complete exact oracle;
2. complete EFX endpoints;
3. no endpoint simultaneously paying `q` and `s` with at most one hole.

At the terminal profile endpoint `Z4` is EFX and has exactly the two holes
`{r,d}`.  The CEGAR record is
`allocated_e_form2_seven_endpoint_one_hole_qs_paid_pi_cegar.json`, SHA-256
`1d0e9cc89b79c63e02eff0b7324d0506eeae039b87ccfd8f09ada6169e4ed43c`.
An independent exact-Fraction audit reconstructs the master, reruns the full
generalized-PI oracle, and checks all seven endpoints.  Its record is
`allocated_e_form2_seven_endpoint_one_hole_qs_paid_pi_cegar_audit.json`,
SHA-256
`6af3370f07b2a0c9ab51c5cf645589e780ffd9ca1ef55b989754179fdc1510a9`.

Separately, requiring the root `r` to be paid is false even while permitting
two holes.  The independently audited exact PI-free profile is recorded in
`allocated_e_form2_seven_endpoint_two_hole_root_paid_full_pi_decision.json`
and its audit.  Thus a proof cannot simply import a strict-root endpoint
premise.

## Cap-free consequence

Physical packet expansion preserves owner utilities.  Therefore `q` and `s`
remain paid for arbitrary packet cardinalities.  Combining this theorem with
the physical-failure localization lemma gives the following exact fork:

1. the expanded endpoint is complete physical EFX;
2. a failed paid observer exposes an ordinary physical base response; or
3. every failed physical EFX comparison is observed by `r` or `d`.

After ordinary response augmentation is excluded by saturation, the entire
physical-tail obstruction is therefore a two-row root/sacrifice problem.  It
is the same typed pair appearing in the companion root-retention and
two-creditor Hall analysis.

## Claim boundary

Proved: the exact bounded `q,s`-paid theorem, its sharp two-debt boundary, and
the cap-free localization of all residual failed observers to `{r,d}`.

Not proved: supplier-compatible repair of those two rows, elimination of the
resulting two-creditor Hall cut, the universal saturated fixed-`U` theorem,
four-agent EFX, or general additive EFX.

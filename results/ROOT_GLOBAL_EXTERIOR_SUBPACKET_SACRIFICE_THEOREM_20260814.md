# Root global-exterior subpacket sacrifice theorem

**Date:** 2026-08-14

**Correction (2026-08-14):** the supplier-star allocation below empties
later owners and therefore is not yet admitted under the frozen requirement
that every candidate preserve its declared floors.  The scalar cut and old-
root-core contradiction remain valid conditional on a controlled floor reset
or floor-paying supplier star, but this document does not currently close
the root-held branch.  See
`ROOT_GLOBAL_SUPPLIER_STAR_FLOOR_ADMISSIBILITY_GAP_20260814.md`.

**Resolution update (2026-08-14).** The new strict first-priority
floor-reset theorem explicitly releases the old later floors and recomputes
the actual state. Its singleton specialization closes the root-holder branch
directly. The unreset all-subpacket formulation below remains conditional;
its full strength is no longer needed for `T_{L,times}^*`.

**Composition closure (2026-08-14):** the strict global underpayment face is
empty under the frozen anchored `GG` interface. The retained old desired root
core `T_q+f` lies in the base exterior and is worth more than `X_r`, whereas
the cut below would put each base-contained retired atom above that entire
exterior. See
`GG_OLD_ROOT_CORE_EXCLUDES_EXTERIOR_DOMINANT_PACKET_THEOREM_20260814.md`.

**Status:** conditional scalar/support reduction; transition admission is
open at the frozen positive-floor sacrifice gate

## Exact root state

Let an exact `T_{L,times}^*` state have first-priority root `r` with

\[
 Z_r=K\mathbin{\dot\cup}H,
 \qquad v_r(Z_r)=x+\delta,
 \qquad\delta>0,                                \tag{1}
\]

where `K` is the named nonempty retired packet.  Let `u != r` be its named
historical recipient, used here only as a fixed nonroot sacrifice target.
Put

\[
 E=G\setminus Z_r.                              \tag{2}
\]

No compatibility assumption is imposed on `E`: every current holder of an
exterior or retired good is named in the complete signed record.

## Global supplier-star sacrifice

For any nonempty `T subseteq K`, form the complete allocation

\[
 Z'_r=G\setminus T=(K-T)+H+E,
 \qquad Z'_u=T,                                 \tag{3}
\]

and give every other nonroot owner and charity the empty bundle.  Equivalently,
every current holder supplies her entire target into the root supplier star,
the root supplies `T` to `u`, and all later owners may be sacrificed.  Every
other retirement collision and physical anchor change is appended to the
exact signed record. No PI edge or historical reversibility is inferred.

The root margin is

\[
 v_r(Z'_r)-x=\delta+v_r(E)-v_r(T).              \tag{4}
\]

Thus the candidate is root-strict whenever

\[
 v_r(E)>v_r(T)-\delta.                           \tag{5}
\]

## Every failed test reduces the named packet

If (3) is EFX under (5), it contradicts global lexicographic maximality.
Otherwise every unsafe target is one of `G-T` or `T`; empty targets are safe.

The root target meets `K` in `K-T`, a proper subset.  If `T subsetneq K`,
the nonroot target meets `K` in the other proper subset `T`.  If `T=K`, a
singleton target cannot be strongly envied, while every EFX wall against a
multigood `K` supplies a desired deletion `K-g`; hence its globally minimum
response is proper.  Consequently every globally minimum response at (3)
has proper or empty `K`-intersection.

Adopting the tested allocation/response is strict reduction of `K` or its
hitting coordinate. Moving a second retired label into the root does not
undo that reduction and is not recorded as history-only progress.

## Equality is impossible at recurrence

Suppose instead that (4) is zero. Bundle nondegeneracy gives

\[
 G\setminus T=X_r,
 \qquad T=G\setminus X_r.                       \tag{6}
\]

Under the frozen three-nonsingleton GG import, `G-X_r` contains the three
nonempty nonroot base bundles and the charity singleton, so `|T|>=4`. Choose
`g in T` and use `T'=T-g`, which is nonempty and still a proper subpacket of
`K`. The corresponding root target is

\[
 G\setminus T'=X_r+g,                           \tag{7}
\]

strictly above base. The strict branch therefore reduces the named packet.
Thus no equality mode survives.

## Exact global-exterior cut

A recurrent root-held packet must satisfy, for every nonempty `T subseteq K`,

\[
 v_r(E)<v_r(T)-\delta.                           \tag{8}
\]

In particular every atom satisfies

\[
 v_r(k)>\delta+v_r(E)\qquad(k\in K),            \tag{9}
\]

and summation gives

\[
 (|K|-1)\delta+|K|v_r(E)<x.                    \tag{10}
\]

This **complete current-exterior dominance** strictly subsumes every
compatible-mode packet-price cut. There is no remaining equality,
supplier-compatibility, or multi-label charge branch on the root side.

## Typed branches

- **Strict capture:** every globally paying subpacket is released and gives
  proper packet response.
- **Equality-critical payment:** root equality is converted by (6)--(7) to a
  strict packet-spread operation.
- **Base-floor debt:** all nonroot owners are explicitly later sacrificed;
  no auxiliary nonroot floor is used.
- **Release compatibility:** every current holder is an explicit supplier;
  no PI claim is made, and every other retired collision/anchor change is
  recorded in the adopted state.

## Verification

The primary audit checks the linear identities with QF_LRA and enumerates
58,975 support configurations. A separate implementation imports no primary
audit code and exhausts a six-good injective integer model, including 55,362
strict cases, 135 equality cases, and 185 fully underpaid recurrent states;
it finds no packet-hit, equality-spread, or base-containment failure. The
finite replay is regression evidence for the analytic proof, not its cap-free
justification.

## Claim boundary

This theorem admits the global supplier-star operation and proves (8)--(10).
The cited composition theorem contradicts complete current-exterior dominance
inside the full anchored `GG` state. This local theorem alone does not eliminate the
one-good on/off root-response normal form, route its source/debt owner through
the retirement supplier, close normalization bypass, `T_{L,times}^*`, GG,
four-agent EFX, or general additive EFX.

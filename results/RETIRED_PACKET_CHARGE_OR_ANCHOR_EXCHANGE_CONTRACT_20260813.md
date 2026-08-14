# Retired-packet charge-or-anchor-exchange: frozen contract

**Date:** 2026-08-13

**Status:** active cap-free proof/refutation contract for
`T_{L,times}^*`

## Exact input

Fix an exact positive-additive four-owner state in the collision subtype
`T_{L,times}^*` of the global retired-support theorem. Retain the complete
state

\[
\mathsf S=(Y,P,r,\alpha,F,\Sigma,M,h,\mathcal R,L,\mathcal C)
\]

and the following named data:

- a nonempty retired packet `K subseteq L_alpha`, with retirement-time floor
  snapshot, original supplier `u`, and current holder `h`;
- an active recipient `s` and original physical candidate
  `A=B dot-union K_s`, where `empty != K_s subseteq K`;
- the canonical cancellation candidate `Z^-`, which leaves every retired
  good with its current holder;
- the exact repeated hitting or normalization-bypass response; and
- the typed reason the canonical realization fails: recipient floor, EFX
  comparison, base-floor debt, or supplier/release closure.

No transfer is admissible merely because it improves a scalar balance.
Every candidate must conserve physical goods, keep its declared floors,
recompute all EFX comparisons, and close its supplier set.

## Exact packet accounting

Write

\[
\mu_s=v_s(A)-F_s\ge0,
\qquad
d_s=F_s-v_s(B)>0.                                \tag{1}
\]

Additivity gives the identity

\[
v_s(K_s)=\mu_s+d_s.                              \tag{2}
\]

For the current holder write

\[
Y_h=H\mathbin{\dot\cup}K_s,
\qquad
\sigma_h=v_h(Y_h)-F_h\ge0,
\]

and define the holder's exact release price

\[
p_h(K_s)=\max\{0,v_h(K_s)-\sigma_h\}.            \tag{3}
\]

Any operation moving `K_s` away from `h` must give `h` a physically released
packet `J` satisfying

\[
v_h(J)\ge p_h(K_s).                              \tag{4}
\]

Equation (2) is a recipient-row capture. It does not imply (4), because
additive valuation rows are independent. The central theorem must therefore
derive (4) from the complete GG state, avoid moving `K_s` by changing the
root/anchor, or use failure of (4) to force another allowed outcome.

## Deterministic branch partition

Process a colliding candidate in this order.

| Branch | Exact condition | Required resolution |
|---|---|---|
| strict capture | `mu_s>0` and `v_s(B)<=F_s` | compensate `h`, reduce the collision packet/hitting multiplicity, exchange the anchor, or contradict maximality |
| equality critical | `mu_s=0` and `v_s(B)<F_s` | use a separately valid earlier-priority handoff/anchor exchange, or prove equality cannot recur |
| base-floor debt | all recipient floors survive but a protected-core assignment or observer comparison is only base-paid | upgrade the underfunded owner, pivot the response rank, or expose an exact payment obstruction |
| release failure | floor and EFX tests pass but the selected transfer is not supplier-closed | close a PI component, recruit a supplier strictly, or prove the exact release separator forces anchor change |

These branches are disjoint by priority. “Base-floor debt” does not include a
recipient whose own floor already failed; “release failure” is tested only
after every floor and EFX comparison passes.

## Permitted conclusions

For every exact `T_{L,times}^*` state, derive at least one of:

1. an EFX allocation lexicographically above the globally maximal base;
2. a release-compatible PI cycle;
3. a valid root-preserving anchor exchange or controlled anchor release;
4. strict reduction of `K`, its collision hitting multiplicity, or the
   response-rank deficiency; or
5. contradiction of global maximality or a typed floor inequality.

Progress must change a physical packet, response rank, or root/anchor state.
Adding another history label is not an outcome.

## Exact refutation standard

A refutation must give positive rational additive valuations and a complete
state satisfying:

1. the globally lexicographically maximal GG base import;
2. the complete signed allocation, charity, response, matching, hole,
   supplier, anchor, floor, retirement, and collision records;
3. an exact `T_{L,times}^*` recurrence;
4. physical failure of every admissible compensation, PI, anchor, reduction,
   and rank-pivot operation; and
5. all four typed branches above that occur in the witness.

A scalar witness to independence of (2) and (4), or a local mixed-cycle
payment countermodel lacking global maximality, is only a no-go certificate
for a proof route—not a refutation of this theorem.

## No-go ledger inherited from earlier work

- Supplier saturation alone does not imply observer payment.
- Complete residual-pool payment can fail and is only an optional shortcut.
- `R_q` alone is not the complete anchor-preserving compensation reservoir.
- Retire-on-backup anchor exchange requires post-handoff safety and payment
  of the backup; those are not generic `T_{L,times}^*` premises.
- A base-floor protected core is not automatically a current-safe response.
- Release compatibility is not implied by a desired-edge cycle without
  supplier closure.

## First load-bearing gate

Let `mathcal J_h` be the complete family of physically releasable packets
that can be transferred to `h` while the colliding recipient receives `A`.
The first direct-payment obligation is the
**holder-compensation-or-anchor gate**:

\[
\max_{J\in\mathcal J_h}v_h(J)\ge p_h(K_s),       \tag{5}
\]

or a valid root/anchor operation that leaves `K_s` with `h`, or an allowed
closing outcome. Failure of (5) is the exact holder-price separator. It is
not automatically terminal: when the earlier root remains strict, the
protected compression lemmas may deliberately sacrifice `h` and route every
resulting wall. The campaign may neither replace (5) with recipient capture
(2) nor demand (5) before testing that priority-valid sacrifice route.


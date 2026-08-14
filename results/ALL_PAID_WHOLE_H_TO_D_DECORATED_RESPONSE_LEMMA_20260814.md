# All-paid whole-`H`-to-`d` decorated-response lemma

**Date:** 2026-08-14

**Status:** cap-free all-paid candidate and single-target response reduction;
exact repeated-response closure remains open

## Setting

Use the physical allocated-`E` form-2 chart and the endpoint-6 hard premises:

1. endpoint `Z6` is EFX;
2. `q` and `s` weakly retain base utility at `Z6`; and
3. the root-retained `q` target `(Q-J)+M+P` is strictly below `q`'s base.

No generalized-PI exclusion is needed for the payment statement below.

Consider the complete allocation

\[
C_d=(A,Q,H+L+W,(E-L)+P).                         \tag{1}
\]

Relative to current support

\[
Y=(A+H,Q,W,E;P),
\]

allocation (1) uses exactly the three support edges

\[
r\to d,\qquad s\to d,\qquad c\to s.             \tag{2}
\]

Packet sizes are unrestricted.

## Theorem

Every owner is weakly base-paid at `C_d`.  Moreover, the targets of `r`, `q`,
and `s` are physically common-safe.  Consequently exactly one of the
following holds:

1. `C_d` is a complete physical EFX allocation through three packet-transfer
   edges; or
2. there is an observer `i` and a physical current-safe, current-desired core

   \[
   D\subseteq H+L+W                              \tag{3}
   \]

   satisfying

   \[
   v_i(D)>v_i((C_d)_i),
   \qquad
   \tau_a(D)\le v_a((C_d)_a)\quad(a\in N).       \tag{3a}
   \]

   In particular `v_i(D)>v_i(X_i)=1` because every owner is base-paid.

The core in (3)--(3a) is an exact current decorated response into the changed
`d` target.
Its physical suppliers belong to `{r,s,d}`.  At a saturated record it must
therefore be an already recorded internal response, or else it gives strict
response, supplier, support-component, or owner-union progress.

## Proof

### Payment

The exact payment decision independently negates each of the twelve
owner/allocation payment inequalities for the three whole-`H` release
candidates.  For `C_d`, all four negations are UNSAT under only the endpoint-6
hard premises.  Payment depends exclusively on packet totals, so the result
is unchanged when any named piece is expanded into arbitrarily many physical
goods.

The identities behind three rows are immediate: the root receives the
strictly base-paying packet `A`, `q` receives the strictly base-paying packet
`Q`, and `s` receives

\[
(E-L)+P=X_s.                                     \tag{4}
\]

The remaining `d` inequality is the exact endpoint-6/master consequence
certified by the payment decision:

\[
v_d(H+L+W)\ge v_d(X_d)=1.                        \tag{5}
\]

### Single-target localization

The physical chart assumes `A` and `Q` are common-safe named responses.  The
bundle in (4) is a base bundle and is physically EFX-safe by the base
allocation premises.  Hence no observer with own utility at least one can
violate EFX against any of those three targets.

If `C_d` is not physical EFX, some observer `i`, target `d`, and good
`g in H+L+W` therefore satisfy

\[
v_i((C_d)_i)<v_i((H+L+W)-g).                    \tag{6}

Among all pairs `(h,B)` with

\[
B\subseteq (H+L+W)-g,\qquad
v_h(B)>v_h((C_d)_h),                              \tag{7}
\]

choose one with inclusion-minimal support.  If some observer `k` preferred
`B-x` to her actual bundle `(C_d)_k` for a good `x in B`, that smaller pair
would contradict minimality.  Thus every one-good deletion of `B` is worth
at most `v_k((C_d)_k)` to every observer `k`.  The selected source prefers
`B` to its actual bundle, so `B` is the physical current-safe,
current-desired core `D` in (3)--(3a).  Base payment gives the earlier
base-threshold form as an immediate corollary.

## Verification

`allocated_e_form2_endpoint6_three_way_h_release_payment_analysis.json`
records all twelve exact payment queries.  `C_d` has four UNSAT underpayment
queries.  The packet identities and three support edges are independently
checked in
`allocated_e_form2_endpoint6_three_way_h_release_lift_audit.json`.

## Claim boundary

Proved: cap-free completeness, the exact three support edges, all-owner
payment, localization of every physical EFX failure to `H+L+W`, and extraction
of one physical current-safe, current-desired decorated response from that
failure.

Not proved: closure of an exact repeated internal response into `H+L+W`,
conversion of its captured-margin branch to PI or fixed-`U` progress, the
universal saturated rank-three four-edge theorem, or general additive EFX.

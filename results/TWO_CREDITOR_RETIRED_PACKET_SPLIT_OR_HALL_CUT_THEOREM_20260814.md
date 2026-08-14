# Two-creditor retired-packet split or Hall-cut theorem

**Date:** 2026-08-14

**Status:** cap-free unification of recipient top-up and protected-holder
payment into one exact two-creditor Hall obstruction

## Exact split accounting

Use

\[
A=B\mathbin{\dot\cup}K,
\qquad
v_s(K)=\mu+d,
\qquad
Y_h=H\mathbin{\dot\cup}K,
\qquad
\sigma=v_h(Y_h)-F_h.                             \tag{1}
\]

Choose a physical split

\[
K=T\mathbin{\dot\cup}U,                         \tag{2}
\]

where `T` moves to recipient `s` and `U` remains with protected holder `h`.
Let `R_s,R_h` be disjoint packets from one jointly compatible supplier-
closed mode, both disjoint from `K` and every retained protected core. Give
`R_s` to `s` and `R_h` to `h`.

The exact post-operation margins are

\[
v_s(B+T+R_s)-F_s
 =\mu-v_s(U)+v_s(R_s),                           \tag{3}
\]

and

\[
v_h(Y_h-T+R_h)-F_h
 =\sigma-v_h(T)+v_h(R_h).                       \tag{4}
\]

Define the two nonnegative prices

\[
a(U)=\max\{0,v_s(U)-\mu\},
\qquad
b(T)=\max\{0,v_h(T)-\sigma\}.                  \tag{5}
\]

Equations (3)--(4) show that both protected floors hold exactly when

\[
v_s(R_s)\ge a(U),
\qquad
v_h(R_h)\ge b(T).                               \tag{6}
\]

## Joint-payment branch

Let `mathcal P_s(U)` be the inclusion-minimal current-safe packets reaching
price `a(U)` in the recipient row, with exact supplier labels. Define
`mathcal P_h(T)` analogously at price `b(T)`. An unsafe inclusion-minimal
threshold crossing is processed first by globally minimum response
extraction; it gives response/rank/supplier progress or a retired collision,
not a member of the terminal families.

If some pair

\[
(R_s,R_h)\in\mathcal P_s(U)\times\mathcal P_h(T) \tag{7}
\]

is disjoint and belongs to one compatible release mode, perform the complete
EFX and release audit. When `T` and `U` are both nonempty, the retired packet
lies in two different targets, so every single-target retired response meets
a proper subset. The audit therefore yields EFX, PI, proper collision-
support reduction, or existing rank/supplier progress.

The boundary splits `T=K,U=empty` and `T=empty,U=K` are respectively the
ordinary holder-compensation test and the whole-packet ledger-free
replacement test.

## Exact Hall obstruction

For every nontrivial split, exactly one of the following ordered branches
holds after unsafe crossings are routed:

1. **recipient deficiency:** `mathcal P_s(U)=empty`;
2. **holder deficiency:** `mathcal P_s(U)!=empty` but
   `mathcal P_h(T)=empty`;
3. **joint incompatibility:** both families are nonempty, but every
   `R_s in mathcal P_s(U)` and `R_h in mathcal P_h(T)` overlap or belong to
   incompatible supplier/protected modes; or
4. **joint payment:** a pair (7) exists and the preceding branch applies.

After branch 4 is exhausted, branches 1--3 are the exact **two-creditor Hall
cut**. It is stronger than two independent scalar underpayment statements:
branch 3 records that both prices can be paid separately, but not by one
physical disjoint supplier-compatible operation.

Equivalently, form a bipartite compatibility graph whose left vertices are
the safe minimal recipient packets and whose right vertices are the safe
minimal holder packets, with an edge for a disjoint compatible pair. The
terminal has an empty side or no edge. No incompatible pools are unioned.

## Composition with the two atomic terminals

- In the sacrifice-eligible nonroot branch, set `b(T)=0`; the theorem reduces
  to the recipient top-up cut.
- In the protected/root branch, `a(U)=0` recovers the holder bi-row cut when
  `T` alone pays the recipient. Allowing both prices positive strictly
  enlarges the operation family beyond that earlier one-sided test.
- In equality capture, `a(U)=v_s(U)` exactly; no false strict margin is used.
- For a root holder, every surviving `T` also lies in the atomwise root loss
  band, so branch 3 is the only obstruction after both one-sided threshold
  families are nonempty.

Thus the charge-or-anchor objective is reduced further to eliminating the
two-creditor Hall cut using the retirement supplier, owner topology, or a
controlled anchor operation.

## Exact scalar obstruction to forcing an edge

Nonemptiness of both threshold families does not imply joint compatibility.
Let `K={k_1,k_2}`. In the recipient row take

\[
v_s(k_1)=v_s(k_2)=2,
\qquad
(\mu,d)\in\{(1,3),(0,4)\}.                       \tag{8}
\]

Let one releasable outside good `z` have

\[
v_s(z)=2-\mu.                                    \tag{9}
\]

For either nontrivial split, the recipient price is `2-mu`, so `z` pays it.
In the protected root row take

\[
v_r(k_1)=v_r(k_2)=2,
\qquad x=5,
\qquad \delta=\sigma=1,
\qquad v_r(H)=2,
\qquad v_r(z)=1.                                 \tag{10}
\]

The root core `H+K` has value six and every one-good deletion has value four,
so it is inclusion-minimal above `x`. For either nontrivial split, `z` also
pays the root price `2-1=1`. But the only recipient packet and holder packet
are the same physical good, so branch 3 holds. The boundary operations fail:

\[
v_r(z)=1<4-1=3,
\qquad
v_s(z)=2-\mu<d.                                  \tag{11}
\]

This exact positive-additive family realizes joint incompatibility in both
strict and equality capture while satisfying the scalar double-atomic root
conditions. It is not a complete GG state, but it refutes any attempt to
derive a Hall edge from the two threshold totals or root atomicity alone.

## Claim boundary

This theorem proves the two floor identities, the joint-payment split,
target locality, and the exhaustive Hall obstruction. It does not prove that
either threshold family is nonempty, force an edge between two nonempty
families (the scalar family (8)--(11) refutes that strengthening), convert
every incompatibility into PI, eliminate the equality or
base-debt Hall cells, close `T_{L,times}^*`, or prove four-agent/general EFX.

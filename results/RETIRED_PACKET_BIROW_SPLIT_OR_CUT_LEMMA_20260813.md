# Retired-packet bi-row split-or-cut lemma

**Date:** 2026-08-13

**Status:** cap-free proper-packet reduction unless an exact recipient/holder
two-row cut blocks every partial transfer

## Exact packet rows

Use the collision contract with

\[
A=B\mathbin{\dot\cup}K,
\qquad
\mu=v_s(A)-F_s\ge0,
\qquad
d=F_s-v_s(B)>0,                                  \tag{1}
\]

so `v_s(K)=mu+d`.  Let the current holder have bundle

\[
Y_h=H\mathbin{\dot\cup}K,
\qquad
\sigma=v_h(Y_h)-F_h\ge0.                         \tag{2}
\]

For every candidate transferred subpacket `T subseteq K`, let
`mathfrak R_h(T)` be its complete family of mutually compatible compensation
modes and put

\[
M_h(T)=\max_{R\in\mathfrak R_h(T)}v_h(R),         \tag{3}
\]

with `M_h(T)=-infinity` if no physical mode exists.  Every mode carries its
full supplier/protected-core labels.

## Exact feasibility identities

Give `B+T` to recipient `s`, leave `K-T` with holder `h`, and give `h` one
compatible return `R`.  The recipient floor holds exactly when

\[
v_s(T)\ge d,                                      \tag{4}
\]

and the holder floor holds exactly when

\[
v_h(T)\le\sigma+v_h(R).                           \tag{5}
\]

The recipient's post-transfer margin is `v_s(T)-d`; equality in (4) is
therefore kept as an equality-critical transition, not called strict.

## Proper floor-feasible split branch

Suppose some nonempty `T subseteq K` satisfies

\[
v_s(T)\ge d,
\qquad
v_h(T)\le\sigma+M_h(T).                           \tag{6}
\]

Choose a compatible return attaining (3).  Equations (4)--(5) pay both
typed owner floors.  Perform the complete observer and supplier audit.
If that audit succeeds, only `T` moves and, when `T subsetneq K`, the
executed collision packet strictly shrinks.

There is also a physical reason that a failed audit cannot silently rebuild
the old packet. At the tested allocation the two nonempty parts lie in
different targets:

\[
K\cap(B+T)=T,
\qquad
K\cap(Y_h-T+R)=K-T.                              \tag{7}
\]

Every other target is disjoint from `K`, because compatible compensation
modes exclude `K`. A globally minimum response is extracted inside one
physical target. Its collision support is therefore contained in `T`, in
`K-T`, or is empty. When `empty != T subsetneq K`, every nonempty possibility
is a proper subset of `K`. A supplier-closed desired cycle is already PI;
an outside supplier strictly enlarges the owner component. Thus an observer,
base-debt, or release failure after the split gives an allowed response/rank
outcome with proper collision support rather than a whole-`K` recurrence.

Now assume the full-packet aggregate-underpayment separator:

\[
M_h(K)<v_h(K)-\sigma.                             \tag{8}
\]

Then `T=K` cannot satisfy (6).  Consequently every floor-feasible `T` in
(6) is automatically proper and, by (7), gives strict packet/collision-
support reduction or an already
closing PI/rank/supplier outcome.

## Exact bi-row cut

If (8) holds and no partial transfer is even floor-feasible, the state
carries the exact separator

\[
v_s(T)\ge d
\quad\Longrightarrow\quad
v_h(T)>\sigma+M_h(T)
\qquad(T\subseteq K).                             \tag{9}
\]

Thus every subpacket large enough in the recipient row is too expensive in
the holder row even after its complete compatible compensation mode.  This
is the irreducible **bi-row packet cut**. Target locality is why a
floor-feasible proper packet cannot return the whole packet through a single
response.

## Strict and equality consequences

### Strict capture

If `mu>0` and no proper subpacket even preserves the recipient floor, then
for every `g in K`,

\[
v_s(K-g)<d
\quad\Longrightarrow\quad
v_s(g)>\mu.                                      \tag{10}
\]

Hence

\[
(|K|-1)\mu<d.                                    \tag{11}
\]

In particular, `mu>=d` forces `K` to be a singleton.  When a recipient-
feasible proper packet exists but (6) fails, (9) identifies holder cost—not
recipient indivisibility—as the obstruction.

### Equality-critical capture

If `mu=0`, then `v_s(K)=d`.  Positivity gives

\[
v_s(T)<d\qquad(T\subsetneq K).                  \tag{12}
\]

Thus no proper packet can preserve the recipient floor.  Equality-critical
capture necessarily uses the whole packet and must close through a
priority-valid sacrifice, root/anchor operation, or contradiction; packet
splitting alone cannot resolve it.

### Base-floor debt and release

Equations (4)--(9) address the recipient and holder floors only.  A
base-paid observer or incompatible supplier mode is retained as its typed
debt/release branch and routed through protected matching, response
extraction, or supplier-component growth. It is not hidden inside (9).

## Claim boundary

This lemma proves the exact partial-transfer identities, proper-packet or
proper-collision-support reduction under (6)--(8), the alternative bi-row
cut (9), and the strict/equality packet consequences. It does not contradict
(9) from global GG maximality, force a compatible compensation mode,
eliminate equality via anchor release, close `T_{L,times}^*`, or prove
four-agent/general EFX.

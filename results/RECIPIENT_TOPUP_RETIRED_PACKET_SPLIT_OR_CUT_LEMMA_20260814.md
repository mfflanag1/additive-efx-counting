# Recipient-top-up retired-packet split-or-cut lemma

**Date:** 2026-08-14

**Status:** cap-free reduction of recipient indivisibility to a compatible
top-up crossing or an exact complete-pool underpayment cut

## Exact input

Use the collision accounting

\[
A=B\mathbin{\dot\cup}K,
\qquad
v_s(K)=\mu+d,
\qquad
d=F_s-v_s(B)>0.                                  \tag{1}
\]

Assume the current holder `h` is a later sacrifice-eligible owner and the
earlier strict root is unchanged. This is the branch in which payment of
`h` is not an endpoint premise.

Choose a nonempty retained subpacket `U subseteq K`. Transfer `K-U` to `s`
and leave `U` with `h`. Let `mathfrak U_s(U)` be the complete finite family
of mutually compatible top-up modes, excluding `K` and every retained
protected root/core good. A mode includes all supplier releases and every
floor that is not explicitly waived for the designated sacrificed holder.
Put

\[
N_s(U)=\max_{R\in\mathfrak U_s(U)}v_s(R),         \tag{2}
\]

with value `-infinity` when no physical mode exists.

## Exact top-up identity

Give `B+(K-U)+R` to `s`. Its margin over the protected recipient floor is

\[
\begin{aligned}
v_s(B+K-U+R)-F_s
 &=\mu-v_s(U)+v_s(R).
\end{aligned}                                    \tag{3}
\]

Define the recipient top-up price

\[
q_s(U)=v_s(U)-\mu.                               \tag{4}
\]

Then the recipient floor holds exactly when

\[
v_s(R)\ge q_s(U).                                \tag{5}
\]

In a recipient-indivisible survivor every nonempty proper `U` has
`q_s(U)>0`: otherwise `K-U` alone would already preserve the floor.

## Top-up crossing

Suppose `empty != U subsetneq K` and

\[
N_s(U)\ge q_s(U).                                \tag{6}
\]

Choose a compatible mode attaining (2), then an inclusion-minimal
`R` in that mode satisfying (5). Execute the complete comparison and release
audit. The earlier root remains strict, the recipient floor is paid by (3),
and the holder is the designated later sacrifice.

At the tested allocation the two nonempty parts of the retired packet lie
in different targets:

\[
K\cap(B+K-U+R)=K-U,
\qquad
K\cap(Y_h-(K-U)-R_h)=U,                          \tag{7}
\]

where `R_h` denotes any holder-owned part of the top-up. Every top-up mode
excludes `K`. Hence a globally minimum response inside one target meets at
most `U` or `K-U`, both proper. A supplied cycle is PI; an outside supplier
or new response coordinate is finite component/rank progress. Thus (6)
gives EFX, PI, a proper collision-support reduction, or existing rank/
supplier progress.

The top-up packet need not be safe in advance. If its enlarged recipient
target is unsafe, globally minimum response extraction is performed at the
actual tested allocation, and (7) still makes every retired hit proper.

## Whole-packet replacement

For `U=K`, equation (3) becomes the canonical ledger-free replacement test

\[
v_s(B+R)\ge F_s
\iff
v_s(R)\ge d.                                     \tag{8}
\]

This does not split `K`; it enters the existing normalization-bypass audit.
An EFX realization closes, a new response/rank coordinate progresses, and
an exact bypass recurrence returns to the already isolated target-envelope/
external-star or root-price branch. Equation (8) is particularly relevant
when `K` is a singleton.

## Exact top-up cut

After every crossing branch is exhausted, a recipient-indivisible
nonroot recurrence must satisfy

\[
N_s(U)<q_s(U)=v_s(U)-\mu
\qquad
(\varnothing\ne U\subsetneq K),                 \tag{9}
\]

and, if whole-packet replacement also fails,

\[
N_s(K)<d.                                        \tag{10}
\]

For singleton retention this reads

\[
N_s(\{g\})<v_s(g)-\mu
\qquad(g\in K).                                 \tag{11}
\]

Let

\[
n_s=\min_{g\in K}N_s(\{g\}).                    \tag{12}
\]

Then (11) implies `v_s(g)>mu+n_s` for every good. Summing and using
`v_s(K)=mu+d` gives the cap-free top-up multiplicity charge

\[
(|K|-1)\mu+|K|n_s<d.                            \tag{13}
\]

Equivalently, if

\[
n_s\ge {d-(|K|-1)\mu\over |K|},                 \tag{14}
\]

some singleton-retention top-up crossing exists. In equality capture this
threshold is exactly `d/|K|`. The inequality uses the weakest complete
singleton top-up capacity, so it does not union incompatible modes.

Thus recipient indivisibility is no longer the final description: the
survivor is a **recipient top-up cut** over the complete compatible outside
reservoir.

## Typed branches

- **Strict capture:** `mu>0` discounts every retained packet by the exact
  captured margin in (4). If a proper packet was already recipient-feasible,
  the earlier sacrifice-split theorem applies with zero top-up.
- **Equality:** `mu=0`, so the exact price of retaining `U` is `v_s(U)`.
  Equality is handled without pretending that a proper part of `K` alone
  pays the floor.
- **Base-floor debt:** only the designated later holder floor is waived.
  Every other protected floor is part of the compatible-mode definition.
- **Release:** modes are separate supplier-closed operations; incompatible
  modes are never unioned. PI is declared only after supplier closure.

## Claim boundary

This lemma proves the top-up identity, proper-split locality, whole-packet
replacement threshold, the exact complete-pool cut (9)--(10), and the
multiplicity charge (13). It does
not force the top-up reservoir to cross, terminate every normalization-
bypass return, eliminate the protected/root double-atomic cut, contradict
the top-up cut from global GG maximality, close `T_{L,times}^*`, or prove
four-agent/general EFX.

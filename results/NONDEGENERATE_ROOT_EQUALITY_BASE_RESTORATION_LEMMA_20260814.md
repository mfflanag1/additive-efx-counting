# Nondegenerate root equality is exact base restoration

**Date:** 2026-08-14

**Status:** cap-free conversion of the root equality-Hall face to a unique
signed base-restoration support pair

## Input

Let `X_r` be the globally maximal base root bundle and `Y_r` the current
strict root bundle. Assume the root valuation is bundle-nondegenerate:

\[
P\ne Q\quad\Longrightarrow\quad v_r(P)\ne v_r(Q). \tag{1}
\]

Transfer `T subseteq Y_r` away from the root and give the root a physically
disjoint outside packet `R`, with

\[
T\cap R=\varnothing,
\qquad
R\cap Y_r=\varnothing.                           \tag{2}
\]

The post-transfer root bundle is

\[
Q_r=(Y_r\setminus T)\mathbin{\dot\cup}R.         \tag{3}
\]

## Equality implies physical identity

Suppose the compensation is exactly equality-critical:

\[
v_r(Q_r)=v_r(X_r).                               \tag{4}
\]

Bundle nondegeneracy (1) gives

\[
Q_r=X_r.                                         \tag{5}
\]

Equations (2)--(3) and the physical set equality (5) then force

\[
T=Y_r\setminus X_r,
\qquad
R=X_r\setminus Y_r.                              \tag{6}
\]

Indeed every current root good outside `X_r` must be removed, no good of
`Y_r intersect X_r` can be removed because `R` is disjoint from `Y_r`, and
every missing base good must be supplied by `R`. Thus the equality packet
and compensation are unique.

Writing

\[
S^+=Y_r\setminus X_r,
\qquad
S^-=X_r\setminus Y_r,                            \tag{7}
\]

additivity also gives the signed surplus identity

\[
v_r(S^+)-v_r(S^-)
 =v_r(Y_r)-v_r(X_r)=\delta.                      \tag{8}
\]

Hence the exact release price of `S^+` is `v_r(S^-)`, and equality payment
restores the physical base root bundle.

## Consequence for the retired-packet Hall cut

In the root equality-Hall branch the transferred set satisfies `T subseteq
K`. Equation (6) therefore forces

\[
S^+\subseteq K.                                  \tag{9}
\]

There is no family of arbitrary equality-paying root packets. There is only
the signed base-restoration operation

\[
S^+\longrightarrow s,
\qquad
S^-\longrightarrow r.                           \tag{10}
\]

If a recipient top-up packet is disjoint and supplier-compatible with
`S^-`, the two-creditor split theorem applies. If none is, the surviving
joint obstruction is the exact **base-restoration hitting cut**:

> every safe recipient top-up crossing for retaining `K-S^+` intersects
> `S^-` or is supplier/protected-mode incompatible with the signed exchange
> (10).

The full signed decoration records where every good of `S^-` moved from the
base root and where every good of `S^+` entered the current root. Thus (10)
is the precise support on which retirement provenance must now act.

## Full-packet underpayment forces a base-crossing packet

Retain the strict full-packet separator from the complete-mode theorem:

\[
M_r(K)<v_r(K)-\delta.                            \tag{11}
\]

For the equality operation, (6), (8), and `T=S^+ subseteq K` give

\[
v_r(S^-)=v_r(T)-\delta.                          \tag{12}
\]

If `T=K`, packet `S^-` pays the full release price exactly, contradicting
(11). Hence the retained part `U=K-T` is nonempty. Since `K subseteq Y_r`
and `T=Y_r-X_r`, the physical support is

\[
\varnothing\ne U=K\cap X_r,
\qquad
T=K\setminus X_r=Y_r\setminus X_r.              \tag{13}
\]

Thus the equality-Hall terminal is not an arbitrary split. The retired
packet crosses the base-root boundary:

- every current root surplus good lies in `K` and must leave;
- a nonempty retired base-root subpacket `K intersect X_r` must remain; and
- the unique missing-base packet `S^-` must return to the root.

The recipient top-up price is consequently fixed at

\[
a(K\cap X_r)=v_s(K\cap X_r)-\mu>0               \tag{14}
\]

in the recipient-indivisible branch. The remaining Hall obstruction says
that every packet reaching (14) conflicts with the fixed signed return
`S^-` or its supplier mode.

## Typed branches

- **Strict capture:** strict recipient margin does not remove root equality;
  (6) still identifies the only equality packet.
- **Equality capture:** both rows may be weak, but the root side is a literal
  base restoration rather than a numerical tie between distinct bundles.
- **Base-floor debt:** a compatible operation must still pay every protected
  nonroot row; (6) does not waive them.
- **Release:** `S^-` retains its exact current suppliers. Returning it to the
  root is executed only through the signed supplier component.

## Claim boundary

This lemma proves (5)--(10) from bundle nondegeneracy and physical
disjointness, and proves the base-crossing form (13) under full-packet
underpayment. It does not guarantee a compatible recipient top-up, turn the
base-restoration hitting cut into PI, prove that restoring `X_r` alone is a
valid lexicographic endpoint, eliminate root-payment deficiency, close
`T_{L,times}^*`, or prove four-agent/general EFX.

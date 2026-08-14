# Restoration-overlap swap or bi-row cut lemma

**Date:** 2026-08-14

**Status:** cap-free conversion of every purely physical root/recipient
restoration overlap into strict root progress or an exact cross-row cut

## Exact base-restoration face

Use the protected-root equality face from the base-restoration lemma.  Write

\[
 S^+=Y_r\setminus X_r,
 \qquad S^-=X_r\setminus Y_r,
 \qquad v_r(S^+)-v_r(S^-)=\delta>0.              \tag{1}
\]

The retired packet is base-crossing:

\[
 K=S^+\mathbin{\dot\cup}U,
 \qquad \varnothing\ne U=K\cap X_r.             \tag{2}
\]

Transferring all of `S^+` while returning all of `S^-` restores the root
exactly to `X_r`.  Let `R_s` be an inclusion-minimal safe recipient top-up
for the retained packet `U`, and put

\[
 a=v_s(U)-\mu>0,
 \qquad
 \varepsilon_s(R_s)=v_s(R_s)-a\ge0.             \tag{3}
\]

Thus transferring `S^+` and assigning `R_s` to `s` leaves recipient margin
`epsilon_s(R_s)` above the typed floor.

Assume the only incompatibility between this top-up mode and the signed
root-restoration mode is physical overlap.  In particular, after deleting
transfers from either mode, their supplier and protected-mode requirements
remain compatible.  Put

\[
 J=R_s\cap S^-\ne\varnothing.                   \tag{4}
\]

## Overlap swap

Choose any proper `V subsetneq S^+`.  Modify the attempted restoration as
follows:

- keep `V` at the root and transfer only `S^+-V` to `s`;
- give `S^--J` to the root;
- give the original top-up `R_s`, including `J`, to `s`; and
- leave `U` at the root.

This operation is physical: `J` is assigned only to `s`, and `V` is never
released.  It is supplier-compatible by the downward-closure premise.

The root target is

\[
 X_r-J+V,
\]

so its exact margin over the base is

\[
 v_r(V)-v_r(J).                                  \tag{5}
\]

The recipient margin is

\[
 \varepsilon_s(R_s)-v_s(V).                     \tag{6}
\]

Consequently, if

\[
 V\subsetneq S^+,
 \qquad v_s(V)\le\varepsilon_s(R_s)
 \quad\hbox{and}\quad
 v_r(V)\ge v_r(J),                              \tag{7}
\]

both floors hold.  Bundle nondegeneracy makes the second inequality strict:
the bundles `X_r-J+V` and `X_r` are physically distinct because `J` is
nonempty and `J subseteq S^-` is disjoint from `V subseteq S^+`.  Therefore

\[
 v_r(X_r-J+V)>v_r(X_r).                          \tag{8}
\]

Equivalently, relative to current root bundle `Y_r`, the packet
`S^+-V` is released and `S^--J` strictly overpays its exact root price.  The
strict-root overpayment/sacrifice theorem therefore applies.  Its complete
comparison audit gives EFX lexicographic improvement, PI, proper retired
collision support, rank/supplier progress, or the already typed root-star
routing.

## Exact pure-overlap survivor

After every overlap swap is exhausted, each minimal top-up `R_s` whose only
conflict with restoration is overlap satisfies

\[
 v_s(V)\le\varepsilon_s(R_s)
 \quad\Longrightarrow\quad
 v_r(V)<v_r(R_s\cap S^-)
 \qquad(V\subsetneq S^+).                        \tag{9}
\]

This is the **restoration-overlap bi-row cut**.  It is stronger than saying
that `R_s` meets `S^-`: every root-surplus packet affordable from the
recipient's top-up slack is worth less to the root than the exact overlap
that blocks restoration.

Equivalently, every proper root-crossing packet is too expensive in the
recipient row:

\[
 V\subsetneq S^+,
 \quad v_r(V)\ge v_r(J)
 \quad\Longrightarrow\quad
 v_s(V)>\varepsilon_s(R_s).                      \tag{10}
\]

Since (1) gives `v_r(S^+)>v_r(J)`, either such a proper root-crossing `V`
exists and (10) prices every one above the available recipient slack, or no
proper subset crosses at all. In the latter, root-atomic branch,
nondegeneracy sharpens the boundary to

\[
 v_r(S^+-g)<v_r(J)<v_r(S^+)
 \qquad(g\in S^+).                               \tag{11}
\]

The obstruction is therefore either genuinely cross-row or a root-atomic
whole-surplus cut. Neither follows from supplier labels or totals alone.

## Typed consequences

- **Strict capture:** the captured margin appears only through the exact
  top-up slack in (3).
- **Equality capture:** `mu=0` is allowed; the base-floor equality face is
  separately impossible by reference-floor rigidity.
- **Base-floor debt:** (7) waives only rows covered by the existing strict-
  root sacrifice theorem.  A protected earlier-row debt remains explicit.
- **Release:** this lemma covers pure physical overlap.  Disjoint packets
  whose supplier/protected modes are incompatible remain a separate signed-
  mode obstruction.

## Claim boundary

This lemma proves the exact margins (5)--(6), the strict-root overlap swap,
and the terminal cuts (9)--(11). It does not force an affordable proper
`V`, resolve
supplier-mode incompatibility without physical overlap, populate a deficient
root-payment family, eliminate the resulting bi-row cut from GG topology,
close `T_{L,times}^*`, or prove four-agent/general EFX.

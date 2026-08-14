# Supplier-aligned base-donation packet-spread theorem

**Date:** 2026-08-14

**Status:** conditional support-spread lemma. The set-theoretic separation is
cap-free, but the restoring donation has not been derived as an admissible
transition from an arbitrary `T_{L,times}^*` state.

## General protected-root packet-spread statement

Let `K subseteq Y_r` be any named root-held retired packet and put

\[
 U=K\cap X_r,
 \qquad W=K\setminus X_r.                        \tag{0}
\]

If `|W|>=2`, choose any `g in W`, restore the base allocation, and donate
`g` from its base cell to the root as below. The enlarged root target meets
`K` in `U+g`, while every other target meets `K` only in a subset of
`W-g`. Both intersections are proper. Conditional on admission of this
restoring donation and its extracted response, the response argument below
separates this branch without any root-payment packet.

Consequently an arbitrary protected-root payment-deficiency terminal can
survive this on-packet donation only if

\[
 K\subseteq X_r
 \quad\hbox{or}\quad
 |K\setminus X_r|=1.                             \tag{0a}
\]

The equality/base-restoration face is sharper: it forces `W=S^+` and
`U` nonempty, as used next.

There is a second, stronger spread whenever some

\[
 h\in G\setminus(X_r\cup K)                       \tag{0b}
\]

exists. Restore the base and donate this off-packet good `h` to the root.
The root target meets `K` only in `U`; every other target meets it only in
`W`. When both are nonempty, neither target can contain all of `K`, so every
response again has a proper or empty intersection. This gives the same
conditional separation for `|W|=1` with nonempty `U` unless `K` contains
every good outside `X_r`.

Under the frozen three-nonsingleton `GG` import, all three nonroot base
bundles are nonempty and base charity is the singleton `{f}`. Hence
`G-X_r` has at least four goods. In the equality/base-restoration face,
`U` is nonempty. If `|S^+|=1`, an off-packet `h` therefore exists; if
`|S^+|>=2`, the on-packet argument applies. Thus the entire root equality
base-restoration face satisfies the support-spread condition inside the exact
`GG` contract. Closing it still requires the transition-admissibility gate.

## Base-crossing input

Let `X` be the globally lexicographically maximal EFX-with-charity base and
let `r` be its first-priority root.  In the surviving nondegenerate root
equality face write

\[
 S^+=Y_r\setminus X_r,
 \qquad S^-=X_r\setminus Y_r,
 \qquad
 K=S^+\mathbin{\dot\cup}U,                       \tag{1}
\]

where

\[
 \varnothing\ne U=K\cap X_r.                    \tag{2}
\]

The full signed decoration identifies the base owner (or base charity) of
every good of `S^+` and the current holder of every good.  Thus restoring
`X` is a physical reversal of the complete signed transfer state, not a
scalar reconstruction.

## One-good base donation

Choose `g in S^+`.  Restore every good to its base cell and then donate `g`
from that base cell to the root.  The resulting complete physical candidate
`Z^g` is

\[
 Z_r^g=X_r+g.                                    \tag{3}
\]

If `g in X_a` for a nonroot owner `a`, put

\[
 Z_a^g=X_a-g,
 \qquad Z_i^g=X_i\quad(i\notin\{r,a\}),          \tag{4}
\]

and retain the base charity.  If `g` was in base charity, shrink charity by
`g` and leave every nonroot base bundle unchanged.  Every transfer has its
actual signed supplier, every nonselected moved good returns to its base
cell, and no good is duplicated or discarded beyond the declared charity.
This is therefore a supplier-complete controlled base restoration followed
by one explicit donation edge.

Positivity gives

\[
 v_r(Z_r^g)>v_r(X_r).                             \tag{5}
\]

If `Z^g` is EFX, it contradicts global fixed-priority maximality.  Otherwise
choose a globally minimum desired response `D` at the actual candidate.
It is current-safe there.  The root-donation blocker localization says that
`D` lies in exactly one candidate target (or charity): the enlarged root
target, the shrunken donor's failure target, or an unchanged base target.

## Packet-spread property

At the base, `U subseteq X_r`, whereas every good of `S^+` lies outside
`X_r`.  In the donation candidate the root target contains exactly

\[
 K\cap Z_r^g=U+g.                                \tag{6}
\]

The intersection of every nonroot or charity target with `K` contains only
goods of `S^+`, and therefore misses the nonempty packet `U`. Hence that
intersection is always proper.

If `|S^+|>=2`, equation (6) also misses at least one surplus good.  Thus
**every** single-target response satisfies

\[
 D\cap K\subsetneq K.                            \tag{7}
\]

If the intersection is nonempty, the response has strictly smaller
intersection with the named packet; if it is empty, it is ledger-free. These
are geometric facts about the tested allocation. They are a permitted
packet/hitting reduction only if full restoration followed by the donation
is itself an admissible `G0--G10` operation, or is decomposed into already
admissible operations preserving floors, supplier releases, and the anchor
label. The frozen contract explicitly rules out promoting an arbitrary test
allocation or response to progress. No such decomposition is proved here.

## Exact singleton-surplus diagnostic before the off-packet refinement

It remains to take

\[
 S^+=\{g\}.                                      \tag{8}
\]

Every response outside the root target still has proper retired
intersection because it misses `U`.  Consequently a whole-`K` recurrence is
possible only when

\[
 D\subseteq X_r+g,
 \qquad K=U+g\subseteq D.                        \tag{9}
\]

The globally minimum response is proper: unsafety of `X_r+g` supplies a
desired deletion, so minimum cardinality cannot select the whole target.
Therefore

\[
 L=(X_r+g)\setminus D
\]

is nonempty.  Equations (8)--(9) force the sharper physical form

\[
 \varnothing\ne L\subseteq X_r\setminus U,
 \qquad
 D=(X_r\setminus L)+g.                           \tag{10}
\]

If no off-packet donation is available, the only whole-packet survivor is a
current-safe nonroot response to a
one-good enlarged base-root target which contains the complete retired
packet and omits a nonempty base-root residual `L` disjoint from `K`.

In the root row, exactly one of the familiar branches holds:

\[
 v_r(D)>v_r(X_r),
 \quadhbox{or}\quad
 v_r(D)<v_r(X_r),                                \tag{11}
\]

where equality is excluded by bundle nondegeneracy.  The first is an
immediate safe root-anchor reselection.  The second is the remaining
singleton-surplus/root-response price face; (10) supplies its exact missing
base residual and eliminates arbitrary packet geometry.

## Typed and provenance consequences

- **Strict/equality capture:** the construction does not use recipient
  margin.  Both enter the same packet-spread argument.
- **Base-floor debt:** no current auxiliary floor is assumed during the
  global base-donation test.  The EFX endpoint is compared directly with
  `X`; every failure is extracted at the actual candidate.
- **Release:** the signed decoration identifies every proposed reversal and
  donation supplier, but identification is not supplier closure. In
  particular, restoration may move retired goods away from their recorded
  current holders. That release must be justified before execution.
- **Finite progress:** a proper intersection or ledger-free response becomes
  progress only after an admissible operation adopts the corresponding
  allocation/response coordinate.

## Claim boundary

This lemma proves feasibility of the displayed donation as a bare
allocation, the on/off-packet support-spread property, and the singleton
diagnostic (10). It does not prove that full base restoration is an
admissible transition, pay the recorded current holders of retired goods,
preserve all typed floors and release modes, or justify adoption of the
extracted response. Consequently it does not yet eliminate a
`T_{L,times}^*` branch or prove four-agent/general EFX.

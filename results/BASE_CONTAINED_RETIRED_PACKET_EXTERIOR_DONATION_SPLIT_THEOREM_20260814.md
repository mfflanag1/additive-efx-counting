# Base-contained retired-packet exterior-donation split theorem

**Date:** 2026-08-14

**Status:** conditional exterior-donation dichotomy. The arithmetic and
support cut are exact, but the global pooling allocation is not yet an
admissible transition from the frozen collision state.

## Input

Let `X` be the globally fixed EFX-with-charity base, with first-priority root
`r`, and let

\[
 O=G\setminus X_r                                  \tag{1}
\]

be the complete physical exterior of the base root bundle, including all
nonroot base bundles and base charity.  Let the named root-held retired
packet satisfy

\[
 \varnothing\ne K\subseteq X_r.                  \tag{2}
\]

This is the branch left by supplier-aligned packet spreading when the packet
has no good outside the base root support.

## Complete exterior-donation candidate

Choose `g in K` and any nonroot owner `a`.  Form the complete allocation

\[
 Z_r=(X_r-g)\mathbin{\dot\cup}O,
 \qquad Z_a=\{g\},                                \tag{3}
\]

give the other two nonroot owners empty bundles, and leave no charity.  This
is a physical allocation of every good.  The full signed supplier component
contains all owners whose base goods enter `O`; the released root good is
assigned exactly once.  No PI or local release shortcut is assumed.

The exact root margin is

\[
 v_r(Z_r)-v_r(X_r)=v_r(O)-v_r(g).                 \tag{4}
\]

If

\[
 v_r(O)>v_r(g),                                   \tag{5}
\]

the root is strictly above the globally maximal base.  The singleton target
`{g}` is universally EFX-safe because every one-good deletion is empty; the
other nonroot and charity targets are empty.  Hence every EFX failure is
against the single enlarged root target `Z_r`.

Choose a globally minimum desired response `D subseteq Z_r` at the actual
candidate.  It is current-safe.  Its retired intersection obeys

\[
 D\cap K\subseteq K-g.                            \tag{6}
\]

For `|K|>=2`, every nonempty hit is therefore proper. For `K={g}`, every
response is ledger-free. Thus (5) gives the displayed EFX endpoint or a
response whose intersection with `K` is proper/empty. Calling the latter
strict progress requires an admissible operation that adopts (3) and its
response. The current contract contains no theorem allowing arbitrary
pooling of all exterior goods into the root while sacrificing three nonroot
assignments, so this step remains conditional.

## Exact exterior-dominance survivor

If no `g in K` satisfies (5), bundle nondegeneracy excludes equality between
the physically distinct packets `O` and `{g}`.  The surviving packet obeys

\[
 v_r(O)<v_r(g)
 \qquad(g\in K).                                  \tag{7}
\]

Because valuations are positive, (7) also implies that **no** nonempty
subpacket of `K` can be released while the entire exterior replaces it:

\[
 \varnothing\ne T\subseteq K
 \quad\Longrightarrow\quad
 v_r(O)<v_r(T).                                   \tag{8}
\]

Summing (7) gives the charge

\[
 |K|\,v_r(O)<v_r(K).                              \tag{9}
\]

This is the complete exterior-pool atomwise dominance cut.  It is much
stronger than failure of a named compensation menu: every good outside the
base root bundle, taken together, is worth less to the root than each
individual retired atom.

## Composition consequence

Conditional on admissibility of both global test allocations, combining
supplier-aligned packet spreading with this dichotomy would reduce the
protected-root direct branch to:

1. the exterior-dominance cut (7)--(9) for `K subseteq X_r`; or
2. a packet with at most one good outside `X_r` in a state lacking an
   off-packet donation good; under the frozen GG base-cardinality premises,
   the base-crossing equality face cannot satisfy this second alternative.

Without that admission theorem, (7)--(9) is the exact scalar obstruction to
this proposed exterior-pooling route, not the sole remaining collision
obstruction.

## Claim boundary

This lemma proves physical feasibility of (3) as a bare allocation, wall
localization there, the proper/empty intersection property, and the
conditional cut (7)--(9). It does not establish (3) as an admissible
GG/ledger transition, preserve the sacrificed owners' typed floors, close
their suppliers, or make its extracted response a finite progress step.
Therefore it does not yet reduce the actual `T_{L,times}^*` terminal.

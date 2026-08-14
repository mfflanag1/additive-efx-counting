# Root-equality base-restoration packet-spread admission theorem

**Date:** 2026-08-14

**Status:** cap-free elimination of every admitted root-equality packet-price
mode under the frozen nondegenerate GG import

## Equality normal form

Use the root-strict clean-release theorem and suppose one of its survivor
inequalities is tight for nonempty `T subseteq K` and admitted exterior mode
`R`:

\[
 v_r(R)=v_r(T)-\delta.                           \tag{1}
\]

The post-release root target has value `x`.  Bundle nondegeneracy and the
nondegenerate root-equality theorem force the physical identities

\[
 T=S^+:=Y_r\setminus X_r,
 \qquad R=S^-:=X_r\setminus Y_r,                \tag{2}
\]

and therefore `S^+ subseteq K`.  In particular, `S^-` is already an admitted
signed return mode in the equality branch; the proof below does not assume
that arbitrary full base restoration is available.

## Case I: at least two incoming root goods

Suppose `|S^+|>=2` and choose `g in S^+`.  Release

\[
 T'=S^+-g
\]

using the same admitted packet `S^-`.  This is a nonempty proper subpacket
of `K`.  Set equality (2) gives the new root target

\[
 (Y_r\setminus T')+S^-=X_r+g.                  \tag{3}
\]

It is strictly above the base root value by positivity.  The clean-release
admission theorem therefore applies.  If the candidate is EFX, it
contradicts global lexicographic maximality.  Otherwise its globally minimum
response has proper or empty intersection with `K` because `T'` and
`K-T'` lie in different targets.  Thus the equality mode cannot survive.

Equivalently, the strict inequality is visible directly:

\[
 v_r(S^-)>v_r(S^+-g)-\delta
\]

because `v_r(S^+)-v_r(S^-)=delta`.

## Case II: one incoming root good

Now let `S^+={g}`.  In the frozen GG import, the three nonroot base bundles
are nonempty and base charity is a singleton.  Hence `G-X_r` contains at
least four goods.  Choose

\[
 h\in G\setminus(X_r\cup K).                    \tag{4}
\]

Such an `h` exists because `K-X_r=S^+` is a singleton.  Moreover `h` is not
in the current root target: every current root good outside `X_r` belongs to
`S^+ subseteq K`.

Use the admitted equality return `S^-`, release `S^+` from the root, and
add `h` to the root.  Give `S^+` alone to the named sacrificed nonroot owner;
the current holder of `h` supplies it and may also be sacrificed.  All
displaced goods go to their recorded residual targets or charity.  If `h`
has another retirement label, that collision and its current supplier are
recorded explicitly; it is not silently normalized or called unavailable.
If moving `h` changes a protected physical anchor, that exact label change
is a permitted anchor transition.

The root target is

\[
 X_r+h,                                         \tag{5}
\]

so the root is strict.  The named packet is spread between the restored
root part `K cap X_r` and the target containing `S^+`; the donated good `h`
is outside `K`.  Hence every target has proper or empty intersection with
`K`, except when `K=S^+` is a singleton.  In that exceptional case its
singleton target cannot be strongly envied, so every extracted response
avoids `K`.

Thus an EFX candidate contradicts maximality, while every non-EFX candidate
strictly reduces the named packet intersection.  A second retired label on
`h` does not defeat this conclusion: its signed collision is adopted only
together with the strict root allocation/response, while the selected
coordinate `K` has already decreased.

## Consequence

No equality instance of the packet-price cut survives.  Combining this
theorem with strict clean subpacket release, every admitted mode satisfying

\[
 v_r(R)\ge v_r(T)-\delta
\]

gives an EFX lexicographic contradiction, controlled anchor change, or
strict reduction of the named packet/hitting coordinate.  Therefore a
recurrent root-held packet must satisfy the strict cut

\[
 v_r(R)<v_r(T)-\delta
 \qquad(\varnothing\ne T\subseteq K)            \tag{6}
\]

for every admitted compatible mode.

For a common singleton mode of root value `M_r`, every atom now obeys

\[
 v_r(g)>\delta+M_r.                              \tag{7}
\]

The remaining root obstruction is strict aggregate underpayment, not a
priority equality face.

## Claim boundary

This theorem composes a *given admitted equality mode* with nondegeneracy,
the GG base-size import, and two explicit strict packet-spread operations.
It does not prove that a positive common exterior mode exists, close strict
aggregate underpayment, prove well-foundedness when repeated operations
change to a different retired packet of equal rank, close normalization-
bypass states, `T_{L,times}^*`, GG, four-agent EFX, or general additive EFX.

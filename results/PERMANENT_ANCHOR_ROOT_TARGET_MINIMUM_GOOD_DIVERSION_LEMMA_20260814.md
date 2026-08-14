# Permanent-anchor root-target minimum-good diversion lemma

**Date:** 2026-08-14

**Status:** cap-free reduction of aggregate root-target capture to a
single-good critical envelope or an explicit three-edge probe

## Root-target response

Use the permanent-anchor partial allocation

\[
 B_r=Y_r\mathbin{\dot\cup}A,qquad
 B_q=Y_q\setminus A,qquad v_r(B_r)>v_r(X_r),    \tag{1}
\]

with positive singleton `p` and strict root margin

\[
                         \delta_r=v_r(B_r)-v_r(X_r)>0.           \tag{2}
\]

Suppose a transported disjoint response has nonroot source `i` and root
target, with nonempty core `E subseteq B_r`.  Choose a least-`r` good
`g in E`.

## Divert one good, not the whole response

Give both `p` and `{g}` to source `i`, leave every other owner unchanged, and
remove only `g` from the root:

\[
 C_r=B_r\setminus\{g\},qquad
 C_i=B_i\mathbin{\dot\cup}\{p,g\},qquad
 C_j=B_j\quad(j\notin\{r,i\}).                  \tag{3}
\]

The operation does not need `{g}` to remain desired.  Positivity makes source
`i` strictly better because it receives `p+g` in addition to its old bundle.

If `g` was originally in `Y_r`, the only pairs are

\[
 q\to r:A,qquad r\to i:g,qquad charity\to i:p.
\]

If `g in A`, its transfer uses `q -> i`; an unselected anchor residual may
leave `q -> r` active.  Together with `charity -> i`, this again gives at most
three pairs.  Thus (3) is a complete at-most-three-edge allocation for
arbitrary anchor and response cardinalities.

## Exact item-critical alternative

The root remains strictly above its base exactly when

\[
                         v_r(g)<\delta_r.                         \tag{4}
\]

If (4) fails, minimality of `g` yields

\[
                         v_r(e)\ge v_r(g)\ge\delta_r
                         \qquad(e\in E).                          \tag{5}
\]

Hence aggregate capture `v_r(E)>=delta_r` is replaced by the much stronger
statement that **every physical good** of the response individually captures
the root's entire strict margin.

If (4) holds and (3) is EFX, it is the required strict-root lexicographic
endpoint.  If it is non-EFX, globally minimal extraction supplies an exact
decorated response at this named three-edge probe.  A new record/support
coordinate is saturated progress; an old record is the remaining recurrence.

## Claim boundary

Proved: conservation, strict improvement of the nonroot response source, the
three-edge bound, the exact root inequality, and itemwise capture (5).  Not
proved: contradiction of the item-critical envelope, closure of the probe's
exact repeated response, the singleton-hit changed-state continuation,
global fixed-`U` composition, the fixed-`U` theorem, or general EFX.

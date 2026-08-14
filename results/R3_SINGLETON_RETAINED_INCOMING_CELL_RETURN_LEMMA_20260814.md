# R3 singleton-retained incoming-cell return lemma

**Date:** 2026-08-14

**Status:** cap-free elimination of every remaining two-target support
signature; exact root-margin capture and observer repeat remain

## Signed state after leaf liquidation

Use the nonrecruiting state produced by root-star leaf liquidation.  The
first-priority root `x` is strict, owner `z` holds the positive singleton
`p`, owner `d` is unchanged, and the only possible owner-supplier pairs are

\[
                         y\to x,qquad z\to x,
                         \qquad z\to y.           \tag{1}
\]

Write the corresponding root bundle as

\[
                         B_x=X\mathbin{\dot\cup}U
                              \mathbin{\dot\cup}V,               \tag{2}
\]

where `X,U,V` are supplied by `x,y,z`, respectively.  Empty cells simply
delete their pair from (1).  Put

\[
                         \delta_x=v_x(B_x)-v_x(X_x)>0.           \tag{3}
\]

No response-core assumption is needed below.

## Canonical return menu

Keep `p` at `z` and choose a nonempty packet `L` as follows.

1. For every good `g in V`, include the singleton `{g}` in the menu.
2. If `U` is nonempty, include the whole cell `U`.
3. If both `U,V` are empty, include a least-`x` singleton from `X`.

Choose a menu member of minimum root value and form

\[
 Z_x=B_x\setminus L,qquad Z_z=\{p\}\mathbin{\dot\cup}L,
 \qquad Z_y=B_y,qquad Z_d=B_d.                  \tag{4}
\]

Owner `z` strictly improves for every menu member by positivity.  The root
remains strict exactly when

\[
                         v_x(L)<\delta_x.                         \tag{5}
\]

## Universal four-edge identity

Every menu operation stays within four edges.

- A singleton from `V` returns to its original supplier `z`.  It creates no
  pair and may delete `z -> x` if it exhausts `V`.
- Moving the whole `U` replaces `y -> x` by `y -> z`; it adds no net pair.
- When `U=V=empty`, moving one `x`-supplied good creates only `x -> z`, while
  both incoming-root pairs are absent.

In every case the untouched owner pairs are a subset of (1), and
`charity -> z` remains the single charity pair.  Hence (4) has at most four
packet-transfer edges for arbitrary cell and packet cardinalities.

This removes the five uncompensated signatures in the earlier
response-subpacket census.  Those signatures were artifacts of requiring
`L subseteq D_z`, a restriction unnecessary when `z` retains `p`.

## Exact separator

If (5) holds and (4) is EFX, it is the required strict-root lexicographic
endpoint.  If (4) is not EFX, globally minimal extraction gives an exact
decorated response at this named four-edge probe.

If (5) fails for the minimum menu member, every menu member satisfies

\[
                         v_x(L')\ge\delta_x.                       \tag{6}
\]

Thus every `z`-supplied good currently held by the root and the whole
`y`-supplied root cell (when present) individually capture the root's entire
strict margin.  In the degenerate no-incoming-cell case, even the least root
good does.  The surviving obstruction is therefore a sharply typed
root-critical incoming-support separator, not topology or response-core
compatibility.

## Claim boundary

Proved: completeness, strict improvement of `z`, the exact root condition,
and the universal at-most-four-edge identity for every presence pattern of
`U,V`.  Not proved: contradiction of (6), observer/repeat closure at (4),
the backward path or later-source anchor separator, full fixed-`U`, or
general EFX.

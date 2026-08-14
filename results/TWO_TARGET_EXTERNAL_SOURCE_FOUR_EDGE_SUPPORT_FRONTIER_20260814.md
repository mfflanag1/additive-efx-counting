# Two-target external-source four-edge support frontier

**Date:** 2026-08-14

**Status:** exact cap-free supplier-pair classification for the remaining
`2 targets / 1 external source` Hall star

## Signed target support

Start from the rank-three matching rotation `B`, which uses exactly three
nonself supplier-recipient pairs relative to the saturated allocation `Y`.
Fix a current target owner `t`.  Its bundle has at most two signed parts:

\[
 B_t=R_t\mathbin{\dot\cup}C_t,                    \tag{1}
\]

where `R_t` is retained support originally supplied by `t`, and `C_t` is the
incoming selected matching packet originally supplied by `u != t`.  The
packet `C_t` may be empty when `t` is not a represented matching source.

Let an external Hall source `x != t` receive a response core

\[
 E=R'\mathbin{\dot\cup}C',
 \qquad R'\subseteq R_t,quad C'\subseteq C_t,    \tag{2}
\]

and give the charity singleton `p` to the sacrificed old target `t`.  Leave
every other matching transfer unchanged.  This is the canonical two-edge
charity path `charity -> t -> x` after the initial matching rotation.

## Exact edge-budget theorem

The final allocation has at most four distinct supplier-in-`Y`/recipient
pairs if and only if `C_t` is nonempty and one of the following holds.

1. **Return to the incoming supplier:** `x=u`, and either
   - `R'` is empty (while `C'` is any nonempty subpacket of `C_t`); or
   - `C'=C_t` (while `R'` is arbitrary, including nonempty).
2. **Redirection to a third owner:** `x!=u`, `R'` is empty, and
   `C'=C_t`.

Equivalently, a residual good from `R_t` can enter the response only when the
whole incoming packet returns to its original supplier and thereby removes
the old edge `u->t`.  A proper nonempty split of `C_t` can move only back to
`u`, with no retained-support import.  Any response into a target with no
incoming packet creates a fifth edge.

## Proof by signed destinations

The two matching pairs not entering `t` remain, and `charity->t:p` is the
fourth baseline pair.  It remains to keep the signed contribution of (1)--(2)
to at most one owner edge.

If `x=u`, moving `C'` back to its supplier creates no edge.  The old edge
`u->t` remains exactly when `C'!=C_t`; moving any `R'` creates `t->u`.
Hence the contribution is

\[
 \mathbf 1[C'\ne C_t]+\mathbf 1[R'\ne\varnothing], \tag{3}
\]

which is at most one precisely in case 1.

If `x!=u`, a whole `C_t` replaces `u->t` by `u->x`, a proper nonempty `C'`
uses both pairs, and `R'` adds `t->x`.  Nonemptiness of `E` then leaves only
the whole-incoming/no-residual case 2.

## Consequence

The graph-level `2x1` Hall star is not automatically a four-edge endpoint.
Its exact surviving physical question is whether at least one of the two
target responses can be chosen in the return/redirection forms above.  If
both minimum universally safe cores mix retained support with a proper
incoming residual, the simple charity path is provably outside the edge
budget; one must split/retire support, change the selected matching, use the
`3x2` fork, or produce a countermodel.

## Boundary

This theorem classifies supplier-pair feasibility of the canonical `2x1`
repair.  It does not prove that an edge-compatible desired core exists, show
that either compatible endpoint is EFX, close its observer responses, solve
the `3x2` fork, prove fixed-`U`, or prove four-agent/general additive EFX.

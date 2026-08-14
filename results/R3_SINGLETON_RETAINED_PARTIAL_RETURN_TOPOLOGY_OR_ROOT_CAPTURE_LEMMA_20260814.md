# R3 singleton-retained partial-return topology-or-root-capture lemma

**Date:** 2026-08-14

**Status:** cap-free elimination of 21 of 26 direct-return topology signatures
up to one exact root-margin packet; five uncompensated signatures remain

## Keep the singleton and trim the response

Use the two-target state

\[
 B_x=X\mathbin{\dot\cup}U\mathbin{\dot\cup}V,
 \qquad B_y=Y\mathbin{\dot\cup}W,
\]

with strict root `x`, singleton holder `z`, and signed pairs
`y -> x`, `z -> x`, `z -> y`, and `charity -> z`.  Let the singleton
holder's desired core in the root be

\[
 D_z=A_x\mathbin{\dot\cup}A_y\mathbin{\dot\cup}A_z
       \subseteq X\mathbin{\dot\cup}U\mathbin{\dot\cup}V.     \tag{1}
\]

Unlike the direct-return selector, keep `p` at `z` and move only a nonempty
packet `L subseteq D_z` from the root to `z`:

\[
 Z_x=B_x\setminus L,\qquad Z_y=B_y,
 \qquad Z_z=\{p\}\mathbin{\dot\cup}L,
 \qquad Z_d=B_d.                                  \tag{2}
\]

Positivity makes `z` strictly better for every nonempty `L`; `L` need not
remain desired by itself.  Thus inclusion-minimality of `D_z` does not block
this trimming operation.

## Complete topology criterion

Write `L=L_x dotcup L_y dotcup L_z` according to the three supplier cells.
Besides the mandatory pairs `charity -> z` and `z -> y`, the exact indicators
are

\[
 x\to z\iff L_x\ne\varnothing,
 \quad y\to x\iff U\setminus L_y\ne\varnothing,
 \quad y\to z\iff L_y\ne\varnothing,
 \quad z\to x\iff V\setminus L_z\ne\varnothing. \tag{3}
\]

Hence (2) uses at most four edges exactly when at most two conditions in (3)
hold.  Such a nonempty `L subseteq D_z` exists if and only if

\[
                         A_z\ne\varnothing
                         \quad\text{or}\quad A_y=U.             \tag{4}
\]

Indeed, if `A_z` is nonempty, return any one good of `A_z`; this creates no
new owner pair.  If `A_z` is empty but `A_y=U`, move the whole cell `U`, which
replaces `y -> x` by `y -> z`.  Conversely, with `A_z` empty and `A_y` empty
or proper, every nonempty subpacket either creates `x -> z` without deleting
an edge, creates `y -> z` while retaining `y -> x`, or does both.

Thus 21 of the 26 nonempty none/proper/all signatures admit a partial return.
The five exact topology obstructions are

\[
 (A_x,A_y,A_z)\in
 \{(0,P,0),(P,0,0),(P,P,0),(A,0,0),(A,P,0)\},   \tag{5}
\]

where `0,P,A` mean none, proper, and all.

## Root-margin alternative

Let

\[
                         \delta_x=v_x(B_x)-v_x(X_x)>0.          \tag{6}
\]

Form the canonical packet menu consisting of every singleton `{g}` with
`g in A_z`, together with `U` when `A_y=U`, and choose an `x`-minimum member
`L`.  Condition (4) says this menu is nonempty.  The root remains strict
exactly when

\[
                         v_x(L)<\delta_x.                        \tag{7}
\]

If (7) fails, the canonical edge-compatible packet obeys

\[
                         v_x(L)\ge\delta_x.                      \tag{8}
\]

If (8) holds, every available `z`-supplied singleton and, when available, the
whole `y`-supplied cell has root value at least `delta_x`.  In particular the
separator is witnessed by either one physical good or one complete old
supplier cell, and the minimum choice rules out a cheaper compatible repair.

## Consequence and boundary

If (7) holds and (2) is EFX, it is the required strict-root four-edge
endpoint.  If it is not EFX, it gives an explicit decorated-response probe.
Therefore every singleton-holder root response now yields one of:

1. a priority-valid four-edge partial-return probe;
2. a single-good or whole-cell root-margin capture (8); or
3. one of the five exact uncompensated signatures (5).

This lemma does not contradict (8), route the five signatures, close the
probe's observer/repeat response, handle the backward path or singleton
star, close the later-source anchor separator, prove fixed-`U`, or prove
general EFX.

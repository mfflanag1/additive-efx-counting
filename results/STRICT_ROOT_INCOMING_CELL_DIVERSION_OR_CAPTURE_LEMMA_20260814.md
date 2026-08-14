# Strict-root incoming-cell diversion-or-capture lemma

**Date:** 2026-08-14

**Status:** cap-free elimination of incoming-root support topology at every
at-most-four-edge probe; root-origin response recurrence remains open

## Setting

Let `C` be a complete allocation reached from a fixed physical supplier state
through at most four nonidentity supplier-recipient pairs.  Owner `r` is
strictly above its immutable base:

\[
                         \eta_r=v_r(C_r)-v_r(X_r)>0.              \tag{1}
\]

For a supplier `s!=r`, let `K_s` be the complete nonempty cell of goods
originally supplied by `s` and currently held by `r`.  Thus the current
support contains the pair `s -> r`.  Choose any nonroot owner `j`.

## Divert the whole incoming cell

Move all of `K_s` from the root to `j`, leaving every other good fixed:

\[
 C'_r=C_r\setminus K_s,\qquad
 C'_j=C_j\mathbin{\dot\cup}K_s.                  \tag{2}
\]

Owner `j` strictly improves by positivity.  The root remains strictly above
base exactly when

\[
                         v_r(K_s)<\eta_r.                          \tag{3}
\]

## Edge identity

Because `K_s` is the complete `s`-supplied root cell, operation (2) deletes
`s -> r`.  It adds `s -> j` when `s!=j`; if `s=j`, the cell simply returns to
its supplier and adds no edge.  Therefore

\[
 |E(C')|=|E(C)\setminus\{s\to r\}
                    \cup (\{s\to j\}\text{ if }s\ne j)|
          \le |E(C)|\le4.                        \tag{4}
\]

This remains true when another packet already uses `s -> j`, because directed
pairs merge.  Packet cardinality is unrestricted.

## Exact alternative at a failed root probe

Apply (2) to every nonroot incoming supplier cell of a strict-root probe.
Either one cell satisfies (3), giving another explicit complete priority-valid
probe without increasing the four-edge count, or

\[
                         v_r(K_s)\ge\eta_r                         \tag{5}
\]

for every nonroot incoming root cell.

At a permanent-anchor bilateral probe these cells include, when present:

1. the residual anchor cell supplied by `q`;
2. the returned compensator cell supplied by the response source; and
3. the charity singleton supplied by charity.

Consequently topology cannot obstruct diversion of any of those cells.  A
survivor makes each complete incoming cell individually capture the root's
entire remaining margin.  After this reduction, the only cell for which a
diversion may add a fifth edge is root-origin residual support.

If a displayed diversion is EFX, it is the required endpoint.  If it is
non-EFX, minimum-response extraction gives the next exact decorated response
at a named four-edge probe.

## Claim boundary

Proved: conservation, strict recipient improvement, the exact root inequality,
the nonincreasing-edge identity, and the incoming-cell capture separator.
Not proved: contradiction of simultaneous capture (5), closure of the
decorated response at a diversion probe, handling of a four-edge root-origin
response, the singleton-hit envelope after changing state, the fixed-`U`
theorem, or general EFX.

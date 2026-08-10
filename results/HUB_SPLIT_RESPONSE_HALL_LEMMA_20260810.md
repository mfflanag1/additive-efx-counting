# Hub-split response-Hall lemma

**Date:** 2026-08-10

**Status:** cap-free analytic lemma; flower-specific response matching remains
open

## Response sources

Let `(X,{f})` be a partial EFX allocation and consider an improving complete
hub split

\[
Y_h=X_h\setminus R+f,
\qquad Y_k=X_k+R_k\quad(k\in L),
\qquad R=\mathbin{\dot\bigcup}_{k\in L}R_k.
\]

Every changed owner strictly prefers her proposed target bundle to her base
bundle.  Therefore every proposed target is envied relative to `X` and has
at least one most-envious agent.  Define `C_j` to be the set of all such
agents for target `Y_j`, always relative to the base allocation `X`, not to
the candidate owners' increased utilities.

Each `a in C_h` supplies a generalized `(f|R)` edge `a -> h`.  Each
`a in C_k` supplies a generalized `(R_k|empty)` edge `a -> k`.  The labels
record the entire offered incoming sets even when the selected desired
subset discards some of them, exactly as in BCFF Definition 3.1.

## Response-Hall conclusion

Let `T={h}\cup L` and restrict every `C_j` to internal sources in `T`.

1. If `h in C_h`, the hub self-edge is a PI self-cycle: its incoming set
   `{f}` is unallocated.  Thus a PI-free state has `h notin C_h`.
2. If the internal response sets admit a system of distinct representatives,
   choose one distinct source for every target.  The selected directed edges
   form vertex-disjoint cycles on `T`.  Their incoming sets `{f}` and the
   packets `R_k` are pairwise disjoint, while the selected hub edge releases
   all of `R`.  Hence they form a BCFF PI edge set.
3. Consequently, in a PI-free state the internal response relation is Hall
   deficient.  A target with no internal response source has only sources
   outside `T` and gives a forced component-growth edge.  Otherwise an
   inclusion-minimal Hall-deficient target set is the exact closed remainder.

This restores the correct logical order.  Strong-envy observers of the
candidate are useful inequality witnesses, but they need not themselves be
the most-envious sources of the generalized edges.  Response matching must
be built from `C_j`, not from the observer set.

## Flower anchors

Two response sources in the three-packet flower are available without any
new inequality argument.

- If `c -> s` is the singleton envy edge, then `c in C_s` for every leaf
  target `X_s+R_s`: the singleton `X_s={z}` is a common-safe subset and is
  already envied by `c`.
- If the arm edge `r -f-> c` decomposes `X_c=T_c\mathbin{\dot\cup}B_c` and the hub
  releases exactly `B_c`, then `r in C_c`, since the proposed hub target is
  the arm's desired set `T_c+f`.

Thus, whenever `c(f)>c(B_c)` and `B_c` is split between leaves `r,s`, the
response matching is complete as soon as `s in C_r`; the edges

\[
r\longrightarrow c,\qquad c\longrightarrow s,\qquad s\longrightarrow r
\]

form a PI three-cycle.  In a PI-free obstruction, every such packet split
must therefore exclude `s` from the response set of the augmented `r`
target.  This is a concrete flower-specific exclusion condition, not a
generic wall sign.

## Claim boundary

The response-Hall implication is arbitrary-packet and cap-free.  It does not
prove that `c(f)>c(B_c)`, that `B_c` has a nontrivial partition, or that some
more general top/bottom packet choice admits the required matching.  Those
are the remaining flower selector obligations.

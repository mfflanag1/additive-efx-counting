# Two-source root-threshold debt derangement theorem

**Date:** 2026-08-14

**Supersession (2026-08-14):** this is a conditional diagnostic. The full
anchored `GG` collision cannot reach its exterior-dominant input.

**Status:** cap-free reduction of the final exterior-dominant source face to
a single-edge envy graph, forced CGM champion pattern, and cyclic cross-owner
root-threshold debt; debt-cycle conversion remains open

## Input

Use the exterior-dominant restricted nonroot instance

\[
 (X_1,X_2,X_3;\{f\})
\]

from the source-reduction theorem. Its ordinary envy graph is acyclic and has
exactly two sources. Write `a,b` for the sources and `t` for the unique
non-source. Every base owner satisfies

\[
 v_j(X_j)\ge\tau_j(X_r).                        \tag{1}
\]

## The ordinary graph has exactly one edge

At least one source points to `t`, since `t` is not a source. If both `a` and
`b` point to `t`, the first case of CGM Section 4 produces a complete EFX
allocation Pareto dominating the partial allocation. Fixing the root at
`X_r`, (1) preserves every cross-root threshold and exterior dominance
protects the root against every bundle in `G-X_r`. The resulting four-agent
allocation is therefore complete EFX and lexicographically above the base.

Consequently a recurrent state has exactly one ordinary edge. Relabel so that

\[
 a\longrightarrow t,
 \qquad b\not\longrightarrow t.                \tag{2}
\]

There is no edge between `a` and `b`, because both are sources.

## Forced hard champion pattern

If a nonroot agent self-champions, CGM Corollary 7 again gives a
Pareto-dominating complete EFX allocation, which closes by the same root
argument. Excluding that case, the hard two-source analysis in CGM Section 4
forces:

\[
 b\xrightarrow{f}a,
 \qquad t\xrightarrow{f}b,
 \qquad C_f(t)\cap\{a,b\}\ne\varnothing,        \tag{3}
\]

where `C_f(t)` is the set of `f`-champions of `t`. Indeed, `t` championing
`a` gives the reachable-champion Pareto update; otherwise `b` champions `a`.
If `a` champions `b`, the two-source 2-cycle case gives a Pareto update;
otherwise `t` champions `b`. Finally `t` has a champion and cannot
self-champion, leaving `a`, `b`, or both.

Thus the surviving ordinary/champion topology is one of the three hard CGM
configurations, now with the GG identities `{c,q}` or `{c,s}` substituted for
`{a,b}`.

## Three designated completions force cyclic debt

CGM fix the first agent in their lexicographic potential arbitrarily and
prove Lemma 19 for each of the three choices. For each designated nonroot
owner `j`, let `Y^j` be the resulting complete internally EFX allocation,
chosen so that

\[
 v_j(Y^j_j)>v_j(X_j).                            \tag{4}
\]

If every owner met her root threshold in `Y^j`, fixing the root at `X_r`
would again give a complete EFX allocation lexicographically above the base.
Hence each `Y^j` has a debt owner `d(j)` satisfying

\[
 v_{d(j)}(Y^j_{d(j)})<\tau_{d(j)}(X_r).          \tag{5}
\]

Equation (1) and the strict improvement (4) imply

\[
 d(j)\ne j.                                     \tag{6}
\]

Choose one debtor for each `j`. The directed map `j -> d(j)` is a self-loop-
free functional graph on three vertices. It necessarily contains a directed
cycle of length two or three.

This is a **threshold-debt cycle across designated CGM completions**. It is
not yet a release-compatible PI cycle: its edges refer to different complete
allocations, and no common family of disjoint desired cores or supplier
releases has been proved.

## Interface with the retired packet

The exact remaining collision can now be indexed by:

1. the source pair `{c,q}` or `{c,s}`;
2. the unique ordinary edge (2);
3. one of the three champion patterns (3);
4. the named charity-reset whole-`K` response source;
5. the retirement supplier/current holder; and
6. a two- or three-cycle in the debt map (5)--(6).

The next operation must realize one debt-cycle edge as a physical
supplier-compatible core exchange, contradict a retirement-time floor, or
change the root/anchor while leaving `K` at the root. Merely composing the
three output allocations is invalid.

## Claim boundary

This theorem closes the double-edge two-source graph, derives the forced hard
champion pattern, and proves cyclic cross-owner threshold debt. It does not
construct a common physical exchange from different CGM completions, identify
the debt cycle with a PI cycle, route the retirement supplier or response
source, close `T_{L,times}^*`, GG, four-agent EFX, or general additive EFX.

# Permanent-anchor different-source cross-state normalization lemma

**Date:** 2026-08-14

**Status:** cap-free transport of alternating root responses to one fixed
two-edge probe; overlap/capture and final recurrence remain open

## Alternating responses are desired at the fixed partial state

Let `B` be the permanent-anchor partial allocation of all goods except the
positive singleton `p`, with `B_r=Y_r dotunion A`.  A bilateral probe with
moved nonroot owner `a` changes only bundles `r,a` and assigns `p` to the
root.  Every other nonroot owner `u!=a` retains exactly `B_u`.

Suppose a root-target response at that probe has source `u!=a` and residual
core

\[
                         \varnothing\ne F_u\subseteq B_r.        \tag{1}
\]

Because `u` is unchanged at the probe,

\[
                         v_u(F_u)>v_u(B_u).                       \tag{2}
\]

Take two such responses with distinct sources `u,v`.  This is precisely what
two consecutive different-source steps of the bilateral recurrence provide:
each next source was unchanged at the probe where its core was discovered.

Among the three nonroot owners, let `k` be the unique owner outside `{u,v}`.
Use the original complete singleton probe

\[
 Z^k_r=B_r,qquad Z^k_k=B_k+p,qquad
 Z^k_h=B_h\quad(h\notin\{r,k\}).                  \tag{3}
\]

It uses only `q -> r:A` and `charity -> k:p`.  Both response sources retain
their fixed bundles, so (2) makes `F_u,F_v` simultaneously desired at the
same physical root target of (3).

## Safe normalization by strict cardinality descent

Start with either desired core `C subseteq B_r` and its current named source
`s`.  If `C` is not common-safe at the floors of `Z^k`, some observer `h`
satisfies

\[
                         \tau_h(C)>v_h(Z^k_h).                    \tag{4}
\]

Choose a good whose deletion realizes `tau_h(C)`.  Then `C-g` is a strictly
desired packet for source `h` at `Z^k`.  Replace `C` by an inclusion-minimal
desired subcore of `C-g` and replace its source by `h`.

Every unsafe step strictly decreases physical cardinality.  A singleton is
automatically safe because its one-good deletion is empty.  Therefore the
process terminates after at most `|C|-1` steps with a common-safe desired
response

\[
                         C^*\subseteq C                           \tag{5}
\]

at the single fixed probe `Z^k`.  No value, goods, or packet-size cap is used.
The root cannot become the terminal source: every candidate core remains a
subbundle of its own bundle `B_r`, and positivity prevents a self-response.

Normalize `F_u` and `F_v` independently.  Exactly one of the following holds.

1. **Source collision.**  Their terminal named sources coincide.  The
   alternating branch has collapsed to one root-response source at the fixed
   probe and re-enters the permanent-anchor one-source transfer/bilateral
   frontier.
2. **Distinct safe sources.**  Their terminal sources remain distinct.  The
   two terminal cores are simultaneously desired and common-safe at `Z^k`.
   If they are disjoint, the exact two-source topology-or-cross-capture lemma
   applies.  If they overlap, shared-target uncrossing yields disjoint safe
   subcores or a shared packet capturing the response margins of both
   sources.

Thus cross-state observer floors do not create a third terminal.  They cause
a well-founded core shrink and possibly a source change, both of which are
already represented in the response-saturation ledger.

## Consequence for the permanent-anchor route

Combine this lemma with same-source replacement and the two-source topology
classification.  Every residual root-response recurrence now reaches one of:

1. a four-edge priority-valid probe with response/history progress;
2. source collision and the one-source branch;
3. root-margin capture;
4. shared-overlap double capture;
5. the two-source/two-supplier cross-capture certificate; or
6. the separately typed singleton/incoming-cell continuation.

The previously named “cross-state transport gap” is therefore closed at the
level of desire, safety, and physical core localization.

## Claim boundary

Proved: common-state desire, the two-edge common probe, safe normalization by
strict core descent, and the collision/distinct-source dichotomy.  Not proved:
that every normalized distinct pair pays the root after simultaneous transfer,
contradiction of the resulting root/overlap/cross-capture inequalities,
semantic closure of the source-collision recurrence, the singleton-hit
changed-state continuation, the fixed-`U` theorem, or general EFX.

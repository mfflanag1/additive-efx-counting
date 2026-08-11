# Owner-rooted hub-split response-Hall lemma

**Date:** 2026-08-10

**Status:** cap-free analytic component lemma; flower-specific packet selection
remains open

## Owner-rooted exchange star

Let `(X,P)` be a partial EFX allocation with charity packet `P`.  Choose a
hub owner `h`, a donor leaf `d`, and a nonempty donor packet `H subseteq X_d`.
Choose a nonempty hub packet `R subseteq X_h` and partition it among distinct
leaf owners `L subseteq N\{h}`, with `d in L`:

\[
R=\mathbin{\dot\bigcup}_{k\in L}R_k.
\]

Form

\[
Y_h=X_h\setminus R+H,
\]

\[
Y_d=X_d\setminus H+R_d,
\]

\[
Y_k=X_k+R_k \quad(k\in L\setminus\{d\}),
\]

leaving every other bundle and the charity packet fixed.  Assume

\[
v_h(H)>v_h(R),
\qquad
v_d(R_d)>v_d(H). \tag{1}
\]

Every other leaf strictly improves by positivity.  Thus all changed owners
strictly improve.

## Response edges

Put `T={h} union L`.  Every proposed target `Y_j`, `j in T`, is envied
relative to `X` by its intended owner and therefore has at least one
most-envious source.  Let `C_j` be the set of all such sources, defined
relative to the base allocation `X`.

Each response source supplies the following generalized edge:

| target | incoming set | prescribed release |
|---|---|---|
| `h` | `H` | `R` |
| donor `d` | `R_d` | `H` |
| other leaf `k` | `R_k` | empty |

The label records the whole offered incoming set even if the chosen desired
subset discards part of it.  Additional discard only enlarges the release
set.

## Response-Hall theorem

Restrict every `C_j` to sources in `T`.

1. If the internal response relation admits a system of distinct
   representatives, select one source for every target.  The resulting
   directed edges form a set of vertex-disjoint cycles on `T`.
2. Their incoming sets are pairwise disjoint: they are `H` and the cells of
   the partition of `R`.
3. Every incoming set is supplied within the selected edge set.  The donor
   target edge releases `H`, while the hub target edge releases all of `R`
   and hence every `R_k`.

Consequently the selected cycles form a BCFF Pareto-improvable edge set.  In
a PI-free state an internal system of distinct representatives is
impossible.  Hall's theorem then supplies a deficient target set.  A target
with no internal response source has only sources outside `T` and is an open
component-growth boundary; otherwise an inclusion-minimal Hall-deficient
set is the exact closed remainder.

If `Y` itself is EFX, (1) makes it a Pareto improvement.  If it is not EFX,
only changed targets can create new walls because every changed observer is
better off and every unchanged target is unchanged.  Strong-envy observers
of those walls must not be substituted for the most-envious response sources
in `C_j`.

## Why this is the missing primitive

The charity-rooted hub lemma is the special case in which `H` is supplied by
the charity slot.  It cannot represent the owner cycle repeatedly appearing
in the flower countermodels: an owner receives a packet from a donor while
splitting two or more of her own goods among that donor and another leaf.

For the three-owner motif, the transfer support is

\[
d\longrightarrow h,
\qquad h\longrightarrow d,
\qquad h\longrightarrow q.
\]

The donor/hub edges release each other's incoming packets, and the hub also
releases the packet sent to `q`.  This is exactly the release compatibility
that a collection of unrelated bilateral swaps lacks.

The finite support audit
[`owner_rooted_hub_split_release_audit.json`](owner_rooted_hub_split_release_audit.json)
checks all internal response permutations for two and three leaves.  The
argument itself is for arbitrary positive packets and any number of leaves.

## Claim boundary

The lemma classifies the response-Hall remainder after an improving
owner-rooted exchange star has been selected.  It does not prove that the
flower supplies packets satisfying (1), eliminate open/Hall-deficient
response sets, close `GG`, or prove four-agent additive EFX.  The live
selection problem is now precise: use the opposite-sign polarity and the
payment-critical residual top packet to select `h,d,H,R`, and its partition.

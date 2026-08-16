# Two-nonsingleton cycle-class composition

**Date:** 2026-08-09

**Status:** cap-free composition theorem for the exactly-two-nonsingleton
branch; independent referee audit remains required

## Theorem

Consider four positive, nondegenerate additive agents.  Let `X` be a
globally lexicographically maximal noncomplete partial EFX allocation in the
BCFF one-charity normal form, and suppose exactly two allocated bundles are
nonsingletons.

The following four proved cycle-class statements apply:

1. the length-two trapped-source return theorem;
2. the cap-free length-three global-lex escape theorem for every external
   singleton source and every fixed priority order;
3. the adjacent-large length-four global-lex escape theorem; and
4. the alternating length-four global-lex escape theorem.

Then `X` cannot exist.  Equivalently, a globally maximal noncomplete
four-agent EFX state cannot have exactly two nonsingleton bundles.

## Selected-cycle classification

Select one incoming basic `f`-champion edge for every allocated bundle.  If
the selected desired set discards `f`, it lies inside the target's old
bundle, so the source envies that target; replace the selected edge by the
parallel ordinary envy edge.  Call every remaining selected `f`-edge
**genuine**.

Every vertex has exactly one selected incoming edge.  Following predecessors
in this finite directed graph yields a simple directed cycle.  A cycle with
zero or one genuine edge is a basic PI cycle and contradicts global
maximality, so the selected simple cycle contains at least two genuine edges.

*Referee repair 2026-08-16.*  The selected graph has in-degree one at every
vertex, so it may in principle contain several vertex-disjoint cycles rather
than one.  That does not create an unhandled case: every cycle of the
selected graph must itself carry at least two genuine edges by the sentence
above, while the whole selected graph carries at most two genuine edges,
since a genuine edge is the selected incoming edge of one of the two
nonsingleton owners (next paragraph).  A second disjoint cycle would need two
further genuine edges and none exist.  Hence at a globally maximal state the
selected graph contains exactly one cycle, and it is the cycle classified
below.

No genuine edge enters a singleton bundle.  If the target is `{z}`, a
genuine desired set inside `{z,f}` must be `{f}` or `{z,f}`.  The first is
not envied because the charity set is unenvied.  The second is not
common-safe: deleting `f` leaves the envied singleton `{z}`.  Hence genuine
edges can target only the two nonsingleton owners.

The selected cycle therefore contains exactly two genuine edges, targeting
the two nonsingleton bundles.  Its length is two, three, or four:

| cycle length | positions of the two genuine targets | cycle class |
|---|---|---|
| 2 | both vertices | length two |
| 3 | consecutive | length three |
| 4 | consecutive | adjacent large targets |
| 4 | opposite | alternating large targets |

These possibilities are exhaustive up to relabeling.  Applying the
corresponding item 1--4 contradicts global maximality in every case, proving
the theorem.

## Packet nondegeneracy

*Referee repair 2026-08-16* (closes gap G1 of the referee report
`TWO_NONSINGLETON_COMPOSITION_REFEREE_REPORT_20260816.md`, currently on
`codex/efx-breakthrough-next-20260802`).  Items 1, 3 and 4 require the top
and bottom packets of the two nonsingleton bundles to be nonempty; only the
length-three branch discharged this, in
[`LENGTH_THREE_BCFF_COMPOSITION_AUDIT.md`](LENGTH_THREE_BCFF_COMPOSITION_AUDIT.md)
(row "Nonempty `T_r,B_r,T_q,B_q`").  The argument is topology-independent, so
it is proved here once for all four cycle classes.

Fix either genuine edge of the selected cycle.  It enters a nonsingleton
bundle `X_w` with owner `w`, and it retains `f`, so its selected desired set
has the form `D=T+f` with `T subseteq X_w`; the bottom packet released by the
edge is `B=X_w\T`.  The argument uses only that the edge is genuine, that `D`
is common-safe by selection, that valuations are strictly positive, and that
the base allocation `X` is globally lexicographically maximal.  It therefore
applies verbatim to both nonsingleton bundles in every one of the four
classes.

**(a) The bottom packet is nonempty.**  Suppose `B` is empty.  Then `T=X_w`
and the selected desired set is the whole bundle plus charity, `D=X_w+f`.
Being a selected desired set, `D` is common-safe: `v_i(D-g)<=b_i` for every
agent `i` and every `g in D`, where `b_i=v_i(X_i)`.  Strict positivity gives

\[
v_w(D)=b_w+v_w(f)>b_w,
\]

so the owner `w` strictly prefers `D` to her own bundle and is a
self-`f`-champion.  This is exactly the configuration excluded by BCFF
Observation 2.10 at a maximum: negating the self-edge `w -> w` would force
`v_w(X_w)>v_w(X_w+f)`, contradicting positivity.  Explicitly, let `Y` agree
with `X` except that `Y_w=X_w+f`.  The only new comparison any observer `i`
makes is against `Y_w`, and `v_i(Y_w-g)=v_i(D-g)<=b_i=v_i(Y_i)` is precisely
the common safety of `D`; the owner `w` strictly improves, so every
comparison she made at the base still holds.  Hence `Y` is a partial EFX
allocation with `Y_i=X_i` for all `i!=w` and `v_w(Y_w)>v_w(X_w)`.  Absorbing
`f` therefore improves that owner alone and leaves every other utility
untouched, which is a strict lexicographic improvement in **every** priority
order, contradicting the global lexicographic maximality of `X`.  (In the
one-charity normal form `Y` is in fact complete; that is not needed here,
since maximality is taken over all partial EFX allocations, of which the
complete ones are a special case.)  This is the "clean direct
absorption" of `ONE_LARGE_CHAMPION_CLOSURE_REDUCTION.md`, line 239, and the
same self-`f`-champion route the length-three audit takes through BCFF
Observation 2.10.  (That file is not yet on this branch; it currently lives
on `codex/efx-breakthrough-next-20260802`, one instance of the version
fragmentation recorded as gap G5.)

**(b) The top packet is nonempty.**  Suppose `T` is empty.  Then the selected
desired set is `D={f}`, so its source strictly prefers the lone charity good
to her own bundle.  Charity dominance in the BCFF one-charity normal form
says every owner strictly prefers her own bundle to `f`, i.e. the charity set
is unenvied — the same fact used above to exclude genuine edges into
singleton bundles.  So `T` empty is impossible.

Consequently `T_r,B_r,T_q,B_q` are all nonempty at any state surviving the
classification.  The nonempty-packet hypotheses of items 1, 3 and 4, and the
strict positivity they are stated with, are discharged here rather than
assumed; the per-lemma bookkeeping is in
[`LENGTH_THREE_BCFF_COMPOSITION_AUDIT.md`](LENGTH_THREE_BCFF_COMPOSITION_AUDIT.md),
[`ALTERNATING_BCFF_COMPOSITION_AUDIT.md`](ALTERNATING_BCFF_COMPOSITION_AUDIT.md),
and
[`ADJACENT_BCFF_COMPOSITION_AUDIT.md`](ADJACENT_BCFF_COMPOSITION_AUDIT.md).

## Why extra edges do not create a fifth class

The classification selects a cycle; it does not assume that the full envy
or champion graph is chordless.  A self-edge or an additional edge closing
a cycle with at most one genuine `f`-edge is already a PI certificate.  Any
other edge is simply extra information available to the applicable
all-source reservoir or compatible-family lemma.

Relabeling a selected cycle transports the original fixed priority order to
the role names.  It never changes the priority used to define global
maximality.  The alternating and adjacent theorems cover all 24 transported
orders, while the length-three target explicitly indexes its external source
and transported order.

## Dependency ledger

| class | authoritative artifact | current boundary |
|---|---|---|
| length two | [`TRAPPED_SOURCE_RETURN_LENGTH_TWO_CLOSURE_THEOREM.md`](TRAPPED_SOURCE_RETURN_LENGTH_TWO_CLOSURE_THEOREM.md) | analytic, conditional on the BCFF Theorem 3.16 external-bottom-edge interface; independent review still required |
| length three | [`LENGTH_THREE_RESERVOIR_ORDER_ESCAPE_THEOREM.md`](LENGTH_THREE_RESERVOIR_ORDER_ESCAPE_THEOREM.md) and [`LENGTH_THREE_BCFF_COMPOSITION_AUDIT.md`](LENGTH_THREE_BCFF_COMPOSITION_AUDIT.md) | all 24 priority orders and all three external singleton sources closed cap-free; exact packet audit replays all 24 indexed cases |
| adjacent length four | [`ADJACENT_LARGE_GLOBAL_LEX_TARGET_20260809.md`](ADJACENT_LARGE_GLOBAL_LEX_TARGET_20260809.md) and [`ADJACENT_BCFF_COMPOSITION_AUDIT.md`](ADJACENT_BCFF_COMPOSITION_AUDIT.md) | all 24 orders closed cap-free |
| alternating length four | [`ALTERNATING_GLOBAL_LEX_CAPFREE_THEOREM.md`](ALTERNATING_GLOBAL_LEX_CAPFREE_THEOREM.md) and [`ALTERNATING_BCFF_COMPOSITION_AUDIT.md`](ALTERNATING_BCFF_COMPOSITION_AUDIT.md) | all 24 orders closed cap-free |

*Referee repair 2026-08-16:* the two audit columns above were added with the
new premise tables (gap G4); every remaining BCFF premise is marked
EXTERNAL-TRUSTED inside them.

The length-two artifact was recovered from the original research worktree;
it had been cited by the roadmap but was absent from the repository history.
Capturing it here repairs that provenance gap.  Its use of BCFF Theorem 3.16
is the most important external interface to audit independently.

## Current consequence and boundary

This establishes the exactly-two-nonsingleton theorem within the positive,
nondegenerate BCFF one-charity normal form.  It is not a proof of complete
four-agent additive EFX.  That result still requires
contraction/augmentation theorems for states with three and four
nonsingleton bundles, followed by the nonnegative/tie wrapper.  The
length-two BCFF interface and the new length-three composition should be
checked by an independent human referee before either is used as a published
lemma.

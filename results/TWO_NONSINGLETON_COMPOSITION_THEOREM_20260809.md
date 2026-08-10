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

Every vertex has a selected incoming edge.  Following predecessors in this
finite directed graph yields a simple directed cycle.  A cycle with zero or
one genuine edge is a basic PI cycle and contradicts global maximality, so
the selected simple cycle contains at least two genuine edges.

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
| adjacent length four | [`ADJACENT_LARGE_GLOBAL_LEX_TARGET_20260809.md`](ADJACENT_LARGE_GLOBAL_LEX_TARGET_20260809.md) | all 24 orders closed cap-free |
| alternating length four | [`ALTERNATING_GLOBAL_LEX_CAPFREE_THEOREM.md`](ALTERNATING_GLOBAL_LEX_CAPFREE_THEOREM.md) | all 24 orders closed cap-free |

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

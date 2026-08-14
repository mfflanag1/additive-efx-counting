# Rank-three one-edge charity-substitution lemma

**Date:** 2026-08-13

**Status:** cap-free reduction of all four corrected response forms to one
omitted-source payment/observer inequality

**Boundary correction (2026-08-13):** the response-core substitution family
is not universally sufficient under the current necessary packet/rank
premises, even after arbitrary residual goods are appended along its three
fixed supplier edges. The exact boundary profile has no EFX candidate in
this family but has twenty EFX allocations on eleven other four-edge
topologies. See
[`ONE_EDGE_CHARITY_SUBSTITUTION_BOUNDARY_20260813.md`](ONE_EDGE_CHARITY_SUBSTITUTION_BOUNDARY_20260813.md).
Accordingly this document is a conditional normal form, not the remaining
universal selector.

The corrected exact support relation also contains the mandatory strong-wall
response `d -> r` in addition to the four responses enumerated below. Thus
the construction omits at least two of the five live responses, not exactly
one. Its conservation statements remain correct for the displayed four-edge
subrelation, but it is not an exhaustive normal form of the saturated gate.

## Why one response must be omitted

Each corrected root-facing rank-three form contains four nonself owner
responses: the three selected matching edges and the unmatched root-facing
edge.  Reversing all four would already consume four owner-transfer edges,
leaving no edge with which to empty the singleton charity `{p}`.

Choose one response source `h` to omit.  Reverse the other three response
cores, leave `h`'s unused core with its physical target, and give `p` to `h`.
This uses exactly

\[
 3\text{ owner edges}+1\text{ charity edge}=4.     \tag{1}
\]

Every good is conserved and final charity is empty.  Packet cardinalities
are unrestricted.

## Payment reduction

Every nonomitted source receives a base-desired core and is therefore
strictly above its GG base, irrespective of retained residuals.  Only `h`
can be unpaid.  Let

\[
 \Delta_h=v_h(Y_h)-v_h(X_h),\qquad
 L_h=v_h(\text{cores supplied from }Y_h).          \tag{2}
\]

Its exact final base margin is

\[
 m_h=\Delta_h-L_h+v_h(p).                         \tag{3}
\]

Thus owner payment has collapsed to `m_h>=0` for one chosen source.  Final
EFX additionally requires `m_i` to dominate every changed-target observer
debt, as in the signed-margin identity lemma.

## Shared-target overlap disappears in two choices

The permanent anchor source `r` and unmatched root-facing source `d` both
target `q`.  If `h` is either `r` or `d`, only one q-target core is moved.
Hence omitting either of those sources automatically eliminates the physical
double-core overlap.  Omission of `q` or `s` retains both q-target cores and
is admissible only after the disjoint-or-capture gate is resolved.

The universal theorem is therefore reduced to the following finite analytic
alternative:

> Either the `r`-omission or `d`-omission candidate satisfies its single
> payment and observer budgets, or both fail with exact signed deficits that
> must fund a disjoint q-core choice in a `q`/`s` omission—or activate a
> saturated support/response exit.

This is not a bounded atom or moved-good statement.  It is four scalar
omission choices over arbitrary physical packets.

## Verification and boundary

[`audit_rank_three_one_edge_charity_substitution.py`](../tracks/parkability/audit_rank_three_one_edge_charity_substitution.py)
independently constructs all sixteen `(response form, omitted source)` cases,
checks conservation, empty charity, exactly four support edges, desired-core
payment of every nonomitted owner, and elimination of shared-q overlap under
`r` or `d` omission.

The lemma does not prove that one omission satisfies (3) and all observer
budgets. The bounded boundary shows that this cannot be derived from the
currently encoded necessary packet/rank premises alone.

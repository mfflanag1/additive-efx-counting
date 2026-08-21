# Pattern-dependent mixed menus: exact refutation and a four-split threshold

**Date:** 2026-08-21

**Status:** the proposed pattern-dependent mixed-menu theorem is false for the
declared exact-response form-2 master; two coordinated split roles do not
suffice on an explicit physical realization; four are necessary and
sufficient for that realization. General additive EFX is not refuted.

## Exact result

There is an admissible positive-rational form-2 totals/minima profile with the
following two properties.

1. For every tame role `G` and every one of its eight witness-side cells,
   allow that cell to choose its own anchor role `H`, anchor observer, two
   distinct anchor-piece recipients, allocation of every other role whole,
   and arbitrary support topology with at most four edges. No choice of `G`
   closes all eight cells.
2. The same profile has a concrete two-good-per-multirole realization for
   which no complete four-edge EFX allocation splits zero, one, two, or three roles.
   A complete four-edge EFX allocation splitting exactly four roles exists.

Thus both proposed universal conclusions are false:

- one tame witness-side split plus one dynamically selected anchor does not
  suffice; and
- even arbitrary coordinated allocations with at most two physically split
  roles do not suffice; in fact, three do not suffice either.

The second statement strictly strengthens a failure of a particular selector:
its oracle ranges over every complete allocation of the displayed physical
goods, not a template menu.

## Exact mixed-cell inequalities

Fix a tame conditioning role `G`, a side pattern `sigma`, an anchor role `H`,
and anchor observer `a`. For observer `i`, let the two `G`-piece values be

```text
(M_i(G), T_i(G)-M_i(G))
```

in the order specified by `sigma(i)`. Let `x_i` denote the value of the
selected `H` good. The exhaustive endpoint set is:

```text
two-good H:        x_a=M_a(H)
                   x_i in {M_i(H), T_i(H)-M_i(H)} for i != a

three-or-more H:  x_a=M_a(H)
                   x_i in {M_i(H), T_i(H)-2M_i(H)} for i != a
```

The deletion floor of the selected piece is `x_i`. The complement floor is
`T_i(H)-x_i` in the two-good case and `M_i(H)` in the three-or-more case.
Every other whole role has value `T_i` and deletion floor `M_i`.

For every observer `i`, target bundle `B_t`, and piece `p` in `B_t`, the
solver imposes exactly the affine EFX inequality

```text
U_i(B_i) - U_i(B_t) + floor_i(p) >= 0.
```

All slacks are affine in the selected-good coordinates, so the displayed
endpoints are sufficient and necessary. Cardinalities above three only shrink
the feasible interval. Piece-owner variables enumerate every recipient pair
and whole-role assignment; supplier/recipient edge indicators enumerate every
support topology within the four-edge cap.

## Exhaustive coverage

The obstruction contains eight tame conditioning roles and eleven roles
eligible to be anchors. Pinning observer `r`'s side removes only the global
relabeling of the two tame goods, leaving eight patterns per tame role.

```text
tame roles                                      8
witness-side cells                         8 x 8 = 64
cells admitting some permitted repair            18
cells admitting no permitted repair               46
unknown cells                                      0
anchor lanes in each negative cell                40
```

Every one of the eight possible conditioning roles has at least one negative
cell. An independently written integer-owner encoding rechecks one such cell
per role, including its tame-only allocation universe and all `10 x 4 = 40`
anchor-role/observer lanes: 320 independent anchor-lane UNSAT decisions in
total. The profile itself replays SAT against the complete form-2 master.

These eight negative local patterns can be imposed simultaneously: witness
sides belonging to distinct roles are independent coordinates of the chart.
Their product is therefore one global witness-side cell in which *every*
possible choice of conditioning role has its audited negative pattern. Since
all roles other than the chosen tame and anchor roles remain whole, their side
identities do not enter that candidate's affine inequalities. This product-cell
argument refutes the fully dynamic interpretation in which the menu may choose
its conditioning role only after seeing the entire witness-side vector; it is
not merely eight unrelated failures of preselected menus.

A supplementary two-anchor endpoint search exhausts all 55 unordered pairs of
eligible roles and all 16 anchor-observer pairs per role pair. All 880 lanes
are UNSAT with no timeout. This is useful mechanism evidence, but the physical
split-count result below is stronger.

## Exact physical four-split threshold

The independently audited realization is the same global product cell used
above. Its tame-role side patterns, in owner order `(r,q,d,s)`, are:

```text
h:0000    j:0000    k:0000    q0:0000
l:0000    e:0000    m:0001    gq:0001
```

The three wild roles use the all-coincident two-good realization. Every row
has exactly the frozen total and minimum, so this is an admissible physical
realization of the form-2 profile.

An independent integer-owner solver then ranges over every complete
allocation, deriving support edges from owner equalities and enforcing every
good-deletion EFX inequality in exact rational arithmetic:

```text
split-role cap 0       UNSAT
split-role cap 1       UNSAT
split-role cap 2       UNSAT
split-role cap 3       UNSAT
split-role cap 4         SAT
```

The exact four-split certificate splits roles `{a0,j,k,m}` and uses edges

```text
charity -> d,  d -> r,  q -> s,  r -> q.
```

Its allocation and complete rational value matrix are frozen in the
independent-audit JSON and rechecked outside the solver. Therefore four is
the exact minimum number of split roles for this realization under the
four-support-edge constraint. This is split-count minimality, not coefficient
minimality of the totals/minima profile.

## Independent-verification boundary

The independent verifier shares only the declared form-2 premise builder and
the public role/owner labels with the primary search. It does not import the
primary Boolean mixed oracle or the two-anchor oracle. It uses integer owner
variables, derives edge flags directly from owner equalities, reconstructs the
physical realization independently, and checks the positive four-split
certificate again using `Fraction` arithmetic.

This establishes an independently encoded computational theorem about the
declared form-2 master and the displayed rational realization. It has not yet
received external human review or proof-assistant formalization.

## Reproduction

```bash
python -m tracks.parkability.audit_fixed_u_pattern_dependent_mixed_menu \
  --profile results/fixed_u_tame_or_anchor_cegar_20260821.json \
  --output results/fixed_u_pattern_dependent_mixed_menu_obstruction_20260821.json \
  --edge-cap 4 --timeout-seconds 30

python -m tracks.parkability.independently_verify_fixed_u_mixed_and_four_split \
  --profile results/fixed_u_tame_or_anchor_cegar_20260821.json \
  --primary-audit results/fixed_u_pattern_dependent_mixed_menu_obstruction_20260821.json \
  --output results/fixed_u_pattern_mixed_four_split_independent_audit_20260821.json \
  --timeout-seconds 30

pytest -q tracks/parkability/test_fixed_u_pattern_mixed_four_split.py
```

Frozen principal artifact hashes:

```text
0237ad9cb47244946341de96b99cc7a7f1b7e652088dcf49f3a5126094171365  results/fixed_u_pattern_dependent_mixed_menu_obstruction_20260821.json
359ed19d497bd2d47eec018c7d63d658a1e6e01b574307aedd6d1608196a9ba8  results/fixed_u_pattern_mixed_four_split_independent_audit_20260821.json
4df0002fa19eebea63324b26dec092b9532290a25ae761f8eb019f4605e1dd5c  results/fixed_u_two_anchor_obstruction_aggregate_20260821.json
```

## Exact remaining bridge

The surviving local mechanism must permit at least four coordinated physical
splits. The sharp next theorem is:

> Every admissible form-2 profile and every physical realization consistent
> with it has a complete EFX allocation using at most four support edges and
> at most four split roles.

A theorem over two-good realizations alone would still leave the cap-free
wild-role bridge: a wild role can contain three or more goods, with minimum
identities and packet values not captured by a binary side pattern. After the
form-2 four-split theorem, the remaining global steps are still (i) lifting
from form 2 to every saturated fixed-`U` separator and (ii) lifting the
fixed-`U` closure to general additive EFX.

No complete-EFX counterexample, universal fixed-`U` theorem, or resolution of
general additive EFX is claimed.

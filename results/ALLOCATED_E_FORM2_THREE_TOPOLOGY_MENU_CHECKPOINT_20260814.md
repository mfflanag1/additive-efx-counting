# Allocated-E form-2 three-topology menu checkpoint

**Date:** 2026-08-14

**Status:** exact bounded search checkpoint at an iteration limit; neither a
bounded theorem nor a countermodel

## Decision problem

The exact twelve-atom allocated-E form-2 master negates every complete EFX
allocation supported by the following three physical packet graphs:

1. `charity->r`, `r->d`, `r->s`;
2. `charity->r`, `q->d`, `r->d`, `r->q`;
3. `charity->q`, `d->q`, `q->d`, `r->s`.

Their exact stay/send allocation counts are `12`, `84`, and `343`; the union
contains `439` distinct complete allocations.  Packet contents are arbitrary
subsets of the twelve declared atoms.

## Exact outcome

The initial run generated `19,747` distinct closed generalized-PI cuts before
an honest solver timeout.  A resumed run completed ten more SAT rounds and
ended at its declared iteration limit with `25,413` cumulative cuts.  Every
candidate valuation encountered in both runs contained at least one exact
closed generalized-PI family.  No generalized-PI-free counterprofile was
found, but the final master was not proved UNSAT.

Across all `25,413` unique witnesses, `2,125` use three owners and `23,288`
use all four owners.  The strong four-owner concentration is discovery
evidence for an alternating uncrossing/full-owner lemma; it is not itself a
mathematical implication.

## Independent structural audit

`audit_allocated_e_form2_three_topology_menu.py` does not import the primary
driver.  It independently reconstructs the `439` allocations and validates:

- exact topology and allocation counts;
- resume-source hash continuity;
- global uniqueness of all `25,413` cut signatures;
- nonempty, pairwise-disjoint desired cores;
- exact base incoming/released identities; and
- release coverage for every allocated incoming good.

The audit status is `STRUCTURE_VALID`.  It intentionally does not replay the
QF_LRA master.

## Frozen artifacts and hashes

- Initial raw trace SHA-256:
  `8cf4b172f247a88c1576ca63f1e0400c0179d0c68332f72dc73e2885cfda7956`
- Initial compressed trace SHA-256:
  `9e021644d56a71012d5cd21293b1a6972ba1d4943de6219ffdb39210b484f14f`
- Resume raw trace SHA-256:
  `814a92cbe5c8c2154b03d8f9fd317c61069c12c466ea2c1f8be3496c15591a82`
- Resume compressed trace SHA-256:
  `b6dcc9321cb592c91ba0488895545bd4895eb13a2e7f433259db502bdebb007a`
- Structural audit SHA-256:
  `9b921a7aa14db5d1599bcf9a2b1001e9523de67d321cfd3c2e21970b8e7e7f2e`
- Primary driver SHA-256:
  `284e313fdab7fc14348d25f5dc7fed891248dafed4f565039465d6044cb3ee4e`
- Independent audit SHA-256:
  `8f0474ca187117cdc693886a8a36c4e6214e140f94c29d774beaafb406a97044`

The repository stores the two large traces in gzip form.  After expanding
them to their displayed raw filenames, the shortest structural replay is:

```bash
python -m tracks.parkability.audit_allocated_e_form2_three_topology_menu \
  --source results/allocated_e_form2_three_topology_menu_cegar.json \
  --source results/allocated_e_form2_three_topology_menu_cegar_resume19747.json \
  --output /tmp/form2-menu-structural-audit.json
```

## Route correction

The three-topology menu is empirical, not a cap-free normal form.  In
particular it omits the six canonical response branches, including the
natural path `charity->r->s->q->d`.  The next exact decision therefore
enlarges the menu rather than treating convergence of this search as evidence
that these three topologies are exhaustive.

## Claim boundary

Proved: exact enumeration of the bounded menu and solver-independent
combinatorial validity of every recorded PI witness.

Not proved: UNSAT of the bounded master, existence of a PI-free
counterprofile, exhaustion by the three topologies, the cap-free fixed-`U`
theorem, or general EFX.

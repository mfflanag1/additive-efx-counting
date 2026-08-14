# R2 role-split 20,000-cut checkpoint

**Date:** 2026-08-14

**Status:** fail-closed exact-search checkpoint; no SAT or UNSAT conclusion

## Decision cell

The role-split driver strengthens the original twelve-supergood R2 cell by
splitting each of the nine provenance regions in `A+H`, `Q`, and `W` at
membership in fixed witnesses for

\[
                         r\to q,\quad q\to r,\quad s\to d.
\]

Each inside/outside role may be absent, but every original provenance region
is nonempty and every represented good has strictly positive value in every
row.  Together with the unaffected regions `l,e,p`, the model has at most
twenty-one active goods and quantifies over all witness-membership patterns
in that cell.

The master includes the minimized R2 numerical premises: positive additive
values, normalized base bundles, base EFX, retained base-common-safe desired
cores `A,Q,E`, the base response of `d` to `Q`, the three fixed physical
response witnesses, and the root-facing/nonroot wall inequalities.  It does
not impose the full exact response nonedge relation, rank formula, or any
upper value bound.

## Exact separation

For each rational valuation model, an independent binary-QF_LRA oracle
searches all nonempty owner subsets for a closed pairwise-disjoint family of
physical common-safe desired cores.  It uses one Boolean selection variable
per source/good and does not enumerate all `2^21` bundles.  Every returned
family gives a globally valid generalized-PI exclusion cut.

The chained run installed exactly 20,000 distinct structurally valid family
cuts.  The final master was still satisfiable after 19,750 cuts; the next
model supplied 250 more valid families.  The following master check was
interrupted at a deliberate checkpoint and recorded `UNKNOWN`, rather than
being promoted to either SAT or UNSAT.

The final active model before interruption used seventeen of the twenty-one
possible roles.  This is evidence that the contradiction, if one exists, is
not confined to the original twelve aggregated atoms.

## Artifacts

The exact resume chain is:

1. `allocated_e_form0_role_split_pi_cegar.json` — 1,000 cuts;
2. `allocated_e_form0_role_split_pi_cegar_resume1000.json` — continuation;
3. `allocated_e_form0_role_split_pi_cegar_batch_resume1096.json` — batched continuation;
4. `allocated_e_form0_role_split_pi_cegar_batch_resume6346.json` — recursive-chain repair;
5. `allocated_e_form0_role_split_pi_cegar_resume15250.json` — 20,000-cut checkpoint.

`audit_allocated_e_form0_role_split_checkpoint.py` validates every resume
hash, deduplicates the full chain, and independently checks nonemptiness,
source distinctness, pairwise disjointness, and base-owner closure of every
installed family.

Resume from the repository root with:

```bash
/private/tmp/efx-charity-py/bin/python -m \
  tracks.parkability.run_allocated_e_form0_role_split_pi_cegar \
  --output results/allocated_e_form0_role_split_pi_cegar_resume20000.json \
  --resume results/allocated_e_form0_role_split_pi_cegar_resume15250.json \
  --timeout-seconds 900 --maximum-iterations 100 \
  --maximum-families-per-round 250 --random-seed 6151
```

## Claim boundary

This checkpoint proves only that 20,000 specific generalized-PI family
regions are excluded from the declared twenty-one-role cell.  It does not
prove that the cell is UNSAT, exhibit a PI-free SAT endpoint, cover the
optional twenty-second critical-minimum role, convert hidden minima to a
four-edge transfer, or prove the active fixed-`U` theorem.

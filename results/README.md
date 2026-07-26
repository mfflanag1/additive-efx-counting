# Results directory

This directory contains both current evidence and historical campaign output.
Do not infer claim status from a filename alone.

Current paper evidence is exactly the subset referenced by:

- `repro/counting_witnesses/instances.json`
- `repro/countcegar_k4/MANIFEST.json`
- `artifacts/generalized_parking/certificates.json`
- `supplement/build_release.py`

The exact-real checkpoint inventory is separately pinned by
`repro/countcegar_real/MANIFEST.json`. It is reproducible research state, not a
paper theorem.

All other files should be treated as exploratory or historical unless a
current package README explicitly promotes them. In particular,
`CAMPAIGN_LOG.md`, `REPORT.md`, and `REVIEW.html` preserve superseded states and
corrections.

See `../ACCOMPLISHMENTS.md` for current claims and
`../docs/CAMPAIGN_ARCHIVE.md` for the archive map.

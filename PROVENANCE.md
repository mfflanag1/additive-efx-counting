# Provenance

## Source snapshot

This standalone repository was assembled on 2026-07-26 from:

```text
/Users/maxf/projects/counterexample-hunt/efx
```

The source directory belonged to the larger `counterexample-hunt` repository,
whose base commit was:

```text
a9c88411593cefe464a0731cd15bc1d03ae97d31
```

The imported EFX snapshot intentionally includes the audited modified and
untracked files in that working tree. A subtree export of the parent commit
would have omitted much of the current paper, proof package, and audit
hardening. This repository therefore begins with a fresh history; references
to `a9c8841...` in manifests identify the source campaign baseline, not a
commit that contains every imported artifact.

The contents of the old `efx/` directory became this repository root. Relative
paths used by verifiers and manifests were preserved.

## Evidence preservation

Claim-bearing data, programs, formulas, and certificates were copied
byte-for-byte. Three active READMEs received repository-root wording, and the
corresponding K4 package hash was updated. The paper PDF was rebuilt from the
unchanged imported LaTeX source with TeX Live 2026. Caches, Python bytecode,
the empty `transcripts/` directory, macOS metadata, and LaTeX intermediate
files were excluded. Zero-byte files elsewhere in the campaign archive were
retained as historical placeholders.

Two exact-real SMT-LIB files are between GitHub's 50 MiB warning threshold and
100 MiB hard limit:

```text
results/countcegar_real_4x7_long_cardinality.smt2
results/countcegar_real_4x7_final_cardinality.smt2
```

They remain ordinary Git files so a clone contains the complete manifest-bound
checkpoint without an additional release or LFS retrieval step. They are not
part of the 57-file paper supplement.

## Historical machine metadata

Several frozen records contain local paths or a development-machine hostname:

- `repro/countcegar_k4/certificates/cadical-1.9.5.solve.log`
- `results/countcegar_K4_reconstructed.json`
- `results/countcegar_slot_boundary.json`
- `repro/countcegar_real/MANIFEST.json`
- `results/REVIEW.html`

Those strings are provenance, not runtime dependencies or credentials. They
were retained because sanitizing evidence-bearing records would require
rewriting their dependent hashes and would blur the distinction between the
original run and the standalone import. Current commands are repository
relative.

The publication audit found no access tokens, passwords, private keys,
credential files, or embedded secrets.

## Canonical and historical documents

Use these files for current status:

- `README.md`
- `ACCOMPLISHMENTS.md`
- `REPRODUCIBILITY.md`
- `AUDIT_HISTORY.md`
- the READMEs inside `repro/`, `artifacts/`, and `supplement/`
- `paper/main.tex`

`LEDGER.md`, `PLAN.md`, `results/CAMPAIGN_LOG.md`,
`results/REPORT.md`, `results/REVIEW.html`, root discovery programs, and
unmanifested result files are preserved campaign history. They may describe
withdrawn conjectures, superseded runs, or then-current engine status.

## Publication metadata

No license has been selected, so no permission to redistribute or reuse is
granted by this repository. No `CITATION.cff` is included because the paper's
author, affiliation, and citation details are still unresolved in
`paper/main.tex`. Resolve those items before making the repository public.

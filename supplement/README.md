# Main-paper supplementary release

This workflow packages only the claims in `paper/main.tex`: the six exact
count-\(n\) witnesses, the generalized-parking certificates, and the bounded
\((4,7)\), \(K=4\) counting result. Exploratory exact-real, chamber, and
multi-floater work is intentionally outside this submission profile.

The explicit main-paper profile includes the paper source and PDF, every file
in the three claim-bearing artifact directories, and every root or `results/`
file referenced by their manifests. `build_release.py` requires the directory
inventories and nested references to equal that profile, then checks the
nested hashes before packaging. It writes a deterministic `.tar.xz` archive
and an identical sidecar copy of the manifest embedded in the archive.

## Release build

Build from the repository root after the paper PDF and nested manifests are
final. Both outputs must be outside the source tree:

```sh
python3 supplement/build_release.py build \
  --archive /absolute/output/efx-paper-supplement.tar.xz \
  --manifest /absolute/output/efx-paper-supplement.manifest.json
```

The default build refuses modified, deleted, untracked, or profile-unexpected
selected files, requires every payload path to be tracked, and compares every
working-tree blob directly with the Git index (including `skip-worktree`
paths). It then reads each payload exactly once, binds that byte snapshot to
the initially captured stage-zero Git blob, and uses the same snapshot for the
manifest and archive. It rediscovers the full profile after writing and
verifying the archive. This makes a clean commit or tag part of the release procedure.
`--allow-dirty` exists only for testing the workflow; the resulting manifest
records the selected Git status and should not be submitted.

Running the same command from the same clean commit produces the same manifest
and archive bytes. Archive members have sorted names, fixed ownership and mode,
and timestamp zero. Output paths are explicit and are not stored in the
manifest. The build prints the archive size and SHA-256 digest; retain that
digest with the two release files.

## Recipient verification

Verify the archive without extracting it:

```sh
python3 supplement/build_release.py verify \
  --archive /absolute/output/efx-paper-supplement.tar.xz \
  --manifest /absolute/output/efx-paper-supplement.manifest.json
```

The verifier independently requires the manifest inventory to equal the
explicit main-paper profile; a mutually consistent empty or partial
manifest/archive pair is rejected. It also rejects POSIX- or Windows-unsafe,
out-of-order, duplicate, missing, extra, non-regular, or non-canonical members,
including nonempty owner, link, device, or PAX metadata, and checks every
payload size and SHA-256 digest. The sidecar manifest must be byte-identical
to `RELEASE_MANIFEST.json` inside the archive.

Run the adversarial release-gate regressions from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 supplement/test_build_release.py
```

## Pinned external tools

The release contains the exact CNF, compressed proof, Python sources, and
Python dependency pins. It does not bundle third-party solver or checker source.
Their repositories and exact revisions are recorded both in the release
manifest and in
`repro/countcegar_k4/certificates/DRAT_CERTIFICATE.json`:

- CaDiCaL 1.9.5, tag `rel-1.9.5`, commit
  `146207318796f094dcded87349a64f0c6927309e`,
  `https://github.com/arminbiere/cadical.git`;
- `drat-trim`, commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`,
  `https://github.com/marijnheule/drat-trim.git`.

After building that `drat-trim` revision, check the archived DRAT proof from an
extracted release with:

```sh
python3 repro/countcegar_k4/verify_drat.py \
  --checker /absolute/path/to/drat-trim
```

The certificate check therefore has a narrow, explicit external-tool trust
boundary; the evidence package itself is fully hashed and frozen.

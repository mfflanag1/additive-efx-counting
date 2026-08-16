# EFX(4,8) release-hardening checkpoint

Date: 2026-08-01  
Status: same-host macOS and clean Linux/ARM v2 replays verified; external
human review and physically independent-host reproduction still required

## Headline

The coherent v2 package verifies the hybrid theorem:

> Every nonnegative additive instance with four agents and eight goods admits
> a complete EFX allocation.

The final Lean theorem is
`EFX48.admitsEFX_4x8_of_standard_published_inputs_nonnegative`. Pinned Lean
4.32.1 builds it with the axiom boundary
`[propext, Classical.choice, Quot.sound]` and no `sorryAx`, `native_decide`, or
`ofReduceBool` dependency.

## Coherent v2 snapshot

Certification root:

```text
game-theory/experimental-runs/additive-efx-counting-runs/
parkability/certification-20260801-v2
```

Load-bearing identities:

- end-to-end certificate SHA-256:
  `4ba602e217d964e80b6d477d2bc187400717a0ea9f083bbbdab87f8169fd6158`;
- end-to-end manifest SHA-256:
  `9d0634131027eec7b892dd5cb87f96fbba0e79efa621368aa112ff99b9726d78`;
- deterministic source archive SHA-256:
  `2e5a6743f5d9970472fa8a72cabaca5156f925f51bc6f97e94884a6eeaeedc63`;
- 124 end-to-end manifest entries;
- 96 terminal-certificate manifest entries; and
- 72 files in the deterministic source archive.

The complete 124-entry manifest passed `shasum -a 256 -c` on 2026-08-01.

The v2 source archive contains the submission manuscript as it stood when the
snapshot was finalized (archived `submission.tex` SHA-256
`27648e57698a3b6b9afe12865148865fb26260ffb49112a054719a79b39b38a1`).
The working manuscript was subsequently updated to report the completed
all-eight relocatability replay (working `submission.tex` SHA-256
`aea96a620034e9e26436d055c896a1424a896ea3de01c34f2c751bf40c4be1b3`).
Thus the theorem package remains coherent, but the current manuscript and PDF
are **post-v2 working artifacts**, not members of the v2 manifest.  A release
submission must cut and verify a new coherent snapshot rather than mixing the
working manuscript with the v2 manifest.

## New hardening evidence

1. The permanent formula-to-CPC auditor expands all eight proof term DAGs and
   matches 545,360 formula assertions to 545,360 permanent CPC assumptions in
   order, with zero mismatches.
2. The official cvc5 1.3.3 source archive has SHA-256
   `7eeeb65a6c5bfe985a6b3fc7938b87709bbc0e3f72d661b1d0587d4173ad9b33`.
   All 51 transitive `.eo` signature files match it; their tree hash is
   `d782730973035ced5410a0b7160a2b7f29a28978a915aa318aeccb615bbc1fd2`.
3. The terminal finalizer manifest-binds the assumption audit, official source
   archive, and all 51 signature files.
4. A true moved-root smoke test on `top4-second211` rewrote only the first two
   include lines, preserved all 18,119,382 remaining proof-body bytes, and
   received `correct` from pinned Ethos. The record is
   `results/efx48_relocatable_cpc_smoke_20260801.json`.
5. The v2 finalizer regenerated the semantic and published-input audits before
   binding them. It thereby caught and resolved stale hashes caused solely by
   the newly added nonnegative Lean wrappers and by absolute formula-root paths
   in the semantic JSON.
6. A clean Ubuntu 24.04 Linux/ARM container replay started from the deterministic
   source archive and a read-only v2 certificate mount. It installed Lean
   4.32.1 through `elan`, completed all 1,574 `lake build` jobs, reproduced the
   theorem axiom boundary, and passed both independent Python audits. The
   semantic audit SHA-256 is
   `283dced3f0e00beb8cf22aada9644222bf0a70db9605ea6d7275e07a622d8e04`;
   the published-input audit SHA-256 is
   `5bf022e2e937b3e9b8b5fa1c5e34e9ebf6676de1e6566381cc7aa0dbb19c11b0`.
   The exact environment and outcomes are pinned in
   `results/EFX48_LINUX_REPLAY_20260801.json`.
7. The full temporary-root replay has now checked all eight CPC proofs.  For each proof,
   the verifier rewrote only the two leading signature include lines, preserved every
   remaining proof-body byte, and pinned Ethos returned `correct`.  The complete run took
   8,333.440 seconds; its semantic summary SHA-256 is
   `9e5b4398943599966b535a32e32747c06298d9cd917b7bfd368e7d9fb4a69373`.
   Compact durable record: `results/EFX48_RELOCATABLE_CPC_REPLAY_20260801.json`.

## Exact claim boundary

- The eight archived CPC proofs themselves still contain their original two
  absolute signature include lines. Relocatability is implemented by a
  byte-preserving temporary transformation in the verifier; it is not a claim
  about those archived lines.
- All eight proofs pass the byte-preserving moved-root transformation.  This establishes
  verifier-level relocatability; it does not rewrite the archived proof files themselves.
- The clean Linux/ARM replay ran in Docker on the same physical Mac. It is a
  cross-OS/toolchain reproducibility check, not an independent-host or
  independent-person replication. It rebuilt the Lean and semantic layers;
  the separate full eight-cell temporary-root Ethos replay has also passed on that same
  physical host.
- The two published smaller-case proofs, the Lean kernel/toolchain, Ethos, and
  the hand-audited Python-specification-to-Lean semantic correspondence remain
  in the stated trust boundary.
- Internal adversarial review is not external peer review.
- The current working manuscript postdates the coherent v2 source archive.
  Re-finalizing a v3 snapshot is a release gate for any manuscript that cites
  the completed all-eight relocatability replay.

## Minimal verification

```sh
shasum -a 256 -c EFX48_END_TO_END_MANIFEST.sha256
```

From the source repository, the strengthened release gate is:

```sh
make verify-efx48-release \
  EFX48_CERT_ROOT=/absolute/path/to/certification-20260801-v2 \
  VERIFY_TMP=/private/tmp/efx48-release-v2
```

That target reruns the formula-assumption audit and all eight temporary-root
Ethos checks.  The full eight-cell component passed on 2026-08-01.

# Independent code review and checked dispositions

Review: Fable 5.1 snapshot-only, high effort, completed 16 October 2026.
Run: `20261016-131132-0e55a364` in the local `claude-reviews` store for this
worktree. Reviewed the two verifiers, both test files, and the reproduction README.
The reviewer had no execution tools; execution claims below are the
coordinator's checks, not the reviewer's.

Full local review:
`~/.local/state/claude-reviews/efx-audit-20260927-9080c6f5d94b/20261016-131132-0e55a364/review.md`.
Review SHA-256: `3ecbe9f4155256aaedd358deccbb9afe259d1232b9278fdc256146c8bf9c1394`.

Verdict: no false-acceptance finding in the reviewed exact arithmetic. Two
low-severity notes were independently investigated rather than adopted blindly.

## 1. Claimed missing Pareto test — rejected

The code reviewer incorrectly stated that BCFF Theorem 5.1 guarantees Pareto
improvement. It guarantees domination under Definition 2.3, namely improvement
in the fixed lexicographic order. The primary paper explicitly distinguishes
this from Pareto domination. The coordinator and both source reviews had already
checked that distinction. Adding a Pareto requirement would incorrectly narrow
the repair contract; no such restriction was added.

A new exact regression accepts a valid two-step EFX trace in which one owner
strictly improves while a later-priority owner temporarily loses utility. This
tests the intended lex-only contract. The existing README separately discloses
that the checker verifies a supplied successor, not its construction by a
particular case in the BCFF algorithm.

## 2. Exponential checks without a size guard — accepted and fixed

The trace verifier enumerates subset sums to check bundle nondegeneracy. A huge
input could therefore consume excessive resources. Added a default sixteen-good
guard to both the full-trace and isolated-pool APIs, with an explicit positive
integer override and CLI `--max-goods`. The guard precedes exponential routines.
Tests patch those routines to prove that oversized input never reaches them.
Invalid bounds and ordinary overrides are also tested.

This narrow post-review patch was inspected and tested by the coordinator; the
full snapshot was not resubmitted. The mathematical predicates and theorem
boundary are unchanged. The final suite has **48 passing tests**, and all three
physical trace certificates still pass. Finite machine checks do not re-prove
the published BCFF theorem or the historical transition lemmas.

The reviewed snapshot was before the guard and its new regressions. Exact
pre-change code hashes are retained in the local review's `request.json`; the
Git checkpoint identifies the final, locally tested version. No claim of a
hash-identical post-change cross-model review is made.

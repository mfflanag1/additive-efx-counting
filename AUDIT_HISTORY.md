# Audit history

This file records the material corrections and verification boundaries behind
the current paper. It is a status summary, not a replacement for the detailed
campaign log.

## Corrections that changed the project

### Rotation claim re-audited

An attempted correction asserted that the relevant rotation operation did not
preserve the property under study. A computational re-audit of 34,538
rotations found zero breaks: the attempted correction, not the original lemma,
was wrong. The current paper does not rely on that campaign-level rotation
argument.

### Flat-shape conjecture refuted

The internal implication “flat implies 2222” was false. The identical-lumpy
test case has 2,520 allocations of the tested class, all with shape 3221. The
conjecture was withdrawn and is not used in the paper.

### Invalid duplicated-type symmetry removed

One \((5,9)\) completion run imposed a lexicographic order that forced a
duplicated valuation type to be lexicographically greatest. Agent relabeling
does not justify that constraint because type multiplicities are fixed. That
UNSAT result covered only a subclass. The run was repaired with equality on
the duplicated rows and ordering only among singleton rows; the current
narrow paper nevertheless excludes the \((5,9)\) composite result.

### Historical K4 endpoint separated from the replacement endpoint

The historical K4 log reported a terminal 1,295-allocation pool, but the last
retained checkpoint had 1,250 entries and only 1,134 distinct allocations.
The missing cuts cannot be reconstructed from the archive. A new
atomic-checkpoint run produced a different complete 1,240-allocation terminal
pool. Current documentation calls it an alternative terminal master, never a
reconstruction of the missing historical pool.

### Exact-real outputs downgraded to checkpoints

The exact-real result schema now distinguishes the pool actually checked from
the pool after refinement. Both retained terminal masters were SAT before new
cuts were added; their exported post-cut formulas were not checked. The
closure validator replays seven branches and 80 refinements, but the result
remains `CHECKPOINT`, not `UNSAT`.

### Release snapshot race closed

The supplement builder originally re-read selected files at different stages.
A selected file could, in principle, change and revert between the Git check
and archive verification. The builder now reads each payload once, verifies
that immutable byte snapshot against the initial stage-zero Git blob, and uses
the same snapshot for the manifest and archive. Adversarial tests cover that
race along with inventory, path, type, ordering, ownership, link, device, and
PAX metadata.

## Claims that survived the audits

- all six exact count-\(n\) witness matrices and counts;
- agreement among the two pure-Python counters and the vectorized counter;
- the generalized single-floater parking theorem and seven certificates;
- the protected-slot soundness argument for the bounded counting master;
- the alternative 1,240-allocation K4 terminal pool;
- CP-SAT infeasibility and independent CNF UNSAT for that finite master;
- the archived CNF and independently checked DRAT proof; and
- the precise framing of \((4,8)\) as the first additive cell not covered by
  the cited general existence theorems.

## Remaining trust boundaries and open items

- The unrestricted additive lower-bound conjecture remains open.
- The bounded theorem has no magnitude-reduction step beyond
  \(\{1,\ldots,4\}\).
- The CNF translation is tested and audited but not formalized in a proof
  assistant.
- Logical DRAT verification depends on the pinned `drat-trim` checker.
- Exact-real, chamber, and multi-floater work is outside the current paper.
- `paper/main.tex` still needs author name, affiliation, and email before
  external submission.

For the current claim inventory, use
[ACCOMPLISHMENTS.md](ACCOMPLISHMENTS.md). For older records, see
[docs/CAMPAIGN_ARCHIVE.md](docs/CAMPAIGN_ARCHIVE.md).

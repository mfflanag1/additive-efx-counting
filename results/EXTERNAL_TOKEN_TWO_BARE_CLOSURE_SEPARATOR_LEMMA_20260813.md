# External-token two-bare closure inference — withdrawn

**Date:** 2026-08-13

**Status:** invalid inference caught before use; provenance census retained as
diagnostic only

## Proposed inference

The attempted argument began with the valid base-support closure reassembly.
Every closure owner recovers her whole base bundle and retains any support
from base charity or outside the closure. If the current charity token is
external, a closure with at most one owner receiving no such external packet
can be made strictly above base for every owner.

It then claimed that an all-owner-strict complete allocation automatically
supplies four common-safe desired self-responses and hence a generalized PI
edge set. That step is false as stated.

## Exact failure

For strict owner `j`, inclusion-minimality among subsets desired by `j` proves
only

\[
 v_j(D_j-g)\le v_j(X_j)\qquad(g\in D_j).          \tag{1}
\]

It does **not** prove

\[
 v_h(D_j-g)\le v_h(X_h)
 \qquad(h\ne j),                                  \tag{2}
\]

which is required for a base-common-safe desired core. Minimizing over
subsets desired by any owner restores common safety, but its response source
need not be `j`. The resulting response graph contains a directed cycle, yet
the incoming/outgoing packet labels of that subcycle need not be internally
release-compatible. Distinct target bundles alone do not repair this.

Therefore all-owner strictness does not, from the presently stated premises,
imply generalized PI. The claimed two-bare separator and the claimed
analytic exclusion of the repaired `K=Q` atomization are withdrawn.

## What survives

The underlying provenance census is exact:

- the repaired full-capture seed-`d` closure is `{d,q,r}`;
- `r` receives no base-charity/outside-closure support;
- `q` retains base-charity good `j`;
- `d` retains base-charity good `gr`; and
- current charity `p` is base-owned by outside owner `s`.

These facts show why the tempting strictness argument arose, but they imply
no PI-free exclusion. The exploratory two-bare CEGAR is a provenance variant,
not a faithful saturation model unless generalized PI and the full response
labels are encoded independently.

## Verification boundary

[`audit_external_token_two_bare_closure_separator.py`](../tracks/parkability/audit_external_token_two_bare_closure_separator.py)
checks only the signed conservation and provenance facts. Its status is
`WITHDRAWN_PI_INFERENCE`; it deliberately does not certify the former
separator.

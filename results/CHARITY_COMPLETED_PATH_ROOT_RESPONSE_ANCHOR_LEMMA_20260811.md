# Charity-completed path root-response anchor lemma

**Date:** 2026-08-11

**Status:** cap-free root anchoring of the complete transfer-path response
boundary; the root-monopoly target pair remains open

## Permanent root edge inside the donor target

Use the complete transfer-path candidate

\[
 Y_q=(X_q\setminus K)+f,
 \qquad Y_r=(X_r\setminus G)+K,
\]

where `K subseteq B_q` and `X_q=T_q+B_q`.  Then

\[
 D_r=T_q+f\subseteq Y_q.                            \tag{1}
\]

The original flower edge makes `D_r` common-safe and strictly desired by
the earlier root `r`.  Hence every response relation for the complete path
contains the anchored edge

\[
 r\longrightarrow q:D_r.                           \tag{2}
\]

Regarded as a replacement for base slot `q`, this edge has incoming packet
`{f}` and prescribed release

\[
 X_q\setminus D_r=B_q.                              \tag{3}
\]

In particular it releases the entire joint packet `K` needed by the changed
root target.

## Root-target source trichotomy

Suppose the changed root target has a common-safe desired response core

\[
 A\subseteq (X_r\setminus G)+K
\]

with source `i`.  Relative to base slot `r`, its incoming packet is contained
in `K`, while every discarded root good only enlarges its release.  Combine
this response with (2).

### 1. Source `i=q`

Targets `(q,r)` have distinct sources `(r,q)`.  The edge into `q` consumes
`f` and releases all of `B_q`, while the edge into `r` consumes only a subset
of `K subseteq B_q`.  The incoming packets are disjoint and internally
supplied.  Thus the two responses form a release-compatible PI 2-cycle.

### 2. External source `i in {c,s}`

The two targets have the matching `(r,i)` on distinct sources.  The
root-anchored represented owner set strictly grows to include an external
owner.  If the other changed target has a distinct internal source, the
matching grows again; otherwise maximum-matching owner-union compression
names its exact residual owners.

### 3. Source `i=r`

Both targets may share the root as their only available source.  If any
nonroot source also responds to the root target, cases 1--2 apply.  The sole
survivor is therefore the explicit two-target root-monopoly defect

\[
 \{Y_q,Y_r\}\longleftarrow\{r\}.                   \tag{4}
\]

It is not an unstructured sacrificed-owner Hall relation: both targets and
their unique common source are named, and the edge into `q` releases the
whole payment reservoir `B_q`.

## Sink-target augmentation

When `G` is nonempty, the external sink target `X_a+G` is strictly desired
by its intended owner `a`.  Global minimal desired-subset extraction gives
a common-safe response source.  A source outside the current root-target
matching grows the represented owner set; an internal source either supplies
an SDR or produces a minimal defect containing the anchored edge (2).

Thus every complete-path response relation has one of four outcomes:

1. an EFX lexicographic endpoint;
2. the immediate root/`q` PI 2-cycle;
3. root-anchored external owner growth followed by maximum-matching
   compression; or
4. the exact root-monopoly pair (4), possibly extended by a sink-target
   minimal Hall defect.

The earlier root can never disappear silently from the response boundary.

## Verification and claim boundary

[`charity_completed_path_root_response_anchor_audit.json`](charity_completed_path_root_response_anchor_audit.json)
checks the support containment, full `B_q` release, internal supply of every
possible `K`-incoming root response, and exhaustive four-source split.  The
scalar desired/common-safe premises are inherited from the original flower
anchor audit.

This lemma root-anchors the sacrificed-owner response boundary and closes
its `q`-source branch by PI.  It does not eliminate the root-monopoly pair,
prove every external/sink matching has an SDR, terminate the compressed
residual branch, close `GG`, or prove four-agent/general additive EFX.

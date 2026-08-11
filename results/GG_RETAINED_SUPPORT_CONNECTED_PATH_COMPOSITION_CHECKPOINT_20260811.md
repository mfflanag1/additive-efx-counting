# GG retained-support connected-path composition checkpoint

**Date:** 2026-08-11

**Status:** cap-free composition through every root-sourced/unsafe evolved-
target branch; two root-anchored Hall terminals remain, so `GG` is not closed

## Starting state

Use the positive, nondegenerate, globally lex-maximal `GG` flower after the
removed-top potential has retained `U subseteq T_r`.  When the reduced
mutual core ceases to pay `q`, the anchored residual rotation extends `U`
only as needed and forms

\[
 D_r=T_q+f,
 \qquad W=B_q+L,
 \qquad R=(T_r\setminus L)+B_r,
\]

with both mutual owners strictly improving.  Every failure is a wall against
the sole evolved target `W`.

## Cap-free composition chain

The following alternatives are exhaustive.

### 1. Minimal evolved-target source

Globally minimize a desired subset of `W`.  The resulting core is
common-safe.

- Source `q` closes with the root edge as a release-compatible PI component.
- Source `c` or `s` enters the finite external return/owner-growth component
  and its minimal Hall boundary.
- Source `r` enters the canonical two-stage root selector.

Thus an unsafe target is not a separate branch.

### 2. Canonical root response

At fixed `L`, first minimize the root core's `q`-value, maximizing anchor-
return payment over every common-safe root response.  If every return fails,
maximize the value of the floater-substituted root target.  If that also
fails, one canonical response `A=K+J` exposes a nonempty physical packet

\[
 K\subseteq B_q
\]

with the joint strict certificate

\[
 \begin{aligned}
 v_q(K)&>v_q(L\setminus J)+v_q(f),\\
 v_r(K)&>v_r(f)+v_r(A)-v_r(X_r).
 \end{aligned}                                      \tag{1}
\]

Changing common-safe root response cores at the same retained state cannot
avoid (1).

### 3. Global bilateral selector

Maximize `q(G)` over every root packet satisfying `v_r(G)<v_r(K)`.  Either
the bilateral exchange of `G` and `K` pays both mutual owners, or every
root-improving bilateral packet has the same strict order in both rows:

\[
 v_r(G)<v_r(K)\Longrightarrow v_q(G)<v_q(K).        \tag{2}
\]

Thus the later-owner sacrifice in the next operation is necessary across
the entire packet family, not an artifact of a local choice.

### 4. Complete connected transfer path

For any root-affordable `G`, including `G=empty`, allocate

\[
 Y_q=(X_q\setminus K)+f,
 \qquad Y_r=(X_r\setminus G)+K,
\]

and, when `G` is nonempty, give it to either external sink.  This is the
complete connected path

\[
 \mathrm{charity}\to q\to r\;(\to a).
\]

The root strictly improves, `q` loses only `K-f`, and an EFX endpoint is a
strict global lexicographic improvement.  Every non-EFX target has an exact
packet-replacement or target-threshold polarity, and the path's response
incoming packets are internally supplied.

### 5. Permanent root response anchor

The completed `q` target contains the original common-safe desired root core

\[
 T_q+f.
\]

As an edge into slot `q`, it releases all of `B_q`, including `K`, and
therefore supplies every response into the changed root target.  A `q`
source for that root target closes a PI 2-cycle.  An external source grows a
root-anchored matching.  The only source collision is the explicit pair

\[
 \{Y_q,Y_r\}\longleftarrow\{r\}.                   \tag{3}
\]

## Exact remaining terminals

The chain above removes the former unnamed branches: q-margin reset,
switching among root responses, unsafe evolved targets, absence of a
nonempty compensation packet, fixed bilateral choice, and disconnected
release support.

It does **not** yet close two terminals.

1. **Root-monopoly pair.** In (3), prove a complement has a nonroot source,
   or derive a fresh retained-support increase/root change.  A reset to the
   permanent external-bottom anchor is available but is not progress unless
   it preserves a strictly larger global potential.
2. **Root-anchored sacrificed-`q` Hall defect.** After an external source or
   sink response grows the matching, maximum-matching owner-union
   compression may leave `q` as a sacrificed residual owner.  Existing
   recapture, source-inactive repair, and two-hole selectors terminate their
   local chains, but a proof must show their reset cannot decrease the outer
   retained-support/response-rank potential.

These are two presentations of the same global issue: a local Hall repair
can return to a lower-rank root anchor without yet forcing fresh `T_r`
support.  The initially proposed lexicographic potential was

\[
 (|U|,\ \text{response rank},\ \text{represented owner union},\
   \text{missing-owner residual value})             \tag{4}
\]

Its raw fourth coordinate is now exactly refuted: it compares utilities
from different valuation rows after a hole change and is reversed by a
positive rescaling that preserves every EFX/response premise.  At rank two
there are also two holes, so the coordinate is not single-valued.  See
[`GG_RANK_RESET_RAW_POTENTIAL_REFUTATION_20260811.md`](GG_RANK_RESET_RAW_POTENTIAL_REFUTATION_20260811.md).

The live replacement is an owner-indexed normalized residual ledger together
with historical (rather than instantaneous) rank and supplier-union maxima.
A valid proof must still show that every rank-lowering reset advances that
ledger or its physical-support history; finiteness alone does not suffice.

## Verification and claim boundary

The focused dependency replay currently passes 43 tests spanning the retained-support,
dual-anchor frozen-profile census, response compression, two-hole/root-
critical machinery, and the new connected-path chain.  The dependency
manifest is
[`gg_retained_support_connected_path_composition_audit.json`](gg_retained_support_connected_path_composition_audit.json).

That manifest proves artifact integrity and replay status, not the corrected
support-ledger monotonicity theorem.  This checkpoint does not close `GG`,
the other seven three-nonsingleton classes, the four-nonsingleton branch, the
tie/zero wrapper, or four-agent/general additive EFX.

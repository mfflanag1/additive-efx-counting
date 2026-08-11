# Joint-packet charity-completed transfer-path lemma

**Date:** 2026-08-11

**Status:** cap-free complete connected candidate from every canonical joint
packet; termination of its sacrificed-owner response/Hall boundary remains
open

## Complete transfer path

Use the canonical joint packet

\[
 \varnothing\ne K\subseteq B_q\subseteq X_q
\]

and any root-affordable packet, possibly empty,

\[
 G\subseteq X_r,
 \qquad v_r(G)<v_r(K).                              \tag{1}
\]

If `G` is nonempty, choose either external sink `a in {c,s}` and let `b` be
the other external owner.  If `G` is empty, omit the sink step and keep both
external bundles fixed.  Define

\[
 Y_q=(X_q\setminus K)+f,
 \qquad Y_r=(X_r\setminus G)+K,                     \tag{2}
\]

and, when `G` is nonempty,

\[
 Y_a=X_a+G,
 \qquad Y_b=X_b.                                    \tag{3}
\]

Leave no charity.  The transfer multigraph is the single connected path

\[
 \mathrm{charity}\longrightarrow q:f,
 \qquad q\longrightarrow r:K,
\]

extended, when `G` is nonempty, by

\[
 r\longrightarrow a:G.                             \tag{4}
\]

The construction is complete for every packet cardinality.

## Priority and payment

Equation (1) makes the earlier root strictly improve.  The external sink,
when present, strictly improves by positivity.  The joint-packet certificate
gives

\[
 v_q(K)>v_q(f),                                     \tag{5}
\]

so the later mutual owner `q` loses, but by only `v_q(K)-v_q(f)` rather than
the full value of `K`.  Every owner before `r` is unchanged or is the
improving sink, and `r` precedes the losing `q`.  Hence any EFX instance of
(2)--(3) is a complete strict lexicographic improvement.

This candidate exists even when the empty packet is the only
root-affordable `G`: then the connected path simply ends at `r`.

## Exhaustive wall localization

Every owner other than `q` is weakly nonworse than at the base, and there is
no charity target.  Therefore every EFX failure is one of:

1. a wall by the sacrificed owner `q` against an owner target;
2. a wall against the changed `q` target `(X_q\setminus K)+f`;
3. a wall against the changed root target `(X_r\setminus G)+K`; or
4. when `G` is nonempty, a wall against the enlarged sink target `X_a+G`.

All unchanged targets remain base-safe for every nonlosing observer.

The three non-donor target types carry exact strict polarities.

### Floater-replacement target

Because `K subseteq B_q` and `T_q` is nonempty, `X_q\setminus K` is
nonempty.  The packet-for-charity threshold comparison applies.  Any
unchanged observer whose first new wall is against `(X_q\setminus K)+f`
must satisfy

\[
 v_i(f)>v_i(K).                                     \tag{6}
\]

A minimal desired response core either consumes `f`, giving the generalized
`(f|K)` edge, or yields the parallel ordinary response into the `q` slot.

### Root and sink targets

An unchanged observer's wall against the root or sink target forces,
respectively,

\[
 \tau_i((X_r\setminus G)+K)>\tau_i(X_r),            \tag{7}
\]

or

\[
 \tau_i(X_a+G)>\tau_i(X_a).                         \tag{8}
\]

Global minimal desired-subset extraction makes each response core
common-safe and names its source.

## Release-compatible response component

Relative to the base state, the changed target labels have incoming and
release packets

| target | incoming | release |
|---|---|---|
| `q` | `{f}` | `K` |
| `r` | `K` | `G` |
| `a` (if present) | `G` | `empty` |

The incoming packets are pairwise disjoint and every one is supplied by the
preceding target on path (4), with `f` supplied by charity.  Consequently
any internal response SDR is a release-compatible generalized PI component.
An outside source strictly grows the owner union.  Without either, maximum-
matching owner-union compression yields the existing sacrificed-owner
minimal Hall boundary; `q` is priority-eligible to be the missing source.

Thus every canonical joint packet now produces a complete connected
candidate with exactly three outcomes: EFX lex improvement, PI/owner-union
growth, or a named sacrificed-owner Hall defect.  No nonempty compensation
packet, fixed move radius, or item cap is assumed.

## Verification and claim boundary

[`joint_packet_charity_completed_transfer_path_audit.json`](joint_packet_charity_completed_transfer_path_audit.json)
checks support conservation with and without the external sink, strict root
payment, the donor's exact loss, and the root/sink target-wall polarities
under Z3 5.0.0.  The floater packet-replacement implication and internal
response support reuse their earlier independent audits.

This lemma constructs the complete connected candidate required by the
joint-packet terminal.  It does not prove that its response relation has an
SDR, eliminate every sacrificed-owner Hall defect, terminate a later
recapture, close `GG`, or prove four-agent/general additive EFX.

# Joint-packet external-sink rerouting lemma

**Date:** 2026-08-11

**Status:** cap-free construction of the required `q -> r -> external`
connected topology; termination of its sacrificed-owner response boundary
remains open

## External rerouting

Use the joint packet `K subseteq X_q` and any nonempty root-affordable
packet

\[
 \varnothing\ne G\subseteq X_r,
 \qquad v_r(G)<v_r(K).                              \tag{1}
\]

For either external owner `a in {c,s}`, let `b` be the other external owner
and form

\[
 Y_r=(X_r\setminus G)+K,
 \qquad Y_q=X_q\setminus K,
 \qquad Y_a=X_a+G,
 \qquad Y_b=X_b,
 \qquad P_Y=\{f\}.                                 \tag{2}
\]

This is the connected transfer path

\[
 q\longrightarrow r:K,
 \qquad r\longrightarrow a:G.                     \tag{3}
\]

The root strictly improves by (1), and the external sink strictly improves
by positivity.  Every owner before `r` is either unchanged or is the
improving sink `a`, while the losing mutual owner `q` occurs after `r`.
Therefore an EFX instance of (2) is a strict global lexicographic
improvement.

Unlike charity donation, (2) leaves the charity bundle unchanged.  It is
exactly the cap-free packet lift of the first connected escape in the
hardened weighted-Hall profiles.

## Exact wall localization

If (2) is not EFX, every failure has one of the following forms.

1. **Sacrificed-owner wall.** The losing owner `q` fails an owner-target
   comparison or charity dominance.
2. **Root-target wall.** An owner in `{a,b}` strongly envies
   `(X_r\setminus G)+K`.
3. **Sink-target wall.** An owner in `{r,b}` strongly envies `X_a+G`.

No other wall is possible.  Every owner other than `q` is weakly nonworse
than at the base.  Hence those owners remain safe against the unchanged
target `X_b`, the shrunken target `X_q\setminus K`, and the unchanged
charity `{f}`.  The root and sink cannot fail against their own targets.
Only the two enlarged/altered targets in branches 2--3 remain.

For an unchanged observer, a new root-target wall forces

\[
 \tau_i((X_r\setminus G)+K)>\tau_i(X_r),            \tag{4}
\]

and a new sink-target wall forces

\[
 \tau_i(X_a+G)>\tau_i(X_a).                         \tag{5}
\]

Global minimal desired-subset extraction converts either target wall into a
common-safe response core with a named source.

## Sacrificed-owner component

The affected physical owner union is `{q,r,a}`: packet `K` is released by
`q`, and packet `G` is passed through `r` to `a`.  Apply maximum-matching
owner-union compression to the response relation on the two changed target
slots together with every target named by a `q` wall.  The root is already
strictly improving and precedes `q`; any still earlier changed sink also
improves.  Thus `q` is sacrifice-eligible.

Consequently every external rerouting has one of four outcomes:

1. an EFX strict lexicographic improvement;
2. a release-compatible PI response component;
3. strict growth to the fourth owner `b`; or
4. the existing source-inactive/minimal-Hall sacrificed-owner boundary,
   with the captured packet and owner union explicit.

No item or value cap is used.  Both external sinks may be tested; changing
the sink cannot create an unbounded dependency because there are only two
external owners.

## Verification and claim boundary

[`joint_packet_external_sink_rerouting_audit.json`](joint_packet_external_sink_rerouting_audit.json)
checks support conservation, root/sink improvement, and both strict target-
threshold polarities under Z3 5.0.0.  Release support of the resulting
owner-union compression is inherited from the maximum-matching compression
audit.

This lemma supplies the cap-free connected topology required by the frozen
adversaries and localizes every failure.  It does not prove that a nonempty
root-affordable `G` always exists, close every sacrificed-owner Hall
boundary, terminate both external sink choices, close `GG`, or prove
four-agent/general additive EFX.

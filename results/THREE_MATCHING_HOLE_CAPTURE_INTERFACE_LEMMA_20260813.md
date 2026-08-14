# Three-matching hole-capture interface lemma

**Date:** 2026-08-13

**Status:** cap-free exact reduction of rank-three payment failure to three
signed hole certificates; simultaneous-capture reversal remains open

## Near-perfect response matching

Let `(Y,P)` be a physical allocation of all goods among four owners and a
nonempty charity packet. Let `M` be any matching of three distinct response
sources to three distinct owner targets. For every edge `i->t` choose a
nonempty desired core

\[
                     C_i\subseteq Y_t,
       \qquad v_i(C_i)>v_i(X_i).                  \tag{1}
\]

The three cores are disjoint because their physical targets are distinct.
Let `h` be the unique owner not used as a response source. For every owner
target `t`, write `O_t` for the core removed from `Y_t`, or the empty packet
when `t` is the unmatched target.

Reverse the three response edges, retain every target residual, and give the
whole charity packet to `h`:

\[
 Z_i=(Y_i\setminus O_i)\mathbin{\dot\cup}C_i
       \quad(i\ne h),                             \tag{2}
\]

where `C_i` is present exactly for the three matched sources, and

\[
 Z_h=(Y_h\setminus O_h)\mathbin{\dot\cup}P.       \tag{3}
\]

Equations (2)--(3) partition every good and leave empty charity. They use at
most the three reversed response supplier-recipient pairs plus the single
charity-to-`h` pair. Thus the support-edge count is at most four, with no
bound on the sizes of `P`, the cores, or the residuals.

Every matched source is strictly base-paid: its final bundle contains the
desired core `C_i`. The exact margin of the unmatched source is

\[
 v_h(Z_h)-v_h(X_h)
 =\Delta_h-v_h(O_h)+v_h(P),
 \qquad \Delta_h=v_h(Y_h)-v_h(X_h).              \tag{4}
\]

Consequently the candidate is all-owner-paid unless

\[
             v_h(O_h)>\Delta_h+v_h(P).           \tag{5}
\]

This includes the bare sacrificed-owner deficit: if `h` is the unmatched
target, then `O_h` is empty and (5) is simply
`v_h(Y_h)+v_h(P)<v_h(X_h)`.

## The three matchings at the fixed-U gate

In either surviving five-response form there are three canonical
near-perfect matchings at the graph level:

1. the selected rank-three matching on sources `{r,q,s}`;
2. replace the selected core in target `q` by a disjoint `d`-response core;
3. replace the selected core in target `r` by a disjoint `d`-response core.

No disjointness from the omitted selected core is needed: a replacement
matching allocates the `d` core and simply leaves the replaced core unused.
Its three used cores lie in distinct physical targets and are automatically
disjoint.

There is a load-bearing status distinction. The `d->q` core is an ordinary
base-desired core and therefore pays matched source `d`. The strong-wall
edge `d->r` may be only current-desired; because `d` is the unpaid sacrificed
owner, current desire alone does not imply base payment. Consequently the
payment theorem above applies unconditionally to the selected matching's
represented sources and to the `d->q` replacement, but applies to the
`d->r` replacement only if its chosen core is also base-desired or its signed
residual independently pays `d`.

The shared-target disjoint-or-capture lemma and generalized-PI capture also
apply only to a base-common-safe desired `d` core. The unconditional fixed-U
survivor is therefore one exact hole certificate at target `q`, plus a
mixed-status `d->r` payment/observer branch—not three symmetric base-response
certificates.

If any candidate is paid, every observer failure is routed by the paid-splice
lemma to a full decorated current response. At an exact saturated repeat that
response must augment/grow/progress, enter generalized PI, or be handled by
represented-component extraction. Thus the genuine survivor is not an
unclassified topology: it is **simultaneous three-hole capture at one signed
physical record**.

## Interaction with generalized PI

For every base-common-safe desired `d` core, the closed disjoint-core theorem
says a disjoint replacement avoiding the selected union completes a
generalized PI family. Hence the selected union captures its complete strict
base-response margin. This applies unconditionally to `d->q`; extending it
to `d->r` requires first converting the current-only wall response to a base
response or using a current-floor analogue that does not invoke base PI.

The remaining closure-or-transfer lemma must combine these two facts with
the three certificates above. It must show either:

1. the alternating captured cores close into a disjoint desired-core family,
   contradicting generalized PI-freeness; or
2. one can trim/reroute the matched cores along the drainage arborescence so
   that all three hole inequalities reverse while retaining the four-edge
   support graph.

This is a strictly smaller obligation than searching arbitrary packet
graphs: graph completeness, conservation, and all matched-source payments
are already exact.

## Boundary

The lemma proves the candidate construction and the exact failure
certificates. It does not prove that one of the three candidates is paid,
reverse simultaneous capture, establish observer safety without invoking
the saturated decorated-response continuation, or finish the active
four-edge theorem.

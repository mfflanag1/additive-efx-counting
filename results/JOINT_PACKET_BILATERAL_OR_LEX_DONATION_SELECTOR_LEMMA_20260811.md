# Joint-packet bilateral-or-lex-donation selector lemma

**Date:** 2026-08-11

**Status:** cap-free global selection over every root-affordable bilateral
exchange; termination after necessary later-owner sacrifice remains open

## Root-affordable compensation family

Use the canonical joint packet

\[
 \varnothing\ne K\subseteq X_q
\]

with `r` preceding `q`.  Define the finite nonempty family

\[
 \mathcal G(K)=\{G\subseteq X_r:v_r(G)<v_r(K)\}.    \tag{1}
\]

It contains the empty packet.  Choose

\[
 G^*\in\arg\max_{G\in\mathcal G(K)}v_q(G).          \tag{2}
\]

## Paying bilateral exchange

If

\[
 v_q(G^*)\ge v_q(K),                                \tag{3}
\]

form

\[
 Z_r=(X_r\setminus G^*)+K,
 \qquad Z_q=(X_q\setminus K)+G^*,
\]

fix the external bundles, and leave `{f}` as charity.  Equation (1) makes
the earlier root strictly improve.  Equation (3) makes `q` weakly nonworse;
nondegeneracy makes her comparison strict because the exchanged packets
are physically distinct.

Every owner is therefore weakly nonworse than at the base allocation and
still dominates `{f}`.  Only the two exchanged targets have changed.  An
EFX endpoint contradicts global lexicographic maximality; otherwise global
minimal desired-subset extraction produces a common-safe response core and
the resulting two-target response/Hall boundary is explicit.

## Universal bilateral failure

If (3) fails, maximality in (2) gives, for every root-affordable packet,

\[
 G\in\mathcal G(K)
 \quad\Longrightarrow\quad
 v_q(G)<v_q(K).                                     \tag{4}
\]

Thus every packet satisfying the strict root order

\[
 v_r(G)<v_r(K)
\]

has the same strict order in `q`'s row.  There is no root-improving
bilateral exchange that also pays the later owner.  This is a global
two-row separation over all subsets of `X_r`, not a bounded-radius or
single-good obstruction.

In this branch invoke the maximal charity-safe donation frontier.  It
selects `G_d in G(K)` satisfying root charity dominance and forms the
connected lexicographic component

\[
 q\longrightarrow r:K,
 \qquad
 r\longrightarrow\mathrm{charity}:G_d
\]

when `G_d` is nonempty.  Equation (4) proves that allowing `q` to lose in
that component is necessary for every root-affordable choice, rather than
an avoidable failure of packet selection.

## Composition consequence

The canonical joint packet now has an exhaustive global entrance:

1. a mutually paying bilateral exchange, followed only by a named
   response/Hall boundary; or
2. the universal separation (4), followed by a charity-safe connected
   lexicographic donation with only donor or external blockers.

Changing the root packet cannot escape branch 2.  The remaining proof must
use the donor's loss-band wall or add an external response owner to the
connected component; it should not search for another bilateral packet.

## Verification and claim boundary

[`joint_packet_bilateral_or_lex_donation_selector_audit.json`](joint_packet_bilateral_or_lex_donation_selector_audit.json)
checks both-owner payment in the bilateral allocation and propagation of
the global maximum's failure to every root-affordable packet under Z3
5.0.0.

This lemma globally eliminates bilateral packet choice as an open search.
It does not close the paying exchange's response relation, pay the donor in
the universal-failure branch, terminate the external connected component,
close `GG`, or prove four-agent/general additive EFX.

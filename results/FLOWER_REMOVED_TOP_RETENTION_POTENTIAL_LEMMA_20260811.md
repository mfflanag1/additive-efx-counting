# Flower removed-top retention potential lemma

**Date:** 2026-08-11

**Status:** cap-free global potential across q-oriented/root-oriented resets;
terminal q-margin capture and unsafe augmentation remain open

## Persistent reduced mutual core

The later mutual owner initially desires the common-safe core

\[
 D_q=T_r+f,
 \qquad \mu_0=v_q(D_q)-v_q(X_q)>0.                  \tag{1}

Let `U subseteq T_r` be the union of every root-top packet removed from this
core by a fresh top switch.  Define

\[
 D(U)=(T_r\setminus U)+f.                            \tag{2}

Deletion preserves common safety, so `D(U)` is common-safe for every `U`.
Its exact `q`-response margin is

\[
 \mu(U)=v_q(D(U))-v_q(X_q)=\mu_0-v_q(U).             \tag{3}

Consequently exactly one of the following holds:

1. `mu(U)>0`, and `D(U)` remains a valid desired core for `q`; or
2. `mu(U)<=0`, and

   \[
   v_q(U)\ge\mu_0,                                   \tag{4}
   \]

   so the removed packet captures `q`'s whole original response margin.

## Retention across root changes

During a root-oriented detour, the goods of `U` may be assigned to external
cores, residual cells, or a root-payment packet.  Nothing in the flower
operations requires putting them back into `q`'s mutual core.  On returning
to a q-oriented rank-two state, select `D(U)`, not the original `D_q`.

If (4) has not occurred, `D(U)` is still disjoint, common-safe, and desired,
so every dual-anchor/root-paid and canonical external-response selector
applies verbatim.  Thus root flips and response resets can preserve the same
removed support `U`; resetting the mutual core to `D_q` is unnecessary.

## Global well-founded potential

Whenever a continuation needs a good of the current mutual core, remove a
nonempty fresh packet

\[
 K\subseteq T_r\setminus U
\]

and update

\[
 U'=U+K.                                              \tag{5}

If `D(U')` remains desired, then

\[
 U\subsetneq U',
 \qquad
 0<\mu(U')=\mu(U)-v_q(K)<\mu(U).                     \tag{6}

Otherwise (4) holds with `U'`.  Since `T_r` is finite, there are at most
`|T_r|` fresh-good additions.  The potential survives any number of
root-oriented detours because those detours retain `U` by construction.

At fixed `U`, the canonical external-core selector simultaneously eliminates
every common-safe external-core/source change disjoint from `D(U)`.  Hence a
PI-free recurrence can no longer alternate indefinitely between q-oriented
and root-oriented rank-two resets: it must expose a fresh packet, an unsafe
core, a root-sourced response, or the q-margin capture (4).

## Verification and claim boundary

[`flower_removed_top_retention_potential_audit.json`](flower_removed_top_retention_potential_audit.json)
checks the margin identity, strict fresh-packet descent, and terminal capture.

This lemma proves a persistent potential, not GG closure.  It does not
convert (4) into an EFX/PI component, eliminate unsafe response cores, prove
that every root-sourced response returns to the canonical family, close
`GG`, or prove four-agent/general additive EFX.

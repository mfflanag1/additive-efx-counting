# Decorated-target-owner complement-return selector lemma

**Date:** 2026-08-11

**Status:** cap-free intermediate bilateral selector; strictly strengthened
by the source-bundle charity-complement selector, whose separator supersedes
the old-core-only boundary below

## Sole surviving observer

Use the mixed Hamiltonian-path state after every observer other than the
decorated target owner has been closed by released-residual payment or a new
self-response.  Let

\[
 D\subseteq Y_t,
 \qquad R=Y_t\setminus D,                         \tag{1}
\]

where `D` is assigned to decorated source `s`, while target owner `t` is
assigned an old base-common-safe core `A_t` disjoint from `Y_t`.  Suppose

\[
 v_t(A_t+R)<\tau_t(D).                            \tag{2}
\]

Thus even returning the entire released target residual does not pay `t`.

## Nonempty complement-return family

Let `g` be a least-`t` good of `D`.  Then

\[
 v_t(D-g)=\tau_t(D)>v_t(A_t+R)>v_t(X_t).          \tag{3}
\]

Consequently the finite family

\[
 \mathcal J={J\subseteq D:
              v_t(D\setminus J)>v_t(X_t)}        \tag{4}
\]

is nonempty: `{g} in mathcal J`.  For `J in mathcal J`, make the connected
complement return

\[
 Z_t=D\setminus J,
 \qquad Z_s=A_t+R+J.                              \tag{5}
\]

Every good in `A_t dotunion Y_t` is conserved.  Owner `t` is strictly above
base and directly safe against every unchanged old common-safe core.

## Priority-valid source floor

Let `rho_s` equal `v_s(X_s)` when `s` must remain weakly above base to
preserve the fixed lexicographic prefix.  When an earlier root is already
strict and `s` is sacrifice-eligible, let `rho_s` instead be the maximum
direct threshold of the unchanged old cores and final charity.

For each `J in mathcal J` define

\[
 F_s(J)=\max\{\rho_s,\tau_s(D\setminus J)\},      \tag{6}
\]

and select `J*` maximizing the exact slack

\[
 \Phi(J)=v_s(A_t+R+J)-F_s(J).                     \tag{7}

No cardinality or value cap is involved; this is a maximum over physical
subsets of the one finite decorated core.

### Successful handoff

If `Phi(J*)>=0`, both `t` and `s` meet their priority-valid direct floors.
The target `D-J*` weakly lowers every observer threshold relative to `D`.
Every remaining old core is base-common-safe.  The only possible new wall is
therefore against the complement target `A_t+R+J*`; a wall there yields the
ordinary/full-decorated current-response augmentation, while no wall gives
an EFX/lex endpoint.  The moved packets form one connected cycle/residual
handoff.  Any deleted charity packet is handled by the arbitrary-charity
collapse lemma.

### Exact separator

If `Phi(J*)<0`, then for every target-owner-paying complement return,

\[
 v_s(A_t+R+J)
 <\max\{\rho_s,\tau_s(D\setminus J)\}.            \tag{8}

This excludes every bilateral division of `A_t dotunion Y_t`, including
every multi-good return packet.  The smallest remaining operation must bring
a packet from outside this two-target pool into `s`, change the decorated
source/root, or replace `D`.  It is the exact residual-handoff separator to
be contradicted by the full signed-transfer component or instantiated by a
globally maximal GG countermodel.

## Verification and boundary

[`decorated_target_owner_complement_return_selector_audit.json`](decorated_target_owner_complement_return_selector_audit.json)
checks nonemptiness via the least-good complement, conservation, target-owner
payment, the source-floor success implication, and the universal failure
separator symbolically.

This lemma does not eliminate (8), force an outside compensation packet,
produce a globally maximal countermodel, close the mixed-margin theorem,
close GG, or prove four-agent/general additive EFX.

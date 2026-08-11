# Component-wide return-compensation selector lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of every internal multi-donor ordering in a
surplus component; forcing success from the full GG return structure remains
open

## Connected observer component

Use the decorated response and cross-component debt

\[
 D\subseteq Y_j,
 \qquad \mu_s=v_s(D)-v_s(Y_s)>0,
 \qquad \tau_h(D)>v_h(X_h).                       \tag{1}

\]

Let `C` be the complete nontrivial physical signed-transfer component
containing observer `h`, disjoint from the component containing target `j`
and response source `s`.  Let

\[
 P_C=\mathop{\dot\bigcup}_{a\in C}Y_a             \tag{2}

\]

be its entire current goods pool.  For each `a in C`, fix a protected utility
floor `b_a` containing base payment, all already retained observer-safety
requirements, and any strict priority requirement.  The current component
allocation is feasible:

\[
 v_a(Y_a)\ge b_a.                                  \tag{3}

\]

## Global component selector

Choose a nonempty debt-removing packet

\[
 J\subseteq D,
 \qquad \tau_h(D\setminus J)\le v_h(X_h).         \tag{4}

\]

Partition the complete pool `P_C+J` as

\[
 P_C+J=L\mathbin{\dot\cup}
       \mathop{\dot\bigcup}_{a\in C}Z_a,          \tag{5}

\]

where `L` is returned to source `s`, subject to

\[
 v_a(Z_a)\ge b_aqquad(a\in C).                   \tag{6}

\]

The family is nonempty: take `J=D`, `L=empty`, keep `Z_a=Y_a` for `a!=h`,
and set `Z_h=Y_h+D`.  Among all feasible choices maximize

\[
 \Omega_C=v_s(L)-v_s(J).                          \tag{7}

\]

with deterministic physical tie-breaking.

## Exact dichotomy

1. **Component-wide paid bridge.** If

   \[
    \Omega_C>-\mu_s,                              \tag{8}
   \]

   give `D-J+L` to `s` and give `Z_a` to every `a in C`.  Source `s`
   strictly improves relative to `Y_s`, all component owners retain their
   complete protected floors, and (4) removes `h`'s old base-safety debt.
   The old transfer component on `C` is connected.  The nonempty edge
   `j -> C:J` joins it to the target component; `C -> s:L` and
   `j -> s:D-J` supply the response source whenever nonempty.  Since (8)
   makes `s` strict, at least one incoming source packet is nonempty, so all
   participating owners lie in one physical component.  Any new target-
   safety failure is routed by the surplus-decorated current-response lemma.
2. **Component-wide separator.** If (8) fails, then for every debt-removing
   `J` and every redistribution of the **entire** component pool retaining
   all floors,

   \[
    v_s(J)-v_s(L)\ge\mu_s.                         \tag{9}
   \]

   No donor ordering, alternating path, or branching transfer internal to
   `C` can compensate the response source.  The next operation must either
   recruit a packet from a different physical component, use an explicitly
   priority-valid base-floor sacrifice for `s`, or replace `D` by another
   response.  Re-running a local donor chain inside `C` cannot help.

The selector is finite for every finite instance but imposes no item or
value cap.  It optimizes the complete operation rather than enumerating a
bounded family of GG cells.

## Verification and boundary

[`component_wide_return_compensation_selector_audit.json`](component_wide_return_compensation_selector_audit.json)
checks nonempty feasibility, the source payment identity, component-floor
preservation, physical connectivity, and the global separator implication.

This lemma does not force (8) from the GG flower inequalities, preserve every
new observer comparison after `L` is attached, close outside-component
recruitment or a priority-valid source sacrifice, establish a globally
maximal GG countermodel, close GG, or prove four-agent/general additive EFX.

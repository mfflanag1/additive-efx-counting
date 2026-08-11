# Global-residual root-facing rigidity lemma

**Date:** 2026-08-11

**Status:** cap-free collapse of the root-preserving partition family at an
arbitrary-hole residual maximum; only unsafe augmentation, a top packet, or
the `f`-only captured-bottom handoff survives

## Setting

Use a state selected by the fixed-`U` arbitrary-hole residual theorem. The
distinguished nonroot hole `d` holds residual `W`, and the permanent root core
is

\[
 A=T_q+f.
\]

Suppose `d` has the surviving root-facing strong-envy wall against `A`, and
the root-facing exhaustion inequality gives

\[
 v_r(A)>v_r(W),
 \qquad v_r(A)>v_r(X_r).                            \tag{1}
\]

## Root-preserving selector

Among partitions

\[
 A\mathbin{\dot\cup}W=H\mathbin{\dot\cup}L
\]

satisfying

\[
 v_r(H)\ge v_r(A),
 \qquad v_r(H)\ge v_r(L),                          \tag{2}
\]

choose one maximizing `v_d(L)`. The old partition `(H,L)=(A,W)` is feasible
by (1), so

\[
 v_d(L)\ge v_d(W).                                  \tag{3}
\]

## Rigidity theorem

Exactly one of the following holds.

1. `H` is unsafe, and globally minimal desired-subset extraction supplies a
   named response augmentation.
2. The two-hole allocation closes by EFX/PI.
3. The selected common-safe root core is physically the old core and the
   residual is physically the old residual:
   \[
   (H,L)=(A,W).                                     \tag{4}
   \]

Indeed, suppose `H` is common-safe and the partition differs from `(A,W)`.
The root remains represented by a common-safe desired core, every other core
and retained support `U` is unchanged, and `d` remains the distinguished
residual owner. Nondegeneracy makes distinct residual supports have distinct
`d`-values. Together with (3), this gives

\[
 v_d(L)>v_d(W),
\]

contradicting the global choice of `W`. If `d` becomes response-active in the
new state, whole-core/nonroot descent or the anchor collision is invoked
before re-selection; an EFX endpoint or internal SDR closes. Thus no distinct
common-safe root-preserving partition survives.

## Item-critical consequence

In branch (4), `d` still strongly envies `A`. Let `g` be a least-`d` good of
`A`. Moving `g` to `W` strictly improves the selected residual, so at least
one root constraint in (2) must fail:

\[
 v_r(A-g)<v_r(X_r)                                  \tag{5}
\]

or

\[
 v_r(A-g)<v_r(W+g).                                 \tag{6}
\]

This is the root-critical least-good certificate at the original physical
state, not at an unrelated repartition.

Apply the root-critical compensator dichotomy and alternating frontier. They
terminate in a nonempty old-root-core packet `R_A subseteq A` satisfying

\[
 v_r(R_A)>v_r(W\setminus R_W)                       \tag{7}
\]

for the exact recruited residual packet `R_W`. Since `A=T_q+f`, either:

1. `R_A` contains a top good and enters top-core exchange/reset; or
2. `R_A={f}` and enters the captured-bottom handoff, with strict residual-
   support descent whenever `R_W` is nonempty.

## Verification and boundary

[`global_residual_root_facing_rigidity_audit.json`](global_residual_root_facing_rigidity_audit.json)
records exact hashes for the arbitrary-hole selector, root-preserving
selector, compensator dichotomy, and alternating frontier, and checks the
root-feasibility and strict-max implications symbolically.

This lemma removes every distinct common-safe root-preserving repartition. It
does not terminate the resulting top reset or `f`-only captured-bottom
exchange-stable frontier, select the final connected fork, close `GG`, or
prove four-agent/general additive EFX.

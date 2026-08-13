# Corrected mixed-edge deletion-return composition

**Date:** 2026-08-13

**Status:** cap-free re-run of the paid-response move in the `kappa=1`
Hamiltonian branch. The direct two-core exchange below is a useful strict
subselector, but it is not terminal: the unused hole-source core and deleted
good must be included in the general pool selector

## Correct input

Use the one-decorated interface from
`GENUINE_MIXED_EDGE_HAMILTONIAN_INTERFACE_20260813.md`.  The selected path is

\[
 h_0=t\to h_1\to h_2\to h_3\to c.               \tag{1}
\]

Its selected source cores are `K_i`, where exactly one core

\[
 K_d=D                                                     \tag{2}
\]

is current-desired/current-safe at the paid state `Y`, and the other three
are old base-common-safe desired cores.  A distinct current-safe response

\[
 E\subseteq Y_t                                             \tag{3}

from a nonhole source closes the path prefix.  Write

\[
 H=Y_t\setminus E.                                          \tag{4}

Assume the deletion-return target-owner separator

\[
 v_t(K_t+H)<\tau_t(E).                                      \tag{5}

Choose a least-`t` good `g in E` and put `P=E-g`.  Then

\[
 v_t(P)=\tau_t(E)>v_t(K_t+H)>v_t(X_t),                      \tag{6}
\]

and `P` is current-safe because deletion cannot raise any EFX threshold.

## Atomic corrected candidate

Do not attach any residual initially.  Allocate

\[
 Q_t=P,\qquad
 Q_d=D\quad(d\ne t),\qquad
 Q_i=K_i\quad(i\notin\{t,d\}).                              \tag{7}

When `d=t`, the selected `D=K_t` is left unallocated and (7) consists of
`P` plus the other three old cores.

The bundles in (7) are pairwise disjoint.  Every owner is strictly above
base: (6) pays `t`; (3) for selected `D` pays `d` above `Y_d`; and every old
core pays its source above `X`.  This removes the unsafe assumption that all
four selected path cores are old while retaining the actual mixed core.

All comparisons against old cores are automatically safe.  The only direct
EFX debts are against `P` and, when `d!=t`, against `D`.  Define

\[
 \mu_h=v_h(Q_h)-v_h(X_h)>0                                  \tag{8}
\]

and

\[
 \Gamma_h=max\left\{
   (\tau_h(P)-v_h(X_h))_+\ \ (h\ne t),
   (\tau_h(D)-v_h(X_h))_+\ \ (d\ne t,\ h\ne d)
 \right\},                                                 \tag{9}

omitting inapplicable entries.  Candidate (7) is EFX exactly when

\[
 \mu_h\ge\Gamma_h\qquad(h\in N).                            \tag{10}

Hence (10) gives an immediate partial EFX Pareto contradiction.

## Ordinary-observer compensation

Let `h notin {t,d}` fail (10).  Its own nonhole target has the exact path
decomposition

\[
 Y_h=C_h\mathbin{\dot\cup}R_h,                              \tag{11}

where `C_h` is its incoming selected core.  Both `P` and `D` are current-safe,
so the required threshold in row `h` is at most `v_h(Y_h)`.

1. If `K_h+R_h` reaches the required threshold, attaching `R_h` pays row
   `h`.  The only new risk is the enlarged target `K_h+R_h`; if unsafe, its
   globally minimal response is a new/current decorated response with the
   complete target and signed-transfer label.
2. If `K_h+R_h` still fails, cancellation gives

   \[
   v_h(C_h)>v_h(K_h)>v_h(X_h).                    \tag{12}
   \]

   If `C_h` is old, (12) is a base-common-safe replacement response.  If
   `C_h=D`, it is a second current source for the same mixed core, with a
   changed physical target label after (7).  It may be pivoted along the
   path only with its signed release label; it is not automatically an old
   self-PI edge.

This classifies every nonhole/nonmixed observer without making a
current-safe-to-base-safe substitution.

## Unique direct cross-decorated debt

The selected mixed source `d` automatically pays its comparison to `P`:

\[
 v_d(D)>v_d(Y_d)\ge\tau_d(E)\ge\tau_d(P).         \tag{13}

If `d=t`, there is no allocated `D`, so after the ordinary-observer branches
the direct two-core gate is finished.

If `d!=t`, the only special owner not covered above is the hole owner `t`.
Its survivor is

\[
 v_t(P)<\tau_t(D).                                \tag{14}

For every `J subseteq D`, form the connected two-core exchange

\[
 Q_t(J)=P+J,\qquad Q_d(J)=D\setminus J.           \tag{15}

Call `J` feasible when:

1. `v_d(Q_d(J))>v_d(X_d)`;
2. `t` and `d` are mutually EFX under (15); and
3. every unchanged old-core owner is safe against both bundles in (15).

Any feasible `J`, together with the two old cores, is a partial EFX
allocation strictly improving all owners.  The selector ranges over every
subpacket of `D` and uses no cap.

If no feasible `J` exists, the direct subselector has the
**cross-decorated two-core exchange separator**: every packet that removes
the hole owner's debt either consumes the mixed source's strict base margin,
creates reverse envy from `d` to `P+J`, or exceeds another old owner's
available margin.  A positive-rational local model in the audit satisfies
all current-safety and payment premises while this selector is empty.
Therefore the separator is not contradicted by positivity, deletion
minimality, or the two current-safety inequalities alone.

## Result of the re-run

The corrected one-decorated composition has the following exhaustive exits:

1. atomic EFX/Pareto via (10);
2. residual-paid observer, possibly followed by a newly labeled unsafe
   enlarged target;
3. old incoming-core replacement or an additional source for `D` via (12);
4. feasible cross-decorated exchange (15); or
5. the exact cross-decorated exchange separator.

This separator is not the final residual. The positive-rational model in the
audit has no feasible `J`, but the complete pool `Y_t+K_t+D` has 89 feasible
partial-EFX exchanges. Thus the model demonstrates why the deleted good,
hole complement, and unused hole-source core cannot be omitted. The general
mixed-edge deletion-return theorem supersedes this subselector.

## Claim boundary

This theorem proves payment, disjointness, the complete base-debt matrix,
ordinary-observer cancellation, and the finite two-core exchange selector.
It does not eliminate the exchange separator using the GG root/q
inequalities, terminate an old exact response from an unsafe enlarged
target, solve `kappa=2,3`, close GG, or prove four-agent/general additive
EFX.

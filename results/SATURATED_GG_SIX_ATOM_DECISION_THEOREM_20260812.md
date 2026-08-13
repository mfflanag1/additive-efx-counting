# Saturated GG six-atom adversarial decision theorem

**Date:** 2026-08-12

**Status:** exact bounded-atom UNSAT theorem; not cap-free

## Declared atomization

Use six positive atoms `P, g, A_r, A_q, A_c, A_s` and the Hamiltonian
current state

\[
 Y_r=P+g,\quad Y_q=A_r,\quad Y_c=A_q,\quad
 Y_s=A_c,\quad Q_Y=A_s.                          \tag{1}
\]

The exact decision model symbolically ranges over every base allocation of
these atoms. It includes the following named premise blocks:

1. positive normalized additive values;
2. a noncomplete base allocation that is EFX with charity;
3. selected common-safe desired path cores;
4. complete ordinary PI-freeness over every desired common-safe subset of
   every base owner target;
5. global lex maximality against every noncomplete allocation;
6. the full signed-transfer owner/charity coverage cut constraints;
7. current payment, a current-safe decorated response, response saturation,
   and observer-surplus inequalities;
8. the physical component-pool source-margin separator over every deletion
   and redistribution; and
9. failure of the direct deletion-return charity-safety candidate.

All `5^6=15,625` final owner/charity assignments are enumerated. Of these,
11,529 are noncomplete and enter the global-lex block. Every induced net
packet graph is included; there is no topology or moved-good-radius
restriction in the rival search.

## Exact result

The complete formula is **UNSAT**. Deletion minimization leaves exactly four
premise groups:

1. positivity and normalization;
2. weak current payment with the first owner strict;
3. exact current-response saturation; and
4. global lex maximality over all noncomplete allocations.

The other complete premise blocks are encoded but unnecessary for this
atomization.

## Extracted inequality

Current target `r` has the only nonsingleton owner bundle, `P+g`. Every
other owner target is a singleton and therefore has EFX threshold zero. If
some observer `i` violated EFX against `P+g`, then either

\[
 v_i(P)>v_i(Y_i)
 \quad\text{or}\quad
 v_i(g)>v_i(Y_i).                                 \tag{2}
\]

Either singleton is automatically current-common-safe, so (2) would be a
new current response, contrary to saturation. Similarly, unsafe singleton
charity would give

\[
 v_i(A_s)>v_i(Y_i),                               \tag{3}
\]

another forbidden current response. Consequently

\[
 v_i(Y_i)\ge
 \max\{v_i(P),v_i(g),v_i(A_s)\}                  \tag{4}
\]

for every owner. Equations (1) and (4) prove that `Y` is EFX with charity.
Current payment and the strict first row make `Y` a lexicographic improvement
of the base, contradicting global maximality.

## Verification and boundary

[`decide_saturated_gg_six_atom.py`](../tracks/parkability/decide_saturated_gg_six_atom.py)
is the exact QF_LRA/integer-holder decision encoding. Its output is
[`saturated_gg_six_atom_decision.json`](saturated_gg_six_atom_decision.json).
[`audit_saturated_gg_six_atom.py`](../tracks/parkability/audit_saturated_gg_six_atom.py)
independently reconstructs the four-group proof without Z3 and independently
enumerates the 15,625 allocation words; its output is
[`saturated_gg_six_atom_audit.json`](saturated_gg_six_atom_audit.json).

This is a **bounded six-atom theorem**. It is not the cap-free extraction
theorem, does not cover a target other than `P+g` with multiple atomic goods,
and does not exclude split or multi-good path cores. The shortest next
adversarial atomization must therefore split at least one singleton owner
target or the charity packet; merely adding packet-graph radius cannot alter
this UNSAT core.

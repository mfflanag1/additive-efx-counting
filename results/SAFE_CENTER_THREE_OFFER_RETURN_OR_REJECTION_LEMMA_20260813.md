# Safe-center three-offer return-or-rejection lemma

**Date:** 2026-08-13

**Status:** cap-free reduction of the safe-center star to two-hole response
machinery or an exact three-row center-return rejection separator

## Safe-center star

Let `s` be the center, let `H=N-{s}` be the three leaves, and let the current
owner bundles be `U_i`.  Assume:

1. `U_s` is current-safe and `b_s=v_s(U_s)`;
2. for every leaf `h in H`, a packet `O_h subsetneq U_h` is current-safe and
   strictly desired by `s`; and
3. the three offers and `U_s` are pairwise disjoint.

Let `F_h<=v_h(U_h)` be the protected floor that leaf `h` must retain.

## Canonical center return

For each leaf define the exact two-core threshold

\[
\rho_h=\max\{F_h,\tau_h(O_h)\}.                  \tag{1}
\]

If some leaf satisfies

\[
v_h(U_s)\ge\rho_h,                               \tag{2}
\]

assign `O_h` to the center and `U_s` to `h`.  The center strictly improves
because `O_h` is desired over `b_s`, and the safety of `U_s` gives

\[
\tau_s(U_s)\le b_s<v_s(O_h).                     \tag{3}
\]

Leaf `h` keeps her protected floor and pays her only other selected-core
comparison by (1)--(2).  Both selected cores are current-safe and physically
disjoint.  They therefore form a protected two-core input; pool the exact
complement for the other two leaves and invoke the existing two-hole cut-and-
choose response-Hall machinery.

## Exact rejection separator

If no leaf satisfies (2), then the star carries the simultaneous strict
certificate

\[
v_h(U_s)<\max\{F_h,\tau_h(O_h)\}
\qquad(h\in H).                                  \tag{4}

Thus the safe center bundle cannot serve as the direct return payment for
any of the three offer suppliers.  This is not merely response-rank one; it
is a named three-row payment separator.  Any closing arm transfer must use a
different physically released packet, lower a protected/observer threshold,
or change the root/anchor.  If all complete arm-compensation reservoirs also
fail, (4) enters the general holder-price separator family.

## Claim boundary

This lemma proves the canonical protected swap and the exhaustive rejection
certificate.  Entry into two-hole machinery is a reduction, not final GG
closure.  The lemma does not show that (4) contradicts global maximality,
force another compensation packet, close the atomwise/root holder-price
walls, close `T_{L,times}^*`, or prove four-agent/general EFX.


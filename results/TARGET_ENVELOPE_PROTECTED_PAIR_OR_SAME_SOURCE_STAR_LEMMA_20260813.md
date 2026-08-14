# Target-envelope protected-pair-or-same-source-star lemma

**Date:** 2026-08-13

**Status:** cap-free reduction of the safe-payment normalization wall to the
existing two-core/two-hole machinery or one three-offer same-source star

## Protected target envelope

Use one paid current state `Z`, one active target `U_j`, and its complete
current-safe response family `R_j`.  Let `F_h<=v_h(U_h)` be the exact
protected floor for each external observer `h != j`.  Define

\[
\widehat\Lambda_{hj}
 =\max\left\{F_h,\max_{D\in R_j}\tau_h(D)\right\}.               \tag{1}
\]

Choose an inclusion-minimal `Q_h subseteq U_h` with

\[
v_h(Q_h)\ge\widehat\Lambda_{hj}.                 \tag{2}
\]

If `Q_h` is current-safe, it is a protected universal payment packet: it
pays `h`'s floor and every response from `U_j`.  If it is unsafe, minimal
reversal gives a current-safe response `A_h subsetneq U_h`, desired by a
source `a_h != h`.

If all three external packets are unsafe, the target-envelope universal-
payment-or-PI lemma gives a supplier-closed PI cycle.  Assume henceforth that
at least one external packet is safe.  Fix any `D in R_j` and one of its
sources `s`; necessarily `s != j`.

## Exact reduction

Exactly one of the following routes is available.

### 1. Protected distinct-owner pair

If some safe `Q_h` has `h != s`, then `D` and `Q_h` are disjoint and
current-safe, `D` is current-desired by `s`, and

\[
v_h(Q_h)\ge F_h,
\qquad
v_h(Q_h)\ge\tau_h(D).                            \tag{3}
\]

They form two protected cores assigned to the distinct owners `s,h`.  Pool
the exact complement for the other two owners and invoke the existing
two-core/two-hole cut-and-choose response-Hall machinery.  Every later
same-target replacement of `D` remains paid in row `h` by (1).

### 2. Two distinct desired response cores

Suppose no safe packet belongs to an owner other than `s`.  Then `Q_s` is
safe and the other two external packets are unsafe.  If either reversal
source satisfies `a_k != s`, the pair `D,A_k` consists of disjoint current-
safe responses desired by two distinct owners.  This is again a rank-two
current-response input to the two-core/two-hole machinery.

### 3. Three-offer same-source star

The only remaining pattern is

\[
Q_s\text{ safe},
\qquad
Q_k,Q_\ell\text{ unsafe},
\qquad
a_k=a_\ell=s,                                    \tag{4}
\]

where `{s,k,ell}=N-{j}`.  The packets

\[
D\subseteq U_j,
\qquad A_k\subseteq U_k,
\qquad A_\ell\subseteq U_\ell                  \tag{5}
\]

are pairwise disjoint, current-safe, and all strictly desired by `s`.
Meanwhile `Q_s subseteq U_s` is current-safe, disjoint from (5), pays the
protected floor `F_s`, and pays `s` against every response in `R_j`.

This is the **protected-center three-offer star**.  It has no desired-edge
cycle and no rank-two response matching because all three offers have the
same source.  It is the sole normalization pattern not immediately sent to
PI or the existing two-hole machinery by the protected target envelope.

The center's whole current bundle `U_s` must itself be current-safe.  If it
were unsafe, globally minimal extraction inside `U_s` would give a
current-safe packet `A_s subsetneq U_s` desired by some source `a != s`.
The leaf `a` is one of `{j,k,ell}`, and its corresponding offer in (5) is
desired by `s`.  The two disjoint packets give the supplier-source edges

\[
s\longrightarrow a:A_s,
\qquad
a\longrightarrow s:O_a,                         \tag{6}
\]

a release-compatible PI 2-cycle.  Therefore the surviving star has a
common-safe center bundle `U_s` at value `b_s`; it may replace `Q_s` and pays
the center against all three current-safe offers.

## Why the split is exhaustive

If all packets are unsafe, PI closes.  Otherwise choose a safe packet.  A
safe owner different from `s` gives branch 1.  If none exists, the unique
possible safe external owner is `s`; each of the two other packets reverses.
A reversal source different from `s` gives branch 2, and both equal to `s`
give exactly (4).  No valuation or item enumeration is involved.

## Claim boundary

This lemma proves the protected-envelope case split, eliminates an unsafe
center by PI, and localizes the sole new obstruction to a safe center with
three same-source offers. Entry into two-core/two-hole machinery is a reduction, not
an assertion that every downstream retired-support collision is closed.  It
does not allocate the three leaves of the safe-center star, pay the retired-packet holder,
close the holder-price separator, close `T_{L,times}^*`, or prove four-agent /
general EFX.

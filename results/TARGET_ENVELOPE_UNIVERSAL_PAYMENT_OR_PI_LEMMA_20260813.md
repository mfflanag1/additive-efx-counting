# Target-envelope universal-payment-or-PI lemma

**Date:** 2026-08-13

**Status:** cap-free universal observer payment for one active target, or a
supplier-closed PI cycle

## One-target response family

Let `Z` be an exact paid current state with owner bundles `U_i=Z_i` and

\[
b_i=v_i(U_i).
\]

Fix a target owner `j`.  Let `R_j` be the complete nonempty family of
current-safe desired response cores contained in `U_j` that the active
selector may use during the current target phase.  Thus, for every
`D in R_j`,

\[
\tau_i(D)\le b_i\quad(i\in N),                   \tag{1}
\]

and `D` is strictly desired by at least one named source.  Positivity implies
that no such source is `j`, because `D subseteq U_j` has
`v_j(D)<=v_j(U_j)=b_j`.

For each external observer `h != j`, define the target-envelope threshold

\[
\Lambda_{hj}=\max_{D\in R_j}\tau_h(D).           \tag{2}
\]

The family is finite and (1) gives `Lambda_hj<=b_h`.  Choose an inclusion-
minimal packet `Q_h subseteq U_h` satisfying

\[
v_h(Q_h)\ge\Lambda_{hj}.                         \tag{3}
\]

## Safe universal-payment branch

If `Q_h` is current-safe, then it is physically disjoint from every member
of `R_j` and, for all `D in R_j`,

\[
v_h(Q_h)\ge\Lambda_{hj}\ge\tau_h(D).             \tag{4}
\]

Thus `Q_h` is a common-safe **universal payment packet** for observer `h`
against the entire current response family of target `j`.  Replacing one
response from `R_j` by another cannot recreate row-`h` debt while `Q_h`
remains assigned to `h`.

## Unsafe reversal branch

If `Q_h` is unsafe, some `g in Q_h` has a desired subset inside `Q_h-g`.
Choose a globally minimum such subset `A_h`.  It is current-safe, physically
contained in `U_h`, and desired by a named source `a_h`.  Minimality of
`Q_h` gives

\[
v_h(A_h)<\Lambda_{hj}.                            \tag{5}
\]

Also `a_h != h`, because positivity and strict containment give
`v_h(A_h)<v_h(U_h)=b_h`.

## Three-observer exhaustion

Run the construction for all three `h != j`.  If any safe branch occurs,
return its universal payment (4).  Otherwise choose any `D in R_j`, with
source `s != j`, and direct the four physical supplier-source edges

\[
j\longrightarrow s,
\qquad
h\longrightarrow a_h\quad(h\ne j).              \tag{6}
\]

Every owner has one outgoing nonself edge.  The corresponding packets
`D` and `A_h` lie in four distinct current owner bundles and are pairwise
disjoint.  The finite functional graph contains a directed cycle; every
cycle packet is supplied by its tail and strictly desired by its head.
Therefore the cycle is release-compatible PI.

Hence every active target phase has one of two outcomes:

1. an external common-safe packet universally pays one observer against all
   current responses from that target; or
2. a supplier-closed PI cycle.

No item, value, response-count, or valuation cap is used.

## Consequence for normalization bypass

The earlier pairwise safe-payment wall can be strengthened: the payment is
chosen at the complete target envelope, not at the threshold of one response.
An exact same-target selector reset cannot invalidate that row's payment.
If a specified blocking row has an unsafe envelope packet, its reversed
desired response is an actual new source/target edge and must be processed;
if all external rows are unsafe, PI closes immediately.

## Claim boundary

This lemma guarantees at least one external universal payer, not a distinct
universal payer for every observer.  It does not prove a simultaneous
protected perfect matching, ensure the safe payer is the currently decorated
head, resolve an unsafe specified-head reversal without changing target,
pay a retired-packet holder, close the holder-price separator, close
`T_{L,times}^*`, or prove four-agent/general EFX.


# Minimal safe root anchor or atomwise core lemma

**Date:** 2026-08-13

**Status:** cap-free root-support reduction; every recurrent protected-root
cut has an atomwise base-critical root core

## Exact root input

Let the globally maximal base root value be

\[
x=v_r(X_r)>0.
\]

At an exact ledger-normalized collision state, let the current physical root
core `A_r` be safe and strict:

\[
v_r(A_r)=x+\delta,
\qquad
\delta>0.                                        \tag{1}
\]

Every good of `A_r` carries its complete retired/support supplier label.
Deleting goods from a safe target preserves safety.

## Minimal-anchor operation

Choose an inclusion-minimal nonempty `Q subseteq A_r` satisfying

\[
v_r(Q)>x.                                        \tag{2}
\]

Such a packet exists by (1), and it is safe because `Q subseteq A_r`.

If `Q subsetneq A_r`, retain `Q` at the root and release `A_r-Q` with its
exact signed provenance. The root remains strictly above the globally
maximal base and the new root target is safe. This is a valid current-phase
root-preserving anchor reselection with a strict physical support/label
change. A released residual wall is processed as an actual response; a
retired hit is normalized before execution. The old root support cannot be
reported again at the same anchor-label coordinate.

Thus a recurrent state in which no valid root-support reduction remains must
have `Q=A_r`.

## Atomwise terminal

When `Q=A_r`, minimality gives for every `g in A_r`

\[
v_r(A_r-g)\le x,
\qquad
v_r(g)\ge\delta.                                 \tag{3}
\]

Summing the second inequality and using (1) yields

\[
(|A_r|-1)\delta\le x.                            \tag{4}
\]

Moreover every proper `D subsetneq A_r` satisfies

\[
v_r(D)\le x.                                     \tag{5}
\]

Hence no proper safe packet inside the root can trigger strict base-root
reselection. A hole-to-root response in the surviving loss band must be
paid by the retained complement/release reservoir or handled by controlled
anchor release; choosing another proper root subset cannot close it.

## Composition with the retired-packet cut

In the protected-holder branch `h=r`, combine (3)--(5) with the bi-row cut.
For every recipient-feasible `T subseteq K subseteq A_r`, the exact survivor
satisfies

\[
\sigma+M_r(T)<v_r(T)\le x.                       \tag{6}
\]

The lower bound blocks the compensated complement operation; the upper
bound follows automatically from root-anchor minimality whenever `T` is
proper. Thus the terminal is a **double atomic cut**:

1. `A_r` is inclusion-minimal above the base root value and obeys (3)--(4);
2. the recipient side is either packet-indivisible or every feasible packet
   is too expensive under (6); and
3. the scalar family realizing the bi-row cut also realizes (3)--(6), so a
   further proof must use physical response/anchor structure.

## Typed boundaries

- **Strict capture:** a sacrifice-eligible nonroot packet is already reduced
  unless recipient-indivisible; a root-held packet additionally lies in
  (6).
- **Equality:** every proper packet is recipient-infeasible, while root
  minimality blocks proper base-root reselection.
- **Base-floor debt:** (2) preserves the first-priority root only; another
  protected row retains its separately typed debt.
- **Release:** releasing `A_r-Q` is executed only with its signed suppliers;
  normalization may redirect a retired hit but may not silently restore the
  old label.

## Claim boundary

This lemma proves the valid minimal-anchor reduction and atomwise root-core
terminal. It does not pay (6), guarantee a nonempty released compensation
mode, resolve the recipient-indivisible whole packet, eliminate the double
atomic cut from global maximality, close `T_{L,times}^*`, or prove
four-agent/general EFX.

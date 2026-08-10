# Tail escape for the external-`r`, `p`-before-`r` rows

**Date:** 2026-08-09

**Status:** cap-free analytic theorem

**Priority orders:** `(p,s,r,q)` and `(s,p,r,q)`

## Theorem

Use the length-three normal form and put

\[
E=T_r+f,\qquad \theta=\tau_r(E).
\]

Assume the external singleton envy edge is `r -> s`.  Then the base state
is not globally lexicographically maximal in either order `(p,s,r,q)` or
`(s,p,r,q)`.

## Proof

As in the canonical external-`p` lemma,

\[
v_r(B_r+X_q)>b_r\ge\theta.
\]

Choose an inclusion-minimal `R subseteq B_r+X_q` with
`v_r(R)>=theta`.  Test deletion remainders of `R` at the ceilings

\[
v_p(E),\qquad v_q(x),\qquad b_s.
\tag{1}
\]

If all remainders satisfy (1), then

\[
(E,R,\{x\},\{y\})
\tag{2}
\]

is EFX.  It fixes `s` and improves `p`, so it closes both stated orders.

Otherwise extract an inclusion-minimal crossing set `F` inside a violating
deletion.  Every deletion of `F` lies below all three ceilings in (1), and
minimality of `R` gives

\[
v_r(F)<\theta.
\tag{3}
\]

There are three possible sources.

1. If `F` is `p`-sourced, `(F,E,{x},{y})` is EFX and improves `p`.
2. If `F` is `s`-sourced, `(E,{y},{x},F)` is EFX.  Each changed recipient
   receives a desired bundle: `p` gets `E`, `r` gets the envied singleton,
   `q` gets `x`, and `s` gets `F`.
3. Suppose `F` is `q`-sourced.  If `v_r(x)>=theta`, then
   `(E,{x},F,{y})` is EFX and improves `p`.  If `v_r(x)<theta`, choose a
   least-`r` good `h in E` and use
   
   \[
   (\{x,h\},E-h,F,\{y\}).
   \tag{4}
   \]

The EFX verification of (4) is the same least-pivot calculation as in the
external-`p` lemma.  The only source-dependent comparison is made by `s`.
Here `v_s(x)<=b_s`: otherwise the ordinary envy edges `s -> p` and
`r -> s`, together with the genuine edge `p -f-> r`, form a PI cycle with
one genuine charity edge.  Common safety of `E` gives `v_s(h)<=b_s`, and
the deletion bounds for `F` settle the rest.  Allocation (4) fixes `s` and
improves `p`.

All branches contradict lexicographic maximality in both orders. \(\square\)

## Boundary

The proof relies on `p` preceding `r`.  In orders `(s,r,p,q)` and
`(s,r,q,p)`, a tail payment or the bundle `E-h` may lower `r` before the
later improvement of `p` or `q`. Those two rows are now closed by the
independent cap-free reservoir extraction in
[`LENGTH_THREE_RESERVOIR_ORDER_ESCAPE_THEOREM.md`](LENGTH_THREE_RESERVOIR_ORDER_ESCAPE_THEOREM.md).

The four source/scalar packet calculations used here are included in the
exact aggregate audit
[`length_three_canonical_packet_audit.json`](length_three_canonical_packet_audit.json).

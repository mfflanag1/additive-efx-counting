# R3 two-target foreign-import edge-cancellation and margin lemma

**Date:** 2026-08-14

**Status:** exact cap-free edge criterion and critical foreign-margin
separator for the favorable root path

## Five signed cells

Use the favorable response path `z -> x -> y` from the two-target residual,
where `x` is the strict root and `z` currently owns the singleton `p`.
Decompose the two nonsingleton targets by their original saturated-support
suppliers:

\[
 B_x=X\mathbin{\dot\cup}U\mathbin{\dot\cup}V,
 \qquad B_y=Y\mathbin{\dot\cup}W,                \tag{1}
\]

where `X` is `x`-supplied, `U,Y` are `y`-supplied, and `V,W` are
`z`-supplied.  The current owner pairs are `y -> x`, `z -> x`, and
`z -> y` whenever the corresponding cells are nonempty.

Let the singleton holder's response core and the root's response core be

\[
 D_z=A_x\mathbin{\dot\cup}A_y\mathbin{\dot\cup}A_z
       \subseteq X\mathbin{\dot\cup}U\mathbin{\dot\cup}V,
 \qquad
 D_x=C_y\mathbin{\dot\cup}C_z
       \subseteq Y\mathbin{\dot\cup}W.           \tag{2}
\]

Apply the allocation in the favorable root-path lemma: give `D_z` to `z`,
give `D_x` to `x`, retain both target residuals, and give `p` to `y`.

## Exact edge identity

Besides the mandatory charity pair `charity -> y`, the final owner pairs are
exactly the following five indicators:

\[
\begin{array}{c|c}
x\to z&A_x\ne\varnothing,\\
y\to x&(U\setminus A_y)\ne\varnothing
        \text{ or }C_y\ne\varnothing,\\
y\to z&A_y\ne\varnothing,\\
z\to x&(V\setminus A_z)\ne\varnothing
        \text{ or }C_z\ne\varnothing,\\
z\to y&(W\setminus C_z)\ne\varnothing.
\end{array}                                      \tag{3}
\]

Consequently the endpoint uses at most four packet-transfer edges if and
only if at most three conditions in (3) hold.  This is the complete
supplier-compatibility criterion.  It permits many foreign-support cores:
an added `x -> z` or `y -> z` pair is affordable whenever completion/return
of old `y -> x`, `z -> x`, or `z -> y` cells cancels enough pairs.

For the maximal nondegenerate signature in which all five cells of (1) are
nonempty, classify each intersection in (2) as none, proper, or all.  Among
the 208 patterns with both response cores nonempty, exactly 69 satisfy the
four-edge criterion.  Fifty-three of those 69 use foreign support
`A_x union A_y`.  Thus the former sufficient condition `D_z subseteq V`
captures only 16 feasible signatures and is far from necessary.

## Foreign-margin separator

Put

\[
 F=A_x\mathbin{\dot\cup}A_y,
 \qquad \mu_z=v_z(D_z)-v_z(p)>0.                 \tag{4}
\]

If some subpacket of `A_z` is itself desired above `v_z(p)`, choose a minimal
such subpacket and invoke the supplier-compatible root-path lemma.  Otherwise
`v_z(A_z)<=v_z(p)`, and additivity gives

\[
                         v_z(F)\ge\mu_z>0.         \tag{5}
\]

If `D_z` was chosen inclusion-minimal desired, then for every good `g in D_z`

\[
                         v_z(g)\ge\mu_z,          \tag{6}
\]

because `D_z-g` is not desired.  Hence every genuinely incompatible survivor
contains an indispensable foreign physical packet carrying the singleton
holder's complete strict response margin; it is not merely a core with a
foreign label.

## Consequence and boundary

The favorable root path now has an exact split:

1. one of the edge-cancelling signatures (3) supplies a four-edge candidate;
2. a `z`-only desired subcore supplies the earlier compatible candidate; or
3. every candidate core contains a critical foreign packet satisfying
   (5)--(6), and its signed pattern violates the indicator budget in (3).

The third branch must be routed through generalized PI, support refinement,
or exact base-margin admission.  This lemma does not prove that routing,
observer safety of the candidate, repeat closure, the backward path,
singleton star, later-source anchor separator, fixed-`U`, or general EFX.

# Root-missing anchor substitution or critical-split frontier

**Date:** 2026-08-14

**Status:** conditional cap-free frontier inside the pure-cell model of the
parent census; the required lift from accumulated fan cores is not proved

## Six-map input

Use one of the six root-missing, missing-supplies-duplicate maps isolated
inside the conditional pure-cell model of
`LIQUIDATED_ROOT_THREE_SOURCE_PHYSICAL_COMPRESSION_FRONTIER_LEMMA_20260814.md`.
The nonroot target-to-source relation is a directed three-cycle.  The pure
root anchor `A`, originally supplied by `q`, is desired by a duplicated
nonroot source `a`.  The unique nonroot predecessor `u` of `a` also supplies
a desired core to `a`.  The root additionally owns its nonempty original
residual cell `Y_r`, and charity is the positive singleton `p`.

Let `F_i` be owner `i`'s current floor at this probe.  The whole anchor is
desired by `a`, so

\[
                    v_a(A)>F_a,
 \qquad \mu_a:=v_a(A)-F_a>0.                    \tag{1}
\]

All conclusions below require the parent lemma's pure-cell lift.  In
particular, the two selected nonroot response cores must be payable by their
whole single-supplier cells without a jointly required `Y_r` packet.  The
corrected reservoir-fan premises alone do not imply this.

## Anchor substitution

Omit the nonroot target `u`, rather than the root target.  Send the entire
anchor `A` to `a`, retain the whole cell of `u`, execute the other two edges
of the nonroot response cycle, retain `Y_r` at the root, and give `p` to the
root.

Every nonroot owner is paid.  Source `a` receives the whole desired anchor.
The other two sources receive their whole desired target cells, while `u`
also retains its own omitted cell.  The only possible payment failure is the
root:

\[
                         v_r(Y_r+p)>v_r(X_r).     \tag{2}
\]

The only possible nonself original-supplier pairs are

\[
 q\to a:A,\qquad
 t\to f(t)\quad(t\in\{1,2,3\}\setminus\{u\}),
 \qquad charity\to r:p.                          \tag{3}
\]

Self-pairs disappear and coincident pairs merge.  Thus (3) always contains
at most four pairs, for every anchor supplier and every one of the six maps.
If (2) holds, this is an all-owner-paid complete four-edge probe.  Failure is
the exact root-release wall

\[
                         v_r(Y_r+p)\le v_r(X_r). \tag{4}
\]

## Supplier-aligned partial-anchor split

Suppose `a=q`.  For any packet `H subseteq A`, retain `H` at the root and
send `A-H` to `a=q`, leaving the rest of the construction unchanged.  The
packet `A-H` returns to its original supplier and creates no edge.  If
`H` is nonempty, its retention uses `q->r`; together with the two surviving
cycle edges and charity this is still at most four pairs.

The root and source conditions are exactly

\[
 v_r(H)>\rho:=v_r(X_r)-v_r(Y_r)-v_r(p),          \tag{5}
\]

and

\[
                         v_a(H)<\mu_a.           \tag{6}
\]

If (4) holds, then `rho>=0`; since the current root owns `Y_r+A` strictly
above its base, `A` crosses the threshold in (5).  Choose an inclusion-
minimal `H_* subseteq A` satisfying (5).  Either it satisfies (6), giving the
four-edge paid probe, or

\[
\begin{aligned}
 v_r(H_*)&>\rho,\\
 v_r(H_*-g)&\le\rho &&(g\in H_*),\\
 v_a(H_*)&\ge\mu_a.                              \tag{7}
\end{aligned}
\]

Thus failure leaves one physical packet simultaneously critical for the
root's entire release deficit and large enough to capture the duplicated
source's full anchor-response margin.

## Supplier-misaligned boundary

When `a!=q`, a nonempty proper split of `A` activates both `q->r` and
`q->a`.  Together with the two surviving nonroot-cycle pairs and charity,
this has five pairs.  Hence the same split argument does not meet the edge
bound.  The full-release probe (3) still uses four and remains valid whenever
(2) holds.

Closing failure of (2) in the supplier-misaligned class requires a genuinely
different cyclic packet routing, cancellation of one surviving cycle pair,
or a signed PI/saturation implication.  Merely splitting the anchor cannot
do it.

## Claim boundary

Proved conditionally on the pure-cell lift: conservation, all nonroot
payments, the four-edge anchor-substitution
probe for all six maps, its exact root wall, and the cap-free critical-packet
alternative for the two supplier-aligned maps per anchor supplier.

Not proved: applicability to the actual accumulated fan; observer EFX safety
of the paid probe; closure of its decorated
response; elimination or routing of the critical packet; the four
supplier-misaligned maps per anchor supplier under wall (4); the universal
fixed-`U` theorem; or additive EFX.

# Predecessor cross-exchange overlap bicriteria lemma

**Date:** 2026-08-14

**Status:** cap-free conversion of shared-target capture in the two
predecessor-duplicate terminal maps to a paid four-edge split or one exact
minimal critical overlap packet

## Shared target

Use the predecessor-duplicate terminal construction from
`TERMINAL_PATH_OMITTED_CORE_CROSS_EXCHANGE_FRONTIER_20260814.md`.  Target
`q` contains:

- a base-desired core `C` for missing owner `m`; and
- a current-desired omitted core `E` for predecessor `x`.

Write

\[
 C_0=C\setminus E,\qquad E_0=E\setminus C,\qquad O=C\cap E.   \tag{1}
\]

The predecessor's path core `D subseteq B_x` is desired by `q`.  Let `R_m`
and `R_x` be the goods retained by `m` and `x` after the other declared
transfers.  Their required floors are `F_m=X_m` and `F_x` respectively.
Charity `p` goes to `m`.

## Exact overlap split

Choose `H subseteq O`, give

\[
 C_0+H\quad\text{to }m,qquad
 E_0+(O\setminus H)\quad\text{to }x,             \tag{2}

\]

send `D` to `q`, and retain every other good.  Define

\[
\begin{aligned}
 \alpha&=F_m-v_m(R_m+p+C_0),\\
 \gamma&=v_x(R_x+E_0+O)-F_x.                    \tag{3}
\end{aligned}

\]

The missing owner is paid exactly when

\[
                         v_m(H)\ge\alpha,         \tag{4}

\]

and predecessor `x` is paid exactly when

\[
                         v_x(H)\le\gamma.         \tag{5}

\]

Because the complete core `C=C_0+O` is base-desired by `m`, the full overlap
`H=O` satisfies (4).  Choose an inclusion-minimal `H_* subseteq O`
satisfying (4).

If (5) holds for `H_*`, every owner is paid.  Target `q` receives desired
core `D`; the fourth owner is unchanged.  The current-holder pairs remain

\[
       x\to q:D,qquad q\to x:E_0+(O\setminus H_*),qquad
       q\to m:C_0+H_*,qquad charity\to m:p.      \tag{6}


Empty packets delete their pair, so (6) uses at most four edges.

## Critical-overlap alternative

If (5) fails, minimality gives

\[
\begin{aligned}
 v_m(H_*)&\ge\alpha,\\
 v_m(H_*-g)&<\alpha &&(g\in H_*),\\
 v_x(H_*)&>\gamma.                               \tag{7}
\end{aligned}

\]

The same physical packet is therefore indispensable for repairing the
missing owner's base deficit and too expensive in the predecessor row to
divert from the predecessor's response bundle.

This strictly refines the earlier full-margin capture inequality.  Capture
does not remain an unnamed overlap case; it ends at one inclusion-minimal
two-row packet separator.

## Physical boundary

The two outgoing packets in (6) lie in current target `q`, but their goods
may have several frozen-`Y` suppliers.  Splitting `O` can therefore induce
more frozen-supplier/recipient pairs than the four current-holder pairs.
No frozen-supplier compression is asserted.

## Claim boundary

Proved: exact payment equivalences, existence and minimality of `H_*`, the
four-edge current-holder construction on success, and the critical-overlap
separator on failure.  Not proved: contradiction of (7) from the signed
fixed-`U` ledger, frozen-supplier compression, observer EFX safety,
decorated recurrence, or the fixed-`U` theorem.

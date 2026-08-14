# Form-0 full-owner Hamiltonian-path payment lemma

**Date:** 2026-08-14

**Status:** cap-free exact path construction and root separator; composition
with the saturated full-owner theorem is conditional on its complete signed
interface

## Response-chain input

Let `B=(B_r,B_q,B_d,B_s)` allocate every ordinary good and leave a positive
singleton `p` in charity.  Suppose the form-0 response relation supplies
pairwise-disjoint common-safe base-desired cores

\[
 C_q\subseteq B_r,
 \qquad C_d\subseteq B_q,
 \qquad C_s\subseteq B_d,                         \tag{1}
\]

for sources `q,d,s`, respectively.  Thus

\[
 v_q(C_q)>v_q(X_q),\quad
 v_d(C_d)>v_d(X_d),\quad
 v_s(C_s)>v_s(X_s).                               \tag{2}
\]

These are exactly the reverse-response edges on the full-owner chain

\[
                   q\to r,\qquad d\to q,
                   \qquad s\to d.                \tag{3}
\]

## Hamiltonian path allocation

Reverse (3) and insert charity at the root:

\[
\begin{aligned}
 Z_r&=(B_r\setminus C_q)+p,\\
 Z_q&=(B_q\setminus C_d)+C_q,\\
 Z_d&=(B_d\setminus C_s)+C_d,\\
 Z_s&=B_s+C_s.                                    \tag{4}
\end{aligned}
\]

The four packets in (4) partition all goods and use only

\[
             \mathrm{charity}\to r\to q\to d\to s. \tag{5}
\]

No packet-size bound is used.  By (2), owners `q,d,s` are strictly above
their base bundles, irrespective of the residual packets retained in (4).
The root has the exact base margin

\[
 v_r(Z_r)-v_r(X_r)
 =v_r(B_r)+v_r(p)-v_r(C_q)-v_r(X_r).              \tag{6}

\]

Consequently (4) is all-owner paid whenever

\[
 v_r(C_q)\le v_r(B_r)+v_r(p)-v_r(X_r).            \tag{7}

\]

Failure is the single exact root-capture separator

\[
 v_r(C_q)>v_r(B_r)+v_r(p)-v_r(X_r).               \tag{8}

\]

## Saturated composition

The final bundles in (4) need not be observer-safe merely because the three
cores are common-safe: each bundle also contains a retained residual.  If
(7) holds, however, (4) is an all-owner-paid four-edge candidate.  Any EFX
failure is therefore a paid-splice decorated response on a component already
containing all four owners.

At the exact saturated form-0 terminal, either one such path redistribution
is paid and enters that continuation, or failure of every debt-removing path
redistribution is part of the component-wide base-margin separator.  After
verifying the complete signed response/release labels required by
`UNIVERSAL_FULL_OWNER_CHARITY_EXCHANGE_EXTRACTION_THEOREM_20260812.md`, both
alternatives close: the first by paid-splice continuation and the second by
the full-owner extraction theorem.

This explains the unique topology in
`ALLOCATED_E_FORM0_HAMILTONIAN_PATH_BOUNDED_THEOREM_20260814.md`: the bounded
solver is selecting the physical reverse of the full-owner response chain,
not an accidental atom-level graph.

## Claim boundary

Proved unconditionally: conservation, the four-edge Hamiltonian path,
payments of `q,d,s`, and the exact root separator (8).

Conditional composition: exclusion of the saturated form-0 terminal requires
checking that its current response cores and every failed path candidate
carry the full signed/base-margin interface of the cited extraction theorem.
This lemma does not perform that statement-integrity audit, close form 2,
prove the complete fixed-U theorem, or prove general additive EFX.

# Retired-packet bi-row cut: cap-free scalar realizability

**Date:** 2026-08-13

**Status:** exact parametric no-go for a row-local contradiction; not a GG
counterexample

## Statement

The final bi-row separator

\[
v_s(T)\ge d
\quad\Longrightarrow\quad
v_h(T)>\sigma+M_h(T)
\qquad(T\subseteq K)                              \tag{1}
\]

is compatible with positive additive valuations for every finite nonempty
packet size, in both strict and equality-critical capture. It remains
compatible with the full-packet aggregate-underpayment wall and with the
bounded root-holder loss band. Consequently
no argument using only the recipient row, holder row, typed floors, packet
cardinality, and downward closure of the compensation modes can contradict
(1).

## Parametric construction

Let `K` be any finite nonempty set and choose arbitrary positive rational
weights `a_g`. Put

\[
S=\sum_{g\in K}a_g,
\qquad
v_s(g)=a_g,
\qquad
v_h(g)=L a_g                                    \tag{2}
\]

for any rational `L>0`. Choose `0<d<=S` and set `mu=S-d`. Give the recipient
a disjoint positive-valued base packet `B` and set

\[
F_s=v_s(B)+d.
\]

Then `A=B dot-union K` has

\[
v_s(A)-F_s=\mu,
\qquad
F_s-v_s(B)=d,
\qquad
v_s(K)=\mu+d.                                   \tag{3}
\]

Give the holder `Y_h=H dot-union K` and take
`F_h=v_h(Y_h)`, so `sigma=0`. Let the only physically compatible release
mode be the empty mode; equivalently `M_h(T)=0` for every transfer. This is a
downward-closed mode and models the exact branch in which every other good
is protected or supplier-incompatible.

The zero-slack version already gives, for every recipient-feasible packet,

\[
v_s(T)\ge d>0
\quad\Longrightarrow\quad
v_h(T)=L v_s(T)\ge Ld>0=\sigma+M_h(T),           \tag{4}
\]

which proves (1). In particular

\[
M_h(K)=0<v_h(K)-\sigma=LS,                       \tag{5}
\]

so the complete full-packet pool also underpays.

## Simultaneous root-holder band

The construction can also make `h=r` the protected root. Choose

\[
0<\delta< Ld,
\qquad
x>LS,
\qquad
v_r(H)=x+\delta-LS>0.                            \tag{6}
\]

Then the current root bundle `H+K` has value `x+delta`, so its exact slack
above the base root value `x` is `sigma=delta`. For every recipient-feasible
`T`,

\[
\delta<v_r(T)\le LS<x.                           \tag{7}
\]

With the empty compatible mode, (7) is simultaneously:

- strict holder underpayment `v_r(T)>sigma+M_r(T)`;
- failure of the unassisted complement branch; and
- failure of strict root reselection, because `v_r(T)<x`.

Thus the exact closed root-surplus band is itself scalar-consistent. The
additional historical inequality that the retired packet has root value at
most the base is also satisfied strictly: `v_r(K)=LS<x`.

- Taking `d<S` gives strict capture `mu>0`.
- Taking `d=S` gives equality-critical capture `mu=0`; positivity makes the
  whole packet the only recipient-feasible subpacket.

The construction is cap-free and analytic. The number of goods and their
positive rational weights are arbitrary.

## Consequence for the proof architecture

The packet cut and root loss band are not disguised numerical
contradictions. A successful
closure must use information absent from (2)--(5), such as:

1. a globally maximality-blocking EFX allocation obtained by sacrificing a
   later owner;
2. a safe root/anchor response permitting controlled release or reselection;
3. a release-compatible PI component; or
4. an exact response-rank operation tied to the physical GG topology.

The smallest unresolved operation is therefore not another packet threshold
or valuation bound. It is a **global cut-to-anchor conversion**: turn the
holder-infeasible contested packet into a safe root/anchor exchange or an
external-observer-safe suffix reallocation while preserving the earlier
strict root.

## Claim boundary

This theorem refutes only row-local and scalar-potential proofs of the
bi-row cut, including the existing root-surplus split. The empty release mode has exact physical meaning only after the
full GG protected/supplier record certifies that all nonempty modes are
unavailable. The construction does not supply an allocation, matching,
anchor, retirement history, global lexicographic maximality certificate, or
exact recurrence. It is therefore not a counterexample to
`T_{L,times}^*`, four-agent additive EFX, or general EFX.

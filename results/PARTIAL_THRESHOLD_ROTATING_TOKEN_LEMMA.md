# Rotating-token lemma and canonical pair-Hall sector

## Human theorem

Let

\[
B=01\mid23\mid45\mid67;\qquad f=8
\]

be an eligible positive-additive partial allocation.  Write (c_i=2i) for
owner (i)'s core and (t_i=2i+1) for its unique minimum, so
(v_i(t_i)<v_i(c_i)).  Suppose fixed-token-orbit maximality has the following
standard consequence: whenever a permutation of (t_0,t_1,t_2,t_3,f) over
the four fixed cores is eligible, every assigned token is worth at most that
owner's core.

Then

\[
\boxed{\ \exists i\in\{0,1,2,3\}:\quad
v_i(c_i)\ge v_i(t_{i+1})\ },
\]

where indices are cyclic.  In good labels this is

\[
\exists i:\quad v_i(2i)\ge v_i((2i+3)\bmod 8).
\]

### Proof

Assume the contrary: every owner values the next owner's token more than its
own core.  Give the tokens ((3,5,7,1)) to owners ((0,1,2,3)), retaining the
same cores and floater 8.  For every owner (i), the new token is worth more
than (c_i), while its old unique-minimum token is worth less than (c_i).
Thus every owner's new bundle is strictly better than its bundle in (B).
Since (B) is eligible, the rotated state is eligible as well.  Fixed-token-
orbit maximality now says each newly assigned token is worth at most its
owner's core, contradicting all four strict inequalities.  \(\square\)

The minimized structural core contains exactly the base-eligibility premise,
the four unique-minimum inequalities, and the orbit-maximality implication for
assignment ((3,5,7,1;8)).  It contains no pair-Hall edge, global-maximality
cut, completion cut, owner wall, or cross-row clause.

Default, QF_LRA, and arithmetic-solver-2 Z3 replay the theorem from an empty
CEGAR pool in 0.0450, 0.0453, and 0.0245 seconds.

## Consequence for the cyclic pair-Hall cell

The pair-Hall antecedent is invariant under simultaneous cyclic rotation of
owners and paired goods.  Therefore any surviving counterexample may be
rotated so that

\[
v_0(0)\ge v_0(3).
\]

This is a legitimate symmetry break, not a universal owner-0 inequality.

Three exact CEGAR iterations in this canonical sector found finite-pool SAT
valuations, but every valuation had an exact EFX-completing token-orbit state.
They added 3, 1, and 4 sound whole-orbit blockers.  The canonical pool now has
159 global cuts, 78 matching cuts, and 38 whole-orbit blockers.  The sector is
not yet closed.

## Compact analytic proof of cross-row clause A0

The tracked structural core also converts clause A0 into a short exchange
argument.  Assume

\[
v_0(3)>v_0(0),\qquad
v_2(2)>v_2(3)+v_2(4).
\]

Consider the two exchange states

\[
01\mid34\mid25\mid67
\quad\text{and}\quad
01\mid35\mid24\mid67.
\]

In either state, owners 0 and 3 retain their base bundles and owner 2 strictly
improves.  If owner 1 is also eligible, global threshold maximality gives,
respectively,

\[
v_1(4)+v_2(2)\le v_1(2)+v_2(4),\qquad
v_1(5)+v_2(2)\le v_1(2)+v_2(4).
\]

If owner 1 is not eligible, comparison with base eligibility gives the same
strict conclusions.  Hence

\[
v_1(4)<v_1(2),\qquad v_1(5)<v_1(2).
\]

The pair-Hall nonedge for observer 1 assigned bundle 23 when host 2 receives
8 now forces either a threshold involving good 8 or
(v_1(2)+v_1(3)<v_1(4)+v_1(5)).  In the latter case, the companion nonedge
for observer 1 assigned bundle 45 when host 1 receives 8 forces a threshold
involving good 8.  Using (v_1(3)<v_1(2)), all cases yield

\[
v_1(8)>v_1(3).
\]

Thus the state

\[
13\mid28\mid45\mid67;\qquad f=0
\]

strictly improves owners 0 and 1 and leaves owners 2 and 3 unchanged, so it is
eligible.  Its maximality inequality selecting goods (3,2,4,6) gives

\[
v_0(3)+v_1(2)+v_2(4)+v_3(6)
\le
v_0(0)+v_1(2)+v_2(4)+v_3(6),
\]

contradicting (v_0(3)>v_0(0)).  Therefore

\[
v_0(0)\ge v_0(3)
\quad\text{or}\quad
v_2(2)\le v_2(3)+v_2(4).
\]

The standalone ten-assertion formula is independently UNSAT under default Z3,
arithmetic-solver-2 Z3, and cvc5 1.3.3, each in under 0.08 seconds.

## Claim boundary

The rotating-token lemma is human-proved and reusable beyond the pair-Hall
cell.  It does not prove the pair-Hall cell, four-agent EFX, or general EFX.
The immediate gate is the canonical sector with 38 whole-orbit blockers.

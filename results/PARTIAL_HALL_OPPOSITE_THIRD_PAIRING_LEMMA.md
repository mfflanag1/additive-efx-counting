# Opposite-third-pairing conversion lemma

## Lemma

Let valuations be positive and additive. Consider a partial allocation whose
relevant bundles are

\[
X_0=\{6,7\},\qquad X_2=\{0,4\},
\]

and the exchange allocation

\[
Z_0=\{4,7\},\qquad Z_2=\{0,6\},
\]

with every other bundle and the unallocated good unchanged. Suppose (Z) is
an eligible partial EFX allocation and the following comparison walls hold:

\[
\begin{aligned}
v_0(\{1,6\})&<v_0(\{0,7\}),\\
v_0(\{0,7\})&<v_0(\{1,4\}),\\[2mm]
v_2(\{0,3\})&<v_2(8),\\
v_2(\{0,4\})&<v_2(\{6,7\}),\\
v_2(\{1,3,4,7\})&<v_2(0),\\
v_2(\{6,7\})&<v_2(\{3,8\}),\\
v_2(\{1,8\})&<v_2(\{0,4\}).
\end{aligned}
\]

Then (Z) strictly Pareto-improves (X) for the two changing agents and
leaves every other agent unchanged. Consequently, (X) cannot maximize any
positive weighted sum of agents' utilities over eligible partial allocations.

The lemma is independent of the total number of goods: goods not displayed
above may exist and remain fixed.

## Proof

The two agent-0 walls give

\[
v_0(1)+v_0(6)<v_0(0)+v_0(7)<v_0(1)+v_0(4),
\]

so cancellation yields (v_0(6)<v_0(4)). Hence agent 0 strictly prefers
(Z_0) to (X_0).

For agent 2, multiply the five displayed walls, in order, by
(1,3,1,2,3), respectively, and add them together with four copies of the
strict positivity inequality (v_2(1)>0). Every term cancels except

\[
v_2(4)<v_2(6).
\]

Thus agent 2 strictly prefers (Z_2) to (X_2). The remaining bundles are
unchanged, completing the Pareto comparison.

## Exact certification

The lemma was extracted from the eligibility/Hall cell of the exact valuation
profile with hash
`023d18621bee45b13f735868575ef4404ea30c8e97f4b0f8cec36a0eb7fb13f9`.

- [`partial_hall_complementary_swap_gate8_frozen_cell.json`](partial_hall_complementary_swap_gate8_frozen_cell.json)
  records the deletion-irreducible nine-constraint core.
- [`partial_hall_complementary_swap_gate8_frozen_cell_farkas.json`](partial_hall_complementary_swap_gate8_frozen_cell_farkas.json)
  verifies exact coefficient cancellation and positive strict weight.
- Z3 returns `UNSAT` on the frozen cell.
- The syntax-normalized formula has SHA-256
  `868d682023f42edaa16476a54fbc8ed431bdc58c5404aba40b92e220b97f1f1d`;
  cvc5 1.3.4 independently returns `UNSAT` in 7.57 seconds.
- The standalone nine-inequality theorem formula
  [`partial_hall_opposite_third_pairing_algebra.smt2`](partial_hall_opposite_third_pairing_algebra.smt2)
  has SHA-256
  `0011cb9bc4b1bc1ef22cc1a295b863c183384bc110e92f3780f27d26476df72e`;
  both Z3 and cvc5 return `UNSAT` directly.

The positive complementary-swap-sum assumption does not occur in the minimal
core and is unnecessary for this lemma.

## Claim boundary

This proves one cap-free eligibility-wall conversion. It does not show that
every Hall obstruction contains these seven walls or that (Z) is always
eligible. The canonical radius-five improvement theorem, the one-good
completion lemma, four-agent EFX, and general EFX therefore remain open.

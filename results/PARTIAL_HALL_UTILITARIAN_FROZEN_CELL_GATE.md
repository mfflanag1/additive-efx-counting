# Normalized-utilitarian Hall selector: frozen-cell gate

## Claim boundary

The global selector is **not decided**. The exact result here eliminates two
specific combinatorial cells around positive $4\times9$ radius-one Hall
obstructions. It neither proves four-agent EFX nor refutes complete EFX.

For the canonical partial allocation

\[
X=(\{6,7\},\{1,2,3\},\{0,4\},\{5\}),\qquad f=8,
\]

write

\[
\Phi(X)=\sum_i \frac{v_i(X_i)}{v_i(M)}.
\]

Annealing produced a radius-one Hall obstruction whose score is
`0.9985823876150579` times the maximum over all eligible one-floater states.
The frozen-cell decision retains exactly:

1. the seed's eligible partial states and one strict violated comparison for
   every ineligible state;
2. the seed's radius-one EFX edge graph; and
3. the requirement that $X$ weakly maximize $\Phi$ over every retained
   eligible state.

This is a rational QF_LRA problem. Z3 returns `UNSAT` in 0.39 seconds after
the cell is constructed, and an independent cvc5 replay returns `UNSAT` in
2.01 seconds. The extracted core has five constraints.

## Five-inequality core

Let $v_i(S)=\sum_{g\in S}v_i(g)$. The core is:

\[
\begin{aligned}
v_1(2)&>0,\\
v_2(3)&>0,\\
v_1(\{1,2,3\})&<v_1(\{0,4\}),\\
v_1(\{0,2,4\})&<v_1(\{1,8\}),\\
\Phi(X)&\ge
\Phi(\{6,7\},\{1,8\},\{0,3,4\},\{5\};f=2).
\end{aligned}
\]

The first strict comparison and positivity give

\[
v_1(\{1,2,3\})<v_1(\{0,4\})+v_1(2)
<v_1(\{1,8\}).
\]

Also

\[
v_2(\{0,4\})<v_2(\{0,3,4\}).
\]

Agents 0 and 3 have unchanged bundles in the rival state. The rival
therefore has strictly larger normalized-utilitarian score, contradicting
the final inequality. This is a human-checkable proof of the frozen-cell
UNSAT verdict.

## Extracted completion-or-improvement lemma

The core lifts beyond the single frozen truth assignment. Under base
eligibility and 13 deletion-irreducible supporting edge comparisons, every
positive normalized valuation profile has at least one of the following:

1. the direct complete EFX allocation
   $(\{6,7\},\{1,2,3\},\{0,4,8\},\{5\})$ with the identity matching;
2. the transfer-and-rematch complete EFX allocation
   $(\{6,7\},\{1,3,8\},\{0,2,4\},\{5\})$, with agents 1 and 2
   receiving the opposite middle bundles; or
3. the eligible partial allocation
   $(\{6,7\},\{1,8\},\{0,3,4\},\{5\});f=2$, with strictly larger
   normalized-utilitarian potential.

The proof is the two-comparison case split exposed above. The 13 retained
support comparisons ensure that crossing either wall supplies all remaining
EFX edges for the corresponding completion; if neither wall is crossed,
they ensure the rival is eligible and the five-inequality argument makes it
strictly better. The support is deletion-irreducible under the extraction
order, not claimed minimum-cardinality. Z3 and cvc5 independently return
`UNSAT` on the negation of this trichotomy.

Abstracting the labels gives a cap-free lemma for arbitrary numbers of
agents and goods with nonnegative additive valuations: the
[two-wall Hall conversion lemma](PARTIAL_HALL_TWO_WALL_CONVERSION_LEMMA.md).
It isolates the remaining global task sharply: prove that every relevant
Hall-deficient cell supplies the lemma's three support conditions, or cover
the exceptions with additional conversion types.
An exact six-profile corpus audit finds two gates on the best near-maximal
profile but covers only that one profile; the known Pareto-maximal
obstruction is outside this conversion type.

The second frozen cell yields a distinct cap-free
[six-wall replacement lemma](PARTIAL_HALL_SIX_WALL_REPLACEMENT_LEMMA.md).
Six bundle comparisons imply that replacing one allocated good by the
floater strictly improves its owner; if the replacement state is eligible,
it Pareto-dominates the base. This explains the eight-constraint core but
does not yet connect every failed wall to a complete allocation.

The original Pareto-maximal obstruction requires a third mechanism. Its
complete comparison cell is excluded by a
[three-rival weighted cycle](PARTIAL_HALL_THREE_RIVAL_WEIGHTED_CYCLE.md):
a deletion-irreducible 25-constraint core has an exact integer-scaled
Farkas certificate, proving that the base cannot weakly beat all three
eligible rivals. This is fixed to the nine-good cell rather than cap-free.

The boundary is structurally informative. In the seed, both strict
comparisons and $v_2(3)>0$ have one-unit integer gaps. Moving one unit of
agent 1's value from good 8 to good 2 flips the two comparisons, but exact
enumeration immediately produces three radius-one EFX completions. An
exhaustive second-transfer search (4,352 candidates, deltas through 16)
found no nontrivial way to cross that wall while retaining the obstruction.

## Artifacts and replay

- [`partial_hall_utilitarian_maximality_anneal_seed17_cont117.json`](partial_hall_utilitarian_maximality_anneal_seed17_cont117.json)
  is the near-maximal obstruction.
- [`partial_hall_utilitarian_frozen_cell_seed17_cont117_core.json`](partial_hall_utilitarian_frozen_cell_seed17_cont117_core.json)
  records the exact five-constraint core.
- [`partial_hall_utilitarian_frozen_cell_seed17_cont117_core.smt2`](partial_hall_utilitarian_frozen_cell_seed17_cont117_core.smt2)
  is the tracked exact formula, SHA-256
  `f3a949008774ca2040fd0271d376eb53f4f240645a8d635ad6361af366d69cce`.
- [`partial_hall_utilitarian_frozen_cell_seed17_cont117_core_cvc5.json`](partial_hall_utilitarian_frozen_cell_seed17_cont117_core_cvc5.json)
  records the independent cvc5 `UNSAT` replay of the syntax-normalized
  formula, SHA-256
  `40b596a41f323a01481230fbd0f922d17562b331211e57480d35b0131bc424cc`.
- [`partial_hall_cell_crossing_cont117_1_8_2_1.json`](partial_hall_cell_crossing_cont117_1_8_2_1.json)
  is the exhaustive two-transfer boundary search.
- [`partial_hall_completion_improvement_lemma_seed17.json`](partial_hall_completion_improvement_lemma_seed17.json)
  records the 13-support analytic lemma. Its standalone Z3 formula has
  SHA-256
  `b51fdacb52db15ad0866e9be4c271c88628a3c518dc607bc3876a7e292a70514`;
  the syntax-normalized cvc5 formula has SHA-256
  `d68945cb092da4f517786d6bf448bda3e0b52de9c15768006aabf05517c053fb`.

Rebuild the exact core:

```sh
python tracks/parkability/decide_partial_hall_utilitarian_frozen_cell.py \
  --seed results/partial_hall_utilitarian_maximality_anneal_seed17_cont117.json \
  --output /tmp/frozen-cell.json \
  --smt2-output /tmp/frozen-cell.smt2 \
  --timeout-seconds 600 --track-unsat-core
```

The next proof target is a finite family of clauses of this form: every
radius-one Hall-obstruction cell either exposes a completion edge or an
eligible Pareto-improving rival. A cover of all cells would prove the
selector; one satisfiable frozen cell would refute it.

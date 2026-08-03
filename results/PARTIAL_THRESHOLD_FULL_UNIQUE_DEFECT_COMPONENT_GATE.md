# Full unique-defect connected-component gate

## Exact correction

No fixed radius-three gradient lemma is valid, even in the narrowest dominant
four-agent branch.

Let \((X,\{f\})\) be a positive-additive EFX-with-charity state. Suppose its
optimal absorption candidate uses the identity matching, has exactly one
negative slack, and has a full Hall witness: nobody accepts the bad agent's
bundle. One might hope that some eligible state changing at most three item
labels must improve the lexicographic extremum \((\Theta,\Lambda)\).

The exact profile below refutes that statement:

\[
V=\begin{pmatrix}
23&171&39&129&183&72&127&142&15\\
250&51&195&53&129&107&105&112&39\\
7&1&247&110&118&13&164&44&88\\
240&191&1&207&98&44&59&159&24
\end{pmatrix}.
\]

Take charity good 1 and bundle masks \((448,48,12,1)\). The optimal blocked
candidate has host 3, unique bad agent 1, full Hall witness, and signature

\[
\left(-\frac{14}{1041},\frac{101}{901},
      \frac{35}{264},\frac{71}{341}\right).
\]

Exhausting every eligible state whose owner/charity label vector differs in
one, two, or three positions finds no strict improvement of
\((\Theta,\Lambda)\). This includes every charity swap, one-good transfer,
two-good swap, and arbitrary simultaneous three-good relabeling.

The witness was found after 3,410 accepted mutations constrained to retain
the full/unique-defect premise and the absence of the standard one- and
two-good move menu. A corrected final replay exhausts all simultaneous
relabelings through radius three, including non-swap two-good paths. It is
replayed exactly by
`test_unique_defect_radius3_gradient.py`.

## First escape

The first improving radius is four. Relabel goods \((0,3,4,8)\) from slots
\((3,2,1,0)\) to \((1,3,3,2)\), producing masks

\[
(192,33,260,24)
\]

with charity good 1 unchanged. This state is EFX with charity and raises
\(\Theta\) by

\[
\frac{56,811,503}{319,837,881}.
\]

It is also directly absorbable, with signature

\[
\left(\frac{65}{1023},\frac{59}{901},
      \frac{37}{347},\frac{43}{198}\right).
\]

The four changed goods form one transfer component spanning all four agents.
Thus the failure does not weaken the global-extremum program; it determines
the necessary scale of its move-completeness lemma.

The champion bridge gives a second, conceptually cleaner radius-four escape
for the same profile. The forced champion edge from bad agent 1 to host 3
discards \(f\), so agent 1 ordinarily envies bundle 3. Conversely, agent 3
champions bundle 1 using desired set \(\{1,4\}\) and discarding good 5. The
ordinary-envy/champion 2-cycle produces the EFX-with-charity state

\[
(448,1,12,18),\qquad f'=5.
\]

It Pareto-improves the owner-utility vector from
\((284,236,357,240)\) to \((284,250,357,289)\), raises \(\Theta\) by
\(22288/354981\), and is directly absorbable with signature

\[
\left(\frac{49}{1023},\frac{101}{901},
      \frac{35}{264},\frac{140}{1041}\right).
\]

Thus generalized championship reconstructs an improving connected component
that the bounded item-move menu could not see. The exact replay is included
in the radius-three counterexample test.

## Surviving analytic target

The full-witness proof must allow a connected transfer component of arbitrary
item radius, although for four agents it spans at most four owner vertices:

> At a blocked full/unique-defect state, the Hall-wall dependencies either
> produce an eligible connected transfer component with positive total
> normalized owner-threshold gain, or a threshold-neutral component that
> strictly improves the matched-slack signature.

This is the full/unique-defect specialization of the existing
augmenting-component-cycle alternative. The correct proof unit is therefore
wall cancellation around owner vertices, not enumeration by the number of
goods moved. Multiple goods on the same component edge may be required to
preserve EFX eligibility.

The next analytic task is to aggregate each source--target transfer by its
net owner-threshold marginal, cancel internal wall terms at owner vertices,
and use the strict Hall crossing to make the component's total normalized
gain positive. A fixed-radius strengthening is now retired.

The general
[`transfer-component hybrid wall lemma`](GENERAL_TRANSFER_COMPONENT_HYBRID_WALL_LEMMA.md)
now proves the exact decomposition needed for this step: potential gain is
component-additive, and every failed hybrid inequality crosses the selected
component cut. Its crossing-wall polarity formula additionally labels every
dependency by a strict threshold-change sign in the blocking row. What
remains is to cancel these row-labeled signs while retaining positive total
owner gain.

The
[`unique-defect champion bridge`](UNIQUE_DEFECT_CHAMPION_BRIDGE_LEMMA.md)
supplies a second construction language: the bad agent necessarily
\(f\)-champions the host, with either an ordinary envy edge or a nonempty
released bottom bundle. The next proof should use generalized-champion cycles
to build an EFX-preserving component and the signed-wall lemma to certify its
extremal improvement. The component must preserve charity cardinality and have
nonnegative total threshold change; Pareto improvement by itself is not
enough. The exact distinction and a local counterexample are recorded in the
[`reciprocal-champion threshold gate`](RECIPROCAL_CHAMPION_THRESHOLD_GATE.md).

## Claim boundary

The counterexample refutes only bounded local-gradient lemmas. Its radius-four
escape is constructive evidence, not a proof that every full/unique-defect
state has a connected improving component. Four-agent and general additive
EFX remain unproved.

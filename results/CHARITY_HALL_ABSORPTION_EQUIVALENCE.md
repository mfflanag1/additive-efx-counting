# Charity Hall-absorption equivalence

## Exact equivalence

Let \((X,P)\) be an EFX allocation with charity for \(n\) positive-additive
agents, so

\[
v_i(X_i)\geq v_i(P)\qquad(i\in N).
\]

Fix a charity good \(f\in P\) and a host bundle \(h\). Form the complete
allocated-bundle partition

\[
Y_h=X_h+f,\qquad Y_j=X_j\quad(j\ne h),
\]

and leave \(P'=P-f\) in charity. Construct a bipartite graph between agents
and the \(n\) bundles. Agent \(i\) accepts bundle \(Y_j\) exactly when

\[
v_i(Y_j)\geq
\max\!\left\{
v_i(P'),
\max_{k\ne j}\left(v_i(Y_k)-\min_{g\in Y_k}v_i(g)\right)
\right\}. \tag{1}
\]

Then \(Y\) can be assigned to the agents to obtain an EFX allocation with
charity \(P'\) if and only if this graph has a perfect matching.

## Proof

If the graph has a perfect matching, assign each agent her matched bundle.
The second term on the right side of (1) gives every ordered EFX comparison,
and the first term gives collective dominance over the remaining charity.
Thus the matched allocation is EFX with charity \(P'\).

Conversely, any assignment of the bundles that is EFX and dominates \(P'\)
satisfies both inequalities in (1) for every assigned agent-bundle pair.
Those \(n\) pairs form a perfect matching. \(\square\)

## Bottleneck form

Define normalized absorption-edge scores

\[
s^{f,h}_{ij}
=\frac{
v_i(Y_j)-
\max\!\left\{
v_i(P-f),
\max_{k\ne j}\tau_i(Y_k)
\right\}
}{v_i(M)}
\]

and the best absorption margin

\[
\beta(X,P)=
\max_{\substack{f\in P,\ h\in N\\
\pi:N\to N\ {\rm bijective}}}
\min_{i\in N}s^{f,h}_{i,\pi(i)}.
\]

The charity can be reduced by one good exactly when \(\beta(X,P)\geq0\).
If \(\beta(X,P)<0\), choose an optimizing \(f,h,\pi\) and apply the
bottleneck Hall-cut normal form to its score matrix. Every obstruction is
therefore an equality edge across an inclusion-minimal critical cut, followed
by either proper-cut factorization or expansion.

For proof progress, refine \(\beta\) to the lexicographically maximum sorted
vector \(\Lambda(X,P)\) of all \(n\) matched slacks. Its first coordinate is
\(\beta\), so the absorption criterion is unchanged. Unlike the scalar
margin, \(\Lambda\) strictly improves when one tight matched edge improves
and every other matched edge is preserved. See
`PARTIAL_CHARITY_LEXICOGRAPHIC_BOTTLENECK_LEMMA.md`.

When \(P=\{f\}\), the charity term is zero and this specializes to the
one-floater completion graph used in the four-agent program.

## Unified extremal target

At a fixed charity cardinality \(p\), select an EFX-with-charity state
lexicographically as follows:

1. maximize normalized owner-threshold potential \(\Theta(X,P)\);
2. among those maxima, maximize the finite lexicographic absorption signature
   \(\Lambda(X,P)\).

The charity/minimum exchange lemma shows that every eligible exchange of a
charity good with an owner minimum remains on the first plateau. Hence the
single missing theorem is:

> **Absorption-gradient lemma.** If \(P\ne\varnothing\) and
> \(\Lambda_1(X,P)<0\), some eligible exchange either strictly increases
> \(\Theta\), or preserves \(\Theta\) and strictly increases \(\Lambda\).

The selected state would contradict this lemma unless
\(\Lambda_1(X,P)=\beta(X,P)\geq0\). One good could then be absorbed, and induction on
\(|P|\) would produce a complete EFX allocation.

The owner-exchange plateau lemma widens the admissible move family: every
eligible cycle in which each selected owner receives a weakly preferred good
also remains on the same global \(\Theta\)-plateau. The live gradient target
therefore allows both charity/minimum exchanges and owner-Pareto exchange
cycles before seeking a strict increase in \(\Lambda\).

Its equality case also imposes a limitation: every strict owner-Pareto
plateau cycle only permutes unique owner-minimum tokens over fixed cores.
Consequently the complete extremal alternative must additionally allow an
eligible connected transfer union with positive *total* \(\Theta\)-gain,
even if one participating owner loses. Global \(\Theta\)-maximality rules out
that outcome; plateau maximality of \(\Lambda\) rules out the token-exchange
outcome. More precisely, lexicographic maximality of \(\Lambda\) lets the
proof improve one tight matching edge at a time. A proof must derive one of
the two extremal contradictions from the critical Hall walls.

For four agents, the known one-unallocated-good theorem starts the induction
at \(p=1\), so the \(p=1,n=4\) specialization would prove complete
four-agent additive EFX. For arbitrary \(n\), the known EFX-with-charity
theorem starts with \(p<n\), so the full lemma would prove general additive
EFX.

## Initial adversarial evidence

The exact scanner
tracks/parkability/scan_charity_threshold_absorption.py enumerates every
EFX-with-charity state at a fixed charity cardinality, then exactly computes
all global \(\Theta\)-maximizers and their best rational absorption margin.
The selector survives:

- all 47 stored hard four-agent profiles at charity size two;
- all 30 of those profiles admitting a charity-size-three state;
- 199 of 199 eligible random \(4\times8\) profiles at charity size two; and
- 22 of 22 eligible random \(5\times8\) profiles at charity size two.

Every surviving best margin in the two hard-corpus scans is strictly
positive, not merely zero. These are finite falsification tests. They neither
prove the selector nor show that the local absorption-gradient move exists.

The random \(4\times8\) scan also contains selector boundaries with best
margin exactly zero. Around the first such boundary, every one of the 288
one-entry replacements in the integer box \(\{1,\ldots,10\}\) remains
nonnegative. In the hard 47-profile charity-size-two scan, exactly one profile
has blocked global threshold maxima: 2 of its 24 maximizers are blocked, and
each reaches one of the other 22 absorbing maximizers by a single eligible
owner-minimum/charity swap. At charity size three, every maximum in every
profile admitting such a state is already absorbing.

A separate simulated-annealing falsification pass began at a zero-margin
\(4\times8\), charity-size-two boundary and evaluated 241 exact selector
profiles in the positive integer box \(\{1,\ldots,10\}\). Its best margin
remained zero and it found no negative selector profile. This is heuristic
adversarial evidence, not an exhaustive neighborhood theorem.

The next falsification layer checked zero-margin five-agent boundaries at
charity sizes two and three, evaluating another 262 exact adversarial
profiles without finding a negative margin. Seven complete row-normalized
integer domains were also exhausted: 811,315 profiles total, including the
full \(3\times4\) cap-three/one-charity and \(3\times5\)
cap-two/two-charity boxes. All 680,109 profiles admitting an
EFX-with-charity state had nonnegative selected absorption margin. Of the
full domains, 153,675 profiles attain margin exactly zero. These are exact
finite theorems only; they do not imply the unrestricted selector.

These sharper checks support the local-gradient form rather than merely the
existential selector, but remain finite evidence.

## Claim boundary

The matching equivalence and bottleneck reduction are proved. The
absorption-gradient lemma is not proved; it is now the common explicit
breakthrough gate rather than two separate informal goals.

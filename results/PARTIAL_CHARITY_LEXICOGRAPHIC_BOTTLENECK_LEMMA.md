# Charity lexicographic bottleneck lemma

## Definition

Fix an EFX-with-charity state \((X,P)\). For every choice of charity good
\(f\), host bundle \(h\), and perfect assignment \(\pi\) of the resulting
bundles, let

\[
\sigma^{f,h,\pi}(X,P)
=\operatorname{sort}_{\uparrow}
\bigl(s^{f,h}_{i,\pi(i)}:i\in N\bigr)
\]

be the vector of its normalized acceptance slacks in nondecreasing order.
Define the **lexicographic absorption signature**

\[
\Lambda(X,P)=\max_{\mathrm{lex},,f,h,\pi}
\sigma^{f,h,\pi}(X,P).
\]

The first coordinate of \(\Lambda\) is the ordinary best bottleneck margin
\(\beta(X,P)\).

## Lemma 1: exact absorption criterion

One charity good can be absorbed if and only if
\(\Lambda_1(X,P)\geq0\).

### Proof

All coordinates of one candidate signature are nonnegative exactly when its
matching consists entirely of acceptance edges. Since the coordinates are
sorted, this is equivalent to its first coordinate being nonnegative.
Maximizing that first coordinate over the same finite candidate set gives the
ordinary bottleneck margin. \(\square\)

## Lemma 2: tight-edge improvement

Let a candidate \((f,h,\pi)\) attain \(\Lambda(X,P)\), and label its \(n\)
matched slacks by agent. Suppose an eligible fixed-charity-cardinality move
produces \((X',P')\) and a corresponding absorption candidate whose matched
slacks \(s'_i\) satisfy

\[
s'_i\geq s_i\quad\text{for every }i,
\qquad
s'_j>s_j\quad\text{for some }j.
\]

Then

\[
\Lambda(X',P')>_{\rm lex}\Lambda(X,P).
\]

### Proof

If labeled coordinates are increased coordinatewise and at least one is
increased strictly, every sorted order statistic is weakly increased and at
least one is increased strictly. Hence the new candidate's sorted signature
strictly lexicographically dominates the old optimal signature. The optimum
\(\Lambda(X',P')\) weakly dominates that candidate. \(\square\)

The useful special case is when one currently smallest matched slack is
strictly improved and no other matched slack falls. This reduces the
multiplicity of the current bottleneck level even when another edge remains
tight; a scalar \(\beta\) would record no progress, while \(\Lambda\) does.

## Lemma 3: critical-cut form at the first coordinate

Let \(\lambda=\Lambda_1(X,P)<0\), and use a candidate attaining \(\Lambda\).
The weak graph of edges with slack at least \(\lambda\) has a perfect matching,
while the strict graph of edges with slack greater than \(\lambda\) has none.
Consequently every inclusion-minimal strict Hall witness has the bottleneck
Hall-cut normal form, and every weak perfect matching crosses that cut through
at least one equality edge of value \(\lambda\).

### Proof

The chosen matching lies in the weak graph. If the strict graph had a perfect
matching, its minimum slack would exceed \(\lambda\), contradicting maximality
of the first coordinate. Hall's theorem and the bottleneck Hall-cut lemma now
apply. \(\square\)

## Strengthened extremal selector

At fixed charity cardinality, select an EFX-with-charity state by:

1. maximizing normalized owner-threshold potential \(\Theta\); and
2. subject to that, maximizing the full vector \(\Lambda\), not only
   \(\beta=\Lambda_1\).

If \(\Lambda_1<0\), an eligible move contradicts this selection whenever it
either has positive total \(\Theta\)-gain, or preserves \(\Theta\) and weakly
preserves every matched slack of a \(\Lambda\)-optimal absorption candidate
while strictly improving one. This is the sharpened absorption-gradient gate.

The lexicographic refinement removes a genuine proof nuisance: proper Hall
cuts can leave several equality edges at the same bottleneck value. It is no
longer necessary to improve all of them simultaneously merely to register
progress. They may be eliminated one at a time, provided previously matched
slacks do not fall.

## Proper-cut one-edge upgrade corollary

Let \(S\) be an inclusion-minimal strict Hall witness and
\(T=N_{>\lambda}(S)\). In the factorizing case of the bottleneck Hall-cut
lemma, choose a crossing equality edge \((a,w)\) with \(a\in S\),
\(w\notin T\), a strict matching from \(S-a\) onto \(T\), and a residual
matching from the remaining agents to the remaining bundles so that their
union attains \(\Lambda\).

If an eligible state move strictly raises the slack of \((a,w)\) and weakly
preserves the slack of every other edge in this factorized matching, then it
strictly raises \(\Lambda\). This follows immediately from Lemma 2. If the
residual factorization does not exist, the residual Hall witness expands
\(S\) to a strictly larger deficient set. Hence a proof may alternate between
single crossing-edge upgrades and strict cut expansion; it never needs to
repair all proper-cut equality edges simultaneously.

## Claim boundary

The three lemmas above are cap-free and valid for arbitrary positive-additive
instances. They refine the extremal objective and the critical-cut reduction.
They do **not** prove that a tight-edge-improving eligible move exists, so they
do not resolve four-agent or general EFX.

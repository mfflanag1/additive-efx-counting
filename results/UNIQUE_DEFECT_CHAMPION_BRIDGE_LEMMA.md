# Unique-defect champion bridge lemma

## Statement

Let \(X=(X_1,\ldots,X_n)\) be an EFX allocation and let \(f\) be an
unallocated good. Fix a host \(h\), put

\[
S=X_h\cup\{f\},
\]

and suppose that assigning the augmented bundles by identity creates exactly
one EFX defect, at agent \(b\). Then \(b\ne h\), agent \(b\) is the unique
strong envier of \(S\), and \(b\) champions \(h\) with respect to \(f\).

More precisely, there is a nonempty discard set \(D\subsetneq S\) such that

\[
T=S\setminus D,qquad v_b(T)>v_b(X_b),
\]

and no agent strongly envies \(T\). The discard has exactly one of two forms:

1. \(D=\{f\}\), in which case \(T=X_h\) and \(b\) ordinarily envies
   \(h\); or
2. \(D\subseteq X_h\), in which case \(f\in T\), the champion edge genuinely
   \(f\)-decomposes the host, and the nonempty bottom bundle \(D\) is
   released.

The statement holds for every number of agents and arbitrary monotone
valuations for which strong envy is defined; additivity is needed only to
identify the identity defect with the deletion threshold used in the current
Hall formulation.

## Proof

The host cannot be the defective agent. Her own bundle gains \(f\), while
every competing bundle is unchanged, so all of her old EFX inequalities
remain valid. Hence \(b\ne h\).

For additive valuations, the strong-envy threshold of \(S\) is

\[
\tau_i(S)=\max_{g\in S}v_i(S-g).
\]

The original allocation is EFX, and only the host bundle changed. Therefore
the unique negative identity slack says exactly that \(b\) strongly envies
\(S\), while no other agent does.

Because \(b\) strongly envies \(S\), there is a proper subset of \(S\) that
she envies. Choose an inclusion-minimal envied subset \(T\subsetneq S\), and
put \(D=S\setminus T\). Minimality implies that \(b\) does not strongly envy
\(T\): removing any good from \(T\) destroys her envy.

No other agent strongly envies \(T\). Otherwise some agent \(i\ne b\) and
good \(g\in T\) would satisfy

\[
v_i(T-g)>v_i(X_i).
\]

Monotonicity and \(T-g\subseteq S-g\) would then give

\[
v_i(S-g)>v_i(X_i),
\]

contradicting that \(b\) is the unique strong envier of \(S\). Thus \(b\) is
most envious of \(S\), which is precisely the champion relation
\(b\xrightarrow{f}h\), with discard set \(D\). The set \(D\) is nonempty
because \(T\) is proper.

It remains to classify whether \(f\) is discarded. If \(f\notin D\), then
\(D\subseteq X_h\), giving case 2. Suppose instead that \(f\in D\), so
\(T\subseteq X_h\). If \(T\ne X_h\), choose
\(g\in X_h\setminus T\). Monotonicity gives

\[
v_b(X_h-g)\geq v_b(T)>v_b(X_b),
\]

so \(b\) strongly envies the original bundle \(X_h\), contradicting that
\(X\) is EFX. Therefore \(T=X_h\) and \(D=\{f\}\), proving case 1.
\(\square\)

## Consequence for the four-agent full witness

The dominant Hall branch is no longer merely an acceptance-graph pattern.
Its unique bad--host arc is a genuine generalized-champion edge. If case 1
holds, the branch already contains an ordinary envy edge. If case 2 holds, it
contains a nonempty released bottom bundle to feed a Pareto-improvable
generalized-champion cycle.

Every target bundle also has at least one incoming \(f\)-champion by the
standard most-envious-agent argument. Choosing incoming champion edges
therefore yields a directed champion cycle. The remaining four-agent proof
task is now finite at the owner-graph level: determine how the forced edge
\(b\xrightarrow{f}h\), the full Hall witness at bundle \(b\), and the bottom
bundle released above force either a Pareto-improvable edge set or the signed
transfer-component contradiction.

This is complementary to the transfer-component hybrid wall lemma. Champion
edges make EFX-preserving component construction possible; the component
lemma supplies the extremal contradiction once the constructed endpoint has
positive threshold gain.

## Claim boundary

The champion bridge and discard dichotomy are proved. The existence of a
Pareto-improvable cycle using the forced edge is not proved. Consequently the
lemma does not resolve four-agent or general additive EFX.

## Primary source for terminology

Berger, Cohen, Feldman, and Fiat, *(Almost Full) EFX Exists for Four Agents
(and Beyond)*, AAAI 2022 / arXiv:2102.10654, Definitions 2.3 and 3.1--3.3.

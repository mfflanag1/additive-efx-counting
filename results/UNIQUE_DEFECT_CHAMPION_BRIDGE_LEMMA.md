# Unique-defect two-source champion bridge lemma

## Statement

Let \(X=(X_1,\ldots,X_n)\) be an EFX allocation, let \(f\) be an
unallocated good, fix a host \(h\) with nonempty bundle, and put
\(S=X_h\cup\{f\}\). Suppose assigning the augmented bundles by identity
creates exactly one EFX defect, at agent \(b\). Then:

1. \(b\ne h\), and \(b\) strongly envies \(S\);
2. no agent outside \(\{b,h\}\) strongly envies \(S\); and
3. some agent in \(\{b,h\}\) is a most-envious source for \(S\), and hence
   \(f\)-champions \(h\).

If the source is \(b\), let \(T=S\setminus D\) be its desired bundle. Its
nonempty discard has exactly one of two forms:

1. \(D=\{f\}\), in which case \(T=X_h\) and \(b\) ordinarily envies \(h\);
   or
2. \(D\subseteq X_h\), in which case \(f\in T\) and a nonempty bottom
   bundle from \(X_h\) is released.

If the host strongly envies \(S\), additivity gives the exact alternative

\[
v_h(f)>\min_{x\in X_h}v_h(x). \tag{1}
\]

Thus the bridge has two possible sources. The unique bad identity agent is
not universally forced to be the champion.

## Proof

The host cannot be the defective identity agent. Her assigned bundle gains
\(f\), while every competing bundle is unchanged, so her old EFX
inequalities remain valid. Hence \(b\ne h\).

Only the host bundle changed. The negative identity slack of \(b\) therefore
says that \(b\) strongly envies \(S\). Every external agent
\(i\notin\{b,h\}\) retains a valid identity edge whose comparisons include
\(S\), so no such agent strongly envies \(S\). The identity test does not
make the analogous statement about \(h\), because the host is assigned
\(S\), rather than her old bundle \(X_h\).

Because \(b\) strongly envies \(S\), some proper subset of \(S\) is envied.
Choose, across all agents, an inclusion-minimal proper subset
\(T\subsetneq S\) that some agent \(j\) envies. No agent strongly envies
\(T\): otherwise deleting the witnessing good would give a smaller envied
subset. If \(j\notin\{b,h\}\), choose any \(x\in S\setminus T\). Then
\(T\subseteq S-x\), so monotonicity implies that \(j\) strongly envies
\(S\), a contradiction. Hence \(j\in\{b,h\}\), proving the two-source
champion claim.

Suppose \(j=b\), and put \(D=S\setminus T\). The set \(D\) is nonempty. If
\(f\notin D\), then \(D\subseteq X_h\), giving case 2. If \(f\in D\), then
\(T\subseteq X_h\). Were \(T\ne X_h\), choosing
\(g\in X_h\setminus T\) would give

\[
v_b(X_h-g)\ge v_b(T)>v_b(X_b),
\]

contradicting EFX of \(X\). Therefore \(T=X_h\) and \(D=\{f\}\), giving
case 1.

Finally, for positive-additive valuations,

\[
\tau_h(S)=\max\!\left\{v_h(X_h),
v_h(X_h)+v_h(f)-\min_{x\in X_h}v_h(x)\right\}.
\]

Consequently \(h\) strongly envies \(S\) relative to her old bundle exactly
when (1) holds. \(\square\)

## Consequence for the extremal route

The bad-source branch retains the discard dichotomy and reciprocal-champion
analysis, now explicitly as a conditional branch. For a nonsingleton host,
the new
[`host-interference localization lemma`](HOST_INTERFERENCE_LOCALIZATION_LEMMA.md)
shows that after releasing one host minimum the incoming blocker is exactly
\(b\): either \(b\) becomes a generalized champion source or the blocked
move has strictly positive threshold gain. For a singleton host, the
singleton-chain lemma propagates the charity wall to a nonsingleton positive
incoming-target wall and generalized champion edge.

An exact positive-additive \((4,8)\) state shows that the correction is
necessary: it has a unique bad identity agent that does not champion the
augmented host, while the host strongly envies that set and self-champions.
The state lies strictly below absorbing global \(\Theta\)-maximizers. See
[`unique_defect_bad_champion_local_counterexample.json`](unique_defect_bad_champion_local_counterexample.json).

## Claim boundary

The two-source bridge and the bad-source discard dichotomy are proved. A
bad-to-host champion edge is conditional, not forced. Neither branch has yet
been shown to terminate in a nonnegative-threshold eligible component, so
this lemma does not resolve four-agent or general additive EFX.

## Primary source for terminology

Berger, Cohen, Feldman, and Fiat, *(Almost Full) EFX Exists for Four Agents
(and Beyond)*, AAAI 2022 / arXiv:2102.10654, Definitions 2.3 and 3.1--3.3.

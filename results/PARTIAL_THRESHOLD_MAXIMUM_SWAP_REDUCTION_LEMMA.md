# Threshold-maximum floater-swap reduction

## Proved cap-free lemma

Let \((X,f)\) be an eligible one-floater EFX allocation for positive-additive
agents, and define

\[
\Theta(X,f)=\sum_i\frac{\tau_i(X_i)}{v_i(M)},
\qquad
\tau_i(B)=v_i(B)-\min_{g\in B}v_i(g),
\]

with \(\tau_i(\varnothing)=0\).  Suppose \((X,f)\) globally maximizes
\(\Theta\) among eligible one-floater EFX allocations.  Choose an owner
\(s\) and an owner-minimum good

\[
g\in\arg\min_{x\in X_s}v_s(x).
\]

Form \((Y,g)\) by putting \(f\) in bundle \(s\), removing \(g\), and leaving
every other bundle unchanged.  If \((Y,g)\) is eligible one-floater EFX, then

\[
\Theta(Y,g)=\Theta(X,f).
\]

Thus every eligible owner-minimum floater swap out of a global threshold
maximum remains on the same global maximum plateau.  If \(X_s\setminus\{g\}\)
is nonempty, the incoming floater is an owner-minimum good of its new bundle:

\[
v_s(f)\le
\min_{x\in X_s\setminus\{g\}}v_s(x).
\]

The statement holds for arbitrary numbers of agents and goods.

## Proof

Write \(R=X_s\setminus\{g\}\).  Because \(g\) is owner-minimum,

\[
\tau_s(X_s)=v_s(R).
\]

For the swapped bundle,

\[
\tau_s(R\cup\{f\})
=v_s(R)+v_s(f)-\min\bigl(v_s(f),\min_{x\in R}v_s(x)\bigr)
\ge v_s(R),
\]

with the singleton case interpreted as \(\tau_s(\{f\})=0=\tau_s(\{g\})\).
Every other owner's threshold term is unchanged.  Hence
\(\Theta(Y,g)\ge\Theta(X,f)\).  Eligibility of \((Y,g)\) makes it a state in
the domain over which \((X,f)\) is globally maximal, so equality is forced.
For nonempty \(R\), equality in the displayed inequality is equivalent to
\(v_s(f)\le\min_{x\in R}v_s(x)\), proving the final assertion.

## Exact four-agent completion reduction

For an eligible state \((X,f)\), define its exact direct-completion margin

\[
H(X,f)=\max_{h,\pi}\min_i
\frac{
v_i(B^h_{\pi(i)})-
\max_{j\ne\pi(i)}\tau_i(B^h_j)
}{v_i(M)},
\]

where \(B^h\) is the complete partition obtained by inserting \(f\) into
host bundle \(h\), and \(\pi\) ranges over bijections from agents to bundle
labels.  By definition,

\[
H(X,f)\ge0
\quad\Longleftrightarrow\quad
\text{some direct insertion has an EFX perfect matching}.
\]

Choose, among global \(\Theta\)-maximizers, a state maximizing \(H\).  The
proved lemma shows that any eligible owner-minimum floater swap remains in
the primary maximum set.  Therefore the following local statement would
complete the four-agent proof:

> **Exact Hall-gradient lemma.**  If a four-agent global
> \(\Theta\)-maximizer has \(H<0\), some eligible owner-minimum floater swap
> has strictly larger \(H\).

Indeed, that swap contradicts secondary maximality.  Hence \(H\ge0\), and
the corresponding insertion and matching give a complete EFX allocation.

The Hall-gradient lemma is not proved.  It is now the precise remaining
four-agent gate; it subsumes the earlier informal finite Hall-defect order.
The cap-free
`PARTIAL_THRESHOLD_BOTTLENECK_HALL_CUT_LEMMA.md` rewrites “strictly larger
\(H\)” as a perfect matching in the successor graph of edges whose slack is
strictly above the old \(H\).  This is the preferred analytic form of the
gate.

## Exact evidence and its limit

`partial_hall_threshold_plateau_exact_path_audit.json` recomputes every Hall
margin with exact rational arithmetic on the 46-profile fixed-tie-break
failure corpus.  It finds:

- 15,557 global threshold-maximal states;
- 7,655 blocked maximum states;
- an exact strictly \(H\)-increasing owner-minimum floater-swap path from all
  7,655 blocked states to a completing maximum state;
- maximum path length two;
- all 4,848 transitions used by the originally selected 4,847 blocked states
  release an owner-minimum good and insert a new owner-minimum good; and
- none of those transitions uses a singleton source bundle: 4,845 start from
  a two-good source, two from a three-good source, and one from a four-good
  source.

Artifact SHA-256:
`16d1d9041c32278cf243462d8bea679926cced30817c21b34b9f2f53448fcdb2`.

These are finite corpus facts.  The deficient-set role of the swapped owner
is not fixed: it belongs to some minimum-cardinality Hall-deficient set in
4,684 of the 4,848 selected-path transitions, not all of them.  Consequently
the analytic proof cannot assume one designated Hall role; it must use the
full slack maximum \(H\), or derive a separate exchange when that role rule
fails.

Indeed, 145 transitions place the source owner in none of the tested Hall or
bottleneck roles (deficient set, deficient neighborhood, best host,
bottleneck observer, bottleneck assigned bundle, or bottleneck worst target).
All 145 have a two-agent/one-neighbor canonical witness and a two-good source
bundle.  Taking unions of those roles therefore does not repair a fixed-role
proof.

There is an additional important limitation: every audited profile already
has at least one completing threshold maximizer.  The path census therefore
describes the geometry of successful plateaus; it does not directly sample a
hypothetical counterexample plateau on which every threshold maximizer is
blocked.  Excluding that regime remains the entire content of the exact
Hall-gradient lemma.

## General-EFX boundary

The plateau-preservation lemma is already valid for arbitrary \(n\), but the
completion reduction uses a single charity good.  General additive EFX still
requires an invariant that absorbs one good from a charity set while keeping
the remaining charity collectively unenvied, together with a deficient-set
version of the Hall-gradient lemma.  No such arbitrary-\(n\) absorption
theorem is claimed here.

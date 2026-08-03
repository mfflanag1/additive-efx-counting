# Exact obstruction to an owner-minimum floater swap

## Statement

Let \((X,f)\) be an eligible one-floater partial EFX allocation for positive
additive valuations. Choose an owner \(q\) and an owner-minimum good
\(g\in X_q\), and let \((X',g)\) be obtained by replacing \(g\) with \(f\) in
\(q\)'s bundle.

If \(X_q\) is nonsingleton, every agent weakly prefers her old bundle to the
new floater \(g\). Consequently the new state can be ineligible only through:

1. an **incoming-target wall** for some external agent \(i\ne q\),
   \[
   v_i(X_i)<\tau_i(X_q-g+f);
   \]
2. a **source-owner shortfall** for \(q\) against some \(j\ne q\),
   \[
   v_q(X_q-g+f)<\tau_q(X_j).
   \]

Every incoming-target wall forces

\[
v_i(f)>v_i(g), \tag{1}
\]

whereas every source-owner shortfall forces

\[
v_q(f)<v_q(g). \tag{2}
\]

For a singleton source \(X_q=\{g\}\), add the possible floater wall
\(v_q(f)<v_q(g)\), which has the same sign as (2).

## Proof

For any observer \(i\) and any good \(g\in X_q\), nonsingletonness gives

\[
\tau_i(X_q)=v_i(X_q)-\min_{x\in X_q}v_i(x)\geq v_i(g).
\]

Old EFX therefore implies \(v_i(X_i)\geq v_i(g)\) for \(i\ne q\). For \(q\),
the new bundle \(X'_q\) contains a remaining good worth at least \(v_q(g)\)
and also the positive good \(f\), so \(v_q(X'_q)>v_q(g)\). Hence nobody
envies the new floater.

Only \(q\)'s bundle changes. For an external agent, all EFX comparisons
except the one targeting \(q\)'s new bundle are unchanged. For \(q\), only
the left side of her comparisons changes. This proves the exhaustive list.

Write \(R=X_q-g\). An incoming-target wall and old EFX give

\[
\tau_i(R+f)>v_i(X_i)\geq\tau_i(R+g).
\]

For fixed \(R\), the map

\[
x\longmapsto\tau_i(R+x)
=v_i(R)+\max\{v_i(x)-\min_{r\in R}v_i(r),0\}
\]

is nondecreasing in \(v_i(x)\). Its strict increase from \(g\) to \(f\)
forces (1).

For a source-owner shortfall, old EFX gives

\[
v_q(R)+v_q(f)<\tau_q(X_j)\leq v_q(R)+v_q(g),
\]

which yields (2). The singleton floater wall is itself (2). \(\square\)

## Dependency-cycle consequence

The wall types demand opposite comparisons. A failed incoming move points to
an observer who ranks the incoming floater above the released good; a failed
source move says the source owner ranks them in the reverse order. A
dependency-cycle proof must additionally show that the simultaneous union is
EFX-feasible; the opposite signs alone do not provide that missing step.

## Claim boundary

This completely classifies local swap ineligibility. It does not prove that
one swap or one dependency-cycle union is eligible.

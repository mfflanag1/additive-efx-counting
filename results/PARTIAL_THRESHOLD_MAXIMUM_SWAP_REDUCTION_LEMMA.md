# Threshold-maximum owner-minimum swap lemma

## Statement

Let \((X,f)\) be an eligible partial allocation with one unallocated good for
positive additive valuations. For each owner \(i\), write

\[
\tau_i(X_i)=v_i(X_i)-\min_{g\in X_i}v_i(g),
\qquad
\Theta(X,f)=\sum_i\frac{\tau_i(X_i)}{v_i(M)}.
\]

Assume \((X,f)\) globally maximizes \(\Theta\) among eligible one-floater
states. Choose an owner \(q\), an owner-minimum good \(g\in X_q\), and form

\[
X'_q=X_q-g+f,\qquad X'_i=X_i\ (i\ne q),\qquad f'=g.
\]

If \((X',g)\) is eligible, then

\[
\Theta(X',g)=\Theta(X,f)
\]

and \(f\) is an owner-minimum good of \(X'_q\). Thus every eligible
owner-minimum/floater swap from a global threshold maximum remains on the
same maximum plateau and creates another minimum slot.

## Proof

Put \(R=X_q-g\), and let \(r=\min_{x\in R}v_q(x)\), with \(r=+\infty\) when
\(R\) is empty. Because \(g\) is an owner minimum,

\[
\tau_q(X_q)=v_q(R).
\]

After the swap,

\[
\tau_q(X'_q)
=v_q(R)+v_q(f)-\min\{r,v_q(f)\}
\geq v_q(R)=\tau_q(X_q).
\]

Every other owner's threshold is unchanged. Hence
\(\Theta(X',g)\geq\Theta(X,f)\). Eligibility of the new state and global
maximality of the old one force equality. Therefore
\(v_q(f)=\min\{r,v_q(f)\}\), so \(f\) is a minimum of \(R+f=X'_q\).
\(\square\)

## Claim boundary

This lemma proves plateau preservation conditional on eligibility. It does
not say that any particular swap is eligible or that a sequence reaches an
EFX-completable state.

## Pareto-sensitive extremum corollary

Refine the selection rule by maximizing, among all global \(\Theta\)-maxima,
the owner-utility vector in any fixed lexicographic agent order. Then every
eligible owner-minimum/floater swap above must satisfy

\[
v_q(f)\le v_q(g).
\]

Indeed, the swap remains on the maximum \(\Theta\)-plateau by the lemma and
changes no owner's utility except \(q\)'s, whose change is
\(v_q(f)-v_q(g)\). A positive change would strictly improve the secondary
utility vector. Thus an eligible swap with \(v_q(f)>v_q(g)\) is already an
extremal contradiction; no completion or Hall-signature argument is needed.

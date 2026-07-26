# Scratch theorem: injective parking of multiple leftovers

This is a scratch extension of the generalized single-floater parking theorem.
It is not yet part of the paper.  Goods and agents are labeled, valuations are
additive and nonnegative, and EFX means EFX0.

## Setup and exact criterion

Let \(G_0\) be a set of base goods, let \(F\) be a disjoint set of leftover
goods, and let \(B=(B_1,\ldots,B_n)\) be an EFX0 allocation of \(G_0\).
Assume \(|F|\le n\).  For an observer \(k\), put
\[
\tau_k(S)=
\begin{cases}
v_k(S)-\min_{g\in S}v_k(g),&S\ne\varnothing,\\
0,&S=\varnothing.
\end{cases}
\]
For \(f\in F\), a prospective host \(h\), and \(k\ne h\), define the
single-parking slack
\[
\sigma^f_{k,h}(B)=v_k(B_k)-\tau_k(B_h\cup\{f\}).
\]
If \(B_h\ne\varnothing\), its target threshold is equivalently
\[
\tau_k(B_h\cup\{f\})
=v_k(B_h)+\max\{0,v_k(f)-\min_{g\in B_h}v_k(g)\}.
\]
If \(B_h=\varnothing\), the threshold is \(0\), since the only target good is
\(f\).

Let \(\phi:F\hookrightarrow N\) be an injection and let \(X^\phi\) be the
complete allocation obtained by assigning \(f\) to \(\phi(f)\).  For a used
host \(k\), write \(f_k=\phi^{-1}(k)\), and define
\[
d_k(\phi)=
\begin{cases}
v_k(f_k),&k\in\operatorname{im}\phi,\\
0,&k\notin\operatorname{im}\phi.
\end{cases}
\]

**Theorem (exact injective multi-parking criterion).**
The allocation \(X^\phi\) is EFX0 if and only if
\[
\sigma^{f_h}_{k,h}(B)+d_k(\phi)\ge0
\qquad
\text{for every }h\in\operatorname{im}\phi\text{ and every }k\ne h.
\tag{1}
\]

**Proof.**
Fix an ordered observer--target pair \((k,h)\), \(k\ne h\).  If \(h\) receives
the leftover \(f_h\), then the observer's own bundle has value
\(v_k(B_k)+d_k(\phi)\), while the removal threshold of the target is
\(\tau_k(B_h\cup\{f_h\})\).  Its EFX0 inequality is therefore exactly (1).
If \(h\) receives no leftover, its target bundle remains \(B_h\).
The base EFX0 inequality gives
\(v_k(B_k)\ge\tau_k(B_h)\), and nonnegativity gives
\(v_k(B_k)+d_k(\phi)\ge v_k(B_k)\).  Thus every unfilled-target constraint
holds automatically.  These cases exhaust the ordered pairs, proving both
directions. \(\square\)

Equivalently, a chosen edge \(f\mapsto h\) must satisfy
\(\sigma^f_{k,h}(B)\ge0\) for every unused observer \(k\ne h\), while an
observer \(k\) receiving \(f_k\) may rescue that edge by the bonus \(v_k(f_k)\).
This coupling is why the exact criterion is not, in general, an ordinary
bipartite matching condition.

## Safe-edge matching theorem

Build a bipartite graph with left side \(F\) and right side \(N\).  Call
\((f,h)\) **safe** when
\[
\sigma^f_{k,h}(B)\ge0\qquad\text{for every }k\ne h.
\tag{2}
\]

**Theorem (safe matching suffices).**
Every matching of safe edges that saturates \(F\) gives an EFX0 allocation.

**Proof.**
For every selected edge, (2) supplies the corresponding inequalities in (1)
without using an observer bonus.  Since every \(d_k(\phi)\) is nonnegative,
(1) follows. \(\square\)

Consequently Hall's condition on the safe graph guarantees at least one EFX0
injective completion.  More strongly, if \(\mathcal M_F\) is the set of
matchings that saturate \(F\) (equivalently, size-\(|F|\) matchings), then
\[
\#\{\text{labeled EFX0 allocations}\}\ \ge\ |\mathcal M_F|.
\tag{3}
\]
Distinct matchings give distinct allocations: if two injections differ, some
labeled leftover good has a different owner.  This remains true when two
leftovers have identical value vectors.  For \(F=\varnothing\), the unique
empty matching gives the base allocation.  When \(|F|<n\), this is a
left-saturating rectangular matching count, not the permanent of the full
bipartite adjacency matrix; it becomes the usual square permanent only when
\(|F|=n\).

Safe edges are sufficient, not necessary.  For example, take two agents, base
\(B_1=\{b\},B_2=\varnothing\), and leftovers \(p,q\).  Let agent 1 value every
good at \(0\), and let agent 2 value \(b,p,q\) at \(1\).  Under
\(p\mapsto1,q\mapsto2\), the edge \((p,1)\) has
\(\sigma^p_{2,1}=-1\), but agent 2's own leftover contributes
\(d_2=1\), so (1) holds and the simultaneous allocation is EFX0.

## Universal-minimum specialization

Call a leftover \(f\) **base-universal-minimum** if
\[
v_k(f)\le v_k(g)
\qquad\text{for every observer }k\text{ and every base good }g\in G_0.
\]
No comparison with the other leftovers is required because injectivity puts at
most one leftover in each target bundle.  For such an \(f\), an edge \((f,h)\)
is safe exactly when
\[
v_k(B_k)\ge v_k(B_h)\qquad\text{for every }k\ne h.
\]
(For an empty \(B_h\), this follows from nonnegativity.)  Thus all such
leftovers have as safe hosts the base bundles unenvied by every other agent.
If there are \(u\) such hosts and \(r=|F|\le u\), (3) gives at least
\[
(u)_r=\frac{u!}{(u-r)!}
\]
labeled EFX0 allocations.  In particular, if \(B\) is envy-free, all \(n\)
hosts are safe and every injection is EFX0, giving at least
\((n)_r=n!/(n-r)!\) allocations.

The injectivity assumption is essential to these formulas.  If a host may
receive several leftovers, its target-removal threshold depends jointly on all
of them, so neither the single-edge slack nor the stated matching count applies.
Nonnegativity is also essential to the stated reduction: it is what guarantees
that an observer's assigned leftover cannot break a base EFX0 constraint toward
an unfilled target.

## Exhaustive regression

Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python artifacts/multifloater_parking/verify_small.py
```

The verifier exhausts:

- two-agent instances with up to two base goods, up to two leftovers, and
  values in \(\{0,1,2\}\);
- three-agent instances with up to one base good, up to two leftovers, and
  values in \(\{0,1\}\);
- every labeled base allocation, every injective leftover placement, and every
  EFX0 base in those ranges.

It compares (1) with the definition-faithful EFX0 predicate, checks every
safe-matching implication, matching-count lower bound, and Hall feasibility
condition, exercises empty bundles, checks the base-universal-minimum
specialization, requires an example where an observer bonus rescues an unsafe
edge, and verifies that distinct matchings always give distinct labeled
allocations.

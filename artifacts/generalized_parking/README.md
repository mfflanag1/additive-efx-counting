# Generalized parking theorem and fixed-witness certificates

This artifact gives the exact parking criterion for an arbitrary leftover good and
checks it on the six count-\(n\) matrices printed in the paper, plus the second
\((4,8)\) basin retained as an extra certificate. Agents and goods are zero-based
in `certificates.json` and in the verifier.

## Theorem

Let \(v_0,\ldots,v_{n-1}\) be additive, nonnegative valuations on a set
\(M\) of indivisible goods. For a bundle \(S\), define
\[
\tau_k(S)=
\begin{cases}
v_k(S)-\min_{g\in S}v_k(g),&S\ne\varnothing,\\
0,&S=\varnothing.
\end{cases}
\]
Thus an allocation \(X\) is EFX\(_0\) exactly when
\(v_k(X_k)\geq\tau_k(X_j)\) for every ordered pair \(k\ne j\).

Fix a good \(f\), and let \(B=(B_0,\ldots,B_{n-1})\) be an EFX\(_0\)
allocation of \(M\setminus\{f\}\). Write
\[
m_k(B_h)=\min_{g\in B_h}v_k(g),
\]
with the convention \(m_k(\varnothing)=+\infty\). For observer \(k\ne h\)
and prospective host \(h\), define the generalized parking slack
\[
\sigma^f_{kh}(B)
=v_k(B_k)-v_k(B_h)
-\max\!\left\{0,\ v_k(f)-m_k(B_h)\right\}.
\]
Let \(P^h\) be the complete allocation obtained by adding \(f\) to \(B_h\).
Then
\[
P^h\text{ is EFX}_0
\quad\Longleftrightarrow\quad
\sigma^f_{kh}(B)\geq0\quad\text{for every }k\ne h.
\]

Equivalently, put a directed edge \(k\to h\) whenever
\(\sigma^f_{kh}(B)<0\). The number of EFX\(_0\) allocations obtained by
parking \(f\) into the fixed base \(B\) is exactly the number of
indegree-zero vertices of this \(f\)-envy digraph.

### Proof

For \(k\ne h\), additivity gives
\[
\begin{aligned}
\tau_k(B_h\cup\{f\})
&=v_k(B_h)+v_k(f)
  -\min\{m_k(B_h),v_k(f)\}\\
&=v_k(B_h)+
  \max\{0,v_k(f)-m_k(B_h)\}.
\end{aligned}
\]
The identity also holds when \(B_h=\varnothing\) under the stated
\(+\infty\) convention: both sides are zero. Hence the EFX\(_0\)
constraint from a non-host observer \(k\) toward the enlarged host bundle
is exactly \(\sigma^f_{kh}(B)\geq0\).

It remains to check every ordered pair whose target is not the host.
If neither observer nor target is \(h\), both bundles are unchanged and the
constraint follows from EFX\(_0\) of \(B\). If the **host is the observer**,
say the ordered pair is \((h,j)\) with \(j\ne h\), then the target bundle is
unchanged while the host's own value changes from \(v_h(B_h)\) to
\(v_h(B_h)+v_h(f)\geq v_h(B_h)\). Its old EFX\(_0\) inequality therefore
continues to hold. These cases exhaust all ordered pairs, proving
sufficiency. Necessity follows from the observer-to-host constraints
computed in the first display. The graph-count statement follows because
different hosts give different owners to \(f\). \(\square\)

## Universal-minimum specialization

Suppose \(f\) is a universal minimum:
\[
v_k(f)\leq v_k(g)\qquad
\text{for every agent }k\text{ and every }g\ne f.
\]
Then \(v_k(f)\leq m_k(B_h)\) for every nonempty host bundle, so the surplus
term vanishes and
\[
\sigma^f_{kh}(B)=v_k(B_k)-v_k(B_h).
\]
Consequently \(P^h\) is EFX\(_0\) if and only if \(B_h\) is unenvied in
the ordinary envy graph of \(B\). The number of EFX\(_0\) parkings is
exactly the number of unenvied base bundles. In particular, if \(B\) is
envy-free, all \(n\) parkings are EFX\(_0\), yielding \(n\) distinct
allocations of the full instance. This is an at-least-\(n\) conclusion;
it does not exclude additional EFX\(_0\) allocations outside this fixed
base.

## Printed-witness certificate summary

Every recorded witness has an envy-free base and all its generalized parking
slacks are strictly positive. Only the \((6,9)\) witness has a
universal-minimum floater; the generalized theorem is essential for the other
five paper witnesses and for the extra \((4,8)\) certificate.

| certificate | cell | floater (zero-based / paper good) | base bundles (zero-based) | min base EFX slack | min base envy slack | min parking slack | universal minimum | exact EFX\(_0\) count |
|---|---:|---:|---|---:|---:|---:|:---:|---:|
| `n4_m7` | \((4,7)\) | 3 / 4 | `{0,4,5}; {2}; {6}; {1}` | 22 | 1 | 1 | no | 4 |
| `n5_m8` | \((5,8)\) | 6 / 7 | `{3}; {2}; {0}; {4}; {1,5,7}` | 22 | 3 | 3 | no | 5 |
| `n6_m9` | \((6,9)\) | 8 / 9 | `{0,1,2}; {3}; {4}; {5}; {6}; {7}` | 29 | 1 | 1 | yes | 6 |
| `n4_m8_basin1` | \((4,8)\), basin 1 | 3 / 4 | `{2}; {0,1}; {5,6,7}; {4}` | 3 | 1 | 1 | no | 4 |
| `n4_m8_basin2` | \((4,8)\), basin 2 | 7 / 8 | `{2}; {0,3,5,6}; {1}; {4}` | 9 | 1 | 1 | no | 4 |
| `n4_m9` | \((4,9)\) | 0 / 1 | `{3,5,6,7,8}; {1}; {2}; {4}` | 2 | 1 | 1 | no | 4 |
| `n4_m10` | \((4,10)\) | 5 / 6 | `{2}; {4}; {1}; {0,3,6,7,8,9}` | 6 | 1 | 1 | no | 4 |

The full observer-by-host matrices \((\sigma^f_{kh})\) are in
`certificates.json`; rows are observers, columns are hosts, and diagonal
entries are `null`.

## Reproduction

From the repository root:

```sh
python3 artifacts/generalized_parking/verify_certificates.py
```

The default command uses exact integer arithmetic and exhaustively checks all
\(n^m\) labeled allocations. It verifies both that every recorded parking is
EFX\(_0\) and that the complete EFX\(_0\) set consists of exactly those
parkings. A fast check of only the theorem hypotheses and recorded slack
matrices is:

```sh
python3 artifacts/generalized_parking/verify_certificates.py --skip-exact
```

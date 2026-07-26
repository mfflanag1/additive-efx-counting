# Scratch theorem: full-dimensional chambers of exact EFX0 sets

This scratch artifact formalizes when the complete labeled EFX0 allocation set
is locally constant under entrywise perturbations of an additive valuation
matrix.  It is not yet part of the paper.

## Sign forms and chambers

Fix \(n,m\), and let \(V=(v_{i,g})\in\mathbb R_{>0}^{n\times m}\).
For a labeled allocation \(A\), an observer \(i\ne j\), and a removable good
\(g\in A_j\), define
\[
\Delta_{A,i,j,g}(V)
=v_i(A_i)-v_i(A_j\setminus\{g\}).
\tag{1}
\]
Then \(A\) is EFX0 exactly when every form (1) belonging to \(A\) is
nonnegative.  Its coefficient support has size
\[
\ell_{A,i,j,g}=|A_i|+|A_j|-1.
\tag{2}
\]
If \(\ell=0\), both bundles in (1) are empty and the equality
\(\Delta=0\) is an identity, not a chamber wall.  Every other equation
\(\Delta=0\) is a genuine hyperplane.  The exact EFX0 set is constant on each
open chamber of this finite hyperplane arrangement.

There is a useful coarser statement that is exact for the EFX0 set itself.
Write \(\mathcal E(V)\) for the set of labeled EFX0 allocations.

**Theorem (full-dimensional exact-set criterion).**
The matrix \(V\) is an interior point of
\[
\{W\in\mathbb R_{>0}^{n\times m}:\mathcal E(W)=\mathcal E(V)\}
\]
if and only if
\[
\Delta_{A,i,j,g}(V)>0
\tag{3}
\]
for every \(A\in\mathcal E(V)\) and every nontrivial form belonging to \(A\).

**Proof.**
If (3) holds, every currently EFX0 allocation has finitely many strict
inequalities.  Every allocation outside \(\mathcal E(V)\) already has at least
one strict violation \(\Delta<0\).  Finiteness therefore gives a neighborhood
in which the former inequalities stay positive and a selected violation for
each latter allocation stays negative.

Conversely, suppose a nontrivial form of an EFX0 allocation has
\(\Delta(V)=0\).  Decrease the entries with coefficient \(+1\) and increase
those with coefficient \(-1\) by an arbitrarily small common amount.  Because
the form is nontrivial and \(V\) is strictly positive, this can be done inside
the positive orthant and makes \(\Delta<0\).  That allocation ceases to be
EFX0 in every neighborhood of \(V\), so \(V\) is not an interior point.
\(\square\)

This condition deliberately examines equalities of the allocations that are
EFX0 at \(V\).  Equalities belonging only to an allocation that already has a
different strict violation need not obstruct local constancy.  The verifier
reports nontrivial equalities separately from the support-zero identities.

## An exact rational radius certificate

For a nontrivial form, entrywise perturbation obeys
\[
|\Delta(W)-\Delta(V)|
\le \ell\,\|W-V\|_\infty.
\tag{4}
\]
Define
\[
\begin{aligned}
\alpha(V)
&=\min_{\substack{A\in\mathcal E(V)\\\ell_q>0}}
  \frac{\Delta_q(V)}{\ell_q},\\
\beta(V)
&=\min_{A\notin\mathcal E(V)}
  \max_{\substack{q\text{ belongs to }A\\\Delta_q(V)<0}}
  \frac{-\Delta_q(V)}{\ell_q},\\
p(V)&=\min_{i,g}v_{i,g},\qquad
R(V)=\min\{\alpha(V),\beta(V),p(V)\}.
\end{aligned}
\tag{5}
\]
The usual \(+\infty\) convention applies to an empty outer minimum.  Under
(3), all relevant quantities in (5) are positive.  For every
\[
\|W-V\|_\infty<R(V),
\tag{6}
\]
the matrix \(W\) remains positive and
\(\mathcal E(W)=\mathcal E(V)\).  Indeed, (4) preserves every EFX0 inequality,
while for each non-EFX0 allocation the violation attaining its inner maximum
stays negative.  Thus \(R(V)\) is a certified open-box radius; it is not
claimed to be the largest possible radius, because several violated forms may
have to move simultaneously before a non-EFX0 allocation enters the set.

For a closed-box statement with no boundary ambiguity, this artifact records
\[
\rho(V)=R(V)/2.
\tag{7}
\]
Every \(W\) with \(\|W-V\|_\infty\le\rho(V)\) is positive and has exactly the
same labeled EFX0 set.  When \(V\) is rational, all numbers in (5)--(7) are
rational and are computed with integer comparisons and `fractions.Fraction`.

If a nontrivial equality occurs in a currently EFX0 allocation, the artifact
reports `OBSTRUCTED` and radius zero instead of claiming a full-dimensional
chamber.

## The six count-\(n\) witnesses

The source paths and SHA-256 digests are inherited from
`repro/counting_witnesses/instances.json`.  Exhaustive enumeration gives:

| witness | \(\alpha\) | \(\beta\) | \(p\) | open \(R\) | closed \(\rho\) | nontrivial EFX equalities |
|---|---:|---:|---:|---:|---:|---:|
| `n4_m7` | \(1/4\) | \(1/4\) | \(1\) | \(1/4\) | \(1/8\) | 0 |
| `n5_m8` | \(3/4\) | \(1/4\) | \(1\) | \(1/4\) | \(1/8\) | 0 |
| `n6_m9` | \(1/2\) | \(1/4\) | \(1\) | \(1/4\) | \(1/8\) | 0 |
| `n4_m8` | \(1/5\) | \(1/5\) | \(1\) | \(1/5\) | \(1/10\) | 0 |
| `n4_m9` | \(1/6\) | \(1/6\) | \(1\) | \(1/6\) | \(1/12\) | 0 |
| `n4_m10` | \(1/7\) | \(1/7\) | \(1\) | \(1/7\) | \(1/14\) | 0 |

Thus none of the six witnesses has the equality obstruction: each belongs to a
full-dimensional region of positive additive matrices with the same exact
count-\(n\) labeled EFX0 set.

## Verification

Install the pinned dependency for the vectorized checker and run both
implementations:

```sh
python -m pip install -r artifacts/efx_chambers/requirements.txt
PYTHONDONTWRITEBYTECODE=1 python artifacts/efx_chambers/verify_radii.py
PYTHONDONTWRITEBYTECODE=1 python artifacts/efx_chambers/verify_radii_exact.py
```

The first verifier checks the inherited source hashes, enumerates all \(n^m\)
allocations, recomputes every sign form, uses an integer common denominator for
all normalized margins, verifies the exact EFX0 counts and rational
certificates, and checks a synthetic equality-obstruction instance.  NumPy
uses signed 64-bit integer arithmetic only after an explicit instance-specific
overflow bound; no floating-point value enters a certificate.

`verify_radii_exact.py` is a genuinely separate standard-library
implementation: it imports neither NumPy nor `verify_radii.py`.  It enumerates
labeled allocations with a base-\(n\) odometer and uses independently built
subset tables.  Its checks are certificate-style:

- every nontrivial form of every EFX0 allocation is at least the claimed
  \(\alpha\), and an explicit form attains equality;
- every non-EFX0 allocation has an explicit violated form of normalized
  magnitude at least the claimed \(\beta\), and one allocation is scanned
  completely to show that its strongest violation is exactly \(\beta\); and
- the positivity margin and the two radius formulas are recomputed with
  `fractions.Fraction`.

For a fixed observer--target pair, all removed-good forms have the same support
size, and removing an observer-minimum good gives the least slack.  The
independent checker uses this exact reduction to find a violation certificate
quickly, then compares it against a literal every-removable-good implementation
on exhaustive synthetic cases.  Its obstruction regression also constructs a
positive rational perturbation that destroys an EFX0 allocation at a
nontrivial equality, while separately checking that support-zero identities do
not obstruct a chamber.

On the recorded development machine, the independent checker verifies all
\(11{,}860{,}961\) labeled allocations in about \(14.1\) seconds, of which the
\((6,9)\) witness takes about \(12.1\) seconds.  Timings are descriptive, not
certificate data.

`MANIFEST.json` pins the source manifest, certificate file, both verifier
sources, dependency file, and base repository commit.  The commit identifies
the repository state on which this uncommitted scratch artifact was assembled;
it does not claim that the artifact files occur in that commit.  Both programs
remain executable computations rather than a proof-assistant formalization,
but their enumeration strategies and arithmetic paths are independent.

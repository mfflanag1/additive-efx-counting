# Complementary EFX Wall at a Four-Allocation Basin

This note records an exact local mechanism found while minimizing the number
of complete EFX\(_0\) allocations at \((4,8)\). It is a local certificate, not
a proof of global EFX existence.

## Shared-minimum swap lemma

Let \(P,D\) be disjoint bundles and let \(q\) be another good. Fix an
observer \(i\), and suppose

\[
  v_i(q)\le\min_{g\in P\cup D}v_i(g).
\]

Consider two complete candidate allocations. In \(X\), agent \(i\) owns
\(P\) and some target owns \(D\cup\{q\}\). In \(Y\), agent \(i\) owns \(D\)
and some target owns \(P\cup\{q\}\). Suppose every EFX inequality of each
candidate except the displayed observer-to-target comparison is already
valid. Then

\[
\begin{aligned}
X\text{ is EFX}_0
&\Longleftrightarrow v_i(P)\ge v_i(D),\\
Y\text{ is EFX}_0
&\Longleftrightarrow v_i(D)\ge v_i(P).
\end{aligned}
\]

Thus at least one candidate is EFX, and both are EFX on the equality wall.
The proof is immediate: removing the shared minimum \(q\) maximizes the value
left in each target bundle. The usefulness of the lemma is not the scalar
dichotomy itself, but the possibility of constructing a dual allocation for
which every noncritical inequality remains valid.

Consider the positive additive matrix

```text
     3    5492   2694   22602   31736      4   21010   34539
   348   28272  16010   84861   36138     18   10058   60455
   372  110006  23178  206395   86612  12994  206519  180484
    12   36021  17067  145590   48350   2707  148982   73591
```

For \(0\le d\le3\), transfer \(d\) units in row 0 from good 5 to good 1.
Put

\[
 p=v_0(0)=3,\quad q=v_0(5)=4-d,\quad
 L=v_0(1)+v_0(4)=37228+d,\quad
 R=v_0(2)+v_0(7)=37233.
\]

## Primary family

The four allocations

```text
(h,2,0,1,2,2,3,0),  h=0,1,2,3
```

park good 0 at each of the four hosts over the same seven-good base. The
tight member is \(h=2\). Once \(q\le p\), its only moving EFX inequality is

\[
 R\ge p+L,
\]

whose slack is \(2-d\). All four primary allocations are EFX for
\(0\le d\le2\).

## Dual family

The following four allocations use the exchanged triple partition
\(\{0,1,4\},\{2,5,7\},\{3\},\{6\}\):

```text
(0,0,1,3,0,1,2,1)
(0,0,1,2,0,1,3,1)
(0,0,2,1,0,2,3,2)
(0,0,3,1,0,3,2,3)
```

For every member, the only inequality that can fail in this interval is row
0 comparing its owned triple \(\{0,1,4\}\) with the other triple
\(\{2,5,7\}\). Because \(q\) is the least good in the target, that inequality
is

\[
 p+L\ge R,
\]

with slack \(d-2\). All four dual allocations are EFX for \(2\le d\le3\).
Every other dual-family EFX slack is at least 2,733 throughout the interval.

The two critical slacks are exact negatives. Therefore the wall \(d=2\)
cannot be crossed without handing EFX feasibility from one four-allocation
family to the other:

| \(d\) | primary family | dual family | exact total EFX count |
|---:|---:|---:|---:|
| 0 | 4 | 0 | 4 |
| 1 | 4 | 0 | 4 |
| 2 | 4 | 4 | 8 |
| 3 | 3 | 4 | 7 |

This explains why locally reducing the surviving margins does not approach a
zero-EFX chamber: the boundary creates a second allocation family before the
first disappears. It gives a concrete target for a broader proof strategy:
pair prospective failure inequalities with exchanged allocations whose
critical slack is complementary.

## A second wall changes the shape completely

A different one-row transfer from the repository's second count-four basin
moves \(d\) units in row 1 from good 0 to good 2. The exact shape census is

| \(d\) | \(4211\) | \(5111\) | total |
|---:|---:|---:|---:|
| 0 | 3 | 1 | 4 |
| 1 | 2 | 5 | 7 |
| 2 | 2 | 5 | 7 |
| 3 | 2 | 7 | 9 |
| 4 | 1 | 8 | 9 |
| 5 | 0 | 8 | 8 |

At \(d=5\) the matrix is

```text
 3  95 100   6 64 20 23  9
23  75  82  20 74  9 21  2
 9  94   4  13 93 63  3  5
21  58  31  19 96 34 20 10
```

This matrix has exactly eight complete EFX\(_0\) allocations, and all eight
have shape \(5111\). It has no universal-minimum good, no peelable good, and
four pairwise distinct normalized rows. Thus even inside the exact residual
case, the tempting conjecture that a hard matrix must retain an EFX
allocation of shape \(4211\) or \(3311\) is false. The coverage handoff can
change the bundle shape, not merely exchange two nearby allocations.

`tracks/parkability/test_parkability.py` exhaustively checks all four points
and the shape-switch matrix with the optimized enumerator; the broader
differential suite checks that enumerator against a definition-literal
implementation.

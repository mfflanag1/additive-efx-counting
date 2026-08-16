# Maximum-Nash Local Completion: Exact Radius-Three Refutation

**Status:** exactly verified for four agents and nine goods  
**Refuted route:** same-floater local repair of a maximum-Nash eligible state  
**Not refuted:** existence of complete EFX allocations

## Statement

Call a one-floater partial allocation \((X,f)\) **eligible** when \(X\) is EFX
and

\[
v_i(X_i)\ge v_i(f)\qquad\text{for every agent }i.
\]

For two eligible states with the same floater, let their owner distance be the
number of allocated goods whose owners differ. The following natural repair
of direct maximum-Nash completion is false:

> From a maximum-product eligible state, one can preserve eligibility while
> transferring one allocated good, and thereby reach an eligible state into
> which the same floater can be inserted.

The exact profile below has a stronger property. Its unique maximum-product
eligible state is blocked at every host and is isolated in the graph whose
edges are same-floater, one-good-owner changes. Moreover, there is no eligible
same-floater state permitting insertion at owner distance at most three. The
nearest such states have distance four.

This is a refutation of a proof mechanism, not of complete additive EFX. The
same profile has 128 complete EFX allocations.

## Fixed profile

Rows are agents and columns are goods \(0,\ldots,8\):

\[
\begin{pmatrix}
76&134&10&311&10&1080&4844&4266&20\\
11822&5667&21581&5696&7339&33090&30279&1&2796\\
12476&135&17143&7875&18062&3&29666&1367&6968\\
2661&3970&5976&91&14072&19546&450&10190&6019
\end{pmatrix}.
\]

The candidate leaves good 8 unallocated and uses

\[
X_0=\{6,7\},\qquad
X_1=\{1,2,3\},\qquad
X_2=\{0,4\},\qquad
X_3=\{5\}.
\]

Its utility vector and exact product are

\[
(9110,32944,30538,19546),\qquad
179140256386440320.
\]

The second-largest eligible product is \(178611984443889542\), so the unique
maximum has the strict gap

\[
528271942550778.
\]

The minimum partial-EFX slack is 872, and the four floater-nonenvy slacks are

\[
(9090,30148,23570,13527).
\]

Thus eligibility is not a numerical boundary artifact.

## Why direct insertion fails

For each proposed host, the audit records a negative EFX slack. One shortest
witness per host is:

| Host | Observer | Removed good | Slack |
|---:|---:|---:|---:|
| 0 | 1 | 7 | -131 |
| 1 | 2 | 1 | -1448 |
| 2 | 3 | 0 | -545 |
| 3 | 1 | 8 | -146 |

Hence no bundle accepts the floater directly.

## Exact local boundary

There are exactly

\[
1+8(4-1)=25
\]

owner vectors at distance at most one: the candidate itself and the 24 ways
to transfer one of its eight allocated goods to a different agent. Literal
reconstruction finds that the candidate is the only eligible one. Therefore
it has no eligible same-floater one-transfer neighbor at all, insertable or
otherwise.

The full eligible-state census then measures every same-floater state. No
insertable state occurs at distances 0, 1, 2, or 3. Exactly seven insertable
eligible states first occur at distance 4. This rules out both an immediate
one-transfer repair and any iterative procedure whose individual moves must
be same-floater one-good transfers preserving eligibility: such a procedure
cannot leave the candidate.

It does not rule out changing the floater, making a simultaneous multi-good
move, or temporarily leaving the eligible-state class.

## Exhaustive verification

The audit checks all \(9\cdot4^8=589824\) one-floater assignments. It finds:

- 314 eligible partial states;
- 312 distinct eligible utility vectors;
- one maximum-product state;
- no eligible radius-one neighbor of that state other than itself;
- no same-floater insertable state through radius three;
- seven nearest same-floater insertable states at radius four.

The classifications agree across a direct literal implementation, the
repository's independent core iterator, and the vectorized subset-sum
implementation at radii three and four. A separate literal enumeration of
all \(4^9=262144\) complete allocations agrees with the core iterator and
finds 128 complete EFX allocations. Their ordered allocation-list hash is

```text
bedacc8d0e3f4038d3300ff2791a8201d2f63261c6861c9bbb0b7e3b46ede3ae
```

## Frozen artifacts

- Profile: `partial_nash_one_transfer_refutation_profile.json`  
  SHA-256 `bf9f69ad9673566b6f0c255b81bb8f6d830965ba649007ef06133add0d211f7c`
- Exhaustive audit: `partial_nash_one_transfer_refutation_audit.json`  
  SHA-256 `82af6794de0f99c4eaea49a19fef5aa4f8308b82ebe5af627b35ae493bb419e3`
- Discovery checkpoint: `partial_nash_one_transfer_refutation_candidate.json`  
  SHA-256 `48a87396e62fb5bc10ced5ed74b4cbd6ff058a9ba66e15a41337fd76e4603c12`
- Independent checker:
  `../tracks/parkability/audit_partial_nash_one_transfer_refutation.py`

The discovery checkpoint deliberately retains its historical
`PENDING_INDEPENDENT_REPLAY` label; the fixed profile and exhaustive audit are
the promoted result.

## Replay

From the repository root:

```bash
make verify-partial-nash-one-transfer-refutation
```

The command rebuilds the exhaustive audit in a temporary directory and
requires byte-for-byte equality with the frozen artifact.

## Consequence for the general program

Maximum-Nash direct insertion and its same-floater local one-good repair are
both closed. The surviving possibilities must use structure absent from this
selector: floater substitution, simultaneous multi-good rearrangement,
nonmonotone motion outside the eligible class, or the independent
partition/Hall route. Complete additive EFX remains open.

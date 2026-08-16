# Maximum-Nash Source Completion: Exact Refutation

**Status:** exactly verified for four agents and nine goods  
**Refuted route:** one source-good substitution plus arbitrary bundle rematching  
**Not refuted:** existence of complete EFX allocations

## Refuted selector

Call a one-floater partial allocation \((X,f)\) **eligible** when \(X\) is EFX
and \(v_i(X_i)\ge v_i(f)\) for every agent. Select an eligible state
maximizing

\[
\prod_i v_i(X_i).
\]

A bundle \(X_h\) is a **source bundle** when no other agent strictly prefers
it to its own bundle. The strongest local descendant of the maximum-Nash
program considered here was:

> If the selected state is not directly completable, choose a source bundle,
> replace one of its goods \(r\) by the floater \(f\), make \(r\) the new
> floater, and permute all four resulting bundles among the agents. Some such
> rematching is eligible and directly completable.

This statement is false. In the exact profile below, the unique
maximum-product eligible state is blocked. It has two source bundles, but all
120 source-good substitutions and bundle permutations fail partial EFX;
there is not even an eligible successor in the proposed family.

The profile nevertheless has 87 complete EFX allocations. It refutes the
selector, not complete additive EFX.

## Fixed profile

Rows are agents and columns are goods \(0,\ldots,8\):

\[
\begin{pmatrix}
96&123&33&738&267&930&5537&3010&17\\
15054&10496&18340&4209&3746&33127&32860&330&109\\
9772&7609&18659&570&21490&254&30109&236&4996\\
80&5355&516&1522&13190&19373&14748&1579&6612
\end{pmatrix}.
\]

The selected state leaves good 8 unallocated and has

\[
X_0=\{6,7\},\qquad
X_1=\{1,2,3\},\qquad
X_2=\{0,4\},\qquad
X_3=\{5\}.
\]

Its utility vector and exact product are

\[
(8547,33045,31262,19373),\qquad
171053946045626490.
\]

The second-largest eligible product is \(161282001348477240\), giving the
strict maximum gap

\[
9771944697149250.
\]

The candidate's minimum partial-EFX slack is 185. Its floater-nonenvy slacks
are

\[
(8530,32936,26266,12761).
\]

Thus its eligibility and unique maximality are not tie artifacts.

## Direct obstruction

Each possible host has a negative insertion slack:

| Host | Observer | Removed good | Slack |
|---:|---:|---:|---:|
| 0 | 1 | 8 | -145 |
| 1 | 2 | 3 | -2 |
| 2 | 3 | 0 | -429 |
| 3 | 1 | 8 | -82 |

The host-1 obstruction is only two integer units from equality, which explains
why the adversarial search approached a narrow numerical boundary before
crossing into the stronger source-completion refutation.

## Exhaustive source-substitution boundary

The source bundles are exactly \(X_1=\{1,2,3\}\) and
\(X_2=\{0,4\}\). Hence the proposed family contains

\[
(3+2)\cdot4!=120
\]

generated states. They are all distinct. Literal enumeration finds:

- 120 partial-EFX failures;
- 67 states that also violate new-floater nonenvy;
- zero eligible states;
- consequently, zero eligible insertable states.

The canonical list of all 120 classified rematchings has SHA-256

```text
e8b24fc7ef124b2f92bbb0771c36367525ccc1f9822c2f1e8185cc839ab9193c
```

Because no proposed successor is eligible, this profile also blocks an
iterative proof whose first step must be one of these source substitutions
while staying inside the eligible class.

## Independent verification

The audit directly checks all \(9\cdot4^8=589824\) one-floater assignments
and finds 279 eligible states with 279 distinct utility vectors. Literal,
core-iterator, and vectorized implementations agree on the unique maximum and
its blocked status. The 120 source substitutions are independently rebuilt by
literal bundle manipulation and by the source-completion implementation.

A separate literal enumeration of all \(4^9=262144\) complete allocations
agrees with the core iterator and finds 87 complete EFX allocations. Their
ordered allocation-list hash is

```text
1df3ddc539041387a2f6e9486f6cdbe4bacb828e3cb87504fa97a027a9bb3921
```

## Frozen artifacts

- Profile: `partial_nash_source_completion_refutation_profile.json`  
  SHA-256 `a12e9519f02570976f913a2a56b5e550e478cb2767f03eff14dd03f7a93c148c`
- Exhaustive audit: `partial_nash_source_completion_refutation_audit.json`  
  SHA-256 `cd187140171ff5817adcda6060cab0ed0f6526b71feea869edf6d7f7903fa022`
- Discovery output: `partial_nash_source_completion_anneal_seed619.json`  
  SHA-256 `fc355aff0ef3af8ac7056a4263305631d82750c5dfa7e1907974041147aa1bdd`
- Corpus scan: `partial_nash_source_completion_corpus_scan.json`  
  SHA-256 `bc13d548ea5ab0a40d19d39c880e37f9420d682b6b9bca4eb26fe394777726cf`
- Independent checker:
  `../tracks/parkability/audit_partial_nash_source_completion_refutation.py`

The refreshed corpus scan covers 159 distinct stored profiles with at most
nine goods. Three have blocked maximum-Nash states; the two earlier profiles
are rescued by a source substitution, while this profile is the unique exact
failure. This finite scan is calibration, not a theorem.

## Replay

From the repository root:

```bash
make verify-partial-nash-source-completion-refutation
```

The target rebuilds the exhaustive audit in a temporary directory and
requires byte-for-byte equality with the frozen artifact.

## Consequence for the research program

Three nested maximum-Nash claims are now exactly false:

1. the maximum state need not accept its floater directly;
2. it can be isolated under same-floater eligible one-good transfers, with no
   same-floater completion through owner distance three;
3. even replacing a good in any source bundle and arbitrarily rematching all
   bundles can yield no eligible successor.

The maximum-Nash partial-state branch has therefore exhausted its natural
local and one-substitution descendants. A surviving proof needs a genuinely
global construction not anchored to that state, a path allowed to leave the
eligible class, or the independent partition/Hall program. The exact profile
does not support any claim against complete additive EFX.

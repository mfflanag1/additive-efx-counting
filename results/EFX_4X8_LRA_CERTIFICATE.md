# Solver-Backed EFX Certificate at \((4,8)\)

> **Historical stage record.** This document predates the CPC/Ethos closure
> and the Lean-checked extension from positive to nonnegative weights. Use
> `EFX48_BREAKTHROUGH_CONVERSION_20260730.md` and the submission manuscript
> for the current theorem and status.

**Status (2026-07-29):** exhaustive exact-QF_LRA closure candidate for
strictly positive additive valuations. The analytic reduction is proved
below. Every one of the eight terminal cells returned `unsat`, and seven
replayed in fresh standalone Z3 processes. This is not yet called a theorem
because most cells do not have independently checked proof objects.

By the Threshold-Cycle Normal Form Theorem in
`REVERSE_PARKING_LEMMA.md`, the result simultaneously covers complete
EFX\(_0\) existence and parkable deletion.

## 1. Analytic coverage reduction

Assume for contradiction that a positive additive \(4\times8\) instance has
no complete EFX\(_0\) allocation.

1. **Every relevant allocation is onto.** If an owner were empty, some one
   of the other three bundles would contain at least three positive goods,
   whose one-good-removed threshold is positive. The empty owner would
   strongly envy it.
2. **Universal-minimum goods are safe.** Delete such a good, use the
   seven-good EFX theorem, eliminate ordinary envy cycles, and park the
   deleted minimum at a source.
3. **Peelable goods are safe.** If
   \(v_i(t)\ge\tau_i(M\setminus\{t\})\), give \(t\) alone to \(i\) and use
   the three-agent EFX theorem on the remaining goods.
4. **Nonexistence is open.** For each of the finitely many complete
   allocations choose one strict failed EFX inequality. A sufficiently
   small normalized perturbation preserves positivity and all chosen
   failures. It can simultaneously avoid every within-row value equality
   and every equality between two normalized rows. Thus a counterexample,
   if one exists, has a generic counterexample in the residual cases used
   by the formulas.
5. **Favorite-good matching is safe.** If the four agents can be matched to
   four distinct weakly favorite goods, pair each matched favorite with one
   of the four leftover goods. For observer \(i\), its own pair is worth at
   least its favorite, while the EFX threshold of every target pair is the
   value of one target good and is at most that favorite. The \(2222\)
   allocation is EFX.

In a generic counterexample, every agent therefore has a unique favorite and
the four favorite labels repeat. Up to relabeling agents and goods, there are
four multiplicity types:

\[
4,\qquad 3+1,\qquad 2+2,\qquad 2+1+1.
\]

The last three are the strict favorite patterns
\((0,0,0,1),(0,0,1,1),(0,0,1,2)\). If all agents prefer good 0, each has a
unique second favorite among the other seven goods. Their second-favorite
labels have exactly five possible multiplicity types:

\[
1+1+1+1,\qquad4,\qquad3+1,\qquad2+2,\qquad2+1+1.
\]

Canonical second patterns are
\((1,2,3,4),(1,1,1,1),(1,1,1,2),(1,1,2,2),(1,1,2,3)\). These three
first-level cells and five second-level cells exhaust the positive domain.

The cell stabilizers are conservative. They sort only agents with the same
prescribed ranking prefix and columns unused by that prefix. Both operations
preserve the cell, so a lexicographically maximal member of every stabilizer
orbit satisfies the constraints.

## 2. Exact terminal encoding

There are \(S(8,4)=1{,}701\) unlabeled partitions of the goods into four
nonempty bundles. For a partition
\(\mathcal B=\{B_0,B_1,B_2,B_3\}\), put edge \(iB_b\) when

\[
v_i(B_b)\ge \max_{c\ne b}\tau_i(B_c).
\]

An assignment of these four bundles is EFX exactly when its four
agent--bundle edges form a perfect matching. A counterexample therefore
requires all 1,701 graphs to have no perfect matching. Each terminal formula
defines the 16 edges of every partition by exact rational linear
inequalities and excludes all \(4!=24\) matchings.

Each formula also asserts:

- positive row-normalized values;
- no universal-minimum good;
- no peelable agent--good pair;
- pairwise distinct normalized rows;
- its strict favorite or two-good ranking-prefix cell; and
- only the cell-preserving stabilizer, where used.

The two fixed-matrix encodings (`matching_clauses` and `hall_selectors`) agree
on all 384 combinations of every partition and every positive binary
\(2\times3\) matrix. The allocation predicates are separately
definition-literal tested.

## 3. Terminal cells

All formulas contain all 1,701 partitions and use the
`matching_clauses` obstruction.

| leaf | strict pattern | stabilizer | solve s | SMT2 SHA-256 |
|---|---|---|---:|---|
| \(2+1+1\) favorites | \(f=(0,0,1,2)\) | none | 742.878 | `59fc36550cca86bd4e981cbcc33b333dfd5f77dab2f31f0cd27261d316c898de` |
| \(3+1\) favorites | \(f=(0,0,0,1)\) | favorite | 4,090.177 | `dfe7bb6689aa2bc8682d869cd4b93b8ee52b78d57fbda910fc013c9b32243c6d` |
| \(2+2\) favorites | \(f=(0,0,1,1)\) | favorite | 2,179.563 | `075193d5e4fdc2197bc95ac4d7011286bae356082af0170de6baf934fa71fe54` |
| distinct seconds | \(f=(0,0,0,0),s=(1,2,3,4)\) | prefix | 59.097 | `85baf8d9127611483d2cd98985b84d13c3801d4a85eb7047cb53a61cf80be5b9` |
| \(4\) seconds | \(f=(0,0,0,0),s=(1,1,1,1)\) | prefix | 5,989.274 | `5b2a9a416a4ed6007b0a6526baae4200ca419c2cd7bfff0e459eaab24cc57971` |
| \(3+1\) seconds | \(f=(0,0,0,0),s=(1,1,1,2)\) | prefix | 959.765 | `bc1e0cc20ec6002ba1f018afb82cfd5c6879dcd0f082e970df0d634fe2c65849` |
| \(2+2\) seconds | \(f=(0,0,0,0),s=(1,1,2,2)\) | prefix | 555.783 | `d550c963306267a3d38de5c04a6636bd7c084714f569f26f7e68bfca58b9e72f` |
| \(2+1+1\) seconds | \(f=(0,0,0,0),s=(1,1,2,3)\) | prefix | 73.282 | `ac1813e9e6e6cb9810e4b34184d4aaebd1c5fdfed4f694f392b17178cc61348f` |

Every creating-process result was `unsat`. Seven frozen formulas also
returned `unsat` in fresh standalone Z3 processes. The all-four-equal
second-favorite cell's standalone replay was intentionally interrupted after
24 minutes when the goal window elapsed; its creating-process result remains
the 5,989-second UNSAT result in the table. Replay status is tracked
separately so that an interruption cannot be mistaken for confirmation.

As an encoding cross-check, the distinct-second cell was rebuilt by directly
negating all 40,824 labeled onto allocations, without partition edge
variables or perfect-matching clauses. It returned UNSAT in 39.214 seconds:

```text
direct-allocation formula SHA-256:
3a67237b65c9edb48a6d8d9498c71ec3569ec4fc412a54a9db41a2fc4c78f1dd
```

This does not make Z3 an independent checker, but it separates an error in
the partition-matching reduction from an error in the direct EFX clauses.

## 4. Core and proof artifact

Two activation-literal passes on the \(2+1+1\)-favorite formula reduced the
1,701 partition obstructions first to 216 and then to a sufficient
200-partition core:

| shape | partitions in core |
|---|---:|
| \(2222\) | 51 |
| \(3221\) | 98 |
| \(3311\) | 20 |
| \(4211\) | 30 |
| \(5111\) | 1 |

The rebuilt conventional core formula is 3.2 MB and has SHA-256

```text
7c25dae47bec3dd8626dfb82cce4ad6cd6e18dbd302174f7d3b9f2a58f645c60
```

It returned `unsat` both when rebuilt and in a fresh standalone Z3 process.

The full cell also generated a 96 MB native Z3 proof term:

```text
1a33c917102600d9e6143d0afea3ab6410af92ea1f19787dfe1d2e23c1c2e4b8
```

Replaying the full formula with native proof production and Z3's
`sat.smt.proof.check=true` option also returned `unsat`. Native proof
production and internal checking are stronger than an unrecorded solver
verdict, but are not an independent proof check. The immediate certification
target is to validate a compressed proof with a separate checker or translate
the small core into a hand-auditable Farkas/resolution certificate.

## 5. What may be claimed

Subject to the eight exact UNSAT results, every positive additive
\(4\times8\) instance has a complete EFX\(_0\) allocation. The
Threshold-Cycle Normal Form Theorem then transforms one into an allocation
with an owner-removable good, proving parkable deletion.

Until the arithmetic proofs are independently checked, the appropriate
language is:

> exhaustive exact-LRA solver-backed closure candidate for positive
> additive EFX and parkable deletion at \((4,8)\).

It is premature to call this an unconditional theorem or a resolution of the
open additive EFX cell.

## 6. Preliminary literature position

Ashuri, Gkatzelis, and Sgouritsa,
[*EF2X Exists for Four Agents*](https://arxiv.org/abs/2412.00254), state that
complete EFX existence for four agents remains open even for additive
valuations. Akrami et al.,
[*A Counterexample to EFX*](https://arxiv.org/abs/2604.18216), obtain
monotone-valuation counterexamples from \(m\ge n+5\); their construction does
not cover the \(m=n+4\) cell studied here. Their positive three-agent,
seven-good result is backed by a roughly 30 GB DRAT-checked UNSAT proof,
which is the right certification standard to emulate. A targeted arXiv
search on 2026-07-29 did not locate a published additive \((4,8)\) theorem.
This is a preliminary check, not a novelty proof.

## 7. Frozen evidence

The eight result records and SMT-LIB formulas, the direct-allocation
cross-check, the 200-partition core, native proof terms, coverage audit, and
individual replay observations are frozen under
[`goal-20260729-favorite-cells`](../../experimental-runs/additive-efx-counting-runs/parkability/goal-20260729-favorite-cells).
`MANIFEST.sha256` binds every archived file.

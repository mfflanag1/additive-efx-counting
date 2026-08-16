# Parkable Deletion Goal Log — 2026-07-29

**Target.** Decide whether every positive additive \(4\times8\) valuation
matrix has a good whose deletion admits an EFX\(_0\) base and a host at which
the good can be restored while preserving EFX\(_0\).

**Current status.** Exhaustive exact-LRA closure candidate. Eight generic
favorite/ranking cells cover the positive-real domain after proved reductions,
and every cell is solver-UNSAT. Seven of the eight frozen formulas replayed
UNSAT in standalone Z3 processes; the longest replay was interrupted when the
goal window elapsed. This is strong solver-backed evidence, not yet an
independently proof-checked theorem.

## Threshold-cycle equivalence

The parkability target is now proved equivalent to complete EFX existence.
For a bundle \(S\), write

\[
  \tau_i(S)=v_i(S)-\min_{g\in S}v_i(g).
\]

In a complete EFX allocation, owner \(i\) has a removable good exactly when
its own bundle maximizes \(\tau_i\) among all bundles. If no owner does,
point every owner to a threshold-maximizing bundle. The resulting functional
graph contains a cycle. Rotating bundles along it preserves EFX: every moved
agent receives a bundle whose total is at least the largest threshold it
faces. The potential \(\sum_i\tau_i(X_i)\) strictly increases. Since there
are finitely many allocations, the process terminates with a removable
least good.

Therefore, for positive valuations with \(m\ge n\),

\[
  \text{complete EFX exists}\iff\text{parkable deletion exists}.
\]

This is constructive and implemented by
`core.threshold_cycle_normal_form`; exhaustive literal controls cover all
240 EFX allocations from the 64 positive \(2\times3\) matrices over
\(\{1,2\}\), plus a directed \(4\times8\) allocation requiring a three-agent
rotation. Originality has not yet been checked.

The computational consequence is important: the exact certificate universe
can be reduced from 524,288 deletion/base/host triples to 65,536 complete
allocations. A zero-triple rational model would necessarily have zero
complete EFX allocations and would be a genuine counterexample, not merely
a failed bridge.

## Recovered bounded campaign

The durable \(K=4\) campaign had stopped after 376 completed refinements with
17,376 pooled triples. Its authoritative pool is byte-identical to the final
session snapshot:

```text
SHA-256 27fea36e1f77896fc3646d2b74c86e77eaa68209a59cd7f663e24e9837707a4d
```

The supervisor's `CORRUPT` status is path-identity drift caused by the
repository move, not artifact corruption. All differential, terminal-CNF,
and durable-supervisor tests pass.

An independent 7,113,994-variable, 14,004,822-clause terminal CNF solve
returned SAT after 581.9 wall-seconds:

```text
3 2 4 2 1 1 1 1
1 2 4 2 1 1 1 1
4 2 2 2 1 1 1 1
4 2 1 2 1 1 1 1
```

The decoded model satisfies every clause and invalidates every pooled triple.
It is not a counterexample: exact enumeration finds 576 parkable triples and
294 complete EFX\(_0\) allocations. Goods 4--7 are universal minima, and all
576 triples delete one of those goods. This diagnoses the old campaign's
main inefficiency: it repeatedly learned small prefixes of large,
theorem-safe universal-minimum landscapes.

Terminal result:

```text
SHA-256 c7c594b3c32220b5ce7f93ba2e9585223d169c5c469ec37fc42233c520f1e559
```

## Structural case cut

If \(f\) is a universal-minimum good, delete it. Mahara's \(m\le n+3\)
theorem supplies an EFX allocation of the seven remaining goods. Envy-cycle
rotation preserves EFX and terminates at an acyclic plain-envy graph, which
has a source. Because every observer values \(f\) no more than any good in
the source bundle, parking \(f\) at that source preserves EFX.

Therefore a zero-parkability matrix cannot have a universal-minimum good.
The exact negation used by the real-arithmetic master is

\[
  \bigwedge_g\ \bigvee_{i,g'\ne g} v_i(g)>v_i(g').
\]

This is a proved case split, not a heuristic filter.

## Exact real-arithmetic CEGAR

`tracks/parkability/lra_master.py` and `run_lra_cegar.py` now search all
strictly positive real valuations after per-row normalization. Every pooled
triple contributes the exact disjunction

```text
base not EFX0  OR  parked completion not EFX0.
```

All inequalities are rational and strict reversals are represented directly
in QF_LRA. SAT models are converted exactly to primitive integer rows and
checked by the solver-free and literal enumerators. An UNSAT result would
cover the whole no-universal-minimum case; combined with the structural case
above, it would prove parkable deletion for positive \(4\times8\) instances.
Such a solver result would still need independent proof checking.

The search uses balanced floater/host certificate selection. This removed the
old scan-order bias: early candidate counts fell from 1,008 to below 100 while
incremental solves were still generally short. Multiple global pools are
being merged; no terminal global result is yet claimed.

## Direct complete-allocation master

The threshold-cycle equivalence permits a smaller exact master:
`run_efx_lra_cegar.py` negates complete EFX allocations directly. For a fixed
complete allocation \(X\), its cut is the exact QF_LRA clause

\[
 \bigvee_{i\ne j,\ g\in X_j}
 v_i(X_i)<v_i(X_j\setminus\{g\}).
\]

Positivity implies that a complete EFX allocation at \((4,8)\) is onto. The
exact relevant universe therefore has 40,824 allocations, distributed as

| shape | allocation count |
|---|---:|
| \(5111\) | 1,344 |
| \(4211\) | 10,080 |
| \(3311\) | 6,720 |
| \(3221\) | 20,160 |
| \(2222\) | 2,520 |

The old 64,525-triple global pool collapsed to 20,449 distinct completions.
Merging the new direct CEGAR history with the repository's earlier
`z3`, `anatomy`, `corridor`, `park`, and `peaks` allocation pools raised the
warm start to 33,303 allocations. A later 94,391-triple shape campaign added
2,214 more distinct completions. The current exact warm start thus contains
35,517 of the 40,824 onto allocations (87.0%); its pool SHA-256 is

```text
0ec540fa70813396d536dcebef037eba3e32f5886190b9503b8599781592d395
```

All 40,824 onto allocations have also been materialized independently as a
3,429,403-byte terminal pool:

```text
SHA-256 5f4a64a3e7201f658e94c48470e94f10ab561056be51431ec9e11424868bbbf8
```

The strengthened 35,517-allocation CEGAR master returned `UNKNOWN` after its
1,200-second limit. This is an inconclusive checkpoint, not evidence in
either direction. A one-shot formula containing the full onto universe is in
progress.

The direct runner optionally composes three proved residual reductions:

1. no universal-minimum good, by the seven-good theorem and source parking;
2. no peelable good \(t\) satisfying
   \(v_i(t)\ge\tau_i(M\setminus\{t\})\), since assigning \(t\) as a singleton
   reduces the remainder to the three-agent EFX theorem; and
3. pairwise distinct normalized rows, since at most three valuation types are
   already EFX-safe.

DoubleLex is an orbit-complete symmetry break. These are explicit case splits,
not witness-shaping heuristics. Fixed rational regressions check that each
encoded cut accepts and rejects the intended side.

A fourth proved reduction comes from favorite goods. At \(m=2n\), if the
agent--favorite-good graph has a matching saturating all agents, give every
agent its matched favorite and pair the remaining \(n\) goods arbitrarily
with them. Each own pair is worth at least the observer's favorite, while
the threshold of every target pair is at most that favorite. This is an
EFX \(2222\) allocation. Hence a counterexample must have a Hall-deficient
favorite graph. The exact optional cut
`--require-favorite-hall-deficiency` rules out all 1,680 injective
agent-to-good matchings. The two low-count basins satisfy this necessary
condition: in each, two agents have the same unique favorite.

The openness of nonexistence reduces this further to four generic cells.
If a counterexample exists, a small perturbation can preserve one strict
failure for every allocation while making all values within every row
distinct. The unique favorite labels must then repeat, and up to relabeling
their multiplicity pattern is one of \(4,3+1,2+2,2+1+1\), represented by
\((0,0,0,0),(0,0,0,1),(0,0,1,1),(0,0,1,2)\). The partition runner accepts
these as strict `--favorite-pattern` cells. This replaces a continuum of
favorite tie graphs by four open exact subproblems.

The first full cell solve closed the empirically hardest \(2+1+1\) pattern
\((0,0,1,2)\) after 742.878 solver-seconds, using all 1,701 partitions,
no unrestricted symmetry, and the proved universal-minimum, peeling, and
generic-distinct-row reductions:

```text
status: UNSAT_CANDIDATE
formula SHA-256: 59fc36550cca86bd4e981cbcc33b333dfd5f77dab2f31f0cd27261d316c898de
```

This is exact Z3 QF_LRA solver evidence, not yet a theorem. The frozen
\(2+1+1\) formula returned `unsat` in a standalone Z3 process as well.
The \(3+1\) and \(2+2\) cells subsequently returned `UNSAT_CANDIDATE`:

| favorite type | solve seconds | formula SHA-256 |
|---|---:|---|
| \(2+1+1\) | 742.878 | `59fc36550cca86bd4e981cbcc33b333dfd5f77dab2f31f0cd27261d316c898de` |
| \(3+1\) | 4,090.177 | `dfe7bb6689aa2bc8682d869cd4b93b8ee52b78d57fbda910fc013c9b32243c6d` |
| \(2+2\) | 2,179.563 | `075193d5e4fdc2197bc95ac4d7011286bae356082af0170de6baf934fa71fe54` |

The unsplit all-shared-favorite type \(4\) timed out after 7,200 seconds.
The second-favorite split below, rather than the unrestricted formula,
closed this final generic region. Several coarser restricted-shape and
alternative-encoding runs also timed out; those timeouts are inconclusive
and are not part of the closure claim.

The type-\(4\) cell was split exhaustively by the multiplicities of the
agents' strict second favorites. Genericity leaves five canonical patterns.
All five full exact formulas returned `UNSAT_CANDIDATE`, using only
stabilizer permutations that preserve both the common first favorite and
the specified second favorites:

| second-favorite pattern | solve seconds | formula SHA-256 |
|---|---:|---|
| \((1,2,3,4)\) | 59.097 | `85baf8d9127611483d2cd98985b84d13c3801d4a85eb7047cb53a61cf80be5b9` |
| \((1,1,2,3)\) | 73.282 | `ac1813e9e6e6cb9810e4b34184d4aaebd1c5fdfed4f694f392b17178cc61348f` |
| \((1,1,2,2)\) | 555.783 | `d550c963306267a3d38de5c04a6636bd7c084714f569f26f7e68bfca58b9e72f` |
| \((1,1,1,2)\) | 959.765 | `bc1e0cc20ec6002ba1f018afb82cfd5c6879dcd0f082e970df0d634fe2c65849` |
| \((1,1,1,1)\) | 5,989.274 | `5b2a9a416a4ed6007b0a6526baae4200ca419c2cd7bfff0e459eaab24cc57971` |

Together with the first-level \(3+1,2+2,2+1+1\) cells, this is an exhaustive
solver-backed closure of the positive additive \((4,8)\) problem. It is not
yet promoted to a theorem because the trust boundary still includes Z3 and
the generated formulas.

For the first-level \(2+1+1\) cell, two activation-literal passes reduced the
1,701 partitions first to 216 and then to a sufficient 200-partition UNSAT
core:

```text
51 x 2222, 98 x 3221, 20 x 3311, 30 x 4211, 1 x 5111
core formula SHA-256:
7c25dae47bec3dd8626dfb82cce4ad6cd6e18dbd302174f7d3b9f2a58f645c60
```

The conventional 3.2 MB core formula replayed UNSAT in both the creating
process and a fresh standalone Z3 process.
The original 27 MB cell formula produced a 96 MB Z3 proof object with SHA-256
`1a33c917102600d9e6143d0afea3ab6410af92ea1f19787dfe1d2e23c1c2e4b8`.
It also replayed UNSAT with Z3's internal proof-checking option enabled. The
proof object has not been checked by an independent proof checker.

An independent direct-allocation formula for the distinct-second cell
negated all 40,824 labeled onto allocations rather than the 1,701
partition-matching graphs. It returned UNSAT in 39.214 seconds:

```text
SHA-256 3a67237b65c9edb48a6d8d9498c71ec3569ec4fc412a54a9db41a2fc4c78f1dd
```

This cross-checks the partition reduction at the encoding level, while still
sharing Z3 as the solver trust boundary.

The tempting shortcut “a common unique favorite forces shape \(3221\)” is
false. An exact rational residual candidate avoiding all 840 \(3221\)
partitions has 98 EFX allocations, all \(3311\) or \(4211\). Even the
two-shape claim “common favorite forces \(3221\) or \(2222\)” is false:
another exact candidate avoids all 945 such partitions and has 137 EFX
allocations of shapes \(3311,4211,5111\). Thus the second-favorite cell split
is doing real work rather than hiding a simpler one-shape theorem.

The fixed-partition viewpoint gives a second terminal encoding. For each of
the 1,701 unlabeled nonempty bundle partitions, build the \(4\times4\)
agent--bundle graph whose edges are EFX-feasible assignments. An EFX
allocation on that partition is exactly a perfect matching. The complete
master therefore requires every graph to be Hall-deficient.
`run_partition_lra.py` implements two equivalent encodings:

- 24 no-perfect-matching clauses per partition; and
- explicit Hall-witness selectors with neighborhood cardinality constraints.

Both encodings passed 384 fixed-matrix checks spanning every partition of
every one of the 64 positive binary \(2\times3\) matrices. Their complete
\((4,8)\) SMT-LIB formulas are 27--28 MB, versus 68 MB for only the
35,517-allocation direct checkpoint. The terminal cells use matching
clauses; a direct-allocation formula independently cross-checks one cell.

## Near-zero record sequence

The vectorized counter in `fast_count.py` is exact and has been
differentially checked against full enumeration. Annealing and local LRA
produced the following progression, with every record subsequently checked
by both independent enumeration orders:

| record | method | parkable triples | complete EFX\(_0\) allocations |
|---|---|---:|---:|
| initial real-master candidate | QF_LRA | 1,008 | not used |
| first hard chamber | annealing | 8 | 7 |
| second hard chamber | local QF_LRA | 6 | 6 |
| current record | annealing from the six-triple model | 5 | 4 |

The five-triple record has no universal-minimum good. Four certificates park
one low good at all four hosts; a fifth deletes the other low good. A second
five-triple basin reverses those roles. This is the same robust charity
coupling seen in the historical count-four witnesses, now reached from the
no-universal-minimum side.

The provisional conjecture that the no-universal-minimum case had an
eight-triple floor was falsified immediately by the exact six-triple model.
No stronger positive lower bound is claimed.

Direct-count annealing made 300,000 additional exact vectorized moves from
three independent count-four basins. It never reached 3, 2, 1, or 0 complete
EFX allocations. This is heuristic evidence only and agrees with the
pre-existing count-\(n\) search history in the repository.

The most fragile four-allocation chamber exposed a sharper phenomenon. Along
a one-row transfer, the last tight inequality of the original four parking
allocations has slack \(2-d\), while four exchanged-triple allocations have
critical slack \(d-2\). At the wall \(d=2\), both four-allocation families are
EFX. Crossing the wall activates the dual family before the primary family
disappears. The exact matrices, allocations, and four exhaustive counts are
recorded in `COMPLEMENTARY_WALL_CERTIFICATE.md`. This is a local certificate,
but it suggests pairing prospective failure inequalities with exchanged
allocations having complementary slack.

A second certified wall falsifies a tempting shape reduction. A five-unit
one-row transfer from basin 2 changes the exact EFX census

```text
4 -> 7 -> 7 -> 9 -> 9 -> 8
```

while the surviving shapes move from three \(4211\) plus one \(5111\) to
eight \(5111\) and no \(4211\) or \(3311\). The endpoint still has no
universal minimum, no peelable good, and no repeated normalized rows.
Therefore even the strengthened residual case cannot be reduced to the
\(4211/3311\) shapes.

## Local exact closures

Normalized \(L_\infty\) boxes around the first eight-triple chamber closed at
radii \(0.01,0.02,0.05,0.10\). The radius-\(0.10\) formula used 1,316 pooled
triples and was replayed as UNSAT by the standalone Z3 binary.

```text
radius-0.10 result SHA-256
4029c236164c081f3db6332a45a2454a8dc7b033da6cb2b8b93be25b6f48ec5a
```

A different radius-\(0.05\) chamber generated the six-triple model and then
closed after 55 refinements and 2,793 triples:

```text
SHA-256 59574b1f5b935e5360fc3ac5484e6e52849445b129acdb55c7df04636b038d12
```

The five-triple record's radius-\(0.01\) box closed after five master checks
and 224 triples:

```text
SHA-256 dba7b61052cd30d265e1bae7de890899586dfde0cdbfcbe53ddf3abdaf77495c
```

These are solver-checked local closures, not proof certificates and not a
global theorem.

## Reverse formulation

`REVERSE_PARKING_LEMMA.md` proves that a parkable triple is equivalently a
complete EFX allocation with an owner-removable good. If

\[
  \sigma_h(X)=
  \min_{j\ne h}
  \left(v_h(X_h)-\tau_h(X_j)\right),
\]

then \(f\in X_h\) is removable exactly when \(v_h(f)\le\sigma_h(X)\).
The threshold-cycle theorem now closes the exchange step: orient each rigid
owner toward a threshold-maximizing target, rotate a directed cycle, and
strictly increase the sum of own-bundle thresholds. Hence a deletion-rigid
EFX allocation can exist, but not as a potential-maximal endpoint; some EFX
allocation in the same instance always has a removable good.

## Next decisive checks

1. Complete the full 40,824-onto formula and both 1,701-partition formulas.
2. Continue to a rational zero-EFX model or global UNSAT while retaining an
   unrestricted no-symmetry replay as an independent encoding target.
3. Independently replay any terminal result and freeze the SMT-LIB formula;
   an UNSAT solver response still needs a checkable LRA proof before theorem
   promotion.
4. Generalize the complementary-wall exchange from the certified local
   chamber into a shape-level covering lemma, or find a chamber in which the
   handoff fails.
5. Check the threshold-cycle theorem against prior literature before making
   a novelty claim.

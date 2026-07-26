# EFX Additive-Goods Campaign Log

Target: EFX existence, n=4 agents, additive valuations, indivisible goods (open).
Discipline: exact-verifier-first; nothing is a "witness" until verify.py AND verify2.py
agree, minimized, and hand-checkable.

## Verified pipeline calibrations (all match known theorems)
- n=2, m=3, K=3: UNSAT (2 agents safe — cut-and-choose) ✓
- n=3, m=5, K=3: UNSAT (3 additive agents safe — CGM) ✓
- n=4, m=7, K=3: UNSAT (m ≤ n+3 safe — Mahara) ✓
- n=4, m=8, K=2: UNSAT (bivalued safe — Amanatidis et al.) ✓

## New bounded no-go results (integer CEGAR, cp-sat, double-lex + 4-distinct-rows cuts)
- 2026-07-23: n=4, m=8, values in [1,3]: UNSAT (190 iters, pool 567, 56s).
  THEOREM (bounded): no additive EFX counterexample with 4 agents, 8 goods, values in {1,2,3}.
  Caveats: distinct-rows cut relies on <=3-types theorem (LEDGER to confirm exact statement);
  double-lex sound (Flener et al.). All-positive values => EFX0 = EFX+.

## Session 1 progress (2026-07-23, cont.)
- K=4 rung: UNSAT (576 iters, pool 1725, 25min). THEOREM: no counterexample n=4, m=8,
  values in {1..4}. K=5 launched.
- Near-witness ladder (all dual-verified by verify.py + verify2.py):
  count 18 (trackB anneal) -> count 5 -> count 4 (surrogate-objective anneal; robustness
  margin of survivors as tiebreak was the decisive lever).
  Count-4 instance: [[11,8,20,1,4,1,16,1],[16,49,32,2,16,2,60,1],
  [28,28,59,1,60,7,46,8],[10,12,24,1,59,1,17,1]]
- Structural discovery: survivor families are k-TREASURE allocations (k singleton bundles
  = strong-envy-immune + remainder split). Count-4 survivors = one base allocation +
  4 parking spots of a floater good. The hunt = the almost-full/charity gap made concrete.
- Exact local no-gos: BOX-UNSAT delta=6 around count-5 seed (CP-SAT 16s, pool 195).
  Two-treasure repair lemma + floater detonation system delegated to theory1.

## Session 1, continued
- Boundary intelligence (LEDGER '## Boundary intelligence'): monotone (4,8) UNRESOLVED —
  2604.18216 solved n=3 only; n>=4 counterexamples are algebraic extensions at m>=n+5.
  So additive (4,8) is the FIRST genuinely open additive cell (above Mahara m<=n+3), and
  our Z3 full-cell UNSAT would resolve it unconditionally. (4,9) also open; monotone
  witnesses exist there; additivizing them == the open problem itself (no shortcut).
- Second count-4 basin (trackB round 4, values<=100): dual-verified; survivors =
  THREE-treasure + block + floater(good7). Same terminal structure as basin 1.
- Exact local no-gos accumulated: tb5 delta=6 (pool 195); tb4b delta=10 + floater col
  FREE (pool 469); count-4 basin 1 with floater col 3 FREE 1..200, delta=8 (pool 579).
  The floater CANNOT be made a universal detonator in either count-4 basin — empirical
  support for a "parking always possible" lemma in terminal families.
- K=4 UNSAT (values {1..4} impossible at (4,8)); K=5 and (4,9) K=3 running.

## Running
- Integer ladder K=4 (n=4, m=8)
- Z3 continuous CEGAR: n=3 m=6 calibration; n=4 m=8 FULL CELL (UNSAT would prove
  "every 4-agent 8-good all-positive additive instance has an EFX allocation" — a new
  unconditional theorem; SAT+verify would be the counterexample)
- Track C boundary landscape (min #EFX0 hill-climb)
- Subagents: LEDGER (citations + prior-work check), verify2 (independent verifier),
  lifting (Track A: additivize the 2026 submodular/chores witnesses)
- (4,9) K=3 rung: UNSAT (448 iters, pool 1341, 18min). THEOREM: no counterexample n=4, m=9, values {1..3}.
- Peaks-family CEGAR: STALL at pool 1799 (master >900s). Pool persisted (peaks_pool.json); superseded by anatomy.py. NC-A encoding validated in-run.
- Spread-ratio residual family (theory1 PEAKS_WINDOW): UNSAT in 2s (pool 105). Peaks window closed at tested bands (identical: proven Theorem 2; spread: exact).
- G1 misaligned-signature family (private good 45-65 own/1-20 others + contested 40-60 + flat tails, NC-A): UNSAT in 35s (pool 365). The near-witness regime is closed at these bands. G2/G3 running.
- tb5 delta=15 finisher: STALL (master >600s at pool 2204) — partial; delta=6 exact UNSAT stands.

## Session 2 (2026-07-23, resume)
- STATUS VET: additive EFX n≥4 still OPEN (WebSearch, July 2026; latest partial results are
  EF2X for 4 agents 2412.00254, almost-full 2102.10654, bivalued ≤4 — none resolve the cell).
  No published resolution; hunt is live. Continue.
- Inherited runs: NO terminal witness anywhere; all verdicts UNSAT/BOX_UNSAT (bounded no-gos).
  All CEGAR runs are STALLING (superlinear master slowdown): Z3 full-cell (4,8) at iter540/
  pool2700/25000s (~7h, will NOT terminate as-is — unconditional theorem out of reach this
  route); K=5 integer ladder at pool3150/7762s; anatomy at pool6250/22900s; families G2_bumpy,
  cegar_local bd10, sweep still grinding. The realistic negative product remains the bounded-K
  ladder (K≤4 UNSAT proven; K=5 incomplete).
- PARKING-FLOOR LEMMA (new, results/PARKING_FLOOR_LEMMA.md): for a universal-min floater f and
  EFX₀ base B, #(EFX₀ completions of f) = #sources of B's plain-envy digraph. Envy-free base ⇒
  exactly (#agents) parkings ⇒ the observed count floor. Un-parkable ⟺ sourceless base ⟺ full
  plain-envy cycle. Verified on count-4 witness (predicted sources {0,1,2,3} = actual parkings).
  This is NC-D with an EXACT count and reduces single-floater EFX to the COUPLING CONJECTURE:
  "a sourceless base forces an EFX₀ allocation of some other shape." Prove ⇒ EFX exists (regime);
  refute ⇒ counterexample. Not closed.
- COUPLING refutation attempt: sourceless-base 8-good instance (base ({6},{2,4},{0,5},{1,3}),
  global-min floater good7) has 197 total EFX₀ (kills its 4 parkings, 197 elsewhere) — direct
  coupling evidence. Count-minimizer parkfloor.py seeded from near-witnesses AND this instance,
  9 background seeds, driving total count down; watching for sub-4 / count-0 (parkfloor_elites.jsonl).
- G2 bumpy family: killed at pool 5748/5hr (partial: no witness through 1150 iters; band covered piecemeal by sweep cells). bd10 d8 finisher: see json/log.
  Correction: the killed cegar_local was bd10 d8 mid-run (iter 1080, pool 5410, 7h, no witness found; no verdict reached). Superseded by anatomy (searches all values<=120 with skeleton constraint). tb5 d15 had already stalled earlier.

## Novelty correction (2026-07-23, ledger check)
- SOURCE LEMMA is a REDISCOVERY: = Mahara arXiv:2008.08798 Lemma 7, rooted in Lipton et al. EC 2004
  (envy-cycle swap preserves EFX, Pareto-dominates; acyclic envy graph WLOG). Cite, do not headline.
- Correction to framing: the safe ingredient is 'swap without adding a good', not completeness;
  Lemma 7 holds for partial EFX allocations too.
- Parking/slack framing = the known crux of the charity line (1907.04596, 2102.10654: maintain EFX +
  acyclic envy graph, allocate to a source; stuck at one leftover good for 4 agents).
- What remains genuinely novel if achieved: (a) unconditional resolution of additive (4,8) — never
  proven, our Z3 full-cell UNSAT or a witness would both be new; (b) extending Mahara-style case
  analysis from m=n+3 to (n,m)=(4,8); (c) a witness at (4,9)/(4,10)/(5,9); (d) the bounded
  exhaustion ladder + phase-diagram no-go map as computational results.

## Session 3 (2026-07-23, round 2)
- Killed stalled non-converging runs (Z3 full-cell, anatomy, cegar_local, families, sweep,
  source_probe) to free compute; kept K=5 (4,8) ladder grinding.
- GENERALIZED PARKING LEMMA (new, proven, machine-verified 16057/0, genpark.py): for ANY
  leftover f and EFX0 base B, #(EFX0 completions) = #(sources of the f-envy digraph), where
  f-envy strengthens plain-envy by max(0, v_k(f)-min_{g in Bi}v_k(g)). Universal-min f =>
  f-envy = plain-envy (recovers the count-source identity). NARROWING THEOREM: a counterexample
  needs every EFX0 base of every M\{f} to be f-envy-SOURCELESS. Un-parkability is a HIGH-VALUE
  floater phenomenon (universal-min un-parkable bases: 0 in 4000 random; need directed construction).
- COUPLING CONJECTURE evidence (coupling_fast.py, 2500 instances, 635 un-parkable bases):
  0 COUNTEREXAMPLES (every un-parkable base's full instance has EFX0 elsewhere, 635/635).
  Cycle-rotation mechanism recovers 342/635 (54%); all base-permutations 641/811 (79%); rest
  need a genuinely DIFFERENT partition. Welfare-termination gives a source (partial theorem) but
  EFX0 is owner-dependent so rotation does not preserve it -> NO simple rearrangement proof;
  witness hunt must confront full re-partition. Coupling conjecture true empirically, still open.
- n=5 ladder: (5,10) K=2 UNSAT in 1.8s (THEOREM: no counterexample n=5,m=10,values{1,2});
  (5,10) K=3 and (5,11) K=2 grinding. No witness anywhere.
- Artifacts: genpark.py, coupling.py, coupling_fast.py, nomin.py; PARKING_FLOOR_LEMMA.md updated.

## Correction 2 (rotation proof flawed)
- theory1's coupling sweep: naive envy-cycle rotation FAILS to preserve EFX0 in ~46% of tested
  configurations (owner-dependence of EFX0 under fixed bundle multiset). The in-campaign 'Claim 2'
  proof was wrong; the acyclic-envy-WLOG fact stands on Mahara 2008.08798 Lemma 7 (published proof),
  which we cite rather than rederive. Second error caught by empirics before external claim.
- PARKING_FLOOR_LEMMA (proven, novel-pending-check): for a universal-min good f, EFX0 completions of a
  base = number of envy-graph SOURCES; explains floor=4 (completely envy-free bases: 4 sources).
- MAHARA_EXTENSION: five-shape reduction proven (S0); coverage: 5111=3-dominant, 2222=flat,
  4211/3311=two-treasure; residual open core = tight-source 4211/3221 — matches search empirics.

## Session 4 (2026-07-23, round 3 — coupling proof landscape)
- Coupling conjecture now 0 CEX across ~1340 un-parkable configs. Mapped 3 proof routes, all fail:
  (A) canonical welfare potentials (util/Nash/leximin) are NOT EFX0 on the near-witnesses
  (EFX0 allocs are lumpy k-treasure, not welfare-optimal) — route dead. (B) cycle-rotation:
  welfare-max permutation always has a source (400/400, matches DAG argument) but is EFX0/parkable
  only ~97%; full rotation 100% on universal-min samples but 54% general — partial, no proof.
  (C) bounded local move: nearest EFX0 within Hamming <=3 of un-parkable base ALWAYS (90% dist 1);
  the dist-1 repair moves a non-floater good out of an envied bundle (93%), often its cheapest
  (60%) — structured but = restatement of conjecture, not a lemma.
- Witness/hard-core search: sourceless-seeded count-minimizer descended 197 -> 4, landed on the
  parking floor (3rd dual-verified count-4 instance, single-floater structure), never reached 0.
  Proof search = witness search, realized: directed search always returns to count = #agents.
- CONCLUSION: coupling conjecture true empirically, no clean proof via rotation/potential/local-move.
  EFX for 4 additive agents needs a genuinely new idea; parking toolkit provably insufficient.
  Solid deliverable remains the Generalized Parking Lemma. New: potential.py, route1.py.
- Ladders: n=5 K=3 (5,10) and K=2 (5,11) grinding (no verdict); K=5 (4,8) was stalled at pool 3150,
  killed. n=5 K=2 (5,10) UNSAT stands (round 2).

## Floor-trend result (2026-07-23, trackB + dual verification)
- Min EFX0 count over deep surrogate-anneal search: (4,8)=4, (4,9)=4, (4,10)=4 — all floors
  dual-verified on explicit instances. The floor is PINNED at n=4 (=agent count = parkings of a
  universal-min floater into a fully-unenvied base, per PARKING_FLOOR_LEMMA) while the allocation
  space grows 65k->1.05M. The annealer gains no traction toward 0 with more goods.
- Diagnostic verdict: 'holds' branch — evidence FOR additive-EFX existence at n=4 (all m tested).
- (5,9) floor still under-powered (best 12); deeper runs in flight.

## Variant upgrade (ledger, arXiv:2001.09838 reduction)
- Zeros are WLOG for additive: EFX0-with-zeros reduces to EFX+ all-positive at same (n,m)
  (MNW perturbation). ALL our all-positive UNSAT theorems upgrade to full EFX0-incl-zeros
  statements; Z3 (4,8) UNSAT would be the complete EFX0 resolution. Zeros probes killed
  ((3,6) UNSAT was redundant with CGM anyway). cegar_z3.py docstring caveat superseded.
- Parking-Floor Lemma: verified true by ledger; sufficiency = standard charity argument;
  iff-counting form is a minor original sharpening (check AAAI 33536 before claiming).
- Competition sweep July 15-23: clear; (4,8) additive uncontested.

## k-treasure ladder (theory2, RESIDUAL_ATTACK.md)
- Residual claim (4211/3221 sufficiency) REFUTED by dual-verified sole-shape instances
  (sole-2222/3311/5111 all satisfying the necessary conditions). Sampling artifact identified.
- LADDER LAW (empirical + partial proof): sole EFX0 shape = f(k universally-contested high goods):
  k=0 to 2222, 1 to 3221, 2 to 3311/4211, 3 to 5111 (3000/3000 in 3-peak regime). Every shape
  individually necessary. Witness must thread k~2 breaking 3221+4211+3311 at once while lumpy
  enough to kill 2222 and below 3 contested to kill 5111 — the named reason searches floor at 4.
- Proof obligation reframed: per-k feasibility, k=0..3. 0 EFX0-free in 18172 instances incl.
  6172 in the ambiguous-k danger zone.

## Peeling Theorem + corridor (theory1 PER_K)
- PEELING THEOREM proven: any dominant good (v_a(t)>=tau_a(M-t)) peels to a singleton + CGM on
  remaining 3 agents => EFX0. Witness has NO dominant good at all (strictly strengthens NC-A).
- Ladder k ill-defined for MISALIGNED instances (k(V)=4 nonsensical); per-k program covers aligned
  regime only. Open core = misaligned two-treasure NC-B corridor at zero slack. corridor.py CEGAR
  launched with no-dominant-good + no-universal-min encoded.
- (5,9) K=3 rung: UNSAT (1137 iters, pool 5088, 6.5h). THEOREM: no counterexample n=5, m=9, values {1..3}. First exact n=5 result; covers EFX0-incl-zeros via 2001.09838 reduction.
- (4,9) K=4 rung: UNSAT (697 iters total, pool 3669). THEOREM: no counterexample n=4, m=9, values {1..4}. Ladder now: (4,8) K<=4, (4,9) K<=4, (5,9) K<=3.

## Referee round 1 (2026-07-24) — all points verified before acceptance
- (5,9) K=3 DOWNGRADED to partial: distinct-rows cut = 5 types at n=5; 4-type profiles unsearched.
  Sound completion (duplicate-pair encoding, n5_fourtype.py) launched.
- Zeros-coverage claim WITHDRAWN for bounded-K rows (eps-perturbation escapes the value box);
  transfer valid only for unrestricted results (Z3).
- Rotation reversal: re-audit 34,538 cycle-rotations, 0 EFX0 breaks — pure rotation PRESERVES EFX0
  (Mahara Lemma 7 correct); the 46% stat was rotation+parking (coupling.py), mislabeled. My
  'Correction 2' was wrong and is withdrawn.
- Floor law reframed: empirical observation, prior art = Neoh-Teh AAAI 2025 (counting EFX).
  Basin-1 floater NOT universal-min (agent1: 2 vs min 1) — universal-min lemma doesn't cover it.
- 'flat=>2222' withdrawn ([100,1x7]x4: 2520 EFX0, all 3221 — verified). Three-dominant needs
  distinct agents/goods. Corridor reclassified as hypothesis. Mahara m<=n+3 = arXiv:2107.09901
  (strong variant stated there; variant flag closed); 2008.08798 = two-valuations/Lemma 7.
- Engine truth: anatomy STALL pool 14,654; corridor STALL pool 7,420; Z3 RUNNING pool 6,312.
- REVIEW.html rev.2 republished with executive claim replaced by referee's defensible version.

## Referee round 2 (2026-07-24)
- Four-type completion v1 UNSOUND (forced duplicated type lex-max — not WLOG; type multiplicity
  not relabelable). v1 UNSAT covers only that subclass. Corrected v2 (singleton-row ordering only,
  no column lex) relaunched from warm pool. (5,9) row stays PARTIAL until v2 terminates.
- Supporting docs bannered (rotation, identical=>2222, zeros caveat). Dominant-pair shape claim
  weakened (5111/4211/3311 possible). Over-broad statements tempered. Neoh-Teh Thm 3.3 contains
  the universally-zero case of the parking-floor counting (referee-checked). Citations fixed:
  Avi Cohen (2102.10654); HV-first order (2410.13580); Flener, Plaut-Roughgarden, Branzei added.

## Count-hunt round (Conjecture 6.1 campaign)
- (5,8): TWO instances dual-verified at exactly 5 = n EFX0 allocations (ch5_A, ch5_B in results/).
  Improves the known minimum-count upper bound at m=n+3, n=5 from n!=120 (and random-search 14)
  to n=5 — tight if Neoh-Teh Conjecture 6.1 holds. No count < n found anywhere yet.
- trackB's (5,9) count-12 instance verified exactly 12 by counthunter; (5,9) descent continues.
- (5,8) floor-tightness: radius-1 exhaustive scans (2360 neighbors each) around ch5_A and ch5_B:
  ZERO neighbors below count 5; both strict local minima. Three signals agree floor = n at (5,8).
- Negative datum: appending any 9th good to A/B jumps count to 24-422 — m=n+3 tight structure
  does not extend to m=n+4 by extension; (5,9) fresh descent relaunched (best verified still 12).
- (6,9): pivoted to cap-accelerated parking-structured CONSTRUCTION sweep (anneal impractical).

## theory3 delivery (COUNT_LB_M_N3.md)
- (4,7) floor=4 empirical; tight set characterized EXACTLY: star join-graph, envy-free 3111
  base + floater, 66/66 verified; 2221 never essential at the floor.
- Named obstruction to unconditional >=4: Lemma 3.9/Algorithm-1 constructive core breaks (pool
  grows 3->4; naive analog EFX only 6.5% vs 98% at m=n+2).
- CONDITIONAL THEOREM (rigorous): envy-free 3111 base => >=4 EFX0. Sole gap = crux lemma
  'every (4,7) instance admits such a base'. base_cegar.py launched (K=8) to bounded-verify
  or refute the crux. FALSE-BY-TEST logged: parking-lifting count bound (count can DROP when
  adding back a universal-min good: 12 -> 5 example).

## Counting-CEGAR first verdict (2026-07-24)
- THEOREM (bounded): every (4,7) instance with values <=4 has >=4 EFX0 allocations. First exact
  verification of Neoh-Teh Conjecture 6.1 beyond the proven m=n+2 regime; method = novel
  slot-protected counting-CEGAR (countcegar.py; 260 iters, pool 1295, ~1h). K=6 running.
- Structured no-base instance found (4 distinct rows, spread>=4): count 130 — dichotomy-consistent
  (no envy-free 3111 base => abundance). Instance in results/base_cegar_K8.json; forwarded to theory3.

## Tight-family verdict (theory3, TIGHT_FAMILY.md)
- min-count <= n at m=n+3 PROVEN for n=4 ((4,7) witness, dual-verified below) and n=5 (ch5_A/B).
  >= n parking direction rigorous+uniform. Uniform all-n family blocked by two verified
  mechanisms: symmetry-multiplicity + singleton-immunity derangements (knife-edge variety,
  needs all-distinct dense contested values). Closure path: Sidon/geometric formulaic scheme;
  n=6 witness = third data point.

## TIGHT (6,9) WITNESS (2026-07-24, anatomy-CEGAR, dual-verified)
- Exactly 6 = n EFX0 allocations at (6,9); values in results/tight69_witness.json. Third data
  point: min-count upper bound at m=n+3 now n for n=4,5,6 (published bound: n!). Knife-edge
  anatomy exactly as TIGHT_FAMILY.md predicted (hub 204 vs singletons 191-196 for the hub agent).
- TIGHT_FAMILY v2: hub gadget FORMULAIC (3 proven conditions: distinct knife-edge gaps; hub-good
  > max gap; own-singleton > hub total). Non-hub remainder = generic O(n^2)-inequality variety,
  no closed form (necessity!=sufficiency: clean hub + uniform rest gives 28 not 4, param-invariant).
  <= n PROVEN n=4,5,6 via witnesses; all-n theorem routed to existence/dimension argument (approved).
- TIGHT_FAMILY v3: directed interpolation descent WORKS (28->4); 4th condition found (all
  non-hub agents value every singleton highly => kills all 2-2-2). Residual = (n-1)x(n-1)
  singleton-permutation S-matrix design; diagonal-dominant bottoms at exactly 2n; blocking
  mechanism = floater-elsewhere weakens hub knife-edge. S-matrix push approved (per-agent
  floater window analysis).
- CORRECTION (theory3 self-caught, TIGHT_FAMILY s12): 'condition 4' (all-singletons-high) is NOT
  universal — n=6 witness violates it (mixed low cross-values). Only the THREE hub conditions are
  witness-consistent; non-hub block is generic. Condition 4 demoted to n=4 search heuristic.
  Paper correction dispatched to writer.
- n=7: no cheap start (structured template >=200; extend-n6 >=60); targeted 16-var anneal running
  (2h budget, ~10s/eval). Plateau near 2n=14 would itself confirm residual-class law at n=7.
- n=7 verdict: NO witness — structural compute wall (cap-blind objective at 282M assignments;
  160 evals flat at cap). Decision: ship paper with 3 data points; anatomy-CEGAR collector build
  deferred unless a reviewer requires n=7. Paper n=7 placeholder -> honest outcome statement.
  theory3's counting work COMPLETE.
- Z3 (4,8) PAUSED by decision (memory-pressure risk to near-term runs; pool persisted ~6.8k).
  Resume solo after K6/four-type/split land: python3 -u cegar_z3.py --n 4 --m 8 --add 25 --out results/z3_n4_m8.json

## (5,9) K=3 THEOREM COMPLETE (2026-07-25)
- Corrected four-type run: UNSAT, 968 iters, pool 10,385 (~7x the unsound v1's 1,505 —
  validates referee round 2's concern as material). Composite now sound: <=3 types (HV et al.
  2410.13580) + exactly-4-types (duplicate-pair encoding, singleton-rows-only order, no col-lex)
  + 5-distinct-types (pool 5,088). THEOREM: no EFX0 counterexample at n=5, m=9, values {1..3}.
- Referee re-send confirmed as round-3 duplicate EXCEPT two new items: (a) four-type encoding
  soundness ratified (its UNSAT has since landed => (5,9) promotion valid per referee's own
  criterion); (b) Z3 necessary-condition cuts scope-guarded to n==4, m<=8 (Peeling needs 3-agent
  remainder; universal-min parking needs Mahara base m-1<=n+3). Patched while paused.

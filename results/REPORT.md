# EFX Additive Goods (n=4): Campaign Report (working draft)

Status: 2026-07-23, session 1. Target: EFX0 existence, 4 agents, additive positive
valuations, first open cell (4,8). No resolution yet; substantial no-go map built.
All computational claims dual- or exactly verified; novelty checked against literature.

## 1. Position of the problem (verified intelligence)
- Additive goods n>=4 is the last open EFX tower (monotone/submodular fell 2604.18216,
  2605.06451; additive chores fell 2606.08872).
- (4,8) = m=n+4 is the FIRST open additive cell: n<=3 (CGM), m<=n+3 (Mahara), <=3 types,
  bivalued all safe; monotone (4,8) also unresolved (SAT work was n=3 only).
- Known crux (charity line, 1907.04596 + 2102.10654): maintain EFX + acyclic envy graph,
  park goods at sources; for 4 agents this gets stuck at exactly ONE leftover good.
  [In-campaign rederivation attempt had a FLAWED proof (rotation does not preserve EFX0, 46% fail rate
  in coupling sweep); the acyclic-envy fact stands on Mahara Lemma 7. Identified as
  Mahara 2008.08798 Lemma 7 / Lipton et al. 2004 by novelty check BEFORE claiming.]

## 2. New bounded no-go theorems (CP-SAT CEGAR, exact; calibrated on 4 known theorems)
- No counterexample at (4,8) with values in {1..3} (56s), {1..4} (25min, pool 1725).
  K=5 running. No counterexample at (4,9) with values in {1..3} (18min, pool 1341).
- Sound cuts used: 4 distinct rows (<=3-types theorem), double-lex (Flener et al.).

## 3. Near-witness structure (dual-verified by two independent verifiers)
- Surrogate-objective annealing (EFX count + survivor-fragility tiebreak) drives
  random instances (count ~300-2500) down a ladder 184 -> 118 -> 18 -> 5 -> 4.
- FLOOR = 4 at (4,8): six independent basins all bottom at exactly 4; flat at 4 for
  (4,9) (first pass). Two count-4 instances known (different basins).
- Terminal structure is universal: k singleton "treasure" bundles (strong-envy-immune)
  + block split + one FLOATER good with 4 parking spots = the 4 survivors. Bases are
  completely envy-free; the floater parks anywhere. Count<4 requires an instance whose
  every EFX0 base is fully envy-cycled — i.e. defeat of the charity invariant.
- Witness-necessary conditions (proven in-campaign; NC-A also encoded in masters):
  at most one agent with a good >= half its total (NC-A); no good that is every agent's
  minimum (parking corollary); pairwise non-proportional rows.

## 4. Exact local/family exhaustions (all UNSAT, no witness)
- Boxes around near-witnesses: L-inf 6 (count-5), 10 + floater-column-free (count-4 #2),
  8 + floater-free (count-4 #1). Partial: L-inf 15 (stall, no witness through pool 2204).
- Families: spread-ratio peaks; G1 misaligned-signature (the near-witness template);
  6 phase-diagram cells incl. gap-closing signature (all seconds-fast UNSAT);
  G2 bumpy partial (no witness through pool 5748). Identical-peaks regime PROVEN safe
  (ladder argument; consistent with known results).

## 5. Open engines (running)
- Z3 LRA full-cell CEGAR (unconditional: UNSAT resolves (4,8) for ALL positive reals;
  per-agent scaling + Hadamard rationality note make integer/real equivalent).
- Anatomy CEGAR: master forces the witness skeleton (EFX0 base + all-parkings-fail),
  values<=120; pool 6300+.
- park_hunt: values<=30 + all proven necessary conditions.
- Ladder K=5; trackB deep anneals at (4,9)/(4,10)/(5,9) with floor-trend diagnostic.
- theory1: Mahara-technique case analysis aimed at proving "EFX exists at (4,8)".

## 6. Assessment
Evidence strongly favors (4,8) being EFX-safe: every structured family and local box is
UNSAT; the floor-4 phenomenon is exactly the known charity obstruction resisting; the
trend (4,8)->(4,9) is flat, not dropping. The genuine-breakthrough paths, in order:
(a) unconditional (4,8) resolution by Z3 UNSAT or by Mahara-extension proof (both would
be new results); (b) witness at larger cells if the deep scaling runs break the floor;
(c) failing both, the bounded ladder + phase diagram + floor structure publishes as a
computational study of the first open cell. Rediscoveries caught pre-claim: 1 (Lemma 7).

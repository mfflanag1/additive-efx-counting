> **SUPERSEDED NOTE (2026-07-24):** the zero-values caveat below is obsolete for UNRESTRICTED
> results: the eps-perturbation reduction (arXiv:2001.09838) transfers an unrestricted all-positive
> existence theorem to nonnegative valuations. (Bounded-K searches remain positive-integers-only.)

# A value-magnitude bound for minimal additive EFX counterexamples

**Lemma.** Fix n agents and m goods. If some additive instance with all-positive real
values admits no EFX0 allocation, then some instance with positive INTEGER values
bounded by B(n,m) = (nm)^{nm/2} admits none either. Hence "EFX0 exists for all
all-positive additive (n,m) instances" is decidable by finite search, and any exact-LP
(LRA) refutation over the reals is unconditional.

**Proof.** For an instance V ∈ R_{>0}^{n×m} and a complete allocation A with bundles
X_1..X_n, A fails EFX0 iff some triple (i,j,g), g ∈ X_j, has
    v_i(X_i) − v_i(X_j∖{g}) < 0,
a strict linear inequality in V with coefficients in {−1,0,+1} (goods in X_i get +1,
goods in X_j∖{g} get −1; note g itself cancels).

V is a counterexample iff EVERY allocation fails, i.e. iff there is a choice function φ
assigning to each of the n^m allocations a violated triple, with V in the open polyhedron
    P_φ = { V : c_{A,φ(A)} · V < 0 for all A,  V > 0 }.
The counterexample set is the (finite) union of the P_φ. Suppose some P_φ ≠ ∅. Add the
per-row normalization Σ_g v_i(g) = 1 (EFX0 is invariant under per-agent positive scaling,
so P_φ is a cone per agent-row and normalization preserves nonemptiness). Consider the LP
    max δ  s.t.  c_{A,φ(A)} · V ≤ −δ ∀A,   v_i(g) ≥ δ ∀i,g,   Σ_g v_i(g) = 1 ∀i.
P_φ ≠ ∅ forces optimum δ* > 0, attained at a basic feasible solution. Every basis matrix
has entries in {−1,0,+1}, dimension ≤ nm+1, so by Hadamard its determinant has absolute
value ≤ (nm+1)^{(nm+1)/2}; by Cramer the BFS coordinates are ratios of such determinants.
Clearing denominators (multiply each row by the common denominator; per-agent scaling
invariance again) yields a positive integer instance with entries ≤ (nm)^{nm/2} up to the
stated normalization of the bound, which still lies in P_φ (the inequalities are scale-
invariant per row and are satisfied with margin δ*). ∎

**Consequences.**
- (n,m) = (4,8): B ≈ 32^16 ≈ 1.2·10^24 — astronomically beyond a K-ladder, so bounded-K
  UNSAT results remain conditional. BUT:
- The Z3 LRA CEGAR (cegar_z3.py) works directly over the reals with exact arithmetic and
  strict inequalities, so its UNSAT verdict resolves the (n,m) cell UNCONDITIONALLY for
  all-positive values — no magnitude assumption. The lemma guarantees that its SAT verdict
  yields a rational (hence integer) witness.
- Zero-valued goods are outside this statement (EFX0 vs EFX+ diverge there); the all-
  positive case is the standard hard core (any EFX+ counterexample with zeros restricts,
  after deleting zero-columns per... NOTE: deletion changes other agents' values — do NOT
  claim a reduction from zeros to positive; left open, flagged.)

Status: statement + proof drafted 2026-07-23, needs one careful pass on the constant and
the normalization step. Novel per LEDGER.md intelligence question B (no published bound).

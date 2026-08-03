# Universal-Threshold Balanced Gate

**Status:** closed by a cap-free, proof-checked computer-assisted theorem  
**Scope:** strict common favorite, four agents, nine goods  
**Not claimed:** the full common-favorite dichotomy or general additive EFX

## Basic explanation

Try to isolate the common favorite \(f\) for one agent and give the other
eight goods to the remaining three agents. The singleton owner accepts a
residual partition exactly when each residual bundle becomes worth at most
\(f\) after its least-valued good is removed.

This file studies the clean extreme in which every possible singleton owner
rejects every residual partition on that scalar test alone. The goal is to
prove that such a profile must instead have a balanced complete EFX
allocation of shape \(3+2+2+2\).

## Exact one-row reduction

For an agent, sort the eight residual values as

\[
x_1\ge x_2\ge\cdots\ge x_8,\qquad F=v(f).
\]

The full set of 966 residual partitions is unnecessary. The owner rejects
every residual partition if and only if

\[
x_5+x_6+x_7>F
\quad\text{and}\quad
\bigl(x_3+x_7>F\ \text{or}\ x_4+x_5>F\bigr).
\tag{1}
\]

The proof optimizes the \(3+3+2\) and \(4+2+2\) shapes exactly, then converts
every safe partition in the other three shapes to one of those two without
increasing its threshold. See
[OWNER_THRESHOLD_SHAPE_ENVELOPE.md](OWNER_THRESHOLD_SHAPE_ENVELOPE.md).

There is also an exact sorting-free form. Make a graph on the eight residual
goods, joining two goods when their pair value exceeds \(F\). Equation (1)
is equivalent to both of the following:

1. every four residual goods contain a triple worth more than \(F\); and
2. at least three pair-graph vertices have degree at least six, or at least
   four vertices have degree at least four.

The proof and a 2,695-case regression audit are in
[OWNER_THRESHOLD_PAIR_DEGREE_ENCODING.md](OWNER_THRESHOLD_PAIR_DEGREE_ENCODING.md).

Equation (1) has two useful density consequences:

\[
x_5>F/3,\qquad \sum_{k=1}^8x_k>7F/3.
\]

## Half-favorite dichotomy

Let

\[
H_i=\{g\ne f:2v_i(g)>v_i(f)\}.
\]

The disjunction in (1) implies \(|H_i|\ge3\) for every agent. Hall's theorem
therefore gives exactly two cases:

1. the four agents have distinct representatives \(q_i\in H_i\); or
2. every \(H_i\) is the same set of exactly three goods.

The second case is closed. A Hall matching constructs four valid
anchor--low pairs and one low floater. Choosing a lexicographically maximal
valid state with the intended host last proves that the floater parks
safely. The cap-free proof is
[COMMON_THREE_LEXICOGRAPHIC_PARKING_LEMMA.md](COMMON_THREE_LEXICOGRAPHIC_PARKING_LEMMA.md).
Matching-clause and Hall-selector QF_LRA encodings independently return
UNSAT on all 240 anchor-separated balanced partitions; their frozen audit is
[efx49_common_three_dual_encoding_audit.json](efx49_common_three_dual_encoding_audit.json).

## Universal-threshold branch closed

The distinct-representative branch, and in fact the entire branch defined
by (1), is now closed by the
[strict-common-favorite universal-threshold theorem](COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_THEOREM.md).
Choose one bottom-two residual pair for each agent. A pair shared by at least
three agents is handled by the three-agent-bottom conversion theorem.
Otherwise an exhaustive multigraph census gives 20 canonical patterns:
two of type $2+2$, seven of type $2+1+1$, and eleven with four distinct
edges. Every pattern has a proof-checked favorite-triple/full-cell or
favorite-pair-conversion theorem. The aggregate audit is
[efx49_common_favorite_universal_threshold_efx_audit.json](efx49_common_favorite_universal_threshold_efx_audit.json).

The earlier distinct-representative work below remains useful proof-mining
and boundary evidence. In particular, the one-row profile

\[
(F;x_1,\ldots,x_8)=(7;4,4,4,4,4,2,2,1)
\]

satisfies (1), but four valid owner-floor pairs need not exist. This explains
why the successful proof had to range over favorite-triple cells and the
complete conversion closures rather than only four owner-floor pairs.

The triple-aware owner-floor starting state is now analytically proved.
Under (1) and fixed representatives \(q_i=i+1\), some partition

\[
\{f,p\}\mid P\mid Q\mid T,\qquad |P|=|Q|=2,\quad |T|=3,
\]

can be assigned so every owner receives value at least its favorite. The
cap-free construction is
[DISTINCT_HALF_DENSITY_FLOOR_LEMMA.md](DISTINCT_HALF_DENSITY_FLOOR_LEMMA.md).
It only uses the tail inequality \(x_5+x_6+x_7>F\), three half-favorites
per row, and the saturating matching. The matching-clause and
Hall-obstruction exact-real encodings remain independently frozen at
[efx49_distinct_half_floor_dual_encoding_audit.json](efx49_distinct_half_floor_dual_encoding_audit.json).
An assumption-core minimization leaves only 22 favorite-pair partitions:
[efx49_distinct_half_floor_minimized_core.json](efx49_distinct_half_floor_minimized_core.json).
Those 22 partitions are the current finite proof-mining target.
It is also not EFX: in any such state, pair targets are automatically safe,
but a nonhost agent may still strongly envy the triple after one good is
removed. The live conversion problem is to choose a lexicographically
maximal owner-floor state and rehouse the triple owner after an envier takes
its preferred two-good remainder.

A fixed-host version of that lexicographic rule is false even in strict
generic position: the audited boundary has 369 favorite-pair balanced EFX
partitions, but its fixed-host lexicographic maximum is not EFX. See
[efx49_distinct_half_fixed_host_lex_boundary_audit.json](efx49_distinct_half_fixed_host_lex_boundary_audit.json).
The alternating exchange must therefore allow the triple owner to change.

Ordinary Nash-product maximization over owner-floor allocations is also
false, as is maximizing the product of each owner's surplus over its
favorite. In 1,000 deterministic exact-branch profiles, the two weak claims
fail on 21 and 22 profiles respectively; some maximizers are non-EFX even
though the same profile has balanced EFX allocations. The frozen
falsification is
[efx49_nash_floor_candidate_audit.json](efx49_nash_floor_candidate_audit.json).

Matching rank was tested as a replacement for owner utility. On the
840 favorite-pair partitions, connect states by one shape-preserving
single-good exchange and assign each state the maximum matching rank of its
exact EFX-feasibility graph. The proposed cap-free candidate said every
constant-rank plateau below rank four has an exit to higher rank. Four hard
profiles and 256 deterministic exact-branch profiles passed the original
stress test, but the conjecture is now exactly refuted. A strict
branch-valid profile has no rank-four state in the entire 840-partition
universe. All 324 of its complete EFX allocations instead put the favorite
in a triple with the same two common low goods. A separate strict profile
also refutes the former radius-two strengthening. The precise boundaries
are in
[DISTINCT_HALF_RANK_AUGMENTATION_GATE.md](DISTINCT_HALF_RANK_AUGMENTATION_GATE.md).

The exact favorite-triple conversion criterion is now
[FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md).
If two goods \(a,b\) join the favorite, the triple is feasible for every
agent, and the other three pairs only need a Hall matching to three agents
at threshold \(F_i+\max\{v_i(a),v_i(b)\}\). Requiring every pair to clear
this threshold for every observer is a stronger sufficient special case,
proved in
[COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md](COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md).
The next gate is to prove the exact dichotomy “favorite-pair EFX or
favorite-triple Hall matching.”

On the strictly positive integer domains through cap 6, the stronger
full-cell form of this dichotomy is now independently closed by CP-SAT,
QF_LIA, and threshold-CNF/CaDiCaL replays with checked DRAT proofs. The
cap-5 proof has a deletion-minimal 17-partition core; the cap-6 extension
has a deletion-minimal 21-partition core. These are finite-domain theorems
inside the present branch, not arbitrary-real closure; see
[DISTINCT_HALF_FULL_CELL_CAP5_THEOREM.md](DISTINCT_HALF_FULL_CELL_CAP5_THEOREM.md)
and
[DISTINCT_HALF_FULL_CELL_CAP6_THEOREM.md](DISTINCT_HALF_FULL_CELL_CAP6_THEOREM.md).
The 17 cap-5 literal templates fail already at cap 6 even though the full
cap-6 theorem holds. Their symmetry-aware replacement is a six-orbit family
of 624 favorite-pair partitions, but that selection statement is exactly
refuted at cap 20. The refuting profile has no full Hall cell, 45 repairs
in two omitted orbits, and 900 complete EFX allocations. Thus only the
selector fails, not EFX existence; see
[DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md](DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md).

A cap-free conversion theorem now closes every profile in which some pair
of residual goods is bottom-two for at least three agents. For any fixed
pairing of the other six goods, either that pairing has the required Hall
matching or one of six favorite-pair conversions supports EFX. The failed
pairings inject into distinct conversions, giving
$P_f+H_{a,b}\ge15$. Consequently, zero favorite-pair repairs force a full
Hall cell. Cardinal and sorting-network Z3 encodings, pinned cvc5, and all
five canonical Hall-role cells return `unsat`; the formal proof-checking
record is in
[THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md](THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md).
The live branch therefore has no pair shared as bottom-two by three agents.
Selecting one bottom pair per agent leaves only the sharing patterns $2+2$,
$2+1+1$, and $1+1+1+1$. Their exhaustive 20-pattern multigraph census and
the first cross-pair solver boundaries are recorded in
[BOTTOM_PAIR_MULTIPLICITY_GATE.md](BOTTOM_PAIR_MULTIPLICITY_GATE.md).
The overlapping-$2+2$ pilot now has four distinct three-repair profiles from
annealing and CP-SAT. Each is an exact $12+3$ Hall/conversion equality case,
but no positive floor has been proved.

The stronger common-low sufficient version now has a compact exact-real
boundary with 24 diversified favorite-pair cuts and 9 triple-repair cuts;
Z3 returned `unknown` after 300 seconds. Adversarial exact-census search also
reached a one-repair knife edge with zero favorite-pair EFX partitions and
252 complete EFX allocations. See
[DISTINCT_HALF_CONVERSION_DICHOTOMY_GATE.md](DISTINCT_HALF_CONVERSION_DICHOTOMY_GATE.md).
This does not prove the stronger dichotomy, but it reduces its proof-mining
target to forcing even a unique all-safe repair. If that sufficient claim
fails, the exact agent-relative Hall alternative remains open.

The hard zero-favorite-pair boundaries share a full 15-pairing Hall cell,
but three fixed universal acceptors are not forced, nor is acceptance of
each residual edge by three agents. Both stronger conditional routes now
have strict counterexamples. The surviving sufficient form is the
[two-core/Tutte corollary](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md): two
agents accept every residual edge and the graph of edges rejected by both
outsiders has no perfect matching. Its sharp boundary is
[efx49_distinct_half_two_core_boundary_audit.json](efx49_distinct_half_two_core_boundary_audit.json).
Restricting the two-core search to representative lows and complementary
agents is also exactly refuted: the strict boundary in
[efx49_distinct_half_canonical_two_core_boundary_audit.json](efx49_distinct_half_canonical_two_core_boundary_audit.json)
has its unique witness at nonrepresentative lows (5,6).
Direct negation of the two-core target remains unresolved: exact-real
matching and Hall CEGAR reached 40- and 24-cut boundaries, while a full
cap-20 CP-SAT solve returned `UNKNOWN` after 300 seconds. The replayed
decision ledger is
[efx49_distinct_half_two_core_decision_boundary_audit.json](efx49_distinct_half_two_core_decision_boundary_audit.json).

Two stricter observer-independent normal forms are false even for
row-distinct profiles with distinct item values. The exact boundaries and
the replacement dichotomy are in
[DISTINCT_HALF_FAVORITE_GATE.md](DISTINCT_HALF_FAVORITE_GATE.md).

The theorem does not finish the full common-favorite target.
The mixed case still permits a residual partition to pass the owner
threshold while its three-resident feasibility graph fails Hall's
condition.

## Exact decision workbench

The script
[run_universal_threshold_balanced_cegar.py](../tracks/parkability/run_universal_threshold_balanced_cegar.py)
encodes (1) with an exact sorting network, optionally fixes a
without-loss-of-generality half-favorite matching
\(q_i=i+1\), and learns balanced-partition obstructions.
The same workbench now exposes the equivalent sorting-free four-set and
pair-degree encoding above. The corrected Hall-layer and local-rank
diagnostics use that cardinal form and the full four-bundle EFX-feasibility
graph; pair feasibility depends on both the favorite and the triple's
top-two value, so the triple is not treated as universally feasible.

The first fixed-representative rational model supports 375 of the 1,260
balanced partitions. After 64 of those partitions were obstructed, Z3
returned unknown at 300 seconds:
[efx49_universal_threshold_distinct_reps_cegar_session1.json](efx49_universal_threshold_distinct_reps_cegar_session1.json).
Loading all 375 repairs and solving from that boundary returned unknown at
600 seconds under both matching-clause and Hall-selector encodings:

- [efx49_universal_threshold_distinct_reps_seeded_cegar_session1.json](efx49_universal_threshold_distinct_reps_seeded_cegar_session1.json); and
- [efx49_universal_threshold_distinct_reps_seeded_hall_session1.json](efx49_universal_threshold_distinct_reps_seeded_hall_session1.json).

As a separate stress test, seeding all 514 balanced repairs of the
balanced-only boundary profile also returned unknown at 600 seconds:
[efx49_universal_threshold_balanced_envelope_seeded_cegar_session1.json](efx49_universal_threshold_balanced_envelope_seeded_cegar_session1.json).
These are live exact-real boundaries, not counterexamples and not theorem
verdicts.

The old direct formulas returned `unknown`, but adversarial integer search
subsequently produced exact rational witnesses. One refutes radius-two
augmentation; another refutes the full favorite-pair rank conjecture.
Independent enumeration over all 840 and 1,260 relevant partitions, plus
literal enumeration over all \(4^9\) assignments, freezes the trust
boundary. See
[DISTINCT_HALF_RANK_AUGMENTATION_GATE.md](DISTINCT_HALF_RANK_AUGMENTATION_GATE.md)
and
[efx49_distinct_half_favorite_pair_rank_boundary_audit.json](efx49_distinct_half_favorite_pair_rank_boundary_audit.json).

Any zero-balanced model must be audited against all 1,260 balanced
partitions and all \(4^9\) labeled allocations. Any UNSAT endpoint requires
an independent encoding or proof-producing replay before it is promoted to
a computer-assisted theorem.

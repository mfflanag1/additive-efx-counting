# Physical cycle release: original-floor entry beyond an assumed GG layout

16 October 2026. Continuation of A1 from checkpoint `2930168`.

## Frozen attack and permitted boundary

Start with the original selected allocation O, not numerical BASE. Four positive
additive, bundle-nondegenerate agents; a fixed priority pi; O globally maximizes that
priority over all partial EFX allocations. Assume its safe charity is {p}. A0 gives
this singleton condition if complete EFX does not exist, but the lemmas below also
apply when it is assumed directly in an instance with complete EFX.

Here EFX compares assigned owner bundles only; it imposes no charity comparison.
The selected original O has safe singleton charity by the declared premise. A new
partial EFX exit may have larger or envied charity: A0's selection domain includes
all partial EFX allocations, not just those with safe singleton charity.

The immediate target is to construct actual support states and exact observer/floor
inequalities from every overlapping-charity cycle. Success means a genuine legal
exit or a physically derived residual problem. It does not mean renaming this
residual as the old twelve-role master or asserting that the residual is closed.

Two-sided routes:

1. Canonical physical cycle and priority-compatible release; derive all deficit and
   observer inequalities without packet-cardinality assumptions.
2. Independent attack on contracting ordinary-edge chains while retaining original
   floors; exact obstruction if an unconditional contraction fails.
3. All-genuine cross-residual pools and the precise role of BCFF's bottom-edge lemma;
   do not assume common-safety of an entire demand pool or a full owner matching.

Calibration is the existing exact nine-good global maximum. All choices in its
augmented minimal-core graph must be retained. No long search, new fixed template
menu, or claim of complete-EFX nonexistence is authorized by a failed calibration.

## 1. Canonical cycle from the full physical graph

Use the [A1 physical-core construction](PHYSICAL_ADMISSION_A1_20261016.md), retaining
every minimal envied core and every champion. An edge i->j is decorated by its actual
O-common-safe core C contained in O_j union {p}. Call the edge G if p is in C,
and E otherwise. An E core is exactly O_j. A G core has the form R_j union {p},
where O_j=R_j disjoint-union D_j and both parts are nonempty. The subscript j below
always refers to the decomposition chosen by the single incoming cycle edge.

Choose a decorated simple cycle minimizing, in order: its length, its number of G
edges, and a fixed deterministic label order. A1 guarantees a cycle exists and every
cycle has at least two G edges. Thus 2<=k<=ell<=4, where k is the G count and ell the
cycle length.

**Lemma 1 (chordless original-floor cycle).** There is no champion edge between cycle
vertices except the selected successor direction (parallel core choices may exist).
There is no ordinary envy edge parallel to a selected G edge. For each selected
G edge i->j,

    v_i(D_j) < v_i(p),       v_j(D_j) > v_j(p).

**Proof.** Self edges are already excluded by A1's global-maximality argument. A
non-successor edge between distinct cycle vertices would close a shorter directed
cycle, contradicting the first minimization. If an
ordinary parallel edge existed, its common-safe whole-target core would give a
decoration with the same cycle length and one fewer G edge. Hence
v_i(O_j)<=u_i(O)<v_i(R_j)+v_i(p), yielding the first inequality. The second is A1's
no-self-champion residual inequality, strict by nondegeneracy. All quantities are
values of original disjoint sets. No intermediate base or rescaling is involved. QED.

For an all-G canonical cycle these conditions establish BCFF Definition 3.9's good
cycle. The full minimal-core graph, rather than a single arbitrarily selected core
per target, is necessary for the absent-chord statement. BCFF's core definition
allows arbitrary common-safe envied subsets; monotonicity identifies these with
our minimal envied subsets. Its all-G bottom-edge results do not assert a mixed
ordinary-edge contraction. [Primary source, section 2.3 and Definition 3.9](https://arxiv.org/pdf/2102.10654v2).

## 2. Release exactly the duplicated charity uses

Let I be the cycle's owners, sigma its successor map, and Gsrc the sources of its
G edges. Let a be the earliest owner of I in the original priority. Choose a winner
w in Gsrc subject to the rule: if a belongs to Gsrc, set w=a; otherwise any w in
Gsrc is allowed. Define a physical allocation Y(w):

- Y_i=O_i for i outside I;
- Y_i=O_sigma(i) on an E edge;
- Y_w=R_sigma(w) union {p};
- Y_i=R_sigma(i) on every other G edge.

Put D_j in charity for every G target j. These sets account for all goods exactly
once; they are an actual allocation, not independently chosen observer marginals.
The charity is the union of the k residual packets, and p itself is allocated.

**Theorem 2 (physical release and localized underpayment).** Every displayed bundle
is O-common-safe. All E sources and w strictly improve, all nonparticipants are fixed,
and precisely k-1 agents are underpaid: the set U=Gsrc minus {w}. For i in U,

    delta_i = u_i(O)-v_i(Y_i),       0 < delta_i < v_i(p).

Y(w) strictly improves O in priority pi. Every EFX violation of Y(w) has its observer
in U. For every such observer i, target t, and deleted physical good g in Y_t,
the positive violation amount satisfies

    0 < v_i(Y_t minus {g})-v_i(Y_i) <= delta_i < v_i(p).

**Proof.** Distinct cycle targets are disjoint; only the winner receives p. For G
targets, R_j and D_j partition O_j; E targets are assigned whole. This proves
conservation and the charity formula. Original bundles are common-safe by EFX;
the winning core is common-safe by definition; every other R_j is a subset of an
original bundle and therefore is common-safe as well.

An E source desires its whole target, and w desires its selected core. For an unpaid
source, R_j is a proper subset of O_j, so original EFX gives v_i(R_j)<=u_i(O).
Distinct-subset nondegeneracy makes this strict (i differs from j). Desire for
R_j+p gives delta_i<v_i(p). The earliest changed owner a is either an improving E
source or the winner by construction, proving strict lexicographic improvement.

Every paid or fixed observer retains at least her original utility, while every
assigned bundle is common-safe at that original threshold; therefore she satisfies
all EFX comparisons. For i in U, common-safety bounds every deletion value by
u_i(O). Subtract v_i(Y_i)=u_i(O)-delta_i to obtain the displayed shortfall bound. QED.

The construction and weak deficit inequalities remain valid with ties, but zero
deficits then need not count as genuinely underpaid. The theorem's exact k-1 count
uses the declared nondegeneracy. The executable verifier may accept tied local inputs
and distinguishes nominated trimmed sources from those with positive deficits.

**Corollary 3 (derived residual wall).** At the selected global maximum, Y(w) is not
EFX, so at least one of these unpaid observers has a literal deleted-good violation.
If k=2, exactly one owner d is unpaid and every failure is her own EFX comparison.
Thus the one-underpaid support state is derived from physical O for every two-G
cycle, including mixed cycles; it is not assumed as an abstract role layout.

For the unique unpaid owner set

    theta_d=max({tail_d(Y_t):t differs from d} union {0}).

Then v_d(Y_d)<theta_d<=u_d(O), with deficit smaller than v_d(p). The offending target
may be the winning core, another trimmed core, a whole ordinary target, or an
unchanged external bundle. No root-facing target type is WLOG. A1's old P7 and its
specific A,H,W decomposition do not follow merely from this inequality.

For k=3 or 4 this construction leaves two or three potentially failing observers.
Reducing that number without introducing other observers' EFX failures remains a
separate theorem. This is not full branch closure.

## 3. A real large external observer obstruction

The archived nine-good example has unique canonical cycle 1->3->2->1, with
G sources {2,3}; the earliest cycle owner 1 has an E edge. Both winners are allowed:

| winner | Y_0 | Y_1 | Y_2 | Y_3 | charity | unique failing observer |
|---|---|---|---|---|---|---|
| 2 | {6,7} | {5} | {2,3,8} | {4} | {0,1} | 3 |
| 3 | {6,7} | {5} | {2,3} | {4,8} | {0,1} | 2 |

In both probes the only failing target is the unchanged external bundle O_0={6,7}.
At winner 2: owner 3's utility is 18448, versus the target deletion value 19520;
the violation 1072 is below her original deficit 2064 and p value 4352.
At winner 3: owner 2's utility is 26636, versus 29760; violation 3124 is below
her original deficit 4101 and p value 6400. Both probes improve owner 1, the first
changed owner, from 32782 to 34848, but neither is EFX.

Thus the unconditional assertion that these cycle probes can only be blocked inside
their cycle is false even at an exact global maximum. The large external observer
is a physical obstruction to that shortcut, not an EFX counterexample. This instance
has 103 complete EFX allocations. Its complete EFX allocation

    ({6,8}, {1,2,3,7}, {0,4}, {5})

lowers the highest-priority owner's utility from 10432 to 6464. It is a valid terminal
exit but not a partial-improvement argument. The intended global admission dichotomy
must preserve this complete-exit branch.

The original exhaustive global-selector audit supplies maximality and nondegeneracy;
the new probe verifier checks the constructions independently on the original goods.
It does not import or assert a no-complete-EFX premise.

## 4. Return the residuals: a complete all-paid probe, with a different wall

An ordinary run is a maximal nonempty consecutive string of E edges on the cycle.
There are zero, one, or two runs; two requires the alternating four-cycle GEGE.

**Theorem 4 (one-run residual-return probe).** If the cycle has one ordinary run,
let w be its terminal vertex (incoming E, outgoing G). If it has none, choose any
cycle vertex w. Start with the release allocation formula Y(w), whether or not this
w was priority-compatible for the release-only probe. Return every D_j to its
original owner j:

    Z_j = Y_j union D_j  for G targets j;    Z_i = Y_i otherwise.

Then Z is complete and physical, every cycle participant strictly improves, and
every outsider is fixed. Every EFX failure must have as target a **junction bundle**,
meaning the newly enlarged bundle of an incoming-G vertex. Such a failure is not
confined to outsiders: its observer may be another cycle participant. At global O,
at least one junction failure necessarily occurs.

**Proof.** The release allocation's charity is exactly the disjoint union of the
D_j, so returning each to j conserves all goods and leaves empty charity. An E source
already improves from the whole next bundle, and returning a residual only helps.
For a G source i that has incoming G, its returned D_i satisfies v_i(D_i)>=v_i(p),
so desire for R_sigma(i)+p gives v_i(R_sigma(i)+D_i)>u_i(O). Any additional p only
helps. The only G source without incoming G is the terminal vertex of an ordinary
run. With at most one such run, that vertex is w and receives its desired core.
Thus every participant strictly improves, regardless of the priority order.

Targets without an incoming G retain a bundle common-safe at O: an old whole bundle
or the winner's core. All observer utilities are now at least their O floors, so those
targets cannot cause EFX failure. The remaining targets are exactly the junctions.
If all those inequalities held too, Z would be an EFX Pareto improvement of the
global maximum, a contradiction. QED.

This is a probe, **not** a complete EFX theorem. Combining individually safe pieces
does not preserve common-safety. With two ordinary runs, there are two incoming-E /
outgoing-G vertices and only one p; the preceding all-paid proof does not apply.
Nor is EFX itself a necessary condition for a merely lex-improving probe: it is a
separate required condition for that probe to be a legal exit.

### Exact internal junction obstruction

The nine-good calibration's one-run probe chooses w=3 and gives

    Z=({6,7}, {1,5}, {0,2,3}, {4,8}),   charity empty.

Its utilities are (10432,38946,36877,22800): every cycle owner strictly improves.
There is exactly one failed physical EFX deletion comparison:

    v_1(Z_2 minus {3}) = 40965 > v_1(Z_1) = 38946.

The shortfall is 2019. The obstruction is inside the cycle, at a junction made
from owner 2's residual {0} and owner 1's retained part {2,3}. The release-only
probes were blocked by the external fixed bundle; residual return pays that
underpayment but creates this different observer failure. Neither failure can be
erased by relabeling it as a safe response.

Even the simpler transitive-graph shortcut fails. The graph has 1->3 (ordinary)
and 3->2 (G), but owner 1 values all of O_2+p at only 18705<32782; she cannot
champion any subset of it. Hence replacing that ordinary/G chain by 1->2 is invalid
at an exact global maximum. This is a counterexample to the graph contraction,
not to the desired complete-exit/admission dichotomy.

## 5. All-G cross-pools and genuinely forced observer/Hall data

If every edge is G, there is a selected split at every cycle owner. For i->j,
no self champion gives v_i(R_i+p)<=u_i(O)<v_i(R_j+p), hence v_i(R_j)>v_i(R_i).
Consequently the physical p-free pool P_i=D_i union R_j strictly exceeds u_i(O).
These cross-pools are disjoint. A globally minimal envied subset of P_i is
common-safe at O, but its champion need not be i. In particular the entire pool
is not certified common-safe merely because i wants it.

BCFF Lemmas 3.13-3.14 and Theorem 3.16 propagate these bottom-bundle demands for
good all-G cycles. For a GG two-cycle the archived PI exclusions leave external
bottom-edge sources, not predetermined sources or full owner matching. The import
keeps original O floors. [Primary source, pages 10-11](https://arxiv.org/pdf/2102.10654v2).

No analogous derivation follows just by contracting an ordinary-edge chain: the
released D at the start of that chain is valued by a different owner from the next
G source. Its original owner's payment inequality cannot be transferred between
observers. Such a contraction needs a new inequality, routing, or complete exit.

**Theorem 5 (two distinct foreign-observer-unsafe pools).** In an all-G cycle at O,
at least two distinct P_i have a foreign observer a, a differs from i, satisfying
tail_a(P_i)>u_a(O).

**Proof.** For each h, give h its desired core R_sigma(h)+p, every other cycle i its
P_i, and outsiders their old bundles. Leave D_h in charity. This is physical and
every participant strictly improves. Any EFX failure must target one of the P_i
with i differing from h, because all other targets are common-safe at O and every
observer is at least as well off. Such a failure is by an observer a differing
from i and has tail_a(P_i)>v_a(Z_a)>=u_a(O). If at most one P_i had a foreign
old-floor failure, choose it as h (or choose any h if none); all foreign comparisons
would hold, while self comparisons always hold. This would give an EFX Pareto
improvement, a contradiction. QED.

Do not include the intended recipient's old-floor inequality in this definition:
her new own value is v_i(P_i), and comparing tail_i(P_i) with her OLD value would
introduce a spurious safety requirement. The theorem concerns distinct pools,
not necessarily distinct observers.

**Theorem 6 (physical Hall witness, without an assumed rank).** For the all-G cycle
make four disjoint slots: one P_i per participant and one keeper O_b per outsider.
A pool slot is adjacent to agent a if some O-common-safe desired core Q contained
in that slot strictly exceeds u_a(O). A keeper is adjacent to a when its whole
bundle has value at least u_a(O). Retain ALL possible core recipients.

At global O there is no perfect matching. Consequently there is a nonempty
inclusion-minimal agent-side Hall witness S with

    |N(S)| = |S|-1,        |N_pool(S)| <= |S intersect I|-1.

In particular S meets the cycle. The statement does not assert matching rank three.

**Proof.** A perfect matching selects disjoint common-safe bundles, preserves every
owner's floor, and strictly improves recipients of the nonempty collection of pool
slots, contradicting global maximality. Hall's theorem supplies S. Every proper
subset of a minimal S satisfies Hall; deleting one element gives |N(S)|>=|S|-1,
and failure gives equality. Each outsider in S has a distinct own keeper neighbor,
so there are at least |S outside I| keeper neighbors. Subtract these from |N(S)|.
This also rules out S consisting solely of outsiders. QED.

Every desired core Q in P_i must intersect both D_i and R_sigma(i): each part alone
is a proper subset of an original bundle and is valued below or at every original
observer floor. In the GG case, neither cycle participant can champion such a core.
The source i could be paired with the other cycle owner's original p-core to give
a disjoint EFX Pareto improvement. The other participant j has
v_j(D_i)<v_j(p)<v_j(D_j), by Lemma 1, so does not even desire P_i=R_j+D_i.
Thus every bottom-core champion is external in this case, by a direct physical
argument with original floors.

For GG, both pools in Theorem 5 are foreign-observer-unsafe. Neither intended
recipient nor the other cycle owner can cause the actual failure of the paired
probe, so an external observer witnesses it. A minimal envied core Q is therefore
a proper crossing subset of its pool. This forces at least one omitted physical
good, but it does not specify which component loses it: D_i may be fully retained,
R_j may be fully retained, or both may be truncated. The distinction must not be
replaced by requiring every named remainder role to be nonempty.

These Hall/observer consequences are derived entry conditions, not a repair theorem
or a novel claim about Hall's theorem/BCFF. They show exactly which kind of witness
can be extracted without assigning it an unproved rank or support shape.

## 6. Live remaining gate

The next proof must either repair the actual unpaid-owner wall using the released
physical residuals without making another observer fail, or turn that wall into
the full declared fixed-U data with original floors. It must include the external
fixed-bundle wall above, not only the internal/root-facing wall. For k>=3 it must
also treat multiple unpaid observers, or prove a different admissible cycle exists.

The complementary residual-return construction shows why paying the deficit alone
is not the missing proof: it can create a new junction observer failure even when
the allocation is complete and every cycle owner improves. The general bridge must
repair both kinds of wall or permit a complete EFX exit that lowers some original
utilities. The exact calibration exhibits that latter possibility.

This checkpoint gives physical layouts and inequalities for a larger, honestly
derived support family. It does not justify importing existing twelve-role closure
results into that family. P5 budgets, special old-owner provenance, response
saturation, and global termination remain unproved where not separately sourced.

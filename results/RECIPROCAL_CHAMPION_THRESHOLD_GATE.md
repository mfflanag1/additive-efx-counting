# Reciprocal-champion threshold gate

## Extremum used by the revised route

Among EFX-with-one-charity states, first maximize the normalized owner
threshold potential

\[
\Theta(X)=\sum_i\frac{\tau_i(X_i)}{v_i(M)}.
\]

Among the \(\Theta\)-maximizers, maximize the owner-utility vector in any
fixed lexicographic agent order, and only then maximize the Hall signature.
Consequently, an EFX transition preserving one-good charity is impossible at
the selected state whenever it either strictly raises \(\Theta\), or preserves
\(\Theta\) and Pareto-improves owner utilities.

The utility tie-break is essential for using champion cycles. A
Pareto-improving champion cycle need not raise owner deletion thresholds.

## Full-witness external no-incoming-envy lemma

Let \((X,\{f\})\) be EFX with charity. Insert \(f\) into host \(h\), keep the
identity assignment, and suppose the only identity defect is agent \(b\).
If the resulting acceptance graph has the full Hall witness--no agent accepts
candidate bundle \(X_b\)--then

\[
v_i(X_i)>v_i(X_b)\qquad(i\notin\{b,h\}).
\]

In particular, neither external agent envies \(b\) in the original
four-agent allocation. No analogous conclusion is valid for host \(h\),
whose identity bundle after insertion is \(X_h+f\), not \(X_h\).

### Proof

Write \(C_h=X_h+f\) and \(C_j=X_j\) for \(j\ne h\). Fix
\(i\notin\{b,h\}\). Because the identity edge of agent \(i\) is valid,

\[
v_i(X_i)\ge \max_{j\ne i}\tau_i(C_j). \tag{1}
\]

When agent \(i\) is tentatively assigned candidate bundle \(X_b\), every
other candidate bundle is a comparison target. Its rejection of \(X_b\)
therefore says

\[
v_i(X_b)<\max_{j\ne b}\tau_i(C_j). \tag{2}
\]

Every term on the right of (2) is at most \(v_i(X_i)\): this is (1) when
\(j\ne i\), while \(\tau_i(X_i)<v_i(X_i)\) for the possible term \(j=i\)
because valuations are positive and \(X_i\ne\varnothing\). Combining (1) and
(2) proves the claim. For \(i=h\), identity acceptance controls
\(v_h(X_h+f)\), so this argument cannot compare \(v_h(X_h)\) with
\(v_h(X_b)\). \(\square\)

## Reciprocal singleton swap reduction

Suppose host \(h\) \(f\)-champions \(b\) with desired bundle

\[
T=X_b-g+f
\]

and singleton discard \(\{g\}\). If

\[
v_b(f)\ge v_b(g)
\quad\text{and}\quad
v_h(X_h)\ge v_h(g), \tag{3}
\]

then replacing \(X_b\) by \(T\) and charity \(f\) by charity \(g\), while
leaving every other owner bundle fixed, is EFX with charity.

Indeed, the champion property says no agent strongly envies \(T\). Agent
\(b\)'s own utility does not fall, so all of her old comparisons remain
valid, and she dominates the new charity good. Each external agent dominates
\(g\) because the external no-incoming-envy lemma gives
\(v_i(X_i)>v_i(X_b)\ge v_i(g)\). The second inequality in (3) supplies the
only missing charity comparison, that of host \(h\).

If \(g\) is a \(b\)-minimum and the first inequality in (3) is strict, this
eligible swap contradicts the revised \((\Theta,U)\) extremum by the
Pareto-sensitive owner-minimum swap corollary. Thus this entire reciprocal
subcase reduces to one possible wall:

\[
v_h(g)>v_h(X_h). \tag{4}
\]

When (4) holds, host \(h\) envies the bad bundle \(X_b\). If a bad-to-host
champion exists and discards \(f\), then \(b\) also envies \(h\), producing
an ordinary envy two-cycle. That cycle is EFX-preserving and Pareto-improving,
but its threshold change can be negative.

### Host-wall propagation lemma

Wall (4) forces a new owner-minimum swap candidate at the host. Let
\(x\in X_h\) minimize \(v_h(x)\). Then

\[
v_h(f)>v_h(x). \tag{5}
\]

To see this, (4) gives \(v_h(X_b)\ge v_h(g)>v_h(X_h)\). When host \(h\) is
tentatively assigned candidate bundle \(X_b\), every old nonhost threshold
is at most \(v_h(X_h)\) by EFX. Since the full witness says that \(h\) rejects
\(X_b\), the rejecting comparison must therefore be the augmented host bundle:

\[
v_h(X_h)<v_h(X_b)<\tau_h(X_h+f).
\]

But \(\tau_h(X_h+f)>v_h(X_h)\) holds exactly when \(f\) is worth more to
\(h\) than her old minimum \(x\), proving (5).

Consequently, swapping \(x\) with \(f\) would be threshold-nondecreasing and
strictly improve host utility. At the revised extremum this host swap must be
ineligible. Its failed EFX or charity inequality is the next named wall in
the dependency process. Thus the reciprocal singleton branch cannot stop at
(4): it either contradicts the extremum immediately or propagates to another
owner/component.

If \(X_h\) is nonsingleton, the Pareto-sensitive one-floater dependency
corollary makes this propagation exact: some other agent \(i\ne h\)
strongly envies \(X_h-x+f\), and necessarily
\(v_i(f)\) exceeds both \(v_i(x)\) and the least \(i\)-valued good in
\(X_h-x\). If \(X_h\) is a singleton, an external charity wall is the only
immediate wall type, but the singleton-chain elimination lemma propagates it
through distinct singleton owners until it reaches a positive incoming-target
wall. Thus both size branches produce a cap-free directed edge in the
remaining wall-dependency graph. By the incoming wall-to-champion corollary,
the nonsingleton endpoint also yields a generalized
\(\{f\}\mid\{x\}\)-champion into host bundle \(h\), releasing \(x\) and any
additional bottom discard (with the resource good and target renamed at the
end of a singleton chain).

## Two-source correction and exact reciprocal-cycle criterion

The corrected unique-defect bridge gives a most-envious source in
\(\{b,h\}\), not necessarily the edge
\(b\mathrel{\smash{\xrightarrow{f}}}h\). If the source is \(h\), then
\(v_h(f)>\min_{x\in X_h}v_h(x)\), which enters the host-minimum dependency
route above. The remainder of this section is conditional on the bad-source
branch. If its discard is \(\{f\}\), then
\(b\) ordinarily envies \(h\). Suppose also that \(h\) \(f\)-champions
\(b\) with desired bundle

\[
T=X_b-g+f
\]

and singleton discard \(\{g\}\). The envy/champion two-cycle produces an EFX
allocation with bundles

\[
Y_b=X_h,\qquad Y_h=T,\qquad Y_i=X_i\ (i\notin\{b,h\}),
\qquad P_Y=\{g\}.
\]

The old full witness makes the bad and external agents dominate \(g\), but
host dominance of the new charity is an additional condition. If
\(v_h(T)\ge v_h(g)\), then \(Y\) is EFX with charity and Pareto-improves the
owners on the cycle. Its exact threshold change is

\[
\Delta\Theta=
\frac{\tau_b(X_h)-\tau_b(X_b)}{v_b(M)}+
\frac{\tau_h(X_b-g+f)-\tau_h(X_h)}{v_h(M)}. \tag{6}
\]

Therefore (6) being nonnegative contradicts the revised
\((\Theta,\text{owner utility})\) extremum: a positive value contradicts
primary maximality and zero contradicts the Pareto-sensitive tie-break.

## Four reciprocal edge types

When the reciprocal edge exists, the owner graph has only four qualitative
types. For each direction, use an ordinary envy edge whenever the source
already envies the target; otherwise Observation 2.5 makes the champion edge
a genuine \(f\)-decomposition retaining \(f\).

1. Both directions are ordinary envy edges. Swapping the two bundles is an
   EFX-preserving Pareto improvement with the original charity good.
2. Only \(b\to h\) is envy. Combine it with the reciprocal
   \(f\)-champion edge; charity becomes that edge's discard set.
3. Only \(h\to b\) is envy. Combine it with the bad-source
   \(f\)-champion edge; charity becomes that edge's discard set.
4. Neither direction is envy. The two edges form a good \(f\)-cycle. The
   bottom-edge theorem supplies an internal good edge or an external bottom
   edge for each of its two released bottom bundles.

Cases 2 and 3 have a one-good charity set exactly when the used champion edge
has singleton discard; they additionally require dominance of that new
charity good. Case 4 is the only reciprocal type requiring the full
generalized-bottom-edge machinery. The unresolved conditions are therefore
charity control and threshold compatibility, not merely existence of a PI
cycle.

## Nonreciprocal routing lemma

If host \(h\) does not \(f\)-champion \(b\), Observation 2.4 still supplies
an incoming \(f\)-champion of \(b\). Its source is either \(b\) itself or one
of the two external agents. In the external case, the full-witness external
no-incoming-envy lemma says that the source does not envy \(X_b\); hence
Observation 2.5 makes the edge a genuine \(f\)-decomposition retaining
\(f\) and releasing a bottom subset of \(X_b\). Thus failure of reciprocity
does not terminate the champion construction: it redirects the released
bottom bundle through an external owner. The remaining issue is again
charity-cardinality and threshold compatibility.

## Exact corpus result

The full plateau corpus contains 4,320 distinct identity/unique-defect/full-
witness states. Exact enumeration gives, for every one of them:

1. the bad-to-host champion exists and discards the floater, so the bad agent
   envies the host;
2. the host reciprocally champions the bad bundle;
3. a reciprocal desired set has singleton discard, preserving one-good
   charity; and
4. the resulting two-cycle has \(\Delta\Theta=0\).

Thus all 4,320 states are excluded by the revised secondary utility tie-break.
This is an exact finite-corpus statement, not a universal theorem. The replay
is
[`unique_defect_champion_cycle_corpus_audit.json`](unique_defect_champion_cycle_corpus_audit.json).

The revised extremum itself has also been audited, rather than inferred from
those transitions. For the 46-profile hard plateau corpus and the separate
Chaudhury lex-potential counterexample, and for each of all 24 fixed agent
orders, exact enumeration first selects the global \(\Theta\)-plateau and then
the lexicographically maximum owner-utility vector. In all 1,128
profile/order cases, at least one utility-tied maximizer is Hall-absorbable.
Maximizing \(\Lambda\) within that final tie therefore selects an absorber in
every audited case. See
[`threshold_utility_tiebreak_corpus_audit.json`](threshold_utility_tiebreak_corpus_audit.json).
This is finite-corpus evidence for the revised selector, not a universal
proof.

## Why global maximality cannot be omitted

The local nonnegativity claim is false. The exact positive \(4\times6\)
profile

```text
 7 25  9 27 19 23
 4 28 18 14  3 11
 6  8 13  9 26 25
11 12  8 26  7 26
```

has the EFX-with-charity state

\[
(X_0,X_1,X_2,X_3;f)=(\{1\},\{0,2\},\{4\},\{3\};5).
\]

Inserting \(f\) into host 0 has unique bad agent 1 and the full Hall witness.
Agent 1 envies host 0, and host 0 has two reciprocal singleton-discard
champion choices. Both preserve one-good charity and both change \(\Theta\)
by

\[
-\frac{31}{1430}.
\]

This state is not globally maximal: its score is \(3/13\), while the global
maximum is \(14/39\); both global maximizers directly absorb. The frozen
record is
[`unique_defect_champion_threshold_local_counterexample.json`](unique_defect_champion_threshold_local_counterexample.json).

A second exact \(4\times6\) profile also blocks the combined local rule
"nonnegative reciprocal cycle or improving owner-minimum swap." Its host
envies the bad singleton bundle, so wall (4) holds; swapping the two envying
bundles preserves charity and Pareto-improves but lowers \(\Theta\) by
\(607/5561\). It too lies strictly below absorbing global maximizers. This
shows that even the one-wall reduction needs global maximality or a signed
component argument. The exact replay is
[`unique_defect_champion_combined_local_counterexample.json`](unique_defect_champion_combined_local_counterexample.json).

Reciprocity itself is also not a local consequence of the full Hall witness.
An exact positive \(4\times6\) state has an identity unique defect, the full
witness, and a bad-to-host champion, while the host is not a
champion of the bad bundle. Its score is \(30/91\), below the absorbing global
maximum \(29/84\). See
[`unique_defect_missing_reciprocal_local_counterexample.json`](unique_defect_missing_reciprocal_local_counterexample.json).

Exact enumeration of all eligible one-charity states in these three profiles
finds a shortest strict \((\Theta,U)\) escape in every case. The escapes have
label distances one, two, and two; each is one connected transfer component,
and every endpoint is directly Hall-absorbable. They respectively realize a
positive one-good owner transfer, a threshold-neutral host-minimum charity
swap with strict host utility gain, and a positive two-good/three-owner
transfer. See
[`unique_defect_champion_local_escape_audit.json`](unique_defect_champion_local_escape_audit.json).

Singleton bottom discard is not a universal fallback. An exact full-witness
\((4,8)\) state has a bad-to-host champion that retains the floater, does not
envy the old host, and has a unique desired bundle whose discard contains two
host goods. This state too lies below 24 absorbing global maxima. See
[`unique_defect_multi_bottom_local_counterexample.json`](unique_defect_multi_bottom_local_counterexample.json).
Nor can the multi-bottom branch always be repaired by a positive one-good
owner transfer or by redistributing only the host bundle before insertion.
Exact \((4,8)\) witnesses refute both local strengthenings. The first needs a
connected two-good/three-owner escape; the second cannot complete through the
original host after redistributing that host's bundle. Its nearest escape
moves one host good but absorbs the floater through a different host. See
[`unique_defect_multi_bottom_one_transfer_local_counterexample.json`](unique_defect_multi_bottom_one_transfer_local_counterexample.json)
and
[`unique_defect_multi_bottom_host_split_local_counterexample.json`](unique_defect_multi_bottom_host_split_local_counterexample.json).

Even allowing every insertion host and all 24 bundle matchings does not make
host-only redistribution universal. An exact QF_LRA search in the canonical
\(3+2+1+1\) bundle cell produced a positive-rational profile for which all
175 reachable host-redistribution partitions have deficient EFX matching
graphs after every insertion. Literal integer replay confirms the full
unique-defect multi-bottom hypotheses and zero completions. See
[`unique_defect_host_redistribution_lra_counterexample.json`](unique_defect_host_redistribution_lra_counterexample.json).

## Remaining theorem gate

Champion topology alone is insufficient. At a globally \(\Theta\)-maximal
full/unique-defect state, prove one of the following cap-free alternatives:

1. global maximality forces a usable reciprocal edge, and a reciprocal
   singleton-discard champion cycle has
   \(\Delta\Theta\ge0\);
2. a generalized champion edge set reallocates every released bottom bundle,
   preserves charity cardinality, and has nonnegative total threshold change;
   or
3. the signed transfer-component walls imply a different eligible state with
   larger \(\Theta\).

The first alternative exactly explains every known full-witness transition.
The local counterexample proves that global maximality or the wall alternative
must be used in its proof.

## Claim boundary

The external no-incoming-envy lemma, the singleton-swap and host-wall
propagation lemmas, the nonreciprocal routing lemma, criterion (6), the exact
audits, and the local counterexamples are verified. The
three-way extremal alternative is not yet
proved, so neither four-agent nor general additive EFX is resolved here.

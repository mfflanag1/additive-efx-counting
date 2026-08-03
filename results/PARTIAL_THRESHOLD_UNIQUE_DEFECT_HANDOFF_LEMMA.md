# Unique-defect handoff lemma

## Statement

Let \((X,\{f\})\) be a positive-additive EFX allocation with one charity
good. Choose distinct agents \(b\) and \(h\), and form the complete identity
candidate

\[
Y_h=X_h+f,\qquad Y_i=X_i\quad(i\ne h).
\]

Assume every identity acceptance edge is valid except agent \(b\)'s own edge.
Equivalently, after inserting \(f\) into host \(h\), the only remaining EFX
defect is agent \(b\)'s strong envy of the host bundle.

Choose \(g\in X_b\), exchange \(f\) and \(g\), and write

\[
X'_b=X_b-g+f,qquad P'=\{g\},qquad X'_i=X_i\ (i\ne b).
\]

Suppose:

1. \((X',P')\) is EFX with charity;
2. every external agent \(i\notin\{b,h\}\) satisfies
   \(v_i(g)\leq v_i(f)\); and
3. the bad agent clears the single handoff inequality

   \[
   v_b(X_b-g+f)\geq \tau_b(X_h+g). \tag{1}
   \]

Then the complete identity allocation

\[
Z_b=X_b-g+f,qquad Z_h=X_h+g,qquad
Z_i=X_i\quad(i\notin\{b,h\})
\]

is EFX.

## Proof

Start from the eligible swap state \((X',\{g\})\). Completing it changes
only host \(h\)'s bundle, from \(X_h\) to \(X_h+g\).

Agent \(h\)'s own bundle strictly improves, while every competing bundle is
unchanged, so all of her EFX inequalities remain valid. Agent \(b\)'s own
bundle and every nonhost competing bundle are unchanged from \(X'\); her only
new comparison is against \(X_h+g\), and (1) verifies it.

Fix an external agent \(i\notin\{b,h\}\). Her own bundle is unchanged. Her
comparison with the repaired bad bundle \(X_b-g+f\) is valid because it was
already present in the EFX state \(X'\). Comparisons with every bundle other
than \(h\) are likewise unchanged. For the host bundle, the original
one-defect hypothesis gives

\[
v_i(X_i)\geq\tau_i(X_h+f).
\]

Since \(v_i(g)\leq v_i(f)\), coordinate monotonicity of the owner-deletion
threshold gives

\[
\tau_i(X_h+g)\leq\tau_i(X_h+f).
\]

Thus the host comparison also remains valid. Every ordered EFX comparison in
\(Z\) is now covered. \(\square\)

## Exact scalar form of the remaining defect

Let \(m_b=\min_{x\in X_h}v_b(x)\). Relative to the failed candidate \(Y\),
the bad agent's host slack changes by exactly

\[
v_b(f)-v_b(g)
+\max\{0,v_b(f)-m_b\}
-\max\{0,v_b(g)-m_b\}. \tag{2}
\]

Hence, once the swap state and the external order conditions are certified,
the entire completion question is one scalar inequality: the gain in (2)
must cover the unique original negative slack.

## Lexicographic strengthening: closure is unnecessary

For the extremal proof, condition (1) can be dropped. Retain the one-defect
hypothesis and suppose only that:

1. the swap state \((X',\{g\})\) is EFX with charity;
2. every external \(i\notin\{b,h\}\) has \(v_i(g)\leq v_i(f)\); and
3. the bad agent has the strict order \(v_b(f)>v_b(g)\).

Insert \(g\) into the same host \(h\) and consider the identity matching. By
the proof above, the host and both external agents have nonnegative matched
slacks; condition (1) was used only for agent \(b\).

Let \(s_b<0\) be \(b\)'s unique old matched slack. Since the original partial
state was EFX and only host \(h\)'s bundle changed, the active failed
comparison in the old candidate is necessarily \(X_h+f\). In the new
candidate, either \(b\)'s slack is already nonnegative, or its active
comparison is \(X_h+g\). In the latter case its increase is exactly the
positive quantity in (2). Therefore its new slack is strictly greater than
\(s_b\) in both cases.

The old optimal signature had exactly one negative coordinate, namely
\(s_b\). The new identity candidate has every other coordinate nonnegative
and its only possibly negative coordinate is strictly larger than \(s_b\).
Its sorted signature therefore strictly lexicographically dominates the old
one, whether or not it is already a complete EFX matching.

Consequently, at a state selected lexicographically by
\((\Theta,\Lambda)\), a blocked identity/unique-defect candidate is impossible
as soon as some owner-minimum \(g\in X_b\) satisfies the eligible-swap and two
item-order conditions above. Owner-minimality plus swap eligibility preserves
\(\Theta\), while the handoff strictly improves \(\Lambda\).

## Alternating-cycle normal form

The unique-defect hypothesis also determines the completion graph. Index each
candidate bundle by its old owner and draw a directed arc \(i\to j\) when
agent \(i\) accepts bundle \(j\). Every diagonal arc except \(b\to b\) is
present.

Moreover, \(b\to h\) is present. Indeed, the negative self edge means

\[
v_b(X_b)<\tau_b(X_h+f).
\]

The old partial EFX inequalities give
\(v_b(X_b)\geq\tau_b(X_j)\) for every old competing bundle. Hence the total
value \(v_b(X_h+f)\), which strictly exceeds its threshold, is larger than
every competing threshold when bundle \(h\) is assigned to \(b\). Thus
\(b\) accepts \(h\).

In any directed graph containing every diagonal arc except \(b\to b\), the
associated bipartite graph has a perfect matching if and only if \(b\) lies on
a nontrivial directed cycle. One direction assigns bundles along that cycle
and uses every remaining diagonal edge. Conversely, in any perfect-matching
permutation, \(b\) cannot be a fixed point; the permutation cycle containing
\(b\) is a nontrivial directed acceptance cycle.

Therefore a blocked unique-defect candidate has no directed return path from
any accepted bundle of \(b\) back to \(b\); in particular, there is no path
from host \(h\) to \(b\). For four agents this reduces the matching
obstruction to a directed reachability set of size at most three. The
valuation proof can work on that reachability cut rather than an arbitrary
four-by-four Hall graph.

## Role in the four-agent gate

This lemma isolates the dominant exact-corpus mechanism. At a global
threshold maximum, choosing \(g\) as an owner minimum makes every eligible
\(f/g\) exchange plateau-neutral. The unresolved step is no longer a full
EFX verification, or even the bad-row closure inequality: it is to prove that
a unique-defect optimal insertion has some owner-minimum \(g\) for which the
exchange is eligible, the two external rows satisfy \(g\preceq f\), and the
bad row satisfies the strict order \(g\prec f\).
Failure in either external row creates the receiver-edge dependency from the
matched-slack exchange lemma.

The exact plateau audit reconstructs 4,847 selected blocked-to-completing
transitions. Of these, 4,323 start from an identity-matched optimal insertion
with exactly one negative matched slack and finish in one minimum-slot step.
Exactly 4,320 use the canonical pattern in this lemma: the charity good enters
the unique bad agent's bundle, its released good is inserted into the same
old host, the endpoint matching is identity, both external rows rank the
released good below the old charity good, and the bad row clears (1). All
4,320 replay exactly. Three corpus transitions use a different source and are
outside the lemma rather than counterexamples to it. See
`unique_defect_handoff_audit.json`.

The Hall trichotomy separates these counts perfectly: all 4,320 canonical
handoffs are full witnesses with zero acceptors for the bad bundle. The three
exceptions are exactly two copies of one bad--host pair profile and one
bad--host--external triple profile. Thus this handoff is empirically the
full-witness repair, while the proper-cut cases require different exchange or
rematching arguments.

## Claim boundary

The handoff lemma is cap-free and valid for arbitrary numbers of agents, with
one charity good and one unique identity defect. It is conditional on the
eligible swap, external order, and bad-row closure inequality. It does not by
itself prove that such a released good exists, and therefore does not resolve
four-agent or general EFX.

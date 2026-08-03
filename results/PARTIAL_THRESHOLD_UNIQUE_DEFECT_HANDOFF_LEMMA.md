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

## Role in the four-agent gate

This lemma isolates the dominant exact-corpus mechanism. At a global
threshold maximum, choosing \(g\) as an owner minimum makes every eligible
\(f/g\) exchange plateau-neutral. The unresolved step is no longer a full
EFX verification: it is to prove that a unique-defect optimal insertion has
some owner-minimum \(g\) for which the exchange is eligible, the two external
rows satisfy \(g\preceq f\), and the single bad-row inequality (1) holds.
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

## Claim boundary

The handoff lemma is cap-free and valid for arbitrary numbers of agents, with
one charity good and one unique identity defect. It is conditional on the
eligible swap, external order, and bad-row closure inequality. It does not by
itself prove that such a released good exists, and therefore does not resolve
four-agent or general EFX.

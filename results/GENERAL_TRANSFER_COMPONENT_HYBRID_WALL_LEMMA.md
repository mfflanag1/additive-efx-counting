# Transfer-component hybrid wall lemma

## Statement

Fix positive-additive valuations and a charity cardinality \(p\). Let
\((X,P)\) and \((Y,Q)\) be two EFX-with-charity states with
\(|P|=|Q|=p\), using the convention \(\tau_i(\varnothing)=0\). Introduce one
slot for every owner and one charity slot
\(c\). For every good whose slot differs between the two states, draw a
directed edge from its \(X\)-slot to its \(Y\)-slot, labeled by that good.
Let \(C_1,\ldots,C_r\) be the connected components of the underlying
undirected transfer multigraph.

For a set \(A\subseteq\{C_1,\ldots,C_r\}\), define the hybrid state
\(Z^A\) by applying exactly the item moves in the components in \(A\).
Then:

1. \(Z^A\) is a valid allocation/charity partition with charity cardinality
   \(p\).
2. Every owner bundle and the charity bundle in \(Z^A\) is exactly its bundle
   from either \(X\) or \(Y\). It is the \(Y\)-bundle precisely when its slot
   lies in a component of \(A\).
3. The normalized owner-threshold change is component-additive:

   \[
   \Theta(Z^A)-\Theta(X)
   =\sum_{C\in A}\Delta(C),
   \]

   where

   \[
   \Delta(C)=
   \sum_{i\in C\cap N}
   \frac{\tau_i(Y_i)-\tau_i(X_i)}{v_i(M)}.
   \]

4. If \(Z^A\) is not EFX with charity, every failed inequality crosses the
   selected-component cut. Concretely, either:

   - an owner \(i\) and a compared owner \(j\) lie on opposite sides and

     \[
     v_i(Z^A_i)<\tau_i(Z^A_j),
     \]

     or
   - owner \(i\) and the charity slot lie on opposite sides and

     \[
     v_i(Z^A_i)<v_i(Z^A_c).
     \]

No inequality whose two slots lie on the same side can fail.

## Proof

Every moved good is one edge and every edge belongs to exactly one transfer
component. Applying a set of components chooses, independently for each good,
either its \(X\)-slot or its \(Y\)-slot, so every good is assigned exactly
once.

All moved goods incident to a fixed slot belong to the same connected
component. Therefore applying that component changes every incident good at
once and turns the slot's bundle from its complete \(X\)-bundle into its
complete \(Y\)-bundle. Not applying it leaves the complete \(X\)-bundle.
There is at most one component incident to the charity slot. Because
\(|P|=|Q|\), applying that entire component preserves the charity
cardinality; components not incident to charity do not change it. This proves
items 1 and 2.

The potential \(\Theta\) is a sum of one term depending only on each owner's
own bundle. Each changed owner belongs to exactly one selected component, so
grouping its change by that component gives item 3 exactly. No linearity of
the threshold function inside a bundle is required.

For item 4, consider a pairwise EFX inequality between owner \(i\) and target
bundle \(j\). If both slots are outside \(A\), the two sides are exactly the
corresponding inequality in \(X\), which holds. If both are inside \(A\),
they are exactly the corresponding inequality in \(Y\), which also holds.
Thus failure requires the slots to lie on opposite sides. The identical
argument applies to owner-versus-charity dominance, using the charity slot in
place of \(j\). Moreover, the opposite slot cannot be isolated in the
transfer graph: an isolated slot has the same bundle in \(X\) and \(Y\), so
the mixed inequality would again be an inequality of \(Y\). Hence every wall
really names another transfer component. \(\square\)

## Positive-component corollary

If \(\Theta(Y)>\Theta(X)\), at least one transfer component \(C\) has
\(\Delta(C)>0\). Applying only \(C\) therefore gives one of two outcomes:

1. an eligible connected transfer with strictly larger \(\Theta\); or
2. a named EFX or charity wall crossing from \(C\) to another transfer
   component.

Starting from a positive component and repeatedly adjoining the component
named by a crossing wall yields the exact dependency-growth process needed by
the augmenting-component-cycle program. If it reaches an eligible union while
the accumulated component gain is positive, global \(\Theta\)-maximality is
contradicted. If it closes a dependency cycle first, the remaining proof task
is to show that the normalized wall inequalities cancel without exhausting
the positive gain.

## Why this is the correct replacement for bounded radius

The full/unique-defect radius-three counterexample has a first improving
endpoint whose transfer multigraph is one component spanning all four owner
vertices. Earlier fixed-core witnesses require as many as seven moved goods
but likewise have one transfer component. The number of moved goods is thus
not the invariant; connectedness in owner/charity slot space is.

The lemma is valid for arbitrary \(n\), arbitrary bundle sizes, and arbitrary
fixed charity cardinality. It therefore applies both to the four-agent
one-charity gate and to the general multi-good charity induction.

## Claim boundary

The hybrid decomposition and crossing-wall statement are proved. The lemma
does not prove that the dependency-growth process preserves positive
accumulated gain or terminates in an eligible union. That wall-cancellation
step remains the breakthrough gate, so neither four-agent nor general EFX is
claimed.

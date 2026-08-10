# Transfer-component hybrid wall lemma

## Statement

Fix positive-additive valuations. Let \((X,P)\) and \((Y,Q)\) be any two
EFX-with-charity states; the charity cardinalities may differ. Use the
convention \(\tau_i(\varnothing)=0\). Introduce one
slot for every owner and one charity slot
\(c\). For every good whose slot differs between the two states, draw a
directed edge from its \(X\)-slot to its \(Y\)-slot, labeled by that good.
Let \(C_1,\ldots,C_r\) be the connected components of the underlying
undirected transfer multigraph.

For a set \(A\subseteq\{C_1,\ldots,C_r\}\), define the hybrid state
\(Z^A\) by applying exactly the item moves in the components in \(A\).
Then:

1. \(Z^A\) is a valid allocation/charity partition. If the charity component
   is outside `A`, its charity bundle is `P`; if that component is inside
   `A`, its charity bundle is `Q`.
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

5. Every crossing wall has an exact strict polarity. Write

   \[
   d_i(j)=\tau_i(Y_j)-\tau_i(X_j)
   \]

   for an owner slot and

   \[
   d_i(c)=v_i(Q)-v_i(P)
   \]

   for the charity slot. Let \(a_s=1\) when slot \(s\) lies in a selected
   component and \(a_s=0\) otherwise. A failed owner--target or
   owner--charity inequality between slots \(i\) and \(s\) satisfies

   \[
   (a_s-a_i)d_i(s)>0. \tag{1}
   \]

   Thus an outside owner blocked by an inside target sees that target's
   threshold strictly increase, while an inside owner blocked by an outside
   target sees the outside target's threshold strictly decrease between
   \(X\) and \(Y\).

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
every good entering or leaving charity is incident to that slot, applying
the entire charity component changes the charity bundle exactly from `P` to
`Q`; components not incident to charity do not change it. No equality of
charity cardinalities is needed. This proves items 1 and 2.

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
really names another transfer component.

For item 5, suppose first that owner \(i\) is outside and target \(s\) is
inside. The failed hybrid inequality and feasibility of \(X\) give

\[
\tau_i(Y_s)>v_i(X_i)\geq\tau_i(X_s),
\]

with \(\tau_i\) replaced by charity value when \(s=c\). Hence \(d_i(s)>0\),
which is (1). If \(i\) is inside and \(s\) is outside, failure in the hybrid
and feasibility of \(Y\) give

\[
\tau_i(X_s)>v_i(Y_i)\geq\tau_i(Y_s),
\]

so \(d_i(s)<0\), again yielding (1). \(\square\)

## Positive-component corollary

If \(\Theta(Y)>\Theta(X)\), at least one transfer component \(C\) has
\(\Delta(C)>0\). Applying only \(C\) therefore gives one of two outcomes:

1. an eligible connected transfer with strictly larger \(\Theta\); or
2. a named EFX or charity wall crossing from \(C\) to another transfer
   component, carrying the strict polarity (1).

For an extremum taken at fixed charity cardinality, outcome 1 contradicts
maximality only when `C` avoids charity or `|P|=|Q|`. For an extremum over
all partial EFX-with-charity states, no such restriction is needed.

Starting from a positive component and repeatedly adjoining the component
named by a crossing wall yields the exact dependency-growth process needed by
the augmenting-component-cycle program. If it reaches an eligible union while
the accumulated component gain is positive and that union lies in the chosen
extremal domain, maximality is contradicted. If it closes a dependency cycle
first, the remaining proof task is to show that the normalized wall
inequalities cancel without exhausting the positive gain.

## Distinguished lex-component corollary

Fix an agent priority and suppose `Y` lexicographically dominates `X`. Let
`a` be the first owner in priority whose utility is strictly higher in `Y`,
and let `C*` be the transfer component containing slot `a`. Every hybrid
whose selected component set contains `C*` also lexicographically dominates
`X`: each owner before `a` receives either her `X`- or `Y`-bundle, which have
equal utility, while `a` receives her strictly better `Y`-bundle.

Consequently, start from `{C*}`. If the corresponding hybrid is EFX, it is
already a lexicographic improvement. Otherwise item 4 supplies a wall across
the selected cut and therefore names an unselected component. Add that
component and repeat. The process adds a new component at every failed step
and reaches `Y` after at most `r-1` additions. It remains valid when the
charity component changes the number of unallocated goods.

Accordingly, an EFX hybrid contradicts lexicographic maximality over all
partial EFX-with-charity states. If maximality was defined on a restricted
charity-cardinality slice, only hybrids in that slice are eligible
contradictions.

This corollary does not assume that every intermediate hybrid is EFX. It
states exactly what a failed intermediate contributes—a new component and a
strict wall polarity—while preserving the lexicographic sign of the whole
selected union.

## Why this is the correct replacement for bounded radius

The full/unique-defect radius-three counterexample has a first improving
endpoint whose transfer multigraph is one component spanning all four owner
vertices. Earlier fixed-core witnesses require as many as seven moved goods
but likewise have one transfer component. The number of moved goods is thus
not the invariant; connectedness in owner/charity slot space is.

The full-capture flower path gate gives both boundary types explicitly. Its
nearest partial endpoint increases charity cardinality and has one component
on `q,charity`; its nearest complete endpoint has one seven-edge component
spanning all four owners and charity. Both are covered by the statement
above without adding a balancing edge.

The lemma is valid for arbitrary \(n\), arbitrary bundle sizes, and arbitrary
charity bundles at both endpoints. It therefore applies both to the
four-agent one-charity gate and to components that temporarily increase,
decrease, or eliminate charity.

## Claim boundary

The hybrid decomposition, variable-charity extension, crossing-wall
statement, and distinguished lex-component corollary are proved. The lemma
does not construct a dominating endpoint `Y` from the flower's champion
data, nor does it prove that a locally generated dependency process agrees
with the components of one globally feasible endpoint. That endpoint-
construction step remains the breakthrough gate, so neither four-agent nor
general EFX is claimed.

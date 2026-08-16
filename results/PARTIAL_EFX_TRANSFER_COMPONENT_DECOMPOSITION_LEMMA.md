# Transfer-component decomposition lemma

## Lemma

Let $X$ and $Y$ be allocations of the same goods to $n$ labeled owners with
exactly one unallocated good in each allocation and no empty owner bundle.
Create a directed multigraph on vertices $\{1,\ldots,n,\bot\}$ by adding one
edge for every good whose owner changes from $X$ to $Y$; $\bot$ denotes the
unallocated position.

For every weak component $C$ of this transfer graph, define $Y^C$ by applying
to $X$ exactly the good transfers whose edge lies in $C$. Then:

1. $Y^C$ is a valid allocation with exactly one unallocated good and no empty
   owner bundle;
2. its nontrivial transfer graph is exactly $C$; and
3. for arbitrary real-valued functions $\phi_i$ on nonempty bundles,

\[
 \Phi(Z)=\sum_i \phi_i(Z_i)
 \quad\Longrightarrow\quad
 \Phi(Y)-\Phi(X)=\sum_C\bigl(\Phi(Y^C)-\Phi(X)\bigr).
\]

The statement therefore applies not only to normalized-utilitarian potential,
but also to the normalized owner-threshold potential

\[
\Theta(Z)=\sum_i
\frac{v_i(Z_i)-\min_{g\in Z_i}v_i(g)}{v_i(M)}.
\]

## Proof

Every changed-good edge incident to an owner vertex belongs to the same weak
component. Consequently, for a selected component $C$, an owner in $C$
receives all of its changes from $X$ to $Y$ and hence has bundle $Y_i$;
an owner outside $C$ receives none and retains $X_i$. Both are nonempty.

If $X$ and $Y$ have different floaters, the edge assigning the old floater
and the edge releasing the new floater are both incident to $\bot$, hence lie
in the same component. Applying that component changes the floater from the
old one to the new one; applying any other component leaves it unchanged. If
the floater is the same in $X$ and $Y$, no transfer edge touches $\bot$.
Thus every $Y^C$ has exactly one floater. The construction also makes its
changed-good graph exactly $C$.

Finally, the owner vertices occurring in distinct components are disjoint.
Every owner in a selected component receives its entire bundle from $Y$,
while every owner outside it retains its entire bundle from $X$.  Hence each
owner-level difference

\[
\phi_i(Y_i)-\phi_i(X_i)
\]

belongs to exactly one component, regardless of whether $\phi_i$ is linear.
Summing those differences proves the displayed identity.

## Consequence and exact limitation

If $Y$ improves any owner-separable $\Phi$, at least one component has
positive potential gain.
If its component allocation $Y^C$ is also eligible partial EFX, it is a
connected improving rival. Eligibility, however, is not componentwise.

The exhaustive seven-profile
[`partial_hall_augmenting_exchange_topology_audit.json`](partial_hall_augmenting_exchange_topology_audit.json)
checks the decomposition identity for every disconnected improving state.
Among 103 such states, 34 have no independently eligible positive component.
The first recorded example has two separately positive components, neither
of which is EFX, although their union is EFX. The resulting cross-component
walls are localized by the
[dependency-cycle lemma](PARTIAL_EFX_TRANSFER_COMPONENT_DEPENDENCY_LEMMA.md).
Thus decomposition isolates the remaining difficulty but does not prove the
connected-exchange target.

## Scope

The algebraic lemma is cap-free and valid for arbitrary numbers of agents and
goods. It makes no EFX-existence claim. The finite-profile failures are exact
refutations of the additional assertion that a positive component is
automatically eligible.  They were originally audited for normalized
utilitarian gain; the decomposition identity itself now also supplies the
global-restart interface needed by the threshold selector.

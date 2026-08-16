# Transfer-component dependency-cycle lemma

## Lemma

Let $X$ and $Y$ be partial EFX allocations of the same goods to the same
labeled agents, each with one unallocated good and no empty bundle. Let the
weak components of their changed-good transfer graph be defined as in the
[transfer-component decomposition lemma](PARTIAL_EFX_TRANSFER_COMPONENT_DECOMPOSITION_LEMMA.md),
and let $Y^C$ apply only component $C$ to $X$.

Every EFX violation in $Y^C$ crosses the boundary between $C$ and one other
nontrivial transfer component $D$. More precisely, if agent $i$ envies a
one-good residual of target bundle $j$ in $Y^C$, then $i$ and $j$ belong to
different transfer components and exactly one belongs to $C$.

Consequently, if no component allocation $Y^C$ is EFX, choose one violation
for each $C$ and draw a dependency edge from $C$ to the other component in
that violation. This finite directed graph has outdegree at least one at
every vertex and therefore contains a directed cycle.

The same conclusion holds for full one-floater **eligibility**, including the
requirement that every agent weakly dominate the floater. If the floater is
unchanged between $X$ and $Y$, every component state inherits floater-nonenvy
from the appropriate endpoint. If the floater changes, every new
floater-nonenvy violation crosses between the unique transfer component
containing $\bot$ and another nontrivial component. Thus, if no $Y^C$ is
eligible, selecting either an EFX violation or a floater-nonenvy violation for
each component again yields an outdegree-one dependency graph and hence a
directed cycle.

## Proof

In $Y^C$, every owner vertex in $C$ has its bundle from $Y$, while every
owner outside $C$ has its bundle from $X$.

If both the observing agent $i$ and target $j$ lie in $C$, their two bundles
are exactly those in $Y$, so the EFX inequality follows from EFX of $Y$. If
both lie outside $C$, their bundles are exactly those in $X$, so it follows
from EFX of $X$. Hence a violation must cross the boundary of $C$.

Suppose the endpoint outside $C$ does not occur in any transfer component.
Its bundle is then identical in $X$ and $Y$. If that endpoint is the target,
the allegedly violated comparison is already safe in $Y$; if it is the
observing agent, the comparison is already safe in $Y$ because its own
bundle is also unchanged. Both are contradictions. The outside endpoint
therefore lies in another nontrivial component $D$.

The dependency-cycle conclusion is the standard finite outdegree argument:
repeatedly follow an outgoing edge; some component must repeat.

For the floater condition, first suppose the same good is unallocated in
$X$ and $Y$. An owner in $C$ has its bundle from $Y$ and dominates that
common floater by eligibility of $Y$; an owner outside $C$ has its bundle from
$X$ and dominates it by eligibility of $X$.

Now suppose the floaters differ, and let $C_\bot$ be the transfer component
containing $\bot$. In $Y^{C_\bot}$ the floater is the one from $Y$ and every
owner inside $C_\bot$ has its bundle from $Y$, so only an owner in another
component can violate floater-nonenvy. This creates an edge from $C_\bot$ to
that component. For $C\ne C_\bot$, the component state retains the floater
from $X$, and every owner outside $C$ retains its $X$ bundle. Only an owner
inside $C$ can violate. The old floater is allocated in $Y$, so its ownership
change is incident to $\bot$ and its new owner belongs to $C_\bot$; the
violation therefore creates an edge from $C$ to $C_\bot$. This proves the
full-eligibility extension.

## Interpretation

This lemma identifies exactly why a positive transfer component may fail to
be an EFX allocation: it needs another component either to raise the
observing agent's bundle or to lower the offending target residual. If every
component fails, those needs form a directed cycle. That cycle is the natural
source of the weighted eligibility-wall contradiction required by the live
Hall conversion program.

The lemma does not itself prove that a component is improving, nor that the
dependency cycle has a favorable weighted potential sum. Combined with the
owner-separable strengthening of the decomposition lemma, it applies directly
to normalized owner-threshold gain and to full eligibility.

## Exact audit

[`partial_hall_augmenting_exchange_topology_audit.json`](partial_hall_augmenting_exchange_topology_audit.json)
replays the localization for every component of every disconnected improving
state in seven obstruction profiles. All 82 observed positive components that
are not independently eligible satisfy the floater-nonenvy condition and fail
only EFX. Twenty-two disconnected improving states have every component fail
EFX; every one has exactly two components and a mutual two-cycle dependency.
Twenty-one have positive potential gain in both components; one has one positive
and one negative component whose union is positive. The first displayed
example is a two-positive-component mutual dependency.

These counts are corpus facts. The localization and dependency-cycle
statements above are cap-free analytic results for arbitrary $n$ and $m$.

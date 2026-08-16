# Two-component reroute gate

## Falsified candidate

Fix the canonical partial allocation

\[
X=(\{6,7\},\{1,2,3\},\{0,4\},\{5\});f=8.
\]

Consider an eligible improving partial EFX allocation $Y$ at owner distance
at most five whose transfer graph has exactly two components. Suppose both
component allocations have positive normalized-utilitarian gain, satisfy
floater nonenvy, and fail only EFX. The candidate claimed that changing the
destination of one good in $Y$ always produces a connected eligible improving
allocation.

This candidate is false.

## Exact refutation

The positive-additive profile in
[`partial_hall_radius_one_2321_lra_compact.json`](partial_hall_radius_one_2321_lra_compact.json)
is independently certified as an eligible canonical radius-one Hall
obstruction. It contains four distinct distance-five improving allocations
with the stated two-positive mutual-dependency structure and no successful
one-good reroute.

The four rivals use floaters 2 or 3 and transfer-component good sets

\[
\{0,5,6\}\mid\{2,8\},\quad
\{4,5,6\}\mid\{2,8\},\quad
\{0,5,6\}\mid\{3,8\},\quad
\{4,5,6\}\mid\{3,8\}.
\]

Every component has strictly positive potential gain and satisfies floater
nonenvy, while both component allocations fail EFX. Exact enumeration of all
valid one-good destination changes finds no connected eligible improving
successor. The nearest connected improving allocation is two ownership
changes away in all four cases.

## Wider corpus search

[`partial_hall_two_positive_reroute_corpus_search.json`](partial_hall_two_positive_reroute_corpus_search.json)
row-normalizes stored profiles before deduplication and reports:

- 189 distinct positive $4\times9$ profiles;
- 21 eligible canonical radius-one Hall obstructions;
- 25 qualifying two-positive distance-five rivals;
- 21 with a successful one-good reroute; and
- four refutations, all in the single profile above.

All four refutations have a connected eligible improving state at reroute
distance two. Thus a two-good reroute remains corpus-supported, not proved.

## Strategic consequence

Connectedness is a proof aid, not part of the original improvement theorem.
Each refuting $Y$ is already an eligible improving allocation, so its
disconnected union is sufficient to contradict potential maximality. The
failed reroute shows that forcing every dependency cycle into one connected
exchange adds a genuinely false intermediate lemma.

The higher-value proof target is therefore a component-or-cycle conversion:
from the designated Hall trap, construct either an independently eligible
positive component or a collection of mutually dependent components whose
union is eligible and has positive total gain. A connected two-good splice is
a secondary option, not a required theorem.

## Claim boundary

This refutes only the one-good reroute conversion. It does not refute the
unrestricted radius-five improvement conjecture, the existence of a connected
radius-five improver, complete EFX, or additive EFX existence. Indeed, the
same profile has connected improving allocations, including one at owner
distance two from the base.

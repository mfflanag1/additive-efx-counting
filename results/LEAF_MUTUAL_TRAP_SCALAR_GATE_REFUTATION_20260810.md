# Leaf-mutual trap scalar gate refutation

**Date:** 2026-08-10

**Status:** exact additive refutation of local-inequality closure; flower
structure and alternate hubs remain live

## Refuted shortcut

The three-target Hall classification leaves one closed PI-free pattern:
leaves `r,s` block each other's augmented targets, both block the new hub
target, and hub `h` blocks neither leaf.  A tempting next step is to sum the
four strict wall inequalities with base EFX, charity dominance, and the hub
owner's improvement and derive a contradiction.

That implication is false even for positive integer additive valuations at
value cap six.

## Exact local model

Use base bundles

\[
X_h=\{hc_1,hc_2,a,b\},\quad X_r=\{r_1,r_2\},\quad
X_s=\{z\},\quad X_q=\{q_1,q_2\},
\]

with charity `{f}`.  The candidate split gives `h` the bundle
`{hc_1,hc_2,f}`, gives `a` to `r`, gives `b` to `s`, and fixes `q`.
The frozen model simultaneously satisfies:

1. positivity, base pairwise EFX, and base charity dominance for all four
   agents;
2. `v_h(f)>v_h(a)+v_h(b)`, so the hub owner strictly improves;
3. the four strict walls `r -> s`, `s -> r`, `r -> h`, and `s -> h`; and
4. absence of hub walls into either leaf target.

Every strict wall has integer margin one.  The hub owner gains one, and her
safety slacks against the two leaf targets are six and seven.  The exact
profile and diagnostics are frozen in
[`three_target_leaf_mutual_trap_cap6.json`](three_target_leaf_mutual_trap_cap6.json).
Both Z3 5.0.0 and 4.15.3 return SAT.

The residual hub must contain at least two goods in this witness.  With a
singleton residual, its new target is a two-good bundle, and base charity
dominance plus base EFX can make the corresponding hub walls artificially
impossible.  The two-good residual prevents that bounded degeneracy.

## Corrected target

The leaf-mutual trap cannot be eliminated from the four local wall signs
alone.  The next proof must use information omitted by this model:

- the three genuine flower champion arms and their released bottoms;
- the full-capture/crossing identities tying the hub packet to the mutual
  cycle; or
- a comparison with a different hub or a different partition of the same
  packet.

The most economical next selector is therefore an **alternate-hub
dichotomy**: show that whenever one eligible two-leaf split realizes the
leaf-mutual trap, a flower-induced alternate split is EFX, closes a PI
cycle, or has a Hall witness of size at most two and hence a forced open
growth direction.

## Claim boundary

The frozen allocation is not required to realize the flower's champion
edges or be globally lexicographically maximal.  It refutes only a proof
from local star inequalities.  It is not a counterexample to the hub
selector, the three-nonsingleton contraction, or EFX existence.

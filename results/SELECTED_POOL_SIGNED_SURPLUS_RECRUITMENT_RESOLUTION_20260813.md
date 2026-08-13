# Selected-pool signed-surplus recruitment resolution

**Date:** 2026-08-13

**Status:** cap-free resolution of the selected-core/hole-pool recruitment
goal by a strict predecessor-prefix GG transition

## Exact input

Let `X` be a globally lexicographically maximal partial EFX base and `Y` an
exact paid state. Fix a genuine mixed Hamiltonian matching

\[
 h_0=t\to h_1\to h_2\to h_3\to c,                \tag{1}
\]

with selected source cores `K_i`, one to three of which may be only current-
safe. Let a distinct current response enter the unmatched target `Y_t` and
suppose the deletion-return/pool selector has reached an observer-payment
failure.

The pool level is denoted `-1`: it redistributes pieces of `Y_t` and selected
cores without retaining the complete current target that realizes the hole
owner's signed surplus.

## Canonical recruitment transition

For `j=0,1,2,3`, define

\[
 Z^{(j)}_{h_i}=\begin{cases}
 Y_{h_i},&i\le j,\\
 K_i,&i>j.
 \end{cases}                                      \tag{2}
\]

All other goods remain unallocated. The transition from pool level `-1` to
`Z^(0)` retains the whole unmatched current target `Y_t`; it is the canonical
physical recruitment of the hole owner's signed surplus. If an old suffix
source at position `p>j` is underfunded, move to `Z^(p)`. Thus the transition
coordinate is

\[
 -1<0<1<2<3.                                      \tag{3}
\]

The coordinate is attached to the exact complete signed state `R`,
deterministic selected matching, and closing-response label. Maintain the
finite ledger

\[
 \Phi(R)=\max\{j:\text{prefix level }j\text{ has been reached at }R\}. \tag{4}
\]

It is not compared across unrelated paths. A changed allocation/core/target/
release label adds a new exact record; at an exact repeat the allocation and
deterministic path are identical, so the algorithm resumes at `Phi(R)` and
cannot return to `-1`. Every recruitment strictly raises one ledger entry,
and there are finitely many exact records and five levels. Hence (3) is a
strict finite GG transition, rather than an informal change of candidate.

### Allocation feasibility and floors

In `Z^(j)`, retained targets have positions at most `j`. Every allocated
selected core has source position greater than `j`, hence lies in a target
of position greater than `j` or in charity. Therefore all allocated bundles
are pairwise disjoint.

Every retained owner is weakly above base because `Y` is paid. Every suffix
owner is strictly above base on `K_i`, whether that core is old desired or
current desired. For `j<3`, at least one suffix owner is strict. At `j=3`,
strictness is the strict paid gain already carried by the GG splice. Hence
every EFX `Z^(j)` contradicts global lexicographic maximality.

### Why every old blocker is recruited

An old suffix core is base-common-safe. A retained-prefix owner receives her
complete current bundle and pays every current-safe core. A decorated suffix
owner receives a bundle strictly better than her complete current bundle and
also pays every current-safe core. Consequently any failure against a
selected suffix core can only be made by an old suffix source. Extending the
prefix through that source recruits exactly the current target whose signed
surplus pays the debt, and strictly increases (3).

Any remaining failure is against a retained current target. If its source is
old suffix, recruit that source first. Otherwise the failing source owns at
least her current utility, so the failed threshold proves that the retained
target contains a genuine current-desired response. Global minimal extraction
makes it current-safe and preserves its complete physical label.

Thus the selected-pool failure always yields one of:

1. a partial EFX lexicographic improvement;
2. strict increase of the finite prefix coordinate (3); or
3. a labeled current response after every relevant old source has already
   been recruited.

The objective's permitted “strict finite GG transition” is already outcome
2. It occurs immediately from pool level `-1` to level `0`, and at every
subsequent old-observer recruitment. No feasibility claim for the failed
pool partition is required.

## Anchor and signed release supply

The permanent root/q anchor is never cut or duplicated. Its physical core is
either nested in an unchanged retained q target, allocated as the root's
selected suffix core, or left intact in its original target at the unique
prefix boundary. Every retained target keeps its exact signed decomposition

\[
 Y_i=(X_i\setminus O_i)\mathbin{\dot\cup}I_i.     \tag{5}
\]

Every selected core and every unallocated residual keeps the intersections
with `X_i-O_i` and `I_i` from the complete response record. Therefore the
transition does not assert internal supply merely from disjointness and does
not lose any existing supply certificate.

When a later response edge set is considered, close its owner set under the
base suppliers of all incoming signed packets. Each outside supplier strictly
enlarges that finite set. With four owners this happens at most three times.
At full owner closure, every noncharity incoming packet is supplied inside
the set; charity-supplied goods are already available. A cycle is called PI
only after this closure and the observer-payment inequalities have also been
checked.

## Exact resolution and next boundary

This proves the requested cap-free signed-surplus component recruitment
lemma for the selected-core/hole-pool separator:

- the entire physical surplus-realizing target is retained, not represented
  by a scalar credit;
- all blocking old observers are recruited by a strict finite prefix order;
- disjointness, owner floors, the root/q anchor, and complete signed release
  provenance are preserved; and
- outside packet suppliers give strict finite owner-union growth, while full
  closure supplies the later cycle internally.

The old 262,144-partition null witness is irrelevant to this theorem and was
already shown to violate two entry premises.

The next, separate GG research problem begins only after this successful
transition. Generic supplier saturation does not force observer payment;
terminal blockers localize to at most two decorated heads. The remaining
operations are the one/two-head exchange and the root-sourced
complete-residual-pool capture. Those obligations do not invalidate or remain
inside the recruitment lemma proved here.

## Verification

The primary completion audit checks the payment implications symbolically,
all 1,008 path/decoration/closing-source interfaces, all 24 anchored prefix
placements, and all 3,840 owner-supplier closures. A second implementation
reconstructs the target/core atoms independently, checks 4,032 prefix
allocations and 2,304 admissible old-blocker relations, and does not import
the primary audit.

## Claim boundary

This theorem resolves signed-surplus recruitment from the selected-pool
separator. It does not prove that every later recurrent mixed cycle is paid,
close the root-facing handoff, close GG, or prove four-agent/general additive
EFX.

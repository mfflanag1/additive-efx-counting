# Four-placement singleton response-transport lemma

**Date:** 2026-08-14

**Status:** cap-free elimination of the relay's cross-state safety bands;
source parking and response-rank compression remain

## Complete four-probe family

Let `B=(B_i)_{i in N}` allocate every good except a positive singleton `p`
among four owners.  For each owner `a`, let `Z^a` be the complete allocation
obtained by giving `p` to `a` and changing nothing else:

\[
 Z^a_a=B_a+p,
 \qquad Z^a_i=B_i\quad(i\ne a).                  \tag{1}
\]

In the rank-three matching relay, `B` is the allocation obtained by reversing
the three selected response cores.  Therefore every `Z^a` uses the same at
most three owner-transfer pairs plus the single pair `charity->a`; all four
probes satisfy the required four-edge bound.

Assume every `Z^a` is non-EFX.  At each state, a **response** is a nonempty
packet `E` contained in one owner target such that, for its source `i`,

\[
 v_i(E)>v_i(Z^a_i),
 \qquad
 \tau_h(E)\le v_h(Z^a_h)quad(h\in N).           \tag{2}
\]

Choose, over the responses at all four states, a response `E` of globally
minimum cardinality `k`.  Let `i` be its source and let `a` be a state where
it is selected.  Suppose first that `p notin E`.

## Universal safety

For every owner `b`, the same physical packet `E` is safe at `Z^b`.

Only one floor decreases when moving from `Z^a` to `Z^b`: the floor of `a`
drops from `v_a(B_a+p)` to `v_a(B_a)`.  If `E` were unsafe at `Z^b`, then

\[
 \tau_a(E)>v_a(B_a).                              \tag{3}
\]

Consequently some one-good deletion `E-g` is desired by `a` at `Z^b`.
Global minimum desired-subset extraction inside that failed wall produces a
safe desired response of cardinality at most `k-1`, contradicting the choice
of `E`.  The argument is unchanged when `a=b`; then there is no decreased
floor.  Hence

\[
 \tau_h(E)\le v_h(Z^b_h)quad(h,b\in N).          \tag{4}
\]

## Desire transport and the unique parking exception

When `b != i`, the source `i` does not gain `p` relative to `Z^a`: its bundle
is unchanged, or it loses `p` when `a=i`.  Therefore `E` remains desired at
every `Z^b` with `b != i`.

At the single placement `Z^i`, the source gains `p`.  Either `E` remains
desired there and is a response at all four probes, or

\[
 v_i(B_i)<v_i(E)\le v_i(B_i)+v_i(p).             \tag{5}

Thus a globally smallest disjoint response has no observer-safety exception
and at most one desire exception: parking the singleton at its own source.

## Packet-hitting branch

If the globally smallest response contains `p`, its target is the current
singleton holder's bundle.  This is the declared whole-hit branch of the
retired-packet interface.  The theorem does not remove that branch; it shows
that every response outside it admits the universal transport (4)--(5).

## Rank-three relay consequence

Test all four complete allocations obtained from the reversed rank-three
matching.  If none is EFX, then exactly one of the following holds:

1. a globally smallest response hits `p`;
2. one fixed physical response core is safe at every probe and desired at
   every probe except possibly the placement at its own source; or
3. that core is desired even at its own-source placement and is a response
   at all four probes.

The previous pairwise root/unmatched-owner critical safety intervals vanish:
any such unsafe crossing would manufacture a smaller response in another
probe.  The live cap-free obstruction is now purely combinatorial.  Repeatedly
park `p` at the source of a neutralized minimum core; either minimum response
cardinality rises, another source supplies a same-cardinality universally
safe core, or a packet-hitting response appears.  Completing this source
parking process requires a matching/Hall argument for the accumulated cores.

## Claim boundary

This lemma proves universal safety and all-but-one-placement desire transport
for a globally smallest response across the four complete singleton probes.
It does not prove that accumulated cores have distinct targets, close their
Hall defect, eliminate the whole-hit branch, prove the fixed-`U` four-edge
theorem, or prove four-agent/general additive EFX.

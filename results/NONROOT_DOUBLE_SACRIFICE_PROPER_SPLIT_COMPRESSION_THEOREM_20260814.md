# Nonroot double-sacrifice proper-split compression theorem

**Date:** 2026-08-14

**Status:** cap-free elimination of every multi-good nonroot whole-packet
recurrence; the nonroot survivor is a singleton retired packet

## Protected split input

Let `r` be the unchanged first-priority root, strictly above the globally
maximal base. Let distinct later owners `s,h` be the colliding recipient and
current packet holder. Write

\[
Y_h=H\mathbin{\dot\cup}K,
\qquad
A=B\mathbin{\dot\cup}K.                         \tag{1}
\]

Use the exact priority-sacrifice candidate in which:

1. the root and the fourth owner's retained protected targets are unchanged;
2. `A` is a safe candidate target;
3. `Y_h` is the exact current holder target, with every pre-existing wall
   already present in the response record; and
4. every other non-`K` transfer and supplier label is fixed.

Unlike the one-floor split theorem, this theorem permits both later owners
`s,h` to fall below their auxiliary protected floors. Their failures become
decorated heads; the root floor is never waived.

## Proper split

Suppose `|K|>=2`. Choose any physical nontrivial partition

\[
K=T\mathbin{\dot\cup}U,
\qquad
T,U\ne\varnothing.                               \tag{2}
\]

Give `B+T` to `s` and `H+U` to `h`, preserving the root, the fourth protected
target, and all fixed non-`K` assignments. Feasibility is immediate. The
direct packet edge is supplied by `h`, and no compensation packet is used.

The recipient target is safe by deletion:

\[
B+T\subseteq A,
\qquad
H+U\subseteq Y_h.                                \tag{3}
\]

If `H+U` is unsafe, extract a globally minimum response inside it before
forming the protected graph. A response meeting `U` has proper retired
support; a response avoiding `U` is a genuine ledger-free current response
and enters the existing rank/normalization routing. At an exact repeat after
those branches are exhausted, `H+U` may therefore be treated as safe. Thus
no unchanged observer has an unprocessed wall against either split target.
Only `s` or `h` can remain underfunded by the split; they are the complete
decorated-head set, of size at most two.

## EFX or protected compression

If the tested allocation is EFX, the unchanged strict root makes it a
lexicographic contradiction. Otherwise form the protected whole-bundle
acceptance graph at the actual allocation.

The two nonheads `r` and the fourth owner have their distinct identity
edges. Every nonempty head row is processed by globally minimum safe response
extraction. Therefore:

- a perfect protected matching gives an EFX lexicographic improvement;
- a maximum matching of rank three can be chosen to cover the root and gives
  the protected three-core/one-residual compression star; and
- rank two retains the root identity core and the other nonhead core, then
  enters the two-core/two-hole cut-and-choose response-Hall boundary.

A maximum matching covers the root because its identity edge uses a target
not required by the other nonhead identity edge; if necessary replace the
edge occupying the root target by `r -> r` without lowering rank, or choose
the maximum matching containing both forced nonhead identities before
augmenting with head edges.

## Retired-support progress

At the split allocation,

\[
K\cap(B+T)=T,
\qquad
K\cap(H+U)=U,                                    \tag{4}
\]

and every other target is disjoint from `K`. Hence every globally minimum
single-target response that meets retired support meets a proper subset of
`K`. A ledger-free response enters the rank-two/rank-three compression just
described; a supplied cycle is PI; an outside supplier or new response edge
is strict component/rank progress. The existing two-hole and external-star
routing returns only to proper retired collision, PI/rank progress, or the
already isolated protected-root price/anchor gate.

Consequently no exact nonroot whole-packet recurrence with `|K|>=2` survives.

## Typed consequences

- **Strict capture:** no recipient-floor assumption is needed; any loss of
  the captured margin is represented by head `s` inside the protected graph.
- **Equality capture:** equality likewise creates a decorated head rather
  than a false strict response. Multi-good equality packets split.
- **Base-floor debt:** the only waived auxiliary floors are those of the two
  explicitly named later heads. Root and fourth-owner floors remain
  protected in the matching.
- **Release:** the split uses only the direct holder-supplied edge. Every
  later PI edge is checked with its signed suppliers.

## Exact survivor

The sacrifice-eligible nonroot terminal is therefore

\[
|K|=1.                                           \tag{5}
\]

For a singleton, no proper split exists. Whole-packet recipient replacement,
normalization bypass, or a root/anchor operation remains necessary.

## Claim boundary

This theorem proves the arbitrary proper split, two-head localization,
root-covered rank-2/3 compression, and singleton nonroot terminal under the
stated protected candidate premises. It does not split a singleton, prove
that every downstream root-price return closes, eliminate the protected-root
base-crossing Hall cut, close `T_{L,times}^*`, or prove four-agent/general
EFX.

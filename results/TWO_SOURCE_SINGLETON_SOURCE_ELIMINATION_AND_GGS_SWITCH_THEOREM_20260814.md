# Two-source singleton-source elimination and forced `GGS` switch theorem

**Date:** 2026-08-14

**Supersession (2026-08-14):** this is a conditional diagnostic. The full
anchored `GG` collision is already contradicted before the forced-`GGS`
stage.

**Status:** cap-free elimination of source pair `{c,s}` and reduction of the
sole remaining two-source hard topology to an exact nonroot `GGS` cycle;
ledger-preserving cycle-class conversion remains open

## Input

Use the single-edge two-source hard topology from the root-threshold debt
derangement theorem. The frozen length-two flower has nonroot owners `c,q,s`,
where `s` owns the base singleton. The source pair is `{c,q}` or `{c,s}`;
write `a` for the source with the unique ordinary edge to the non-source `t`,
and `b` for the other source:

\[
 a\longrightarrow t,
 \qquad b\not\longrightarrow t.                \tag{1}
\]

The hard CGM pattern forces

\[
 b\xrightarrow{f}a,
 \qquad t\xrightarrow{f}b,
 \qquad a\text{ or }b\xrightarrow{f}t.         \tag{2}
\]

Recall the frozen singleton rule: a selected champion edge into `s` cannot be
genuine. Its desired set discards `f`, so its source ordinarily envies `s`.

## The singleton cannot be a source

Suppose the source pair is `{c,s}` and the non-source is `q`.

- If `a=c` and `b=s`, the forced edge `t ->^f b` in (2) is an incoming
  champion `q ->^f s`. The singleton rule makes `q -> s` an ordinary envy
  edge, contradicting that `s` is a source.
- If `a=s` and `b=c`, the forced edge `b ->^f a` is `c ->^f s`. Again the
  singleton rule gives an ordinary incoming edge into `s`, a contradiction.

Therefore

\[
 \{c,s\}\text{ is impossible}.                 \tag{3}
\]

## The remaining source pair forces `GGS`

The only source pair is `{c,q}`, and `t=s`. The unique edge (1) is either
`c -> s` or `q -> s`. Let `a` be its source and `b` the other member of
`{c,q}`.

Because `a` and `b` are both sources, `b` does not ordinarily envy `a`.
Hence the forced champion `b ->^f a` is genuine. The singleton `s` has no
ordinary outgoing edge in the single-edge envy graph, so the forced champion
`s ->^f b` is also genuine. Finally a champion of the singleton `s` must be
nongenuine and hence an ordinary envier. The unique such source is `a`, so
the third edge in (2) is exactly the ordinary edge `a -> s`.

Thus the three nonroot owners contain the directed selected cycle

\[
 b\xrightarrow{G}a\xrightarrow{S}s\xrightarrow{G}b, \tag{4}
\]

whose cyclic word is `GGS`.

## Exact interpretation

Equation (4) does not by itself close the retired-packet recurrence. Its two
genuine edges both use the same charity good, so it is not automatically a
release-compatible PI cycle. Moreover, the existing three-nonsingleton census
lists `GGS` as a distinct unresolved cycle class.

The remaining operation is now exact: convert the root-held `GG`
retired-packet state to the forced nonroot `GGS` selector while preserving the
retired ledger, root/anchor floor, response source, and supplier releases; or
use the combined `GG` and `GGS` edges directly to obtain PI, anchor exchange,
packet/rank reduction, or a floor contradiction. Merely changing the selected
cycle label is not finite progress.

## Claim boundary

This theorem eliminates source pair `{c,s}` and forces (4) in the sole
surviving source topology. It does not prove a well-founded cycle-class order,
make two `f`-edges supplier-disjoint, close the `GGS` class, execute the
ledger-preserving switch, close `T_{L,times}^*`, GG, four-agent EFX, or general
additive EFX.

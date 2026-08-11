# Minimal-Hall owner-union compression lemma

**Date:** 2026-08-11

**Status:** cap-free analytic component reduction; residual-pool partition
selection remains open

## Arbitrary minimal defect

Let `Y` be a complete proposed allocation and let `C_j` be the nonempty set
of response sources for each represented target `Y_j`. Let `U` be any
inclusion-minimal Hall-deficient target set, and put

\[
S=\bigcup_{j\in U}C_j. \tag{1}
\]

For every `j in U`, minimality gives Hall's condition on `U\setminus{j}`.
Since its neighborhood is contained in `S`,

\[
|U|-1\le |S|<|U|,
\]

and therefore

\[
|S|=|U|-1. \tag{2}
\]

Every minimal defect has deficiency exactly one, regardless of whether it
contains two, three, or four targets.

Hall's theorem matches `S` to every target deletion `U\setminus{j}`. As in
the all-owner case, every prescribed response edge `i -> j` extends to a
near-perfect matching: match `U\setminus{j}` to `S`, delete the edge using
source `i`, and insert `i -> j`.

## Owner-union compression

Choose a near-perfect matching `mu:S -> U\setminus{j_0}` and one
common-safe desired core

\[
A_i\subseteq Y_{\mu(i)}
\qquad(i\in S). \tag{3}
\]

The cores are pairwise disjoint. Define the affected owner union and its
unmatched owners by

\[
V=U\cup S,
\qquad M=V\setminus S. \tag{4}
\]

Collect every unselected good currently held by an owner in `V` into

\[
P=\left(\mathop{\dot\bigcup}_{v\in V}Y_v\right)
\setminus\left(\mathop{\dot\bigcup}_{i\in S}A_i\right). \tag{5}
\]

For any disjoint partition

\[
P=\mathop{\dot\bigcup}_{m\in M}P_m, \tag{6}
\]

form

\[
Z_i=A_i\quad(i\in S),
\qquad Z_m=P_m\quad(m\in M), \tag{7}
\]

and fix every owner outside `V`. This is a complete allocation. Every source
in `S` strictly improves, every selected core is common-safe, and all goods
removed from source owners are retained in the residual pool. Thus (7) is a
release-compatible owner component for every packet cardinality.

If every unmatched owner is weakly nonworse, no observer can newly fail EFX
against a selected core.  Among targets changed by this compression, only
the residual-pool targets `P_m` can be new walls.  A wall already present
against a target fixed outside `V` remains present; eliminating those
inherited walls requires compressing a maximum matching of the entire active
target relation. If some unmatched owner is sacrificed, the priority check
and loss-band localization must be applied separately to every losing
owner; the single-residual sacrifice lemma is only the `|M|=1` special case.

## Four-agent specialization

For a two-target/one-source defect there are only two forms.

1. If the source owner lies in `U`, then `|V|=2` and `M` is a singleton;
   all leftovers go to one residual owner.
2. If the source owner lies outside `U`, then `|V|=3` and `M` has two owners;
   the compression itself reduces to a two-way partition of `P`, together
   with any inherited walls against active targets outside `V`.

This second form is exactly the terminal witness missed by all-owner
compression in the bounded weighted-Hall adversary: the three signatures are

\[
\{q,s\}\to\{c\},
\qquad \{q,c\}\to\{c\},
\qquad \{c,s\}\to\{c\}. \tag{8}
\]

In the hardened bounded adversary, compressing the first signature with edge
`c -> s`, core `{z}`, and a two-way partition of the combined `q,s,c` pool
produces a complete EFX lex improvement. The profile is positive and
subset-sum-injective, and the premises, response relation, and endpoint
replay solver-independently in
[`owner_union_compression_hardened_profile_audit.json`](owner_union_compression_hardened_profile_audit.json).
This is not used in the analytic proof and is not a universal
residual-partition theorem.

The deficiency-one, matching-extension, and packet-support statements
replay in
[`minimal_hall_owner_union_compression_audit.json`](minimal_hall_owner_union_compression_audit.json).

## Claim boundary

This lemma generalizes response compression to every minimal Hall defect and
identifies its owner-union residual partition.  It does not eliminate walls
against fixed active targets outside that union.  The maximum-matching
owner-union compression lemma is the correct global composition.  Neither
lemma proves that every residual partition meets all utility and EFX
thresholds, eliminates the cross-star in every flower, closes the `GG`
class, or proves four-agent additive EFX.

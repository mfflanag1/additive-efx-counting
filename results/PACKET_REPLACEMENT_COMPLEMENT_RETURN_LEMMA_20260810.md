# Packet-replacement complement-return lemma

**Date:** 2026-08-10

**Status:** cap-free analytic response reduction; the strict core-capture and
closed Hall-defect branches remain open


*Convention note 2026-08-16 (`tau`).* This file uses `tau` **without defining it** (inherited), once, in the
convention-agnostic form "every one-good deletion of `X_q` has value at most
`tau_i(X_q)`" — true under either reading.

The two forms coincide **only under additivity**: for additive `v`,
`max_{g in Z} v(Z\{g}) = v(Z) - min_{g in Z} v(g)`, but for a merely monotone
cancelable `v` they are different functionals. Composing this file with one that
uses the other form is therefore sound only inside the additive class, where this
rung currently sits. The rung's live conflict —
`FLOWER_MINIMAL_PAYMENT_RESIDUAL_ROTATION_LEMMA_20260810` and
`FLOWER_RESIDUAL_WALL_PAYMENT_POLARITY_LEMMA_20260810` (additive form) against
`CROSS_STAR_HOLE_PIVOT_LEMMA_20260811` (max-deletion) — is recorded at section 8,
item 2 of
[`THREE_NONSINGLETON_CANCELABLE_CONSTRAINT_MAP_20260816.md`](THREE_NONSINGLETON_CANCELABLE_CONSTRAINT_MAP_20260816.md).
Nothing is broken today; the banner exists so the conflict cannot hide when the
rung's proofs are composed. **Labeling only**: no definition and no step in this
file is changed.

## Setting

Let `(X,{f})` be an EFX allocation with unenvied charity.  Choose a nonempty
proper packet `R subset X_q`, put `C=X_q\R`, and assume

\[
v_q(f)>v_q(R). \tag{1}
\]

The selected replacement target is `C+f`.  Suppose a most-envious external
source `a != q` responds with a common-safe desired bundle
`A subseteq C+f`.

## Floater-retention fact

Every such external response has the form

\[
A=K+f,
\qquad \varnothing\ne K\subseteq C. \tag{2}
\]

Indeed, if `f notin A`, then `A subseteq C subset X_q`.  Every proper subset
of `X_q` has value at most `tau_i(X_q)<=v_i(X_i)` for every observer `i`, so
no external agent can desire `A`.  Thus `f in A`.
Moreover `K` cannot be empty, because base charity dominance prevents any
agent from desiring `{f}`.

Regarded as a replacement target for slot `q`, bundle (2) has exact label

\[
I_q=\{f\},
\qquad
O_q=X_q\setminus K=R+(C\setminus K). \tag{3}
\]

## Complement-return theorem

Define the full released-complement target

\[
H_a=X_a+O_q. \tag{4}

Then the following sequential alternatives are exhaustive.

1. **Direct `q` self-source.** If `q` desires `A`, its common safety makes
   `q -> q` a PI self-edge, whose only incoming good `f` is unallocated.
2. **Complement return.** If `q` is a most-envious source for `H_a`, then
   `a -> q -> a` is a release-compatible PI two-cycle.
3. **Named augmentation.** If `q` desires `H_a` but is not a source, an
   inclusion-minimal desired subset names a non-`q` source `b`.  A source
   outside `{q,a}` grows the component; if all sources are internal, both
   targets have only source `a` and form an explicit Hall defect missing `q`.
4. **Core capture.** If `q` does not desire `H_a`, then
   \[
   v_q(X_a+X_q\setminus K)\le v_q(X_q). \tag{5}
   \]

The incoming sets in branch 2 are `{f}` and `O_q`.  They are disjoint, `f`
is initially unallocated, and edge (3) releases all of `O_q`; hence the
cycle is PI.  Branch 3 uses the identical support after replacing `q` by an
actual most-envious source of (4).  No packet cardinality enters the proof.

## Strict capture interval

Put `b=v_q(X_q)`.  Equation (5) and additivity give

\[
v_q(K)\ge v_q(X_a). \tag{6}

In the positive nondegenerate convention the compared bundles are distinct,
so (6) is strict.  In a PI-free state branch 1 is excluded; common safety of
`A=K+f` then gives

\[
v_q(K)+v_q(f)<b. \tag{7}

Every surviving external response therefore satisfies the strict interval

\[
v_q(X_a)<v_q(K)<v_q(X_q)-v_q(f). \tag{8}

This is stronger than a generic failure to return: the response must retain
inside `X_q` a core worth more to `q` than the source's entire old bundle,
but not enough to let `q` source the `f`-augmented response itself.

## Mutual-source exclusion in the flower

Let `r` be the other mutual-cycle owner.  The flower gives a desired bundle
`T_r+f` for `q`, while `X_r=T_r+B_r` with nonempty positive `B_r`.  Therefore

\[
v_q(X_r)>v_q(X_q)-v_q(f). \tag{9}
\]

Taking `a=r` in (8) contradicts (9).  Hence the other mutual owner can never
survive as a strict core-capture source: every `r`-sourced replacement wall
closes by a direct or complement return.  Only the two external owners
`c,s` remain possible in a PI-free flower obstruction.

## Root-flip payment reservoir

For an external survivor put

\[
\Delta_a=v_q(K)-v_q(X_a)>0.
\]

The same desired bundle `T_r+f` and the upper half of (8) give

\[
v_q(T_r)>v_q(X_q)-v_q(f)>v_q(K)>\Delta_a. \tag{10}
\]

Consequently there is an inclusion-minimal nonempty packet
`P subseteq T_r` with

\[
v_q(P)>\Delta_a. \tag{11}
\]

Giving `K+f` to `a`, giving

\[
Q=(X_q\setminus K)+X_a+P
\]

to `q`, and leaving `r` with `X_r\P` is therefore a complete half-turn in
which `a,q` strictly improve and only `r` may lose.

More generally choose `H subseteq X_q\K` and form

\[
Y_a=K+f,
\qquad
Y_q=(X_q\setminus(K\cup H))+X_a+P,
\qquad
Y_r=(X_r\setminus P)+H, \tag{12}
\]

fixing the fourth owner.  This is a complete allocation.  It preserves `r`
and strictly improves `q,a` whenever

\[
v_r(H)\ge v_r(P),
\qquad
v_q(P)>\Delta_a+v_q(H). \tag{13}
\]

Thus the external core-capture branch has a canonical cap-free root flip.
Its only remaining packet-selection question is the two-row compensation
system (13).  Once such `P,H` are selected, the response-Hall labels are

| target | incoming | release |
|---|---|---|
| `a` | `K+f` | `X_a` |
| `q` | `X_a+P` | `K+H` |
| `r` | `H` | `P` |

The three incoming sets are pairwise disjoint.  Every one is supplied:
`f` is initially unallocated, while the three edges release `K`, `X_a`,
`P`, and `H`.  In the nondegenerate convention (13) makes all three intended
owners strict improvers.  Hence an internal response SDR is a PI edge set;
without one, Hall's theorem gives the exact open or deficient boundary.

## Composition with charity absorption

If the same packet replacement also has a charity wall, the charity-
absorption lemma adds a target consuming `R`.  Thus both failure types now
feed one finite response-Hall relation:

- target responses retain `f` and release `X_q\K`;
- complement returns consume that whole release;
- charity absorptions consume `R subseteq X_q\K` and release an owner
  bundle.

With four owners, only the other external owner can be newly exposed before
the source relation is closed.

The support and scalar implications replay in
[`packet_replacement_complement_return_audit.json`](packet_replacement_complement_return_audit.json).

## Claim boundary

This theorem closes every direct or complement return, eliminates the other
mutual owner as a surviving source, and supplies a canonical paid half-turn
with exact response-Hall support for every external survivor.  It does not
prove the two-row compensation system (13), eliminate the remaining Hall
defects, close the `GG` flower, or prove four-agent additive EFX.

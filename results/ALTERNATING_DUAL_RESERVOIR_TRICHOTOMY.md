# Alternating dual-reservoir trichotomy

**Date:** 2026-08-09

**Status:** cap-free analytic escape theorem; strict same-offer refinement open

**Orders:** `(p,s,q,r)` and `(p,q,s,r)` with `p={x}` fixed, plus their
half-turns

## Purpose

The anchored-or-any-desired extension target asks for either an anchored EFX
suffix improvement or an EFX allocation promoting `p` to a desired subset of
its champion offer `X_r+f`. The reservoir-exchange theorem settles the
surviving external-observer order `(p,s,r,q)`, but does not preserve the
relative priority of `q` and `r` required here.

The theorem below isolates the exact additional obstruction. It uses no
packet-size bound.

## Setup

Let

\[
X_p=\{x\},\quad X_s=\{y\},\quad
X_r=T_r\mathbin{\dot\cup}B_r,\quad
X_q=T_q\mathbin{\dot\cup}B_q,
\]

with charity good `f`, and put `b_i=v_i(X_i)`. Let

\[
D_p=T_r+f,\qquad W=X_q+B_r,qquad t=\tau_r(D_p).
\]

The sets `D_p` and `W` are disjoint. Assume `D_p` is desired by `p`, `q`
strictly envies `X_p={x}`, `B_r` is nonempty, and the two compatible families
from `r` and `s` into `X_q` are absent. Equivalently, no subset of `W` is
desired by `r` or `s`.

## Theorem

At least one of the following holds:

1. **Same-offer extension.** There is a common-safe `R subseteq W` with
   `v_r(R)>=tau_r(D_p)`. Then

   \[
   (Y_p,Y_s,Y_q,Y_r)=(D_p,\{y\},\{x\},R)
   \]

   is EFX and promotes `p` to its selected champion set.
2. **Anchored q-handoff.** There is a desired `A subseteq W` for `q` with
   `v_r(D_p)>=tau_r(A)`. Then

   \[
   (Y_p,Y_s,Y_q,Y_r)=(\{x\},\{y\},A,D_p)
   \]

   is EFX and lexicographically improves the base in `(p,s,q,r)`.
3. **Opposite-reservoir promotion.** There is a desired `A subseteq W` for
   `p` with `v_r(D_p)>=tau_r(A)`. Then

   \[
   (Y_p,Y_s,Y_q,Y_r)=(A,\{y\},\{x\},D_p)
   \]

   is EFX and improves `p`, but `A` need not lie in the champion offer
   `X_r+f`.

## Proof

Because `q` owns `X_q` and values are positive,

\[
v_q(W)=b_q+v_q(B_r)>b_q.
\tag{1}
\]

Hence `W` contains a desired set: choose an inclusion-minimal subset on which
some agent crosses her base utility. Every one-good deletion lies below every
observer's base, so the subset is common-safe. Compatible-family absence
rules out `r` and `s` as its source; its source is `p` or `q`.

If `v_r(W)<t`, choose such a desired set `A subseteq W`. Then

\[
\tau_r(A)\le v_r(A)\le v_r(W)<t\le v_r(D_p).
\]

Source `q` gives alternative 2 and source `p` gives alternative 3.

Now suppose `v_r(W)>=t`. Choose an inclusion-minimal `R subseteq W` with
`v_r(R)>=t`. If `R` is common-safe, alternative 1 holds. Otherwise some
deletion `R-h` crosses an observer's base utility. A minimal crossing subset
`A subseteq R-h` is desired, and its source is again `p` or `q`. Minimality
of `R` gives

\[
v_r(A)\le v_r(R-h)<t\le v_r(D_p),
\]

so source `q` gives alternative 2 and source `p` gives alternative 3.

In every allocation above, the active and payment bundles are disjoint and
common-safe. Agents retaining `x` or `y` have only base-safe comparisons.
Agent `q`, when assigned `x`, strictly exceeds `b_q` by the alternating envy
premise; an agent assigned a desired set strictly exceeds her base. The only
recipient who can remain below base is `r`, and the displayed `r` inequality
is exactly her sole nontrivial external EFX comparison. Thus each
construction is EFX. \(\square\)

## Cap-free priority-order consequence

All three alternatives are EFX and lexicographically improve the base in
both `(p,s,q,r)` and `(p,q,s,r)`: alternative 1 and alternative 3 improve
first-priority `p`, while alternative 2 fixes `p,s` and improves `q`.
Therefore:

> **Dual-reservoir escape theorem.** An arbitrary-packet alternating state
> with the compatible families absent is not globally lexicographically
> maximal in either priority order `(p,s,q,r)` or `(p,q,s,r)`.

If one of the compatible families is present, its standard PI cycle already
gives an EFX improvement. Hence the conclusion holds without assuming their
absence as a separate global branch. Half-turn relabeling proves the same
statement for `(s,p,r,q)` and `(s,r,p,q)`.

Together with the root-flip and reservoir-exchange theorems, all eight hard
alternating priority orders are now closed cap-free. Combined with the 16
easy orders, this proves the
[`cap-free alternating global-lex theorem`](ALTERNATING_GLOBAL_LEX_CAPFREE_THEOREM.md).

This order-level theorem is sufficient for the wider lexicographic
maximality argument. The stricter same-champion-offer dichotomy requested in
the present goal remains unresolved for the reason below.

## Exact remaining same-offer gate

The requested two-branch extension-or-handoff lemma follows if alternative 3
can always be converted into either:

- an anchored suffix reallocation; or
- a promoted allocation whose root bundle is a desired subset of `X_r+f`.

This is the only branch not settled by the two reservoir arguments. It is a
genuine branch, not a proof artifact: one of the 18 frozen eleven-good
profiles selects an opposite-reservoir `p`-set
`{tq1,bq1,br0,br1}`. In that profile a different same-offer desired set
`{br0,f}` does extend, paid by `{tr1}`. Thus “any desired subset” is already
essential at this reduced gate.

Two sharper normal forms are exactly false in the binary split cell:

1. every same-offer desired set need not admit a two-safe payment; and
2. even after forcing the primal and dual reservoir reversals to have the
   hard sources `r` and `p`, the same-offer two-safe-pair condition can fail.

The second strict model still has many anchored EFX improvements. Therefore
neither bounded refutation is a counterexample to the unrestricted dichotomy.
It shows that the final proof must use a genuinely three-agent anchored
suffix allocation or a promoted residual allocation more general than the
two-safe normal form.

## Evidence and trust boundary

The constructive audit
[`alternating_dual_reservoir_trichotomy_audit.json`](alternating_dual_reservoir_trichotomy_audit.json)
replays the theorem on 18 frozen eleven-good profiles:

- 16 use the selected same-offer extension;
- one uses the anchored `q`-handoff;
- one exposes the opposite-reservoir `p` branch; and
- all 18 nevertheless have a same-offer desired/payment pair after allowing
  an alternate desired subset.

The analytic theorem is cap-free; the census is corroboration only. The SAT
profiles
[`alternating_same_offer_pair_gate_2222.json`](alternating_same_offer_pair_gate_2222.json)
and
[`alternating_cross_source_no_same_offer_pair_2222.json`](alternating_cross_source_no_same_offer_pair_2222.json)
are bounded falsification probes and support no negative conclusion about the
unrestricted dichotomy.

Half-turn relabeling gives the identical trichotomy for both `s`-rooted hard
orders. The anchored-or-any-desired same-offer refinement and complete
four-agent additive EFX remain open; the alternating global-lex topology does
not.

# Alternating two-safe-bundle reduction

**Date:** 2026-08-09
**Status:** cap-free analytic reduction and cap-free safe-pair existence theorem
**Order:** `(p,s,r,q)` with `p` fixed at `{x}`

## Common safe-set system

Let `X` be the base EFX allocation and write

\[
 b_i=v_i(X_i),\qquad
 \tau_i(Z)=\max_{g\in Z}v_i(Z\setminus\{g\})
\]

for every nonempty bundle `Z`, with `tau_i(empty)=0`.

(*Cancelable-class repair 2026-08-16, second pass:* the definition previously
read `tau_i(Z)=v_i(Z)-min_{g in Z}v_i(g)` — the additive form, which
coincides with the max-deletion form above only under additivity and
conflicts with the convention of `ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md`,
which hands off directly to this reduction.  The proof below already uses the
max-deletion reading at every step — its key step states "Inequality (3) is
precisely `v_q(Y_q) >= max_{g in D} v_q(D\{g})`", and the downward-closure
and deletion-remainder uses follow from monotonicity alone — so line 12 was
the only outlier.  Flagged as the blocking defect of the final-gate referee
report; fix verified there before application.)  Define the common
base-safe family

\[
 \mathcal C=\{Z:\tau_i(Z)\le b_i\text{ for every agent }i\}.
\tag{1}
\]

This family is downward closed.  A bundle `D` is a desired set for agent
`a` at the base exactly when

\[
 D\in\mathcal C\quad\text{and}\quad v_a(D)>b_a.
\tag{2}
\]

The definition is independent of packet sizes.

## Reduction lemma

Assume `X_p={x}` and `X_s={y}`.  Let `D,Q` be disjoint bundles containing
neither `x` nor `y`, and suppose

\[
 D,Q\in\mathcal C,
 \qquad v_q(Q)\ge\tau_q(D).
\tag{3}
\]

Then either of the following conditions produces a rooted EFX allocation
that lexicographically improves `X` in priority order `(p,s,r,q)`:

1. `D` is desired by `s`.  Allocate
   \[
   Y_p=\{x\},\quad Y_r=\{y\},\quad Y_s=D,\quad Y_q=Q.
   \tag{4}
   \]
2. `D` is desired by `r`.  Allocate
   \[
   Y_p=\{x\},\quad Y_s=\{y\},\quad Y_r=D,\quad Y_q=Q.
   \tag{5}
   \]

All other goods may remain unallocated.

## Proof

Consider (4).  Agent `p` keeps its base bundle.  Every deletion remainder
of `D` and `Q` is worth at most `b_p` to `p` by (1), while deleting the only
good from `{y}` leaves the empty bundle.  Hence `p` has no strong envy.

Agent `r` receives `{y}`.  In the alternating state `r` strictly envies
`X_s={y}`, so `v_r(y)>b_r`.  The base-safety of `D` and `Q` therefore makes
all of `r`'s comparisons safe.  Agent `s` receives the desired bundle `D`,
so `v_s(D)>b_s=v_s(y)`.  Base-safety of `Q` makes `s`'s only nontrivial
external comparison safe.  Self-comparisons are automatic by
nonnegativity.

Finally, `q`'s only nontrivial comparison is to `D`: comparisons to the two
singleton bundles vanish after deletion, and self-comparisons are
automatic.  Inequality (3) is precisely

\[
 v_q(Y_q)\ge
 \max_{g\in D}v_q(D\setminus\{g\}),
\]

so `q` has no strong envy.  Thus `Y` is EFX.  Agent `p` is unchanged and
`s` strictly improves, so `Y` lexicographically improves `X` in order
`(p,s,r,q)`.

For (5), agents `p` and `s` retain their base singleton bundles.  Agent `r`
receives a desired bundle and hence strictly improves over `b_r`.
Base-safety handles every comparison made by `p`, `s`, and `r`; (3) again
handles `q`'s comparison to `D`.  Consequently (5) is EFX, and its utility
vector agrees with `X` at `p,s` and strictly improves at `r`.  This is the
required lexicographic improvement. \(\square\)

## Safe-pair packing theorem

The surviving external-observer theorem is implied by the following pure
packing statement.

> **Alternating safe-pair packing lemma.** Under the alternating structural
> premises and absence of the four compatible desired families, there are
> disjoint `D,Q` in the common safe family `C` such that `D` is desired by
> `s` or `r` and `v_q(Q)>=tau_q(D)`.

The [`reservoir-exchange lemma`](ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md)
now proves this statement for arbitrary packet sizes.  It starts from
`D=T_q+f` and `U=X_r+B_q`, then uses an inclusion-minimal `q`-threshold set
or reverses an unsafe threshold set into a new desired set.  The proof uses
only positivity, the selected desired block, and absence of the compatible
`p`- and `q`-into-`X_r` families.

The packing formulation has three useful features:

- it mentions no candidate allocation or moving EFX threshold;
- all feasibility constraints except the final `q` threshold belong to one
  downward-closed set system; and
- the critical-minimum contraction lemma applies to both `D` and `Q`
  directly, giving a cap-free route through minimal unsafe walls.

## Exact binary theorem and frozen-profile evidence

The safe-pair packing lemma is exact QF_LRA-UNSAT in the corrected full
binary `(2,2,2,2)` cell.  The direct formula blocks all 37,338 feasible
ordered choices of source, desired bundle, and disjoint safe `q` bundle.
Together with the reduction above, this proves the singleton-return target
and hence the rooted external-observer lemma in the sole binary cell that
was previously unresolved.  See
[`ALTERNATING_TWO_SAFE_BUNDLE_BINARY_THEOREM.md`](ALTERNATING_TWO_SAFE_BUNDLE_BINARY_THEOREM.md).

An exhaustive census over all 39,366 singleton-return allocations in each
of 18 exact eleven-good adversarial profiles finds at least one safe pair in
every profile.  The corpus includes the 12 models produced by the targeted
singleton-return CEGAR run, the three exact countermodels to narrower
structured menus, and three exact countermodels to false base-remainder
strengthenings.  See
[`alternating_singleton_return_model_analysis.json`](alternating_singleton_return_model_analysis.json)
and
[`analyze_alternating_singleton_return_models.py`](../tracks/parkability/analyze_alternating_singleton_return_models.py).

The direct UNSAT result proves the full binary cell, while the census is only
an adversarial audit.  The later analytic reservoir-exchange proof supersedes
the packet-size restriction and does not depend on that UNSAT result.
Complete four-agent additive EFX remains open.

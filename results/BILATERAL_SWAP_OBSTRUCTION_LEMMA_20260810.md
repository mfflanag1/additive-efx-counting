# Bilateral item-swap obstruction lemma

**Date:** 2026-08-10

**Status:** cap-free analytic lemma; the flower-specific PI routing remains
open

## Statement

Let `X` be an EFX allocation for positive additive valuations. Choose
distinct owners `r,q`, goods `h in X_r`, `b in X_q`, and form

\[
Y_r=X_r-h+b,\qquad Y_q=X_q-b+h,
\]

leaving every other bundle unchanged. Assume `r` precedes `q` in the fixed
priority and

\[
v_r(b)>v_r(h). \tag{1}
\]

If `Y` is not EFX, at least one of the following exhaustive obstructions
occurs:

1. an external observer `i notin {r,q}` has an incoming wall against `Y_r`,
   which forces `v_i(b)>v_i(h)`;
2. an external observer `i notin {r,q}` has an incoming wall against `Y_q`,
   which forces `v_i(h)>v_i(b)`; or
3. agent `q` fails one of her EFX comparisons, which forces
   `v_q(b)>v_q(h)`.

Agent `r` cannot fail any comparison. If none of the three obstructions
occurs, `Y` is EFX and is a strict fixed-order lexicographic improvement.

The symmetric statement holds when `q` precedes `r`.

## Proof

For a fixed residual bundle `R`, positivity gives

\[
\tau_i(R+x)
=v_i(R)+\max\{v_i(x)-m_i(R),0\}, \tag{2}
\]

where `m_i(R)` is the least `i`-value of a good in `R`, with the evident
empty-residual convention. Hence the threshold is nondecreasing in the
value of the inserted good, and a strict threshold increase forces a strict
item-value increase.

By (1), `r` strictly improves her own bundle. Her comparisons against every
unchanged target remain safe. Her only changed external target is `Y_q`;
in `r`'s row it replaces the more valuable `b` by the less valuable `h`, so
its threshold weakly decreases by (2). Thus `r` cannot fail.

Every observer outside `{r,q}` keeps her old bundle. Only the two swapped
targets change. If such an observer fails against `Y_r`, old EFX and (2)
give

\[
\tau_i(X_r-h+b)>v_i(X_i)\ge\tau_i(X_r-h+h),
\]

forcing `v_i(b)>v_i(h)`. The target-`q` case reverses the two inserted goods
and forces `v_i(h)>v_i(b)`.

It remains to consider `q`. If `v_q(h)>=v_q(b)`, then `q` weakly improves
her own bundle. Every unchanged target stays safe, while target `r` replaces
the weakly more valuable `h` by `b` and therefore has weakly smaller
threshold in `q`'s row. Hence `q` also remains EFX. Contrapositively, any
failure by `q` forces `v_q(b)>v_q(h)`. This proves exhaustiveness.

When no obstruction occurs, all agents are EFX. Agents preceding `r` are
unchanged, `r` strictly improves, and the only possibly losing changed agent
`q` follows `r`; therefore `Y` is a strict lexicographic improvement.
\(\square\)

## Wall-to-edge consequence

An incoming target-`r` wall strongly envies `X_r-h+b`. Taking an
inclusion-minimal envied subset produces a generalized
`({b}|{h})`-champion edge into `r`. A target-`q` wall similarly produces a
generalized `({h}|{b})`-edge into `q`. Thus every external blockage of a
priority-directed swap supplies exactly one of the two exchange-edge
orientations needed by the flower's bottom-packet PI routing.

The remaining source-`q` obstruction is purely ordinal: both mutual-cycle
owners rank `b` above `h`. The full-capture theorem must either choose an
extremal pair excluding this common orientation or use it to select the next
bottom-crossing swap.

The four scalar implications replay as QF_LRA-UNSAT in
[`bilateral_swap_obstruction_audit.json`](bilateral_swap_obstruction_audit.json).

## Claim boundary

This lemma classifies every failed bilateral swap and converts external
walls to generalized edges. It does not prove that some swap is eligible or
that the resulting exchange edges close a PI cycle. That flower-specific
selection/routing is the next gate.

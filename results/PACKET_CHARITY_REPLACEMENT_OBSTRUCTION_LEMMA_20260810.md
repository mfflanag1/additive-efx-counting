# Packet-for-charity replacement obstruction lemma

**Date:** 2026-08-10

**Status:** cap-free analytic lemma; endpoint selection in the flower remains
open

## Statement

Let `(X,{f})` be an EFX allocation with one unenvied charity good under
positive additive valuations. Choose an owner `q` and a nonempty packet
`R subseteq X_q`. Put `C=X_q\R` and form

\[
Y_q=C+f,\qquad P_Y=R,
\]

leaving every other owner bundle fixed. Assume

\[
v_q(f)>v_q(R). \tag{1}
\]

Then `q` strictly improves and cannot violate either pairwise EFX or charity
dominance. If `(Y,R)` is not EFX with charity, at least one of the following
exhaustive obstructions occurs:

1. an external observer `i != q` strongly envies `C+f`; this forces
   \(v_i(f)>v_i(R)\) and yields a generalized `(f|R)` edge into `q` after
   taking an inclusion-minimal envied subset; or
2. an external observer `i != q` envies the new charity packet `R`; this
   forces \(v_i(R)>v_i(f)\).

If neither obstruction occurs, `Y` is EFX with charity and is a strict
lexicographic improvement for every fixed agent priority.

## Threshold polarity

For a nonempty core `C`, write `c=v_i(C)`, `m_C=min_{g in C}v_i(g)`,
`r=v_i(R)`, and `m_R=min_{g in R}v_i(g)`. Then

\[
\tau_i(C+f)=c+v_i(f)-\min\{m_C,v_i(f)\},
\]

\[
\tau_i(C+R)=c+r-\min\{m_C,m_R\}.
\]

Suppose `v_i(f)<=r`. If `v_i(f)` is below both packet minima, then
`tau_i(C+f)=c`, while `tau_i(C+R)>=c`. Otherwise
`min{m_C,m_R}<=min{m_C,v_i(f)}`, and therefore

\[
\tau_i(C+f)
\le c+v_i(f)-\min\{m_C,m_R\}
\le \tau_i(C+R).
\]

Thus a strict target-threshold increase forces `v_i(f)>v_i(R)`. If `C` is
empty, the new singleton target has zero tail, so no target wall is possible.

For a charity wall, old charity dominance and new failure give directly

\[
v_i(R)>v_i(X_i)\ge v_i(f). \tag{2}
\]

The two wall types therefore have opposite aggregate signs.

## EFX exhaustiveness

By (1), `q` improves her own bundle. Her comparisons against every other
owner are unchanged, and

\[
v_q(C+f)>v_q(C+R)=v_q(X_q)\ge v_q(f)>v_q(R),
\]

so she also dominates the new charity packet. Every other owner keeps her
old bundle. Her only changed owner target is `q`, and her only changed
charity target is `R`. Hence the two obstructions above exhaust every
possible failure.

If an external target wall occurs, the observer strongly envies
`(X_q\R)+f`. Choosing an inclusion-minimal envied subset makes some agent
most envious and gives a generalized edge whose incoming set is `{f}` and
whose prescribed release is `R` (with any additional discard also released).
If the selected desired subset discards `f`, monotonicity gives the parallel
ordinary envy consequence into `q`; otherwise the edge genuinely consumes
`f`. The edge conversion is exactly compatible with BCFF Definition 3.1.

## Flower consequence

The path-blocked full-capture model's nearest partial escape is precisely
this operation: `q` releases two goods to charity and receives `f`. The
lemma explains why any globally lex-maximal flower obstruction must block
every such improving packet replacement with one of two oppositely signed
dependencies. This supplies the charity-incidence rule missing from the
bilateral swap obstruction lemma.

The four scalar implications replay as QF_LRA-UNSAT in
[`packet_charity_replacement_obstruction_audit.json`](packet_charity_replacement_obstruction_audit.json).

## Claim boundary

The obstruction classification is arbitrary-packet and cap-free. It does
not prove that some owner has a packet satisfying (1), nor that successive
target/charity dependencies terminate in an eligible endpoint. Those are the
remaining selection and component-growth gates.

# Exact rank-three five-response classification lemma

**Date:** 2026-08-13

**Status:** cap-free reduction of the exact support response relation to two
forms; sacrificed-owner completion remains

## Five mandatory response edges

At the paid singleton-charity rank-three gate, charity is not a response
target for a represented source. The selected matching contains `r -> q`,
represents `r,q,s`, and has two further owner targets. The sacrificed source
has both

\[
 d\to q\quad\text{and}\quad d\to r.               \tag{1}
\]

The second edge is forced by the literal strong-envy wall against the root
core `A subseteq Y_r`; it cannot be erased when translating the abstract
response graph to the physical support state.

The four possible selected matchings therefore give four five-edge response
relations.

## Two exact exclusions

One form contains

\[
 r\to q,\quad q\to s,\quad s\to d,\quad d\to r,   \tag{2}
\]

which is already a rank-four matching. It is not a live rank-three state.

Another form requires `q -> d` while excluding `q -> r`. This contradicts
the fixed-U q-budget. Let `W=Y_d`. The named packet inequality gives

\[
 v_q(a_1)>v_q(W).                                  \tag{3}
\]

If q has any desired response `D subseteq W`, then

\[
 v_q(a_1)>v_q(W)\ge v_q(D)>F_q,                   \tag{4}
\]

where `F_q` is the relevant base or current floor. The singleton `{a1}` lies
in `Y_r` and is automatically common-safe, so (4) forces `q -> r`. Hence the
claimed exact form cannot occur.

## The two survivors

Exactly two response relations remain:

\[
\begin{aligned}
\mathcal R_2={}&\{r\to q,q\to r,s\to d,d\to q,d\to r\},\\
\mathcal R_3={}&\{r\to q,q\to s,s\to r,d\to q,d\to r\}.
\end{aligned}                                      \tag{5}
\]

The represented paid owners form respectively the cycle `r <-> q` or
`r -> q -> s -> r`. The sacrificed owner `d` lies outside that paid cycle
and responds into both `q` and `r`. This explains why rotating the bare paid
cycle does not close the state: it leaves precisely `d` unpaid.

## Remaining theorem

For either relation in (5), use arbitrary packets on at most three owner
support edges plus one singleton-charity edge to give `d` a safe bundle,
preserve the represented owners' signed payment/observer budgets, and make
the final complete allocation EFX. Alternatively, prove that failure activates
rank growth, a release-compatible PI component, signed support progress, or
a new exact response record.

## Verification and boundary

[`audit_exact_rank_three_five_response_classification.py`](../tracks/parkability/audit_exact_rank_three_five_response_classification.py)
enumerates the four graph forms, independently checks the rank-four exclusion,
and proves implication (4) in exact QF-LRA.

This classifies the named cap-free response interface. It does not establish
full recurrence reachability or finish the four-edge complete-EFX theorem.

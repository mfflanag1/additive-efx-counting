# Four-edge surplus-star selector lemma

**Date:** 2026-08-13

**Status:** cap-free necessary-and-sufficient selector for an all-owner-paid
star completion; failure is an exact separable donor-budget certificate

## Donor budgets

Let `(Y,P)` be the physical rank-three support state.  The represented owners
`R={r,q,s}` are strictly paid, while `d` is the sacrificed owner.  Put

\[
 \Delta_i=v_i(Y_i)-v_i(X_i)>0\quad(i\in R),       \tag{1}
\]

and define the amount needed to restore `d` after giving it current charity:

\[
 \rho_d=\bigl(v_d(X_d)-v_d(Y_d)-v_d(P)\bigr)_+.  \tag{2}
\]

For each represented supplier independently choose

\[
 M_i\in\arg\max\{v_d(S):S\subseteq Y_i,
                              v_i(S)\le\Delta_i\}. \tag{3}
\]

The family is finite and nonempty because the empty packet is feasible.

## Star allocation

Send every nonempty `M_i` to `d`, give all charity `P` to `d`, and retain
every other good:

\[
 Z_i=Y_i\setminus M_i\quad(i\in R),               \tag{4}
\]

\[
 Z_d=Y_d\mathbin{\dot\cup}P
       \mathbin{\dot\cup}\mathop{\dot\bigcup}_{i\in R}M_i,
 \qquad P'=\varnothing.                           \tag{5}
\]

Every represented supplier has at most one outgoing recipient, `d`, and
charity also sends only to `d`.  Therefore (4)--(5) use at most four support
edges, with unrestricted packet sizes.

By (1) and (3), every represented donor remains weakly paid.  Owner `d` is
weakly paid exactly when

\[
 \sum_{i\in R}v_d(M_i)\ge\rho_d.                  \tag{6}
\]

Thus (6) produces an all-owner-paid complete candidate to which the paid-
splice observer-response theorem applies.

## Exact failure separator

Because the feasible sets in (3) are independent, their individual maxima
maximize the total `d`-value over *every* four-edge surplus star.  Hence if
(6) fails, then for every collection of packets `S_i subseteq Y_i`,

\[
 \left[v_i(S_i)\le\Delta_i\ (i\in R)\right]
 \Longrightarrow
 \sum_{i\in R}v_d(S_i)<\rho_d.                   \tag{7}
\]

This is a three-knapsack separator, not a missing topology.

Let

\[
 C_i=Y_i\cap X_d                                  \tag{8}
\]

be the captured base-`d` packet at supplier `i`.  If every `C_i` were donor-
affordable, choosing `S_i=C_i` would return all missing base-`d` support; with
charity, `d` would be paid.  Therefore failure of (6) forces at least one

\[
 v_i(C_i)>\Delta_i.                               \tag{9}

So the only payment obstruction is genuine captured donor margin.  The
four-edge limit itself is already respected.

## Consequence and remaining gate

At a saturated state, either the surplus star is paid and an observer wall
creates a full decorated response, or (9) enters captured-margin response/
support repair.  A universal proof must show that the simultaneous separator
(7) activates retained-support growth, a response replacement, or a
release-compatible connected component.  A countermodel must satisfy (7)
alongside every saturation exclusion at the identical physical record.

## Verification and boundary

[`audit_four_edge_surplus_star_selector.py`](../tracks/parkability/audit_four_edge_surplus_star_selector.py)
exhausts all positive integer valuation rows on a three-donor/two-good-per-
donor model, compares independent maximization with every feasible joint
selection, and checks conservation, edge counts, donor payments, (6)--(7),
and the captured-support implication.  QF-LRA independently verifies all
margin identities.

This lemma does not force (6), reverse (7) or (9), establish observer EFX,
close rank-three recurrence, or prove the four-edge theorem.

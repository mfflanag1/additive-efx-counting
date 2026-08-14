# Rank-three four-edge signed-margin identity lemma

**Date:** 2026-08-13

**Status:** cap-free closure of owner payment for every base- or current-
desired incoming response; exact observer debts remain

## Exact owner margin

Use the four-edge response-reversal candidate.  For owner `i`, write

\[
 \Delta_i=v_i(Y_i)-v_i(X_i),\qquad
 L_i=v_i(\text{packets supplied from }Y_i),\qquad
 I_i=v_i(D_i),                                      \tag{1}
\]

where `D_i` is the response packet received by `i`.  Because the retained
part of `Y_i` and `D_i` are disjoint, the final base margin is exactly

\[
 m_i=v_i(Z_i)-v_i(X_i)=\Delta_i-L_i+I_i.           \tag{2}
\]

This is the full signed-transfer payment coordinate; no packet-size or
item-count assumption occurs.

## Every response incoming core pays

If `D_i` is current-desired,

\[
 I_i>v_i(Y_i),                                     \tag{3}
\]

then `L_i <= v_i(Y_i)` implies

\[
 v_i(Z_i)=v_i(Y_i)-L_i+I_i>v_i(Y_i).              \tag{4}

If instead `D_i` is an ordinary base-desired core, then

\[
 I_i>v_i(X_i).                                     \tag{5}
\]

Since `L_i<=v_i(Y_i)`, nonnegativity of the retained bundle gives

\[
 v_i(Z_i)=v_i(Y_i)-L_i+I_i\ge I_i>v_i(X_i).       \tag{6}

Thus **every** owner receiving a valid ordinary or current response core is
strictly base-paid even if she supplies her entire current bundle. There is
no mixed old-core payment separator. Payment can fail only for an owner who
receives no response core (for example a path endpoint or sacrificed owner).

## Exact observer budget

For each final target `j`, define the base-relative observer debt

\[
 b_{ij}=\bigl(\tau_i(Z_j)-v_i(X_i)\bigr)_+.        \tag{7}

The candidate is EFX exactly when

\[
 m_i\ge\max_{j\ne i} b_{ij}\qquad(i\in N).        \tag{8}

Hence, for every owner receiving a response core, a saturated countermodel
must exhibit a changed target with `b_ij>m_i`. The remaining separator is
observer surplus, not owner payment or an additional graph case.

## Verification and boundary

[`audit_rank_three_four_edge_signed_margin.py`](../tracks/parkability/audit_rank_three_four_edge_signed_margin.py)
independently proves (2), automatic current payment (4), automatic ordinary
payment (6), and the surplus implication in exact QF-LRA.

This lemma does not give an incoming response to every endpoint/sacrificed
owner, establish safety of enlarged final targets, or finish the universal
four-edge theorem.

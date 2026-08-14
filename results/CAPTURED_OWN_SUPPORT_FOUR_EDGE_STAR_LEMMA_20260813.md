# Captured-own-support four-edge star lemma

**Date:** 2026-08-13

**Status:** cap-free complete four-edge return of every captured `d`-base
good; donor capture/payment and observer safety remain

## Canonical return

Let `(X,P_X)` be the base allocation and let `(Y,P)` be the physical paid
rank-three support state with sacrificed owner `d`.  For each represented
owner `i != d`, define the captured `d`-base packet

\[
 C_i=Y_i\cap X_d.                                  \tag{1}
\]

Return every `C_i` to `d`, leave every other owner good at its current
holder, and give the complete current charity packet `P` to `d`:

\[
 Z_i=Y_i\setminus C_i\quad(i\ne d),               \tag{2}
\]

\[
 Z_d=Y_d\mathbin{\dot\cup}
       \mathop{\dot\bigcup}_{i\ne d}C_i
       \mathbin{\dot\cup}P,
 \qquad P'=\varnothing.                           \tag{3}
\]

Goods of `X_d` already held by `d` stay in place.  If a base-`d` good is in
current charity, it is included through `P`.

## Edge bound and sacrificed-owner payment

Every represented supplier sends goods only to `d`.  There are at most three
such suppliers, and charity also sends only to `d`.  Hence the complete
allocation uses at most four support-transfer edges:

\[
 \{i\to d:C_i\ne\varnothing, i\ne d\}
 \mathbin\cup\{\mathrm{charity}\to d\}.           \tag{4}
\]

Packet cardinalities are unrestricted.  The final `d` bundle contains all
of `X_d` plus every non-base-`d` good previously held by `d` and every
current charity good not already in `X_d`.  Since current charity is
nonempty and disjoint from the base owner bundles,

\[
 v_d(Z_d)>v_d(X_d).                                \tag{5}
\]

Thus the sacrificed owner is strictly paid without any residual-split or
provenance-alignment hypothesis.

## Exact donor separator

For represented donor `i != d`, put

\[
 \Delta_i=v_i(Y_i)-v_i(X_i)>0.                    \tag{6}
\]

Its exact final base margin is

\[
 m_i=v_i(Z_i)-v_i(X_i)
     =\Delta_i-v_i(C_i).                           \tag{7}

Therefore donor `i` remains weakly paid if and only if

\[
 v_i(C_i)\le\Delta_i.                             \tag{8}

Failure is the strict captured-margin inequality

\[
 v_i(C_i)>\Delta_i.                               \tag{9}

If (8) holds for all represented owners, (2)--(3) are an all-owner-paid
complete candidate on at most four edges.  Any EFX failure then enters the
paid-splice decorated-response machinery.  If (9) holds, the entire remaining
problem is donor compensation or a captured-margin saturated exit; returning
captured own support itself never violates the four-edge budget.

## Relation to the two-hole polarity

The two-hole residual-split lemma showed that terminal split failure
concentrates enough `d`-value in captured base support (and possibly one
parked own good).  The present lemma supplies the missing physical return
geometry for that support.  It does not pay donors whose margins are
captured; those inequalities must be reversed by a response replacement,
retained-support growth, or a connected compensation component.

## Verification and boundary

[`audit_captured_own_support_four_edge_star.py`](../tracks/parkability/audit_captured_own_support_four_edge_star.py)
exhausts every distribution of labeled base-`d`, outside, and charity atoms
among the four owners and charity in a small independent universe.  It checks
conservation, empty charity, the four-edge bound, strict `d` payment, and the
donor margin identity.  QF-LRA separately verifies (7)--(9).

This lemma does not eliminate donor capture, pay all represented owners,
prove observer safety, close exact rank-three recurrence, or prove the
four-edge theorem.

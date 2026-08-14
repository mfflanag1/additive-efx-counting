# PI-free rank-three cycle current-edge lemma

**Date:** 2026-08-13

**Status:** cap-free exclusion of the all-ordinary response-cycle subcase

## Two exact response forms

The saturated paid-singleton rank-three relation has one of the owner cycles

\[
 r\to q\to r                                           \tag{1}
\]

or

\[
 r\to q\to s\to r.                                    \tag{2}
\]

Call a displayed edge **ordinary-available** when its target contains a
base-common-safe subset desired above the source's base utility. If every
edge of (1), respectively (2), is ordinary-available, choose one such core
on each edge. Their parent owner targets are distinct, so the cores are
pairwise disjoint. The cycle is an ordinary release-compatible PI cycle,
forbidden at the globally maximal PI-free base.

Therefore a PI-free survivor satisfies

\[
 \neg O_{rq}\ \lor\ \neg O_{qr}                  \tag{3}
\]

in the two-cycle form, and

\[
 \neg O_{rq}\ \lor\ \neg O_{qs}\ \lor\ \neg O_{sr} \tag{4}
\]

in the three-cycle form.

The exact response relation guarantees that each missing ordinary edge is
nevertheless realized by a current-safe desired core. Hence at least one
cycle edge is genuinely current-only. If source `i` receives its core after
reversal, then

\[
 v_i(D_i)>v_i(Y_i)                                  \tag{5}
\]

and `i` remains strictly above her current utility even if she releases her
entire current bundle. Thus every PI-free cycle rotation has at least one
automatically strict current-paid owner. Any remaining payment failure is
confined to the old/mixed edges and the sacrificed owner.

## Verification and boundary

[`audit_pi_free_rank_three_cycle_current_edge.py`](../tracks/parkability/audit_pi_free_rank_three_cycle_current_edge.py)
exhausts all ordinary/current labels of the two exact cycle forms and checks
(3)--(4). QF-LRA independently verifies (5) with unrestricted outgoing
packet value.

This lemma does not pay the remaining old-edge owners, restore the sacrificed
owner, prove observer safety, force a functional four-edge completion, or
close the rank-three theorem.

# Permanent-anchor two-source root-response topology-or-cross-capture lemma

**Date:** 2026-08-14

**Status:** cap-free exact topology for two disjoint root responses; cross-
state coexistence and simultaneous capture remain open

## Two disjoint root responses

Use the permanent-anchor partial allocation

\[
 B_r=Y_r\mathbin{\dot\cup}A,
 \qquad \delta_r=v_r(B_r)-v_r(X_r)>0,             \tag{1}
\]

where `Y_r` is supplied by `r`, `A` by `q`, and singleton `p` by charity.
Let distinct nonroot sources `u,v` have pairwise-disjoint common-safe cores

\[
 F_u,F_v\subseteq B_r,qquad
 v_u(F_u)>v_u(B_u),\quad v_v(F_v)>v_v(B_v).       \tag{2}
\]

Give each source its core and give `p` to the root.  Both sources strictly
improve.  The root remains strict exactly when

\[
                         v_r(F_u\mathbin{\dot\cup}F_v)
                         <\delta_r+v_r(p).         \tag{3}
\]

## Exact support census

Only two current supplier cells occur in the root.  For each cell, record
which of `root,u,v` retains a nonempty part.  Across the three possible source
pairs and every nonempty presence pattern in which both sources receive a
packet, there are 96 signatures:

- 76 already use at most four supplier pairs including charity;
- 20 initially use five or six pairs.

Let

\[
 K=A\setminus(F_u\mathbin{\dot\cup}F_v)           \tag{4}
\]

be the residual anchor cell.  Return all of `K` to its supplier `q`.  This
deletes `q -> r` without adding an edge.  It repairs every overflow signature
except exactly the following `2 x 2` cross:

\[
 \{u,v\}=\{d,s\},qquad
 F_u\cap Y_r,F_u\cap A,F_v\cap Y_r,F_v\cap A
 \text{ all nonempty}.                            \tag{5}
\]

There are four presence variants of (5), depending on residual root support.
After returning `K`, (5) still uses

\[
 r\to d,\ r\to s,\ q\to d,\ q\to s,
 \ \mathrm{charity}\to r.                       \tag{6}
\]

and therefore five pairs.  Every other signature uses at most four.  This is
an if-and-only-if physical classification; packet sizes are unrestricted.

Returning `K` changes the root condition to

\[
 v_r(F_u\mathbin{\dot\cup}F_v\mathbin{\dot\cup}K)
 <\delta_r+v_r(p).                                \tag{7}
\]

Failure of (7) is an exact anchor-residual root-capture certificate.

## Uncross the unique `2 x 2` overflow

Write

\[
 R_x=F_x\cap Y_r,qquad Q_x=F_x\cap A
 \quad(x\in\{d,s\}),                              \tag{8}
\]

and put `mu_x=v_x(F_x)-v_x(B_x)>0`.

If one of `R_x,Q_x` remains desired above `B_x`, replace `F_x` by an
inclusion-minimal desired subcore of that pure supplier cell.  Deletion
preserves common safety.  Recompute the residual anchor relative to the two
cores actually moved and return **all** of that residual to `q`.  The other
source may retain its mixed core, but the resulting graph has only three
owner pairs plus charity, so it fits within four edges.  Root failure is the
exact value of the new moved union plus this recomputed anchor residual
against `delta_r+v_r(p)`.

If neither supplier portion remains desired for either source, additivity
gives the four simultaneous capture inequalities

\[
 v_x(R_x)\ge\mu_x,qquad v_x(Q_x)\ge\mu_x
 \quad(x\in\{d,s\}).                              \tag{9}
\]

Thus the unique irreducible topology is converted into either a pure-cell
four-edge probe, root capture, or a **two-source/two-supplier cross-capture**
certificate.  No generic packet-graph obstruction remains.

## Relation to alternating response recurrence

An alternating different-source root recurrence would supply precisely two
or three source-labeled cores in the same physical root target.  First apply
the ordinary shared-target uncrossing lemma to make a pair disjoint or obtain
overlap capture.  Conditional on transporting the two disjoint cores to one
common fixed-`B` state with (2), the present lemma closes their entire
physical topology.

That cross-state transport is still load-bearing: safety and desire at two
different bilateral probes do not automatically imply (2) at a common state.
The theorem therefore does not claim that every alternating recurrence has
already produced the simultaneous pair.

## Claim boundary

Proved: the exact 96-pattern topology classification, anchor-residual repair,
pure-cell uncrossing, source payment, root-payment identities, and the cross-
capture alternative (9).  Not proved: common-state transport of responses
from distinct probes, contradiction of root/cross capture, observer safety of
the simultaneous candidate, closure of three alternating sources, the
fixed-`U` theorem, or general EFX.

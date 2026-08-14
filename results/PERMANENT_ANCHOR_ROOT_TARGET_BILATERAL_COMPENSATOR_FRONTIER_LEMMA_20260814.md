# Permanent-anchor root-target bilateral-compensator frontier lemma

**Date:** 2026-08-14

**Status:** cap-free exact four-edge frontier for every root/source bilateral
exchange with charity paid to the root; exact response recurrence remains open

## Setting

Use the permanent-anchor partial allocation

\[
 B_r=Y_r\mathbin{\dot\cup}A,\qquad
 B_q=Y_q\setminus A,
 \qquad \delta_r=v_r(B_r)-v_r(X_r)>0,             \tag{1}
\]

with positive singleton charity good `p`.  A transported disjoint response
into the root fixes a nonroot source `i`.  The construction below does not
restrict itself to the response core: it exhausts every bilateral exchange
between the complete physical bundles `B_r` and `B_i` of the stated form.

Choose any nonempty packet `H subseteq B_r` and any `D subseteq B_i`.  Form

\[
\begin{aligned}
 C_r&=(B_r\setminus H)\mathbin{\dot\cup}D
                         \mathbin{\dot\cup}\{p\},\\
 C_i&=(B_i\setminus D)\mathbin{\dot\cup}H,\\
 C_j&=B_j\qquad(j\notin\{r,i\}).                 \tag{2}
\end{aligned}
\]

This is a complete physical allocation.  Put

\[
 H_r=H\cap Y_r,\qquad H_q=H\cap A.               \tag{3}
\]

## Exact physical edge criterion

Relative to the original current suppliers, (2) can use only

\[
 charity\to r,quad r\to i\ (H_r\ne\varnothing),
 \quad q\to i\ (H_q\ne\varnothing),
 \quad i\to r\ (D\ne\varnothing),
 \quad q\to r\ (A\setminus H_q\ne\varnothing). \tag{4}
\]

Self-pairs disappear and coincident pairs merge.  Hence if `i=q`, every
choice uses at most three edges.  If `i!=q`, the allocation has five edges
in exactly one support signature:

\[
 H_r\ne\varnothing,\quad
 \varnothing\ne H_q\subsetneq A,\quad
 D\ne\varnothing.                                \tag{5}
\]

Every other choice has at most four edges.  Criterion (5) is if and only if;
no packet-size assumption is used.

## Exact payment inequalities

The source is strictly better than at `B` exactly when

\[
                         v_i(H)>v_i(D).            \tag{6}
\]

The root remains strictly above its fixed base exactly when

\[
 v_r(H)-v_r(D)<\delta_r+v_r(p).                   \tag{7}
\]

Call `(H,D)` **admissible** when `H` is nonempty, (5) does not hold, and
(6) holds.  Whenever an admissible pair also satisfies (7), (2) is an
explicit priority-valid complete probe through at most four physical
supplier pairs.  If it is EFX, it is the required endpoint.  If not,
minimum-response extraction gives the next precisely located decorated
response at this probe.

## Exact universal failure separator

For every nonempty `H`, the empty compensator is admissible by positivity.
Choose

\[
 D_H\in\arg\max\{v_r(D):(H,D)\text{ is admissible}\}.           \tag{8}
\]

If no admissible pair satisfies (7), then

\[
 v_r(D_H)\le v_r(H)-\delta_r-v_r(p),              \tag{9}
\]

and maximality propagates the following inequality to the entire exact
four-edge bilateral family:

\[
 \boxed{
 (H,D)\text{ admissible}
 \quad\Longrightarrow\quad
 v_r(D)\le v_r(H)-\delta_r-v_r(p)
 }.                                                \tag{10}
\]

Taking `D=emptyset` gives, for every nonempty physical root packet,

\[
 v_r(H)\ge\delta_r+v_r(p).                        \tag{11}
\]

In particular (11) holds for every singleton good in `B_r`.  This is much
stronger than the earlier response-only wall.  For every `H` outside the
unique overflow pattern (5), (10) additionally says that **every** packet
strictly cheaper to the source than `H` is too root-poor to compensate it.
In the overflow pattern, only `D=emptyset` is edge-feasible, and (11) is the
exact residual.

## Full-bundle swap reaches direct safety

Now use the response premise.  If its desired core is `E subseteq B_r`, then
positivity gives

\[
                         v_i(B_r)\ge v_i(E)>v_i(B_i).             \tag{12}
\]

Take `H=B_r` and `D=B_i`.  This pair is admissible: (12) pays the source,
and `H_q=A` exhausts the anchor so the five-edge signature (5) is impossible.
The corresponding probe simply swaps the complete root and source bundles
and gives charity to the root.  Its root condition (7) reduces exactly to

\[
                         v_r(B_i)+v_r(p)>v_r(X_r).                \tag{13}
\]

Consequently failure of every bilateral probe implies the direct-safety wall

\[
                         v_r(B_i)+v_r(p)\le v_r(X_r).             \tag{14}
\]

This is not merely a large-response inequality: the protected root's base
bundle directly covers the response source's entire current bundle together
with charity.  Equation (14) is the exact interface that must next be matched
against the sacrificed-source direct-safety/base-margin continuation; that
interface is not asserted here without checking its other observer rows.

## Cardinality consequence of universal failure

Let `k=|B_r|`.  Summing (11) over its singleton packets yields

\[
 v_r(B_r)\ge k(\delta_r+v_r(p)).                  \tag{15}
\]

Since `v_r(B_r)=v_r(X_r)+\delta_r`, this is equivalent to

\[
 v_r(X_r)\ge k v_r(p)+(k-1)\delta_r.              \tag{16}
\]

Thus universal bilateral failure forces a quantitatively large old root
base.  This is a necessary condition, not a contradiction by itself.

## Exact local nonvacuity witness

The separator is consistent with positive additivity.  Take

```text
B_r = {a,b},       B_i = {c},       charity = {p},
root row:          a=6, b=6, c=1, p=1, X_r=10,
source row:        a=2, b=2, c=3, p>0.
```

Then `delta_r=2`, the response `E={a,b}` is desired by `i`, and every
admissible `(H,D)` fails (7).  For singleton `H`, the nonempty compensator
is too expensive to the source; with `D=emptyset`, the root loses `6>3`.
For `H={a,b}`, even `D={c}` leaves net root loss `11>3`.  The full-swap wall
is `v_r(B_i)+v_r(p)=2<=10=v_r(X_r)`.

This witness refutes any attempt to close the branch from the bilateral
payment inequalities and positivity alone.  It is not a fixed-`U`, EFX-base,
PI-free, saturated-GG, or general-EFX countermodel.

## Claim boundary

Proved: conservation, the if-and-only-if support criterion (5), exact
source/root inequalities, exhaustive maximization over the complete declared
four-edge bilateral family, the universal separator (10)--(11), the
full-bundle direct-safety alternative (14), and the cardinality inequality
(16).  The exact local witness proves that the separator is scalar-feasible.
Not proved: that these separators contradict generalized PI or all GG
premises, satisfaction of the other observer rows required by the extraction
theorem, observer safety of a probe, closure of its decorated-response
recurrence, the singleton-hit branch, the fixed-`U` theorem, or general EFX.

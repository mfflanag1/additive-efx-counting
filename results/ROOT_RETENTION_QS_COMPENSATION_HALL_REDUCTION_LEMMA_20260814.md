# Root-retention q/s-compensation Hall-reduction lemma

**Date:** 2026-08-14

**Status:** cap-free exact accounting and exhaustive two-creditor reduction;
the final supplier-compatible Hall cut remains open

**Endpoint-6 no-go update.** The compensation identities remain valid, but
they cannot close the sole genuine `Z6` second-creditor row while retaining
the root. `ENDPOINT6_ROOT_FIXED_FOUR_EDGE_COMPLETION_NO_GO_20260814.md`
gives an exact PI-free profile with no EFX allocation in the full 6,411-member
root-fixed four-edge menu. A root/anchor-changing transition is necessary.

## Input

Let `Y` be the current physical support allocation and suppose the protected
first-priority root is strict:

\[
v_r(Y_r)>v_r(X_r)=1.                              \tag{1}
\]

Let `Z` be a complete candidate allocation supplied by the sharp bounded
endpoint theorem after physical expansion, so

\[
v_q(Z_q)\ge1,\qquad v_s(Z_s)\ge1.                 \tag{2}
\]

No payment premise is imposed on `r` or on the sacrifice-eligible owner `d`.

## Exact root-retention reassembly

For each nonroot owner put

\[
C_i=Z_i\cap Y_r,
\]

and let

\[
R=Z_r\setminus Y_r.                              \tag{3}
\]

Choose any physical partition

\[
R=R_q\mathbin{\dot\cup}R_s\mathbin{\dot\cup}R_d. \tag{4}
\]

Define

\[
\begin{aligned}
W_r&=Y_r,\\
W_q&=(Z_q\setminus Y_r)\mathbin{\dot\cup}R_q,\\
W_s&=(Z_s\setminus Y_r)\mathbin{\dot\cup}R_s,\\
W_d&=(Z_d\setminus Y_r)\mathbin{\dot\cup}R_d.
\end{aligned}                                    \tag{5}
\]

Because `Z` is complete, (5) is a complete allocation: the goods newly
captured by the retained root are exactly the `C_i`, and every good released
from the endpoint root bundle lies in exactly one `R_i`.

For `i in {q,s}` define the compensation price

\[
\alpha_i=\max\{0,1-v_i(Z_i)+v_i(C_i)\}.          \tag{6}
\]

Then the exact margin identity is

\[
v_i(W_i)-1
=v_i(Z_i)-1-v_i(C_i)+v_i(R_i).                  \tag{7}
\]

Consequently `W_i` pays owner `i` exactly when

\[
v_i(R_i)\ge 1-v_i(Z_i)+v_i(C_i),                \tag{8}
\]

and it is sufficient to require `v_i(R_i)>=alpha_i`.  From (2),

\[
0\le\alpha_i\le v_i(C_i).                       \tag{9}
\]

Thus retaining the current strict root converts the two possible endpoint
debts `{r,d}` into a two-creditor compensation problem for the already paid
owners `{q,s}`.  Owner `d` receives the unused released pool and may be
sacrificed because the first priority coordinate (1) remains strict.

## Exact Hall cut

Let `P_i` be the family of inclusion-minimal packets `A subseteq R` that:

1. satisfy `v_i(A)>=alpha_i`;
2. obey the current supplier/protected-release filters; and
3. together with a packet for the other creditor keep the final directed
   supplier-to-recipient support set within four edges.

If there are disjoint `A_q in P_q` and `A_s in P_s` belonging to one
compatible release mode, take `R_q=A_q`, `R_s=A_s`, and put the remainder in
`R_d`.  Equations (5)--(8) give a complete root-strict allocation paying both
protected nonroot owners.  A complete EFX audit then gives the requested
endpoint; any failed comparison is passed to the already frozen
response/rank/supplier continuation audit.

If no such pair exists, exactly one of the following holds:

1. `P_q` is empty;
2. `P_q` is nonempty but `P_s` is empty; or
3. both are nonempty and every pair overlaps or violates a common
   supplier/protected/edge-budget mode.

This is the exact two-creditor Hall cut.  It is not implied by two scalar
underpayment inequalities, and it does not merge incompatible supplier
modes.

## Composition with the sharp bounded theorem

The `q,s`-paid theorem shows that every generalized-PI-free bounded profile
has an endpoint satisfying (2), and its sharpness countermodel shows that
both `r` and `d` may genuinely be below base.  Therefore (3)--(9), rather
than a proof that the root endpoint is paid, is the correct cap-free bridge.

Combined with physical failure localization, a saturated survivor must now
simultaneously realize:

1. only root/sacrifice sub-base observer walls;
2. failure of every ordinary base-response augmentation; and
3. the supplier-compatible two-creditor Hall cut above.

This is strictly narrower than the former generic two-debt statement.

## Exact audit

`audit_root_retention_qs_compensation_hall.py` exhausts all four-owner
assignments of a four-good universe, every current-root subset, and every
partition of the released root pool.  It verifies 20,000 instances of the
margin identity, 112 active paid-endpoint price bounds, and 4,096 abstract
two-family Hall classifications.  The result is recorded in
`root_retention_qs_compensation_hall_audit.json`.
The finite audit checks the algebra and set accounting; it does not replace
the supplier-compatibility premise.

## Claim boundary

Proved: complete reassembly, exact compensation prices, the bounds (9), and
the exhaustive compatible-pair/Hall alternative for unrestricted packet
sizes.

Not proved: nonemptiness or compatibility of the filtered packet families,
that every failed reassembly response is already saturated at the identical
record, elimination of the Hall cut from the full GG premises, the universal
four-edge theorem, or general EFX.

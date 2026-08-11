# Released-owner compensation-chain lemma

**Date:** 2026-08-10

**Status:** cap-free adaptive strengthening; only the full released-reservoir
R-wall and response-Hall boundaries remain

## Expanded compensation reservoir

Use a strict external core-capture response

\[
Y_a=K+f,
\qquad
O=X_q\setminus K,
\qquad
\Delta_a=v_q(K)-v_q(X_a)>0.
\]

Because owner `a` receives `K+f`, her entire old bundle `X_a` is released.
The earlier compensation chain used only `O`.  Allow it now to partition
both disjoint released packets:

\[
H\subseteq O,
\qquad
G\subseteq X_a. \tag{1}

\]

For `P subseteq T_r`, form

\[
Y_a=K+f,
\]

\[
Y_q=(O\setminus H)+(X_a\setminus G)+P,
\]

\[
Y_r=(X_r\setminus P)+H+G, \tag{2}
\]

fixing the fourth owner.  This is a complete allocation.  It improves `q`
and preserves `r` exactly when

\[
v_q(P)>\Delta_a+v_q(H)+v_q(G), \tag{Q}
\]

\[
v_r(H)+v_r(G)\ge v_r(P). \tag{R}

\]

Owner `a` strictly improves by the selected desired response.

## Finite alternating repair

Run the alternating payment-compensation algorithm with payment reservoir
`T_r` and compensation reservoir

\[
S=O\mathbin{\dot\cup}X_a.
\]

Start from a minimal `P` satisfying (Q) with `H=G=emptyset`.  When (R)
fails, add an inclusion-minimal packet from the unused part of `S`; its
intersection with `O` is added to `H` and its intersection with `X_a` to
`G`.  When (Q) fails, add an inclusion-minimal packet from `T_r-P`.

Both selected sets grow monotonically, so every repair branch terminates
after finitely many additions.  A successful leaf gives (2).  If an
R-repair is impossible, the exact terminal wall is

\[
v_r(O+X_a)<v_r(P)\le v_r(T_r). \tag{R+}

\]

This strictly dominates the earlier wall `v_r(O)<v_r(P)`.

## Q-exhaustion still changes the root

Suppose instead that a Q-repair is impossible.  Put

\[
E_q=O\setminus H,
\qquad
E_a=X_a\setminus G.
\]

Then

\[
v_q(T_r)\le
v_q(K)-v_q(X_a)+v_q(H)+v_q(G). \tag{3}

\]

Combining (3) with `v_q(T_r+f)>v_q(X_q)=v_q(K+O)` gives

\[
v_q(f)>v_q(E_q)+v_q(E_a). \tag{4}

\]

In particular `v_q(f)>v_q(E_q)`.  Therefore root `q` can replace `E_q`
by `f` and transfer `E_q` along a charity-rooted component, exactly as in
the Q-exhaustion root-switch lemma.  The extra unused external packet
`E_a` only strengthens the strict root margin; it need not be moved in the
root-switch allocation.

Thus expanding the compensation reservoir introduces no new Q-terminal
case.  Every leaf is either:

1. a successful three-owner component (2);
2. a q-rooted transfer-tree component forced by (4); or
3. the single sharp R-wall (R+).

## Release compatibility

For the successful component (2), use targets `a,q,r` with incoming and
release sets

| target | incoming | release |
|---|---|---|
| `a` | `K+f` | `X_a` |
| `q` | `(X_a\G)+P` | `K+H` |
| `r` | `H+G` | `P` |

The incoming sets are pairwise disjoint.  They are all supplied: `f` is
initially unallocated, `K,H` are released at `q`, the two cells of `X_a`
are released at `a`, and `P` is released at `r`.  Hence every internal
response SDR is a release-compatible PI edge set.  Without one, an external
source or minimal Hall-deficient target set is explicit.

The scalar exhaustion implications and set support replay in
[`released_owner_compensation_chain_audit.json`](released_owner_compensation_chain_audit.json).

## Claim boundary

This lemma absorbs the responding owner's entire released bundle into the
adaptive selector and converts every Q-exhausted leaf to a root switch.  It
does not eliminate the stronger R-wall (R+), eliminate the response-Hall
boundaries of its successful/root-switch components, close the `GG` flower,
or prove four-agent additive EFX.

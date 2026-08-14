# Base-support closure paid-component lemma

**Date:** 2026-08-13

**Status:** cap-free elimination of captured-donor payment by exact support
reassembly; response rank, observer safety, and four-edge extraction remain

## Signed base-support graph

Let `(X,P_X)` be the base EFX allocation and let `(Y,{p})` be the physical
rank-three state.  Draw a directed provenance edge

\[
 a\longrightarrow b
 \quad\Longleftrightarrow\quad
 X_a\cap Y_b\ne\varnothing ,\qquad a\ne b.       \tag{1}
\]

For a seed owner `d`, let `S` be the least owner set containing `d` and
closed under (1): whenever `a in S` and `a -> b`, also `b in S`.  Equivalently,
`S` is the set reachable from `d` in the base-support graph.  Consequently

\[
 X_a\cap Y_b=\varnothing
 \quad(a\in S,\ b\notin S).                       \tag{2}
\]

Thus every displaced base good owned in `S` is currently held either inside
`S` or in current charity.  A base good in current charity is returned
directly to its base owner in the operation below.

## Complete support reassembly

Return every `S`-owned base good to its base owner, retain every good whose
base owner is outside `S` or is base charity, and leave every outside owner
unchanged.  If the current charity good `p` is not `S`-owned, give it to an
arbitrary `t in S`; if it is `S`-owned, return it to its base owner.  Put
`B=P_X` and

\[
 E_i=Y_i\cap\left(B\mathbin{\dot\cup}
                  \mathop{\dot\bigcup}_{a\notin S}X_a\right).
                                                               \tag{3}
\]

Then

\[
 Z_i=X_i\mathbin{\dot\cup}E_i
      \mathbin{\dot\cup}(\{p\}\text{ if }p\notin
                 \mathop{\dot\bigcup}_{a\in S}X_a\text{ and }i=t)
      \qquad(i\in S),                             \tag{4}
\]

and `Z_i=Y_i` for `i notin S`.  Equation (2) proves conservation: no outside
owner currently holds a good removed by (4), and each internal current
holder releases exactly the `S`-owned goods that their base owners recover.

Every closure owner is weakly base-paid because

\[
 v_i(Z_i)-v_i(X_i)
 =v_i(E_i)+\mathbf 1_{\{p\text{ external to }S,\ i=t\}}v_i(p)\ge0,
                                                               \tag{5}
\]

where the token term is present only when `p` is external to `S`.  An owner
with nonempty `E_i`, or the recipient of an external `p`, is strict by
positivity. Outside owners retain their current bundles. Hence, whenever
every outside owner was already weakly paid, (4) is an all-owner-paid
complete candidate. Strictness is characterized exactly by (5); it is not
silently inferred when `p` is itself restored base support.

The moved packets that reassemble base support are precisely the reversals
`b -> a` of the provenance edges `a -> b` induced on `S`, together with any
charity-to-base-owner return and the final charity edge. Their underlying
owner graph is connected whenever `|S|>1` and every newly reached owner is
an owner holder:
every owner of `S` has a directed provenance path from `d`, whose reversal
is an undirected path back to `d` in the reassembly graph.

## Captured-margin consequence

Suppose represented donor `i` holds captured base-`d` support

\[
 C_i=Y_i\cap X_d\ne\varnothing,
 \qquad v_i(C_i)>v_i(Y_i)-v_i(X_i).               \tag{6}
\]

Then `d -> i` is an edge of (1), so `i in S`.  Returning only `C_i` would
underpay `i`, but the closure reassembly returns all displaced `i`-support
simultaneously and pays `i` by (5).  Therefore captured donor margin is not
a valuation-level payment obstruction.  It forces expansion to the least
closed signed-support component.

If (4) is EFX, it contradicts global lexicographic maximality.  Otherwise
the paid-splice response theorem supplies a decorated observer response on
this exact connected component or from an outside observer into it.  At a
saturated state that response must enlarge/augment, make strict same-record
progress, expose PI, or repeat with the identical physical record.

## Remaining implication

The closure can contain more than four provenance edges.  Moreover, physical
coverage of `S` does not itself prove that the repeated decorated-response
matching has rank `|S|`.  The next theorem must show that a saturated repeat
of (4) either:

1. has the full response-rank premise of represented-component charity
   extraction;
2. admits a rank-augmenting or release-compatible shortcut; or
3. compresses the connected reassembly to a complete EFX allocation using
   at most four packet-transfer edges.

This is strictly sharper than the former donor-compensation gate: payment is
closed cap-free, and only response rank/observer compression remains.

## Verification and boundary

[`audit_base_support_closure_paid_component.py`](../tracks/parkability/audit_base_support_closure_paid_component.py)
exhausts all 4,096 directed owner provenance graphs and all four seeds
(16,384 records). It independently verifies closure, conservation locality,
connected reversal support, and the exact payment identities; QF-LRA checks
(5) and conditional strict external-charity payment.

This lemma does not bound the reassembly itself by four edges, prove observer
EFX, force response rank `|S|`, close the rank-three repeat, or prove the
original four-edge theorem.

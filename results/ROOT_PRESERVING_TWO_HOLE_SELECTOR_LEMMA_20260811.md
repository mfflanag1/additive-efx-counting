# Root-preserving two-hole selector lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of the root-facing priority exception; the
resulting root-critical polarity and 2-by-2 Hall boundary remain open

## Setting

Let `r` be the first owner in the fixed priority.  At a root-facing
J-exhaustion, the two bundles being released are a common-safe desired root
core `A` and the current residual `W`.  The exhaustion inequality gives

\[
 v_r(A)>v_r(W),                                      \tag{1}
\]

and `r` strictly prefers `A` to her base bundle.  Let `d` be the other hole.
The complete released pool is `P=A dot union W`.

## Root-preserving selector

Among all oriented partitions

\[
 P=H\mathbin{\dot\cup}L,
 \qquad v_r(H)\ge v_r(A),                            \tag{2}
\]

choose one maximizing `v_d(L)`.  The feasible family is nonempty because
`H=A,L=W` is feasible.  Give `H` to `r` and `L` to `d`.

Owner `r` is envy-free.  Indeed, additivity, (1), and (2) give

\[
 v_r(L)=v_r(A)+v_r(W)-v_r(H)
       \le v_r(W)<v_r(A)\le v_r(H).                  \tag{3}
\]

Consequently `r` remains strictly above base and cannot create a wall
against `d`.

## Exact dichotomy

Either the selected two-way allocation is EFX for both holes, or it has the
following exact certificate.  Let `g` be a least-`d` good of `H`.  Then

\[
 v_d(L)<v_d(H-g)                                     \tag{4}
\]

and

\[
 v_r(H-g)<v_r(A).                                    \tag{5}
\]

Equation (4) is precisely the only possible two-hole EFX failure, because
`r` is envy-free.  If (5) failed, moving `g` from `H` to `L` would preserve
the root constraint (2) and strictly increase `v_d(L)`, contradicting the
choice of the partition.  Thus (5) is forced.

The support identity also converts (5) into the named strict polarity

\[
 v_r(g)>v_r(H)-v_r(A)=v_r(W)-v_r(L).                 \tag{6}
\]

Thus a failed root-preserving selector does not return to an unnamed
root-facing star: it identifies the least-`d` good `g` as more valuable to
the root than the exact root-value deficit of the complementary residual.
No item cardinality is used.

## Flower composition

Keep the other two common-safe desired cores fixed.  If (4) does not hold,
the two holes are mutually EFX, the represented sources remain safe against
both fixed cores, and all remaining walls lie in the same two-core/two-hole
response boundary as in the unconstrained cut-and-choose lemma.  The
endpoint is priority-valid because `r` retains at least `v_r(A)>v_r(X_r)`.

If (4) holds, equations (4)--(6) replace the formerly priority-invalid
root-facing branch by a strict, item-named cross-row polarity.  The next
operation must either use `g` in a root-preserving transfer component or
show that its return contradicts the minimal-payment/root choice.

## Claim boundary

This lemma eliminates root-facing J-exhaustion as a priority exception and
is valid for arbitrary positive additive packets.  It does not prove that
the root-critical polarity (6) contradicts flower minimality, close a
deficient 2-by-2 response block, terminate hole-pivot recurrence, close the
`GG` flower class, or prove four-agent/general additive EFX.

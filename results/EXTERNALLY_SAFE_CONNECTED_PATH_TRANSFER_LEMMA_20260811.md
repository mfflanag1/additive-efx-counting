# Externally-safe connected path-transfer lemma

**Date:** 2026-08-11

**Status:** cap-free global endpoint lemma; selection of its path packets
from every terminal flower polarity remains open

## Path transfer

Let `(X,P)` be an EFX-with-charity allocation and fix distinct owners

\[
 a_0,a_1,\ldots,a_k.
\]

For each `t<k`, choose a nonempty packet `K_t subseteq X_{a_t}`.  Transfer
the packets along the directed path

\[
 a_0\xrightarrow{K_0}a_1\xrightarrow{K_1}\cdots
 \xrightarrow{K_{k-1}}a_k,                           \tag{1}
\]

so that

\[
Y_{a_0}=X_{a_0}\setminus K_0,
\]

\[
Y_{a_t}=(X_{a_t}\setminus K_t)+K_{t-1}quad(0<t<k),
\]

\[
Y_{a_k}=X_{a_k}+K_{k-1}.                             \tag{2}
\]

Every other owner and the charity bundle remain fixed.

Call a changed target `Y_j` **externally common-safe** when

\[
 \tau_i(Y_j)\le v_i(X_i)\qquad(i\ne j).              \tag{3}
\]

Unlike ordinary common safety, (3) deliberately omits the target's own row;
an owner is automatically EFX-safe against her own bundle.

## Endpoint theorem

Suppose:

1. every changed target is externally common-safe;
2. every changed owner other than the path source `a_0` is weakly nonworse,
   \(v_i(Y_i)\ge v_i(X_i)\);
3. the path source directly satisfies every final comparison,
   \[
   v_{a_0}(Y_{a_0})\ge\tau_{a_0}(Y_j)quad(j\in N),
   \qquad
   v_{a_0}(Y_{a_0})\ge v_{a_0}(P);                  \tag{4}
   \]
4. in the fixed priority, the first owner whose utility changes strictly
   improves.

Then `(Y,P)` is EFX with charity and lexicographically dominates `(X,P)`.
Its transfer multigraph has one nontrivial connected component, namely the
path (1).

## Proof

The source `a_0` satisfies all comparisons by (4).  Consider any other
observer `i`.  If `i` is changed, premise 2 gives
`v_i(Y_i)>=v_i(X_i)`; if she is unchanged, equality holds.  Against any
other changed target `Y_j`, external safety (3) therefore gives

\[
 v_i(Y_i)\ge v_i(X_i)\ge\tau_i(Y_j).
\]

Against her own target, EFX is automatic.  Every unchanged target and the
charity bundle are exactly as in `X`, so their inequalities follow from
base EFX and the same weak-payment comparison.  Thus `(Y,P)` is EFX with
charity.  Premise 4 is precisely strict lexicographic dominance.  Finally,
the nonempty packet edges in (1) form a connected path.  No item count is
used.  \(\square\)

## Flower interpretation

This lemma captures both exact global repairs of the hardened weighted-Hall
adversaries:

1. a one-edge path `c -> r`, where `c` is the only losing owner and `r`
   improves earlier in priority; and
2. a two-edge path `q -> r -> c`, where `q` is the only losing owner while
   `r` and `c` are paid.

In both profiles every changed target is externally common-safe, even though
the recipient's own tail can exceed her base value.  Requiring ordinary
common safety would therefore be unnecessarily strong and would miss the
observed cap-free topology.

At a globally lexicographically maximal flower state, any packets satisfying
premises 1--4 give an immediate contradiction.  The remaining conversion
problem is to select such packets from a terminal hitting-set or
source-inactive polarity, or else expose a generalized PI component.

## Claim boundary

The lemma proves the connected EFX endpoint once its packets and safety
conditions are supplied.  It does not prove that every terminal polarity
supplies them, establish generalized PI-freeness of the hardened profiles,
close `GG`, or prove four-agent/general additive EFX.

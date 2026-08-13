# Paid-response path-core rotation lemma

**Date:** 2026-08-13

**Status:** conditional path/core combinatorics only. Under the all-old-core
premises stated below, the four-old-core shortcut already contradicts global
maximality; a corrected mixed-edge import is required before this rotation
can be used in GG

## State

Write the old Hamiltonian response path as

\[
 h_0=t\longrightarrow h_1\longrightarrow h_2
 \longrightarrow h_3\longrightarrow c.
\]

Its path core `A_i` belongs to source `h_i`.  For `i=1,2,3`, the
old target of `h_i` is

\[
 Y_i=A_{i-1}\mathbin{\dot\cup}R_i.
\]

At the paid deletion-return state let

\[
 Z_0=P,
 \qquad Z_i=A_i\mathbin{\dot\cup}R_i\quad(i=1,2,3),
\]

with `A_0` and any unused goods in charity.  Assume both `Y_i` and `Z_i`
meet owner `h_i`'s protected floor against `P`.  This is exactly the
payment supplied by the old paid state and the deletion-return lemma.

Let the repeated response source be `h_k` and the failed target be `h_l`,
where `k,l in {1,2,3}` and `k != l`.  Assume the response is
**core-supported**:

\[
 v_{h_k}(A_l)>v_{h_k}(Z_k).                       \tag{1}
\]

It is enough that a desired response `E` satisfy `E subseteq A_l`, since
positivity then implies (1).

## Forward target: an internally supplied cycle

Suppose `k<l`.  Rotate the path cores on the segment `[k,l]`:

\[
 W_k=A_l+R_k,
 \qquad W_i=A_{i-1}+R_i=Y_i\quad(k<i\le l),       \tag{2}
\]

and keep every other owner unchanged.  The source `h_k` strictly improves
by (1), and every other changed owner receives a protected old target.

The physical cores in (2) give the directed cycle

\[
 h_k\to h_{k+1}\to\cdots\to h_l\to h_k.          \tag{3}
\]

Every packet in (3) is released by the next edge of the same rotation.
Thus this branch is an internally supplied response component; it is not a
new recurrence.

## Backward target: two path segments

Suppose `l<k`.  Restore the prefix and suffix and send the captured core to
the response source:

\[
 \begin{aligned}
 W_i&=A_{i-1}+R_i=Y_i &&(1\le i\le l),\\
 W_k&=A_l+R_k,\\
 W_i&=A_{i-1}+R_i=Y_i &&(k<i\le3).
 \end{aligned}                                    \tag{4}
\]

Owners strictly between `l` and `k` keep `Z_i`.  Core `A_3` is placed in
charity.  The bundles are pairwise disjoint.  Again (1) pays the source,
restored owners retain their protected floors, and unchanged owners retain
the deletion-return payment.

The old response sources exposed by (4) are

\[
 \{h_0,\ldots,h_{l-1}\}\cup\{h_l\}
 \cup\{h_k,\ldots,h_3\}.                          \tag{5}
\]

Consequently the matching rank is

\[
 4-(k-l-1).                                       \tag{6}
\]

For four owners, (6) is four except when `(l,k)=(1,3)`.  Thus the adjacent
backward orders `(1,2)` and `(2,3)` produce a paid rank-four response
matching immediately.

## Unique survivor

Only

\[
 (l,k)=(1,3)                                      \tag{7}
\]

leaves rank three.  The middle core `A_2` is still assigned to its own
source.  Every other core already has the required path location:

\[
 A_0\to h_1,qquad A_1\to h_3,qquad A_3\to c.
\]

The smallest missing operation is therefore not an arbitrary rank
completion.  It is the following two-packet exchange.  Choose a
base-common-safe desired subcore `H subseteq A_2` for `h_2` and a packet
`K subseteq P`, and put

\[
 W_0=(P\setminus K)+H,
 \qquad
 W_2=R_2+(A_2\setminus H)+K.                     \tag{8}
\]

If both affected owners retain their protected floors, `H` supplies the
missing edge `h_2 -> h_0`, and the matching becomes the Hamiltonian path

\[
 h_2\to h_0\to h_1\to h_3\to c.                 \tag{9}
\]

If no pair `(H,K)` satisfies these two floors, the exact separator is:

> for every desired deletion `H` of `A_2` and every `K subseteq P` that
> pays the displaced middle owner in (8), the hole owner is underpaid.

This is a cap-free two-row hole/core-exchange obstruction.  It is strictly
smaller than the former rank-completion terminal and is the only remaining
core-supported order.

## Adversarial replay and boundary

The exact audit enumerates all six ordered pairs `(k,l)`, verifies the
physical core locations and ranks, and checks the payment implications in
linear rational arithmetic.  Both frozen positive-rational deletion-return
witnesses have `(l,k)=(1,2)` and their rotation (4) is EFX, so neither is a
countermodel to the core-supported bridge.

Calling (3) a PI component requires every rotated core to be
base-common-safe. If that holds for all four cores, the shortcut theorem
already closes before rotation. This lemma also does not handle a residual-essential response satisfying
`v_{h_k}(A_l)<=v_{h_k}(Z_k)`, prove feasibility of (8) in the unique
endpoint order, import the extra GG root/q inequalities needed to refute
its separator, close GG, or prove four-agent/general additive EFX.

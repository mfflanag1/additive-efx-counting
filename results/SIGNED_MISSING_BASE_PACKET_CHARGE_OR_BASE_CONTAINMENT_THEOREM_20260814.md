# Signed missing-base packet charge or base-containment theorem

**Date:** 2026-08-14

**Status:** cap-free reduction of every root-held retired packet to a
base-contained packet or an exact blocker of the signed missing-base return

## Signed root support

Let the current first-priority root bundle be `Y_r`, with base bundle `X_r`,
and put

\[
 S^+=Y_r\setminus X_r,
 \qquad S^-=X_r\setminus Y_r.                   \tag{1}
\]

The root is strict, so additivity gives

\[
 v_r(S^+)-v_r(S^-)=\delta>0.                   \tag{2}
\]

Let `K subseteq Y_r` be the named root-held retired packet.  The signed
missing-base packet `S^-` is disjoint from `Y_r`, hence from `K`.

## Admitted missing-base return

First suppose `S^-` is an admitted compatible exterior mode for every
subpacket used below.  Put

\[
 T=K\cap S^+.                                   \tag{3}
\]

Three support cases are exhaustive.

### 1. Proper incoming intersection

If `T` is nonempty and `T subsetneq S^+`, release `T` and give `S^-` to the
root.  The clean-release margin is

\[
 \delta-v_r(T)+v_r(S^-)
   =v_r(S^+)-v_r(T)>0.                           \tag{4}
\]

Thus the root is strict.  The clean subpacket-release theorem gives an EFX
contradiction, controlled anchor change, or strict reduction of the named
packet/hitting coordinate.

### 2. Complete incoming intersection

If `T=S^+`, then `S^+ subseteq K`.  Releasing `S^+` and returning `S^-`
is the unique root-equality base restoration.  The root-equality packet-
spread theorem eliminates this case by leaving one incoming good at the root
or adding an off-packet donation in the singleton case.

### 3. Empty incoming intersection

The only survivor is `T=empty`.  Since

\[
 Y_r=(Y_r\cap X_r)\mathbin{\dot\cup}S^+,
\]

equation (3) then forces

\[
 K\subseteq Y_r\cap X_r\subseteq X_r.          \tag{5}
\]

Hence an admitted signed missing-base return eliminates every packet that
crosses from the base exterior into the current root.  The packet must be
entirely base-contained.

## Failed missing-base admission is an exact charge

If `S^-` is not an admitted mode, retain its first exact failure from the
canonical transition audit.  It cannot be dismissed as generic scalar
underpayment: (2) shows that `S^-` is the unique signed packet balancing all
current root incoming support.  Its failure must name the moved good/current
holder and one of:

1. another retired packet whose canonical normalization leaves the root
   return incomplete;
2. a protected physical anchor/core whose movement requires an explicit
   label exchange; or
3. an exact supplier/release or typed-floor premise of the originating
   operation that the signed return fails.

Thus the named packet `K` **charges** the obstruction to a different retired
support/anchor/release coordinate carried by `S^-`.  If that coordinate is
new, the actual adopted response/anchor transition is finite progress.  At
an exact repeat it is the global multi-label recurrence that remains to be
shown well-founded or PI; the charge itself is not counted as progress.

## Consequence

Every recurrent root-held packet lies in one of two sharply separated
classes:

\[
 \boxed{K\subseteq X_r}
 \qquad\text{or}\qquad
 \boxed{S^-\text{ has a named retired/anchor/release blocker}.} \tag{6}
\]

The first is the **base-contained retired-anchor face**.  The second is a
directed charge edge from `K` to another physical ledger/anchor coordinate.
There is no remaining root packet that merely straddles the base boundary
while the signed missing-base return is available.

## Claim boundary

This theorem proves the exhaustive support fork, strict margin (4), and the
exact form of a failed signed return.  It does not eliminate a base-contained
packet, prove that multi-label charge edges are acyclic, turn a charge cycle
into PI, close normalization bypass, `T_{L,times}^*`, GG, four-agent EFX, or
general additive EFX.

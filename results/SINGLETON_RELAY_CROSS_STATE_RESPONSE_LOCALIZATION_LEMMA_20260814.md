# Singleton-relay cross-state response-localization lemma

**Date:** 2026-08-14

**Status:** cap-free exact reduction of the disjoint normalization-bypass
branch; a shared safe response or a two-row singleton-critical separator
remains

## Two relay states

Let `B=(B_i)_{i in N}` be any allocation of every good except a positive
singleton `p`, and fix distinct owners `r,d`.  Compare the two complete
allocations

\[
 R_r=B_r+p,\quad R_d=B_d,
 \qquad
 D_r=B_r,\quad D_d=B_d+p,                         \tag{1}
\]

with every other bundle unchanged.  This is exactly the last two probes in
the rank-three matching charity relay.  No packet-size, base-payment, or
response-graph hypothesis is used below.

For a state `Z`, call a nonempty packet `E` a response for source `i` when

\[
 v_i(E)>v_i(Z_i),\qquad
 \tau_h(E)\le v_h(Z_h)\quad(h\in N).             \tag{2}
\]

## Desired-response localization

Let `E` be contained in one of the displayed owner targets and suppose
`p notin E`.  Then `E` is contained in the corresponding `B` target.

If `E` is desired by source `i` at `D`, then it is also desired at `R`
unless `i=r`.  In the exceptional case, if it is not desired at `R`, then

\[
 v_r(B_r)<v_r(E)\le v_r(B_r)+v_r(p).             \tag{3}
\]

Symmetrically, a packet desired at `R` is also desired at `D` unless its
source is `d`; an `R`-only desired packet satisfies

\[
 v_d(B_d)<v_d(E)\le v_d(B_d)+v_d(p).             \tag{4}
\]

Thus a disjoint failed response cannot silently acquire an arbitrary new
source when the singleton moves.  The only possible endpoint-specific
sources are the owner losing `p`: `r` on the `D` side and `d` on the `R`
side.

## Safety localization

Suppose `E` is a response at `D`, is disjoint from `p`, and remains desired
at `R`.  Its safety inequalities remain valid at `R` for every observer
except possibly `d`, whose own floor falls by exactly `v_d(p)`.  Hence either
`E` is a response at both states or

\[
 v_d(B_d)<\tau_d(E)\le v_d(B_d)+v_d(p).          \tag{5}
\]

Likewise, an `R` response which remains desired at `D` is a response at both
states unless

\[
 v_r(B_r)<\tau_r(E)\le v_r(B_r)+v_r(p).          \tag{6}
\]

Equations (3)--(6) exhaust the ways in which a response disjoint from `p`
can fail to be a common response coordinate of the two relay states.

## Consequence for simultaneous non-EFX relay probes

Choose globally minimum responses at both non-EFX probes.  If either chosen
response contains `p`, the existing whole-hit collision interface applies.
Otherwise at least one of the following holds:

1. one chosen packet is a safe desired response at both `R` and `D`;
2. the `D` response is root-specific and satisfies (3);
3. the `R` response is `d`-specific and satisfies (4);
4. cross-state safety fails only in the opposite singleton row and satisfies
   (5) or (6).

In particular, after excluding a shared safe response, every disjoint
normalization bypass is charged to an exact singleton-width interval in one
of only the two rows `r,d`.  No third owner, target, or unbounded packet tail
can create another scalar branch.

The interval separator is feasible in isolation (for example, base bundle
value `1`, singleton value `1/2`, and response/threshold value `5/4`).  Its
elimination therefore must use the saturated rank-three response/support
premises, not positivity or the relay algebra alone.

## Claim boundary

This lemma proves response-source and observer-safety localization for the
two complete relay probes without an item cap.  It does not show that a
shared response creates PI/progress, eliminate the singleton-critical
intervals, close the nonroot normalization bypass, prove the fixed-`U`
four-edge theorem, or prove four-agent/general additive EFX.

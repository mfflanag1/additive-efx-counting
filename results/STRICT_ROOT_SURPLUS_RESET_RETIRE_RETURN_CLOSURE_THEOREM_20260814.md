# Strict-root surplus reset-retire-return closure theorem

**Date:** 2026-08-14

**Status:** candidate cap-free reduction of the strict-root proper-surplus
interface; the imported complete collision closure has an unproved nonroot
normalization-bypass branch

## Input

Fix a finite positive-additive four-owner instance and a globally
fixed-priority lexicographically maximal EFX base allocation `X` (possibly
with charity).  Let `r` be the first-priority owner and write

\[
                         x=v_r(X_r).
\]

Suppose a reachable signed support state has the physical form

\[
                 Y=(A+H,Q,W,E;P)                 \tag{1}
\]

in owner order `(r,q,d,s; charity)`, where:

1. `A,H,Q,W,E,P` are pairwise disjoint physical packets with `H` nonempty;
2. `A` is the permanent physical root-anchor support and
   `v_r(A)>x`;
3. the current suppliers and destinations of all goods are recorded; and
4. the strict first-priority floor-reset operation and the complete
   `T_{L,times}^*` collision theorem at commit
   `34709c9ce22dbde23a5fa381a2ccea7898dfe1ca` are admitted in the frozen
   augmented-state transition language.

The charity packet `P` may be empty.  No bound is imposed on any packet's
cardinality, and no old floor or donor-margin inequality is assumed for
`q,d,s`.

## Two probes

Form the complete allocations

\[
\begin{aligned}
C_d&=(A,Q,W+H+P,E),\\
C_r&=(A+H,Q,W+P,E).
\end{aligned}                                    \tag{2}
\]

Relative to (1), their nonempty supplier-to-recipient edge sets are

\[
\begin{array}{c|c}
C_d&r\to d:H,\quad charity\to d:P,\\
C_r&charity\to d:P,
\end{array}                                      \tag{3}
\]

with the charity edge omitted when `P` is empty.  Hence either endpoint has
at most two transfer edges.  Relative to `C_d`, the second probe changes
only

\[
                         H:d\longrightarrow r.    \tag{4}
\]

Cancelling (4) restores `C_d` exactly.

## Reset, retirement, and capture

Both probes keep the same physical anchor support `A`, and

\[
 v_r((C_d)_r)=v_r(A)>x,
 \qquad
 v_r((C_r)_r)=v_r(A)+v_r(H)>x.                   \tag{5}
\]

Apply the controlled floor reset at `C_d`:

\[
                     F_i=v_i((C_d)_i).            \tag{6}
\]

Every owner pays (6) with equality while the immutable first-priority
certificate (5), the anchor `A`, and every signed supplier label are kept.
If `C_d` is EFX, (5) contradicts maximality of `X` and gives the desired
endpoint.

Otherwise globally minimal response extraction at the actual allocation
`C_d` supplies an adopted current-safe/current-desired signed response
coordinate.  Record the physical move `r->d:H` as a retirement under the
unchanged anchor `A`; its new holder `d` pays the retirement-time floor (6).

The fixed second probe `C_r` consumes the whole retired packet.  Owners
`q,s` keep their reset bundles, the protected root strictly improves, and
`d` has the unique reset-floor deficit.  It is captured exactly by `H`:

\[
 F_d-v_d((C_r)_d)
 =v_d(W+H+P)-v_d(W+P)
 =v_d(H)>0.                                      \tag{7}
\]

Thus `C_r` is a typed strict-root, one-sacrificed-owner candidate rather
than an unclassified unpaid allocation.  If it is EFX, (5) again
contradicts maximality.  If it is not EFX, canonical cancellation of its
only post-retirement transfer (4) gives the already failed allocation
`C_d` and its adopted response coordinate.  At an exact saturated repeat,
the named packet, retirement supplier and holder, same anchor, exact
protected-floor capture (7), failed normalized test, and repeated response
are precisely the normalization-bypass/protected-floor input of
`T_{L,times}^*`.

The imported collision theorem was claimed to exclude that terminal.
`NONROOT_NORMALIZATION_BYPASS_COLLISION_GAP_20260814.md` shows that its cited
dependencies do not cover a nonroot holder whose repeated normalized
response avoids `H`.  Consequently simultaneous failure of `C_d,C_r`
reduces to that exact branch rather than currently yielding a contradiction.

## Consequence for the fixed-`U` program

This theorem removes all provenance, proper-residual, donor-payment, and
observer-surplus hypotheses from the earlier R2 `H`-return lemma.  Every
saturated root-facing state that exposes a nonempty detachable root packet
`H` outside a still-strict permanent anchor `A` is conditionally closed.

The remaining global task is no longer the algebra of the two probes.  It is
the coverage statement that every target fixed-`U` state either has this
strict-root proper-surplus interface or reaches an already closed
EFX/PI/progress/rank-growth branch.  In particular, the present theorem does
not cover a state whose entire current root support is the minimal anchor
`A`, nor a state in which deleting every nonempty root subpacket destroys
the strict first-priority certificate.

## Verification and claim boundary

`audit_strict_root_surplus_reset_retire_return.py` independently checks
physical conservation, all support-edge identities, the two strict-root
inequalities, exact reset payment, the one-hole identity (7), and canonical
cancellation.  It deliberately labels the result conditional because an
arithmetic replay cannot certify admission of a new transition into the
frozen global proof graph.

Proved: the cap-free two-edge construction and reduction to the declared
nonroot normalization bypass.  Not proved: closure of that bypass,
independent semantic validity of the new controlled reset, the full
saturated rank-three fixed-`U` theorem, four-agent additive EFX, or general
additive EFX.

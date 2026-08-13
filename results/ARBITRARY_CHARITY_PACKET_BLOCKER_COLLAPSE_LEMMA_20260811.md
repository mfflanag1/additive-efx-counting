# Arbitrary-charity-packet blocker collapse lemma

**Date:** 2026-08-11

**Status:** cap-free reduction of every unsafe multi-good charity packet to
the singleton exchange walk; owner-target mixed-margin payment remains open

**Superseded status (2026-08-12):** the owner-target mixed-margin payment
gate was subsequently closed by the deletion-return residual-completion
lemma, and the composed exact saturated terminal is excluded by
[`UNIVERSAL_FULL_OWNER_CHARITY_EXCHANGE_EXTRACTION_THEOREM_20260812.md`](UNIVERSAL_FULL_OWNER_CHARITY_EXCHANGE_EXTRACTION_THEOREM_20260812.md).

## Unsafe charity packet

Let `(Y,P)` be a noncomplete paid splice candidate, where `P` is any
nonempty set of unallocated goods and

\[
 v_i(Y_i)\ge v_i(X_i)\qquad(i\in N).              \tag{1}
\]

Suppose charity is unsafe to owner `i`:

\[
 v_i(P)>v_i(Y_i).                                 \tag{2}
\]

Every paid owner bundle is nonempty under positive valuations and a positive
base.  Choose any good `h in Y_i` and set

\[
 Y_i'=(Y_i\setminus\{h\})\cup P,
 \qquad P'=\{h\}.                                 \tag{3}
\]

All other owner bundles remain unchanged.

## Strict improvement and connectedness

Additivity and (2) give

\[
 \begin{aligned}
 v_i(Y_i')-v_i(Y_i)
 &=v_i(P)-v_i(h)\\
 &>v_i(Y_i)-v_i(h)\ge0.                           \tag{4}
 \end{aligned}
\]

Thus exactly one owner strictly improves and no owner loses.  The packet
moves `charity -> i:P` and `i -> charity:{h}` form one connected exchange,
regardless of `|P|`.  The final charity is a singleton.

Apply the singleton-charity exchange walk from this state.  It terminates in
an EFX/lex improvement, an owner-target ordinary or full-decorated response
augmentation, or further strict same-owner current progress.  Consequently
an arbitrary packet deleted from a decorated target may always be parked in
charity: if the resulting charity is safe, its budget is satisfied; if it is
unsafe, (3) collapses it to the already-closed singleton branch.

## Consequence for mixed-margin payment

When a decorated target is trimmed to repair an observer debt, disposition
of the deleted packet is not an additional separator.  The sole remaining
question is whether the trimmed source and the other owner targets can meet
their direct EFX floors.  No `P' subseteq P`, singleton-input, packet-size,
or value cap is required.

## Verification and boundary

[`arbitrary_charity_packet_blocker_collapse_audit.json`](arbitrary_charity_packet_blocker_collapse_audit.json)
checks the strict utility identity, preservation of every other owner,
singleton output, conservation, and the reduction to the verified singleton
walk symbolically.

This lemma does not choose an observer-debt-removing trim, pay the trimmed
source, resolve the mixed old/new margin separator, close the repeated-
support theorem, close GG, or prove four-agent/general additive EFX.

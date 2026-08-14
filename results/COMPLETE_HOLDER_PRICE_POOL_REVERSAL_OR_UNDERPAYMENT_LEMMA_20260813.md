# Complete holder-price pool reversal-or-underpayment lemma

**Date:** 2026-08-13

**Status:** cap-free reduction of the holder-price gate to safe payment,
genuine response progress, or exact aggregate underpayment

## Complete releasable pool

At an exact retired-packet transfer candidate, let holder `h` have release
price

\[
p_h>0.
\]

Let `R_h` be the union of the **complete physically releasable compensation
pool** after supplier closure, excluding the packet being transferred and
every good required by a retained protected core.  Every selected subpacket
retains its full supplier labels.  The admissible compensation family is
downward closed: deleting goods from a proposed return leaves them with their
current holders or charity and cannot introduce a new supplier.  This lemma
does not assume that `R_h` is safe or that its goods have one supplier.

## Exact dichotomy

### 1. Aggregate underpayment

If

\[
v_h(R_h)<p_h,                                     \tag{1}
\]

then no subpacket of the complete pool pays the holder, by positivity and
additivity.  Equation (1) is the exact aggregate holder-price separator.

### 2. Minimal price crossing

Otherwise choose an inclusion-minimal packet `Q subseteq R_h` such that

\[
v_h(Q)\ge p_h.                                    \tag{2}
\]

If `Q` is current-safe at the exact post-transfer floor vector, assign it to
`h`, close its supplier component, and perform the full EFX audit.  The
holder floor is paid by construction.

If `Q` is unsafe, some `g in Q` has a desired subset inside `Q-g`.  Choose a
globally minimum desired subset `A subseteq Q-g`.  It is current-safe and
minimality of `Q` gives

\[
v_h(A)le v_h(Q-g)<p_h.                            \tag{3}
\]

Thus an unsafe price-crossing packet does not disappear as a failed payment:
it produces an actual current-safe desired response with exact supplier
provenance.  A new source/target reduces response deficiency, a supplied
cycle is PI, a retired hit returns to the named collision audit, and an exact
repeat is processed by the target-envelope/external-star ascent chain.

## Consequence

After the response/progress routes in branch 2 are exhausted, the sole
scalar holder-price survivor is (1): even the complete compatible pool is
worth less than the holder's price.  This is stronger than failure of a
fixed packet menu or one residual component.  It is also compatible with
independent additive valuation rows, so recipient capture alone cannot
contradict it.

The smallest missing global operation at (1) is a root/anchor change that
leaves the priced packet with its holder, or a priority-valid sacrifice that
does not require paying that holder.  When the holder is the first-priority
root and all such anchor operations fail, (1) is the final open gate.

## Claim boundary

This lemma proves the complete-pool threshold dichotomy and unsafe reversal.
It does not prove that the pool total reaches the price, that the reversed
response always completes rank/release routing, or that aggregate
underpayment contradicts the full globally maximal GG state.  It does not
close `T_{L,times}^*` or prove four-agent/general EFX.

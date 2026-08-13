# Referee report: closing-source deletion return

**Date:** 2026-08-12

**Verdict:** the payment algebra and physical allocation are correct, but the
claimed terminal conclusion is not proved.  The theorem must be weakened to
a paid-candidate-or-repeated-response reduction.  It does not currently close
mixed-margin recurrence.

## Independent reconstruction

Fix a Hamiltonian response path

\[
 t=h_0\to h_1\to h_2\to h_3\to c.
\]

For each source `i`, its matched core `A_i` lies in its outgoing target.  For
each nonhole owner target `j`, its incoming core is `C_j=A_{pred(j)}` and
`Y_j=C_j dotunion R_j`.  The decorated closing core `D` lies in the unmatched
hole target `Y_t`.

If the target-owner separator holds, choose a least-t good `g in D` and put
`P=D-g`.  The proposed allocation is

\[
 Z_t=P,
 \qquad
 Z_i=A_i+R_i\quad(i\ne t).                         \tag{1}
\]

## Findings by required gate

### Physical disjointness — proved

The old matching uses distinct targets.  In each nonhole target `Y_j`, its
incoming core and residual are disjoint.  Therefore the terms in (1) use at
most one incoming core and its own target residual, and the hole packet `P`
is disjoint from all matched targets.  This proves physical disjointness from
the actual target partition.  The earlier audit's synthetic support labels
did not establish this, although its conclusion was correct.

### Current-safe versus base-common-safe — corrected

Deletion gives

\[
 \tau_h(P)\le\tau_h(D)\le v_h(Y_h),                \tag{2}
\]

so `P` is current-safe.  It need not be base-common-safe: exact rational data
`v_h(X_h)=1`, `v_h(Y_h)=5`, and `tau_h(D)=4` satisfy (2) while violating base
safety.  The proof is sound only because it pays every row directly against
`P`; it may not replace the last term of (2) by `v_h(X_h)`.

### Target owner and nonowners — proved

The target separator and least-good choice give

\[
 v_t(P)=\tau_t(D)>v_t(A_t+R_t)>v_t(X_t).
\]

Any nonowner already paid against `D` remains paid against `P` by threshold
monotonicity.  If its residual failed against `D`, the earlier cancellation
already produced the incoming-core self-response, so that branch is
unchanged.

### Closing-source residual — proved locally

If `A_s+R_s` pays `tau_s(P)`, the source is paid.  Otherwise

\[
 v_s(A_s)+v_s(R_s)<\tau_s(P)\le\tau_s(D)
 \le v_s(C_s)+v_s(R_s),
\]

and cancellation yields `v_s(C_s)>v_s(A_s)>v_s(X_s)`.  Since `C_s` is an old
base-common-safe core, it is a valid base response by `s` into target `s`.
This is a self-response edge.  Calling it a PI contradiction additionally
requires its incoming packets to be internally supplied; otherwise the valid
conclusion is only a named response/support dependency.

### Strict lexicographic progress — proved only at an EFX leaf

Every bundle in (1) is strictly above its owner's base utility.  Consequently
an EFX instance of (1) is a Pareto, hence lexicographic, contradiction.  This
strictness does not turn a non-EFX candidate into progress.

### Repeated decorated response — gap

If (1) is non-EFX, minimal extraction from a failed changed target gives a
response safe relative to (1).  It need not be base-common-safe and, more
importantly, one response does not supply the rank-four matching required by
the five-target hole-pivot theorem.

The dependencies themselves state this limitation:

- `PAID_SPLICE_OBSERVER_FAILURE_CURRENT_RESPONSE_LEMMA_20260811.md` ends at
  the repeated decorated-response connected-splice terminal.
- `CHARITY_AUGMENTED_FIVE_TARGET_HOLE_PIVOT_CYCLE_LEMMA_20260811.md` assumes
  a rank-four matching at one fixed decorated physical state and stable edge
  labels.
- `FULL_SIGNED_TRANSFER_STATE_RECONSTRUCTION_LEMMA_20260811.md` reconstructs
  a repeated state but explicitly does not pay its alternating cycle.

Thus none proves the manuscript sentence that an already recorded response
from an unsafe deletion-return target “invokes” PI or support progress.

## Exact rational local countermodel

The referee audit contains a positive rational four-agent state with:

1. singleton base utilities all equal to one;
2. four old singleton common-safe desired path cores;
3. a current-safe decorated core `D={d0,d1}` desired by the closing source;
4. the target-owner separator;
5. pairwise-disjoint deletion-return candidate bundles, all strictly above
   base; and
6. a strict EFX failure whose minimal response core is `{a1}`.

That response may already be present in the finite history, while every
current response edge has the same single source.  The response graph has
rank one and no directed owner cycle.  Repeating its exact record changes no
support.  This is not a full GG counterexample—it is a countermodel to the
last logical implication under the stated local premises, proving that an
additional global matching/transition premise is necessary.

## Corrected theorem boundary

The referee-grade statement currently justified is:

> Every mixed-margin Hamiltonian state admits either the deletion-return
> allocation (1), with every owner strictly paid, or an incoming-core
> self-response.  If (1) is EFX, it contradicts global lex maximality.  If it
> is non-EFX, it yields an explicitly decorated current response.  An old
> exact response reaches the repeated decorated-response connected-splice
> terminal.

The smallest missing operation is a **rank-completing paid-response splice**:
starting from the unsafe deletion-return candidate and its repeated response,
either complete it to a rank-four internally supplied matching while
preserving all four payment budgets, or prove a strict increase in one fixed
finite state order.  Without that operation the mixed-margin theorem and the
entire GG cycle class remain open.

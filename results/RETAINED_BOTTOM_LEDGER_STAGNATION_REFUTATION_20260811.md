# Retained-bottom ledger stagnation refutation

**Date:** 2026-08-11

**Status:** exact positive-additive refutation of `(V,S)` as a strict inner
termination coordinate; the witness is local and does not satisfy global GG
maximality

## Candidate after bottom absorption

The nested support update gives genuine progress whenever absorbed support
`V` grows or a retained response core consumes a fresh part of it, growing
`S subseteq V`.  One might hope that adding

\[
 (|V|,|S|)                                          \tag{1}
\]

to the historical response/rank ledger makes the entire inner recurrence
strict.  It does not.

## Exact tail lift of the four-state plateau

Start from the exact nine-good positive-additive response plateau used in
the historical-ledger refutation. Add a bottom good `h` to the base root and
a balancing good `k` to the base external owner `s`. Increase the root row
inside each of the two alternative root cores, without crossing its common-
safety threshold. The values are chosen with strict slack so that

\[
 (X_r+h,\ X_q,\ X_c,\ X_s+k;\{f\})
 \quad\text{is EFX}.                               \tag{2}
\]

In every compressed state attach `h` as an unselected tail of the chosen root
target and `k` to the old `A_s` target. The selected root response core omits
`h`; both alternative root cores remain common-safe and desired after the
root-row adjustment. Exact dyadic
perturbations make all eleven-good subset sums injective while preserving
every strict comparison.

The four response states retain maximum rank three, represented owner union
four, and the same two alternating holes and residual supports.  Every state
is non-EFX.  The chosen desired response core inside the root target omits
`h`, so the bottom tail is never consumed:

\[
 V=\{h\},\qquad S=\varnothing                      \tag{3}
\]

in all four states.  After the owner-indexed residual history is saturated,
every coordinate—retained top support, historical rank and owner union,
residual ratios and supports, absorbed bottom support, and consumed bottom
support—is identical across the entire plateau.

## Consequence

The pair `(V,S)` is necessary for the local overlap-reset theorem but is not
a strict global termination potential.  A support-disjoint bottom tail can
remain physically attached to the root while the response compression
changes holes and root cores underneath an already saturated history.

Consequently the support-disjoint repeated-bottom gate cannot be closed by
another historical support counter alone.  It needs a current-state selector
that orients the four compressions, or an operation that exits them together.
The smallest operation already indicated by the hard flower geometry is a
surplus-budgeted connected component that splices the repeated root-facing
return with the retained bottom tail instead of restarting the compression.

## Verification and boundary

[`retained_bottom_ledger_stagnation_refutation_audit.json`](retained_bottom_ledger_stagnation_refutation_audit.json)
uses exact `Fraction` arithmetic, checks positivity and all eleven-good subset
sums, verifies base EFX and charity dominance, exhausts every response
matching, and replays all four non-EFX states and their identical expanded
ledger.

This refutes the expanded local potential, not the existence of a
deterministic current-state selector or connected escape.  It does not assert
global lex maximality or generalized PI-freeness, refute GG closure, or
refute four-agent/general additive EFX.

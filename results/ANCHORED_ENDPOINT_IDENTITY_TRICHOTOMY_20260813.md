# Anchored endpoint identity trichotomy

**Date:** 2026-08-13

**Status:** exact identity reduction of the unique endpoint order; three
flower-specific inequalities remain

## Enumeration

The permanent Hamiltonian anchor is the adjacent edge `r -> q`.  The unique
path-core survivor has failed target at position one and response source at
position three.  Therefore the six anchored paths reduce, after exchanging
the two external labels `c,s`, to exactly three types:

| Type | Path `(h_0,h_1,h_2,h_3)` | Hole | residual-top-up target | endpoint middle core | strict response source |
|---|---|---|---|---|---|
| I | `(r,q,e,e')` | `r` | `q` | external | external |
| II | `(e,r,q,e')` | external | `r` | `q` | external |
| III | `(e,e',r,q)` | external | external | `r` | `q` |

There are two labeled paths of each type.

## Consequence for protected floors

The anonymous joint selector has two possible deficits:

1. removing the residual part `J` of the response can underpay `h_1`; and
2. moving a desired subcore `H subseteq A_2` into the hole can underpay
   `h_0` or `h_2` after the compensating packet `K subseteq P` is chosen.

The identity table shows which already developed GG machinery can possibly
reverse each deficit.

### Type I: root-hole / q-target

The hole floor is the root priority floor and cannot be sacrificed.  The
residual-top-up target is protected `q`.  The required theorem is a
root/q two-row reservoir inequality: jointly replace `q`'s critical `J`
and the external middle owner's exchange packet without consuming the
root's complete surplus on `P`.

### Type II: external-hole / root-target / q-middle

The residual-top-up packet is removed from the restored root target, while
the endpoint exchange displaces the protected `q` core.  The hole is an
external owner and may use the priority-valid direct floor rather than an
unconditional base floor once root or q remains strict.  The required
theorem is precisely a root/q compensation fork with an external sink.

### Type III: external target / root-middle / q-source

The response source `q` is already strict.  The endpoint exchange displaces
a root desired core, so the middle floor is the root priority floor.  The
hole and residual-top-up target are the two external owners.  The required
theorem is a root-preserving two-hole selector with `q`'s strict gain as the
lexicographic witness; no new q-payment inequality is needed.

## Exact remaining disjunction

Consequently a globally realizable endpoint separator must satisfy at least
one of three identity-specific systems:

1. **I:** simultaneous root-hole and q-target blockade;
2. **II:** simultaneous root-target and q-middle blockade after the external
   hole receives its weakest priority-valid floor; or
3. **III:** root-middle blockade after optimizing the two external holes and
   crediting q's strict source gain.

An anonymous positive-rational hole separator does not establish any of
these systems because it contains neither the permanent `r -> q` anchor nor
the corresponding flower reservoir inequalities.  Conversely, proving one
generic scalar exchange without these identities is unnecessarily strong.

## Verification and boundary

The exact audit filters the 18 anchored nonself pivots, selects the six
endpoint source-at-position-three paths, and verifies two labeled instances
of each identity type.  No item/value cap is used.

This trichotomy does not prove the three flower-specific reverse
inequalities, establish a globally maximal endpoint countermodel, close GG,
or prove four-agent/general additive EFX.

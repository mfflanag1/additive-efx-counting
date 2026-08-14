# Closed base-support response old-or-growth lemma

**Date:** 2026-08-13

**Status:** cap-free localization of every decorated response to a reassembled
closure target

## Closed reassembly target

Let `S` be a base-support-closed owner set and let `Z` be its paid reassembly.
For each `j in S`, write

\[
 Z_j=X_j\mathbin{\dot\cup}E_j,                    \tag{1}
\]

where every good of `E_j` is base charity or is base-owned by an owner
outside `S`. This is exactly the decomposition in the base-support closure
lemma.

Let `D subseteq Z_j` be any base-common-safe desired response core for source
`h`:

\[
 v_h(D)>v_h(X_h),
 \qquad \tau_a(D)\le v_a(X_a)\quad(a\in N).       \tag{2}
\]

Then exactly one of the following support alternatives holds.

1. **Old ordinary response:** `D cap E_j` is empty. Then `D subseteq X_j`, so
   `(h,j,D)` was already a valid ordinary base response into owner `j`'s base
   target.
2. **External-support response:** `D cap E_j` is nonempty. Every good in this
   intersection is supplied by base charity or by an owner outside `S`.
   Attaching its exact incoming/release label therefore joins charity to the
   physical component or strictly grows the represented owner union.

This dichotomy is purely set-theoretic and has no item, packet, or value cap.

## Saturation consequence

At an exact saturated repeat, an external-support response cannot be silently
treated as the old internal edge: its supplier and incoming packet are part
of the full signed response record. It either enlarges the component, adds a
new core/release label, or repeats an already recorded external attachment.

Once all such attachments are saturated, an external-support response may
still repeat, but its charity/outside supplier is already part of the signed
component and its full packet label is fixed. Thus the paid-closure recurrence
reduces to a **labeled** Hall relation whose edges are either old ordinary
responses or already-internalized external-support responses. The remaining
rank-three defect is not a donor-payment inequality, but external edges may
not be discarded.

For the repaired full-capture census, the hardest rank-three reassembly has
both kinds: a base-charity-supported self-response into `q`, and an old
response from outside owner `s` into closure target `r`. Hence it activates
charity attachment and owner-union growth before it can qualify as a closed
saturated countermodel. This is descriptive evidence; the bounded master did
not encode these saturation exits.

## Verification and boundary

[`audit_closed_base_support_response_old_or_growth.py`](../tracks/parkability/audit_closed_base_support_response_old_or_growth.py)
exhausts all base/external/response subsets on an eight-good universe and
verifies the dichotomy and supplier classification independently.

This lemma does not prove that the labeled response graph has full rank,
eliminate a repeated Hall defect with already-attached external suppliers,
establish release-compatible PI, bound the final reassembly by four edges, or
prove complete EFX.

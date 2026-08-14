# Saturated represented-component charity-extraction theorem

**Date:** 2026-08-13

**Status:** cap-free extension of full-owner extraction to every saturated
two-, three-, or four-owner response component; outsiders remain unchanged

## Why full physical owner coverage is unnecessary

Let `C subseteq N` be the owners in one exact saturated decorated-response
component, with

\[
 2\le |C|\le4.                                     \tag{1}
\]

Every owner outside `C` is unchanged from the globally lex-maximal base.
Assume its comparisons against every final changed target and charity are
already safe. This is not an extra terminal loophole: if such a comparison
failed, globally minimal extraction would create a decorated response and
either enlarge the represented component or augment the exact response
record, both excluded by saturation.

Within `C`, assume the same current/base source margins, signed observer
surpluses, corrected physical return-packet separator, direct sacrificed-
source checks, and exact response/support saturation as in the full-owner
theorem.

## PI-free path normal form

At response rank `|C|`, a cycle-free matching on the `|C|` owners plus
charity has an owner hole and is a Hamiltonian path

\[
 h_0=t\longrightarrow h_1\longrightarrow\cdots
 \longrightarrow h_{k-1}\longrightarrow c,
 \qquad k=|C|.                                    \tag{2}
\]

Indeed, a charity hole leaves a directed owner cycle; with an owner hole,
every cycle-free rank-`k` functional graph on `k+1` vertices is the single
path (2). A response into `t` has nonself source `s=h_j`, `j>=1`.

Use the path-core/residual notation of the full-owner theorem. Write
`Y_t=D dotunion R_t`, choose a least-`t` good `g in D`, and put `P=D-g`.
Set

\[
 Z_t=P,
 \qquad Z_i=A_i\mathbin{\dot\cup}R_i
       \quad(i\in C\setminus\{t\}),               \tag{3}
\]

with charity

\[
 Q'=A_t\mathbin{\dot\cup}\{g\}\mathbin{\dot\cup}R_t
     \mathbin{\dot\cup}R_c.                       \tag{4}
\]

Owners outside `C` retain `X_i`. Equations (3)--(4) conserve every good.
The incremental supplier graph on `C union {c}` contains

\[
 c\to h_{k-1}\to\cdots\to h_1\to c,
 \qquad h_0\to c,                                 \tag{5}
\]

so it is connected and cyclic for every `k>=2`.

## Payment and terminal contradiction

The target-owner deletion identity, nonowner residual dichotomy, and closing-
source residual dichotomy are independent of `k`. They pay every owner in
`C` or produce PI/self-response, support growth, response augmentation, or
same-record current progress. Saturation excludes every nonpayment exit.

Unsafe changed owner targets and unsafe charity similarly enter decorated-
response augmentation or the finite charity-blocker walk. Saturation forces
the EFX endpoint. Owners outside `C` satisfy all final comparisons by the
outsider-safety premise and remain at their base bundles. The earlier strict
owner inside `C` therefore makes the endpoint a global lexicographic
improvement, contradicting maximality.

## Theorem

No exact saturated decorated-response/base-margin separator exists on a
represented component of size two, three, or four. Full physical coverage
is not required: a safe outside owner may remain unchanged, while an unsafe
outside owner necessarily joins or augments before saturation.

The theorem is cap-free in goods, packet sizes, values, and moved-good
radius. It uses only that the ambient owner set has size four and that the
active component has at least the distinct response target and source.

[`audit_saturated_represented_component_charity_extraction.py`](../tracks/parkability/audit_saturated_represented_component_charity_extraction.py)
independently enumerates all 132 `(component,path,source)` cases: 12 of size
two, 48 of size three, and 72 of size four. It verifies exact atom
conservation, connected cyclic topology, and the payment/saturation
implications.

This theorem closes saturated proper-owner components. It does not by itself
prove that the fixed-`U` recurrence reaches response saturation or close
other GG flower classes.

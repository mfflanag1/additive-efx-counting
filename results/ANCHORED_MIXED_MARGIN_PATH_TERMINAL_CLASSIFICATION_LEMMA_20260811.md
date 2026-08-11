# Anchored mixed-margin path terminal classification lemma

**Date:** 2026-08-11

**Status:** cap-free classification of every permanent-anchor Hamiltonian
path and hole response; anchor-containing critical-top-up payment remains open

## Permanent anchor

In the GG state, the rank-four Hamiltonian charity path contains the permanent
old common-safe response edge

\[
 r\longrightarrow q.                              \tag{1}

Therefore its owner order must contain the adjacent oriented block `(r,q)`.
Among four owners `(r,q,c,s)`, there are exactly six possible paths:

\[
\begin{array}{lll}
 (r,q,c,s),&(r,q,s,c),&(c,r,q,s),\\
 (s,r,q,c),&(c,s,r,q),&(s,c,r,q).
\end{array}                                       \tag{2}

In particular the owner hole—the first vertex—cannot be `q`.

## Response into the hole

The hole owner cannot itself be the decorated source.  A desired core inside
its own current target is a subset of its current bundle and, by positivity,
cannot be strictly better than that whole bundle.

For every remaining source on every path in (2), pivot its response into the
owner hole.

1. In four cases the source is `r` while `r` is not the hole.  The pivot
   removes (1).  This is an explicit anchor release/root change, not an exact
   fixed-anchor recurrence.
2. Exactly two cases close an external two-cycle before reaching the anchor:

   \[
   (c,s,r,q)\text{ with source }s,
   \qquad
   (s,c,r,q)\text{ with source }c.                \tag{3}
   \]

   If the complete two-owner-plus-charity selector fails on (3), every
   remaining packet operation recruits `r` or `q`; the connected owner union
   then strictly grows to the anchored suffix.  Hence (3) cannot be a
   full-owner exact recurrence avoiding (1).
3. The remaining twelve pivots close a prefix owner cycle containing the
   permanent anchor (1).

Thus after anchor/source and owner-union saturation, every exact recurrent
critical-top-up separator contains `r -> q`.  Its target owner lies in
`{r,c,s}`; there is no `q`-hole terminal and no free external cycle.

## Consequence

The source/root-change alternative in the mixed-margin checkpoint is now
finite and explicit.  A non-anchor recurrence releases the root anchor or
strictly grows into it.  The sole stable terminal is an anchor-containing
cycle, so the remaining proof must use the GG root/`q` reservoir inequalities
to substitute the critical top-up, or instantiate an anchored globally
maximal countermodel.

## Verification and boundary

[`anchored_mixed_margin_path_terminal_classification_audit.json`](anchored_mixed_margin_path_terminal_classification_audit.json)
exhausts the six anchored Hamiltonian paths and all eighteen nonself hole
pivots.  It verifies four anchor releases, two external two-cycles, twelve
anchor-containing cycles, and exclusion of a `q` hole.

This lemma does not pay an anchor-containing cycle, force a root/`q`
substitution packet, eliminate the full-owner critical-top-up separator,
produce a globally maximal countermodel, close GG, or prove four-agent/
general additive EFX.

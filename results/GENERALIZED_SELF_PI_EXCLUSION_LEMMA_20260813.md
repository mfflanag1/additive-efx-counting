# Generalized self-PI exclusion lemma

**Date:** 2026-08-13

**Status:** cap-free consequence of the generalized BCFF champion and PI-cycle
definitions; independently checked in both residual twelve-good cells

## Statement

Let `X` be a partial EFX allocation, let `U` be its unallocated set, and let
`i` be an owner.  Suppose that `H` is a nonempty subset of `U`, `S` is a
subset of `X_i`, and `i` is most envious of

\[
                 (X_i\setminus S)\mathbin{\dot\cup}H.       \tag{1}
\]

Equivalently, the generalized champion graph contains the self-edge

\[
                         i\;\xrightarrow{H\mid S}\;i.       \tag{2}
\]

Then (2) is a length-one Pareto-improvable cycle.  Consequently, a state
with no release-compatible generalized PI cycle cannot contain such a
self-response.

## Proof

The single incoming packet on (2) is `H`, so pairwise disjointness of
incoming packets is vacuous.  Since `H` is contained in the unallocated set
`U`, the availability condition in the definition of a generalized PI cycle
holds without using any released packet.  Thus (2) is a PI cycle.  The BCFF
PI-cycle lemma replaces `X_i` by the desired core of (1), leaves every other
owner weakly unchanged, and produces a partial EFX allocation that strictly
improves `i`.  This contradicts either PI-freeness or saturation of strict
same-record progress.  No bound on the number of goods or packet sizes is
used.

The same proof applies when a larger common-safe desired bundle is first
shrunk to an inclusion-minimal desired core: its external part remains a
subset of `U` whenever it contains no allocated goods outside `X_i`.

## Exact residual-cell corollary

Both residual masters require `s` to be most envious of the common-safe core

\[
                              E=\{e,l\}.           \tag{3}
\]

In both base allocations, `X_s=\{e,p\}` and `l` is unallocated.  Hence (3)
is exactly the self-edge

\[
                       s\;\xrightarrow{\{l\}\mid\{p\}}\;s,
\]

which is a one-edge generalized PI cycle.  Therefore the full-capture and
two-bare residual atomizations are inconsistent with the complete PI-free
premise, independently of which of the two rank-three response forms is
selected.

## Verification and boundary

`audit_generalized_self_pi_exclusion.py` reconstructs the offered bundle,
incoming packet, and released packet independently for both bases and asks
QF_LRA for a valuation satisfying the required response together with its
negation as a generalized self response.  All four form/cell records are
UNSAT.  The corresponding master tests now require UNSAT rather than the
obsolete SAT calibration.

This eliminates the two declared residual atomizations.  It does **not**
show that every external response is a self-response: a core may import a
good allocated to another owner.  Such nonself incoming/release dependencies
are the remaining generalized-PI response-closure gate.

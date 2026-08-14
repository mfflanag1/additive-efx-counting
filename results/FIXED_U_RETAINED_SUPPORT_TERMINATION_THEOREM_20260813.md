# Fixed-U retained-support termination theorem

**Date:** 2026-08-13

**Status:** candidate composition, not yet a theorem. Exact repeats at
response rank four enter the Hamiltonian charity-path machinery, but a
sacrificed-hole repeat may remain at response rank three with two unmatched
targets. Closing or refuting that rank-three gate is required before the
fixed-`U` recurrence can be declared closed.

## Exact state and deterministic policy

Fix a finite goods instance and retained support `U`.  An exact continuation
state records all of the following physical data:

1. the owner allocation and charity;
2. retained top support `U`, absorbed/committed bottom supports `(V,S)`, and
   every paid-anchor consumption ledger `(Y_d,T)`;
3. the anchor-constrained full-priority matching and every selected physical
   core;
4. the complete signed incoming/outgoing transfer vector;
5. every ordinary and full decorated response record, including source,
   target support, desired core, released packet, and supplier component; and
6. the current bundle of every source used for same-record progress and the
   current singleton charity token when the blocker walk is active.

Every finite selector in the preceding lemmas uses its stated global
objective and then one fixed deterministic physical tie-break.  In
particular, bare movement among maximum-matching plateau states is not a
permitted continuation: the anchor-constrained priority selector chooses one
state, and an exact return invokes the connected-splice recurrence rule.

## Well-founded exact-history potential

Let `Omega(X)` be the finite universe of exact state signatures, exact
directed transition signatures, support commitments, and decorated response
records on the fixed physical ground set.  No a priori cardinality bound is
used; finiteness follows from finiteness of the instance.

During the proof, retain the set

\[
 \mathcal H\subseteq\Omega(X)                     \tag{1}
\]

of signatures already exposed.  Order the run by

\[
 \Phi=|\mathcal H|.                                \tag{2}
\]

Every first occurrence of an allocation/transition, fresh support packet,
new supplier, new full response record, or higher same-record source bundle
strictly increases (2).  No entry is deleted.  Hence (2) can increase only
finitely often.

This is deliberately not the refuted coarse potential
`(|U|,rank,owner union,residual value)`.  It never compares utilities across
valuation rows, and it does not assume that historical maxima orient the
four-state plateau.  The exact physical state and transition are recorded;
when either repeats, the algorithm executes recurrence closure rather than
silently recompressing.

## Exhaustive recurrence closure

The deterministic fixed-`U` continuation has the following exhaustive
phases.

### 1. Support and matching phase

Top-only reset preserves `U`, strictly grows it, or captures the remaining
q-margin.  Floater-consuming cores enter the named floater/source handoff.
Anchor-constrained full-priority matching makes every unmatched-source
blocker chain priority-decreasing.  An active protected `q` is represented;
a degree-zero `q` invokes the split-support root flip.  Every nonroot wall of
any distinguished hole is eliminated by the fixed-`U` global residual
selector.  A survivor is root-facing.

### 2. Root-facing and bottom-tail phase

The root-budget frontier exhausts all two-row packet exchanges.  The third-
owner fork either succeeds, captures a donor margin, or produces aggregate
root concentration.  Top/floater donor capture grows `U` or enters its named
handoff.  Aggregate concentration grows absorbed bottom support `V`; retained
core overlap grows `S` or captures the root margin.  The support-disjoint
bottom plateau is not iterated: it enters the three-owner cycle splice.

The q-budget, fourth-owner substitution, and residual-compensation selectors
exhaust every paid packet split.  A successful split is an all-owner-paid
candidate.  If the fourth donor cannot be compensated, the
uncompensated-split-donor reassembly theorem restores its whole desired core
and sacrifices only the external hole.  Protected `q` is represented or
uses its split-core handoff; the arbitrary-hole selector then returns EFX/PI,
strict history progress, or the already named root-facing state.  Thus the
final payment separator is part of the exact recurrence, not a new terminal.

### 3. Paid/sacrificed candidate phase

An EFX candidate contradicts global lex maximality.  A non-EFX paid
candidate yields a globally minimal current-safe full decorated response.
Paid-anchor recapture either raises one fixed source's current utility,
augments, consumes new paid-anchor support, or releases a previously
committed core as an explicit return component.  The priority-valid
sacrificed-hole branch has the same alternatives after the protected anchors
are restored.

### 4. Decorated component phase

A failed observer budget gives a named signed surplus transfer.  The
corrected component selector requires every return packet to lie in the
pre-existing component pool `P_C`; a just-deleted packet may not be passed
through and immediately returned.  Success joins components or closes by
EFX/PI.  Failure produces the exact base-margin separator.  A new response,
supplier, release, owner, or source bundle increases (2).

When none is new, the complete signed record reconstructs the exact physical
response state. If its response matching has full rank, the Hamiltonian
charity-path and saturated extraction theorems apply. This implication is
not established at rank three: the sacrificed owner may be physically joined
to the component through a response edge while remaining unmatched, leaving
two target holes. Physical owner coverage therefore does not by itself imply
the rank-`|C|` path premise of saturated represented-component extraction.

## Termination proof

Assume an infinite fixed-`U` continuation avoiding EFX/lex and PI.  Since
`Omega(X)` is finite, (2) eventually stops increasing.  From that point:

- no retained or paid-anchor support grows;
- no matching/source/owner/supplier label is new;
- no decorated response record augments;
- no fixed-record source or charity-blocker utility rises; and
- every deterministic state and transition has occurred before.

Phases 1--3 therefore cannot take a fresh progress exit. Their only
repeatable transition is the root-facing/bottom-tail/split-donor recurrence.
At rank four its exact signed repeat enters phase 4 and closes. At rank
three, however, the present dependencies do not prove either rank growth or
a two-hole connected extraction. The history potential is consequently not
yet a termination proof.

The exact graph obstruction and all three minimum normal forms are recorded
in
[`RANK_THREE_EXACT_REPEAT_CLOSURE_GATE_20260813.md`](RANK_THREE_EXACT_REPEAT_CLOSURE_GATE_20260813.md).
The global residual/charity split in
[`RANK_THREE_TWO_HOLE_GLOBAL_RESIDUAL_SPLIT_LEMMA_20260813.md`](RANK_THREE_TWO_HOLE_GLOBAL_RESIDUAL_SPLIT_LEMMA_20260813.md)
reduces the remaining packet obstruction to one strict capture-or-parked-own-
support polarity, but does not yet reverse it.

## Candidate theorem and remaining gate

To promote the candidate, one must prove that every exact rank-three repeat
in the sacrificed-hole branch has one of:

1. an EFX lexicographic improvement;
2. a release-compatible PI component;
3. strict retained/support/response/current progress; or
4. rank growth to the full Hamiltonian response state; or
5. a priority-valid two-hole connected charity extraction.

The current artifacts establish the rank-four endpoint but not alternatives
4--5 at rank three. Consequently the fixed-`U` retained-support recurrence is
**not yet closed**.

## Independent encoding and claim boundary

[`audit_fixed_u_retained_support_termination.py`](../tracks/parkability/audit_fixed_u_retained_support_termination.py)
is a dependency and coarse phase-graph audit. It does not encode the
rank-three-to-rank-four implication and therefore cannot certify termination.

This candidate does **not** yet close the fixed-`U` recurrence. It also does
not close the other seven three-nonsingleton cycle classes,
the four-nonsingleton branch, degeneracy/tie/zero wrappers, four-agent
additive EFX, or general additive EFX.  Those claims require the separate
branch inventory below.

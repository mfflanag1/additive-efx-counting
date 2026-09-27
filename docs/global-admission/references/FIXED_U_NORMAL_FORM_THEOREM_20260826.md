# Fixed-U normal form: the exact response-relation chart and the immediate-EFX reduction

**Date:** 2026-08-26  **Branch:** `fable/efx-fixed-u-normal-form` (from `69c1dcd`)  
**Status:** exhaustive chart theorems (twelve-atom: 316 cells; cap-free: 679 cells); the named
five-response classification is a premise-level statement, not a normal form; **the frozen
twelve-atom four-edge objective is refuted by two exact rational residual states** of the master
that lie outside the named forms, have no complete EFX allocation within four support edges, and
close with five (outcome 3 of the target: an exact obstruction to the asserted classification,
with the four-edge cap — not EFX — as the boundary).  Nothing here concerns general additive EFX.

Companion: `FIXED_U_NORMAL_FORM_PREMISE_LEDGER_20260826.md` (frozen premises P1–P15).

## 1. Objects

The saturated root-facing rank-three fixed-U separator, as encoded, is the twelve-atom master
`M` = P1–P9 of the ledger: the canonical support state `Y` (r{a0,a1,h}, q{j,k,q0}, d{m,gq,gr},
s{l,e}, charity{p}), positive valuations `0<v<16` with base normalization and base EFX, the named
packet inequalities, the retained cores `A,Q,E`, the root-facing wall on `d`, and no rank-four
response matching at the support, split and reassembly states, with self responses excluded.
The **exact response relation** of a valuation is the set of nonself pairs `s->t` (`s` an owner,
`t` an owner or charity) such that some nonempty subset of `Y_t` is a base-common-safe or
current-common-safe desired core of `s`.  The relation is a function of the valuation; the
premises P10–P15 (global lex maximality, PI-freeness, ledgers, saturation exclusions) are not
encoded and are not used below.

## 2. Chart theorem (exact, twelve-atom)

**Theorem A.**  Exactly 316 exact nonself response relations are realizable under `M`.  In every
one of them `d->q` and `d->r` hold and no response targets charity; the rank (maximum owner
matching) is 3 in 264 relations, 2 in 50 and 1 in 2; the edge counts range from 2 to 9 (80
relations have exactly five edges).  Among the four named "corrected forms", indices 1 and 3 are
unrealizable; indices 0 and 2 occur exactly once each and as strict sub-relations of 8 and 16
further cells respectively.

*Proof.*  `census_fixed_u_exact_response_relations.py` runs the CEGAR "master ∧ (relation ≠ each
recorded relation)" to UNSAT (316 rounds, 15 s), recording a rational witness per relation.
`independently_verify_fixed_u_relation_chart.py` (no solver, no shared code) re-derives at every
witness all displayed premises of `M`, the exact relation and the rank, and the absence of a
rank-four matching at all three states; all 316 verify (`fixed_u_exact_response_relation_chart_*`).
The unrealizability of forms 1 and 3 and realizability of 0 and 2 is additionally confirmed by the
code's own exact-form masters (`unsat, sat, unsat, sat`).  ∎

**Theorem A′ (cap-free chart).**  Under the physical-minimum master (every atom a role with
total `T` and per-observer minimum `M`, singleton iff `T=M` for all observers, otherwise
`T>=2M`; tails `T−min M`), exactly **679** exact nonself response relations are realizable.  The
316 twelve-atom relations are exactly the 316 physical relations containing `d->r`; the other 363
lack `d->r`.  `d->q` is universal, charity is never a target, ranks are 3/2/1 in 545/127/7 cells,
forms 1 and 3 remain unrealizable and forms 0 and 2 occur exactly once each.  Verified by the same
census CEGAR (679 rounds, 60 s) and a solver-free physical verifier at every witness
(`fixed_u_physical_exact_response_relation_chart_*`).  In particular the ledger's statement that
the strong-envy wall *forces* `d->r` (item 4, O:22-25) is true for atoms and **false for packets**.

**Corollary A1 (what the classification lemma proves).**  The step "the exact support relation
has five edges" (ledger item 4) is a premise.  Under `M` alone, 236 realizable relations have
other edge counts and 78 five-edge relations are not of the matching form; the lemma's
"exactly two forms survive" is correct *relative to that premise* and is verified here, but it
is not a normal form for the states of `M`.  No document in the reference set derives the
five-edge premise from the saturation exclusions (items 7–12); it is an inserted saturation step.

## 3. Immediate-EFX closure

**Proposition B (witness level).**  At each of the 316 chart witnesses there is a complete EFX
allocation of the twelve atoms to the four owners (charity empty) using at most four
support-transfer edges from `Y`; the minimal edge counts are 1 (one cell), 2 (12), 3 (180) and
4 (123).  Verified by exact `Fraction` re-audit of every allocation.

**Theorem C (negative, twelve-atom, exact).**  There are valuations of `M` with no complete EFX
allocation of the twelve atoms using at most four support-transfer edges.  Two are pinned in
`fixed_u_twelve_atom_four_edge_residuals_20260826.json`: their exact relations are
`{d>q,d>r,d>s,q>r,r>d,r>q,r>s,s>r}` (8 edges) and `{d>q,d>r,q>r,r>d,r>s,s>q,s>r}` (7 edges), both
rank 3, neither a named form.  At each, every master premise P1–P9 verifies solver-free; the
integer-owner and the Boolean piece-placement encodings both return UNSAT at four edges and SAT
at five; and an exhaustive brute force over all `4^12 = 16,777,216` complete allocations finds
22,364 EFX allocations at the first residual, none with fewer than five support edges.  Hence the
frozen objective "every saturated root-facing rank-three fixed-U state admits a complete EFX
allocation through at most four support-provenance edges" is **false on `M`** (twelve-atom,
unit packets), while complete EFX itself holds there with a fifth edge.  The residuals were found
by the global four-edge CEGAR after 515 closing allocations (the seeded pass plus four parallel
bursts); the 515-allocation menu closes every other master model generated and is pinned as
`fixed_u_master_complete_efx_edge4_cuts_20260826.jsonl`.

*Method.*  `run_fixed_u_master_complete_efx_cegar.py`: the loop "M ∧ (no menu allocation is EFX)
→ valuation → minimal-edge complete EFX allocation → cut" with the EFX conditions of an
allocation being linear in the valuation, seeded with the 165 distinct minimal-edge allocations
of the chart witnesses; parallel seeded bursts with merged, deduplicated cuts.  A terminal UNSAT
is a proof over all valuations of `M`; a terminal UNSAT oracle would be an exact residual
valuation with no four-edge complete EFX allocation.  The menu is not a small fixed-topology
selector: after the seeded pass and the first parallel burst the 292 distinct closing allocations
use 122 distinct support topologies (edge counts 1/2/3/4 in 1/12/118/161 cuts; charity's `p` goes
to each of the four owners), consistent with the corpus's earlier finding that no small named
topology family is a universal selector.

## 4. The reduction and the exact implication

Let FORM2-CLOSURE be the black box "every form-2 state admits a complete EFX allocation with at
most four support edges (and ≤4 split roles)".  On the twelve-atom master `M`:

1. **The literal predicate** (items 1–12 including the five-edge premise) reduces, by Theorem A
   and Corollary A1, to the two cells form 0 and form 2 — a premise-level reduction.  Under it,
   `FORM2-CLOSURE ⇒ UNIVERSAL FIXED-U CLOSURE` needs exactly one more lemma, **FORM0-CLOSURE**
   (the two-cycle R2 cell has only a bounded PI exclusion in the reference set).
2. **Without the five-edge premise** — i.e. for every state of `M` — the implication is
   **false for the four-edge conclusion**: Theorem C exhibits states of `M` outside both named
   forms with no four-edge complete EFX allocation.  Since FORM2-CLOSURE (a statement about
   form-2 states) says nothing about those cells, no conditional reduction of `M` to form 2 can
   be a theorem for the four-edge objective; the exact residual states are the obstruction to the
   asserted classification (target outcome 3).
3. **What survives.**  Every state of `M` examined — all 316 chart witnesses and all 517 master
   models generated by the global CEGAR — has a complete EFX allocation within **five** support
   edges (at most 5 in every case, exactly 5 at the residuals).  The corrected universal statement
   "every state of `M` admits a complete EFX allocation with at most five support-transfer edges"
   is the one remaining lemma for universal fixed-U closure at the twelve-atom level, and its
   cap-free analogue (whole roles, physical master, any of the 679 cells) is the running five-edge
   CEGAR of §4′.  Under that lemma FORM2-CLOSURE is not needed at all.

## 4′. Cap-free lift (physical-minimum master, no form restriction)

- **Four edges, whole roles: refuted** (and, by Theorem C, four edges fail already for atoms).  `run_fixed_u_physical_master_whole_role_cegar.py
  --edge-cap 4` finds after 8 cuts an exact rational profile with no whole-role four-edge EFX
  allocation; its exact relation is `{d>q, q>r, q>s, r>s, s>q, s>r}` (rank 3, no `d>r`, i.e.
  outside the twelve-atom chart).  It closes whole-role at five edges, and at four edges with a
  single split role (universal over its two-good realizations, menu 6).  This matches the
  four-split session: the four-edge cap, not splitting, is the operative obstruction.
- **Five edges, whole roles:** not terminated in the session: 235 distinct whole-role five-edge allocations installed, every physical master model closed, no obstruction; resumable from `fixed_u_physical_whole_role_edge5_cuts_20260826.jsonl`.

## 5. What is not established

- The cap-free lift beyond the two statements above.
- P10–P15 (global lex maximality, PI-freeness, saturation exclusions) are never encoded; they are
  not needed for Theorem C and they are not available for termination arguments.
- Whether every saturated fixed-U state is represented by `M` at all (the "representation by
  form 2" gate of `PHYSICAL_MINIMUM_ROLE_UNION_CHECKPOINT_20260814.md`) is untouched.
- Nothing about four-agent or general additive EFX.

## 6. Reproduction

```bash
python -m tracks.parkability.census_fixed_u_exact_response_relations --output /tmp/chart.json
python -m tracks.parkability.independently_verify_fixed_u_relation_chart --chart /tmp/chart.json
python -m tracks.parkability.run_fixed_u_master_complete_efx_cegar --edge-cap 4 --seed-chart /tmp/chart.json \
  --output /tmp/g4.json --cut-ledger /tmp/g4_cuts.jsonl      # resume with --resume-cuts
pytest -q tracks/parkability/test_fixed_u_normal_form_chart.py
```

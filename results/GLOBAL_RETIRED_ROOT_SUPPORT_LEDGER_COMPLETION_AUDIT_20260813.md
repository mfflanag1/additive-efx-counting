# Global retired-root-support ledger: completion audit

**Date:** 2026-08-13

**Verdict:** the stated ledger-composition objective is internally complete
as a conventional cap-free reduction theorem. The output is the exact typed
union

\[
T^\dagger=T_0^*\mathbin{\dot\cup}T_L^*.
\]

This is not a closure of either splice component, GG, four-agent EFX, or
general additive EFX. The cap-free manuscript proof has exact symbolic and
independent finite mechanics audits, but has not received external expert
review or proof-assistant formalization.

**Subsequent closure update (2026-08-14):** the collision component
`T_{L,times}^*` of this historical output union is now closed by
`RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_RESOLUTION_20260814.md`.  The
current unresolved union is `T_0^* dot-union T_{L,perp}^*`.  This does not
change the ledger-composition theorem proved here; it updates the downstream
frontier.

## Requirement audit

| Objective requirement | Authoritative evidence | Verdict |
|---|---|---|
| Start at the globally maximal GG base | theorem, opening and theorem statement | proved conditionally on the frozen GG import |
| Current root and physical anchor label | contract, augmented state (1) | present |
| Complete signed allocation and response record | contract (1); independent reconstruction replay | present and injectively replayed |
| Monotone retired-root-support ledger `L` | contract; theorem, global order (2) | present |
| Protected floor vector | contract separates typed `F` from physical `alpha` | present |
| Same physical label survives floor changes | contract definition of `L_alpha`; transition audit | proved by representation, without relabeling `alpha` |
| Every `G0--G10` transition | transition table; primary audit | all eleven rows present |
| Root flip and orientation reset | cross-cutting table; primary audit | covered |
| Recapture and hole pivot | cross-cutting table; primary audit | covered |
| Anchor exchange and paid-anchor reset | cross-cutting table; primary audit | covered |
| Two-hole normalization | cross-cutting table; primary audit | covered |
| Enlarged-root sacrifice return | `G10` row and cross-cutting table | covered |
| One of EFX, PI, ledger growth, actual finite coordinate change, anchor exchange, or typed splice | theorem, outcomes 1--5 and canonical audit A--D | exhaustive within the contracted transition pool |
| No history-only progress | selector-collision lemma, branches 3--4; exact audit flag | proved: an extracted/tested response or allocation/label transition must be executed |
| No same-label silent retired-good reuse | selector-collision lemma; theorem conclusion | proved operationally by canonical cancellation and outcome routing |
| Selector availability after deletion | theorem B--C; selector-collision lemma | canonical ledger-free realization is tested; every failure retains an exact floor/EFX/release witness |
| Specialized sacrifice/anchor handoff premise fidelity | selector-collision lemma equality and base-floor branches | guarded; unavailable handoffs enter typed `T_L^*` rather than being assumed |
| New root/anchor return is finite progress or exact recurrence | selector-collision lemma, new-label section | proved; a floor-only change is explicitly not a new label |
| Strictly smaller explicit splice class | contract and theorem, exact surviving class | `T^dagger=T_0^* dot-union T_L^*`; post-ledger states are split exhaustively into complete-pool parked support `T_{L,perp}^*` and certified collision `T_{L,times}^*` |
| Transition-by-transition premise table | `GLOBAL_RETIRED_ROOT_SUPPORT_G0_G10_TRANSITION_AUDIT_20260813.md` | delivered |
| Independently replayable signed-state audit | independent audit script and JSON | 15,625 reconstruction pairs and 125,000 normalization cases |
| Updated proof graph | theorem and GG referee composition | delivered |
| No prohibited search | scripts inspect symbolic scalar implications and finite labeled-state mechanics only | no valuation-cell, residual-only, blind-pool, or generic Hall search performed |

## Corrections made during completion review

1. Protected floors were removed from the physical anchor label. Otherwise a
   floor change could have disguised same-anchor reuse as a new label.
2. Collision logging alone was removed as a progress outcome. Progress now
   requires an executed response, allocation, root, or anchor coordinate.
3. The equality branch no longer assumes the specialized sacrifice handoff
   outside its exact premises; failure enters a typed separator.
4. Exact repetition of a ledger-free response after a colliding normalized
   proposal is retained as the normalization-bypass `T_L^*` subtype.
5. The pre-ledger and post-ledger terminals were unified as `T^dagger`, so the
   theorem covers the full base-to-G10 trajectory rather than only the phase
   after the first peel.
6. The no-collision branch was completed: a post-ledger exact `T*` recurrence
   must audit the whole active pool and enters the parked-support subtype
   `T_{L,perp}^*` when every selector/release avoids retired support.

## Replay

Run, in order:

```bash
python tracks/parkability/audit_global_retired_root_support_transition_contract.py --output results/global_retired_root_support_transition_contract_audit.json
python tracks/parkability/audit_retired_packet_selector_collision_normalization.py --output results/retired_packet_selector_collision_normalization_audit.json
python tracks/parkability/audit_global_retired_root_support_ledger_composition_independent.py --output results/global_retired_root_support_ledger_composition_independent_audit.json
python tracks/parkability/audit_global_retired_root_support_ledger_composition.py --output results/global_retired_root_support_ledger_composition_audit.json
python tracks/parkability/audit_gg_cycle_class_referee_composition.py --output results/gg_cycle_class_referee_composition_audit.json
pytest -q tracks/parkability/test_global_retired_root_support_transition_contract.py tracks/parkability/test_retired_packet_selector_collision_normalization.py tracks/parkability/test_global_retired_root_support_ledger_composition.py tracks/parkability/test_gg_cycle_class_referee_composition.py
```

The independent replay validates exact physical conservation, signed-state
reconstruction, cancellation accounting, strict capture, and equality
criticality. It does not independently prove the cap-free semantic mapping
of every GG operation; that mapping remains the conventional manuscript
argument and is the main target for external referee review.

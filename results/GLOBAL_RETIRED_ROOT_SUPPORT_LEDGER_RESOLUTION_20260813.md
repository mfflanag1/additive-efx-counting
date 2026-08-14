# Global retired-root-support ledger objective: resolution

**Date:** 2026-08-13

**Verdict:** **proved as a no-silent-reuse composition theorem.** The ledger
is not enforced by banning retired goods. Every original `G0--G10`
transition remains available for audit; retired transfers are cancelled in a
canonical candidate, all floors and comparisons are recomputed, and any
failure yields exact protected-floor capture plus a finite signed collision
transition or typed `T_L^*` recurrence.

## Requirement-by-requirement result

| Requirement | Result |
|---|---|
| Root and anchor label | physical label includes root, support, supplier, and orientation; typed floors are separate, so a floor change cannot relabel retired support |
| Complete signed allocation/response state | included; reconstruction remains injective |
| Monotone retired ledger | retirement history is inclusion-monotone; collision, complete-state, and anchor-label provenance is recorded only with an actual response/allocation/label transition |
| Root flips/orientation resets | normalized through the same cancellation/floor audit |
| Recapture/hole pivot/two-hole normalization | explicitly present in the cross-cutting transition table |
| Anchor exchanges | a new exact label is finite progress; old-label/new-state and exact-repeat cases are separated |
| Enlarged-root return | root-high response reselects; root-low response peels; every later return is normalized |
| Selector availability | no selector is forbidden; its ledger-free realization is tried and every failed floor yields exact capture |
| Same-label retired-good return | cannot occur silently: it changes an actual extracted/tested response or complete state and records that provenance, or enters `T_L^*` |
| New root/anchor return | new label, changed exact state, or `T_L^*`; no unlabeled restoration |
| Referee-grade theorem | conventional cap-free proof with explicit claim boundary and dependency table |
| Independent replay | separate implementation exhausts signed reconstruction and 125,000 normalization cases |
| Updated proof graph | pre-peel exact recurrence enters `T_0^*`; `G10 -> reselection` or `grow L -> normalize -> EFX/PI/progress/T_L^*`; globally `T^dagger=T_0^* dot-union T_L^*` |

## Important correction to the literal wording

Positive valuations do not imply that an agent will never again prefer a
retired good. The proved operational invariant is that no same-label selector
is **executed** using it: canonical cancellation either supplies a
ledger-free realization or derives one of the theorem's closing, progress,
or `T_L^*` outcomes. Thus a preference can mention the good, but the physical
collision cannot masquerade as a reset. Treating the good as unavailable
without auditing the failed selector was explicitly avoided.

## Surviving terminals

1. **`T_0^*`**, the exact generic recurrence reached while the ledger is
   empty, before a permanent peel.
2. **`T_L^*`**, the post-ledger retired-packet saturated splice: nonempty
   retired support, fixed provenance/holders/floors, failed canonical
   ledger-free realization, a repeated hitting/bypass response or an
   equality-critical/base-floor typed-operation separator, and rank or
   observer-payment separator.

Together these form the single typed global terminal
`T^dagger=T_0^* dot-union T_L^*`. The union is proper inside the augmented
generic `T*` record space because nonempty-ledger records lacking the exact
collision/provenance certificate are excluded.

Thus the named global ledger gate is closed, but GG and four-agent EFX are
not. The next analytic target is payment or anchor conversion inside
`T_L^*`, preferably by using the exact capture packet and known holder; the
separate pre-ledger target is closure of `T_0^*`.

## Artifacts and replay

- [`GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md`](GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md)
- [`GLOBAL_RETIRED_ROOT_SUPPORT_G0_G10_TRANSITION_AUDIT_20260813.md`](GLOBAL_RETIRED_ROOT_SUPPORT_G0_G10_TRANSITION_AUDIT_20260813.md)
- [`RETIRED_PACKET_SELECTOR_COLLISION_NORMALIZATION_LEMMA_20260813.md`](RETIRED_PACKET_SELECTOR_COLLISION_NORMALIZATION_LEMMA_20260813.md)
- [`GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPOSITION_THEOREM_20260813.md`](GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPOSITION_THEOREM_20260813.md)
- [`GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPLETION_AUDIT_20260813.md`](GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPLETION_AUDIT_20260813.md)
- [`global_retired_root_support_ledger_composition_audit.json`](global_retired_root_support_ledger_composition_audit.json)
- [`global_retired_root_support_ledger_composition_independent_audit.json`](global_retired_root_support_ledger_composition_independent_audit.json)

The exact audit commands are the corresponding scripts under
`tracks/parkability/`; the focused pytest target is
`test_global_retired_root_support_ledger_composition.py` together with its
contract and collision-normalization tests.

## Evidence tier

Internally checked conventional proof with exact symbolic subchecks and an
independent finite signed-state implementation. It has not received external
domain-expert review or proof-assistant formalization.

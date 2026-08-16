import EFX48.TerminalCells

namespace EFX48

def FourBySevenEFXInput : Prop :=
  ∀ weight : Weight48,
    (∀ agent good, 0 < weight agent good) →
    ∀ excluded, DeletedGoodEFX weight excluded

def ThreeAgentSevenGoodEFXInput : Prop :=
  ∀ weight : Weight48,
    (∀ agent good, 0 < weight agent good) →
    ∀ owner excluded,
      DeletedAgentGoodEFX weight owner excluded

theorem universalMinimumSafe_of_fourBySevenInput
    (four_by_seven : FourBySevenEFXInput)
    (weight : Weight48)
    (generic : GenericNormalizedCounterexample weight) :
    UniversalMinimumSafe weight :=
  universalMinimumSafe_4x8_of_deletedGoodEFX
    weight
    (fun agent good => (generic.1 agent good).le)
    (four_by_seven weight generic.1)

theorem peelableSafe_of_threeAgentSevenGoodInput
    (three_agent_seven_good : ThreeAgentSevenGoodEFXInput)
    (weight : Weight48)
    (generic : GenericNormalizedCounterexample weight) :
    PeelableSafe weight :=
  peelableSafe_4x8_of_deletedAgentGoodEFX
    weight
    (fun agent good => (generic.1 agent good).le)
    (three_agent_seven_good weight generic.1)

theorem admitsEFX_4x8_of_verified_inputs
    (four_by_seven : FourBySevenEFXInput)
    (three_agent_seven_good : ThreeAgentSevenGoodEFXInput)
    (terminal_cells_unsat : EightTerminalCellsUnsat)
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good) :
    AdmitsEFX weight :=
  admitsEFX_4x8_of_terminal_cells_unsat
    terminal_cells_unsat
    (universalMinimumSafe_of_fourBySevenInput four_by_seven)
    (peelableSafe_of_threeAgentSevenGoodInput
      three_agent_seven_good)
    weight positive

theorem admitsEFX_4x8_of_verified_inputs_nonnegative
    (four_by_seven : FourBySevenEFXInput)
    (three_agent_seven_good : ThreeAgentSevenGoodEFXInput)
    (terminal_cells_unsat : EightTerminalCellsUnsat)
    (weight : Weight48)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good) :
    AdmitsEFX weight := by
  by_contra no_efx
  obtain ⟨perturbed, positive, perturbed_no_efx⟩ :=
    exists_positive_noEFX_perturbation
      weight nonnegative no_efx
  exact perturbed_no_efx
    (admitsEFX_4x8_of_verified_inputs
      four_by_seven three_agent_seven_good
      terminal_cells_unsat perturbed positive)

end EFX48

import EFX48.PositiveOnto
import EFX48.ThresholdCycle

namespace EFX48

variable {Agent Good : Type*}
variable [Fintype Agent] [DecidableEq Agent] [Nonempty Agent]
variable [Fintype Good] [DecidableEq Good]

theorem positive_threshold_cycle_normal_form_of_card_lt
    (weight : Agent → Good → ℝ)
    (positive : ∀ agent good, 0 < weight agent good)
    (allocation : Allocation Agent Good)
    (valid : ValidAllocation allocation)
    (efx : EFX weight allocation)
    (more_goods : Fintype.card Agent < Fintype.card Good) :
    ∃ normalized : Allocation Agent Good,
      EFX weight normalized ∧
      ValidAllocation normalized ∧
      (∀ agent, (normalized agent).Nonempty) ∧
      ∃ owner good, OwnerRemovable weight normalized owner good :=
  threshold_cycle_normal_form
    weight
    (fun agent good => (positive agent good).le)
    allocation
    valid
    (allocation_nonempty_of_positive_efx_of_card_lt
      weight positive allocation valid efx more_goods)
    efx

theorem positive_threshold_cycle_normal_form_4x8
    (weight : Fin 4 → Fin 8 → ℝ)
    (positive : ∀ agent good, 0 < weight agent good)
    (allocation : Allocation (Fin 4) (Fin 8))
    (valid : ValidAllocation allocation)
    (efx : EFX weight allocation) :
    ∃ normalized : Allocation (Fin 4) (Fin 8),
      EFX weight normalized ∧
      ValidAllocation normalized ∧
      (∀ agent, (normalized agent).Nonempty) ∧
      ∃ owner good, OwnerRemovable weight normalized owner good :=
  positive_threshold_cycle_normal_form_of_card_lt
    weight positive allocation valid efx (by decide)

end EFX48

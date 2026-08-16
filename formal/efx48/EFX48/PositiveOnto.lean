import EFX48.Definitions
import Mathlib.Data.Fintype.Card

namespace EFX48

open Finset

variable {Agent Good : Type*}
variable [Fintype Agent] [DecidableEq Agent]
variable [Fintype Good] [DecidableEq Good]

noncomputable def ownerOf
    (allocation : Allocation Agent Good)
    (valid : ValidAllocation allocation) (good : Good) : Agent :=
  Classical.choose (valid good)

theorem ownerOf_mem
    (allocation : Allocation Agent Good)
    (valid : ValidAllocation allocation) (good : Good) :
    good ∈ allocation (ownerOf allocation valid good) :=
  (Classical.choose_spec (valid good)).1

theorem ownerOf_injective_of_card_le_one
    (allocation : Allocation Agent Good)
    (valid : ValidAllocation allocation)
    (card_le_one : ∀ agent, (allocation agent).card ≤ 1) :
    Function.Injective (ownerOf allocation valid) := by
  intro first second same_owner
  apply (Finset.card_le_one_iff.mp
    (card_le_one (ownerOf allocation valid first)))
      (ownerOf_mem allocation valid first)
  rw [same_owner]
  exact ownerOf_mem allocation valid second

theorem bundle_card_le_one_of_empty_efx
    (weight : Agent → Good → ℝ)
    (positive : ∀ agent good, 0 < weight agent good)
    (allocation : Allocation Agent Good)
    (efx : EFX weight allocation)
    (empty_owner : Agent)
    (empty : allocation empty_owner = ∅) :
    ∀ target, (allocation target).card ≤ 1 := by
  intro target
  by_contra not_small
  have one_lt : 1 < (allocation target).card :=
    Nat.lt_of_not_ge not_small
  rcases Finset.one_lt_card.mp one_lt with
    ⟨first, first_mem, second, second_mem, distinct⟩
  have target_ne_owner : empty_owner ≠ target := by
    intro same
    subst target
    simp [empty] at first_mem
  have second_after_first :
      second ∈ (allocation target).erase first :=
    Finset.mem_erase.mpr ⟨Ne.symm distinct, second_mem⟩
  have erased_positive :
      0 < additiveValue weight empty_owner
        ((allocation target).erase first) := by
    unfold additiveValue
    exact Finset.sum_pos'
      (fun good _ => (positive empty_owner good).le)
      ⟨second, second_after_first, positive empty_owner second⟩
  have efx_bound :=
    efx empty_owner target target_ne_owner first first_mem
  have empty_value :
      additiveValue weight empty_owner (allocation empty_owner) = 0 := by
    simp [empty, additiveValue]
  rw [empty_value] at efx_bound
  exact (not_lt_of_ge efx_bound) erased_positive

theorem allocation_nonempty_of_positive_efx_of_card_lt
    (weight : Agent → Good → ℝ)
    (positive : ∀ agent good, 0 < weight agent good)
    (allocation : Allocation Agent Good)
    (valid : ValidAllocation allocation)
    (efx : EFX weight allocation)
    (more_goods : Fintype.card Agent < Fintype.card Good) :
    ∀ agent, (allocation agent).Nonempty := by
  intro agent
  by_contra not_nonempty
  have empty : allocation agent = ∅ :=
    Finset.not_nonempty_iff_eq_empty.mp not_nonempty
  have card_le_one :=
    bundle_card_le_one_of_empty_efx
      weight positive allocation efx agent empty
  have injective :
      Function.Injective (ownerOf allocation valid) :=
    ownerOf_injective_of_card_le_one allocation valid card_le_one
  exact (Nat.not_le_of_lt more_goods)
    (Fintype.card_le_of_injective (ownerOf allocation valid) injective)

end EFX48

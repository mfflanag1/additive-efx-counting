import EFX48.ResidualCuts
import EFX48.UniversalMinimum

namespace EFX48

open Finset

variable {Agent Good : Type*}
variable [Fintype Agent] [DecidableEq Agent] [Nonempty Agent]
variable [Fintype Good] [DecidableEq Good]

theorem additiveValue_mono
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (agent : Agent) {smaller larger : Finset Good}
    (subset : smaller ⊆ larger) :
    additiveValue weight agent smaller ≤
      additiveValue weight agent larger := by
  unfold additiveValue
  exact Finset.sum_le_sum_of_subset_of_nonneg subset
    (fun good _ _ => nonnegative agent good)

def EFXExceptObserver
    (weight : Agent → Good → ℝ)
    (allocation : Allocation Agent Good)
    (excludedObserver : Agent) : Prop :=
  ∀ observer, observer ≠ excludedObserver →
    ∀ target, observer ≠ target →
      ∀ good ∈ allocation target,
        additiveValue weight observer (allocation observer) ≥
          additiveValue weight observer
            ((allocation target).erase good)

def DeletedAgentGoodEFX
    (weight : Agent → Good → ℝ)
    (owner : Agent) (excluded : Good) : Prop :=
  ∃ allocation : Allocation Agent Good,
    ValidAllocationExcept allocation excluded ∧
    allocation owner = ∅ ∧
    EFXExceptObserver weight allocation owner

theorem efx_addGood_at_peelable_owner
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (allocation : Allocation Agent Good)
    (owner : Agent) (excluded : Good)
    (valid_except : ValidAllocationExcept allocation excluded)
    (owner_empty : allocation owner = ∅)
    (base_efx : EFXExceptObserver weight allocation owner)
    (dominant : ∀ removed ∈ Finset.univ.erase excluded,
      additiveValue weight owner
          ((Finset.univ.erase excluded).erase removed) ≤
        weight owner excluded) :
    EFX weight (addGood allocation owner excluded) := by
  intro observer target observer_ne_target removed removed_mem
  by_cases observer_is_owner : observer = owner
  · subst observer
    have target_ne_owner : target ≠ owner :=
      Ne.symm observer_ne_target
    have own_value :
        additiveValue weight owner
            (addGood allocation owner excluded owner) =
          weight owner excluded := by
      simp [addGood, owner_empty, additiveValue]
    rw [own_value]
    have target_unchanged :
        addGood allocation owner excluded target =
          allocation target := by
      simp [addGood, target_ne_owner]
    rw [target_unchanged] at removed_mem ⊢
    have removed_ne_excluded : removed ≠ excluded := by
      intro equal
      subst removed
      exact valid_except.1 target removed_mem
    have removed_in_rest :
        removed ∈ Finset.univ.erase excluded :=
      Finset.mem_erase.mpr
        ⟨removed_ne_excluded, Finset.mem_univ removed⟩
    apply (additiveValue_mono weight nonnegative owner ?_).trans
      (dominant removed removed_in_rest)
    intro good good_mem
    have good_mem_target : good ∈ allocation target :=
      Finset.mem_of_mem_erase good_mem
    have good_ne_excluded : good ≠ excluded := by
      intro equal
      subst good
      exact valid_except.1 target good_mem_target
    have good_ne_removed : good ≠ removed :=
      Finset.ne_of_mem_erase good_mem
    exact Finset.mem_erase.mpr
      ⟨good_ne_removed,
        Finset.mem_erase.mpr
          ⟨good_ne_excluded, Finset.mem_univ good⟩⟩
  · have own_unchanged :
        addGood allocation owner excluded observer =
          allocation observer := by
      simp [addGood, observer_is_owner]
    rw [own_unchanged]
    by_cases target_is_owner : target = owner
    · subst target
      have removed_is_excluded : removed = excluded := by
        have membership :
            removed ∈ ({excluded} : Finset Good) := by
          simpa [addGood, owner_empty] using removed_mem
        simpa using membership
      subst removed
      have target_zero :
          (addGood allocation owner excluded owner).erase excluded =
            ∅ := by
        simp [addGood, owner_empty]
      rw [target_zero]
      simp only [additiveValue, Finset.sum_empty]
      exact Finset.sum_nonneg
        (fun good _ => nonnegative observer good)
    · have target_unchanged :
          addGood allocation owner excluded target =
            allocation target := by
        simp [addGood, target_is_owner]
      rw [target_unchanged] at removed_mem ⊢
      exact base_efx observer observer_is_owner
        target observer_ne_target
        removed removed_mem

theorem peelableSafe_of_deletedAgentGoodEFX
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (deleted_efx : ∀ owner excluded,
      DeletedAgentGoodEFX weight owner excluded)
    (peelable :
      ∃ owner excluded,
        ∀ removed ∈ Finset.univ.erase excluded,
          additiveValue weight owner
              ((Finset.univ.erase excluded).erase removed) ≤
            weight owner excluded) :
    AdmitsEFX weight := by
  obtain ⟨owner, excluded, dominant⟩ := peelable
  obtain ⟨allocation, valid_except, owner_empty, base_efx⟩ :=
    deleted_efx owner excluded
  exact ⟨addGood allocation owner excluded,
    addGood_valid allocation excluded owner valid_except,
    efx_addGood_at_peelable_owner
      weight nonnegative allocation owner excluded
      valid_except owner_empty base_efx dominant⟩

theorem peelableSafe_4x8_of_deletedAgentGoodEFX
    (weight : Weight48)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (deleted_efx : ∀ owner excluded,
      DeletedAgentGoodEFX weight owner excluded) :
    PeelableSafe weight := by
  intro peelable
  exact peelableSafe_of_deletedAgentGoodEFX
    weight nonnegative deleted_efx
    (by simpa [Peelable] using peelable)

end EFX48

import EFX48.Definitions

namespace EFX48

open Finset

variable {Agent Good : Type*}
variable [Fintype Agent] [DecidableEq Agent]
variable [Fintype Good] [DecidableEq Good]

theorem additiveValue_erase_nonnegative
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ i g, 0 ≤ weight i g)
    (observer : Agent) (bundle : Finset Good) (good : Good) :
    additiveValue weight observer (bundle.erase good) ≤
      additiveValue weight observer bundle := by
  unfold additiveValue
  exact sum_le_sum_of_subset_of_nonneg (erase_subset good bundle)
    (by
      intro item _ _
      exact nonnegative observer item)

theorem eraseValue_le_threshold
    (weight : Agent → Good → ℝ)
    (observer : Agent) (bundle : Finset Good) (good : Good)
    (good_mem : good ∈ bundle) :
    additiveValue weight observer (bundle.erase good) ≤
      threshold weight observer bundle := by
  classical
  have nonempty : bundle.Nonempty := ⟨good, good_mem⟩
  rw [threshold, dif_pos nonempty]
  exact Finset.le_max'
    (bundle.image fun item =>
      additiveValue weight observer (bundle.erase item))
    (additiveValue weight observer (bundle.erase good))
    (Finset.mem_image.mpr ⟨good, good_mem, rfl⟩)

theorem threshold_attained
    (weight : Agent → Good → ℝ)
    (observer : Agent) (bundle : Finset Good)
    (nonempty : bundle.Nonempty) :
    ∃ good ∈ bundle,
      threshold weight observer bundle =
        additiveValue weight observer (bundle.erase good) := by
  classical
  rw [threshold, dif_pos nonempty]
  have maximum_mem :=
    Finset.max'_mem
      (bundle.image fun good =>
        additiveValue weight observer (bundle.erase good))
      (nonempty.image fun good =>
        additiveValue weight observer (bundle.erase good))
  rcases Finset.mem_image.mp maximum_mem with
    ⟨good, good_mem, maximum_eq⟩
  exact ⟨good, good_mem, maximum_eq.symm⟩

theorem efx_iff_value_ge_threshold
    (weight : Agent → Good → ℝ)
    (allocation : Allocation Agent Good)
    (nonempty : ∀ agent, (allocation agent).Nonempty) :
    EFX weight allocation ↔
      ∀ observer target, observer ≠ target →
        additiveValue weight observer (allocation observer) ≥
          threshold weight observer (allocation target) := by
  constructor
  · intro efx observer target observer_ne_target
    rcases threshold_attained weight observer (allocation target)
        (nonempty target) with
      ⟨good, good_mem, threshold_eq⟩
    rw [threshold_eq]
    exact efx observer target observer_ne_target good good_mem
  · intro threshold_bounds observer target observer_ne_target good good_mem
    exact (eraseValue_le_threshold weight observer
      (allocation target) good good_mem).trans
      (threshold_bounds observer target observer_ne_target)

theorem ownerRemovable_iff_owner_observer
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ i g, 0 ≤ weight i g)
    (allocation : Allocation Agent Good)
    (efx : EFX weight allocation)
    (owner : Agent) (good : Good)
    (owned : good ∈ allocation owner) :
    OwnerRemovable weight allocation owner good ↔
      ∀ target, owner ≠ target →
        ∀ removed ∈ allocation target,
          additiveValue weight owner ((allocation owner).erase good) ≥
            additiveValue weight owner ((allocation target).erase removed) := by
  constructor
  · intro removable target owner_ne_target removed removed_mem
    have target_ne_owner : target ≠ owner := Ne.symm owner_ne_target
    have removed_new :
        removed ∈ removeOwnedGood allocation owner good target := by
      simpa [removeOwnedGood, if_neg target_ne_owner] using removed_mem
    simpa [removeOwnedGood, if_neg target_ne_owner] using
      removable.2 owner target owner_ne_target removed removed_new
  · intro owner_inequalities
    refine ⟨owned, ?_⟩
    intro observer target observer_ne_target removed removed_mem
    by_cases observer_is_owner : observer = owner
    · subst observer
      have target_ne_owner : target ≠ owner := by
        exact Ne.symm observer_ne_target
      have removed_original : removed ∈ allocation target := by
        simpa [removeOwnedGood, if_neg target_ne_owner] using removed_mem
      simpa [removeOwnedGood, if_neg target_ne_owner] using
        owner_inequalities target observer_ne_target removed removed_original
    ·
      by_cases target_is_owner : target = owner
      · subst target
        have removed_original : removed ∈ allocation owner :=
          (Finset.mem_erase.mp (by simpa [removeOwnedGood] using removed_mem)).2
        have original :=
          efx observer owner observer_ne_target removed removed_original
        have shrink :=
          additiveValue_erase_nonnegative weight nonnegative observer
            ((allocation owner).erase removed) good
        have erase_order :
            ((allocation owner).erase removed).erase good =
              ((allocation owner).erase good).erase removed := by
          ext item
          simp [and_left_comm]
        have observer_bound :
            additiveValue weight observer (allocation observer) ≥
              additiveValue weight observer
                (((allocation owner).erase good).erase removed) := by
          calc
            additiveValue weight observer (allocation observer) ≥
                additiveValue weight observer
                  ((allocation owner).erase removed) := original
            _ ≥ additiveValue weight observer
                (((allocation owner).erase good).erase removed) := by
              simpa [erase_order] using shrink
        simpa [removeOwnedGood, observer_is_owner] using observer_bound
      · have removed_original : removed ∈ allocation target := by
          simpa [removeOwnedGood, if_neg target_is_owner] using removed_mem
        simpa [removeOwnedGood, observer_is_owner, target_is_owner] using
          efx observer target observer_ne_target removed removed_original

theorem exists_ownerRemovable_of_threshold_maximal
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ i g, 0 ≤ weight i g)
    (allocation : Allocation Agent Good)
    (efx : EFX weight allocation)
    (owner : Agent)
    (owner_nonempty : (allocation owner).Nonempty)
    (maximal : ∀ target, owner ≠ target →
      threshold weight owner (allocation target) ≤
        threshold weight owner (allocation owner)) :
    ∃ good, OwnerRemovable weight allocation owner good := by
  rcases threshold_attained weight owner (allocation owner) owner_nonempty with
    ⟨good, good_mem, threshold_owner⟩
  refine ⟨good, (ownerRemovable_iff_owner_observer
    weight nonnegative allocation efx owner good good_mem).2 ?_⟩
  intro target owner_ne_target removed removed_mem
  calc
    additiveValue weight owner ((allocation owner).erase good) =
        threshold weight owner (allocation owner) := threshold_owner.symm
    _ ≥ threshold weight owner (allocation target) :=
      maximal target owner_ne_target
    _ ≥ additiveValue weight owner ((allocation target).erase removed) :=
      eraseValue_le_threshold weight owner (allocation target) removed removed_mem

theorem threshold_maximal_of_ownerRemovable
    (weight : Agent → Good → ℝ)
    (allocation : Allocation Agent Good)
    (nonempty : ∀ agent, (allocation agent).Nonempty)
    (owner : Agent) (good : Good)
    (removable : OwnerRemovable weight allocation owner good) :
    ∀ target, owner ≠ target →
      threshold weight owner (allocation target) ≤
        threshold weight owner (allocation owner) := by
  intro target owner_ne_target
  rcases threshold_attained weight owner (allocation target)
      (nonempty target) with
    ⟨removed, removed_mem, threshold_target⟩
  have target_ne_owner : target ≠ owner := Ne.symm owner_ne_target
  have removed_new :
      removed ∈ removeOwnedGood allocation owner good target := by
    simpa [removeOwnedGood, target_ne_owner] using removed_mem
  have owner_bound :=
    removable.2 owner target owner_ne_target removed removed_new
  have own_erasure_le :=
    eraseValue_le_threshold weight owner (allocation owner) good removable.1
  calc
    threshold weight owner (allocation target) =
        additiveValue weight owner ((allocation target).erase removed) :=
      threshold_target
    _ ≤ additiveValue weight owner ((allocation owner).erase good) := by
      simpa [removeOwnedGood, target_ne_owner] using owner_bound
    _ ≤ threshold weight owner (allocation owner) := own_erasure_le

end EFX48

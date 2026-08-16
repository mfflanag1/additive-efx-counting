import EFX48.EnvySource
import EFX48.ResidualCuts

namespace EFX48

open Finset

variable {Agent Good : Type*}
variable [Fintype Agent] [DecidableEq Agent] [Nonempty Agent]
variable [Fintype Good] [DecidableEq Good]

def ValidAllocationExcept
    (allocation : Allocation Agent Good)
    (excluded : Good) : Prop :=
  (∀ agent, excluded ∉ allocation agent) ∧
  ∀ good, good ≠ excluded → ∃! owner, good ∈ allocation owner

def addGood
    (allocation : Allocation Agent Good)
    (source : Agent) (good : Good) :
    Allocation Agent Good :=
  fun agent =>
    if agent = source then insert good (allocation source)
    else allocation agent

theorem validAllocationExcept_permute
    (allocation : Allocation Agent Good)
    (excluded : Good)
    (valid : ValidAllocationExcept allocation excluded)
    (permutation : Equiv.Perm Agent) :
    ValidAllocationExcept
      (permuteAllocation allocation permutation) excluded := by
  constructor
  · intro agent
    exact valid.1 (permutation agent)
  · intro good good_ne_excluded
    obtain ⟨owner, owned, unique⟩ :=
      valid.2 good good_ne_excluded
    refine ⟨permutation.symm owner, ?_, ?_⟩
    · simpa [permuteAllocation] using owned
    · intro candidate candidate_owns
      apply permutation.injective
      simpa [permuteAllocation] using
        unique (permutation candidate)
          (by simpa [permuteAllocation] using candidate_owns)

theorem addGood_valid
    (allocation : Allocation Agent Good)
    (excluded : Good) (source : Agent)
    (valid : ValidAllocationExcept allocation excluded) :
    ValidAllocation (addGood allocation source excluded) := by
  intro good
  by_cases is_excluded : good = excluded
  · subst good
    refine ⟨source, ?_, ?_⟩
    · simp [addGood]
    · intro candidate candidate_owns
      by_contra candidate_ne_source
      have excluded_in_base : excluded ∈ allocation candidate := by
        simpa [addGood, candidate_ne_source] using candidate_owns
      exact valid.1 candidate excluded_in_base
  · obtain ⟨owner, owned, unique⟩ :=
      valid.2 good is_excluded
    refine ⟨owner, ?_, ?_⟩
    · by_cases owner_is_source : owner = source
      · subst owner
        simpa [addGood, is_excluded] using owned
      · simpa [addGood, owner_is_source] using owned
    · intro candidate candidate_owns
      apply unique candidate
      by_cases candidate_is_source : candidate = source
      · subst candidate
        simpa [addGood, is_excluded] using candidate_owns
      · simpa [addGood, candidate_is_source] using candidate_owns

theorem addGood_nonempty
    (allocation : Allocation Agent Good)
    (nonempty : ∀ agent, (allocation agent).Nonempty)
    (source : Agent) (good : Good) :
    ∀ agent, (addGood allocation source good agent).Nonempty := by
  intro agent
  by_cases same : agent = source
  · subst agent
    exact ⟨good, by simp [addGood]⟩
  · simpa [addGood, same] using nonempty agent

theorem additiveValue_addGood_ge
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (allocation : Allocation Agent Good)
    (excluded : Good)
    (excluded_absent : ∀ agent, excluded ∉ allocation agent)
    (source observer : Agent) :
    additiveValue weight observer (allocation observer) ≤
      additiveValue weight observer
        (addGood allocation source excluded observer) := by
  by_cases same : observer = source
  · subst observer
    simp [addGood, additiveValue, excluded_absent source,
      nonnegative source excluded]
  · simp [addGood, same]

theorem efx_addGood_at_universal_minimum_source
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (allocation : Allocation Agent Good)
    (excluded : Good) (source : Agent)
    (excluded_absent : ∀ agent, excluded ∉ allocation agent)
    (universal_minimum : ∀ agent other,
      weight agent excluded ≤ weight agent other)
    (efx : EFX weight allocation)
    (source_unenvied :
      PlainEnvySource weight allocation source) :
    EFX weight (addGood allocation source excluded) := by
  intro observer target observer_ne_target removed removed_mem
  by_cases target_is_source : target = source
  · subst target
    have observer_ne_source : observer ≠ source :=
      observer_ne_target
    have own_unchanged :
        addGood allocation source excluded observer =
          allocation observer := by
      simp [addGood, observer_ne_source]
    rw [own_unchanged]
    by_cases removed_is_excluded : removed = excluded
    · subst removed
      simpa [addGood, excluded_absent source] using
        source_unenvied observer
    · have removed_mem_base :
          removed ∈ allocation source := by
        simpa [addGood, removed_is_excluded] using removed_mem
      calc
        additiveValue weight observer
            ((addGood allocation source excluded source).erase removed) =
          weight observer excluded +
            additiveValue weight observer
              ((allocation source).erase removed) := by
                rw [addGood, if_pos rfl,
                  Finset.erase_insert_of_ne
                    (Ne.symm removed_is_excluded)]
                simp [additiveValue, excluded_absent source]
        _ ≤ weight observer removed +
            additiveValue weight observer
              ((allocation source).erase removed) :=
          by
            simpa [add_comm] using
              add_le_add_right
                (universal_minimum observer removed)
                (additiveValue weight observer
                  ((allocation source).erase removed))
        _ = additiveValue weight observer (allocation source) := by
          simp [additiveValue, removed_mem_base]
        _ ≤ additiveValue weight observer (allocation observer) :=
          source_unenvied observer
  · have removed_mem_base :
        removed ∈ allocation target := by
      simpa [addGood, target_is_source] using removed_mem
    have target_unchanged :
        addGood allocation source excluded target =
          allocation target := by
      simp [addGood, target_is_source]
    rw [target_unchanged]
    have base_comparison :=
      efx observer target observer_ne_target
        removed removed_mem_base
    exact base_comparison.trans
      (additiveValue_addGood_ge
        weight nonnegative allocation excluded
        excluded_absent source observer)

def DeletedGoodEFX
    (weight : Agent → Good → ℝ)
    (excluded : Good) : Prop :=
  ∃ allocation : Allocation Agent Good,
    ValidAllocationExcept allocation excluded ∧
    (∀ agent, (allocation agent).Nonempty) ∧
    EFX weight allocation

theorem universalMinimumSafe_of_deletedGoodEFX
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (deleted_efx : ∀ excluded, DeletedGoodEFX weight excluded)
    (universal_minimum :
      ∃ excluded, ∀ agent other,
        weight agent excluded ≤ weight agent other) :
    AdmitsEFX weight := by
  obtain ⟨excluded, excluded_minimum⟩ := universal_minimum
  obtain ⟨allocation, valid_except, nonempty, efx⟩ :=
    deleted_efx excluded
  obtain ⟨normalized, normalized_efx, normalized_valid_except,
      normalized_nonempty, source, source_unenvied⟩ :=
    plain_envy_source_normal_form_with_invariant
      weight nonnegative allocation
      (fun candidate => ValidAllocationExcept candidate excluded)
      valid_except
      (fun candidate candidate_valid permutation =>
        validAllocationExcept_permute
          candidate excluded candidate_valid permutation)
      nonempty efx
  exact ⟨addGood normalized source excluded,
    addGood_valid normalized excluded source normalized_valid_except,
    efx_addGood_at_universal_minimum_source
      weight nonnegative normalized excluded source
      normalized_valid_except.1 excluded_minimum
      normalized_efx source_unenvied⟩

theorem universalMinimumSafe_4x8_of_deletedGoodEFX
    (weight : Weight48)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (deleted_efx : ∀ excluded, DeletedGoodEFX weight excluded) :
    UniversalMinimumSafe weight := by
  intro universal_minimum
  exact universalMinimumSafe_of_deletedGoodEFX
    weight nonnegative deleted_efx
    (by simpa [UniversalMinimum] using universal_minimum)

end EFX48

import EFX48.FiniteCycle
import EFX48.ReverseParking
import Mathlib.Data.Fintype.Lattice
import Mathlib.GroupTheory.Perm.Basic

namespace EFX48

open Finset

variable {Agent Good : Type*}
variable [Fintype Agent] [DecidableEq Agent]
variable [Fintype Good] [DecidableEq Good]

def permuteAllocation (allocation : Allocation Agent Good)
    (permutation : Equiv.Perm Agent) : Allocation Agent Good :=
  fun agent => allocation (permutation agent)

noncomputable def thresholdPotential (weight : Agent → Good → ℝ)
    (allocation : Allocation Agent Good) : ℝ :=
  ∑ agent, threshold weight agent (allocation agent)

theorem threshold_le_additiveValue
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ i g, 0 ≤ weight i g)
    (observer : Agent) (bundle : Finset Good)
    (nonempty : bundle.Nonempty) :
    threshold weight observer bundle ≤
      additiveValue weight observer bundle := by
  rcases threshold_attained weight observer bundle nonempty with
    ⟨good, good_mem, threshold_eq⟩
  rw [threshold_eq]
  exact additiveValue_erase_nonnegative
    weight nonnegative observer bundle good

theorem efx_value_ge_all_thresholds
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ i g, 0 ≤ weight i g)
    (allocation : Allocation Agent Good)
    (nonempty : ∀ agent, (allocation agent).Nonempty)
    (efx : EFX weight allocation) :
    ∀ observer target,
      additiveValue weight observer (allocation observer) ≥
        threshold weight observer (allocation target) := by
  intro observer target
  by_cases same : observer = target
  · subst target
    exact threshold_le_additiveValue weight nonnegative observer
      (allocation observer) (nonempty observer)
  · exact (efx_iff_value_ge_threshold weight allocation nonempty).1
      efx observer target same

theorem permuteAllocation_nonempty
    (allocation : Allocation Agent Good)
    (nonempty : ∀ agent, (allocation agent).Nonempty)
    (permutation : Equiv.Perm Agent) :
    ∀ agent, (permuteAllocation allocation permutation agent).Nonempty :=
  fun agent => nonempty (permutation agent)

theorem permuteAllocation_valid
    (allocation : Allocation Agent Good)
    (valid : ValidAllocation allocation)
    (permutation : Equiv.Perm Agent) :
    ValidAllocation (permuteAllocation allocation permutation) := by
  intro good
  rcases valid good with ⟨owner, owned, owner_unique⟩
  refine ⟨permutation.symm owner, ?_, ?_⟩
  · simpa [permuteAllocation] using owned
  · intro candidate candidate_owns
    have old_owner :
        permutation candidate = owner :=
      owner_unique (permutation candidate)
        (by simpa [permuteAllocation] using candidate_owns)
    apply permutation.injective
    simpa [old_owner]

theorem efx_permute_of_maximal_moves
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ i g, 0 ≤ weight i g)
    (allocation : Allocation Agent Good)
    (nonempty : ∀ agent, (allocation agent).Nonempty)
    (efx : EFX weight allocation)
    (permutation : Equiv.Perm Agent)
    (maximal_moves : ∀ agent, permutation agent ≠ agent →
      ∀ target,
        threshold weight agent (allocation target) ≤
          threshold weight agent (allocation (permutation agent))) :
    EFX weight (permuteAllocation allocation permutation) := by
  apply (efx_iff_value_ge_threshold weight
    (permuteAllocation allocation permutation)
    (permuteAllocation_nonempty allocation nonempty permutation)).2
  intro observer target observer_ne_target
  change additiveValue weight observer (allocation (permutation observer)) ≥
    threshold weight observer (allocation (permutation target))
  by_cases fixed : permutation observer = observer
  · rw [fixed]
    exact efx_value_ge_all_thresholds weight nonnegative allocation
      nonempty efx observer (permutation target)
  · exact (maximal_moves observer fixed (permutation target)).trans
      (threshold_le_additiveValue weight nonnegative observer
        (allocation (permutation observer)) (nonempty (permutation observer)))

theorem thresholdPotential_lt_permute_of_strict_moves
    [Nonempty Agent]
    (weight : Agent → Good → ℝ)
    (allocation : Allocation Agent Good)
    (permutation : Equiv.Perm Agent)
    (weak_moves : ∀ agent,
      threshold weight agent (allocation agent) ≤
        threshold weight agent (allocation (permutation agent)))
    (strict_move : ∃ agent,
      threshold weight agent (allocation agent) <
        threshold weight agent (allocation (permutation agent))) :
    thresholdPotential weight allocation <
      thresholdPotential weight (permuteAllocation allocation permutation) := by
  unfold thresholdPotential permuteAllocation
  exact Finset.sum_lt_sum
    (fun agent _ => weak_moves agent)
    (by
      rcases strict_move with ⟨agent, strict⟩
      exact ⟨agent, Finset.mem_univ agent, strict⟩)

theorem critical_target_exists_of_no_removable
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ i g, 0 ≤ weight i g)
    (allocation : Allocation Agent Good)
    (nonempty : ∀ agent, (allocation agent).Nonempty)
    (efx : EFX weight allocation)
    (no_removable : ¬∃ owner good,
      OwnerRemovable weight allocation owner good) :
    ∀ owner, ∃ target, owner ≠ target ∧
      threshold weight owner (allocation owner) <
        threshold weight owner (allocation target) := by
  intro owner
  by_contra no_target
  push Not at no_target
  have maximal : ∀ target, owner ≠ target →
      threshold weight owner (allocation target) ≤
        threshold weight owner (allocation owner) := by
    intro target owner_ne_target
    exact no_target target owner_ne_target
  rcases exists_ownerRemovable_of_threshold_maximal
      weight nonnegative allocation efx owner (nonempty owner) maximal with
    ⟨good, removable⟩
  exact no_removable ⟨owner, good, removable⟩

theorem maximal_critical_target_exists_of_no_removable
    [Nonempty Agent]
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ i g, 0 ≤ weight i g)
    (allocation : Allocation Agent Good)
    (nonempty : ∀ agent, (allocation agent).Nonempty)
    (efx : EFX weight allocation)
    (no_removable : ¬∃ owner good,
      OwnerRemovable weight allocation owner good) :
    ∀ owner, ∃ target,
      owner ≠ target ∧
      threshold weight owner (allocation owner) <
        threshold weight owner (allocation target) ∧
      ∀ other,
        threshold weight owner (allocation other) ≤
          threshold weight owner (allocation target) := by
  intro owner
  rcases Finite.exists_max
      (fun target =>
        threshold weight owner (allocation target)) with
    ⟨target, target_maximal⟩
  have strict :
      threshold weight owner (allocation owner) <
        threshold weight owner (allocation target) := by
    by_contra not_strict
    have target_le_owner :
        threshold weight owner (allocation target) ≤
          threshold weight owner (allocation owner) :=
      le_of_not_gt not_strict
    have owner_maximal : ∀ other, owner ≠ other →
        threshold weight owner (allocation other) ≤
          threshold weight owner (allocation owner) := by
      intro other _
      exact (target_maximal other).trans target_le_owner
    rcases exists_ownerRemovable_of_threshold_maximal
        weight nonnegative allocation efx owner (nonempty owner)
        owner_maximal with
      ⟨good, removable⟩
    exact no_removable ⟨owner, good, removable⟩
  have owner_ne_target : owner ≠ target := by
    intro same
    subst target
    exact (lt_irrefl _ strict)
  exact ⟨target, owner_ne_target, strict, target_maximal⟩

theorem exists_improving_efx_permutation_of_no_removable
    [Nonempty Agent]
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ i g, 0 ≤ weight i g)
    (allocation : Allocation Agent Good)
    (nonempty : ∀ agent, (allocation agent).Nonempty)
    (efx : EFX weight allocation)
    (no_removable : ¬∃ owner good,
      OwnerRemovable weight allocation owner good) :
    ∃ permutation : Equiv.Perm Agent,
      EFX weight (permuteAllocation allocation permutation) ∧
      (∀ agent,
        (permuteAllocation allocation permutation agent).Nonempty) ∧
      thresholdPotential weight allocation <
        thresholdPotential weight
          (permuteAllocation allocation permutation) := by
  classical
  have critical :=
    maximal_critical_target_exists_of_no_removable
      weight nonnegative allocation nonempty efx no_removable
  let next : Agent → Agent :=
    fun owner => Classical.choose (critical owner)
  have next_spec : ∀ owner,
      owner ≠ next owner ∧
      threshold weight owner (allocation owner) <
        threshold weight owner (allocation (next owner)) ∧
      ∀ other,
        threshold weight owner (allocation other) ≤
          threshold weight owner (allocation (next owner)) := by
    intro owner
    exact Classical.choose_spec (critical owner)
  rcases exists_cycle_permutation next
      (fun owner => Ne.symm (next_spec owner).1) with
    ⟨permutation, moved_to_next, moved_exists⟩
  have maximal_moves : ∀ agent, permutation agent ≠ agent →
      ∀ target,
        threshold weight agent (allocation target) ≤
          threshold weight agent (allocation (permutation agent)) := by
    intro agent moved target
    rw [moved_to_next agent moved]
    exact (next_spec agent).2.2 target
  have weak_moves : ∀ agent,
      threshold weight agent (allocation agent) ≤
        threshold weight agent (allocation (permutation agent)) := by
    intro agent
    by_cases moved : permutation agent ≠ agent
    · rw [moved_to_next agent moved]
      exact (next_spec agent).2.1.le
    · rw [not_ne_iff.mp moved]
  have strict_move : ∃ agent,
      threshold weight agent (allocation agent) <
        threshold weight agent (allocation (permutation agent)) := by
    rcases moved_exists with ⟨agent, moved⟩
    refine ⟨agent, ?_⟩
    rw [moved_to_next agent moved]
    exact (next_spec agent).2.1
  refine ⟨permutation,
    efx_permute_of_maximal_moves weight nonnegative allocation nonempty
      efx permutation maximal_moves,
    permuteAllocation_nonempty allocation nonempty permutation,
    thresholdPotential_lt_permute_of_strict_moves
      weight allocation permutation weak_moves strict_move⟩

theorem threshold_cycle_normal_form
    [Nonempty Agent]
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ i g, 0 ≤ weight i g)
    (allocation : Allocation Agent Good)
    (valid : ValidAllocation allocation)
    (nonempty : ∀ agent, (allocation agent).Nonempty)
    (efx : EFX weight allocation) :
    ∃ normalized : Allocation Agent Good,
      EFX weight normalized ∧
      ValidAllocation normalized ∧
      (∀ agent, (normalized agent).Nonempty) ∧
      ∃ owner good, OwnerRemovable weight normalized owner good := by
  classical
  let Candidate :=
    {candidate : Allocation Agent Good //
      EFX weight candidate ∧
      ValidAllocation candidate ∧
      ∀ agent, (candidate agent).Nonempty}
  let initial : Candidate := ⟨allocation, efx, valid, nonempty⟩
  letI : Nonempty Candidate := ⟨initial⟩
  rcases Finite.exists_max
      (fun candidate : Candidate =>
        thresholdPotential weight candidate.1) with
    ⟨best, best_maximal⟩
  by_cases has_removable :
      ∃ owner good, OwnerRemovable weight best.1 owner good
  · exact ⟨best.1, best.2.1, best.2.2.1, best.2.2.2, has_removable⟩
  · rcases exists_improving_efx_permutation_of_no_removable
        weight nonnegative best.1 best.2.2.2 best.2.1 has_removable with
      ⟨permutation, rotated_efx, rotated_nonempty, potential_increase⟩
    let improved : Candidate :=
      ⟨permuteAllocation best.1 permutation,
        rotated_efx,
        permuteAllocation_valid best.1 best.2.2.1 permutation,
        rotated_nonempty⟩
    exact ((not_lt_of_ge (best_maximal improved)) potential_increase).elim

end EFX48

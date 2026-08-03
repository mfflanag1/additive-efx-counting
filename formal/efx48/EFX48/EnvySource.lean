import EFX48.ThresholdCycle

namespace EFX48

open Finset

variable {Agent Good : Type*}
variable [Fintype Agent] [DecidableEq Agent] [Nonempty Agent]
variable [Fintype Good] [DecidableEq Good]

def PlainEnvySource
    (weight : Agent → Good → ℝ)
    (allocation : Allocation Agent Good)
    (source : Agent) : Prop :=
  ∀ observer,
    additiveValue weight observer (allocation source) ≤
      additiveValue weight observer (allocation observer)

noncomputable def ownValuePotential
    (weight : Agent → Good → ℝ)
    (allocation : Allocation Agent Good) : ℝ :=
  ∑ agent, additiveValue weight agent (allocation agent)

theorem efx_permute_of_weak_own_moves
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (allocation : Allocation Agent Good)
    (nonempty : ∀ agent, (allocation agent).Nonempty)
    (efx : EFX weight allocation)
    (permutation : Equiv.Perm Agent)
    (weak_moves : ∀ agent,
      additiveValue weight agent (allocation agent) ≤
        additiveValue weight agent
          (allocation (permutation agent))) :
    EFX weight (permuteAllocation allocation permutation) := by
  apply (efx_iff_value_ge_threshold weight
    (permuteAllocation allocation permutation)
    (permuteAllocation_nonempty allocation nonempty permutation)).2
  intro observer target _
  change
    additiveValue weight observer
        (allocation (permutation observer)) ≥
      threshold weight observer
        (allocation (permutation target))
  exact
    (efx_value_ge_all_thresholds weight nonnegative allocation
      nonempty efx observer (permutation target)).trans
      (weak_moves observer)

theorem ownValuePotential_lt_permute_of_strict_moves
    (weight : Agent → Good → ℝ)
    (allocation : Allocation Agent Good)
    (permutation : Equiv.Perm Agent)
    (weak_moves : ∀ agent,
      additiveValue weight agent (allocation agent) ≤
        additiveValue weight agent
          (allocation (permutation agent)))
    (strict_move : ∃ agent,
      additiveValue weight agent (allocation agent) <
        additiveValue weight agent
          (allocation (permutation agent))) :
    ownValuePotential weight allocation <
      ownValuePotential weight
        (permuteAllocation allocation permutation) := by
  unfold ownValuePotential permuteAllocation
  exact Finset.sum_lt_sum
    (fun agent _ => weak_moves agent)
    (by
      obtain ⟨agent, strict⟩ := strict_move
      exact ⟨agent, Finset.mem_univ agent, strict⟩)

theorem envier_exists_of_no_plainEnvySource
    (weight : Agent → Good → ℝ)
    (allocation : Allocation Agent Good)
    (no_source : ¬∃ source,
      PlainEnvySource weight allocation source) :
    ∀ target, ∃ observer,
      observer ≠ target ∧
      additiveValue weight observer (allocation observer) <
        additiveValue weight observer (allocation target) := by
  intro target
  by_contra no_envier
  push Not at no_envier
  apply no_source
  refine ⟨target, ?_⟩
  intro observer
  by_cases same : observer = target
  · rw [same]
  · exact no_envier observer same

theorem exists_improving_efx_permutation_of_no_plainEnvySource
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (allocation : Allocation Agent Good)
    (nonempty : ∀ agent, (allocation agent).Nonempty)
    (efx : EFX weight allocation)
    (no_source : ¬∃ source,
      PlainEnvySource weight allocation source) :
    ∃ permutation : Equiv.Perm Agent,
      EFX weight (permuteAllocation allocation permutation) ∧
      (∀ agent,
        (permuteAllocation allocation permutation agent).Nonempty) ∧
      ownValuePotential weight allocation <
        ownValuePotential weight
          (permuteAllocation allocation permutation) := by
  classical
  have envier :=
    envier_exists_of_no_plainEnvySource
      weight allocation no_source
  let predecessor : Agent → Agent :=
    fun target => Classical.choose (envier target)
  have predecessor_spec : ∀ target,
      predecessor target ≠ target ∧
      additiveValue weight (predecessor target)
          (allocation (predecessor target)) <
        additiveValue weight (predecessor target)
          (allocation target) := by
    intro target
    exact Classical.choose_spec (envier target)
  obtain ⟨cycle, moved_to_predecessor, moved_exists⟩ :=
    exists_cycle_permutation predecessor
      (fun target => (predecessor_spec target).1)
  let rotation : Equiv.Perm Agent := cycle.symm
  have strict_of_moved : ∀ agent, rotation agent ≠ agent →
      additiveValue weight agent (allocation agent) <
        additiveValue weight agent
          (allocation (rotation agent)) := by
    intro agent moved
    let target := rotation agent
    have target_moved : cycle target ≠ target := by
      intro fixed
      apply moved
      have inverse : cycle target = agent := by
        simp [target, rotation]
      change target = agent
      exact fixed.symm.trans inverse
    have predecessor_eq :
        predecessor target = agent := by
      rw [← moved_to_predecessor target target_moved]
      simp [target, rotation]
    simpa [target, predecessor_eq] using
      (predecessor_spec target).2
  have weak_moves : ∀ agent,
      additiveValue weight agent (allocation agent) ≤
        additiveValue weight agent
          (allocation (rotation agent)) := by
    intro agent
    by_cases moved : rotation agent ≠ agent
    · exact (strict_of_moved agent moved).le
    · rw [not_ne_iff.mp moved]
  have strict_move : ∃ agent,
      additiveValue weight agent (allocation agent) <
        additiveValue weight agent
          (allocation (rotation agent)) := by
    obtain ⟨target, target_moved⟩ := moved_exists
    let agent := cycle target
    have rotation_agent : rotation agent = target := by
      simp [agent, rotation]
    have agent_ne_target : agent ≠ target := target_moved
    have rotation_moved : rotation agent ≠ agent := by
      rw [rotation_agent]
      exact agent_ne_target.symm
    exact ⟨agent, strict_of_moved agent rotation_moved⟩
  exact ⟨rotation,
    efx_permute_of_weak_own_moves
      weight nonnegative allocation nonempty efx rotation weak_moves,
    permuteAllocation_nonempty allocation nonempty rotation,
    ownValuePotential_lt_permute_of_strict_moves
      weight allocation rotation weak_moves strict_move⟩

theorem plain_envy_source_normal_form_with_invariant
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (allocation : Allocation Agent Good)
    (invariant : Allocation Agent Good → Prop)
    (initial_invariant : invariant allocation)
    (invariant_permute : ∀ candidate,
      invariant candidate →
      ∀ permutation : Equiv.Perm Agent,
        invariant (permuteAllocation candidate permutation))
    (nonempty : ∀ agent, (allocation agent).Nonempty)
    (efx : EFX weight allocation) :
    ∃ normalized : Allocation Agent Good,
      EFX weight normalized ∧
      invariant normalized ∧
      (∀ agent, (normalized agent).Nonempty) ∧
      ∃ source, PlainEnvySource weight normalized source := by
  classical
  let Candidate :=
    {candidate : Allocation Agent Good //
      EFX weight candidate ∧
      invariant candidate ∧
      ∀ agent, (candidate agent).Nonempty}
  let initial : Candidate :=
    ⟨allocation, efx, initial_invariant, nonempty⟩
  letI : Nonempty Candidate := ⟨initial⟩
  obtain ⟨best, best_maximal⟩ :=
    Finite.exists_max
      (fun candidate : Candidate =>
        ownValuePotential weight candidate.1)
  by_cases has_source :
      ∃ source, PlainEnvySource weight best.1 source
  · exact ⟨best.1, best.2.1, best.2.2.1,
      best.2.2.2, has_source⟩
  · obtain ⟨permutation, rotated_efx, rotated_nonempty,
        potential_increase⟩ :=
      exists_improving_efx_permutation_of_no_plainEnvySource
        weight nonnegative best.1 best.2.2.2 best.2.1 has_source
    let improved : Candidate :=
      ⟨permuteAllocation best.1 permutation,
        rotated_efx,
        invariant_permute best.1 best.2.2.1 permutation,
        rotated_nonempty⟩
    exact
      ((not_lt_of_ge (best_maximal improved))
        potential_increase).elim

theorem plain_envy_source_normal_form
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (allocation : Allocation Agent Good)
    (valid : ValidAllocation allocation)
    (nonempty : ∀ agent, (allocation agent).Nonempty)
    (efx : EFX weight allocation) :
    ∃ normalized : Allocation Agent Good,
      EFX weight normalized ∧
      ValidAllocation normalized ∧
      (∀ agent, (normalized agent).Nonempty) ∧
      ∃ source, PlainEnvySource weight normalized source :=
  plain_envy_source_normal_form_with_invariant
    weight nonnegative allocation ValidAllocation valid
    (fun candidate candidate_valid permutation =>
      permuteAllocation_valid candidate candidate_valid permutation)
    nonempty efx

end EFX48

import EFX48.PositiveOnto
import EFX48.Perturbation
import EFX48.ThresholdCycle

namespace EFX48

def FeasibleEdge
    (weight : Weight48)
    (bundles : Allocation (Fin 4) (Fin 8))
    (agent ownSlot : Fin 4) : Prop :=
  ∀ targetSlot, targetSlot ≠ ownSlot →
    ∀ good ∈ bundles targetSlot,
      additiveValue weight agent ((bundles targetSlot).erase good) ≤
        additiveValue weight agent (bundles ownSlot)

def HasFeasiblePerfectMatching
    (weight : Weight48)
    (bundles : Allocation (Fin 4) (Fin 8)) : Prop :=
  ∃ assignment : Equiv.Perm (Fin 4),
    ∀ agent, FeasibleEdge weight bundles agent (assignment agent)

def MatchingObstruction
    (weight : Weight48)
    (bundles : Allocation (Fin 4) (Fin 8)) : Prop :=
  ∀ assignment : Equiv.Perm (Fin 4),
    ∃ agent, ¬FeasibleEdge weight bundles agent (assignment agent)

theorem efx_permuteAllocation_iff_feasibleEdges
    (weight : Weight48)
    (bundles : Allocation (Fin 4) (Fin 8))
    (assignment : Equiv.Perm (Fin 4)) :
    EFX weight (permuteAllocation bundles assignment) ↔
      ∀ agent,
        FeasibleEdge weight bundles agent (assignment agent) := by
  constructor
  · intro efx agent targetSlot target_ne_own good good_mem
    let targetAgent := assignment.symm targetSlot
    have targetAgent_ne_agent : targetAgent ≠ agent := by
      intro equal
      apply target_ne_own
      rw [← equal]
      simp [targetAgent]
    have comparison :=
      efx agent targetAgent targetAgent_ne_agent.symm good
        (by simpa [permuteAllocation, targetAgent] using good_mem)
    simpa [permuteAllocation, targetAgent] using comparison
  · intro edges observer target observer_ne_target good good_mem
    have targetSlot_ne_own :
        assignment target ≠ assignment observer := by
      exact fun equal =>
        observer_ne_target (assignment.injective equal.symm)
    exact edges observer (assignment target) targetSlot_ne_own good
      (by simpa [permuteAllocation] using good_mem)

theorem hasFeasiblePerfectMatching_iff
    (weight : Weight48)
    (bundles : Allocation (Fin 4) (Fin 8)) :
    HasFeasiblePerfectMatching weight bundles ↔
      ∃ assignment : Equiv.Perm (Fin 4),
        EFX weight (permuteAllocation bundles assignment) := by
  constructor
  · rintro ⟨assignment, edges⟩
    exact ⟨assignment,
      (efx_permuteAllocation_iff_feasibleEdges
        weight bundles assignment).2 edges⟩
  · rintro ⟨assignment, efx⟩
    exact ⟨assignment,
      (efx_permuteAllocation_iff_feasibleEdges
        weight bundles assignment).1 efx⟩

theorem matchingObstruction_iff_not_hasFeasiblePerfectMatching
    (weight : Weight48)
    (bundles : Allocation (Fin 4) (Fin 8)) :
    MatchingObstruction weight bundles ↔
      ¬HasFeasiblePerfectMatching weight bundles := by
  simp only [MatchingObstruction, HasFeasiblePerfectMatching,
    not_exists, not_forall]

theorem valid_permuteAllocation
    (bundles : Allocation (Fin 4) (Fin 8))
    (valid : ValidAllocation bundles)
    (assignment : Equiv.Perm (Fin 4)) :
    ValidAllocation (permuteAllocation bundles assignment) :=
  permuteAllocation_valid bundles valid assignment

theorem no_matching_obstruction_of_admitsEFX
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good)
    (admits : AdmitsEFX weight) :
    ∃ bundles : Allocation (Fin 4) (Fin 8),
      ValidAllocation bundles ∧
      (∀ slot, (bundles slot).Nonempty) ∧
      HasFeasiblePerfectMatching weight bundles := by
  rcases admits with ⟨allocation, valid, efx⟩
  have nonempty :=
    allocation_nonempty_of_positive_efx_of_card_lt
      weight positive allocation valid efx (by decide)
  have permute_refl :
      permuteAllocation allocation (Equiv.refl (Fin 4)) =
        allocation := by
    funext agent
    simp [permuteAllocation]
  exact ⟨allocation, valid, nonempty, Equiv.refl (Fin 4),
    (efx_permuteAllocation_iff_feasibleEdges
      weight allocation (Equiv.refl (Fin 4))).1
      (by rw [permute_refl]; exact efx)⟩

theorem matchingObstruction_of_noEFX
    (weight : Weight48)
    (bundles : Allocation (Fin 4) (Fin 8))
    (valid : ValidAllocation bundles)
    (no_efx : ¬AdmitsEFX weight) :
    MatchingObstruction weight bundles := by
  rw [matchingObstruction_iff_not_hasFeasiblePerfectMatching]
  rintro ⟨assignment, feasible⟩
  apply no_efx
  refine ⟨permuteAllocation bundles assignment,
    valid_permuteAllocation bundles valid assignment, ?_⟩
  exact (efx_permuteAllocation_iff_feasibleEdges
    weight bundles assignment).2 feasible

theorem noEFX_of_all_valid_partitions_obstructed
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good)
    (obstructed :
      ∀ bundles : Allocation (Fin 4) (Fin 8),
        ValidAllocation bundles →
        (∀ slot, (bundles slot).Nonempty) →
        MatchingObstruction weight bundles) :
    ¬AdmitsEFX weight := by
  intro admits
  obtain ⟨bundles, valid, nonempty, matching⟩ :=
    no_matching_obstruction_of_admitsEFX weight positive admits
  exact
    ((matchingObstruction_iff_not_hasFeasiblePerfectMatching
      weight bundles).1 (obstructed bundles valid nonempty))
      matching

theorem noEFX_iff_all_valid_partitions_obstructed
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good) :
    ¬AdmitsEFX weight ↔
      ∀ bundles : Allocation (Fin 4) (Fin 8),
        ValidAllocation bundles →
        (∀ slot, (bundles slot).Nonempty) →
        MatchingObstruction weight bundles := by
  constructor
  · intro no_efx bundles valid _
    exact matchingObstruction_of_noEFX
      weight bundles valid no_efx
  · exact noEFX_of_all_valid_partitions_obstructed
      weight positive

end EFX48

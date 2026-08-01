import EFX48.PublishedInputs
import Mathlib.Data.Set.Finite.Basic

namespace EFX48

open Finset

abbrev RemainingGood {Good : Type*} (excluded : Good) :=
  {good : Good // good ≠ excluded}

abbrev RemainingAgent {Agent : Type*} (excluded : Agent) :=
  {agent : Agent // agent ≠ excluded}

def subtypeValEmbedding
    {α : Type*} (predicate : α → Prop) :
    {value : α // predicate value} ↪ α :=
  ⟨Subtype.val, Subtype.val_injective⟩

@[simp] theorem subtypeValEmbedding_apply
    {α : Type*} (predicate : α → Prop)
    (value : {item : α // predicate item}) :
    subtypeValEmbedding predicate value = value.val :=
  rfl

def restrictGoodWeight
    {Agent Good : Type*}
    (weight : Agent → Good → ℝ)
    (excluded : Good) :
    Agent → RemainingGood excluded → ℝ :=
  fun agent good => weight agent good

def liftBundle
    {Good : Type*}
    [DecidableEq Good]
    (excluded : Good)
    (bundle : Finset (RemainingGood excluded)) :
    Finset Good :=
  bundle.map
    (subtypeValEmbedding (fun good => good ≠ excluded))

theorem additiveValue_liftBundle
    {Agent Good : Type*}
    [DecidableEq Good]
    (weight : Agent → Good → ℝ)
    (excluded : Good)
    (agent : Agent)
    (bundle : Finset (RemainingGood excluded)) :
    additiveValue weight agent (liftBundle excluded bundle) =
      additiveValue (restrictGoodWeight weight excluded)
        agent bundle := by
  simp [additiveValue, liftBundle, restrictGoodWeight]

theorem liftBundle_erase
    {Good : Type*}
    [DecidableEq Good]
    (excluded : Good)
    (bundle : Finset (RemainingGood excluded))
    (good : RemainingGood excluded) :
    liftBundle excluded (bundle.erase good) =
      (liftBundle excluded bundle).erase good.val := by
  exact Finset.map_erase
    (subtypeValEmbedding (fun item => item ≠ excluded))
    bundle good

def liftGoodAllocation
    {Agent Good : Type*}
    [DecidableEq Good]
    (excluded : Good)
    (allocation : Allocation Agent (RemainingGood excluded)) :
    Allocation Agent Good :=
  fun agent => liftBundle excluded (allocation agent)

theorem liftGoodAllocation_validExcept
    {Agent Good : Type*}
    [DecidableEq Good]
    (excluded : Good)
    (allocation : Allocation Agent (RemainingGood excluded))
    (valid : ValidAllocation allocation) :
    ValidAllocationExcept
      (liftGoodAllocation excluded allocation) excluded := by
  constructor
  · intro agent
    simp [liftGoodAllocation, liftBundle, subtypeValEmbedding]
  · intro good good_ne_excluded
    let remaining : RemainingGood excluded := ⟨good, good_ne_excluded⟩
    obtain ⟨owner, owned, unique⟩ := valid remaining
    refine ⟨owner, ?_, ?_⟩
    · exact Finset.mem_map.mpr ⟨remaining, owned, rfl⟩
    · intro candidate candidate_owns
      apply unique candidate
      rcases Finset.mem_map.mp candidate_owns with
        ⟨old_good, old_owned, mapped⟩
      have old_good_eq : old_good = remaining := by
        apply Subtype.ext
        exact mapped
      simpa [old_good_eq] using old_owned

theorem liftGoodAllocation_nonempty
    {Agent Good : Type*}
    [DecidableEq Good]
    (excluded : Good)
    (allocation : Allocation Agent (RemainingGood excluded))
    (nonempty : ∀ agent, (allocation agent).Nonempty) :
    ∀ agent,
      (liftGoodAllocation excluded allocation agent).Nonempty := by
  intro agent
  change
    ((allocation agent).map
      (subtypeValEmbedding (fun good => good ≠ excluded))).Nonempty
  exact (nonempty agent).map

theorem liftGoodAllocation_efx
    {Agent Good : Type*}
    [DecidableEq Good]
    (weight : Agent → Good → ℝ)
    (excluded : Good)
    (allocation : Allocation Agent (RemainingGood excluded))
    (efx : EFX (restrictGoodWeight weight excluded) allocation) :
    EFX weight (liftGoodAllocation excluded allocation) := by
  intro observer target observer_ne_target good good_mem
  rcases Finset.mem_map.mp good_mem with
    ⟨old_good, old_good_mem, mapped⟩
  have good_eq : good = old_good.val := mapped.symm
  subst good
  have base :=
    efx observer target observer_ne_target old_good old_good_mem
  rw [← additiveValue_liftBundle
      weight excluded observer (allocation observer)] at base
  rw [← additiveValue_liftBundle
      weight excluded observer
        ((allocation target).erase old_good)] at base
  rw [liftBundle_erase] at base
  simpa [liftGoodAllocation] using base

def FourAgentSevenGoodStandardInput : Prop :=
  ∀ (Good : Type) [Fintype Good] [DecidableEq Good],
    Fintype.card Good = 7 →
    ∀ weight : Fin 4 → Good → ℝ,
      (∀ agent good, 0 < weight agent good) →
      AdmitsEFX weight

theorem fourBySevenInput_of_standard
    (standard : FourAgentSevenGoodStandardInput) :
    FourBySevenEFXInput := by
  intro weight positive excluded
  let restricted :=
    restrictGoodWeight weight excluded
  have remaining_card :
      Fintype.card (RemainingGood excluded) = 7 := by
    simpa using Set.card_ne_eq excluded
  have restricted_positive :
      ∀ agent good, 0 < restricted agent good :=
    fun agent good => positive agent good
  obtain ⟨allocation, valid, efx⟩ :=
    standard (RemainingGood excluded) remaining_card
      restricted restricted_positive
  have nonempty :
      ∀ agent, (allocation agent).Nonempty :=
    allocation_nonempty_of_positive_efx_of_card_lt
      restricted restricted_positive allocation valid efx (by
        simpa [remaining_card])
  exact ⟨liftGoodAllocation excluded allocation,
    liftGoodAllocation_validExcept excluded allocation valid,
    liftGoodAllocation_nonempty excluded allocation nonempty,
    liftGoodAllocation_efx weight excluded allocation efx⟩

def restrictAgentGoodWeight
    {Agent Good : Type*}
    (weight : Agent → Good → ℝ)
    (excludedAgent : Agent)
    (excludedGood : Good) :
    RemainingAgent excludedAgent →
      RemainingGood excludedGood → ℝ :=
  fun agent good => weight agent good

def liftAgentGoodAllocation
    {Agent Good : Type*}
    [DecidableEq Agent] [DecidableEq Good]
    (excludedAgent : Agent)
    (excludedGood : Good)
    (allocation :
      Allocation (RemainingAgent excludedAgent)
        (RemainingGood excludedGood)) :
    Allocation Agent Good :=
  fun agent =>
    if different : agent ≠ excludedAgent then
      liftBundle excludedGood (allocation ⟨agent, different⟩)
    else ∅

theorem liftAgentGoodAllocation_validExcept
    {Agent Good : Type*}
    [DecidableEq Agent] [DecidableEq Good]
    (excludedAgent : Agent)
    (excludedGood : Good)
    (allocation :
      Allocation (RemainingAgent excludedAgent)
        (RemainingGood excludedGood))
    (valid : ValidAllocation allocation) :
    ValidAllocationExcept
      (liftAgentGoodAllocation
        excludedAgent excludedGood allocation)
      excludedGood := by
  constructor
  · intro agent
    by_cases different : agent ≠ excludedAgent
    · simp [liftAgentGoodAllocation, different, liftBundle,
        subtypeValEmbedding]
    · simp [liftAgentGoodAllocation, different]
  · intro good good_ne_excluded
    let remainingGood : RemainingGood excludedGood :=
      ⟨good, good_ne_excluded⟩
    obtain ⟨owner, owned, unique⟩ := valid remainingGood
    refine ⟨owner.val, ?_, ?_⟩
    · simp only [liftAgentGoodAllocation, dif_pos owner.property]
      exact Finset.mem_map.mpr
        ⟨remainingGood, owned, rfl⟩
    · intro candidate candidate_owns
      have candidate_ne_excluded : candidate ≠ excludedAgent := by
        intro equal
        subst candidate
        simp [liftAgentGoodAllocation] at candidate_owns
      have candidate_old_owns :
          remainingGood ∈
            allocation ⟨candidate, candidate_ne_excluded⟩ := by
        simp only [liftAgentGoodAllocation,
          dif_pos candidate_ne_excluded] at candidate_owns
        rcases Finset.mem_map.mp candidate_owns with
          ⟨old_good, old_owned, mapped⟩
        have old_good_eq : old_good = remainingGood := by
          apply Subtype.ext
          exact mapped
        simpa [old_good_eq] using old_owned
      exact congrArg Subtype.val
        (unique ⟨candidate, candidate_ne_excluded⟩
          candidate_old_owns)

theorem liftAgentGoodAllocation_owner_empty
    {Agent Good : Type*}
    [DecidableEq Agent] [DecidableEq Good]
    (excludedAgent : Agent)
    (excludedGood : Good)
    (allocation :
      Allocation (RemainingAgent excludedAgent)
        (RemainingGood excludedGood)) :
    liftAgentGoodAllocation
        excludedAgent excludedGood allocation excludedAgent =
      ∅ := by
  simp [liftAgentGoodAllocation]

theorem liftAgentGoodAllocation_efxExceptObserver
    {Agent Good : Type*}
    [DecidableEq Agent] [DecidableEq Good]
    (weight : Agent → Good → ℝ)
    (excludedAgent : Agent)
    (excludedGood : Good)
    (allocation :
      Allocation (RemainingAgent excludedAgent)
        (RemainingGood excludedGood))
    (efx :
      EFX
        (restrictAgentGoodWeight
          weight excludedAgent excludedGood)
        allocation) :
    EFXExceptObserver weight
      (liftAgentGoodAllocation
        excludedAgent excludedGood allocation)
      excludedAgent := by
  intro observer observer_ne_excluded
  intro target observer_ne_target good good_mem
  by_cases target_ne_excluded : target ≠ excludedAgent
  · simp only [liftAgentGoodAllocation,
      dif_pos target_ne_excluded] at good_mem
    rcases Finset.mem_map.mp good_mem with
      ⟨old_good, old_good_mem, mapped⟩
    have good_eq : good = old_good.val := mapped.symm
    subst good
    have restricted_observer_ne_target :
        (⟨observer, observer_ne_excluded⟩ :
          RemainingAgent excludedAgent) ≠
          ⟨target, target_ne_excluded⟩ := by
      intro equal
      exact observer_ne_target (congrArg Subtype.val equal)
    have base :=
      efx ⟨observer, observer_ne_excluded⟩
        ⟨target, target_ne_excluded⟩
        restricted_observer_ne_target old_good old_good_mem
    change
      additiveValue (restrictGoodWeight weight excludedGood)
          observer
          (allocation ⟨observer, observer_ne_excluded⟩) ≥
        additiveValue (restrictGoodWeight weight excludedGood)
          observer
          ((allocation ⟨target, target_ne_excluded⟩).erase
            old_good) at base
    rw [← additiveValue_liftBundle
        weight excludedGood observer
          (allocation ⟨observer, observer_ne_excluded⟩)] at base
    rw [← additiveValue_liftBundle
        weight excludedGood observer
          ((allocation ⟨target, target_ne_excluded⟩).erase
            old_good)] at base
    rw [liftBundle_erase] at base
    simpa [liftAgentGoodAllocation,
      observer_ne_excluded, target_ne_excluded] using base
  · have target_eq : target = excludedAgent :=
      not_ne_iff.mp target_ne_excluded
    subst target
    simp [liftAgentGoodAllocation] at good_mem

def ThreeAgentSevenGoodStandardInput : Prop :=
  ∀ (Agent Good : Type)
      [Fintype Agent] [DecidableEq Agent]
      [Fintype Good] [DecidableEq Good],
    Fintype.card Agent = 3 →
    Fintype.card Good = 7 →
    ∀ weight : Agent → Good → ℝ,
      (∀ agent good, 0 < weight agent good) →
      AdmitsEFX weight

theorem threeAgentSevenGoodInput_of_standard
    (standard : ThreeAgentSevenGoodStandardInput) :
    ThreeAgentSevenGoodEFXInput := by
  intro weight positive excludedAgent excludedGood
  let restricted :=
    restrictAgentGoodWeight
      weight excludedAgent excludedGood
  have remaining_agent_card :
      Fintype.card (RemainingAgent excludedAgent) = 3 := by
    simpa using Set.card_ne_eq excludedAgent
  have remaining_good_card :
      Fintype.card (RemainingGood excludedGood) = 7 := by
    simpa using Set.card_ne_eq excludedGood
  have restricted_positive :
      ∀ agent good, 0 < restricted agent good :=
    fun agent good => positive agent good
  obtain ⟨allocation, valid, efx⟩ :=
    standard
      (RemainingAgent excludedAgent)
      (RemainingGood excludedGood)
      remaining_agent_card remaining_good_card
      restricted restricted_positive
  exact ⟨liftAgentGoodAllocation
      excludedAgent excludedGood allocation,
    liftAgentGoodAllocation_validExcept
      excludedAgent excludedGood allocation valid,
    liftAgentGoodAllocation_owner_empty
      excludedAgent excludedGood allocation,
    liftAgentGoodAllocation_efxExceptObserver
      weight excludedAgent excludedGood allocation efx⟩

theorem admitsEFX_4x8_of_standard_published_inputs
    (four_agent_seven_good :
      FourAgentSevenGoodStandardInput)
    (three_agent_seven_good :
      ThreeAgentSevenGoodStandardInput)
    (terminal_cells_unsat : EightTerminalCellsUnsat)
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good) :
    AdmitsEFX weight :=
  admitsEFX_4x8_of_verified_inputs
    (fourBySevenInput_of_standard four_agent_seven_good)
    (threeAgentSevenGoodInput_of_standard
      three_agent_seven_good)
    terminal_cells_unsat weight positive

theorem admitsEFX_4x8_of_standard_published_inputs_nonnegative
    (four_agent_seven_good :
      FourAgentSevenGoodStandardInput)
    (three_agent_seven_good :
      ThreeAgentSevenGoodStandardInput)
    (terminal_cells_unsat : EightTerminalCellsUnsat)
    (weight : Weight48)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good) :
    AdmitsEFX weight :=
  admitsEFX_4x8_of_verified_inputs_nonnegative
    (fourBySevenInput_of_standard four_agent_seven_good)
    (threeAgentSevenGoodInput_of_standard
      three_agent_seven_good)
    terminal_cells_unsat weight nonnegative

end EFX48

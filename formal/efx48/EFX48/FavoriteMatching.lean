import EFX48.Definitions
import Mathlib.Data.Fin.Embedding
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Logic.Equiv.Set

namespace EFX48

variable {Agent Good : Type*}
variable [Fintype Agent] [DecidableEq Agent]
variable [Fintype Good] [DecidableEq Good]

def pairAllocation (favorite extra : Agent → Good) :
    Allocation Agent Good :=
  fun agent => {favorite agent, extra agent}

theorem pairAllocation_nonempty
    (favorite extra : Agent → Good) :
    ∀ agent, (pairAllocation favorite extra agent).Nonempty :=
  fun agent => ⟨favorite agent, by simp [pairAllocation]⟩

theorem favorite_pair_allocation_efx
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ observer good, 0 ≤ weight observer good)
    (favorite extra : Agent → Good)
    (favorite_is_maximal : ∀ observer good,
      weight observer good ≤ weight observer (favorite observer)) :
    EFX weight (pairAllocation favorite extra) := by
  intro observer target observer_ne_target removed removed_mem
  have own_lower :
      weight observer (favorite observer) ≤
        additiveValue weight observer
          (pairAllocation favorite extra observer) := by
    by_cases same : favorite observer = extra observer
    · simp [pairAllocation, additiveValue, same]
    · simp [pairAllocation, additiveValue, same,
        nonnegative observer (extra observer)]
  have removed_cases :
      removed = favorite target ∨ removed = extra target := by
    simpa [pairAllocation] using removed_mem
  have target_upper :
      additiveValue weight observer
          ((pairAllocation favorite extra target).erase removed) ≤
        weight observer (favorite observer) := by
    rcases removed_cases with removed_favorite | removed_extra
    · subst removed
      by_cases same : favorite target = extra target
      · simp [pairAllocation, additiveValue, same,
          nonnegative observer (favorite observer)]
      · simpa [pairAllocation, additiveValue, same] using
          favorite_is_maximal observer (extra target)
    · subst removed
      by_cases same : favorite target = extra target
      · simp [pairAllocation, additiveValue, same,
          nonnegative observer (favorite observer)]
      · simpa [pairAllocation, additiveValue, same] using
          favorite_is_maximal observer (favorite target)
  exact target_upper.trans own_lower

theorem favorite_small_bundles_efx
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ observer good, 0 ≤ weight observer good)
    (allocation : Allocation Agent Good)
    (favorite : Agent → Good)
    (favorite_mem : ∀ agent, favorite agent ∈ allocation agent)
    (favorite_is_maximal : ∀ observer good,
      weight observer good ≤ weight observer (favorite observer))
    (card_le_two : ∀ agent, (allocation agent).card ≤ 2) :
    EFX weight allocation := by
  intro observer target _ removed removed_mem
  have own_lower :
      weight observer (favorite observer) ≤
        additiveValue weight observer (allocation observer) := by
    unfold additiveValue
    exact Finset.single_le_sum
      (fun good _ => nonnegative observer good)
      (favorite_mem observer)
  have erased_card_le_one :
      ((allocation target).erase removed).card ≤ 1 := by
    have target_card := card_le_two target
    rw [Finset.card_erase_of_mem removed_mem]
    omega
  have target_upper :
      additiveValue weight observer
          ((allocation target).erase removed) ≤
        weight observer (favorite observer) := by
    by_cases erased_empty :
        (allocation target).erase removed = ∅
    · simp [additiveValue, erased_empty,
        nonnegative observer (favorite observer)]
    · rcases Finset.nonempty_iff_ne_empty.mpr erased_empty with
        ⟨remaining, remaining_mem⟩
      have erased_eq :
          (allocation target).erase removed = {remaining} := by
        apply Finset.eq_singleton_iff_unique_mem.mpr
        exact ⟨remaining_mem, fun good good_mem =>
          (Finset.card_le_one_iff.mp erased_card_le_one)
            good_mem remaining_mem⟩
      simpa [additiveValue, erased_eq] using
        favorite_is_maximal observer remaining
  exact target_upper.trans own_lower

theorem admitsEFX_of_favorite_small_bundles
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ observer good, 0 ≤ weight observer good)
    (allocation : Allocation Agent Good)
    (valid : ValidAllocation allocation)
    (favorite : Agent → Good)
    (favorite_mem : ∀ agent, favorite agent ∈ allocation agent)
    (favorite_is_maximal : ∀ observer good,
      weight observer good ≤ weight observer (favorite observer))
    (card_le_two : ∀ agent, (allocation agent).card ≤ 2) :
    AdmitsEFX weight :=
  ⟨allocation, valid,
    favorite_small_bundles_efx weight nonnegative allocation favorite
      favorite_mem favorite_is_maximal card_le_two⟩

noncomputable def favoriteFiberOwner
    (favorite : Agent → Good)
    (extraOwner : ((Set.range favorite)ᶜ : Set Good) ↪ Agent)
    (good : Good) : Agent :=
  if inRange : good ∈ Set.range favorite then
    Classical.choose inRange
  else
    extraOwner ⟨good, inRange⟩

noncomputable def favoriteFiberAllocation
    (favorite : Agent → Good)
    (extraOwner : ((Set.range favorite)ᶜ : Set Good) ↪ Agent) :
    Allocation Agent Good :=
  fun agent =>
    Finset.univ.filter fun good =>
      favoriteFiberOwner favorite extraOwner good = agent

@[simp] theorem favoriteFiberOwner_favorite
    (favorite : Agent → Good)
    (favorite_injective : Function.Injective favorite)
    (extraOwner : ((Set.range favorite)ᶜ : Set Good) ↪ Agent)
    (agent : Agent) :
    favoriteFiberOwner favorite extraOwner (favorite agent) = agent := by
  unfold favoriteFiberOwner
  split
  next inRange =>
    apply favorite_injective
    exact Classical.choose_spec inRange
  next notInRange =>
    exact (notInRange ⟨agent, rfl⟩).elim

theorem favoriteFiberAllocation_valid
    (favorite : Agent → Good)
    (extraOwner : ((Set.range favorite)ᶜ : Set Good) ↪ Agent) :
    ValidAllocation (favoriteFiberAllocation favorite extraOwner) := by
  classical
  intro good
  refine ⟨favoriteFiberOwner favorite extraOwner good, ?_, ?_⟩
  · simp [favoriteFiberAllocation]
  · intro candidate candidate_mem
    have owner_eq :
        favoriteFiberOwner favorite extraOwner good = candidate := by
      simpa [favoriteFiberAllocation] using candidate_mem
    exact owner_eq.symm

@[simp] theorem favorite_mem_favoriteFiberAllocation
    (favorite : Agent → Good)
    (favorite_injective : Function.Injective favorite)
    (extraOwner : ((Set.range favorite)ᶜ : Set Good) ↪ Agent)
    (agent : Agent) :
    favorite agent ∈ favoriteFiberAllocation favorite extraOwner agent := by
  classical
  simp [favoriteFiberAllocation, favorite_injective]

theorem favoriteFiberAllocation_card_le_two
    (favorite : Agent → Good)
    (favorite_injective : Function.Injective favorite)
    (extraOwner : ((Set.range favorite)ᶜ : Set Good) ↪ Agent) :
    ∀ agent, (favoriteFiberAllocation favorite extraOwner agent).card ≤ 2 := by
  classical
  intro agent
  let allocation := favoriteFiberAllocation favorite extraOwner
  have unique_nonfavorite :
      ∀ {left right : Good},
        left ∈ allocation agent →
        right ∈ allocation agent →
        left ≠ favorite agent →
        right ≠ favorite agent →
        left = right := by
    intro left right left_mem right_mem left_ne right_ne
    have left_owner :
        favoriteFiberOwner favorite extraOwner left = agent := by
      simpa [allocation, favoriteFiberAllocation] using left_mem
    have right_owner :
        favoriteFiberOwner favorite extraOwner right = agent := by
      simpa [allocation, favoriteFiberAllocation] using right_mem
    have left_not_range : left ∉ Set.range favorite := by
      intro left_range
      rcases left_range with ⟨left_agent, rfl⟩
      have left_agent_eq : left_agent = agent := by
        simpa only [
          favoriteFiberOwner_favorite favorite favorite_injective extraOwner
        ] using left_owner
      subst left_agent
      exact left_ne rfl
    have right_not_range : right ∉ Set.range favorite := by
      intro right_range
      rcases right_range with ⟨right_agent, rfl⟩
      have right_agent_eq : right_agent = agent := by
        simpa only [
          favoriteFiberOwner_favorite favorite favorite_injective extraOwner
        ] using right_owner
      subst right_agent
      exact right_ne rfl
    have left_extra :
        extraOwner ⟨left, left_not_range⟩ = agent := by
      simpa [favoriteFiberOwner, left_not_range] using left_owner
    have right_extra :
        extraOwner ⟨right, right_not_range⟩ = agent := by
      simpa [favoriteFiberOwner, right_not_range] using right_owner
    have subtype_eq :
        (⟨left, left_not_range⟩ :
          ((Set.range favorite)ᶜ : Set Good)) =
        ⟨right, right_not_range⟩ :=
      extraOwner.injective (left_extra.trans right_extra.symm)
    exact congrArg Subtype.val subtype_eq
  have erased_card :
      ((allocation agent).erase (favorite agent)).card ≤ 1 := by
    apply Finset.card_le_one_iff.mpr
    intro left right left_mem right_mem
    exact unique_nonfavorite
      (Finset.mem_of_mem_erase left_mem)
      (Finset.mem_of_mem_erase right_mem)
      (Finset.ne_of_mem_erase left_mem)
      (Finset.ne_of_mem_erase right_mem)
  have favorite_mem :
      favorite agent ∈ allocation agent := by
    exact favorite_mem_favoriteFiberAllocation
      favorite favorite_injective extraOwner agent
  rw [Finset.card_erase_of_mem favorite_mem] at erased_card
  change (allocation agent).card ≤ 2
  omega

theorem admitsEFX_of_injective_favorites_and_extra_embedding
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ observer good, 0 ≤ weight observer good)
    (favorite : Agent → Good)
    (favorite_injective : Function.Injective favorite)
    (favorite_is_maximal : ∀ observer good,
      weight observer good ≤ weight observer (favorite observer))
    (extraOwner : ((Set.range favorite)ᶜ : Set Good) ↪ Agent) :
    AdmitsEFX weight := by
  classical
  exact admitsEFX_of_favorite_small_bundles
    weight nonnegative
    (favoriteFiberAllocation favorite extraOwner)
    (favoriteFiberAllocation_valid favorite extraOwner)
    favorite
    (favorite_mem_favoriteFiberAllocation
      favorite favorite_injective extraOwner)
    favorite_is_maximal
    (favoriteFiberAllocation_card_le_two
      favorite favorite_injective extraOwner)

theorem admitsEFX_of_injective_favorites_of_card_le_twice
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ observer good, 0 ≤ weight observer good)
    (favorite : Agent → Good)
    (favorite_injective : Function.Injective favorite)
    (favorite_is_maximal : ∀ observer good,
      weight observer good ≤ weight observer (favorite observer))
    (goods_le_twice_agents :
      Fintype.card Good ≤ 2 * Fintype.card Agent) :
    AdmitsEFX weight := by
  classical
  let favoriteEquiv : Agent ≃ Set.range favorite :=
    Equiv.ofInjective favorite favorite_injective
  have range_card :
      Fintype.card (Set.range favorite) = Fintype.card Agent := by
    exact Fintype.card_congr favoriteEquiv.symm
  have complement_le :
      Fintype.card ((Set.range favorite)ᶜ : Set Good) ≤
        Fintype.card Agent := by
    rw [Fintype.card_compl_set, range_card]
    omega
  let extraOwner :
      ((Set.range favorite)ᶜ : Set Good) ↪ Agent :=
    (Fintype.equivFin ((Set.range favorite)ᶜ : Set Good)).toEmbedding
      |>.trans (Fin.castLEEmb complement_le)
      |>.trans (Fintype.equivFin Agent).symm.toEmbedding
  exact admitsEFX_of_injective_favorites_and_extra_embedding
    weight nonnegative favorite favorite_injective favorite_is_maximal
    extraOwner

def favoritePairAllocation (pairing : (Agent ⊕ Agent) ≃ Good) :
    Allocation Agent Good :=
  pairAllocation
    (fun agent => pairing (Sum.inl agent))
    (fun agent => pairing (Sum.inr agent))

theorem favoritePairAllocation_valid
    (pairing : (Agent ⊕ Agent) ≃ Good) :
    ValidAllocation (favoritePairAllocation pairing) := by
  intro good
  cases tag_eq : pairing.symm good with
  | inl owner =>
      have good_eq : good = pairing (Sum.inl owner) := by
        rw [← pairing.apply_symm_apply good, tag_eq]
      refine ⟨owner, ?_, ?_⟩
      · simp [favoritePairAllocation, pairAllocation, good_eq]
      · intro candidate candidate_owns
        have cases :
            good = pairing (Sum.inl candidate) ∨
              good = pairing (Sum.inr candidate) := by
          simpa [favoritePairAllocation, pairAllocation] using candidate_owns
        rcases cases with favorite_case | extra_case
        · have tags := congrArg pairing.symm favorite_case
          simp only [pairing.symm_apply_apply] at tags
          rw [tag_eq] at tags
          exact (Sum.inl_injective tags).symm
        · have tags := congrArg pairing.symm extra_case
          simp only [pairing.symm_apply_apply] at tags
          rw [tag_eq] at tags
          exact (Sum.inl_ne_inr tags).elim
  | inr owner =>
      have good_eq : good = pairing (Sum.inr owner) := by
        rw [← pairing.apply_symm_apply good, tag_eq]
      refine ⟨owner, ?_, ?_⟩
      · simp [favoritePairAllocation, pairAllocation, good_eq]
      · intro candidate candidate_owns
        have cases :
            good = pairing (Sum.inl candidate) ∨
              good = pairing (Sum.inr candidate) := by
          simpa [favoritePairAllocation, pairAllocation] using candidate_owns
        rcases cases with favorite_case | extra_case
        · have tags := congrArg pairing.symm favorite_case
          simp only [pairing.symm_apply_apply] at tags
          rw [tag_eq] at tags
          exact (Sum.inr_ne_inl tags).elim
        · have tags := congrArg pairing.symm extra_case
          simp only [pairing.symm_apply_apply] at tags
          rw [tag_eq] at tags
          exact (Sum.inr_injective tags).symm

theorem favorite_matching_allocation
    (weight : Agent → Good → ℝ)
    (nonnegative : ∀ observer good, 0 ≤ weight observer good)
    (pairing : (Agent ⊕ Agent) ≃ Good)
    (matched_favorite_is_maximal : ∀ observer good,
      weight observer good ≤
        weight observer (pairing (Sum.inl observer))) :
    ValidAllocation (favoritePairAllocation pairing) ∧
      EFX weight (favoritePairAllocation pairing) := by
  refine ⟨favoritePairAllocation_valid pairing, ?_⟩
  exact favorite_pair_allocation_efx weight nonnegative
    (fun agent => pairing (Sum.inl agent))
    (fun agent => pairing (Sum.inr agent))
    matched_favorite_is_maximal

theorem favorite_injection_allocation_4x8
    (weight : Fin 4 → Fin 8 → ℝ)
    (nonnegative : ∀ observer good, 0 ≤ weight observer good)
    (favorite : Fin 4 → Fin 8)
    (favorite_injective : Function.Injective favorite)
    (favorite_is_maximal : ∀ observer good,
      weight observer good ≤ weight observer (favorite observer)) :
    AdmitsEFX weight := by
  classical
  let favoriteEquiv : Fin 4 ≃ Set.range favorite :=
    Equiv.ofInjective favorite favorite_injective
  have range_card :
      Fintype.card (Set.range favorite) = 4 := by
    rw [← Fintype.card_congr favoriteEquiv]
    simp
  have complement_card :
      Fintype.card ((Set.range favorite)ᶜ : Set (Fin 8)) = 4 := by
    rw [Fintype.card_compl_set, range_card]
    decide
  let extraEquiv :
      Fin 4 ≃ ((Set.range favorite)ᶜ : Set (Fin 8)) :=
    Fintype.equivOfCardEq (by
      simpa using complement_card.symm)
  let pairing : (Fin 4 ⊕ Fin 4) ≃ Fin 8 :=
    (Equiv.sumCongr favoriteEquiv extraEquiv).trans
      (Equiv.Set.sumCompl (Set.range favorite))
  have pairing_favorite : ∀ agent,
      pairing (Sum.inl agent) = favorite agent := by
    intro agent
    simp [pairing, favoriteEquiv]
  rcases favorite_matching_allocation weight nonnegative pairing
      (by
        intro observer good
        rw [pairing_favorite]
        exact favorite_is_maximal observer good) with
    ⟨valid, efx⟩
  exact ⟨favoritePairAllocation pairing, valid, efx⟩

end EFX48

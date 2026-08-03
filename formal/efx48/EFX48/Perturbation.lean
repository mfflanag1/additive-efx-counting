import EFX48.Definitions
import Mathlib.Data.Fintype.Pi
import Mathlib.Tactic.FunProp
import Mathlib.Topology.Algebra.Ring.Real
import Mathlib.Topology.Constructions
import Mathlib.Topology.Order

namespace EFX48

abbrev Weight48 := Fin 4 → Fin 8 → ℝ

structure EFXComparison
    (allocation : Allocation (Fin 4) (Fin 8)) where
  observer : Fin 4
  target : Fin 4
  observer_ne_target : observer ≠ target
  good : Fin 8
  good_mem : good ∈ allocation target

theorem efx_iff_comparisons
    (weight : Weight48)
    (allocation : Allocation (Fin 4) (Fin 8)) :
    EFX weight allocation ↔
      ∀ comparison : EFXComparison allocation,
        additiveValue weight comparison.observer
            ((allocation comparison.target).erase comparison.good) ≤
          additiveValue weight comparison.observer
            (allocation comparison.observer) := by
  constructor
  · intro efx comparison
    exact efx comparison.observer comparison.target
      comparison.observer_ne_target comparison.good
      comparison.good_mem
  · intro comparisons observer target observer_ne_target good good_mem
    exact comparisons
      ⟨observer, target, observer_ne_target, good, good_mem⟩

theorem continuous_additiveValue_4x8
    (observer : Fin 4) (bundle : Finset (Fin 8)) :
    Continuous
      (fun weight : Weight48 =>
        additiveValue weight observer bundle) := by
  unfold additiveValue
  fun_prop

theorem isClosed_efx_set
    (allocation : Allocation (Fin 4) (Fin 8)) :
    IsClosed {weight : Weight48 | EFX weight allocation} := by
  have set_eq :
      {weight : Weight48 | EFX weight allocation} =
        ⋂ comparison : EFXComparison allocation,
          {weight : Weight48 |
            additiveValue weight comparison.observer
                ((allocation comparison.target).erase comparison.good) ≤
              additiveValue weight comparison.observer
                (allocation comparison.observer)} := by
    ext weight
    simp only [Set.mem_setOf_eq, Set.mem_iInter]
    exact efx_iff_comparisons weight allocation
  rw [set_eq]
  apply isClosed_iInter
  intro comparison
  exact isClosed_le
    (continuous_additiveValue_4x8 comparison.observer
      ((allocation comparison.target).erase comparison.good))
    (continuous_additiveValue_4x8 comparison.observer
      (allocation comparison.observer))

theorem isClosed_admitsEFX_set :
    IsClosed {weight : Weight48 | AdmitsEFX weight} := by
  classical
  let candidate :
      Allocation (Fin 4) (Fin 8) → Set Weight48 :=
    fun allocation =>
      if ValidAllocation allocation then
        {weight | EFX weight allocation}
      else ∅
  have set_eq :
      {weight : Weight48 | AdmitsEFX weight} =
        ⋃ allocation, candidate allocation := by
    ext weight
    simp only [Set.mem_setOf_eq, Set.mem_iUnion]
    constructor
    · rintro ⟨allocation, valid, efx⟩
      refine ⟨allocation, ?_⟩
      simp [candidate, valid, efx]
    · rintro ⟨allocation, member⟩
      by_cases valid : ValidAllocation allocation
      · refine ⟨allocation, valid, ?_⟩
        simpa [candidate, valid] using member
      · simpa [candidate, valid] using member
  rw [set_eq]
  apply isClosed_iUnion_of_finite
  intro allocation
  by_cases valid : ValidAllocation allocation
  · simpa [candidate, valid] using isClosed_efx_set allocation
  · simp [candidate, valid]

theorem isOpen_noEFX_set :
    IsOpen {weight : Weight48 | ¬AdmitsEFX weight} := by
  have complement_eq :
      {weight : Weight48 | ¬AdmitsEFX weight} =
        ({weight : Weight48 | AdmitsEFX weight})ᶜ := by
    ext weight
    simp
  rw [complement_eq]
  exact isClosed_admitsEFX_set.isOpen_compl

def uniformPerturb
    (weight : Weight48) (time : ℝ) : Weight48 :=
  fun agent good => weight agent good + time

theorem continuous_uniformPerturb
    (weight : Weight48) :
    Continuous (uniformPerturb weight) := by
  unfold uniformPerturb
  fun_prop

theorem exists_positive_noEFX_perturbation
    (weight : Weight48)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (no_efx : ¬AdmitsEFX weight) :
    ∃ perturbed : Weight48,
      (∀ agent good, 0 < perturbed agent good) ∧
      ¬AdmitsEFX perturbed := by
  let noEFX : Set Weight48 :=
    {candidate | ¬AdmitsEFX candidate}
  let path : ℝ → Weight48 :=
    uniformPerturb weight
  have open_preimage :
      IsOpen (path ⁻¹' noEFX) :=
    isOpen_noEFX_set.preimage
      (continuous_uniformPerturb weight)
  have zero_mem : (0 : ℝ) ∈ path ⁻¹' noEFX := by
    change ¬AdmitsEFX (uniformPerturb weight 0)
    have perturb_zero : uniformPerturb weight 0 = weight := by
      funext agent good
      simp [uniformPerturb]
    rw [perturb_zero]
    exact no_efx
  obtain ⟨radius, radius_positive, ball_subset⟩ :=
    (Metric.isOpen_iff.mp open_preimage) 0 zero_mem
  let time := radius / 2
  have time_positive : 0 < time := by
    exact half_pos radius_positive
  have time_lt_radius : time < radius := by
    exact half_lt_self radius_positive
  refine ⟨path time, ?_, ?_⟩
  · intro agent good
    dsimp [path, uniformPerturb]
    exact add_pos_of_nonneg_of_pos
      (nonnegative agent good) time_positive
  · apply ball_subset
    simpa [Real.dist_eq, abs_of_pos time_positive] using
      time_lt_radius

end EFX48

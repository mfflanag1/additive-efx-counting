import EFX48.Normalization
import EFX48.Perturbation
import EFX48.RankingCells
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Finset.BooleanAlgebra
import Mathlib.Data.Finset.Max
import Mathlib.Data.Set.Finite.Basic
import Mathlib.Order.Interval.Set.Infinite

namespace EFX48

open Finset

def rankPerturb
    (weight : Weight48) (time : ℝ) : Weight48 :=
  fun agent good =>
    weight agent good + time * (good.val : ℝ)

noncomputable def rankingBadTime
    (weight : Weight48)
    (agent : Fin 4) (first second : Fin 8) : ℝ :=
  (weight agent second - weight agent first) /
    ((first.val : ℝ) - (second.val : ℝ))

noncomputable def rankingBadTimes
    (weight : Weight48) : Finset ℝ :=
  Finset.univ.image
    (fun index : (Fin 4 × Fin 8) × Fin 8 =>
      rankingBadTime weight index.1.1 index.1.2 index.2)

theorem continuous_rankPerturb
    (weight : Weight48) :
    Continuous (rankPerturb weight) := by
  unfold rankPerturb
  fun_prop

theorem equal_rankPerturb_coordinates_bad
    (weight : Weight48) (time : ℝ)
    (agent : Fin 4) (first second : Fin 8)
    (different : first ≠ second)
    (equal :
      rankPerturb weight time agent first =
        rankPerturb weight time agent second) :
    time = rankingBadTime weight agent first second := by
  have val_ne : (first.val : ℝ) ≠ (second.val : ℝ) := by
    exact_mod_cast (fun equalVals => different (Fin.ext equalVals))
  have denominator_ne :
      (first.val : ℝ) - (second.val : ℝ) ≠ 0 :=
    sub_ne_zero.mpr val_ne
  apply (eq_div_iff denominator_ne).2
  simp only [rankPerturb] at equal
  linarith

theorem exists_positive_noEFX_row_injective_perturbation
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good)
    (no_efx : ¬AdmitsEFX weight) :
    ∃ perturbed : Weight48,
      (∀ agent good, 0 < perturbed agent good) ∧
      ¬AdmitsEFX perturbed ∧
      ∀ agent, Function.Injective (perturbed agent) := by
  let noEFX : Set Weight48 :=
    {candidate | ¬AdmitsEFX candidate}
  let path : ℝ → Weight48 :=
    rankPerturb weight
  have open_preimage :
      IsOpen (path ⁻¹' noEFX) :=
    isOpen_noEFX_set.preimage
      (continuous_rankPerturb weight)
  have zero_mem : (0 : ℝ) ∈ path ⁻¹' noEFX := by
    change ¬AdmitsEFX (rankPerturb weight 0)
    have rank_zero : rankPerturb weight 0 = weight := by
      funext agent good
      simp [rankPerturb]
    rw [rank_zero]
    exact no_efx
  obtain ⟨radius, radius_positive, ball_subset⟩ :=
    (Metric.isOpen_iff.mp open_preimage) 0 zero_mem
  obtain ⟨time, time_interval, time_not_bad⟩ :=
    (Set.Ioo_infinite radius_positive).exists_notMem_finset
      (rankingBadTimes weight)
  refine ⟨path time, ?_, ?_, ?_⟩
  · intro agent good
    dsimp [path, rankPerturb]
    have good_nonnegative : 0 ≤ (good.val : ℝ) := by positivity
    exact add_pos_of_pos_of_nonneg
      (positive agent good)
      (mul_nonneg time_interval.1.le good_nonnegative)
  · apply ball_subset
    simpa [Real.dist_eq, abs_of_pos time_interval.1] using
      time_interval.2
  · intro agent first second equal
    by_contra different
    apply time_not_bad
    apply Finset.mem_image.mpr
    refine ⟨((agent, first), second), Finset.mem_univ _, ?_⟩
    exact (equal_rankPerturb_coordinates_bad
      weight time agent first second different equal).symm

noncomputable def favoriteOf
    (weight : Weight48) (agent : Fin 4) : Fin 8 :=
  Classical.choose
    (Finset.exists_max_image Finset.univ (weight agent)
      Finset.univ_nonempty)

theorem favoriteOf_max
    (weight : Weight48) (agent : Fin 4) (good : Fin 8) :
    weight agent good ≤ weight agent (favoriteOf weight agent) := by
  exact (Classical.choose_spec
    (Finset.exists_max_image Finset.univ (weight agent)
      Finset.univ_nonempty)).2 good (Finset.mem_univ good)

noncomputable def secondOf
    (weight : Weight48) (agent : Fin 4) : Fin 8 :=
  Classical.choose
    (Finset.exists_max_image
      (Finset.univ.erase (favoriteOf weight agent))
      (weight agent)
      Finset.univ_nontrivial.erase_nonempty)

theorem secondOf_mem_erase
    (weight : Weight48) (agent : Fin 4) :
    secondOf weight agent ∈
      Finset.univ.erase (favoriteOf weight agent) := by
  exact (Classical.choose_spec
    (Finset.exists_max_image
      (Finset.univ.erase (favoriteOf weight agent))
      (weight agent)
      Finset.univ_nontrivial.erase_nonempty)).1

theorem secondOf_ne_favoriteOf
    (weight : Weight48) (agent : Fin 4) :
    secondOf weight agent ≠ favoriteOf weight agent :=
  Finset.ne_of_mem_erase (secondOf_mem_erase weight agent)

theorem secondOf_max_except_favorite
    (weight : Weight48) (agent : Fin 4) (good : Fin 8)
    (not_favorite : good ≠ favoriteOf weight agent) :
    weight agent good ≤ weight agent (secondOf weight agent) := by
  exact (Classical.choose_spec
    (Finset.exists_max_image
      (Finset.univ.erase (favoriteOf weight agent))
      (weight agent)
      Finset.univ_nontrivial.erase_nonempty)).2
        good (Finset.mem_erase.mpr
          ⟨not_favorite, Finset.mem_univ good⟩)

theorem strictRankingPrefix_favoriteOf_secondOf
    (weight : Weight48)
    (row_injective : ∀ agent, Function.Injective (weight agent)) :
    StrictRankingPrefix weight (favoriteOf weight) (secondOf weight) := by
  refine ⟨?_, secondOf_ne_favoriteOf weight, ?_⟩
  · intro agent good not_favorite
    have not_equal :
        weight agent good ≠
          weight agent (favoriteOf weight agent) := by
      intro equal
      exact not_favorite (row_injective agent equal)
    exact lt_of_le_of_ne
      (favoriteOf_max weight agent good) not_equal
  · intro agent good not_favorite not_second
    have not_equal :
        weight agent good ≠
          weight agent (secondOf weight agent) := by
      intro equal
      exact not_second (row_injective agent equal)
    exact lt_of_le_of_ne
      (secondOf_max_except_favorite
        weight agent good not_favorite)
      not_equal

theorem positive_noEFX_has_strict_ranking_counterexample
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good)
    (no_efx : ¬AdmitsEFX weight) :
    ∃ perturbed : Weight48,
      (∀ agent good, 0 < perturbed agent good) ∧
      ¬AdmitsEFX perturbed ∧
      StrictRankingPrefix perturbed
        (favoriteOf perturbed) (secondOf perturbed) := by
  obtain ⟨perturbed, perturbed_positive,
      perturbed_no_efx, row_injective⟩ :=
    exists_positive_noEFX_row_injective_perturbation
      weight positive no_efx
  exact ⟨perturbed, perturbed_positive, perturbed_no_efx,
    strictRankingPrefix_favoriteOf_secondOf
      perturbed row_injective⟩

theorem positive_noEFX_has_normalized_strict_ranking_counterexample
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good)
    (no_efx : ¬AdmitsEFX weight) :
    ∃ normalized : Weight48,
      (∀ agent good, 0 < normalized agent good) ∧
      (∀ agent, ∑ good, normalized agent good = 1) ∧
      ¬AdmitsEFX normalized ∧
      StrictRankingPrefix normalized
        (favoriteOf normalized) (secondOf normalized) := by
  obtain ⟨perturbed, perturbed_positive,
      perturbed_no_efx, perturbed_row_injective⟩ :=
    exists_positive_noEFX_row_injective_perturbation
      weight positive no_efx
  let normalized := normalizeRows perturbed
  have normalized_positive :=
    normalizeRows_positive perturbed perturbed_positive
  have normalized_no_efx : ¬AdmitsEFX normalized := by
    intro normalized_efx
    exact perturbed_no_efx
      ((admitsEFX_normalizeRows_iff
        perturbed perturbed_positive).mp normalized_efx)
  have row_injective :
      ∀ agent, Function.Injective (normalized agent) := by
    intro agent first second equal
    have total_positive :=
      rowTotal_positive perturbed perturbed_positive agent
    dsimp [normalized, normalizeRows] at equal
    exact perturbed_row_injective agent
      ((div_left_inj' (ne_of_gt total_positive)).mp equal)
  exact ⟨normalized, normalized_positive,
    normalizeRows_sum_one perturbed perturbed_positive,
    normalized_no_efx,
    strictRankingPrefix_favoriteOf_secondOf
      normalized row_injective⟩

def LiesInEightCell
    (weight : Weight48) : Prop :=
  RelabelsIntoFavoriteCell weight canonical211 ∨
  RelabelsIntoFavoriteCell weight canonical31 ∨
  RelabelsIntoFavoriteCell weight canonical22 ∨
  RelabelsIntoSecondCell weight second1111 ∨
  RelabelsIntoSecondCell weight second4 ∨
  RelabelsIntoSecondCell weight second31 ∨
  RelabelsIntoSecondCell weight second22 ∨
  RelabelsIntoSecondCell weight second211

theorem positive_noEFX_reduces_to_normalized_eight_cells
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good)
    (no_efx : ¬AdmitsEFX weight) :
    ∃ normalized : Weight48,
      (∀ agent good, 0 < normalized agent good) ∧
      (∀ agent, ∑ good, normalized agent good = 1) ∧
      ¬AdmitsEFX normalized ∧
      LiesInEightCell normalized := by
  obtain ⟨normalized, normalized_positive, normalized_sum,
      normalized_no_efx, normalized_strict⟩ :=
    positive_noEFX_has_normalized_strict_ranking_counterexample
      weight positive no_efx
  refine ⟨normalized, normalized_positive, normalized_sum,
    normalized_no_efx, ?_⟩
  exact strict_counterexample_eight_cell_coverage
    normalized
    (fun agent good => (normalized_positive agent good).le)
    (favoriteOf normalized) (secondOf normalized)
    normalized_strict normalized_no_efx

def normalizedPerturbDirection : Weight48 :=
  fun agent good =>
    2 * (good.val : ℝ) - 7 +
      (if good = 0 then 20 * (agent.val : ℝ)
       else if good = 1 then -20 * (agent.val : ℝ)
       else 0)

set_option maxRecDepth 10000 in
theorem normalizedPerturbDirection_sum_zero :
    ∀ agent, ∑ good, normalizedPerturbDirection agent good = 0 := by
  intro agent
  fin_cases agent
  all_goals
    rw [Fin.sum_univ_eight]
    simp +decide [normalizedPerturbDirection]
    norm_num

theorem normalizedPerturbDirection_row_injective :
    ∀ agent,
      Function.Injective (normalizedPerturbDirection agent) := by
  intro agent first second equal
  fin_cases agent <;> fin_cases first <;> fin_cases second
  all_goals
    norm_num [normalizedPerturbDirection, Fin.ext_iff] at *

theorem normalizedPerturbDirection_good_zero_agent_injective :
    Function.Injective
      (fun agent : Fin 4 => normalizedPerturbDirection agent 0) := by
  intro first second equal
  fin_cases first <;> fin_cases second
  all_goals
    norm_num [normalizedPerturbDirection, Fin.ext_iff] at *

def normalizedPerturb
    (weight : Weight48) (time : ℝ) : Weight48 :=
  fun agent good =>
    weight agent good +
      time * normalizedPerturbDirection agent good

noncomputable def normalizedCoordinateBadTime
    (weight : Weight48)
    (left right : Fin 4 × Fin 8) : ℝ :=
  (weight right.1 right.2 - weight left.1 left.2) /
    (normalizedPerturbDirection left.1 left.2 -
      normalizedPerturbDirection right.1 right.2)

noncomputable def normalizedCoordinateBadTimes
    (weight : Weight48) : Finset ℝ :=
  Finset.univ.image
    (fun pair : (Fin 4 × Fin 8) × (Fin 4 × Fin 8) =>
      normalizedCoordinateBadTime weight pair.1 pair.2)

theorem continuous_normalizedPerturb
    (weight : Weight48) :
    Continuous (normalizedPerturb weight) := by
  unfold normalizedPerturb
  fun_prop

theorem normalizedPerturb_sum
    (weight : Weight48) (time : ℝ)
    (row_sum : ∀ agent, ∑ good, weight agent good = 1) :
    ∀ agent, ∑ good, normalizedPerturb weight time agent good = 1 := by
  intro agent
  simp only [normalizedPerturb, Finset.sum_add_distrib,
    ← Finset.mul_sum]
  rw [row_sum, normalizedPerturbDirection_sum_zero]
  ring

theorem equal_normalizedPerturb_coordinates_bad
    (weight : Weight48) (time : ℝ)
    (left right : Fin 4 × Fin 8)
    (direction_different :
      normalizedPerturbDirection left.1 left.2 ≠
        normalizedPerturbDirection right.1 right.2)
    (equal :
      normalizedPerturb weight time left.1 left.2 =
        normalizedPerturb weight time right.1 right.2) :
    time = normalizedCoordinateBadTime weight left right := by
  have denominator_ne :
      normalizedPerturbDirection left.1 left.2 -
          normalizedPerturbDirection right.1 right.2 ≠ 0 :=
    sub_ne_zero.mpr direction_different
  apply (eq_div_iff denominator_ne).2
  simp only [normalizedPerturb] at equal
  linarith

theorem isOpen_positiveWeight48_set :
    IsOpen {weight : Weight48 |
      ∀ agent good, 0 < weight agent good} := by
  have set_eq :
      {weight : Weight48 | ∀ agent good, 0 < weight agent good} =
        ⋂ agent, ⋂ good,
          {weight : Weight48 | 0 < weight agent good} := by
    ext weight
    simp
  rw [set_eq]
  apply isOpen_iInter_of_finite
  intro agent
  apply isOpen_iInter_of_finite
  intro good
  exact isOpen_lt continuous_const
    ((continuous_apply good).comp (continuous_apply agent))

theorem exists_generic_normalized_noEFX_perturbation
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good)
    (row_sum : ∀ agent, ∑ good, weight agent good = 1)
    (no_efx : ¬AdmitsEFX weight) :
    ∃ perturbed : Weight48,
      (∀ agent good, 0 < perturbed agent good) ∧
      (∀ agent, ∑ good, perturbed agent good = 1) ∧
      ¬AdmitsEFX perturbed ∧
      (∀ agent, Function.Injective (perturbed agent)) ∧
      Function.Injective perturbed := by
  let safe : Set Weight48 :=
    {candidate | ∀ agent good, 0 < candidate agent good} ∩
      {candidate | ¬AdmitsEFX candidate}
  let path : ℝ → Weight48 :=
    normalizedPerturb weight
  have safe_open : IsOpen safe :=
    isOpen_positiveWeight48_set.inter isOpen_noEFX_set
  have open_preimage :
      IsOpen (path ⁻¹' safe) :=
    safe_open.preimage (continuous_normalizedPerturb weight)
  have zero_mem : (0 : ℝ) ∈ path ⁻¹' safe := by
    change
      (∀ agent good, 0 < normalizedPerturb weight 0 agent good) ∧
      ¬AdmitsEFX (normalizedPerturb weight 0)
    have perturb_zero : normalizedPerturb weight 0 = weight := by
      funext agent good
      simp [normalizedPerturb]
    rw [perturb_zero]
    exact ⟨positive, no_efx⟩
  obtain ⟨radius, radius_positive, ball_subset⟩ :=
    (Metric.isOpen_iff.mp open_preimage) 0 zero_mem
  obtain ⟨time, time_interval, time_not_bad⟩ :=
    (Set.Ioo_infinite radius_positive).exists_notMem_finset
      (normalizedCoordinateBadTimes weight)
  have safe_time : path time ∈ safe := by
    apply ball_subset
    simpa [Real.dist_eq, abs_of_pos time_interval.1] using
      time_interval.2
  refine ⟨path time, safe_time.1,
    normalizedPerturb_sum weight time row_sum,
    safe_time.2, ?_, ?_⟩
  · intro agent first second equal
    by_contra different
    apply time_not_bad
    apply Finset.mem_image.mpr
    refine ⟨((agent, first), (agent, second)),
      Finset.mem_univ _, ?_⟩
    exact (equal_normalizedPerturb_coordinates_bad
      weight time (agent, first) (agent, second)
      (fun direction_equal =>
        different
          (normalizedPerturbDirection_row_injective
            agent direction_equal))
      equal).symm
  · intro firstAgent secondAgent rows_equal
    by_contra different
    have coordinate_equal :
        path time firstAgent 0 =
          path time secondAgent 0 := by
      exact congrFun rows_equal 0
    apply time_not_bad
    apply Finset.mem_image.mpr
    refine ⟨((firstAgent, 0), (secondAgent, 0)),
      Finset.mem_univ _, ?_⟩
    exact (equal_normalizedPerturb_coordinates_bad
      weight time (firstAgent, 0) (secondAgent, 0)
      (fun direction_equal =>
        different
          (normalizedPerturbDirection_good_zero_agent_injective
            direction_equal))
      coordinate_equal).symm

theorem positive_noEFX_has_fully_generic_normalized_counterexample
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good)
    (no_efx : ¬AdmitsEFX weight) :
    ∃ generic : Weight48,
      (∀ agent good, 0 < generic agent good) ∧
      (∀ agent, ∑ good, generic agent good = 1) ∧
      ¬AdmitsEFX generic ∧
      Function.Injective generic ∧
      StrictRankingPrefix generic
        (favoriteOf generic) (secondOf generic) := by
  let normalized := normalizeRows weight
  have normalized_positive :=
    normalizeRows_positive weight positive
  have normalized_sum :=
    normalizeRows_sum_one weight positive
  have normalized_no_efx : ¬AdmitsEFX normalized := by
    intro normalized_efx
    exact no_efx
      ((admitsEFX_normalizeRows_iff weight positive).mp normalized_efx)
  obtain ⟨generic, generic_positive, generic_sum, generic_no_efx,
      row_injective, rows_injective⟩ :=
    exists_generic_normalized_noEFX_perturbation
      normalized normalized_positive normalized_sum normalized_no_efx
  exact ⟨generic, generic_positive, generic_sum, generic_no_efx,
    rows_injective,
    strictRankingPrefix_favoriteOf_secondOf generic row_injective⟩

theorem positive_noEFX_reduces_to_generic_normalized_eight_cells
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good)
    (no_efx : ¬AdmitsEFX weight) :
    ∃ generic : Weight48,
      (∀ agent good, 0 < generic agent good) ∧
      (∀ agent, ∑ good, generic agent good = 1) ∧
      ¬AdmitsEFX generic ∧
      Function.Injective generic ∧
      LiesInEightCell generic := by
  obtain ⟨generic, generic_positive, generic_sum,
      generic_no_efx, rows_injective, generic_strict⟩ :=
    positive_noEFX_has_fully_generic_normalized_counterexample
      weight positive no_efx
  refine ⟨generic, generic_positive, generic_sum,
    generic_no_efx, rows_injective, ?_⟩
  exact strict_counterexample_eight_cell_coverage
    generic
    (fun agent good => (generic_positive agent good).le)
    (favoriteOf generic) (secondOf generic)
    generic_strict generic_no_efx

end EFX48

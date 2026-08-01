import EFX48.Definitions
import Mathlib.Algebra.BigOperators.Field

namespace EFX48

open Finset

variable {Agent Good : Type*}
variable [Fintype Agent] [DecidableEq Agent]
variable [Fintype Good] [DecidableEq Good]

def scaleRows
    (weight : Agent → Good → ℝ)
    (scale : Agent → ℝ) : Agent → Good → ℝ :=
  fun agent good => scale agent * weight agent good

theorem additiveValue_scaleRows
    (weight : Agent → Good → ℝ)
    (scale : Agent → ℝ)
    (agent : Agent) (bundle : Finset Good) :
    additiveValue (scaleRows weight scale) agent bundle =
      scale agent * additiveValue weight agent bundle := by
  simp [additiveValue, scaleRows, Finset.mul_sum]

theorem efx_scaleRows_iff
    (weight : Agent → Good → ℝ)
    (scale : Agent → ℝ)
    (positive_scale : ∀ agent, 0 < scale agent)
    (allocation : Allocation Agent Good) :
    EFX (scaleRows weight scale) allocation ↔
      EFX weight allocation := by
  constructor
  · intro scaled observer target observer_ne_target good good_mem
    have comparison :=
      scaled observer target observer_ne_target good good_mem
    rw [additiveValue_scaleRows, additiveValue_scaleRows] at comparison
    exact le_of_mul_le_mul_left comparison (positive_scale observer)
  · intro original observer target observer_ne_target good good_mem
    rw [additiveValue_scaleRows, additiveValue_scaleRows]
    exact mul_le_mul_of_nonneg_left
      (original observer target observer_ne_target good good_mem)
      (positive_scale observer).le

theorem admitsEFX_scaleRows_iff
    (weight : Agent → Good → ℝ)
    (scale : Agent → ℝ)
    (positive_scale : ∀ agent, 0 < scale agent) :
    AdmitsEFX (scaleRows weight scale) ↔ AdmitsEFX weight := by
  constructor
  · rintro ⟨allocation, valid, efx⟩
    exact ⟨allocation, valid,
      (efx_scaleRows_iff weight scale positive_scale allocation).mp efx⟩
  · rintro ⟨allocation, valid, efx⟩
    exact ⟨allocation, valid,
      (efx_scaleRows_iff weight scale positive_scale allocation).mpr efx⟩

def rowTotal
    (weight : Agent → Good → ℝ) (agent : Agent) : ℝ :=
  ∑ good, weight agent good

noncomputable def normalizeRows
    (weight : Agent → Good → ℝ) : Agent → Good → ℝ :=
  fun agent good => weight agent good / rowTotal weight agent

theorem rowTotal_positive
    [Nonempty Good]
    (weight : Agent → Good → ℝ)
    (positive : ∀ agent good, 0 < weight agent good) :
    ∀ agent, 0 < rowTotal weight agent := by
  intro agent
  unfold rowTotal
  exact Finset.sum_pos
    (fun good _ => positive agent good)
    Finset.univ_nonempty

theorem normalizeRows_eq_scaleRows
    (weight : Agent → Good → ℝ) :
    normalizeRows weight =
      scaleRows weight (fun agent => (rowTotal weight agent)⁻¹) := by
  funext agent good
  simp [normalizeRows, scaleRows, div_eq_inv_mul]

theorem normalizeRows_positive
    [Nonempty Good]
    (weight : Agent → Good → ℝ)
    (positive : ∀ agent good, 0 < weight agent good) :
    ∀ agent good, 0 < normalizeRows weight agent good := by
  intro agent good
  exact div_pos (positive agent good)
    (rowTotal_positive weight positive agent)

theorem normalizeRows_sum_one
    [Nonempty Good]
    (weight : Agent → Good → ℝ)
    (positive : ∀ agent good, 0 < weight agent good) :
    ∀ agent, ∑ good, normalizeRows weight agent good = 1 := by
  intro agent
  simp only [normalizeRows, ← Finset.sum_div]
  exact div_self (ne_of_gt (rowTotal_positive weight positive agent))

theorem admitsEFX_normalizeRows_iff
    [Nonempty Good]
    (weight : Agent → Good → ℝ)
    (positive : ∀ agent good, 0 < weight agent good) :
    AdmitsEFX (normalizeRows weight) ↔ AdmitsEFX weight := by
  rw [normalizeRows_eq_scaleRows]
  exact admitsEFX_scaleRows_iff weight
    (fun agent => (rowTotal weight agent)⁻¹)
    (fun agent => inv_pos.mpr
      (rowTotal_positive weight positive agent))

end EFX48

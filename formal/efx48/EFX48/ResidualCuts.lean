import EFX48.StrictPerturbation

namespace EFX48

open Finset

def UniversalMinimum
    (weight : Weight48) : Prop :=
  ∃ good, ∀ agent other,
    weight agent good ≤ weight agent other

def NoUniversalMinimum
    (weight : Weight48) : Prop :=
  ∀ good, ∃ agent other,
    other ≠ good ∧ weight agent other < weight agent good

def Peelable
    (weight : Weight48) : Prop :=
  ∃ agent good,
    ∀ removed ∈ Finset.univ.erase good,
      additiveValue weight agent
          ((Finset.univ.erase good).erase removed) ≤
        weight agent good

def NoPeelable
    (weight : Weight48) : Prop :=
  ∀ agent good, ∃ removed ∈ Finset.univ.erase good,
    weight agent good <
      additiveValue weight agent
        ((Finset.univ.erase good).erase removed)

theorem noUniversalMinimum_iff_not_universalMinimum
    (weight : Weight48) :
    NoUniversalMinimum weight ↔ ¬UniversalMinimum weight := by
  constructor
  · intro no_minimum
    rintro ⟨good, minimum⟩
    obtain ⟨agent, other, _, smaller⟩ := no_minimum good
    exact (not_lt_of_ge (minimum agent other)) smaller
  · intro no_minimum good
    by_contra no_witness
    push_neg at no_witness
    apply no_minimum
    refine ⟨good, ?_⟩
    intro agent other
    by_cases same : other = good
    · rw [same]
    · exact no_witness agent other same

theorem noPeelable_iff_not_peelable
    (weight : Weight48) :
    NoPeelable weight ↔ ¬Peelable weight := by
  constructor
  · intro no_peel
    rintro ⟨agent, good, peelable⟩
    obtain ⟨removed, removed_mem, strict⟩ := no_peel agent good
    exact (not_lt_of_ge (peelable removed removed_mem)) strict
  · intro no_peel agent good
    by_contra no_witness
    push_neg at no_witness
    exact no_peel ⟨agent, good, no_witness⟩

def UniversalMinimumSafe
    (weight : Weight48) : Prop :=
  UniversalMinimum weight → AdmitsEFX weight

def PeelableSafe
    (weight : Weight48) : Prop :=
  Peelable weight → AdmitsEFX weight

theorem noEFX_satisfies_residual_cuts
    (weight : Weight48)
    (no_efx : ¬AdmitsEFX weight)
    (universal_minimum_safe : UniversalMinimumSafe weight)
    (peelable_safe : PeelableSafe weight) :
    NoUniversalMinimum weight ∧ NoPeelable weight := by
  constructor
  · rw [noUniversalMinimum_iff_not_universalMinimum]
    intro universal_minimum
    exact no_efx (universal_minimum_safe universal_minimum)
  · rw [noPeelable_iff_not_peelable]
    intro peelable
    exact no_efx (peelable_safe peelable)

def ResidualCellAssumptions
    (weight : Weight48) : Prop :=
  (∀ agent good, 0 < weight agent good) ∧
  (∀ agent, ∑ good, weight agent good = 1) ∧
  NoUniversalMinimum weight ∧
  NoPeelable weight ∧
  Function.Injective weight

theorem positive_noEFX_reduces_to_residual_generic_eight_cells
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good)
    (no_efx : ¬AdmitsEFX weight)
    (universal_minimum_safe :
      ∀ generic,
        (∀ agent good, 0 < generic agent good) →
        ¬AdmitsEFX generic →
        UniversalMinimumSafe generic)
    (peelable_safe :
      ∀ generic,
        (∀ agent good, 0 < generic agent good) →
        ¬AdmitsEFX generic →
        PeelableSafe generic) :
    ∃ generic : Weight48,
      ResidualCellAssumptions generic ∧
      ¬AdmitsEFX generic ∧
      LiesInEightCell generic := by
  obtain ⟨generic, generic_positive, generic_sum,
      generic_no_efx, rows_injective, eight_cell⟩ :=
    positive_noEFX_reduces_to_generic_normalized_eight_cells
      weight positive no_efx
  obtain ⟨no_universal_minimum, no_peelable⟩ :=
    noEFX_satisfies_residual_cuts generic generic_no_efx
      (universal_minimum_safe generic generic_positive generic_no_efx)
      (peelable_safe generic generic_positive generic_no_efx)
  exact ⟨generic,
    ⟨generic_positive, generic_sum, no_universal_minimum,
      no_peelable, rows_injective⟩,
    generic_no_efx, eight_cell⟩

end EFX48

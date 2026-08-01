import EFX48.Definitions
import Mathlib.Data.Finset.Image
import Mathlib.Logic.Equiv.Fintype

namespace EFX48

open Finset

variable {Agent Good : Type*}
variable [Fintype Agent] [DecidableEq Agent]
variable [Fintype Good] [DecidableEq Good]

def relabelAgentsWeight (weight : Agent → Good → ℝ)
    (permutation : Equiv.Perm Agent) : Agent → Good → ℝ :=
  fun agent good => weight (permutation agent) good

def relabelAgentsAllocation (allocation : Allocation Agent Good)
    (permutation : Equiv.Perm Agent) : Allocation Agent Good :=
  fun agent => allocation (permutation agent)

theorem relabelAgentsAllocation_valid
    (allocation : Allocation Agent Good)
    (valid : ValidAllocation allocation)
    (permutation : Equiv.Perm Agent) :
    ValidAllocation (relabelAgentsAllocation allocation permutation) := by
  intro good
  rcases valid good with ⟨owner, owned, unique⟩
  refine ⟨permutation.symm owner, ?_, ?_⟩
  · simpa [relabelAgentsAllocation] using owned
  · intro candidate candidate_owns
    apply permutation.injective
    simpa [relabelAgentsAllocation] using
      unique (permutation candidate) candidate_owns

theorem relabelAgentsAllocation_efx
    (weight : Agent → Good → ℝ)
    (allocation : Allocation Agent Good)
    (efx : EFX weight allocation)
    (permutation : Equiv.Perm Agent) :
    EFX (relabelAgentsWeight weight permutation)
      (relabelAgentsAllocation allocation permutation) := by
  intro observer target observer_ne_target good good_mem
  change
    additiveValue weight (permutation observer)
        (allocation (permutation observer)) ≥
      additiveValue weight (permutation observer)
        ((allocation (permutation target)).erase good)
  exact efx (permutation observer) (permutation target)
    (fun same => observer_ne_target (permutation.injective same))
    good good_mem

theorem admitsEFX_relabelAgents_iff
    (weight : Agent → Good → ℝ)
    (permutation : Equiv.Perm Agent) :
    AdmitsEFX (relabelAgentsWeight weight permutation) ↔
      AdmitsEFX weight := by
  constructor
  · rintro ⟨allocation, valid, efx⟩
    refine ⟨relabelAgentsAllocation allocation permutation.symm,
      relabelAgentsAllocation_valid allocation valid permutation.symm, ?_⟩
    have relabeled :=
      relabelAgentsAllocation_efx
        (relabelAgentsWeight weight permutation) allocation efx
        permutation.symm
    have restored :
        relabelAgentsWeight
            (relabelAgentsWeight weight permutation) permutation.symm =
          weight := by
      funext agent good
      simp [relabelAgentsWeight]
    rw [restored] at relabeled
    exact relabeled
  · rintro ⟨allocation, valid, efx⟩
    exact ⟨relabelAgentsAllocation allocation permutation,
      relabelAgentsAllocation_valid allocation valid permutation,
      relabelAgentsAllocation_efx weight allocation efx permutation⟩

def relabelGoodsWeight (weight : Agent → Good → ℝ)
    (permutation : Equiv.Perm Good) : Agent → Good → ℝ :=
  fun agent good => weight agent (permutation.symm good)

def relabelGoodsAllocation (allocation : Allocation Agent Good)
    (permutation : Equiv.Perm Good) : Allocation Agent Good :=
  fun agent => (allocation agent).map permutation.toEmbedding

theorem additiveValue_relabelGoods_bundle
    (weight : Agent → Good → ℝ)
    (permutation : Equiv.Perm Good)
    (agent : Agent) (bundle : Finset Good) :
    additiveValue (relabelGoodsWeight weight permutation) agent
        (bundle.map permutation.toEmbedding) =
      additiveValue weight agent bundle := by
  simp [additiveValue, relabelGoodsWeight]

theorem additiveValue_relabelGoods
    (weight : Agent → Good → ℝ)
    (allocation : Allocation Agent Good)
    (permutation : Equiv.Perm Good)
    (agent : Agent) :
    additiveValue (relabelGoodsWeight weight permutation) agent
        (relabelGoodsAllocation allocation permutation agent) =
      additiveValue weight agent (allocation agent) :=
  additiveValue_relabelGoods_bundle
    weight permutation agent (allocation agent)

theorem relabelGoodsAllocation_valid
    (allocation : Allocation Agent Good)
    (valid : ValidAllocation allocation)
    (permutation : Equiv.Perm Good) :
    ValidAllocation (relabelGoodsAllocation allocation permutation) := by
  intro good
  rcases valid (permutation.symm good) with
    ⟨owner, owned, unique⟩
  refine ⟨owner, ?_, ?_⟩
  · exact Finset.mem_map.mpr
      ⟨permutation.symm good, owned, by simp⟩
  · intro candidate candidate_owns
    apply unique candidate
    rcases Finset.mem_map.mp candidate_owns with
      ⟨old_good, old_owned, mapped⟩
    have old_good_eq : old_good = permutation.symm good := by
      apply permutation.injective
      simpa using mapped
    simpa [old_good_eq] using old_owned

theorem relabelGoodsAllocation_efx
    (weight : Agent → Good → ℝ)
    (allocation : Allocation Agent Good)
    (efx : EFX weight allocation)
    (permutation : Equiv.Perm Good) :
    EFX (relabelGoodsWeight weight permutation)
      (relabelGoodsAllocation allocation permutation) := by
  intro observer target observer_ne_target good good_mem
  rcases Finset.mem_map.mp good_mem with
    ⟨old_good, old_good_mem, mapped⟩
  have good_eq : good = permutation old_good := mapped.symm
  subst good
  have original :=
    efx observer target observer_ne_target old_good old_good_mem
  change
    additiveValue (relabelGoodsWeight weight permutation) observer
        ((allocation observer).map permutation.toEmbedding) ≥
      additiveValue (relabelGoodsWeight weight permutation) observer
        (((allocation target).map permutation.toEmbedding).erase
          (permutation old_good))
  have erase_map :
      ((allocation target).map permutation.toEmbedding).erase
          (permutation old_good) =
        ((allocation target).erase old_good).map
          permutation.toEmbedding := by
    symm
    exact Finset.map_erase permutation.toEmbedding
      (allocation target) old_good
  rw [erase_map]
  rw [additiveValue_relabelGoods_bundle,
    additiveValue_relabelGoods_bundle]
  exact original

theorem admitsEFX_relabelGoods_iff
    (weight : Agent → Good → ℝ)
    (permutation : Equiv.Perm Good) :
    AdmitsEFX (relabelGoodsWeight weight permutation) ↔
      AdmitsEFX weight := by
  constructor
  · rintro ⟨allocation, valid, efx⟩
    refine ⟨relabelGoodsAllocation allocation permutation.symm,
      relabelGoodsAllocation_valid allocation valid permutation.symm, ?_⟩
    have relabeled :=
      relabelGoodsAllocation_efx
        (relabelGoodsWeight weight permutation) allocation efx
        permutation.symm
    have restored :
        relabelGoodsWeight
            (relabelGoodsWeight weight permutation) permutation.symm =
          weight := by
      funext agent good
      simp [relabelGoodsWeight]
    rw [restored] at relabeled
    exact relabeled
  · rintro ⟨allocation, valid, efx⟩
    exact ⟨relabelGoodsAllocation allocation permutation,
      relabelGoodsAllocation_valid allocation valid permutation,
      relabelGoodsAllocation_efx weight allocation efx permutation⟩

noncomputable def rangeRepresentative
    {Index Label : Type*} (labels : Index → Label)
    (label : Set.range labels) : Index :=
  Classical.choose label.property

theorem rangeRepresentative_spec
    {Index Label : Type*} (labels : Index → Label)
    (label : Set.range labels) :
    labels (rangeRepresentative labels label) = label :=
  Classical.choose_spec label.property

noncomputable def rangeEquivOfSameKernel
    {Index Label : Type*}
    (actual canonical : Index → Label)
    (same_kernel : ∀ first second,
      actual first = actual second ↔
        canonical first = canonical second) :
    Set.range actual ≃ Set.range canonical := by
  let forward : Set.range actual → Set.range canonical :=
    fun label =>
      ⟨canonical (rangeRepresentative actual label),
        ⟨rangeRepresentative actual label, rfl⟩⟩
  apply Equiv.ofBijective forward
  constructor
  · intro first second same
    apply Subtype.ext
    have canonical_same :
        canonical (rangeRepresentative actual first) =
          canonical (rangeRepresentative actual second) :=
      congrArg Subtype.val same
    calc
      first.val =
          actual (rangeRepresentative actual first) :=
        (rangeRepresentative_spec actual first).symm
      _ = actual (rangeRepresentative actual second) :=
        (same_kernel _ _).mpr canonical_same
      _ = second.val :=
        rangeRepresentative_spec actual second
  · intro target
    rcases target.property with ⟨agent, target_eq⟩
    let source : Set.range actual :=
      ⟨actual agent, ⟨agent, rfl⟩⟩
    refine ⟨source, ?_⟩
    apply Subtype.ext
    change canonical (rangeRepresentative actual source) = target.val
    rw [← target_eq]
    apply (same_kernel _ _).mp
    exact rangeRepresentative_spec actual source

theorem exists_good_permutation_of_same_kernel
    {Index : Type*}
    (actual canonical : Index → Good)
    (same_kernel : ∀ first second,
      actual first = actual second ↔
        canonical first = canonical second) :
    ∃ permutation : Equiv.Perm Good,
      ∀ index, permutation (actual index) = canonical index := by
  classical
  let rangeEquiv :=
    rangeEquivOfSameKernel actual canonical same_kernel
  let permutation : Equiv.Perm Good :=
    rangeEquiv.extendSubtype
  refine ⟨permutation, ?_⟩
  intro index
  have actual_mem : actual index ∈ Set.range actual :=
    ⟨index, rfl⟩
  rw [show permutation (actual index) =
      rangeEquiv ⟨actual index, actual_mem⟩ by
    exact Equiv.extendSubtype_apply_of_mem
      rangeEquiv (actual index) actual_mem]
  change
    canonical
        (rangeRepresentative actual
          ⟨actual index, actual_mem⟩) =
      canonical index
  apply (same_kernel _ _).mp
  exact rangeRepresentative_spec actual
    ⟨actual index, actual_mem⟩

end EFX48

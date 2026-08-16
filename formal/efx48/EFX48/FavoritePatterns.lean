import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Fintype.Perm
import Mathlib.Tactic.FinCases

namespace EFX48

open Finset

def labelRange (labels : Fin 4 → Fin 8) : Finset (Fin 8) :=
  Finset.univ.image labels

def labelFiberCard (labels : Fin 4 → Fin 8) (label : Fin 8) : ℕ :=
  (Finset.univ.filter fun agent => labels agent = label).card

def Multiplicity4 (labels : Fin 4 → Fin 8) : Prop :=
  (labelRange labels).card = 1

def Multiplicity31 (labels : Fin 4 → Fin 8) : Prop :=
  (labelRange labels).card = 2 ∧
    ∃ label, labelFiberCard labels label = 3

def Multiplicity22 (labels : Fin 4 → Fin 8) : Prop :=
  (labelRange labels).card = 2 ∧
    ¬∃ label, labelFiberCard labels label = 3

def Multiplicity211 (labels : Fin 4 → Fin 8) : Prop :=
  (labelRange labels).card = 3

theorem labelRange_card_pos (labels : Fin 4 → Fin 8) :
    0 < (labelRange labels).card := by
  apply Finset.card_pos.mpr
  refine ⟨labels 0, ?_⟩
  exact Finset.mem_image.mpr ⟨0, Finset.mem_univ 0, rfl⟩

theorem labelRange_card_le_four (labels : Fin 4 → Fin 8) :
    (labelRange labels).card ≤ 4 := by
  calc
    (labelRange labels).card ≤ (Finset.univ : Finset (Fin 4)).card :=
      Finset.card_image_le
    _ = 4 := by simp

theorem labelRange_card_eq_four_iff_injective
    (labels : Fin 4 → Fin 8) :
    (labelRange labels).card = 4 ↔ Function.Injective labels := by
  constructor
  · intro range_card
    have image_eq_univ :
        (labelRange labels).card =
          (Finset.univ : Finset (Fin 4)).card := by
      simpa using range_card
    have injective_on :
        Set.InjOn labels (Finset.univ : Finset (Fin 4)) :=
      Finset.card_image_iff.mp image_eq_univ
    intro first second same
    exact injective_on (Finset.mem_univ first)
      (Finset.mem_univ second) same
  · intro injective
    calc
      (labelRange labels).card =
          (Finset.univ : Finset (Fin 4)).card :=
        Finset.card_image_of_injective Finset.univ injective
      _ = 4 := by simp

theorem four_agent_label_multiplicity_coverage
    (labels : Fin 4 → Fin 8) :
    Function.Injective labels ∨
      Multiplicity4 labels ∨
      Multiplicity31 labels ∨
      Multiplicity22 labels ∨
      Multiplicity211 labels := by
  by_cases injective : Function.Injective labels
  · exact Or.inl injective
  · right
    have not_four : (labelRange labels).card ≠ 4 := by
      intro four
      exact injective
        ((labelRange_card_eq_four_iff_injective labels).mp four)
    have positive := labelRange_card_pos labels
    have at_most_four := labelRange_card_le_four labels
    have cases :
        (labelRange labels).card = 1 ∨
        (labelRange labels).card = 2 ∨
        (labelRange labels).card = 3 := by
      omega
    rcases cases with one | two_or_three
    · exact Or.inl one
    · rcases two_or_three with two | three
      · by_cases has_triple :
          ∃ label, labelFiberCard labels label = 3
        · exact Or.inr (Or.inl ⟨two, has_triple⟩)
        · exact Or.inr (Or.inr (Or.inl ⟨two, has_triple⟩))
      · exact Or.inr (Or.inr (Or.inr three))

theorem noninjective_four_agent_label_multiplicity_coverage
    (labels : Fin 4 → Fin 8)
    (not_injective : ¬Function.Injective labels) :
    Multiplicity4 labels ∨
      Multiplicity31 labels ∨
      Multiplicity22 labels ∨
      Multiplicity211 labels := by
  rcases four_agent_label_multiplicity_coverage labels with
    injective | remaining
  · exact (not_injective injective).elim
  · exact remaining

def canonical1111 : Fin 4 → Fin 8 := ![0, 1, 2, 3]
def canonical4 : Fin 4 → Fin 8 := ![0, 0, 0, 0]
def canonical31 : Fin 4 → Fin 8 := ![0, 0, 0, 1]
def canonical22 : Fin 4 → Fin 8 := ![0, 0, 1, 1]
def canonical211 : Fin 4 → Fin 8 := ![0, 0, 1, 2]

@[simp] theorem canonical4_eq_zero (agent : Fin 4) :
    canonical4 agent = 0 := by
  fin_cases agent <;> rfl

def kernel31a : Fin 4 → Fin 8 := ![0, 1, 1, 1]
def kernel31b : Fin 4 → Fin 8 := ![0, 1, 0, 0]
def kernel31c : Fin 4 → Fin 8 := ![0, 0, 1, 0]

def kernel22a : Fin 4 → Fin 8 := ![0, 1, 0, 1]
def kernel22b : Fin 4 → Fin 8 := ![0, 1, 1, 0]

def kernel211a : Fin 4 → Fin 8 := ![0, 1, 0, 2]
def kernel211b : Fin 4 → Fin 8 := ![0, 1, 2, 0]
def kernel211c : Fin 4 → Fin 8 := ![0, 1, 1, 2]
def kernel211d : Fin 4 → Fin 8 := ![0, 1, 2, 1]
def kernel211e : Fin 4 → Fin 8 := ![0, 1, 2, 2]

def KernelEquivalent
    (first second : Fin 4 → Fin 8) : Prop :=
  ∀ left right,
    first left = first right ↔ second left = second right

instance (first second : Fin 4 → Fin 8) :
    Decidable (KernelEquivalent first second) := by
  unfold KernelEquivalent
  exact Fintype.decidableForallFintype

def KernelEquivalent4
    (first second : Fin 4 → Fin 8) : Prop :=
  (first 0 = first 1 ↔ second 0 = second 1) ∧
  (first 0 = first 2 ↔ second 0 = second 2) ∧
  (first 0 = first 3 ↔ second 0 = second 3) ∧
  (first 1 = first 2 ↔ second 1 = second 2) ∧
  (first 1 = first 3 ↔ second 1 = second 3) ∧
  (first 2 = first 3 ↔ second 2 = second 3)

theorem kernelEquivalent_iff_six_pairs
    (first second : Fin 4 → Fin 8) :
    KernelEquivalent first second ↔
      KernelEquivalent4 first second := by
  constructor
  · intro all_pairs
    exact ⟨all_pairs 0 1, all_pairs 0 2, all_pairs 0 3,
      all_pairs 1 2, all_pairs 1 3, all_pairs 2 3⟩
  · intro six_pairs left right
    have reverse (a b c d : Fin 8)
        (forward : a = b ↔ c = d) :
        b = a ↔ d = c := by
      constructor
      · intro same
        exact (forward.mp same.symm).symm
      · intro same
        exact (forward.mpr same.symm).symm
    have h10 := reverse _ _ _ _ six_pairs.1
    have h20 := reverse _ _ _ _ six_pairs.2.1
    have h30 := reverse _ _ _ _ six_pairs.2.2.1
    have h21 := reverse _ _ _ _ six_pairs.2.2.2.1
    have h31 := reverse _ _ _ _ six_pairs.2.2.2.2.1
    have h32 := reverse _ _ _ _ six_pairs.2.2.2.2.2
    fin_cases left <;> fin_cases right <;>
      simp_all [KernelEquivalent4]

theorem fifteen_kernel_coverage
    (labels : Fin 4 → Fin 8) :
    KernelEquivalent labels canonical1111 ∨
    KernelEquivalent labels canonical4 ∨
    KernelEquivalent labels canonical31 ∨
    KernelEquivalent labels kernel31a ∨
    KernelEquivalent labels kernel31b ∨
    KernelEquivalent labels kernel31c ∨
    KernelEquivalent labels canonical22 ∨
    KernelEquivalent labels kernel22a ∨
    KernelEquivalent labels kernel22b ∨
    KernelEquivalent labels canonical211 ∨
    KernelEquivalent labels kernel211a ∨
    KernelEquivalent labels kernel211b ∨
    KernelEquivalent labels kernel211c ∨
    KernelEquivalent labels kernel211d ∨
    KernelEquivalent labels kernel211e := by
  simp_rw [kernelEquivalent_iff_six_pairs]
  by_cases h01 : labels 0 = labels 1 <;>
    by_cases h02 : labels 0 = labels 2 <;>
    by_cases h03 : labels 0 = labels 3 <;>
    by_cases h12 : labels 1 = labels 2 <;>
    by_cases h13 : labels 1 = labels 3 <;>
    by_cases h23 : labels 2 = labels 3 <;>
    simp_all [KernelEquivalent4, canonical1111, canonical4,
      canonical31, kernel31a, kernel31b, kernel31c,
      canonical22, kernel22a, kernel22b,
      canonical211, kernel211a, kernel211b, kernel211c,
      kernel211d, kernel211e]

def AgentKernelRelabels
    (actual canonical : Fin 4 → Fin 8) : Prop :=
  ∃ permutation : Equiv.Perm (Fin 4),
    KernelEquivalent
      (fun agent => actual (permutation agent)) canonical

instance (actual canonical : Fin 4 → Fin 8) :
    Decidable (AgentKernelRelabels actual canonical) := by
  unfold AgentKernelRelabels KernelEquivalent
  exact Fintype.decidableExistsFintype

theorem agentKernelRelabels_refl
    (labels : Fin 4 → Fin 8) :
    AgentKernelRelabels labels labels := by
  refine ⟨Equiv.refl _, ?_⟩
  intro first second
  simp

theorem agentKernelRelabels_of_kernelEquivalent
    {actual intermediate canonical : Fin 4 → Fin 8}
    (same_kernel : KernelEquivalent actual intermediate)
    (relabels : AgentKernelRelabels intermediate canonical) :
    AgentKernelRelabels actual canonical := by
  rcases relabels with ⟨permutation, relabeled_kernel⟩
  refine ⟨permutation, ?_⟩
  intro first second
  exact (same_kernel (permutation first) (permutation second)).trans
    (relabeled_kernel first second)

theorem concrete_kernel_relabelings :
    AgentKernelRelabels kernel31a canonical31 ∧
    AgentKernelRelabels kernel31b canonical31 ∧
    AgentKernelRelabels kernel31c canonical31 ∧
    AgentKernelRelabels kernel22a canonical22 ∧
    AgentKernelRelabels kernel22b canonical22 ∧
    AgentKernelRelabels kernel211a canonical211 ∧
    AgentKernelRelabels kernel211b canonical211 ∧
    AgentKernelRelabels kernel211c canonical211 ∧
    AgentKernelRelabels kernel211d canonical211 ∧
    AgentKernelRelabels kernel211e canonical211 := by
  decide

theorem five_kernel_coverage
    (labels : Fin 4 → Fin 8) :
    AgentKernelRelabels labels canonical1111 ∨
    AgentKernelRelabels labels canonical4 ∨
    AgentKernelRelabels labels canonical31 ∨
    AgentKernelRelabels labels canonical22 ∨
    AgentKernelRelabels labels canonical211 := by
  rcases concrete_kernel_relabelings with
    ⟨r31a, r31b, r31c, r22a, r22b,
      r211a, r211b, r211c, r211d, r211e⟩
  rcases fifteen_kernel_coverage labels with
    h1111 | h4 | h31 | h31a | h31b | h31c |
    h22 | h22a | h22b | h211 | h211a | h211b |
    h211c | h211d | h211e
  · exact Or.inl
      (agentKernelRelabels_of_kernelEquivalent h1111
        (agentKernelRelabels_refl canonical1111))
  · exact Or.inr (Or.inl
      (agentKernelRelabels_of_kernelEquivalent h4
        (agentKernelRelabels_refl canonical4)))
  · exact Or.inr (Or.inr (Or.inl
      (agentKernelRelabels_of_kernelEquivalent h31
        (agentKernelRelabels_refl canonical31))))
  · exact Or.inr (Or.inr (Or.inl
      (agentKernelRelabels_of_kernelEquivalent h31a r31a)))
  · exact Or.inr (Or.inr (Or.inl
      (agentKernelRelabels_of_kernelEquivalent h31b r31b)))
  · exact Or.inr (Or.inr (Or.inl
      (agentKernelRelabels_of_kernelEquivalent h31c r31c)))
  · exact Or.inr (Or.inr (Or.inr (Or.inl
      (agentKernelRelabels_of_kernelEquivalent h22
        (agentKernelRelabels_refl canonical22)))))
  · exact Or.inr (Or.inr (Or.inr (Or.inl
      (agentKernelRelabels_of_kernelEquivalent h22a r22a))))
  · exact Or.inr (Or.inr (Or.inr (Or.inl
      (agentKernelRelabels_of_kernelEquivalent h22b r22b))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr
      (agentKernelRelabels_of_kernelEquivalent h211
        (agentKernelRelabels_refl canonical211)))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr
      (agentKernelRelabels_of_kernelEquivalent h211a r211a))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr
      (agentKernelRelabels_of_kernelEquivalent h211b r211b))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr
      (agentKernelRelabels_of_kernelEquivalent h211c r211c))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr
      (agentKernelRelabels_of_kernelEquivalent h211d r211d))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr
      (agentKernelRelabels_of_kernelEquivalent h211e r211e))))

end EFX48

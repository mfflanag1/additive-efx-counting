import EFX48.FavoritePatterns
import EFX48.Relabeling

namespace EFX48

def Canonicalizes
    (actual canonical : Fin 4 → Fin 8) : Prop :=
  ∃ agentPermutation : Equiv.Perm (Fin 4),
    ∃ goodPermutation : Equiv.Perm (Fin 8),
      ∀ agent,
        goodPermutation (actual (agentPermutation agent)) =
          canonical agent

theorem canonicalizes_of_agentKernelRelabels
    {actual canonical : Fin 4 → Fin 8}
    (relabels : AgentKernelRelabels actual canonical) :
    Canonicalizes actual canonical := by
  rcases relabels with ⟨agentPermutation, same_kernel⟩
  rcases exists_good_permutation_of_same_kernel
      (fun agent => actual (agentPermutation agent))
      canonical same_kernel with
    ⟨goodPermutation, mapped⟩
  exact ⟨agentPermutation, goodPermutation, mapped⟩

theorem five_canonical_pattern_coverage
    (labels : Fin 4 → Fin 8) :
    Canonicalizes labels canonical1111 ∨
    Canonicalizes labels canonical4 ∨
    Canonicalizes labels canonical31 ∨
    Canonicalizes labels canonical22 ∨
    Canonicalizes labels canonical211 := by
  rcases five_kernel_coverage labels with
    h1111 | h4 | h31 | h22 | h211
  · exact Or.inl (canonicalizes_of_agentKernelRelabels h1111)
  · exact Or.inr (Or.inl
      (canonicalizes_of_agentKernelRelabels h4))
  · exact Or.inr (Or.inr (Or.inl
      (canonicalizes_of_agentKernelRelabels h31)))
  · exact Or.inr (Or.inr (Or.inr (Or.inl
      (canonicalizes_of_agentKernelRelabels h22))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr
      (canonicalizes_of_agentKernelRelabels h211))))

theorem canonical1111_injective :
    Function.Injective canonical1111 := by
  decide

theorem injective_of_canonicalizes_1111
    (labels : Fin 4 → Fin 8)
    (canonicalizes : Canonicalizes labels canonical1111) :
    Function.Injective labels := by
  rcases canonicalizes with
    ⟨agentPermutation, goodPermutation, mapped⟩
  intro first second same
  have canonical_same :
      canonical1111 (agentPermutation.symm first) =
        canonical1111 (agentPermutation.symm second) := by
    calc
      canonical1111 (agentPermutation.symm first) =
          goodPermutation
            (labels
              (agentPermutation (agentPermutation.symm first))) :=
        (mapped (agentPermutation.symm first)).symm
      _ = goodPermutation
            (labels
              (agentPermutation (agentPermutation.symm second))) := by
        apply congrArg goodPermutation
        simpa using same
      _ = canonical1111 (agentPermutation.symm second) :=
        mapped (agentPermutation.symm second)
  have preimage_same :
      agentPermutation.symm first =
        agentPermutation.symm second :=
    canonical1111_injective canonical_same
  exact agentPermutation.symm.injective preimage_same

theorem noninjective_canonical_pattern_coverage
    (labels : Fin 4 → Fin 8)
    (not_injective : ¬Function.Injective labels) :
    Canonicalizes labels canonical4 ∨
    Canonicalizes labels canonical31 ∨
    Canonicalizes labels canonical22 ∨
    Canonicalizes labels canonical211 := by
  rcases five_canonical_pattern_coverage labels with
    h1111 | remaining
  · exact (not_injective
      (injective_of_canonicalizes_1111 labels h1111)).elim
  · exact remaining

def second1111 : Fin 4 → Fin 8 := ![1, 2, 3, 4]
def second4 : Fin 4 → Fin 8 := ![1, 1, 1, 1]
def second31 : Fin 4 → Fin 8 := ![1, 1, 1, 2]
def second22 : Fin 4 → Fin 8 := ![1, 1, 2, 2]
def second211 : Fin 4 → Fin 8 := ![1, 1, 2, 3]

def JointCanonicalizes
    (common : Fin 8) (seconds canonical : Fin 4 → Fin 8) : Prop :=
  ∃ agentPermutation : Equiv.Perm (Fin 4),
    ∃ goodPermutation : Equiv.Perm (Fin 8),
      goodPermutation common = 0 ∧
      ∀ agent,
        goodPermutation (seconds (agentPermutation agent)) =
          canonical agent

theorem jointCanonicalizes_of_agentKernelRelabels
    (common : Fin 8)
    (seconds base canonical : Fin 4 → Fin 8)
    (seconds_ne_common : ∀ agent, seconds agent ≠ common)
    (relabels : AgentKernelRelabels seconds base)
    (same_canonical_kernel : KernelEquivalent base canonical)
    (canonical_ne_zero : ∀ agent, canonical agent ≠ 0) :
    JointCanonicalizes common seconds canonical := by
  rcases relabels with ⟨agentPermutation, same_base_kernel⟩
  have same_kernel :
      KernelEquivalent
        (fun agent => seconds (agentPermutation agent)) canonical :=
    fun first second =>
      (same_base_kernel first second).trans
        (same_canonical_kernel first second)
  let actualExtended : Option (Fin 4) → Fin 8
    | none => common
    | some agent => seconds (agentPermutation agent)
  let canonicalExtended : Option (Fin 4) → Fin 8
    | none => 0
    | some agent => canonical agent
  have extended_same_kernel :
      ∀ first second,
        actualExtended first = actualExtended second ↔
          canonicalExtended first = canonicalExtended second := by
    intro first second
    cases first with
    | none =>
        cases second with
        | none => simp [actualExtended, canonicalExtended]
        | some agent =>
            constructor
            · intro equal
              exact (seconds_ne_common (agentPermutation agent)
                equal.symm).elim
            · intro equal
              exact (canonical_ne_zero agent equal.symm).elim
    | some firstAgent =>
        cases second with
        | none =>
            constructor
            · intro equal
              exact (seconds_ne_common
                (agentPermutation firstAgent) equal).elim
            · intro equal
              exact (canonical_ne_zero firstAgent equal).elim
        | some secondAgent =>
            exact same_kernel firstAgent secondAgent
  rcases exists_good_permutation_of_same_kernel
      actualExtended canonicalExtended extended_same_kernel with
    ⟨goodPermutation, mapped⟩
  refine ⟨agentPermutation, goodPermutation, ?_, ?_⟩
  · exact mapped none
  · intro agent
    exact mapped (some agent)

theorem second_pattern_kernel_equivalences :
    KernelEquivalent canonical1111 second1111 ∧
    KernelEquivalent canonical4 second4 ∧
    KernelEquivalent canonical31 second31 ∧
    KernelEquivalent canonical22 second22 ∧
    KernelEquivalent canonical211 second211 := by
  decide

theorem second_patterns_nonzero :
    (∀ agent, second1111 agent ≠ 0) ∧
    (∀ agent, second4 agent ≠ 0) ∧
    (∀ agent, second31 agent ≠ 0) ∧
    (∀ agent, second22 agent ≠ 0) ∧
    (∀ agent, second211 agent ≠ 0) := by
  decide

theorem five_second_pattern_coverage
    (common : Fin 8)
    (seconds : Fin 4 → Fin 8)
    (seconds_ne_common : ∀ agent, seconds agent ≠ common) :
    JointCanonicalizes common seconds second1111 ∨
    JointCanonicalizes common seconds second4 ∨
    JointCanonicalizes common seconds second31 ∨
    JointCanonicalizes common seconds second22 ∨
    JointCanonicalizes common seconds second211 := by
  rcases second_pattern_kernel_equivalences with
    ⟨k1111, k4, k31, k22, k211⟩
  rcases second_patterns_nonzero with
    ⟨n1111, n4, n31, n22, n211⟩
  rcases five_kernel_coverage seconds with
    h1111 | h4 | h31 | h22 | h211
  · exact Or.inl
      (jointCanonicalizes_of_agentKernelRelabels
        common seconds canonical1111 second1111
        seconds_ne_common h1111 k1111 n1111)
  · exact Or.inr (Or.inl
      (jointCanonicalizes_of_agentKernelRelabels
        common seconds canonical4 second4
        seconds_ne_common h4 k4 n4))
  · exact Or.inr (Or.inr (Or.inl
      (jointCanonicalizes_of_agentKernelRelabels
        common seconds canonical31 second31
        seconds_ne_common h31 k31 n31)))
  · exact Or.inr (Or.inr (Or.inr (Or.inl
      (jointCanonicalizes_of_agentKernelRelabels
        common seconds canonical22 second22
        seconds_ne_common h22 k22 n22))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr
      (jointCanonicalizes_of_agentKernelRelabels
        common seconds canonical211 second211
        seconds_ne_common h211 k211 n211))))

end EFX48

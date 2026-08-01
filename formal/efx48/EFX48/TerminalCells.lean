import EFX48.PartitionMatching
import EFX48.Peelable
import EFX48.Stabilizers
import EFX48.UniversalMinimum

namespace EFX48

open Finset

def GenericNormalizedCounterexample
    (weight : Weight48) : Prop :=
  (∀ agent good, 0 < weight agent good) ∧
  (∀ agent, ∑ good, weight agent good = 1) ∧
  ¬AdmitsEFX weight ∧
  Function.Injective weight

def AllPartitionsObstructed
    (weight : Weight48) : Prop :=
  ∀ bundles : Allocation (Fin 4) (Fin 8),
    ValidAllocation bundles →
    (∀ slot, (bundles slot).Nonempty) →
    MatchingObstruction weight bundles

def TerminalBase
    (weight : Weight48) : Prop :=
  ResidualCellAssumptions weight ∧
  AllPartitionsObstructed weight

def FavoriteCellSpec
    (weight : Weight48)
    (favorites : Fin 4 → Fin 8) : Prop :=
  TerminalBase weight ∧
  StrictFavorites weight favorites

def FavoriteStabilizedCellSpec
    (weight : Weight48)
    (favorites : Fin 4 → Fin 8) : Prop :=
  FavoriteCellSpec weight favorites ∧
  FavoriteStabilizer weight favorites

def PrefixStabilizedCellSpec
    (weight : Weight48)
    (seconds : Fin 4 → Fin 8) : Prop :=
  TerminalBase weight ∧
  StrictRankingPrefix weight canonical4 seconds ∧
  PrefixStabilizer weight canonical4 seconds

def EightTerminalCellsHaveCounterexample : Prop :=
  (∃ weight, FavoriteCellSpec weight canonical211) ∨
  (∃ weight, FavoriteStabilizedCellSpec weight canonical31) ∨
  (∃ weight, FavoriteStabilizedCellSpec weight canonical22) ∨
  (∃ weight, PrefixStabilizedCellSpec weight second1111) ∨
  (∃ weight, PrefixStabilizedCellSpec weight second4) ∨
  (∃ weight, PrefixStabilizedCellSpec weight second31) ∨
  (∃ weight, PrefixStabilizedCellSpec weight second22) ∨
  (∃ weight, PrefixStabilizedCellSpec weight second211)

def EightTerminalCellsUnsat : Prop :=
  ¬EightTerminalCellsHaveCounterexample

theorem positive_relabelWeight
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good)
    (agents : Equiv.Perm (Fin 4))
    (goods : Equiv.Perm (Fin 8)) :
    ∀ agent good,
      0 < relabelWeight weight agents goods agent good := by
  intro agent good
  exact positive (agents agent) (goods.symm good)

theorem normalized_relabelWeight
    (weight : Weight48)
    (normalized : ∀ agent, ∑ good, weight agent good = 1)
    (agents : Equiv.Perm (Fin 4))
    (goods : Equiv.Perm (Fin 8)) :
    ∀ agent,
      ∑ good, relabelWeight weight agents goods agent good = 1 := by
  intro agent
  calc
    ∑ good, relabelWeight weight agents goods agent good =
        ∑ good, weight (agents agent) (goods.symm good) := by
      rfl
    _ = ∑ good, weight (agents agent) good :=
      Equiv.sum_comp goods.symm _
    _ = 1 := normalized (agents agent)

theorem injectiveRows_relabelWeight
    (weight : Weight48)
    (rows_injective : Function.Injective weight)
    (agents : Equiv.Perm (Fin 4))
    (goods : Equiv.Perm (Fin 8)) :
    Function.Injective
      (relabelWeight weight agents goods) := by
  intro first second rows_equal
  apply agents.injective
  apply rows_injective
  funext good
  have coordinate_equal :=
    congrFun rows_equal (goods good)
  simpa [relabelWeight, relabelAgentsWeight,
    relabelGoodsWeight] using coordinate_equal

theorem genericNormalizedCounterexample_relabelWeight
    (weight : Weight48)
    (generic : GenericNormalizedCounterexample weight)
    (agents : Equiv.Perm (Fin 4))
    (goods : Equiv.Perm (Fin 8)) :
    GenericNormalizedCounterexample
      (relabelWeight weight agents goods) := by
  refine ⟨positive_relabelWeight weight generic.1 agents goods,
    normalized_relabelWeight weight generic.2.1 agents goods, ?_,
    injectiveRows_relabelWeight weight generic.2.2.2 agents goods⟩
  intro relabeled_efx
  exact generic.2.2.1
    ((admitsEFX_relabelWeight_iff weight agents goods).mp
      relabeled_efx)

theorem terminalBase_of_generic_counterexample
    (weight : Weight48)
    (generic : GenericNormalizedCounterexample weight)
    (universal_minimum_safe : UniversalMinimumSafe weight)
    (peelable_safe : PeelableSafe weight) :
    TerminalBase weight := by
  obtain ⟨no_universal_minimum, no_peelable⟩ :=
    noEFX_satisfies_residual_cuts weight generic.2.2.1
      universal_minimum_safe peelable_safe
  refine ⟨⟨generic.1, generic.2.1,
    no_universal_minimum, no_peelable, generic.2.2.2⟩, ?_⟩
  intro bundles valid _
  exact matchingObstruction_of_noEFX
    weight bundles valid generic.2.2.1

theorem favorite_cell_spec_of_relabels
    (weight : Weight48)
    (generic : GenericNormalizedCounterexample weight)
    (favorites : Fin 4 → Fin 8)
    (cell : RelabelsIntoFavoriteCell weight favorites)
    (universal_minimum_safe :
      ∀ candidate,
        GenericNormalizedCounterexample candidate →
        UniversalMinimumSafe candidate)
    (peelable_safe :
      ∀ candidate,
        GenericNormalizedCounterexample candidate →
        PeelableSafe candidate) :
    ∃ candidate, FavoriteCellSpec candidate favorites := by
  rcases cell with ⟨agents, goods, strict, _⟩
  let candidate := relabelWeight weight agents goods
  have candidate_generic :=
    genericNormalizedCounterexample_relabelWeight
      weight generic agents goods
  exact ⟨candidate,
    terminalBase_of_generic_counterexample candidate
      candidate_generic
      (universal_minimum_safe candidate candidate_generic)
      (peelable_safe candidate candidate_generic),
    strict⟩

theorem favorite_stabilized_cell_spec_of_relabels
    (weight : Weight48)
    (generic : GenericNormalizedCounterexample weight)
    (favorites : Fin 4 → Fin 8)
    (cell : RelabelsIntoFavoriteCell weight favorites)
    (universal_minimum_safe :
      ∀ candidate,
        GenericNormalizedCounterexample candidate →
        UniversalMinimumSafe candidate)
    (peelable_safe :
      ∀ candidate,
        GenericNormalizedCounterexample candidate →
        PeelableSafe candidate) :
    ∃ candidate, FavoriteStabilizedCellSpec candidate favorites := by
  rcases cell with
    ⟨initialAgents, initialGoods, initialStrict, initialNoEFX⟩
  let initial :=
    relabelWeight weight initialAgents initialGoods
  have initial_generic :=
    genericNormalizedCounterexample_relabelWeight
      weight generic initialAgents initialGoods
  obtain ⟨agents, goods, strict, _, stabilized⟩ :=
    exists_favorite_stabilized_counterexample
      initial favorites initialStrict initialNoEFX
  let candidate := relabelWeight initial agents goods
  have candidate_generic :=
    genericNormalizedCounterexample_relabelWeight
      initial initial_generic agents goods
  exact ⟨candidate,
    ⟨terminalBase_of_generic_counterexample candidate
        candidate_generic
        (universal_minimum_safe candidate candidate_generic)
        (peelable_safe candidate candidate_generic),
      strict⟩,
    stabilized⟩

theorem prefix_stabilized_cell_spec_of_relabels
    (weight : Weight48)
    (generic : GenericNormalizedCounterexample weight)
    (seconds : Fin 4 → Fin 8)
    (cell : RelabelsIntoSecondCell weight seconds)
    (universal_minimum_safe :
      ∀ candidate,
        GenericNormalizedCounterexample candidate →
        UniversalMinimumSafe candidate)
    (peelable_safe :
      ∀ candidate,
        GenericNormalizedCounterexample candidate →
        PeelableSafe candidate) :
    ∃ candidate, PrefixStabilizedCellSpec candidate seconds := by
  rcases cell with
    ⟨initialAgents, initialGoods, initialStrict, initialNoEFX⟩
  let initial :=
    relabelWeight weight initialAgents initialGoods
  have initial_generic :=
    genericNormalizedCounterexample_relabelWeight
      weight generic initialAgents initialGoods
  obtain ⟨agents, goods, strict, _, stabilized⟩ :=
    exists_prefix_stabilized_counterexample
      initial canonical4 seconds initialStrict initialNoEFX
  let candidate := relabelWeight initial agents goods
  have candidate_generic :=
    genericNormalizedCounterexample_relabelWeight
      initial initial_generic agents goods
  exact ⟨candidate,
    terminalBase_of_generic_counterexample candidate
      candidate_generic
      (universal_minimum_safe candidate candidate_generic)
      (peelable_safe candidate candidate_generic),
    strict, stabilized⟩

theorem positive_noEFX_reduces_to_eight_terminal_cells
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good)
    (no_efx : ¬AdmitsEFX weight)
    (universal_minimum_safe :
      ∀ candidate,
        GenericNormalizedCounterexample candidate →
        UniversalMinimumSafe candidate)
    (peelable_safe :
      ∀ candidate,
        GenericNormalizedCounterexample candidate →
        PeelableSafe candidate) :
    EightTerminalCellsHaveCounterexample := by
  obtain ⟨genericWeight, genericPositive, genericSum,
      genericNoEFX, rowsInjective, strict⟩ :=
    positive_noEFX_has_fully_generic_normalized_counterexample
      weight positive no_efx
  have generic :
      GenericNormalizedCounterexample genericWeight :=
    ⟨genericPositive, genericSum, genericNoEFX, rowsInjective⟩
  rcases strict_counterexample_eight_cell_coverage
      genericWeight
      (fun agent good => (genericPositive agent good).le)
      (favoriteOf genericWeight) (secondOf genericWeight)
      strict genericNoEFX with
    cell211 | cell31 | cell22 | second1111Cell | second4Cell |
      second31Cell | second22Cell | second211Cell
  · exact Or.inl
      (favorite_cell_spec_of_relabels
        genericWeight generic canonical211 cell211
        universal_minimum_safe peelable_safe)
  · exact Or.inr (Or.inl
      (favorite_stabilized_cell_spec_of_relabels
        genericWeight generic canonical31 cell31
        universal_minimum_safe peelable_safe))
  · exact Or.inr (Or.inr (Or.inl
      (favorite_stabilized_cell_spec_of_relabels
        genericWeight generic canonical22 cell22
        universal_minimum_safe peelable_safe)))
  · exact Or.inr (Or.inr (Or.inr (Or.inl
      (prefix_stabilized_cell_spec_of_relabels
        genericWeight generic second1111 second1111Cell
        universal_minimum_safe peelable_safe))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl
      (prefix_stabilized_cell_spec_of_relabels
        genericWeight generic second4 second4Cell
        universal_minimum_safe peelable_safe)))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl
      (prefix_stabilized_cell_spec_of_relabels
        genericWeight generic second31 second31Cell
        universal_minimum_safe peelable_safe))))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl
      (prefix_stabilized_cell_spec_of_relabels
        genericWeight generic second22 second22Cell
        universal_minimum_safe peelable_safe)))))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr
      (prefix_stabilized_cell_spec_of_relabels
        genericWeight generic second211 second211Cell
        universal_minimum_safe peelable_safe)))))))

theorem admitsEFX_4x8_of_terminal_cells_unsat
    (terminal_cells_unsat : EightTerminalCellsUnsat)
    (universal_minimum_safe :
      ∀ candidate,
        GenericNormalizedCounterexample candidate →
        UniversalMinimumSafe candidate)
    (peelable_safe :
      ∀ candidate,
        GenericNormalizedCounterexample candidate →
        PeelableSafe candidate)
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good) :
    AdmitsEFX weight := by
  by_contra no_efx
  exact terminal_cells_unsat
    (positive_noEFX_reduces_to_eight_terminal_cells
      weight positive no_efx universal_minimum_safe peelable_safe)

end EFX48

import EFX48.TerminalCells

namespace EFX48

open Finset

def canonicalFavoriteGoods211 : Finset (Fin 8) :=
  {0, 1, 2}

def FavoriteGoods211Separated
    (bundles : Allocation (Fin 4) (Fin 8)) : Prop :=
  ∀ first ∈ canonicalFavoriteGoods211,
    ∀ second ∈ canonicalFavoriteGoods211,
      first ≠ second →
      ∀ firstSlot secondSlot,
        first ∈ bundles firstSlot →
        second ∈ bundles secondSlot →
        firstSlot ≠ secondSlot

def NoNonfavoriteSingleton
    (bundles : Allocation (Fin 4) (Fin 8)) : Prop :=
  ∀ slot good,
    bundles slot = {good} →
    good ∈ canonicalFavoriteGoods211

def Anchored211Partition
    (bundles : Allocation (Fin 4) (Fin 8)) : Prop :=
  ValidAllocation bundles ∧
  (∀ slot, (bundles slot).Nonempty) ∧
  FavoriteGoods211Separated bundles ∧
  (((∃ slot, bundles slot = {0}) ∧
      NoNonfavoriteSingleton bundles) ∨
    ∀ slot, (bundles slot).card = 2)

def AnchoredContestedFavoriteLemma : Prop :=
  ∀ weight : Weight48,
    ResidualCellAssumptions weight →
    StrictFavorites weight canonical211 →
    ∃ bundles : Allocation (Fin 4) (Fin 8),
      Anchored211Partition bundles ∧
      HasFeasiblePerfectMatching weight bundles

theorem favorite211_cell_unsat_of_anchored_contested_favorite
    (anchored : AnchoredContestedFavoriteLemma) :
    ¬∃ weight, FavoriteCellSpec weight canonical211 := by
  rintro ⟨weight, cell⟩
  obtain ⟨bundles, family, matching⟩ :=
    anchored weight cell.1.1 cell.2
  have obstruction :=
    cell.1.2 bundles family.1 family.2.1
  exact
    ((matchingObstruction_iff_not_hasFeasiblePerfectMatching
      weight bundles).1 obstruction) matching

end EFX48

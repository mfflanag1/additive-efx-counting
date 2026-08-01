import Mathlib.Data.Fintype.Perm
import Mathlib.Data.Fintype.Pi
import Std.Tactic

namespace EFX48

abbrev OwnerMap48 := Fin 8 → Fin 4

def OntoOwnerMap
    (owner : OwnerMap48) : Prop :=
  ∀ slot, ∃ good, owner good = slot

def RestrictedGrowth
    (owner : OwnerMap48) : Prop :=
  owner 0 = 0 ∧
  ∀ good, good ≠ 0 →
    ∃ earlier,
      earlier.val < good.val ∧
      (owner good).val ≤ (owner earlier).val + 1

instance (owner : OwnerMap48) : Decidable (OntoOwnerMap owner) := by
  unfold OntoOwnerMap
  infer_instance

instance (owner : OwnerMap48) : Decidable (RestrictedGrowth owner) := by
  unfold RestrictedGrowth
  infer_instance

def canonicalOwnerMaps : Finset OwnerMap48 :=
  Finset.univ.filter
    (fun owner => RestrictedGrowth owner ∧ OntoOwnerMap owner)

theorem canonicalOwnerMaps_card :
    canonicalOwnerMaps.card = 1701 := by
  native_decide

theorem ontoOwnerMap_has_restricted_relabel :
    ∀ owner : OwnerMap48,
      OntoOwnerMap owner →
      ∃ relabel : Equiv.Perm (Fin 4),
        RestrictedGrowth (fun good => relabel (owner good)) := by
  native_decide

theorem canonicalOwnerMaps_cover :
    ∀ owner : OwnerMap48,
      OntoOwnerMap owner →
      ∃ canonical ∈ canonicalOwnerMaps,
        ∃ permutation : Equiv.Perm (Fin 4),
          ∀ good, owner good = permutation (canonical good) := by
  intro owner hOnto
  obtain ⟨relabel, hGrowth⟩ :=
    ontoOwnerMap_has_restricted_relabel owner hOnto
  let canonical : OwnerMap48 := fun good => relabel (owner good)
  have hCanonicalOnto : OntoOwnerMap canonical := by
    intro slot
    obtain ⟨good, hgood⟩ := hOnto (relabel.symm slot)
    refine ⟨good, ?_⟩
    simp [canonical, hgood]
  refine ⟨canonical, ?_, relabel.symm, ?_⟩
  · simp [canonicalOwnerMaps, canonical, hGrowth, hCanonicalOnto]
  · intro good
    simp [canonical]

end EFX48

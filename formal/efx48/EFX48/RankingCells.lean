import EFX48.CanonicalCoverage
import EFX48.FavoriteMatching

namespace EFX48

def StrictFavorites
    (weight : Fin 4 → Fin 8 → ℝ)
    (favorites : Fin 4 → Fin 8) : Prop :=
  ∀ agent good, good ≠ favorites agent →
    weight agent (favorites agent) > weight agent good

def StrictRankingPrefix
    (weight : Fin 4 → Fin 8 → ℝ)
    (favorites seconds : Fin 4 → Fin 8) : Prop :=
  StrictFavorites weight favorites ∧
  (∀ agent, seconds agent ≠ favorites agent) ∧
  ∀ agent good,
    good ≠ favorites agent →
    good ≠ seconds agent →
      weight agent (seconds agent) > weight agent good

def relabelWeight
    (weight : Fin 4 → Fin 8 → ℝ)
    (agentPermutation : Equiv.Perm (Fin 4))
    (goodPermutation : Equiv.Perm (Fin 8)) :
    Fin 4 → Fin 8 → ℝ :=
  relabelGoodsWeight
    (relabelAgentsWeight weight agentPermutation)
    goodPermutation

theorem admitsEFX_relabelWeight_iff
    (weight : Fin 4 → Fin 8 → ℝ)
    (agentPermutation : Equiv.Perm (Fin 4))
    (goodPermutation : Equiv.Perm (Fin 8)) :
    AdmitsEFX
        (relabelWeight weight agentPermutation goodPermutation) ↔
      AdmitsEFX weight := by
  rw [relabelWeight, admitsEFX_relabelGoods_iff,
    admitsEFX_relabelAgents_iff]

theorem strictFavorites_relabel
    (weight : Fin 4 → Fin 8 → ℝ)
    (favorites canonical : Fin 4 → Fin 8)
    (strict : StrictFavorites weight favorites)
    (agentPermutation : Equiv.Perm (Fin 4))
    (goodPermutation : Equiv.Perm (Fin 8))
    (mapped : ∀ agent,
      goodPermutation (favorites (agentPermutation agent)) =
        canonical agent) :
    StrictFavorites
      (relabelWeight weight agentPermutation goodPermutation)
      canonical := by
  intro agent good good_ne_favorite
  have favorite_preimage :
      goodPermutation.symm (canonical agent) =
        favorites (agentPermutation agent) := by
    rw [← mapped agent]
    simp
  have other_ne_favorite :
      goodPermutation.symm good ≠
        favorites (agentPermutation agent) := by
    intro equal
    apply good_ne_favorite
    rw [← mapped agent, ← equal]
    simp
  simpa [relabelWeight, relabelGoodsWeight,
    relabelAgentsWeight, favorite_preimage] using
    strict (agentPermutation agent)
      (goodPermutation.symm good) other_ne_favorite

theorem strictRankingPrefix_relabel
    (weight : Fin 4 → Fin 8 → ℝ)
    (favorites seconds canonicalFavorites canonicalSeconds :
      Fin 4 → Fin 8)
    (strict : StrictRankingPrefix weight favorites seconds)
    (agentPermutation : Equiv.Perm (Fin 4))
    (goodPermutation : Equiv.Perm (Fin 8))
    (favorites_mapped : ∀ agent,
      goodPermutation (favorites (agentPermutation agent)) =
        canonicalFavorites agent)
    (seconds_mapped : ∀ agent,
      goodPermutation (seconds (agentPermutation agent)) =
        canonicalSeconds agent) :
    StrictRankingPrefix
      (relabelWeight weight agentPermutation goodPermutation)
      canonicalFavorites canonicalSeconds := by
  refine ⟨strictFavorites_relabel weight favorites canonicalFavorites
    strict.1 agentPermutation goodPermutation favorites_mapped, ?_, ?_⟩
  · intro agent equal
    have mapped_equal :
        goodPermutation (seconds (agentPermutation agent)) =
          goodPermutation (favorites (agentPermutation agent)) := by
      rw [seconds_mapped, favorites_mapped, equal]
    exact strict.2.1 (agentPermutation agent)
      (goodPermutation.injective mapped_equal)
  · intro agent good good_ne_favorite good_ne_second
    have favorite_preimage :
        goodPermutation.symm (canonicalFavorites agent) =
          favorites (agentPermutation agent) := by
      rw [← favorites_mapped agent]
      simp
    have second_preimage :
        goodPermutation.symm (canonicalSeconds agent) =
          seconds (agentPermutation agent) := by
      rw [← seconds_mapped agent]
      simp
    have other_ne_favorite :
        goodPermutation.symm good ≠
          favorites (agentPermutation agent) := by
      intro equal
      apply good_ne_favorite
      rw [← favorites_mapped agent, ← equal]
      simp
    have other_ne_second :
        goodPermutation.symm good ≠
          seconds (agentPermutation agent) := by
      intro equal
      apply good_ne_second
      rw [← seconds_mapped agent, ← equal]
      simp
    simpa [relabelWeight, relabelGoodsWeight,
      relabelAgentsWeight, favorite_preimage,
      second_preimage] using
      strict.2.2 (agentPermutation agent)
        (goodPermutation.symm good)
        other_ne_favorite other_ne_second

theorem admitsEFX_of_injective_strictFavorites
    (weight : Fin 4 → Fin 8 → ℝ)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (favorites : Fin 4 → Fin 8)
    (strict : StrictFavorites weight favorites)
    (injective : Function.Injective favorites) :
    AdmitsEFX weight := by
  apply favorite_injection_allocation_4x8
    weight nonnegative favorites injective
  intro agent good
  by_cases same : good = favorites agent
  · rw [same]
  · exact (strict agent good same).le

theorem counterexample_favorites_not_injective
    (weight : Fin 4 → Fin 8 → ℝ)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (favorites : Fin 4 → Fin 8)
    (strict : StrictFavorites weight favorites)
    (no_efx : ¬AdmitsEFX weight) :
    ¬Function.Injective favorites := by
  intro injective
  exact no_efx
    (admitsEFX_of_injective_strictFavorites
      weight nonnegative favorites strict injective)

def RelabelsIntoFavoriteCell
    (weight : Fin 4 → Fin 8 → ℝ)
    (canonical : Fin 4 → Fin 8) : Prop :=
  ∃ agentPermutation : Equiv.Perm (Fin 4),
    ∃ goodPermutation : Equiv.Perm (Fin 8),
      StrictFavorites
        (relabelWeight weight agentPermutation goodPermutation)
        canonical ∧
      ¬AdmitsEFX
        (relabelWeight weight agentPermutation goodPermutation)

def RelabelsIntoSecondCell
    (weight : Fin 4 → Fin 8 → ℝ)
    (canonicalSeconds : Fin 4 → Fin 8) : Prop :=
  ∃ agentPermutation : Equiv.Perm (Fin 4),
    ∃ goodPermutation : Equiv.Perm (Fin 8),
      StrictRankingPrefix
        (relabelWeight weight agentPermutation goodPermutation)
        canonical4 canonicalSeconds ∧
      ¬AdmitsEFX
        (relabelWeight weight agentPermutation goodPermutation)

theorem relabelsIntoFavoriteCell_of_canonicalizes
    (weight : Fin 4 → Fin 8 → ℝ)
    (favorites canonical : Fin 4 → Fin 8)
    (strict : StrictFavorites weight favorites)
    (no_efx : ¬AdmitsEFX weight)
    (canonicalizes : Canonicalizes favorites canonical) :
    RelabelsIntoFavoriteCell weight canonical := by
  rcases canonicalizes with
    ⟨agentPermutation, goodPermutation, mapped⟩
  refine ⟨agentPermutation, goodPermutation,
    strictFavorites_relabel weight favorites canonical strict
      agentPermutation goodPermutation mapped, ?_⟩
  intro relabeled_efx
  exact no_efx
    ((admitsEFX_relabelWeight_iff
      weight agentPermutation goodPermutation).mp relabeled_efx)

theorem relabelsIntoSecondCell_of_jointCanonicalizes
    (weight : Fin 4 → Fin 8 → ℝ)
    (favorites seconds canonicalSeconds : Fin 4 → Fin 8)
    (common : Fin 8)
    (favorites_common : ∀ agent, favorites agent = common)
    (strict : StrictRankingPrefix weight favorites seconds)
    (no_efx : ¬AdmitsEFX weight)
    (canonicalizes :
      JointCanonicalizes common seconds canonicalSeconds) :
    RelabelsIntoSecondCell weight canonicalSeconds := by
  rcases canonicalizes with
    ⟨agentPermutation, goodPermutation,
      common_mapped, seconds_mapped⟩
  have favorites_mapped : ∀ agent,
      goodPermutation (favorites (agentPermutation agent)) =
        canonical4 agent := by
    intro agent
    rw [favorites_common, common_mapped]
    fin_cases agent <;> rfl
  refine ⟨agentPermutation, goodPermutation,
    strictRankingPrefix_relabel
      weight favorites seconds canonical4 canonicalSeconds
      strict agentPermutation goodPermutation
      favorites_mapped seconds_mapped, ?_⟩
  intro relabeled_efx
  exact no_efx
    ((admitsEFX_relabelWeight_iff
      weight agentPermutation goodPermutation).mp relabeled_efx)

theorem strict_counterexample_eight_cell_coverage
    (weight : Fin 4 → Fin 8 → ℝ)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (favorites seconds : Fin 4 → Fin 8)
    (strict : StrictRankingPrefix weight favorites seconds)
    (no_efx : ¬AdmitsEFX weight) :
    RelabelsIntoFavoriteCell weight canonical211 ∨
    RelabelsIntoFavoriteCell weight canonical31 ∨
    RelabelsIntoFavoriteCell weight canonical22 ∨
    RelabelsIntoSecondCell weight second1111 ∨
    RelabelsIntoSecondCell weight second4 ∨
    RelabelsIntoSecondCell weight second31 ∨
    RelabelsIntoSecondCell weight second22 ∨
    RelabelsIntoSecondCell weight second211 := by
  have favorites_not_injective :=
    counterexample_favorites_not_injective
      weight nonnegative favorites strict.1 no_efx
  rcases noninjective_canonical_pattern_coverage
      favorites favorites_not_injective with
    common_cell | cell31 | cell22 | cell211
  · rcases common_cell with
      ⟨initialAgentPermutation, initialGoodPermutation,
        initialMapped⟩
    have mapped_to_zero : ∀ agent,
        initialGoodPermutation (favorites agent) = 0 := by
      intro agent
      have mapped :=
        initialMapped (initialAgentPermutation.symm agent)
      rw [canonical4_eq_zero] at mapped
      simpa using mapped
    have common : ∀ agent,
        favorites agent = favorites 0 := by
      intro agent
      apply initialGoodPermutation.injective
      rw [mapped_to_zero, mapped_to_zero]
    have seconds_ne_common : ∀ agent,
        seconds agent ≠ favorites 0 := by
      intro agent equal
      exact strict.2.1 agent
        (equal.trans (common agent).symm)
    rcases five_second_pattern_coverage
        (favorites 0) seconds seconds_ne_common with
      seconds1111 | seconds4cell | seconds31cell |
      seconds22cell | seconds211cell
    · exact Or.inr (Or.inr (Or.inr (Or.inl
        (relabelsIntoSecondCell_of_jointCanonicalizes
          weight favorites seconds second1111 (favorites 0)
          common strict no_efx seconds1111))))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl
        (relabelsIntoSecondCell_of_jointCanonicalizes
          weight favorites seconds second4 (favorites 0)
          common strict no_efx seconds4cell)))))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl
        (relabelsIntoSecondCell_of_jointCanonicalizes
          weight favorites seconds second31 (favorites 0)
          common strict no_efx seconds31cell))))))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl
        (relabelsIntoSecondCell_of_jointCanonicalizes
          weight favorites seconds second22 (favorites 0)
          common strict no_efx seconds22cell)))))))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr
        (relabelsIntoSecondCell_of_jointCanonicalizes
          weight favorites seconds second211 (favorites 0)
          common strict no_efx seconds211cell)))))))
  · exact Or.inr (Or.inl
      (relabelsIntoFavoriteCell_of_canonicalizes
        weight favorites canonical31 strict.1 no_efx cell31))
  · exact Or.inr (Or.inr (Or.inl
      (relabelsIntoFavoriteCell_of_canonicalizes
        weight favorites canonical22 strict.1 no_efx cell22)))
  · exact Or.inl
      (relabelsIntoFavoriteCell_of_canonicalizes
        weight favorites canonical211 strict.1 no_efx cell211)

end EFX48

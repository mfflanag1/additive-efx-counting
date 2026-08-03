import EFX48.RankingCells
import Mathlib.Data.Finset.Max
import Mathlib.Data.Fintype.Perm
import Mathlib.Data.Fintype.Prod
import Mathlib.Order.PiLex

namespace EFX48

def AgentPatternPreserving
    {Pattern : Type*}
    (patterns : Fin 4 → Pattern)
    (permutation : Equiv.Perm (Fin 4)) : Prop :=
  ∀ agent, patterns (permutation agent) = patterns agent

def GoodSetFixing
    (used : Finset (Fin 8))
    (permutation : Equiv.Perm (Fin 8)) : Prop :=
  ∀ good ∈ used, permutation good = good

def RowLexGE
    (weight : Fin 4 → Fin 8 → ℝ)
    (left right : Fin 4) : Prop :=
  toLex (weight right) ≤ toLex (weight left)

def ColumnLexGE
    (weight : Fin 4 → Fin 8 → ℝ)
    (left right : Fin 8) : Prop :=
  toLex (fun agent => weight agent right) ≤
    toLex (fun agent => weight agent left)

def MatrixLex
    (weight : Fin 4 → Fin 8 → ℝ) :
    Πₗ agent : Fin 4, Πₗ good : Fin 8, ℝ :=
  toLex (fun agent => toLex (weight agent))

private theorem swap_preserves_pattern
    {Pattern : Type*}
    {patterns : Fin 4 → Pattern}
    {left right : Fin 4}
    (same : patterns left = patterns right) :
    AgentPatternPreserving patterns (Equiv.swap left right) := by
  intro agent
  by_cases left_eq_right : left = right
  · subst right
    simp
  by_cases agent_eq_left : agent = left
  · subst agent
    simp [same]
  by_cases agent_eq_right : agent = right
  · subst agent
    simp [same]
  rw [Equiv.swap_apply_of_ne_of_ne agent_eq_left agent_eq_right]

private theorem swap_fixes_used
    (used : Finset (Fin 8))
    {left right : Fin 8}
    (left_unused : left ∉ used)
    (right_unused : right ∉ used) :
    GoodSetFixing used (Equiv.swap left right) := by
  intro good good_used
  rw [Equiv.swap_apply_of_ne_of_ne]
  · exact fun equal => left_unused (equal ▸ good_used)
  · exact fun equal => right_unused (equal ▸ good_used)

private theorem compose_agent_preserving
    {Pattern : Type*}
    {patterns : Fin 4 → Pattern}
    {first second : Equiv.Perm (Fin 4)}
    (first_preserves : AgentPatternPreserving patterns first)
    (second_preserves : AgentPatternPreserving patterns second) :
    AgentPatternPreserving patterns (first.trans second) := by
  intro agent
  rw [Equiv.trans_apply, second_preserves, first_preserves]

private theorem compose_good_fixing
    {used : Finset (Fin 8)}
    {first second : Equiv.Perm (Fin 8)}
    (first_fixes : GoodSetFixing used first)
    (second_fixes : GoodSetFixing used second) :
    GoodSetFixing used (first.trans second) := by
  intro good good_used
  rw [Equiv.trans_apply, first_fixes good good_used,
    second_fixes good good_used]

private theorem relabelWeight_agent_swap
    (weight : Fin 4 → Fin 8 → ℝ)
    (agents : Equiv.Perm (Fin 4))
    (goods : Equiv.Perm (Fin 8))
    (left right : Fin 4) :
    relabelWeight weight ((Equiv.swap left right).trans agents) goods =
      fun agent => relabelWeight weight agents goods
        (Equiv.swap left right agent) := by
  funext agent good
  simp [relabelWeight, relabelAgentsWeight, relabelGoodsWeight]

private theorem relabelWeight_good_swap
    (weight : Fin 4 → Fin 8 → ℝ)
    (agents : Equiv.Perm (Fin 4))
    (goods : Equiv.Perm (Fin 8))
    (left right : Fin 8) :
    relabelWeight weight agents (goods.trans (Equiv.swap left right)) =
      fun agent good => relabelWeight weight agents goods agent
        (Equiv.swap left right good) := by
  funext agent good
  simp [relabelWeight, relabelAgentsWeight, relabelGoodsWeight]

private theorem matrix_lt_agent_swap
    (weight : Fin 4 → Fin 8 → ℝ)
    {left right : Fin 4}
    (left_lt_right : left < right)
    (bad_order :
      toLex (weight left) < toLex (weight right)) :
    MatrixLex weight <
      MatrixLex (fun agent => weight (Equiv.swap left right agent)) := by
  refine ⟨left, ?_, ?_⟩
  · intro earlier earlier_lt
    have earlier_ne_left : earlier ≠ left := earlier_lt.ne
    have earlier_ne_right : earlier ≠ right :=
      (earlier_lt.trans left_lt_right).ne
    simp [MatrixLex,
      Equiv.swap_apply_of_ne_of_ne earlier_ne_left earlier_ne_right]
  · simpa [MatrixLex] using bad_order

private theorem row_eq_after_column_swap
    (weight : Fin 4 → Fin 8 → ℝ)
    (agent : Fin 4)
    {left right : Fin 8}
    (equal : weight agent left = weight agent right) :
    weight agent =
      fun good => weight agent (Equiv.swap left right good) := by
  funext good
  by_cases left_eq_right : left = right
  · subst right
    simp
  by_cases good_eq_left : good = left
  · subst good
    simp [equal]
  by_cases good_eq_right : good = right
  · subst good
    simp [equal]
  rw [Equiv.swap_apply_of_ne_of_ne good_eq_left good_eq_right]

private theorem row_lt_after_column_swap
    (weight : Fin 4 → Fin 8 → ℝ)
    (agent : Fin 4)
    {left right : Fin 8}
    (left_lt_right : left < right)
    (bad_order : weight agent left < weight agent right) :
    toLex (weight agent) <
      toLex
        (fun good => weight agent (Equiv.swap left right good)) := by
  refine ⟨left, ?_, ?_⟩
  · intro earlier earlier_lt
    have earlier_ne_left : earlier ≠ left := earlier_lt.ne
    have earlier_ne_right : earlier ≠ right :=
      (earlier_lt.trans left_lt_right).ne
    simp [Equiv.swap_apply_of_ne_of_ne
      earlier_ne_left earlier_ne_right]
  · simpa using bad_order

private theorem matrix_lt_good_swap
    (weight : Fin 4 → Fin 8 → ℝ)
    {left right : Fin 8}
    (left_lt_right : left < right)
    (bad_order :
      toLex (fun agent => weight agent left) <
        toLex (fun agent => weight agent right)) :
    MatrixLex weight <
      MatrixLex
        (fun agent good =>
          weight agent (Equiv.swap left right good)) := by
  rcases bad_order with ⟨agent, earlier_equal, agent_lt⟩
  refine ⟨agent, ?_, ?_⟩
  · intro earlier earlier_lt
    exact congrArg toLex
      (row_eq_after_column_swap weight earlier
        (earlier_equal earlier earlier_lt))
  · exact row_lt_after_column_swap weight agent
      left_lt_right agent_lt

theorem exists_stabilized_relabel
    {Pattern : Type*}
    [DecidableEq Pattern]
    (weight : Fin 4 → Fin 8 → ℝ)
    (patterns : Fin 4 → Pattern)
    (used : Finset (Fin 8)) :
    ∃ agentPermutation : Equiv.Perm (Fin 4),
      ∃ goodPermutation : Equiv.Perm (Fin 8),
        AgentPatternPreserving patterns agentPermutation ∧
        GoodSetFixing used goodPermutation ∧
        (∀ left right, left < right →
          patterns left = patterns right →
          RowLexGE
            (relabelWeight weight agentPermutation goodPermutation)
            left right) ∧
        (∀ left right, left < right →
          left ∉ used → right ∉ used →
          ColumnLexGE
            (relabelWeight weight agentPermutation goodPermutation)
            left right) := by
  classical
  let candidates :
      Finset
        (Equiv.Perm (Fin 4) × Equiv.Perm (Fin 8)) :=
    Finset.univ.filter fun candidate =>
      AgentPatternPreserving patterns candidate.1 ∧
      GoodSetFixing used candidate.2
  have identity_mem :
      (Equiv.refl (Fin 4), Equiv.refl (Fin 8)) ∈ candidates := by
    simp [candidates, AgentPatternPreserving, GoodSetFixing]
  obtain ⟨chosen, chosen_mem, maximal⟩ :=
    Finset.exists_max_image candidates
      (fun candidate =>
        MatrixLex
          (relabelWeight weight candidate.1 candidate.2))
      ⟨_, identity_mem⟩
  have chosen_allowed :
      AgentPatternPreserving patterns chosen.1 ∧
      GoodSetFixing used chosen.2 :=
    (Finset.mem_filter.mp chosen_mem).2
  refine ⟨chosen.1, chosen.2, chosen_allowed.1,
    chosen_allowed.2, ?_, ?_⟩
  · intro left right left_lt_right same_pattern
    rw [RowLexGE]
    by_contra not_ordered
    have bad_order :
        toLex
            (relabelWeight weight chosen.1 chosen.2 left) <
          toLex
            (relabelWeight weight chosen.1 chosen.2 right) :=
      lt_of_not_ge not_ordered
    let swapped :
        Equiv.Perm (Fin 4) × Equiv.Perm (Fin 8) :=
      ((Equiv.swap left right).trans chosen.1, chosen.2)
    have swapped_mem : swapped ∈ candidates := by
      apply Finset.mem_filter.mpr
      refine ⟨Finset.mem_univ _, ?_, chosen_allowed.2⟩
      exact compose_agent_preserving
        (swap_preserves_pattern same_pattern) chosen_allowed.1
    have cannot_increase := maximal swapped swapped_mem
    have strictly_increases :
        MatrixLex
            (relabelWeight weight chosen.1 chosen.2) <
          MatrixLex
            (relabelWeight weight swapped.1 swapped.2) := by
      rw [show relabelWeight weight swapped.1 swapped.2 =
          fun agent =>
            relabelWeight weight chosen.1 chosen.2
              (Equiv.swap left right agent) by
        exact relabelWeight_agent_swap
          weight chosen.1 chosen.2 left right]
      exact matrix_lt_agent_swap
        (relabelWeight weight chosen.1 chosen.2)
        left_lt_right bad_order
    exact (not_lt_of_ge cannot_increase) strictly_increases
  · intro left right left_lt_right left_unused right_unused
    rw [ColumnLexGE]
    by_contra not_ordered
    have bad_order :
        toLex
            (fun agent =>
              relabelWeight weight chosen.1 chosen.2 agent left) <
          toLex
            (fun agent =>
              relabelWeight weight chosen.1 chosen.2 agent right) :=
      lt_of_not_ge not_ordered
    let swapped :
        Equiv.Perm (Fin 4) × Equiv.Perm (Fin 8) :=
      (chosen.1, chosen.2.trans (Equiv.swap left right))
    have swapped_mem : swapped ∈ candidates := by
      apply Finset.mem_filter.mpr
      refine ⟨Finset.mem_univ _, chosen_allowed.1, ?_⟩
      exact compose_good_fixing chosen_allowed.2
        (swap_fixes_used used left_unused right_unused)
    have cannot_increase := maximal swapped swapped_mem
    have strictly_increases :
        MatrixLex
            (relabelWeight weight chosen.1 chosen.2) <
          MatrixLex
            (relabelWeight weight swapped.1 swapped.2) := by
      rw [show relabelWeight weight swapped.1 swapped.2 =
          fun agent good =>
            relabelWeight weight chosen.1 chosen.2 agent
              (Equiv.swap left right good) by
        exact relabelWeight_good_swap
          weight chosen.1 chosen.2 left right]
      exact matrix_lt_good_swap
        (relabelWeight weight chosen.1 chosen.2)
        left_lt_right bad_order
    exact (not_lt_of_ge cannot_increase) strictly_increases

def favoriteUsed
    (favorites : Fin 4 → Fin 8) : Finset (Fin 8) :=
  Finset.univ.image favorites

def prefixUsed
    (favorites seconds : Fin 4 → Fin 8) : Finset (Fin 8) :=
  favoriteUsed favorites ∪ favoriteUsed seconds

def FavoriteStabilizer
    (weight : Fin 4 → Fin 8 → ℝ)
    (favorites : Fin 4 → Fin 8) : Prop :=
  (∀ left right, left < right →
    favorites left = favorites right →
    RowLexGE weight left right) ∧
  (∀ left right, left < right →
    left ∉ favoriteUsed favorites →
    right ∉ favoriteUsed favorites →
    ColumnLexGE weight left right)

def PrefixStabilizer
    (weight : Fin 4 → Fin 8 → ℝ)
    (favorites seconds : Fin 4 → Fin 8) : Prop :=
  (∀ left right, left < right →
    (favorites left, seconds left) =
      (favorites right, seconds right) →
    RowLexGE weight left right) ∧
  (∀ left right, left < right →
    left ∉ prefixUsed favorites seconds →
    right ∉ prefixUsed favorites seconds →
    ColumnLexGE weight left right)

theorem exists_favorite_stabilized_counterexample
    (weight : Fin 4 → Fin 8 → ℝ)
    (favorites : Fin 4 → Fin 8)
    (strict : StrictFavorites weight favorites)
    (no_efx : ¬AdmitsEFX weight) :
    ∃ agentPermutation : Equiv.Perm (Fin 4),
      ∃ goodPermutation : Equiv.Perm (Fin 8),
        let stabilized :=
          relabelWeight weight agentPermutation goodPermutation
        StrictFavorites stabilized favorites ∧
        ¬AdmitsEFX stabilized ∧
        FavoriteStabilizer stabilized favorites := by
  obtain ⟨agents, goods, agents_preserve, goods_fix,
      rows_sorted, columns_sorted⟩ :=
    exists_stabilized_relabel weight favorites
      (favoriteUsed favorites)
  refine ⟨agents, goods, ?_, ?_, rows_sorted, columns_sorted⟩
  · apply strictFavorites_relabel
      weight favorites favorites strict agents goods
    intro agent
    rw [agents_preserve]
    exact goods_fix _ (Finset.mem_image_of_mem favorites
      (Finset.mem_univ agent))
  · intro relabeled_efx
    exact no_efx
      ((admitsEFX_relabelWeight_iff weight agents goods).mp
        relabeled_efx)

theorem exists_prefix_stabilized_counterexample
    (weight : Fin 4 → Fin 8 → ℝ)
    (favorites seconds : Fin 4 → Fin 8)
    (strict : StrictRankingPrefix weight favorites seconds)
    (no_efx : ¬AdmitsEFX weight) :
    ∃ agentPermutation : Equiv.Perm (Fin 4),
      ∃ goodPermutation : Equiv.Perm (Fin 8),
        let stabilized :=
          relabelWeight weight agentPermutation goodPermutation
        StrictRankingPrefix stabilized favorites seconds ∧
        ¬AdmitsEFX stabilized ∧
        PrefixStabilizer stabilized favorites seconds := by
  let patterns : Fin 4 → Fin 8 × Fin 8 :=
    fun agent => (favorites agent, seconds agent)
  obtain ⟨agents, goods, agents_preserve, goods_fix,
      rows_sorted, columns_sorted⟩ :=
    exists_stabilized_relabel weight patterns
      (prefixUsed favorites seconds)
  have favorites_preserved :
      ∀ agent, favorites (agents agent) = favorites agent := by
    intro agent
    exact congrArg Prod.fst (agents_preserve agent)
  have seconds_preserved :
      ∀ agent, seconds (agents agent) = seconds agent := by
    intro agent
    exact congrArg Prod.snd (agents_preserve agent)
  have favorites_mapped :
      ∀ agent, goods (favorites (agents agent)) = favorites agent := by
    intro agent
    rw [favorites_preserved]
    exact goods_fix _
      (Finset.mem_union_left _
        (Finset.mem_image_of_mem favorites (Finset.mem_univ agent)))
  have seconds_mapped :
      ∀ agent, goods (seconds (agents agent)) = seconds agent := by
    intro agent
    rw [seconds_preserved]
    exact goods_fix _
      (Finset.mem_union_right _
        (Finset.mem_image_of_mem seconds (Finset.mem_univ agent)))
  refine ⟨agents, goods, ?_, ?_, ?_, columns_sorted⟩
  · exact strictRankingPrefix_relabel
      weight favorites seconds favorites seconds strict
      agents goods favorites_mapped seconds_mapped
  · intro relabeled_efx
    exact no_efx
      ((admitsEFX_relabelWeight_iff weight agents goods).mp
        relabeled_efx)
  · intro left right left_lt_right same_prefix
    exact rows_sorted left right left_lt_right same_prefix

def HasFavoriteStabilizedCounterexample
    (favorites : Fin 4 → Fin 8) : Prop :=
  ∃ weight : Fin 4 → Fin 8 → ℝ,
    StrictFavorites weight favorites ∧
    ¬AdmitsEFX weight ∧
    FavoriteStabilizer weight favorites

def HasPrefixStabilizedCounterexample
    (seconds : Fin 4 → Fin 8) : Prop :=
  ∃ weight : Fin 4 → Fin 8 → ℝ,
    StrictRankingPrefix weight canonical4 seconds ∧
    ¬AdmitsEFX weight ∧
    PrefixStabilizer weight canonical4 seconds

theorem relabelsIntoFavoriteCell_has_stabilized
    (weight : Fin 4 → Fin 8 → ℝ)
    (favorites : Fin 4 → Fin 8)
    (cell : RelabelsIntoFavoriteCell weight favorites) :
    HasFavoriteStabilizedCounterexample favorites := by
  rcases cell with ⟨initialAgents, initialGoods, strict, no_efx⟩
  obtain ⟨agents, goods, finalStrict, finalNoEFX, stabilized⟩ :=
    exists_favorite_stabilized_counterexample
      (relabelWeight weight initialAgents initialGoods)
      favorites strict no_efx
  exact ⟨relabelWeight
    (relabelWeight weight initialAgents initialGoods) agents goods,
    finalStrict, finalNoEFX, stabilized⟩

theorem relabelsIntoSecondCell_has_stabilized
    (weight : Fin 4 → Fin 8 → ℝ)
    (seconds : Fin 4 → Fin 8)
    (cell : RelabelsIntoSecondCell weight seconds) :
    HasPrefixStabilizedCounterexample seconds := by
  rcases cell with ⟨initialAgents, initialGoods, strict, no_efx⟩
  obtain ⟨agents, goods, finalStrict, finalNoEFX, stabilized⟩ :=
    exists_prefix_stabilized_counterexample
      (relabelWeight weight initialAgents initialGoods)
      canonical4 seconds strict no_efx
  exact ⟨relabelWeight
    (relabelWeight weight initialAgents initialGoods) agents goods,
    finalStrict, finalNoEFX, stabilized⟩

theorem strict_counterexample_eight_stabilized_coverage
    (weight : Fin 4 → Fin 8 → ℝ)
    (nonnegative : ∀ agent good, 0 ≤ weight agent good)
    (favorites seconds : Fin 4 → Fin 8)
    (strict : StrictRankingPrefix weight favorites seconds)
    (no_efx : ¬AdmitsEFX weight) :
    HasFavoriteStabilizedCounterexample canonical211 ∨
    HasFavoriteStabilizedCounterexample canonical31 ∨
    HasFavoriteStabilizedCounterexample canonical22 ∨
    HasPrefixStabilizedCounterexample second1111 ∨
    HasPrefixStabilizedCounterexample second4 ∨
    HasPrefixStabilizedCounterexample second31 ∨
    HasPrefixStabilizedCounterexample second22 ∨
    HasPrefixStabilizedCounterexample second211 := by
  rcases strict_counterexample_eight_cell_coverage
      weight nonnegative favorites seconds strict no_efx with
    cell211 | cell31 | cell22 | second1111Cell | second4Cell |
      second31Cell | second22Cell | second211Cell
  · exact Or.inl
      (relabelsIntoFavoriteCell_has_stabilized
        weight canonical211 cell211)
  · exact Or.inr (Or.inl
      (relabelsIntoFavoriteCell_has_stabilized
        weight canonical31 cell31))
  · exact Or.inr (Or.inr (Or.inl
      (relabelsIntoFavoriteCell_has_stabilized
        weight canonical22 cell22)))
  · exact Or.inr (Or.inr (Or.inr (Or.inl
      (relabelsIntoSecondCell_has_stabilized
        weight second1111 second1111Cell))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl
      (relabelsIntoSecondCell_has_stabilized
        weight second4 second4Cell)))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl
      (relabelsIntoSecondCell_has_stabilized
        weight second31 second31Cell))))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl
      (relabelsIntoSecondCell_has_stabilized
        weight second22 second22Cell)))))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr
      (relabelsIntoSecondCell_has_stabilized
        weight second211 second211Cell)))))))

end EFX48

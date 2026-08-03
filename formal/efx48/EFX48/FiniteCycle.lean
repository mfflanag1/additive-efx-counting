import Mathlib.Dynamics.PeriodicPts.Lemmas
import Mathlib.GroupTheory.Perm.Cycle.Concrete

namespace EFX48

open Function

theorem exists_periodic_point
    {α : Type*} [Finite α] [Nonempty α] (next : α → α) :
    ∃ point, point ∈ Function.periodicPts next := by
  classical
  let start : α := Classical.choice inferInstance
  obtain ⟨m, n, equal_iterates, different⟩ :
      ∃ m n,
        next^[m] start = next^[n] start ∧ m ≠ n := by
    simpa [Function.Injective] using
      not_injective_infinite_finite (fun step : ℕ => next^[step] start)
  rcases lt_or_gt_of_ne different with before | after
  · let point := next^[m] start
    refine ⟨point, Function.mk_mem_periodicPts (n := n - m) (by omega) ?_⟩
    unfold Function.IsPeriodicPt Function.IsFixedPt
    dsimp [point]
    rw [← Function.iterate_add_apply, Nat.sub_add_cancel before.le]
    exact equal_iterates.symm
  · let point := next^[n] start
    refine ⟨point, Function.mk_mem_periodicPts (n := m - n) (by omega) ?_⟩
    unfold Function.IsPeriodicPt Function.IsFixedPt
    dsimp [point]
    rw [← Function.iterate_add_apply, Nat.sub_add_cancel after.le]
    exact equal_iterates

theorem periodicOrbit_formPerm_apply_self
    {α : Type*} [DecidableEq α]
    {next : α → α} {point : α}
    (periodic : point ∈ Function.periodicPts next)
    (moves : next point ≠ point) :
    (Function.periodicOrbit next point).formPerm
        (Function.nodup_periodicOrbit (f := next) (x := point)) point =
      next point := by
  let period := Function.minimalPeriod next point
  let orbitList :=
    (List.range period).map fun step => next^[step] point
  have period_positive : 0 < period :=
    Function.minimalPeriod_pos_of_mem_periodicPts periodic
  have period_not_one : period ≠ 1 := by
    intro period_one
    have fixed := Function.iterate_minimalPeriod (f := next) (x := point)
    change next^[period] point = point at fixed
    rw [period_one, Function.iterate_one] at fixed
    exact moves fixed
  have period_at_least_two : 2 ≤ period := by omega
  have orbit_nodup : orbitList.Nodup := by
    simpa [orbitList, period, Function.periodicOrbit] using
      Function.nodup_periodicOrbit (f := next) (x := point)
  have orbit_length : orbitList.length = period := by
    simp [orbitList]
  have two_entries : 1 < orbitList.length := by
    rw [orbit_length]
    omega
  have step :=
    List.formPerm_apply_getElem_zero orbitList orbit_nodup two_entries
  have first_entry : orbitList[0] = point := by
    simp [orbitList, period_positive]
  have second_entry : orbitList[1] = next point := by
    simp [orbitList, period_at_least_two, Function.iterate_one]
  change Cycle.formPerm (orbitList : Cycle α) _ point = next point
  rw [Cycle.formPerm_coe]
  simpa [first_entry, second_entry] using step

theorem periodicOrbit_formPerm_apply
    {α : Type*} [DecidableEq α]
    {next : α → α} {point member : α}
    (periodic : point ∈ Function.periodicPts next)
    (moves : ∀ item, next item ≠ item)
    (member_mem : member ∈ Function.periodicOrbit next point) :
    (Function.periodicOrbit next point).formPerm
        (Function.nodup_periodicOrbit (f := next) (x := point)) member =
      next member := by
  rcases (Function.mem_periodicOrbit_iff periodic).1 member_mem with
    ⟨steps, rfl⟩
  have iterate_periodic :
      next^[steps] point ∈ Function.periodicPts next := by
    rcases periodic with ⟨period, period_positive, point_periodic⟩
    exact ⟨period, period_positive, point_periodic.apply_iterate steps⟩
  have at_head := periodicOrbit_formPerm_apply_self
    iterate_periodic (moves (next^[steps] point))
  have same_orbit :=
    Function.periodicOrbit_apply_iterate_eq periodic steps
  simpa only [same_orbit] using at_head

theorem exists_cycle_permutation
    {α : Type*} [Fintype α] [Nonempty α] [DecidableEq α]
    (next : α → α) (moves : ∀ item, next item ≠ item) :
    ∃ permutation : Equiv.Perm α,
      (∀ item, permutation item ≠ item → permutation item = next item) ∧
      ∃ item, permutation item ≠ item := by
  classical
  rcases exists_periodic_point next with ⟨point, periodic⟩
  let orbit := Function.periodicOrbit next point
  let orbit_nodup : orbit.Nodup :=
    Function.nodup_periodicOrbit (f := next) (x := point)
  let permutation := orbit.formPerm orbit_nodup
  refine ⟨permutation, ?_, ?_⟩
  · intro item moved
    have item_mem : item ∈ orbit := by
      by_contra item_not_mem
      exact moved (Cycle.formPerm_eq_self_of_notMem
        orbit orbit_nodup item item_not_mem)
    exact periodicOrbit_formPerm_apply periodic moves item_mem
  · refine ⟨point, ?_⟩
    have point_mem := Function.self_mem_periodicOrbit periodic
    have point_step :=
      periodicOrbit_formPerm_apply periodic moves point_mem
    intro fixed
    exact moves point (point_step.symm.trans fixed)

end EFX48

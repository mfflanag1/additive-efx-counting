import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Finset.Max
import Mathlib.Data.Real.Basic

namespace EFX48

open Finset

variable {Agent Good : Type*}
variable [Fintype Agent] [DecidableEq Agent]
variable [Fintype Good] [DecidableEq Good]

abbrev Allocation (Agent Good : Type*) := Agent → Finset Good

def ValidAllocation (allocation : Allocation Agent Good) : Prop :=
  ∀ good, ∃! owner, good ∈ allocation owner

def additiveValue (weight : Agent → Good → ℝ) (i : Agent)
    (bundle : Finset Good) : ℝ :=
  ∑ good ∈ bundle, weight i good

noncomputable def threshold (weight : Agent → Good → ℝ) (i : Agent)
    (bundle : Finset Good) : ℝ :=
  if nonempty : bundle.Nonempty then
    (bundle.image fun good => additiveValue weight i (bundle.erase good)).max'
      (nonempty.image fun good => additiveValue weight i (bundle.erase good))
  else 0

def EFX (weight : Agent → Good → ℝ) (allocation : Allocation Agent Good) :
    Prop :=
  ∀ observer target, observer ≠ target →
    ∀ good ∈ allocation target,
      additiveValue weight observer (allocation observer) ≥
        additiveValue weight observer ((allocation target).erase good)

def AdmitsEFX (weight : Agent → Good → ℝ) : Prop :=
  ∃ allocation : Allocation Agent Good,
    ValidAllocation allocation ∧ EFX weight allocation

def removeOwnedGood (allocation : Allocation Agent Good) (owner : Agent)
    (good : Good) : Allocation Agent Good :=
  fun agent => if agent = owner then (allocation owner).erase good
    else allocation agent

def OwnerRemovable (weight : Agent → Good → ℝ)
    (allocation : Allocation Agent Good) (owner : Agent) (good : Good) : Prop :=
  good ∈ allocation owner ∧ EFX weight (removeOwnedGood allocation owner good)

end EFX48

# Mixed-margin Hamiltonian charity-path checkpoint

**Date:** 2026-08-11

**Status:** cap-free reduction of the mixed-margin goal to one full-owner
critical-top-up substitution separator; the goal is not yet closed

## Authoritative state

At an exact complete signed-transfer state, the PI-free rank-four response
matching is a Hamiltonian path from the unique owner hole through all four
owners to charity.  An old decorated response into the hole closes a prefix
owner cycle in one pivot.  Every physical response/release label is fixed by
the complete signed decoration; a changed label is permanent augmentation.

Let `D subseteq Y_t` be the recurrent current-safe response assigned to
source `s`, and let an observer's old assigned-core margin be below its debt
against `D`.

## Exhaustive cap-free reduction

### 1. Non-target observers

For every underfunded observer `h != t,s`, write the exact path target as

\[
 Y_h=C_h\mathbin{\dot\cup}R_h,
\]

where `C_h` is the old incoming core and `R_h` its released residual.  Giving
`R_h` back to `h` either pays the debt or creates a new enlarged-target
response.  If it still does not pay, then

\[
 v_h(C_h)>v_h(A_h)>v_h(X_h),
\]

so the old common-safe core `C_h` is a self-response: it is new augmentation,
PI, or physical component growth.  Thus only target owner `t` can remain.

### 2. Direct-safe target selection

Keep every other owner at the paid state and globally choose an
inclusion-minimal `Q subseteq Y_t` meeting `t`'s priority/direct floor.  If
`Q` is current-safe, replacing `Y_t` by `Q` is a partial EFX lex endpoint;
the discarded packet is handled by arbitrary-charity collapse.

If `Q` is unsafe, globally minimal extraction gives a current-safe response.
A new response augments.  Exact recurrence of `D` forces

\[
 Q=D\mathbin{\dot\cup}K,
 \qquad K\ne\varnothing,                          \tag{1}
\]

where every good of `Q` is critical to `t`'s direct floor.  The mixed debt is
therefore exactly a recurrent critical top-up packet `K`, not an arbitrary
observer inequality.

### 3. Two-owner plus charity exhaustion

For every `J subseteq D`, let source `s` receive `D-J` and target owner `t`
receive

\[
 (Y_t\setminus D)+Y_s+J.                          \tag{2}

Also include giving the complete charity packet to `s` and parking any one
good from the resulting source pool.  These are canonical structured
candidates.  The final selector additionally ranges over every three-way
partition between `s`, `t`, and nonempty charity of the complete pool

\[
 Y_t\mathbin{\dot\cup}Y_s\mathbin{\dot\cup}P.     \tag{3}

A directly feasible partition is EFX/lex or gives a new response from one
of its two changed targets.  Failure excludes all two-owner-plus-charity
partitions, not merely a fixed tree or bounded packet menu.

### 4. Outside-pool recruitment

After failure of (3), the smallest possible operation is a packet from one
of the two remaining owners' signed-transfer components, a decorated
source/root change, or replacement of `D`.  Component-wide return selection
already maximizes over every redistribution of a recruited component while
retaining its owners' protected floors.  Recruiting one owner grows coverage
to three; recruiting once more saturates all four owners.  A new source,
core, signed packet, or release label is permanent augmentation.

## Exact surviving separator

After source/core saturation and full-owner recruitment, the sole unproved
state has all of the following simultaneously:

1. the exact old current-safe response `D` and nonempty target-critical
   top-up `K` from (1);
2. failure of every two-owner-plus-charity partition (2)--(3);
3. failure of every full-component redistribution preserving the protected
   floors of recruited owners;
4. failure even after crediting the decorated source's entire current
   surplus and every priority-valid base-floor handoff;
5. failed direct safety for the sacrifice-eligible source; and
6. no new response core, source/root, signed transfer, supplier, or release
   label.

This is the exact full-owner **critical-top-up substitution separator**.  To
finish the goal one must prove that the globally lex-maximal GG inequalities
force a third-owner substitute for `K`, a source/root change, or a new core;
otherwise one must instantiate all six clauses in an exact globally maximal
GG countermodel.  Local scalar margins, another history ledger, and bounded
cells cannot decide it.

## Verification and claim boundary

[`mixed_margin_hamiltonian_charity_path_composition_audit.json`](mixed_margin_hamiltonian_charity_path_composition_audit.json)
records and hashes every dependency in this reduction.  Its audits verify
the algebraic implications, exact finite selectors, matching classification,
and component-cardinality exhaustion.

The manifest establishes a replayable reduction.  It does not eliminate the
six-clause separator, prove the mixed-margin theorem, close GG, or prove
four-agent/general additive EFX.

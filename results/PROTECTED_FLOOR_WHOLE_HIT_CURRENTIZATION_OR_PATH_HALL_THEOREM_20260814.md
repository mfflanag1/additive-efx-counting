# Protected-floor whole-hit currentization or path-Hall theorem

**Date:** 2026-08-14

**Status:** verified intermediate currentization theorem. Its nonroot
source-inactive branch is superseded by the desire-free envelope descent; its
root branch is superseded by the desire-free complete-pool reduction.

## Protected-floor input

Let `Z` be the actual canonical ledger-free allocation, with current
utilities above the typed protected floors:

\[
 v_i(Z_i)\ge F_i\qquad(i\in N).                  \tag{1}
\]

Let the named packet `K` remain in holder target `Z_h`. Suppose a globally
minimum protected-floor-safe core `D subseteq Z_h` has source `t` and hits
the whole packet:

\[
 K\subseteq D,
 \qquad v_t(D)>F_t.                              \tag{2}
\]

The protected source need not currently prefer `D` to `Z_t`; that is the
base-floor debt which cannot be silently ignored.

## Source-inactive branch

If

\[
 v_t(Z_h)\le v_t(Z_t),                           \tag{3}
\]

then no subset of `Z_h` is current-desired by `t`. The protected response is
entirely explained by the gap between the lower floor and current utility:

\[
 0<v_t(D)-F_t
 \le v_t(Z_t)-F_t.                               \tag{4}
\]

This is the exact **source-inactive debt**. It is not a current response and
cannot enter a PI/current-bundle compensation cycle without a separately
valid priority handoff or top-up. Equation (4), the floor type, and source
label remain in the terminal record.

## Currentization branch

Suppose instead that

\[
 v_t(Z_h)>v_t(Z_t).                              \tag{5}
\]

Among every owner `e` and subset `E subseteq Z_h` with

\[
 v_e(E)>v_e(Z_e),                                \tag{6}
\]

choose a pair of globally minimum cardinality with fixed tie-breaking. The
family is nonempty by (5). The selected `E` is current-safe: if some observer
`j` had `tau_j(E)>v_j(Z_j)`, deleting a least-`j` good would produce a
strictly smaller subset satisfying (6) for source `j`.

Exactly one support branch holds.

1. `E cap K` is empty: a genuine ledger-free current response is obtained.
2. `E cap K` is nonempty and proper: the collision packet strictly shrinks.
3. `K subseteq E`: put
   \[
   L'=Z_h\setminus E.                            \tag{7}
   \]
   Here `L'` is disjoint from `K` and may be empty. Source `e` is distinct
   from `h`, because no subset of an owner's own current bundle is strictly
   current-desired by that owner.

## Path-Hall routing after currentization

In branch 3, give `E` to `e` and route the old bundle `Z_e` through any
simple path of the other two owners back to `h`, finally assigning
`L'+Z_j` to `h`. The proof of the four-owner current-bundle path-Hall theorem
does not require `L'` to be nonempty: its payment identity is still

\[
 v_h(L'+Z_j)\ge v_h(L'+E)
 \quad\Longleftrightarrow\quad
 v_h(Z_j)\ge v_h(E).                             \tag{8}
\]

All five paths are therefore available with `D` replaced by `E`. A paid path
gives an admitted supplier cycle whose only new mixed target is disjoint from
`K`; otherwise the exact five-path Hall cut holds with sink benchmark `E`.
Other retired support in moved old bundles is normalized before execution.

Thus every protected-floor whole hit has one of:

1. source-inactive debt (3)--(4);
2. a ledger-free current response;
3. a proper retired-packet reduction;
4. a paid current-bundle path; or
5. the exact five-path Hall cut for a current-safe/current-desired core.

## GG-role consequence

The generic `T_{L,times}^*` contract does not fix `h,e` to one universal pair
among `r,q,c,s`: collisions can originate in several `G0--G10` operations.
Accordingly, base GG champion inequalities can be applied only after the
originating transition supplies the required role identification. The
currentization theorem is role-free and therefore valid across all origins;
any later role-specific closure must cite the relevant transition premise.

## Claim boundary

This theorem handles the currentization step and cleanly separates the exact
source-inactive debt from current path-Hall failure. It does not eliminate
(3)--(4), force one of the five paths, clear other retired support, supply a
priority-valid top-up, close `T_{L,times}^*`, or prove four-agent/general
EFX.

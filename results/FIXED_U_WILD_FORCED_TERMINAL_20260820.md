# Fixed-U wild-and-forced terminal profile

**Date:** 2026-08-20  
**Status:** exact countermodel to the tame-covering-menu chart theorem. The
realization gap recorded below is now closed by
`FIXED_U_WILD_A1_ALL_REALIZATIONS_LEMMA_20260820.md`; the universal fixed-`U`
theorem remains open.

> **2026-08-20 continuation:** The proposed three-through-seven-good campaign
> closed more strongly than anticipated. One four-edge allocation keeps all
> `a1` goods together and is EFX for every feasible `a1` realization. Treat
> the “remaining problem” and “not proved” items below as historical motivation,
> superseded by the all-realizations lemma.

## Headline

The first genuine wild-and-forced profile has been found.

It satisfies the complete exact-response form-2 fixed-`U` master and defeats
the widest sound tame family: in its canonical physical realization, no
complete four-support-edge EFX allocation exists unless some wild role is
split. This verdict survives an independent Boolean encoding.

It is **not** a four-edge EFX counterexample. Allowing wild roles to split
produces an exact complete EFX allocation after splitting only `a1`. Thus the
profile refutes the hoped-for tame-covering-menu chart theorem, but sharpens
the active fixed-`U` problem to arbitrary realizations of one wild role.

## How it was reached

The certificate-complete cut pool contained 194 audited cuts. Four equivalent
master front ends were tested on exactly those assertions:

| mode | verdict | check time |
|---|---:|---:|
| generic SMT | SAT | 22.96s |
| QF_LRA, seed 820 | SAT | 33.56s |
| ITE elimination | SAT | 57.73s |
| contextual simplification | UNKNOWN | 180.01s |

The generic SMT continuation added four more valid certificates at iterations
194–197—three whole-role and one splitting tame role `k`—then reached the
terminal profile at iteration 198. A later in-place replay advanced seven
additional, unrelated profiles before being paused. The terminal profile was
recovered losslessly from its already frozen rational repair and now lives in
the separate immutable file `fixed_u_wild_forced_terminal_profile_20260820.json`.
That recovery replays SAT against the complete declared form-2 master.

The current durable ledger contains 205 fully replayable cuts:

```text
whole-role certificates       200
one-tame-role certificates      5
terminal discovery iteration  198
current cut count             205
```

## Exact terminal classification

Role slacks `rho = min_i floor(T_i/M_i)` are:

```text
wild:      a0=9, a1=7, j=4, k=3, gq=3
tame:      l=2, e=2, m=2
singleton: h, q0, gr, p
```

The widest realization-free oracle returns
`UNSAT_NO_TAME_SPLIT_ALLOCATION`. Equivalently, in the aligned canonical
realization, every complete four-edge EFX allocation splits at least one role
from `{a0,a1,j,k,gq}`. This is exactly the failure shape isolated in the Aug-16
identity-aware handoff; unlike all earlier reported obstructions, it is not a
selector-cap artifact.

An independent encoding rebuilds the 20 physical goods, assigns every good
directly to an owner, enforces at most four supplier/recipient pairs and every
individual deletion inequality, and constrains the two goods of every wild
role to share a recipient. It independently returns `UNSAT`.

Therefore:

> The universal tame-covering-menu statement for the declared exact-response
> form-2 chart is false.

Theorem 1 of `IDENTITY_AWARE_SLACK_TWO_20260816.md` remains correct as a
conditional realization-free reduction. This profile proves that its tame-menu
hypothesis is not guaranteed by the chart premises.

## Exact wild-role repair

Removing the no-wild-split restriction gives `SAT`. The minimum split count is
one, and the split role is wild `a1` with slack seven. The allocation is:

```text
r: a0 + k + q0
q: high(a1) + j
d: low(a1) + h + m + gq + gr
s: l + e + p
```

Its four frozen-support edges are:

```text
charity -> s
q       -> r
r       -> d
r       -> q
```

Every EFX deletion inequality has been rechecked in exact rational arithmetic.
The minimum slack is `3/481`. The direct decision reports zero split roles
`UNSAT` and one split role `SAT`.

This proves that the terminal profile does not refute the active four-edge
theorem in its canonical two-good realization.

## What the remaining problem now is

The only non-realization-free operation in the repair is the split of `a1`.
Since `rho(a1)=7`, a physical realization may give that role anywhere from two
to seven goods, with different observers attaining their minima at different
goods. The canonical repair aligns every observer's minimum on one of two
goods; it does not cover these wider identity patterns.

The next decisive target is therefore finite and exact:

> Holding the terminal `(T,M)` profile fixed, range over every physical
> realization of `a1` with three through seven goods and every minimum-witness
> identity pattern. Either prove that one of the four-edge wild-split
> allocations always works, or produce a positive-rational realization with
> no four-edge complete EFX allocation.

The first live cell is three goods in `a1`, leaving every other role in its
canonical realization. For each observer, the three positive values must sum
to `T_i(a1)`, have minimum `M_i(a1)`, and may choose different minimizing
goods. Up to permutation, only the set partitions of four observer witnesses
into at most three blocks are needed. A CEGAR over those exact linear cells is
small enough to decide and directly attacks the active theorem:

- `SAT` with no allocation is an exact local four-edge countermodel;
- `UNSAT` for every cell proves the three-good `a1` rung and supplies cores for
  an analytic wild-split lemma.

## Independent audit

```bash
python -m tracks.parkability.audit_fixed_u_wild_forced_terminal \
  --profile results/fixed_u_wild_forced_terminal_profile_20260820.json \
  --repair results/fixed_u_terminal_profile_unrestricted_physical_decision_20260820.json \
  --output results/fixed_u_wild_forced_terminal_independent_audit_20260820.json
```

Recorded verdict:

```text
AUDIT_PASS
canonical goods                 20
no-wild-split decision       UNSAT
unrestricted decision          SAT
repair split role               a1
repair minimum EFX slack     3/481
```

Frozen SHA-256 values:

```text
55be177414982b9a001479b445c99319eee26859495478e559f643cc3d4044d6  results/fixed_u_wild_forced_terminal_profile_20260820.json
f38e303c26b249f7bbb463dd4cf9ee3c530302c11fb5e9b5797e34a7fb540010  results/fixed_u_multi_split_chart_cuts_20260820.jsonl
a47726679aa674b5cb902e5bc34dd1e9e35ddee3ea6c9dfbf1037e137cce47dc  results/fixed_u_terminal_profile_unrestricted_physical_decision_20260820.json
cde2d3c18ef6bc1369acfc3063c165c92ef00fcfe9ad73a51ccad89eb40c9e75  results/fixed_u_wild_forced_terminal_independent_audit_20260820.json
```

## Claim boundary

Proved:

1. an exact positive-rational form-2 profile satisfying all declared master
   premises has no tame covering menu;
2. this no-tame verdict is independently encoded and verified;
3. its canonical physical realization nevertheless has a complete four-edge
   EFX allocation splitting wild role `a1`; and
4. the frozen repair and all deletion inequalities pass an independent exact
   arithmetic audit.

Not proved:

1. existence or failure for every physical realization of the terminal
   profile;
2. the three-through-seven-good `a1` rungs;
3. a universal wild-role splitting lemma;
4. coverage of every saturated root-facing rank-three fixed-`U` state by the
   form-2 chart; or
5. the active universal four-edge theorem.

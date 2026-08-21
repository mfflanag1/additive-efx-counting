# Fixed-U split-switching completion theorem

**Date:** 2026-08-21  
**Status:** exact cap-free theorem for every physical realization of the
immutable terminal profile; independently proved; abstract generalization
tested on all 205 retained form-2 master profiles

## Headline

The immutable wild-and-forced terminal profile admits a complete EFX
allocation using at most four support-transfer edges for **every simultaneous
physical realization of every role** consistent with its fixed observer
totals and minima.

The proposed two-template split-switching selector is universal. In fact, the
result is stronger: each of its two template families is universal by itself.
There is therefore no selector-failure realization and no need to invoke the
unrestricted countermodel oracle.

Two one-line selectors suffice:

1. choose any `a1` good minimizing observer `q`, give it alone to `d`, and
   give every remaining `a1` good to `q` in template A;
2. choose any `k` good minimizing observer `r`, give it alone to `q`, and give
   every remaining `k` good to `r` in template B.

The first selector has worst certified EFX slack `3/481`; the second has worst
slack `23/1924`. Every other role remains whole, so its arbitrary internal
realization disappears into its prescribed total and minimum.

## Exact theorem

Fix the totals and minima in
`fixed_u_wild_forced_terminal_profile_20260820.json`. Replace every named role
by any finite nonempty set of positive goods which, in every observer row,
has exactly the prescribed total and minimum. The good labels are common
across observers, but their minimum-witness identities may be completely
different.

Then either of the following rules constructs a complete EFX allocation.

### Template A: the `q`-minimum `a1` anchor

Let `g` be any `a1` good with `v_q(g)=M_q(a1)`:

```text
d: g + h + m + gq + gr
q: (a1 - g) + j
r: a0 + k + q0
s: l + e + p
```

The support-transfer edges are exactly

```text
charity -> s
q       -> r
r       -> d
r       -> q
```

Every EFX deletion inequality holds with slack at least `3/481`.

### Template B: the `r`-minimum `k` anchor

Let `g` be any `k` good with `v_r(g)=M_r(k)`:

```text
d: l + m + gq + gr
q: g + j + q0 + p
r: (k - g) + a0 + a1
s: h + e
```

The support-transfer edges are exactly

```text
charity -> q
q       -> r
r       -> s
s       -> d
```

Every EFX deletion inequality holds with slack at least `23/1924`.

Because a prescribed minimum is attained, the selected anchor good always
exists. Both split roles necessarily contain at least two goods in this
profile, so the complementary packet is nonempty.

## Reusable anchor-good lemma

Let a split role `H` have observer totals `T_i` and minima `M_i`. A template
assigns whole-role unions `C_j` to each owner, sends one selected good `g` to
recipient `u`, and sends `H-g` to recipient `v`. Write `x_i=v_i(g)`. Then

```text
U_ij(x_i) = v_i(C_j)
          + 1[j=u] x_i
          + 1[j=v] (T_i-x_i).
```

For every observer `i`, target `j`, and possible deleted good, EFX is exactly

```text
U_ii(x_i) - U_ij(x_i) + deletion_value >= 0.                 (1)
```

For a whole role in `C_j`, it is necessary and sufficient to check its
prescribed minimum. For the selected good, check deletion value `x_i`. For
any complement good, the deletion value is at least `M_i`. Thus all relevant
expressions in (1) are affine in `x_i`.

If `g` is selected as an anchor observer's minimum, its anchor coordinate is
fixed at `M`; every other coordinate lies in `[M_i,T_i-M_i]`. Consequently:

> If the affine lower bound of every expression (1) is nonnegative over those
> intervals, choosing any anchor-minimum good produces EFX for every finite
> realization of `H`, independently of cardinality and witness identities.

The independent audit evaluates these endpoint minima with exact `Fraction`
arithmetic and imports neither the SMT encoding nor its template formulas.
It verifies both terminal selectors strictly.

## Exhaustive decision and witness-pattern coverage

The exact QF_LRA master independently imposed, for every observer row,

```text
each good >= M,     sum(goods)=T,     at least one good=M.
```

For each cardinality it negated the disjunction of every labelled assignment
of the split goods to the two recipients. All eight lanes were `UNSAT`:

```text
template A / a1: cardinalities 2,3,4,5,6,7
template B / k:  cardinalities 2,3
```

The decision explicitly considered all 264 packet assignments. Its symbolic
domains cover the following numbers of labelled minimum-witness patterns:

| role | cardinality | witness patterns |
|---|---:|---:|
| `a1` | 2 | 16 |
| `a1` | 3 | 1,296 |
| `a1` | 4 | 38,416 |
| `a1` | 5 | 810,000 |
| `a1` | 6 | 14,776,336 |
| `a1` | 7 | 252,047,376 |
| `k` | 2 | 16 |
| `k` | 3 | 36 |

This totals 267,673,492 labelled witness patterns, represented exactly rather
than sampled or individually enumerated. The anchor proof then explains the
UNSAT verdict without relying on this large count.

## Test against retained saturated profiles

The abstract anchor conditions were evaluated on every one of the 205
hash-verified profiles retained in
`fixed_u_multi_split_chart_cuts_20260820.jsonl`. These are exact admissible
models returned by the declared form-2 physical-minimum master before their
certificate cuts were installed.

| anchor template | applicable profiles | verified | failed |
|---|---:|---:|---:|
| A: `q`-minimum `a1` | 160 | 0 | 160 |
| B: `r`-minimum `k` | 79 | 2 | 77 |

At least one fixed anchor works on only 2 of the 205 retained profiles. The
terminal profile, which is not a successful-cut ledger record, satisfies both
strictly.

This separates the abstract lemma's hypotheses:

- **Definitional/physical:** an attained minimum exists; whole-role totals and
  minima exactly determine bundle totals and hardest deletions; a non-singleton
  role has `T_i>=2M_i` in every row.
- **Combinatorial:** each displayed topology uses at most four support edges.
- **Load-bearing and profile-specific:** all affine EFX lower bounds in (1)
  are nonnegative. The census gives admissible form-2 master profiles with
  negative bounds, so these inequalities do not follow from the declared
  form-2 GG/chart premises alone.

No claim is made that a stronger semantic premise absent from the encoded
master could not imply them. Within the exact declared master used throughout
this campaign, however, the nonimplication is decisive.

## Reproduction

```bash
python -m tracks.parkability.decide_fixed_u_split_switching_templates \
  --profile results/fixed_u_wild_forced_terminal_profile_20260820.json \
  --output results/fixed_u_split_switching_template_decision_20260821.json \
  --timeout-seconds 300

python -m tracks.parkability.audit_fixed_u_split_switching_anchor_lemma \
  --profile results/fixed_u_wild_forced_terminal_profile_20260820.json \
  --output results/fixed_u_split_switching_anchor_lemma_audit_20260821.json

python -m tracks.parkability.scan_fixed_u_split_switching_anchor_ledger \
  --ledger results/fixed_u_multi_split_chart_cuts_20260820.jsonl \
  --terminal-profile results/fixed_u_wild_forced_terminal_profile_20260820.json \
  --output results/fixed_u_split_switching_anchor_ledger_census_20260821.json

pytest -q tracks/parkability/test_fixed_u_split_switching_completion.py
```

Frozen result hashes:

```text
e8ff630bf0e591e806b3695ea2fa8fb44a872bec6a96afbcc9be4a64d0dfc264  results/fixed_u_split_switching_template_decision_20260821.json
603e40823033eb263c461be07196dbecbdbc9c561c32e14f970172f5fe2abed8  results/fixed_u_split_switching_anchor_lemma_audit_20260821.json
bb2ca056b14908149140e755b756c838f5ff0619206a3f40e22096d1fdcf79d5  results/fixed_u_split_switching_anchor_ledger_census_20260821.json
```

## Exact remaining boundary

Proved: the first genuine wild-and-forced terminal profile is EFX-safe under
every simultaneous physical realization of every role, using an explicit
four-edge allocation and a cap-free analytic selector.

Not proved: that either fixed anchor template works on every admissible
fixed-`U` profile, that the affine anchor margins follow from the universal
GG premises, the universal fixed-`U` theorem, or general additive EFX.

The next general step must dynamically choose the split role, anchor observer,
and four-edge topology from the saturated response structure. Reusing A or B
globally is ruled out by the 205-profile census. The sharp target is a
**dynamic anchor extraction theorem**: every wild-split-forced profile either
has a whole-role four-edge allocation or exposes some role/observer/topology
whose anchor-good affine bounds are all nonnegative.

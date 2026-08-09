# Alternating augmented-q-face packing checkpoint

**Date:** 2026-08-09

**Status:** exact bounded progress; cap-free dichotomy open

**Order:** `(p,s,r,q)` with `p={x}` fixed

## Result boundary

The two-safe-bundle reduction converts disjoint bundles `D,Q` in the common
base-safe family into a rooted EFX lexicographic improvement whenever `D` is
desired by `s` or `r` and

\[
v_q(Q)\ge \tau_q(D).
\]

This checkpoint isolates a cap-free-shaped two-branch schema for finding the
pair.

1. **Augmented q-face.** Choose a proper subset `S` of `X_q`, put
   `D=S+f`, require `D` to be desired by `s`, and choose any disjoint common
   base-safe `Q` meeting the `q` threshold.
2. **Bottom return.** Choose `b` in `B_q`, a subset `A` of `X_r+f`, and put
   `D=A+b`. Require `D` to be desired by `s` or `r`, and use
   `Q=X_q-b`.

The statement mentions no packet-size cap. Proving that one branch always
exists under the alternating structural premises would prove the surviving
external-observer lemma for arbitrary packet sizes, by the existing
two-safe-bundle reduction.

## Exact decisions

Z3 5.0.0 proves the schema UNSAT in both cells tested to completion:

| Packet sizes | Schema pairs | Result |
|---|---:|---|
| `(2,2,2,2)` | 1,393 | UNSAT |
| `(2,2,3,2)` | 3,969 | UNSAT |

The second row is the first exact nonbinary theorem on this route. The fully
unrestricted safe-pair formula is independently UNSAT in `(2,2,3,2)` over
114,024 ordered pairs.

Tracked-core extraction gives:

- a deletion-minimal 42-pair core for the unrestricted binary theorem; and
- a replayed 136-pair core for the nonbinary q-face schema, split into 90
  augmented-q-face pairs and 46 bottom-return pairs.

The nonbinary core uses augmented-q-face desired bundles only of sizes two,
three, and four. Its bottom-return pairs always pay `q` with `X_q-b`.

## Exact rejected sharpening

Forcing the augmented-q-face payment to be the complementary base set
`Q=X_q-S` is SAT-refuted already in `(2,2,2,2)`. The strict countermodel has
345 unrestricted safe-pair escapes; its smallest escapes use mixed payment
bundles. Thus the countermodel refutes only the complement identity, not the
two-safe-bundle route or the external-observer lemma.

## Larger-cell boundary

The unrestricted augmented-q-face schema returned `unknown (timeout)` at 180
seconds for `(2,2,4,2)`, `(2,2,5,2)`, and `(3,3,3,3)`. These are not
counterexamples and support no theorem claim. Earlier narrower schemas were
SAT-refuted at `|T_q|=4,5`; their smallest unrestricted escapes motivated the
proper-q-face formulation used here.

## Analytic target

Let `C` be the downward-closed family of common base-safe sets. The remaining
cap-free statement is:

> Under the alternating structural premises and absence of the four
> compatible desired families, either some desired proper face `S+f` of
> `X_q+f` has a disjoint `Q` in `C` with `q(Q)>=tau_q(S+f)`, or some
> `b in B_q` and `A subseteq X_r+f` give a desired `A+b` with
> `q(X_q-b)>=tau_q(A+b)`.

The structural cell supplies the two endpoints needed for a boundary proof:
`T_q+f` is desired by `s`, whereas the full `X_q+f` is not desired. Because
values are strictly positive, the latter failure is a common-safety wall,
not a failure to cross `s`'s utility. The proof must convert the first
critical wall on a chain between those endpoints into either a disjoint safe
payment or the bottom-return branch.

## Verification and trust boundary

The exact results use one generator and Z3 QF_LRA. Every reported UNSAT core
was replayed, but no solver-independent encoding or checked certificate yet
exists. The cap-free dichotomy itself remains unproved. Complete additive EFX
is not proved.

Primary artifacts and SHA-256 hashes:

- `alternating_two_safe_bundle_core_2222.json`:
  `3e4335675dc9ed4d87f9ff1b330a19de392cbf1ca7a64daaac2d5310cd3c8c96`
- `alternating_safe_pair_qface_2222.json`:
  `78f60b0e8ee61ebf46495ea568ebf9008295a0ee4f1bcf121540c25cdefb6e84`
- `alternating_safe_pair_qface_2232.json`:
  `d8fc3d5ff3f6ee811cfc6f268beaac32cf3c292a605953250bd06a1598382069`
- `alternating_safe_pair_qface_core_2232.json`:
  `48b04be1e2a1d14f59fccaae9227c33d941d4edeafeedbc3863c6178b49dfc7a`
- `alternating_safe_pair_qface_remainder_2222.json`:
  `41efcc66c679ecc08c9e274841720b4f33da2143e294b382826bef53188bc513`
- `alternating_safe_pair_qface_remainder_2222_analysis.json`:
  `659915cd6746214d2ccc05c76eab6f758b93ee157fcd9e7bd9f65bd0db5c72ab`
- `alternating_two_safe_bundle_gate_2232.json`:
  `f9cc04eec5ed1c242a2a383e43f1b25f7b99ea39f1c49361a82d0599826a647b`

Shortest theorem replay:

```bash
PYTHONPATH=/private/tmp/efx-z3 python3 tracks/parkability/decide_alternating_safe_pair_schema.py \
  --sizes 2,2,3,2 --q-face-payment any --timeout-seconds 180 \
  --output /tmp/alternating_safe_pair_qface_2232.json
```

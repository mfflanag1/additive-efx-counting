# Fixed-U source-margin-to-fork refutation

**Date:** 2026-08-11

**Status:** exact positive-rational countermodel; the local source-margin
certificate does not force an EFX Pareto-improving charity-rooted transfer
tree

## Certificate instantiated

Use the frozen two-atom full-capture flower with owners `r,q,c,s`, old EFX
allocation `X`, and charity good `f`.  Set root `r`, external source `q`,

\[
A=\{ar\_tr\_0,ar\_tr\_1,tr\_rest\_0,tr\_rest\_1,f\},
\]

and

\[
P=\{aq\_br\_0,aq\_br\_1,br\_rest\_0,br\_rest\_1\}.
\]

The exact profile in
[`fixed_u_charity_tree_countermodel.json`](fixed_u_charity_tree_countermodel.json)
has strictly positive additive values and satisfies every frozen flower
premise.  The core `A` is common-safe, `q` strictly desires it, and
`P+(A-f)=X_r`, so the root-paid exchange family is nonempty.

The audit enumerates every pair `C subseteq A`, `B subseteq P`.  Of the 512
pairs, eight pay `r`; every one leaves `q` at or below her base value.  The
global source-maximizing pair has

\[
 C=\{ar\_tr\_0,tr\_rest\_0,tr\_rest\_1,f\},
 \qquad B=\varnothing,
\]

root slack `5/256`, and source value `35/256`, below source base `131/256`.
The root-critical boundary and both root-affordable swap-order inequalities
of the source-margin frontier replay exactly.

## Exhaustive tree decision

For every nonempty subset of the four owners, every possible root, and every
labeled directed tree oriented away from that root, the decision oracle gives
`f` to the root and permits an arbitrary nonempty packet on each arc.  Packets
on different outgoing arcs are disjoint subsets of the parent's complete old
bundle; there is no packet-cardinality or moved-good bound.

The complete topology count is

| participating owners | labeled rooted topologies |
| ---: | ---: |
| 1 | 4 |
| 2 | 12 |
| 3 | 36 |
| 4 | 64 |
| **total** | **116** |

For the frozen rational profile, a second encoding independently proves
`UNSAT` for the packet variables of every one of the 116 topologies when:

1. every participating owner must be weakly paid relative to `X`, with at
   least one strict improvement; and
2. the resulting complete allocation must be EFX for all four observers.

Thus the fixed-U source-margin/root-critical certificate—even together with
the frozen full-capture flower premises—is insufficient to select the
surplus-safe third- or fourth-owner fork required by the current proof route.

## Consequence for the GG program

The direct local conjecture is false.  Continuing to strengthen only the
two-row root/source frontier cannot close the flower.  A successful proof
must use an additional genuinely global premise, with the leading candidates
being:

1. exclusion of the countermodel by the full PI-free/global-lex-maximality
   conditions;
2. a response-Hall condition that turns the failed EFX tree into an internal
   PI edge set or forces an external-source expansion; or
3. an observer-surplus inequality derived from the fixed-U priority/matching
   history, not from the final exchange certificate alone.

This is a refutation of certificate sufficiency, not a counterexample to GG,
four-agent additive EFX, or general additive EFX.  The model is not claimed
subset-sum injective; ties are allowed by the stated certificate and by
additive EFX.  Any use inside a nondegenerate GG reduction must either derive
the missing global condition before perturbation or separately harden the
profile.

## Verification

The independent replay
[`fixed_u_charity_tree_countermodel_audit.json`](fixed_u_charity_tree_countermodel_audit.json)
checks positivity, the frozen flower master, all 512 exchanges, the selected
frontier inequalities, and all 116 arbitrary-packet topology decisions using
exact rational arithmetic and QF integer/linear arithmetic.

```bash
python tracks/parkability/audit_fixed_u_charity_tree_countermodel.py \
  --source results/fixed_u_charity_tree_countermodel.json \
  --output /tmp/fixed_u_charity_tree_countermodel_audit.json
```

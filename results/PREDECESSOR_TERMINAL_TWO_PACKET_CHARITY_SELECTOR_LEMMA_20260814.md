# Predecessor-terminal two-packet charity selector lemma

**Date:** 2026-08-14

**Status:** cap-free joint optimization of the predecessor cross-exchange;
a paid four-edge allocation or one exact three-corner separator

## Coupled terminal exchange

Use a predecessor-duplicate terminal map. The shared target `q` contains a
base-desired core `C` for missing owner `m` and a response core `E` desired
by predecessor `x`. Put

```text
C0 = C minus E,
E0 = E minus C,
O  = C intersect E,
U  = C union E.
```

The final path core `D subseteq B_x` is desired by `q`. Let `R_m` be the
bundle retained by `m`, let `R_q=B_q minus U`, and let the protected floors
be `F_m,F_q,F_x`. Write

```text
Delta_x = v_x(B_x)-F_x.
```

Choose independently `H subseteq O` and `P subseteq D`, and allocate

```text
m receives C0+H,
x receives E0+(O minus H) and releases P,
q receives P and releases U.
```

Every other ordinary good is retained. Place the singleton charity `p` at
one of `m,q,x`. Giving it to the unchanged fourth owner is payment-wise
dominated.

## Exact thresholds

Define the unsubsidized thresholds and predecessor budget

```text
alpha_m = F_m-v_m(R_m+C0),
alpha_q = F_q-v_q(R_q),
Gamma   = Delta_x+v_x(E0+O).
```

For `a` a real threshold, define

```text
h(a) = min {v_x(H): H subseteq O and v_m(H)>=a},
k(a) = min {v_x(P): P subseteq D and v_q(P)>=a}.
```

Use the empty packet when a threshold is nonpositive. Both minima exist:
the full overlap `O` meets `alpha_m` because `C=C0+O` is desired by `m`,
and the full path core `D` meets `alpha_q` because it is desired by `q`
above the complete old bundle `B_q`.

The three charity placements succeed exactly under:

```text
charity to m: h(alpha_m-v_m(p)) + k(alpha_q) <= Gamma,
charity to q: h(alpha_m) + k(alpha_q-v_q(p)) <= Gamma,
charity to x: h(alpha_m) + k(alpha_q) <= Gamma+v_x(p).
```

Indeed the missing and terminal owners impose the two independent lower
thresholds, while predecessor payment is exactly

```text
v_x(H)+v_x(P) <= Gamma + [charity is at x]v_x(p).
```

Choosing minimum predecessor-cost packets is therefore lossless.

## Four-edge endpoint

Whenever one of the three inequalities holds, its minimizing packets give
an all-owner-paid complete allocation. Its nonempty current-holder pairs
are contained in

```text
q -> m,  q -> x,  x -> q,  charity -> {m,q,x}.
```

Thus it uses at most four current-holder edges, with unrestricted packet
sizes.

## Exact three-corner failure separator

If all three placements fail, the state satisfies simultaneously

```text
h(alpha_m-v_m(p)) + k(alpha_q) > Gamma,
h(alpha_m) + k(alpha_q-v_q(p)) > Gamma,
h(alpha_m) + k(alpha_q) > Gamma+v_x(p).
```

This is strictly sharper than treating the overlap packet and terminal
compensator separately. It says that the predecessor-cost Pareto frontier
misses all three corners of the charity subsidy triangle: charity cannot
repair the missing-owner demand, the terminal demand, or the predecessor
budget.

## Claim boundary

Proved: exact owner-payment equivalences, existence of the packet minima,
losslessness of independent predecessor-cost minimization, the four-current-
holder-edge construction, and the exact three-corner failure system.

Not proved: contradiction of that system from the signed fixed-`U` ledger,
compression by frozen-`Y` supplier rather than current holder, observer EFX
safety, decorated recurrence, closure of the two first-source terminal maps,
the fixed-`U` theorem, or additive EFX.

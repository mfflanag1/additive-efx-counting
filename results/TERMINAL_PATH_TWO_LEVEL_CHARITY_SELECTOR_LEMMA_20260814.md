# Terminal-path two-level charity selector lemma

**Date:** 2026-08-14

**Status:** cap-free all-terminal-map payment selector; a paid four-edge
allocation or one exact three-placement two-level packet separator

## Backward terminal chain

Use the terminal canonical path

```text
m -> y -> x -> q.
```

Let `C subseteq B_q` be the ordinary base-desired core for missing owner
`m`. Let `D_2 subseteq B_x` be desired by `q`, and let
`D_1 subseteq B_y` be desired by `x`. Every represented current bundle is
weakly base-paid. Put

```text
Delta_i = v_i(B_i)-v_i(X_i) >= 0,
beta = v_q(C)-Delta_q.
```

Core `C` alone pays `m`, so charity need not be assigned there.

Choose `P_2 subseteq D_2` for `q` and `P_1 subseteq D_1` for `x`. Give
`C` to `m`, `P_2` to `q`, and `P_1` to `x`; owners retain all other goods.
Place charity at one of `q,x,y`.

## Exact dynamic selector

For a charity recipient `a in {q,x,y}`, define

```text
b_a = beta-v_q(p) if a=q, and beta otherwise,
c_a(P_2) = v_x(P_2)-Delta_x-v_x(p) if a=x,
             v_x(P_2)-Delta_x otherwise,
d_a = Delta_y+v_y(p) if a=y, and Delta_y otherwise.
```

For a nonpositive lower threshold the empty packet is allowed. Define the
two-level predecessor cost

```text
Phi_a = min v_y(P_1)
```

over packets satisfying

```text
P_2 subseteq D_2,  v_q(P_2)>=b_a,
P_1 subseteq D_1,  v_x(P_1)>=c_a(P_2).
```

The feasible set is nonempty. The full `D_2` meets the q threshold because
`C subseteq B_q` and `D_2` is desired above `B_q`. For every
`P_2 subseteq D_2 subseteq B_x`, its x-value is at most `v_x(B_x)`;
therefore the full `D_1`, desired by `x` above `B_x`, meets the second
threshold.

The placement `a` pays every owner exactly when

```text
Phi_a <= d_a.
```

The reason is direct: q requires the first threshold; x requires the second
after releasing `P_2`; and y remains paid exactly when the y-cost of
`P_1` is at most its current surplus plus any charity subsidy.

## Four-edge endpoint

On success, the nonempty current-holder pairs are contained in

```text
q -> m:C,  x -> q:P_2,  y -> x:P_1,
charity -> a:p.
```

Thus the endpoint uses at most four current-holder edges and no packet-size
bound.

## Exact failure separator

All three charity placements fail if and only if

```text
Phi_q > Delta_y,
Phi_x > Delta_y,
Phi_y > Delta_y+v_y(p).
```

This is the complete owner-payment obstruction for the two-level terminal
chain. It is stronger than the earlier one-packet terminal separator:
charity may reduce q demand, reduce x compensation demand, or increase y
release capacity before failure is declared.

The omitted duplicate-target core is not used. In the two predecessor-
duplicate maps it supplies the additional coupled cross-exchange selector;
in the two first-source maps the three inequalities above are the direct
remaining payment frontier.

## Claim boundary

Proved: feasibility of the two-stage packet optimization, exact payment
equivalence for all three charity placements, conservation, and the four-
current-holder-edge bound for all four terminal maps.

Not proved: elimination of the three-placement separator from signed
saturation, frozen-supplier edge compression, observer EFX safety, use of
the omitted first-source response after failure, decorated recurrence, the
fixed-`U` theorem, or additive EFX.

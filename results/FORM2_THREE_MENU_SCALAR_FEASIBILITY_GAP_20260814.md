# Form-2 three-menu scalar-feasibility gap

**Date:** 2026-08-14

**Status:** exact positive-rational local witness showing that the three
cap-free payment frontiers do not contradict one another without signed
saturation/PI premises

## Local packets

Let the current root bundle contain three distinct singleton response goods

\[
                         D,quad P,quad C_s.
\]

Use `D` for the current-only `d->r` response, `P` for the root packet that
would compensate `q`, and `C_s` for the represented `s->r` response.  Let
`C_d` be the ordinary base-desired `d->q` singleton inside `B_q`, and let `p`
be charity.  Singleton response cores are automatically common-safe because
their one-good deletion threshold is zero.

## Exact rational rows

Choose the following aggregate and packet values.

### Root row

\[
 v_r(X_r)=5,quad v_r(B_r)=6,quad v_r(p)=1/10,
 \quad v_r(D)=v_r(P)=v_r(C_s)=2.                  \tag{1}

\]

The three root goods form an inclusion-minimal strict anchor: their total is
`6>5`, while deleting any one leaves value `4<=5`.

### d row

\[
 v_d(X_d)=1,quad v_d(B_d)=1/5,quad
 v_d(D)=3/10,quad v_d(C_d)=11/10.                \tag{2}

\]

Thus `D` is current-desired but does not repair the base deficit, whereas
`C_d` is ordinary base-desired.

### q row

\[
 v_q(X_q)=3,quad v_q(B_q)=31/10,quad
 v_q(C_d)=3,quad v_q(P)=16/5,
 \quad v_q(B_d)=v_q(p)=1/10.                     \tag{3}

\]

The root packet `P` is current-desired and is large enough to compensate the
loss of `C_d`, but it is too expensive in the root row.  The entire old `d`
bundle plus charity is far too small to compensate `q` in the swap topology.

### s row

\[
 v_s(X_s)=1,quad v_s(B_s)=11/10,quad
 v_s(C_s)=6/5.                                    \tag{4}

\]

Thus `s` is represented/base-paid and `C_s` is current-desired.

All unspecified singleton values can be chosen as any sufficiently small
positive rationals; they do not affect the displayed strict inequalities.

## Simultaneous menu failure

1. **Two-edge root-star candidate.**  Its root margin is
   `1+1/10-2=-9/10`, and its `d` margin is
   `-4/5+3/10=-1/2`.  Both payment rows fail.
2. **q-compensation path.**  Its q threshold is
   `v_q(C_d)-Delta_q=3-1/10=29/10`; `P` pays it because
   `16/5>29/10`.  But `v_r(P)=2>11/10`, so the root fails.
3. **q-d swap/root-response candidate.**  The root fails because
   `v_r(C_s)=2>Delta_r=1`; `q` also fails because
   `v_q(B_d)+v_q(p)=1/5<29/10`.

Therefore the three payment frontiers are jointly feasible even with
positive rational values, safe singleton cores, represented-owner payment,
an inclusion-minimal strict root anchor, and the correct current/base status
distinction for the two `d` responses.

## Consequence and claim boundary

This witness is not a countermodel to the saturated fixed-U theorem.  It does
not encode base EFX, the complete signed supplier/release record, generalized
PI-freeness, all response edges, global lex maximality, or the continuation
exclusions.  It proves a sharper methodological point:

> No proof can finish form 2 by algebraically combining only the three menu
> payment inequalities and singleton-core safety.

The next theorem must use a genuinely non-scalar premise: closed-core PI,
base-support drainage, exact response saturation, or a full signed
return/release component.

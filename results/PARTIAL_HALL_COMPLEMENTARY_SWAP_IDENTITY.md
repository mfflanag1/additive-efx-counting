# Complementary-swap potential identity

## Statement

Normalize each additive valuation row by its total value, and consider the
canonical partial allocation

\[
X=(\{6,7\},\{1,2,3\},\{0,4\},\{5\});f=8.
\]

Keep the floater unchanged and define two complementary exchanges between
bundles 0 and 2:

\[
\begin{aligned}
Y^{60}&=(\{0,7\},\{1,2,3\},\{4,6\},\{5\});f=8,\\
Y^{74}&=(\{4,6\},\{1,2,3\},\{0,7\},\{5\});f=8.
\end{aligned}
\]

If \(\Delta_{60}=\Phi(Y^{60})-\Phi(X)\) and
\(\Delta_{74}=\Phi(Y^{74})-\Phi(X)\), then

\[
\Delta_{60}+\Delta_{74}
=
\frac{v_0(\{0,4\})-v_0(\{6,7\})}{v_0(M)}
+
\frac{v_2(\{6,7\})-v_2(\{0,4\})}{v_2(M)}.
\]

Consequently, whenever the right-hand side is positive and both exchanged
allocations are eligible one-floater EFX states, at least one is a strict
normalized-utilitarian improvement over \(X\).

The identity and implication are cap-free algebraic facts; eligibility of the
two swaps is a separate condition.

## Proof

Only agents 0 and 2 change bundles. The two gains are

\[
\begin{aligned}
\Delta_{60}
&=\frac{v_0(0)-v_0(6)}{v_0(M)}
 +\frac{v_2(6)-v_2(0)}{v_2(M)},\\
\Delta_{74}
&=\frac{v_0(4)-v_0(7)}{v_0(M)}
 +\frac{v_2(7)-v_2(4)}{v_2(M)}.
\end{aligned}
\]

Adding and collecting the two original bundles gives the displayed identity.
If the sum is positive, at least one summand is positive.

## Exact corpus audit

[`partial_hall_complementary_swap_audit.json`](partial_hall_complementary_swap_audit.json)
checks the identity with exact rational arithmetic on all 134 distinct stored
canonical Hall obstructions:

- the first swap is eligible and improving in 42 profiles;
- the second is eligible and improving in 26 profiles;
- their union covers 67 profiles;
- the summed identity is positive in 26 profiles; and
- eight positive-sum profiles have neither swap simultaneously eligible and
  improving.

These counts are corpus evidence, not a universal theorem. Their value is that
they isolate the next conversion gate: explain why a positive summed exchange
that hits an EFX eligibility wall admits a short dependency-cycle repair.

## Claim boundary

This identity does not prove the canonical radius-five improvement theorem,
the one-good Hall-completion lemma, four-agent EFX existence, or general EFX.
It supplies the analytic potential half of the dominant two-swap motif; the
eligibility-wall conversion remains open.

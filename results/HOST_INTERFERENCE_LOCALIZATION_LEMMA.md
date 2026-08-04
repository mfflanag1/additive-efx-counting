# Host-interference localization lemma

## Statement

Let \((X,\{f\})\) be an EFX-with-charity state for positive-additive
valuations. Select it by first globally maximizing

\[
\Theta(X)=\sum_i\frac{\tau_i(X_i)}{v_i(M)}
\]

among one-charity states and then lexicographically maximizing the owner
utility vector. Insert \(f\) into a nonsingleton host bundle \(X_h\), and
suppose the identity assignment has exactly one defective agent \(b\). Put
\(S=X_h+f\), and suppose the host also strongly envies \(S\) relative to her
old bundle:

\[
\tau_h(S)>v_h(X_h). \tag{H}
\]

Let \(g\) be an \(h\)-minimum, put \(R=X_h-g\), and set \(T=R+f\). Then:

1. \(v_h(f)>v_h(g)\), and the owner-improving \(f/g\) swap is ineligible.
2. Its incoming-target blocker is exactly the unique defective agent \(b\):
   \[
   v_b(X_b)<\tau_b(T),
   \qquad
   v_b(f)>\max\{v_b(g),\min_{x\in R}v_b(x)\}. \tag{B}
   \]
3. Exactly one of the following proof branches is available:

   - **bad-source branch:** if \(\tau_h(T)\le v_h(X_h)\), then \(b\) is a
     most-envious source for \(T\). Its desired subset contains \(f\), so it
     gives a generalized \(\{f\}\mid\{g\}\)-champion edge into \(h\),
     releasing \(g\) plus any additional bottom discard;
   - **positive host-wall branch:** if \(\tau_h(T)>v_h(X_h)\), then the
     blocked swap would strictly raise \(\Theta\), and, writing
     \(r=\min_{x\in R}v_h(x)\), its exact host condition is
     \[
     v_h(f)>v_h(g)+r. \tag{P}
     \]

Thus host interference does not create an untyped third source. At the
selected extremum it either returns a bad-source generalized champion edge
after one minimum release or exposes a specifically bad-blocked,
strictly-positive threshold move.

## Proof

Condition (H) and additivity imply
\(v_h(f)>\min_{x\in X_h}v_h(x)=v_h(g)\). If the \(f/g\) swap were eligible,
the threshold-maximum swap lemma would keep it on the global
\(\Theta\)-plateau while strictly improving only owner \(h\)'s utility. This
contradicts the secondary utility maximum, so the swap is ineligible.

Because \(X_h\) is nonsingleton, the one-floater obstruction lemma rules out
all new-charity walls. The two source-owner walls have the wrong sign,
because both require \(v_h(g)>v_h(f)\). Hence some external agent
\(i\ne h\) strongly envies \(T\).

Every agent outside \(\{b,h\}\) has a valid identity edge after insertion,
so \(v_i(X_i)\ge\tau_i(S)\). Since \(T=S-g\), monotonicity gives
\(\tau_i(T)\le\tau_i(S)\). Therefore no agent outside \(\{b,h\}\) can be
the incoming blocker. The blocker is exactly \(b\), and the sharpened
incoming-wall inequality from the charity/minimum exchange lemma gives (B).

Suppose first that \(h\) does not strongly envy \(T\) relative to her old
bundle. Agent \(b\) does strongly envy \(T\) by (B). Choose an
inclusion-minimal subset \(A\subsetneq T\) envied by \(b\). Minimality says
that \(b\) does not strongly envy \(A\). If any other agent strongly envied
\(A\), that agent would envy some proper subset of \(A\); monotonicity would
then make the agent strongly envy \(T\). This is impossible for the host by
the branch assumption and impossible for every external agent by
\(\tau_i(T)\le\tau_i(S)\). Thus no agent strongly envies \(A\), and \(b\)
is a most-envious source for \(T\).

Moreover \(f\in A\). Otherwise \(A\subseteq X_h-g\), while old EFX gives
\(v_b(X_b)\ge v_b(X_h-g)\ge v_b(A)\), contradicting that \(b\) envies
\(A\). This proves the bad-source branch.

For the other branch, let \(r=\min_{x\in R}v_h(x)\). Direct calculation gives

\[
\tau_h(T)=v_h(R)+v_h(f)-\min\{v_h(f),r\},
\qquad
v_h(X_h)=v_h(R)+v_h(g).
\]

The strict inequality \(\tau_h(T)>v_h(X_h)\) is equivalent to
\(v_h(f)-\min\{v_h(f),r\}>v_h(g)\). Positivity rules out
\(v_h(f)\le r\), leaving exactly (P). It also gives
\(\tau_h(T)>v_h(X_h)>\tau_h(X_h)\), so the blocked swap has strictly positive
\(\Theta\)-gain. \(\square\)

## Singleton host

When \(X_h=\{g\}\), the replacement target \(\{f\}\) has threshold zero,
so the incoming-target localization above is unavailable. The only residual
wall is an external charity blocker that prefers \(g\) to its own bundle.
The proved singleton-chain elimination lemma handles this case by propagating
through distinct singleton owners until it reaches an eligible improvement
or a nonsingleton positive incoming-target wall.

## Exact local sharpness witness

The positive host-wall branch is realizable. An exact positive-additive
\((4,8)\) state has floater value \(37\) for the host, host minimum \(6\),
and next host minimum \(22\). Thus \(37>6+22\); the reduced swap strictly
raises the host threshold and is blocked exactly by the unique bad agent.
The state is not a global \(\Theta\)-maximizer: all 24 global maximizers are
directly absorbable. The frozen replay is
[`host_interference_positive_wall_local_counterexample.json`](host_interference_positive_wall_local_counterexample.json).

## Claim boundary

The blocker localization, generalized-champion alternative, and exact
positive host wall are proved. What is not yet proved is that repeated
positive bad-blocked walls or the additional bottom discards can always be
combined into a one-charity EFX component with nonnegative total threshold
gain. This lemma therefore does not by itself resolve four-agent or general
additive EFX.

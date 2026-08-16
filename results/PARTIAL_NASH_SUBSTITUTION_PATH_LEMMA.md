# Floater-Substitution Preference-Path Lemma

**Status:** proved cap-free improvement lemma  
**Scope:** any positive-additive eligible one-floater EFX state  
**Remaining cases:** multiple floater supporters, or a unique supporter outside
the source's weak-preference reachability set

Let \((X,f)\) be EFX with one unallocated good and

\[
v_a(X_a)\ge v_a(f)
\qquad\text{for every agent }a.
\tag{E}
\]

Choose a host \(h\), a good \(r\in X_h\), and another agent \(i\). Define the
modified host bundle

\[
B=(X_h\setminus\{r\})\cup\{f\}.
\]

Assume:

1. \(X_h\) contains at least two goods;
2. agent \(i\) is the unique floater supporter for this replacement,
   meaning \(v_i(f)>v_i(r)\) and \(v_a(f)\le v_a(r)\) for every \(a\ne i\);
3. agent \(i\) strictly prefers the modified bundle:
   \(v_i(B)>v_i(X_i)\); and
4. the weak bundle-preference graph contains a simple path

   \[
   h=a_0,a_1,\ldots,a_k=i,
   \]

   with

   \[
   v_{a_t}(X_{a_{t+1}})\ge v_{a_t}(X_{a_t})
   \qquad(t<k).
   \tag{P}
   \]

Reassign bundles along the path by giving \(X_{a_{t+1}}\) to \(a_t\), give
\(B\) to \(i\), leave all other bundles fixed, and make \(r\) the new
floater.

> **Lemma.** The resulting state is EFX and satisfies new-floater nonenvy.
> Every owner weakly improves, agent \(i\) strictly improves, and hence Nash
> welfare strictly increases.

## Proof

Every path agent except \(i\) weakly improves by (P), and \(i\) strictly
improves by assumption 3. Other agents are unchanged.

First consider an observer other than \(i\). For every unchanged target
bundle, its old EFX threshold remains valid because the observer's own utility
does not decrease. If the observer's old own bundle becomes a target, its
removed-good value is at most the observer's old own utility, again at most
the new own utility.

It remains to compare against \(B\). Removing the new good \(f\) leaves
\(X_h\setminus\{r\}\), which was an old EFX remainder for observers other
than \(h\), and is below the old full own bundle for observer \(h\). Removing
an old good \(g\ne r\) leaves

\[
X_h\setminus\{r,g\}\cup\{f\}.
\]

Because this observer is not the unique supporter, replacing \(f\) by
\(r\) weakly raises its value. The resulting bundle
\(X_h\setminus\{g\}\) is controlled by old EFX, or by the old own-bundle
value when the observer is \(h\). Thus every comparison with \(B\) holds.

Agent \(i\) owns \(B\), so no comparison with \(B\) is required. Its own
utility strictly exceeds its old utility, which already dominated every old
target threshold. Its old own bundle is the only newly exposed target, and
every removed-good remainder of that bundle is below its old utility.

Finally, agent \(i\)'s new bundle contains \(f\), which it values strictly
above the new floater \(r\). The old host weakly improves and previously owned
a bundle containing \(r\). Every other observer's old EFX comparison with the
nonsingleton \(X_h\), after removing a good other than \(r\), already implies
that its old own utility is at least \(v_a(r)\). Hence nobody envies the new
floater. Positivity and the owner improvements give the strict Nash increase.

## Maximum-Nash corollary

In the source-host reduction, every insertion blocker \((i,r)\) satisfies
\(v_i(B)>v_i(X_i)\) and \(v_i(f)>v_i(r)\). Therefore:

> **Corollary.** At a maximum-Nash eligible state, if a source-host blocker
> has a unique floater supporter, that supporter is not reachable from the
> source in the weak bundle-preference graph.

Otherwise the lemma constructs a strictly better eligible state.

## Verification

The permanent artifact is
[floater_substitution_cycle_lemma_audit.json](floater_substitution_cycle_lemma_audit.json).
It combines QF_LRA/QF_NRA negated-conclusion checks with two literal audits:

- all 256 two-agent, four-good profiles over values \(\{1,2\}\), exercising
  96 premise paths; and
- 1,024 deterministic three-agent, five-good profiles, exercising 1,767
  premise paths, including 485 paths of length two.

Reproduce it with:

```sh
make verify-floater-substitution-cycle
```

## Calibrated residual

For four agents, a hypothetical blocked maximum is now confined to one of
two configurations at every chosen source blocker:

1. at least two agents rank the floater above the removed host good; or
2. there is one supporter, but no weak-preference path from the source to it.

An exact census on six hard profiles initially supported a broader local
trichotomy. Among 10,777 eligible states, all 3,714 all-host-blocked states
had either a strict bundle cycle (1,890 states) or a source substitution with
larger Nash welfare (1,824 states); only three selected rescues required an
owner loss. The frozen census is
[partial_nash_substitution_census.json](partial_nash_substitution_census.json).

That broader local trichotomy is nevertheless false. The exact matrix in
[partial_nash_local_trichotomy_refutation_audit.json](partial_nash_local_trichotomy_refutation_audit.json)
has an eligible all-host-blocked candidate, no strict bundle cycle, and no
improving eligible rematching among all 192 source substitutions. It has
1,780 larger global eligible rivals, so it does **not** refute maximum-Nash
completion.

The correct next theorem must therefore use global reallocation information
available from Nash maximality. A proof based only on the current state's
bundle cycles and one source-good substitution cannot work.

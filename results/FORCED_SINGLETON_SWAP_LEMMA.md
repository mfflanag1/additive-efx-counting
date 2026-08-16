# Forced Singleton-Swap Handoff Lemma

**Status:** proved analytic lemma. The statement below is valid for any
strictly positive additive valuations and any number of goods. It is a local
exchange lemma, not a proof that complete EFX always exists.

## Statement

Let the four agents be \(a,b,c,d\), and let \(p,q,t,x\) be distinct goods.
Suppose \(A\) and \(B\) are EFX allocations with one unallocated good each.
The two unallocated goods may differ.

Assume:

1. In \(A\),
   \[
   A_a=\{p,q\},\qquad A_d=\{t\}.
   \]
2. In \(B\),
   \[
   B_a=\{q\},\qquad B_c=\{p\},\qquad
   \{t,x\}\subseteq B_b.
   \]
3. Each allocation's unallocated good is not envied by any agent.
4. Direct insertion fails at host \(d\) in \(A\), and at hosts \(a\) and
   \(c\) in \(B\).

Let \(B'\) be obtained from \(B\) by swapping the singleton goods of agents
\(a\) and \(c\):

\[
B'_a=\{p\},\qquad B'_c=\{q\},
\]

with every other bundle and the unallocated good unchanged.

Then:

1. \(B'\) is EFX;
2. the unallocated good remains unenvied in \(B'\); and
3. \(B'\) is strictly lexicographically larger than \(B\) in agent order
   \((b,a,c,d)\).

Consequently, \(B\) cannot be a \((b,a,c,d)\)-lexicographic maximum among
the one-unallocated EFX allocations whose floater is unenvied.

## Proof

Write \(u\) for the floater of \(A\). Inserting \(u\) into
\(A_d=\{t\}\) fails EFX. Because every agent values its own bundle at least
as much as \(u\), the failure cannot arise after removing \(t\), which
would leave only \(u\). Therefore some agent \(i\ne d\) satisfies

\[
v_i(A_i)<v_i(t). \tag{1}
\]

The witness in (1) cannot be \(a\). EFX of \(B\), observed by \(a\) and
compared with \(B_b\) after removing \(x\), gives

\[
v_a(q)=v_a(B_a)
\ge v_a(B_b\setminus\{x\})
\ge v_a(t).
\]

Strict positivity then gives
\(v_a(A_a)=v_a(p)+v_a(q)>v_a(t)\), contradicting (1).

The witness cannot be \(c\) either. EFX of \(A\) after removing \(q\) from
\(A_a\), followed by EFX of \(B\) after removing \(x\) from \(B_b\), gives

\[
v_c(A_c)\ge v_c(p)=v_c(B_c)
\ge v_c(B_b\setminus\{x\})
\ge v_c(t),
\]

again contradicting (1). Hence the witness is \(b\), so

\[
v_b(A_b)<v_b(t). \tag{2}
\]

Now insert the floater of \(B\) into \(B_c=\{p\}\). Floater nonenvy again
implies that a blocking witness \(j\ne c\) must satisfy

\[
v_j(B_j)<v_j(p). \tag{3}
\]

It cannot be \(b\): EFX of \(A\) gives \(v_b(A_b)\ge v_b(p)\), while (2)
and strict positivity give

\[
v_b(B_b)>v_b(t)>v_b(A_b)\ge v_b(p).
\]

It cannot be \(d\): EFX in \(A\) and then in \(B\) gives

\[
v_d(B_d)
\ge v_d(B_b\setminus\{x\})
\ge v_d(t)
=v_d(A_d)
\ge v_d(p).
\]

Thus \(j=a\). Since \(B_a=\{q\}\), (3) forces

\[
v_a(p)>v_a(q). \tag{4}
\]

Apply the same argument to the failed insertion into \(B_a=\{q\}\).
A blocking witness \(k\ne a\) must have \(v_k(B_k)<v_k(q)\). It cannot be
\(b\), because (2), EFX of \(A\), and positivity imply

\[
v_b(B_b)>v_b(t)>v_b(A_b)\ge v_b(q).
\]

It cannot be \(d\), because

\[
v_d(B_d)
\ge v_d(B_b\setminus\{x\})
\ge v_d(t)
=v_d(A_d)
\ge v_d(q).
\]

Therefore \(k=c\), and \(B_c=\{p\}\) yields

\[
v_c(q)>v_c(p). \tag{5}
\]

In \(B'\), agents \(a\) and \(c\) strictly improve their own values by
(4) and (5). Their comparisons with the other nonsingleton bundles are
unchanged, and an EFX comparison with the other singleton becomes zero
after removing its only good. Agents \(b\) and \(d\) keep their bundles;
their comparisons with the two singleton bundles likewise have zero
remainders. Hence \(B'\) is EFX. Floater nonenvy is preserved because two
agents improve and two are unchanged.

Finally, agent \(b\)'s own bundle is unchanged while agent \(a\)'s own
value strictly increases. Thus \(B'\) is strictly larger than \(B\) in
order \((b,a,c,d)\). \(\square\)

## Underlying bundle-swap principle

The last step does not depend on singleton bundles. In any partial EFX
allocation, if two agents strictly prefer each other's entire bundles,
swapping those bundles preserves EFX: the multiset of target bundles is
unchanged, the two swapped agents strictly improve, and every other agent is
unchanged. Floater nonenvy is preserved for the same reason.

The singleton hypotheses above are what convert two failed insertions into
the mutual bundle preferences. For a nonsingleton host, failed insertion can
instead be witnessed after removing an internal good, so the witness need
not prefer the host's whole bundle. Extending the forced-witness argument
across that threshold case is the next analytic generalization.

## Canonical \(4\times9\) instance used for discovery

The proof was extracted from the following canonical bundle pattern:

| State | Agent 0 | Agent 1 | Agent 2 | Agent 3 | Floater |
|---|---|---|---|---|---|
| \(A\) | \(\{6,7\}\) | \(\{1,2,3\}\) | \(\{0,4\}\) | \(\{5\}\) | \(8\) |
| \(B\) | \(\{7\}\) | \(\{0,1,2,5\}\) | \(\{6\}\) | \(\{4,8\}\) | \(3\) |
| \(B'\) | \(\{6\}\) | \(\{0,1,2,5\}\) | \(\{7\}\) | \(\{4,8\}\) | \(3\) |

Here
\[
(a,b,c,d,p,q,t,x)=(0,1,2,3,6,7,5,0).
\]

The exact rational encoding uses only weak EFX, weak floater nonenvy,
strict positivity, and the three failed insertions in the statement. Z3
proves that the premises are satisfiable, while each negated forced item
ordering is UNSAT. It also proves that “\(B'\) is ineligible or
lexicographically lower than \(B\)” is UNSAT. The frozen formula is
independently replayed as UNSAT by cvc5 1.3.3.

## Artifacts

- Symbolic certificate:
  [forced_singleton_swap_lemma.json](forced_singleton_swap_lemma.json)
- Frozen QF_LRA formula:
  [forced_singleton_swap_lemma.smt2](forced_singleton_swap_lemma.smt2)
- Independent cvc5 replay:
  [forced_singleton_swap_lemma.cvc5.json](forced_singleton_swap_lemma.cvc5.json)
- Reconstructing audit:
  [`audit_forced_singleton_swap_lemma.py`](../tracks/parkability/audit_forced_singleton_swap_lemma.py)
- Discovery cell:
  [adaptive_priority_trace92_i5_compact_core.json](adaptive_priority_trace92_i5_compact_core.json)

## Remaining theorem gate

This lemma removes one concrete two-state obstruction motif for arbitrary
goods. To prove four-agent complete EFX by adaptive priority, it remains to
show that every hypothetical all-orders-blocked family contains this motif
or one of a finite set of analogous exchange motifs. The current
simultaneous CEGAR data supports that direction but does not establish the
covering claim.

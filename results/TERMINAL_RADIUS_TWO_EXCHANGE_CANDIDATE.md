# Terminal Radius-Two Exchange Refutation and Boundary

**Status:** refuted by an exact cap-20 profile  
**Immediate scope:** the first canonical matching cell of terminal orbit R  
**Purpose:** postmortem for the former local lemma and its surviving global
successor

## The picture in plain language

The terminal allocation has four bundles:

\[
\{f,p\},\qquad \{a,b,c\},\qquad \{x,y\},\qquad \{z,w\}.
\]

The first bundle contains the common favorite. The second contains three
half-favorite representatives, which is precisely why this partition lies
outside the eight-orbit family. The last two are pairs of unrepresented
goods.

One swap is not enough in general. The former candidate therefore allowed
every eight-orbit state within two single-good swaps, 138 partitions in all.
Some repairs keep the favorite bundle and reconfigure the other bundles;
others give the favorite a new partner while moving an unrepresented good
into the triple. Exact profiles first showed that neither mechanism alone
was sufficient, and the decisive profile below then blocked their union.

## Exact canonical assumptions

Normalize the representatives as \(p=1\), \(a=2\), \(b=3\), \(c=4\), and
the unrepresented goods as \(x=5,y=6,z=7,w=8\). Fix the terminal matching

\[
0\mapsto\{f,p\},\quad
1\mapsto\{a,b,c\},\quad
2\mapsto\{x,y\},\quad
3\mapsto\{z,w\}.
\]

Write \(F_i=v_i(f)\), \(v_i(S)=\sum_{g\in S}v_i(g)\), and

\[
M_i(S)=\max_{g\in S}v_i(S\setminus\{g\}).
\]

Because \(f\) is every agent's strict favorite, EFX of the displayed
terminal matching is exactly

\[
\begin{aligned}
F_0+v_0(p)&\ge M_0(\{a,b,c\}),\\
v_1(\{a,b,c\})&\ge F_1,\\
v_2(\{x,y\})&\ge
\max\{F_2,M_2(\{a,b,c\}),v_2(z),v_2(w)\},\\
v_3(\{z,w\})&\ge
\max\{F_3,M_3(\{a,b,c\}),v_3(x),v_3(y)\}.
\end{aligned}
\]

Add the established hard-branch assumptions:

- \(f\) is a strict common favorite;
- every agent fails the favorite-singleton owner threshold; and
- the half-favorite graph has fixed representatives (1,2,3,4), so
  \(2v_i(i+1)>F_i\) for each agent \(i\).

Finally assume there is no full favorite-triple Hall cell. For every
residual low pair \(L\), at least one of the 15 perfect pairings of the other
six goods therefore lacks a matching of its three pairs to three distinct
agents at thresholds

\[
F_i+\max_{\ell\in L}v_i(\ell).
\]

## Refuted candidate lemma

> **Terminal radius-two alternating exchange.** Under the assumptions
> above, one of the 138 eight-orbit favorite-pair partitions within two
> swaps of the terminal state supports a complete EFX allocation.

This statement would have been sufficient for the canonical R/matching-0
terminal cell. It is false; therefore no work on the other six matching
cells is warranted for this radius.

## Why all 138 states are needed

The natural partner split is exact:

| radius-two family | size | decisive boundary |
|---|---:|---|
| preserve \(\{f,p\}\) | 66 | false over exact reals and at cap 20 |
| change the favorite's partner | 72 | false at cap 20 |
| their union | 138 | false at cap 20 |

The same-favorite refutations have zero repairs in the 66-state family but
27 and 25 new-partner repairs. Conversely, the new-partner refutation has
zero repairs in the 72-state family but 12 same-favorite repairs. All
profiles satisfy the hard branch and have no full Hall cell. Therefore
neither mechanism can be selected in advance. A later profile blocks both.

The new-partner side itself splits into 36 former-triple partners and 36
unrepresented partners. Former-triple-only is false at cap 6 in both
encodings; unrepresented-only is false at cap 20 in CP-SAT. These smaller
refutations explained why static partner selection failed. The full-union
refutation shows that even an adaptive two-swap exchange is insufficient.

## Retired proof route

The attempted contradiction proof had the following finite shape.

1. Assume all 138 radius-two states fail EFX.
2. For each failed state, choose a Hall-deficient agent set in its
   four-agent bundle-feasibility graph.
3. Use the four terminal inequalities above to eliminate deficiencies
   incompatible with bundles unchanged by the corresponding swaps.
4. Separate the remaining witnesses into the same-favorite and new-partner
   mechanisms, but allow the argument to choose between them adaptively.
5. Show that simultaneous obstruction of both mechanisms forces a residual
   low pair \(L\) for which all 15 pairings pass the three-pair Hall test,
   contradicting the no-full-cell assumption.

Step 3 is the algebraic compression: it should replace 138 separate EFX
checks by a short list of Hall-witness types. Step 5 is the bridge to the
cap-free favorite-triple Hall characterization. The paired counterexamples
show that a proof treating either mechanism as globally dominant cannot
work.

The smallest attempted strengthening of Step 5 fixed the Hall cell in advance:

> If all 138 repairs fail in this canonical cell, then low pair
> \(\{p,a\}=\{1,2\}\) is a full favorite-triple Hall cell.

This pair joins the favorite's terminal partner to the representative of the
agent owning the all-representative triple. Forbidding only this cell uses 60
Hall-acceptance literals instead of 1,680. The strengthened negation still
initially returned `unknown` in both exact-real and cap-20 decision
formulations after 300 seconds. Guarded optimization subsequently refuted it.

The specific cell has a small hand-proof split. Its six remaining goods are
\(\{b,c,x,y,z,w\}\). Among their 15 perfect pairings:

- 3 pair (b) with (c) and pair the four unrepresented goods; and
- 12 pair each of (b,c) with an unrepresented good and pair the two goods
  left over.

Those two pairing-shape claims were the intended analytic compression, but
the decisive profile falsifies their required conclusion. The split may
still help classify Hall witnesses, but it cannot prove a radius-two repair.
The live proof target must allow the global 780-state eight-orbit family.

## Computational boundary and trust

The decisive cap-20 profile is

\[
\begin{pmatrix}
17&13&15&15&15&16&1&16&11\\
17&3&14&15&15&9&7&11&9\\
20&1&16&16&15&17&15&6&19\\
19&5&13&13&14&5&18&16&14
\end{pmatrix}.
\]

It satisfies the hard branch and terminal EFX matching, has no full Hall
cell, and has zero repairs in all 138 states. It is not an EFX
counterexample: it has 336 favorite-pair EFX partitions and 1,439 labeled
complete EFX allocations. Of its 290 eight-orbit repairs, 152 are at
distance three and 138 at distance four. The surviving target is therefore
global eight-orbit selection, not a two-move exchange.

The frozen census and artifact hashes are in the
[terminal-exchange audit](efx49_distinct_half_terminal_exchange_gate_audit.json).
The bounded cap-5 theorem and source links are in the
[terminal-exchange gate](DISTINCT_HALF_TERMINAL_EXCHANGE_GATE.md).

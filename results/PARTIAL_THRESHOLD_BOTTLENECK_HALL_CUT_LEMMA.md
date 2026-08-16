# Bottleneck Hall-cut reduction for the threshold selector

## Proved cap-free lemma

Fix a complete partition \(B=(B_0,\ldots,B_{n-1})\).  For every agent \(i\)
and bundle label \(b\), define the normalized EFX edge slack

\[
w_{ib}(B)=
\frac{v_i(B_b)-\max_{j\ne b}\tau_i(B_j)}{v_i(M)}.
\]

Let

\[
\beta(B)=\max_{\pi}\min_i w_{i,\pi(i)}(B),
\]

where \(\pi\) ranges over perfect matchings from agents to bundle labels.
At the bottleneck level \(\beta=\beta(B)\), form two bipartite graphs:

\[
G_{>\beta}=\{(i,b):w_{ib}(B)>\beta\},
\qquad
G_{\ge\beta}=\{(i,b):w_{ib}(B)\ge\beta\}.
\]

Then:

1. \(G_{\ge\beta}\) has a perfect matching;
2. \(G_{>\beta}\) has no perfect matching; and
3. if \(S\) is any Hall-deficient agent set in \(G_{>\beta}\), with
   deficiency
   \[
   d=|S|-|N_{>\beta}(S)|,
   \]
   then every perfect matching \(\pi\) in \(G_{\ge\beta}\) contains at
   least \(d\) agents \(i\in S\) such that
   \[
   \pi(i)\notin N_{>\beta}(S)
   \quad\text{and}\quad
   w_{i,\pi(i)}(B)=\beta.
   \tag{1}
   \]

Thus a strict critical Hall cut exposes not merely a zero-slack obstruction,
but a specified supply of bottleneck-equality edges crossing the cut.

### Full-cut one-bottleneck normal form

Suppose the smallest Hall-deficient agent set in \(G_{>\beta}\) is the full
set \(N\).  Then the strict graph uses exactly \(n-1\) bundle labels, say all
labels except \(b\), and there is a perfect matching in \(G_{\ge\beta}\)
with exactly one equality edge.  That equality edge enters \(b\); its other
\(n-1\) edges are strict.

To see this, every proper agent subset satisfies Hall in the strict graph.
Hence deleting any one agent leaves \(n-1\) agents that can be matched
strictly.  The strict graph itself has a matching of size \(n-1\), so its
total neighborhood has size at least \(n-1\); full-set deficiency makes it
at most \(n-1\).  Thus exactly one bundle label \(b\) is absent.  A weak
perfect matching supplies some weak edge \((a,b)\).  Match the proper subset
\(N-\{a\}\) strictly and add \((a,b)\).  Since no strict edge enters \(b\),
that one edge has weight exactly \(\beta\).

For four agents, this normal form turns the full-cut branch into a sharply
localized task: improve the one equality edge entering the missing bundle
while retaining a strict matching on the other three agents.

## Proof

An optimizer \(\pi\) in the finite definition of \(\beta(B)\) uses only
edges of weight at least \(\beta\), proving 1.  A perfect matching using only
edges of weight strictly greater than \(\beta\) would have bottleneck value
strictly greater than \(\beta\), contradicting the definition, proving 2.

For 3, at most \(|N_{>\beta}(S)|\) agents of \(S\) can be matched by \(\pi\)
into that neighborhood.  Hence at least \(d\) are matched outside it.  Their
matching edges are not in \(G_{>\beta}\), but they are in
\(G_{\ge\beta}\), so their weights equal \(\beta\). \(\square\)

## Partial-allocation corollary

For a one-floater state \((X,f)\), write

\[
H(X,f)=\max_h\beta(C_h(X,f)),
\]

where \(C_h(X,f)\) inserts \(f\) into host \(h\).  Put
\(\beta=H(X,f)\).  Then:

- for every host \(h\), the graph of edges in \(C_h(X,f)\) with slack
  strictly greater than \(\beta\) has no perfect matching;
- for every maximizing host, the graph of edges with slack at least
  \(\beta\) has a perfect matching; and
- for any successor one-floater state \((Y,g)\),
  \[
  H(Y,g)>\beta
  \quad\Longleftrightarrow\quad
  \text{some completion of }(Y,g)\text{ has a perfect matching using only
  edges of slack }>\beta.
  \tag{2}
  \]

Equation (2) is the exact Hall-gradient test.  It eliminates the nested
maximum over successor matchings: the proof needs to augment one strict
threshold graph across the old critical cut.

## Cut-crossing edge lemma

Let \(S\) be Hall-deficient in the old strict graph of a complete partition
\(P\) at level \(\beta\).  Suppose another complete partition \(Q\) has a
perfect matching \(\rho\) using only edges of slack strictly greater than
\(\beta\).  Then some \(i\in S\) is matched to a bundle

\[
b=\rho(i)\notin N^P_{>\beta}(S),
\]

and its individual edge slack crosses the cut:

\[
w_{ib}(P)\le\beta<w_{ib}(Q).
\tag{3}
\]

Indeed, injectivity permits at most \(|N^P_{>\beta}(S)|<|S|\) agents of
\(S\) to be matched inside the old neighborhood.  Any agent matched outside
it supplies (3).

Writing

\[
R_i(B,b)=\max_{j\ne b}\tau_i(B_j),
\]

the strict increase in (3) is exactly

\[
v_i(Q_b)-v_i(P_b)
>
R_i(Q,b)-R_i(P,b).
\tag{4}
\]

Thus every Hall-gradient step has a concrete local mechanism: it either
raises the value of a bundle outside the old deficient neighborhood, lowers
that observer's maximum competing threshold, or does both.  In particular,
if \(Q_b=P_b\), (4) forces a strict decrease of the competing threshold; if
all competing thresholds weakly increase, it forces a strict increase of the
candidate bundle's value.

Combined with
`PARTIAL_THRESHOLD_HALL_COMPLETION_MOVE_REDUCTION_LEMMA.md`, a strict
improvement need only be sought among three completed-partition operations:
a one-good transfer, a two-bundle swap, or a three-bundle augmenting path.
Reinsertion into the source is excluded identically.

## Exact audit and remaining gate

The exact-rational artifact
`partial_hall_threshold_plateau_exact_path_audit.json` constructs both graphs
at every one of its 4,848 selected strict-improvement steps.  In every case,
the strict graph is Hall-deficient and the weak graph has a perfect matching.
The minimum strict-cut witness sizes are 2 in 331 steps, 3 in 58 steps, and 4
in 4,459 steps.

For all 4,459 size-four witnesses, the strict graph has a three-bundle
neighborhood and therefore one missing bundle.  In 4,457 steps, that missing
bundle is the recipient selected by the completion-move trichotomy: the source
receives the old floater in a two-bundle swap, or the new host receives the
released good in a transfer or augmenting path.  The two remaining steps use
the competing-threshold side of (4) together with a changed matching.  This
near-degeneracy is evidence for the case split, not a universal theorem that
the missing bundle must receive a good.

Artifact SHA-256:
`16d1d9041c32278cf243462d8bea679926cced30817c21b34b9f2f53448fcdb2`.

The source owner is still not a universal member of a critical deficient set:
it belongs to some critical deficient set in 4,695 of 4,848 steps.  Therefore
the missing theorem is a cut-augmentation statement, not a fixed-role source
selection rule.  One must use the equality edges in (1), the two exact EFX
swap-wall types, and one of the three completed-partition moves to produce a
strict perfect matching as in (2).  No such universal augmentation theorem is
claimed here.

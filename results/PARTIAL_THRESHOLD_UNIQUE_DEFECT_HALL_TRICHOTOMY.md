# Four-agent unique-defect Hall trichotomy

## Statement

Consider the acceptance graph of a four-agent complete-bundle candidate whose
bundles are indexed by their old owners. Suppose:

1. every diagonal edge \(i\to i\) is present except \(b\to b\); and
2. the bad agent accepts a distinct host bundle, \(b\to h\).

If the graph has no perfect matching, then it has a Hall-deficient agent set
of exactly one of the following forms:

1. **bad--host pair:**
   \[
   S=\{b,h\},\qquad N(S)=\{h\};
   \]
2. **bad--host--external triple:** for one
   \(e\notin\{b,h\}\),
   \[
   S=\{b,h,e\},\qquad N(S)=\{h,e\};
   \]
3. **full witness:**
   \[
   S=N,
   \]
   and no agent accepts bundle \(b\). Equivalently, the three nonbad
   diagonal bundles are the full neighborhood.

The two choices of external agent in case 2 are symmetric. Thus there are
three unlabeled obstruction topologies.

## Proof

Let \(S\) be an inclusion-minimal Hall-deficient agent set. It must contain
\(b\): otherwise every agent in \(S\) has its distinct diagonal bundle as a
neighbor, so \(|N(S)|\geq|S|\).

The singleton \(S=\{b\}\) is not deficient because \(b\to h\) is present.

Suppose \(|S|=2\), writing \(S=\{b,x\}\). The neighborhood contains host
bundle \(h\) and diagonal bundle \(x\). These are distinct unless \(x=h\).
Hence deficiency is possible only for \(S=\{b,h\}\); its neighborhood already
contains \(h\), so Hall deficiency forces \(N(S)=\{h\}\). This is case 1.

Suppose \(|S|=3\). If \(h\notin S\), then the host bundle plus the two
distinct diagonal bundles of \(S-b\) give three neighbors, contradicting
deficiency. Therefore \(S=\{b,h,e\}\) for one external agent \(e\). Bundles
\(h\) and \(e\) are already distinct neighbors, so deficiency forces
\(N(S)=\{h,e\}\). This is case 2.

Finally let \(|S|=4\). The three nonbad diagonal bundles are distinct
neighbors. Deficiency forces them to be the entire neighborhood, which is
equivalent to bundle \(b\) having no incident acceptance edge. This is case
3. The cases exhaust all possible sizes of \(S\). \(\square\)

## Application to one-charity EFX

In the identity/unique-defect absorption branch, the hypotheses hold
automatically. All nonbad identity edges accept by definition. The unique
negative self edge of \(b\) is caused by inserting the charity good into host
\(h\), and the alternating-cycle argument proves \(b\to h\).

Therefore proving the owner-minimum release lemma for four agents requires
only three valuation cases:

1. both \(b\) and \(h\) accept no bundle outside \(h\);
2. \(b,h,e\) accept no bundle outside \(\{h,e\}\); or
3. bundle \(b\) has no acceptor at all.

Every other acceptance edge may be added freely; adding edges cannot destroy
a completion. These are maximal negative-space descriptions, so a proof may
assume the corresponding missing-edge inequalities without enumerating the
remaining graph.

In the exact plateau corpus, the topology split is 4,320 full witnesses, two
copies of one bad--host pair profile, and one bad--host--external triple
profile. All 4,320 full witnesses use the canonical bad-source minimum
handoff. The pair profile instead releases a good from an external source and
inserts it into the bad bundle. The triple profile keeps the charity good
fixed, swaps goods between two allocated bundles, and completes under a
nonidentity matching. These are corpus facts, not proofs of the proper-cut
repairs, but they align the three topologies with three different move
families.

## Claim boundary

The trichotomy is a complete cap-free graph theorem for the four-agent
identity/unique-defect branch. It does not prove that any of the three
topologies is incompatible with global \((\Theta,\Lambda)\)-maximality. That
valuation contradiction is the remaining release gate.

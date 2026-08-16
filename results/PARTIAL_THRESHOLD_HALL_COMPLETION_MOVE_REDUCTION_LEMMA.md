# Hall-margin completion-move reduction

## Proved cap-free lemma

Let \((X,f)\) be any one-floater allocation, and let \((Y,g)\) be obtained
by replacing a good \(g\in X_s\) with the floater \(f\):

\[
Y_s=X_s-\{g\}+\{f\},\qquad Y_j=X_j\quad(j\ne s).
\]

Write \(C_h(X,f)\) for the complete partition obtained by inserting \(f\)
into bundle \(h\), and let \(H(X,f)\) be the maximum normalized EFX
bottleneck margin over all insertion hosts and all bundle matchings.

Then

\[
C_s(Y,g)=C_s(X,f).
\tag{1}
\]

Consequently, if

\[
H(Y,g)>H(X,f),
\tag{2}
\]

no host attaining \(H(Y,g)\) can equal \(s\).

Fix a host \(h\) and matching attaining \(H(X,f)\), and a host \(k\) and
matching attaining \(H(Y,g)\).  Under (2), the change from the old best
complete partition \(P=C_h(X,f)\) to the new best complete partition
\(Q=C_k(Y,g)\) has exactly one of three forms:

1. **one-good transfer:** if \(s=h\), then \(k\ne s\), and \(Q\) is obtained
   from \(P\) by moving \(g\) from bundle \(s\) to bundle \(k\);
2. **two-bundle swap:** if \(s\ne h\) and \(k=h\), then \(Q\) is obtained
   from \(P\) by exchanging \(f\in P_h\) and \(g\in P_s\); or
3. **three-bundle augmenting path:** if \(s,h,k\) are distinct, then the
   changes are
   \[
   f:h\longrightarrow s,
   \qquad
   g:s\longrightarrow k.
   \]

The statement does not require four agents, bounded values, fixed bundle
sizes, EFX eligibility, or an owner-minimum choice of \(g\).  Those
hypotheses enter only when one tries to prove that an improving swap exists.

## Receiver-edge monotonicity

The first two move types have an additional cap-free property.  Use the edge
slack

\[
w_{ib}(B)=
\frac{v_i(B_b)-\max_{j\ne b}\tau_i(B_j)}{v_i(M)}.
\]

For a one-good transfer of a positive good \(g\) from bundle \(s\) to bundle
\(k\), every observer's edge to the receiving bundle strictly improves:

\[
w_{ik}(Q)>w_{ik}(P)
\qquad(i\in N).
\tag{3}
\]

Indeed, the candidate-bundle value rises by \(v_i(g)>0\), while removal of a
good cannot increase the source threshold and all other competing thresholds
are unchanged.

For the two-bundle swap, fix an observer \(i\).  If

\[
v_i(f)>v_i(g),
\tag{4}
\]

then its edge to the bundle \(s\) receiving \(f\) strictly improves:

\[
w_{is}(Q)>w_{is}(P).
\tag{5}
\]

The candidate value rises by \(v_i(f)-v_i(g)>0\).  In the competing host
bundle, replacing \(f\) by the lower-valued \(g\) cannot increase
\(\tau_i\), because \(\tau_i\) is the sum of all but a least-valued item and
is coordinatewise nondecreasing.  Every other competing threshold is
unchanged, proving (5).

The three-bundle augmenting path has no unconditional receiver monotonicity:
putting \(f\) into its middle bundle can raise the maximum threshold competing
with the terminal receiver.  That is the genuinely coupled residual case.

## Proof

Inserting the new floater \(g\) back into its source gives

\[
Y_s\cup\{g\}=X_s\cup\{f\},
\]

and every other bundle is unchanged.  This proves (1).  For every matching,
the bottleneck margin of \(C_s(Y,g)\) is therefore the margin of the identical
old completion candidate \(C_s(X,f)\), and so is at most \(H(X,f)\).  Under
(2), a maximizing new host cannot be \(s\).

It remains only to compare memberships in \(P=C_h(X,f)\) and
\(Q=C_k(Y,g)\).  If \(s=h\), the old best completion contains both \(f\) and
\(g\) in bundle \(s\), while the new one retains \(f\) there and inserts
\(g\) into \(k\).  This is case 1.  If \(s\ne h\) and \(k=h\), the old
completion places \(f\) in \(h\) and \(g\) in \(s\), while the new one
places \(g\) in \(h\) and \(f\) in \(s\).  This is case 2.  In the only
remaining possibility, \(s,h,k\) are distinct: the old host \(h\) loses
\(f\), the source \(s\) exchanges \(g\) for \(f\), and \(k\) receives
\(g\).  This is case 3. \(\square\)

## Exact corpus audit

The exact-rational threshold-plateau artifact
`partial_hall_threshold_plateau_exact_path_audit.json` records 4,848 strict
Hall-margin-increasing owner-minimum floater swaps.  Classifying each step by
the proved trichotomy gives:

- 2,374 one-good transfers;
- 2,440 two-bundle swaps; and
- 34 three-bundle augmenting paths.

No step reinserts the new floater into its source, as the lemma requires.
The old and new maximizing matchings are identical in 4,642 of the 4,848
steps.  These are finite corpus facts, not an existence theorem for an
improving step.

Artifact SHA-256:
`16d1d9041c32278cf243462d8bea679926cced30817c21b34b9f2f53448fcdb2`.

## Breakthrough boundary

Combined with the threshold-maximum swap lemma, the four-agent problem now
has a sharper remaining gate: starting from a blocked state maximizing first
the normalized owner-threshold potential and then \(H\), use a Hall witness
and the two exact EFX swap-wall families to force one of the three completed-
partition moves above with larger bottleneck margin.  The lemma proves the
move classification, not that one of the moves is feasible or improving.

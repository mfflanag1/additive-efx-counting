# Host-redirection audit for the unique-defect gate

## Question tested

Let \((X,\{f\})\) be an EFX-with-charity state for four additive agents.
Suppose inserting \(f\) into host bundle \(h\) under the identity assignment
has a unique bad agent \(b\), and its acceptance graph has the full Hall
witness: nobody accepts bundle \(b\).

The selected plateau corpus suggested a reciprocal pattern: inserting \(f\)
into bundle \(b\) makes only \(h\) bad. A weaker possible lemma said that this
redirection must either complete EFX or leave only \(h\) bad.

## Exact falsification outside the extremal slice

`unique_defect_host_redirection_n4m6_cap5_seed20260803.json` checks every
one-charity EFX state in each sampled valuation profile. It found 278 full,
unique-defect configurations before stopping in profile 25. Of the first 277,
275 completed under redirection and two produced the reciprocal unique defect.
The 278th produced two bad agents, refuting the weaker lemma.

The witness is

\[
V=\begin{pmatrix}
5&3&5&1&3&1\\
1&5&5&5&2&2\\
3&5&3&4&3&1\\
5&1&1&5&1&1
\end{pmatrix},
\]

with charity good 0 and bundle masks \((4,2,48,8)\). Inserting the charity
good into host 1 has unique bad agent 2 and a full Hall witness. Redirecting
it into bundle 2 makes agents 0 and 3 bad.

This is not a counterexample to the extremal selector. In fact the same
partial state has optimal absorption signature
\((0,0,1/19,7/18)\), attained by inserting the good into host 0 under the
identity assignment, so it is immediately completable. What fails is the
attempt to derive the redirection rule from EFX plus the full-witness graph
alone.

## Consequence for the proof program

The apparent host--bad two-cycle in all 4,320 canonical plateau transitions
is not a general consequence of the local Hall topology. Any useful
host-redirection lemma must use global \((\Theta,\Lambda)\)-maximality, or at
least compare against every alternative host and matching. This eliminates a
tempting but false local proof route and keeps the owner-minimum handoff as the
cleaner full-witness target.

## Claim boundary

The witness refutes only the stated local redirection implications. It does
not refute the extremal selector, four-agent EFX, or general EFX.

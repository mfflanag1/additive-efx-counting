# Uncompensated split-donor reassembly handoff lemma

**Date:** 2026-08-13

**Status:** cap-free elimination of the final fourth-donor payment separator;
the output returns to the sacrificed-hole response recurrence

## Split-donor candidate

Use the bottom-tail/fourth-owner state after packets `J,L,M` and the canonical
residual split have been selected.  Let the root `r`, protected owner `q`,
external hole `d`, and fourth donor `s` hold

\[
\begin{aligned}
Y_r&=A+G_r,\\
Y_q&=Q-(K\setminus J)+G_q,\\
Y_d&=(K\setminus J)+H+L,\\
Y_s&=E-L+M,
\end{aligned}                                      \tag{1}
\]

where all displayed packets are pairwise disjoint, `L subseteq E`,
`M subseteq W`, and

\[
 v_r(Y_r)>v_r(X_r),\qquad
 v_q(Y_q)\ge v_q(X_q),\qquad
 v_d(Y_d)>v_d(X_d).                                \tag{2}
\]

The original fourth-owner core `E` is common-safe and strictly desired by
`s`:

\[
 v_s(E)>v_s(X_s).                                  \tag{3}
\]

No payment assumption is made for `Y_s`.  In particular, (1) includes the
residual-compensation separator in which every q-compatible `M` fails to
restore `s`.

## Reassemble the donor core

Undo only the split of `E`: give `L` back to `s` and return `M` to the
external residual.  Define

\[
\begin{aligned}
Z_r&=Y_r,\\
Z_q&=Y_q,\\
Z_s&=E,\\
Z_d&=(K\setminus J)+H+M.
\end{aligned}                                      \tag{4}
\]

Equations (1) and (4) partition exactly the same physical goods.  The
incremental transfers are

\[
 d\longrightarrow s:L,
 \qquad s\longrightarrow d:M,                     \tag{5}
\]

with zero packets omitted.  Thus the reassembly is one bilateral connected
exchange whenever both packets are nonempty, and remains a connected
one-edge handoff when exactly one is nonempty.

By (2)--(3), `r` is strict, `q` is weakly paid, and `s` is strict.  Only the
external hole `d` may be below base.  Since `r` is earlier than `d` in the
fixed GG priority, every EFX instance of (4) strictly lexicographically
dominates `X`; payment of `d` is not required.

## Exact response continuation

If (4) is EFX with charity, global lexicographic maximality is contradicted.
Otherwise apply priority-sensitive response compression to (4).

1. The earlier root cannot be the missing source: it retains its permanent
   desired anchor.
2. If the protected `q` source is ordinary-response active, anchor-constrained
   matching represents it. If it is degree zero because `Q` remains split
   between `q` and `d`, the split-core root flip restores its coverage,
   grows retained support, or captures its response margin.
3. Source `s` holds the whole common-safe desired core `E` and is represented.
4. After that protected-q alternative is discharged, the only
   sacrifice-eligible missing source is the external owner `d`. Every wall
   is a represented-source response into the residual or a `d`-wall against
   a selected core.

The fixed-`U` arbitrary-hole residual selector applies to this exact state.
Every nonroot wall gives EFX/PI, unsafe response augmentation, strict
same-`d` residual progress, or response/support growth.  A survivor is the
already named root-facing handoff.  Therefore failure to compensate `s`
does not create a new payment terminal and cannot justify repeating the
same `(J,L,M)` selection.

At an exact repeated split/reassembly record, the complete signed-transfer
vector contains (5); full-state reconstruction therefore treats the repeat
as a physical decorated-response recurrence rather than forgetting the
donor exchange.  It then enters the component-saturation route.

## Theorem and boundary

Every compensated-fourth-owner payment separator admits the cap-free
priority-valid reassembly (4).  It closes by EFX/lex or returns to the
existing sacrificed-external-hole recurrence with the donor core restored.
There is no residual “fourth donor must be paid” branch.

[`audit_uncompensated_split_donor_reassembly_handoff.py`](../tracks/parkability/audit_uncompensated_split_donor_reassembly_handoff.py)
checks exact conservation, all payment/priority implications, transfer
support, and the four-owner missing-source classification independently of
the compensated selector.

This lemma does not alone terminate the root-facing handoff, prove observer
safety of (4), or close GG.  Those outputs are delegated explicitly to the
fixed-`U` recurrence and saturated-component extraction theorems.

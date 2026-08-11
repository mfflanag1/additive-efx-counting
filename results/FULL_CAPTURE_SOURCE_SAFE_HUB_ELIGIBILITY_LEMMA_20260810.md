# Full-capture source-safe hub-eligibility lemma

**Date:** 2026-08-10

**Status:** cap-free analytic lemma; the strictly separated bottom orientation
remains open

## Setting

Work in the representative full-`X_q` flower cell with priority
`r,q,c,s`.  Write

\[
X_r=T_r\mathbin{\dot\cup}B_r,
\qquad
X_q=T_q\mathbin{\dot\cup}B_q,
\]

and let `H=A_q intersect B_r`.  Full capture means
`A_q=T_q union H` and `B_q subseteq A_r`; all these packets are nonempty.
The displayed flower bundles are common-safe.  In particular,

\[
D_r=T_q+f,
\qquad
D_q=T_r+f,
\]

are desired by `r,q`, respectively, while `A_r` is desired by `c`.

Assume there are goods `h in H` and `b in B_q` satisfying

\[
v_q(h)\ge v_q(b). \tag{1}
\]

No comparison in `r`'s row is needed.

## Lemma

If every lex-valid common-safe cover in this cell fails, then `q` has a
nontrivial release packet `R subseteq X_q` which can be partitioned between
two leaves and satisfies

\[
v_q(f)>v_q(R). \tag{2}
\]

Thus `q` is an eligible hub for the charity-rooted two-leaf split.  The
statement is for arbitrary positive packets and has no item cap.

## Proof

First suppose `B_q={b}`.  The common-safe cover

\[
(Y_r,Y_q,Y_c,Y_s)=(D_c,A_q,A_r,Z)
\]

pays its only potentially unpaid recipient `q`, because

\[
v_q(A_q)=v_q(T_q)+v_q(H)
\ge v_q(T_q)+v_q(h)
\ge v_q(T_q)+v_q(b)=v_q(X_q).
\]

The other recipients are fixed or receive displayed desired bundles, with
`r` improving before any possible loss.  Common safety therefore makes the
cover EFX and lexicographically improving, contrary to simultaneous cover
failure.  Hence `B_q` contains at least two goods.

Assume for contradiction that (2) fails for every admissible packet.  Since
`B_q` itself can be split between two leaves,

\[
v_q(f)\le v_q(B_q). \tag{3}
\]

Put

\[
\mu=\min_{g\in T_q\cup\{f\}}v_q(g).
\]

If `mu=v_q(f)`, positivity gives
`v_q(B_r)+mu>=v_q(f)`.  Otherwise choose a minimum good `g in T_q`.
The two-good packet `{g,b}` is admissible, so failed eligibility and (1)
give

\[
v_q(f)\le v_q(g)+v_q(b)
\le \mu+v_q(h)
\le \mu+v_q(B_r). \tag{4}
\]

Because `q` desires `D_q=T_r+f`,

\[
v_q(T_r)+v_q(f)>v_q(T_q)+v_q(B_q).
\]

Combining this strict inequality with (3)--(4) yields

\[
\begin{aligned}
v_q(X_r)
 &=v_q(T_r)+v_q(B_r)\\
 &>v_q(T_q)+v_q(B_q)-v_q(f)+v_q(B_r)\\
 &\ge v_q(T_q)+v_q(f)-\mu
 =\tau_q(D_r). \tag{5}
\end{aligned}
\]

It remains to use only three common-safe covers.  Abbreviate

\[
R=v_q(X_r),\quad A=v_q(A_r),\quad C=v_q(X_c),\quad
d=\tau_q(D_r),\quad a=\tau_q(A_r),\quad c=\tau_q(X_c).
\]

Positivity gives `a<A` and `c<C`, while (5) gives `R>d`.
Failure of the covers paying `q` with `A_r`, `X_r`, and `X_c`, respectively,
forces

\[
A<\max\{d,c\},\qquad
R<\max\{d,c\},\qquad
C<\max\{d,a\}. \tag{6}
\]

The middle inequality and `R>d` imply `R<c<C`, so `C>R>d`.  The last
inequality in (6) then forces `C<a<A`.  But now both `d` and `c` are below
`C<A`, contradicting the first inequality in (6).  Therefore an eligible
packet (2) exists.  \(\square\)

## Exhaustive ordinal consequence

The full-capture cell now splits into two cap-free orientations:

1. **source-safe:** some `h in H,b in B_q` satisfy `v_q(h)>=v_q(b)`; the
   lemma forces a `q`-hub split or an immediate EFX cover;
2. **strictly separated:** every `b in B_q` and `h in H` satisfies
   `v_q(b)>v_q(h)`.

The second branch is exactly the source-`q` obstruction in the bilateral
swap lemma.  A frozen exact model realizes it while blocking all two-good
hub eligibility.  Its nearest partial EFX improvement is the two-edge owner
path `q -> c -> r`, so the next selector must route the strictly separated
orientation through a packet transfer component rather than another hub
eligibility assertion.

## Verification and claim boundary

The five scalar implications replay as QF_LRA-UNSAT under Z3 5.0.0 in
[`full_capture_source_safe_hub_eligibility_audit.json`](full_capture_source_safe_hub_eligibility_audit.json).
The atomized proof-mining core is
[`three_nonsingleton_flower_no_hub_eligibility_core.json`](three_nonsingleton_flower_no_hub_eligibility_core.json).

The newly proved captured-bottom external-compensation chain supplies the
cap-free `q -> external -> r` packet operation required by the strictly
separated orientation, but its top-switch/source-capture endpoints remain
open.  This lemma supplies hub eligibility only in the source-safe orientation of
the representative full-capture source/order cell.  It does not prove that
the resulting split is EFX or has an internal response matching, and it does
not close the strictly separated orientation, the other source/order cells,
or the `GG` flower class.

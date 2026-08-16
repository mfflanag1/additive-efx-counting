# Lex-sacrificed response-compression lemma

**Date:** 2026-08-11

**Status:** cap-free priority-sensitive obstruction reduction; the terminal
two-sided wall star remains open


*Convention note 2026-08-16 (`tau`).* This file uses `tau` **without defining it** (inherited), once, in (6). The use is
convention-agnostic: it needs only that `tau_d(A_i)` bounds the one-good deletions
of `A_i`, which both readings supply.

The two forms coincide **only under additivity**: for additive `v`,
`max_{g in Z} v(Z\{g}) = v(Z) - min_{g in Z} v(g)`, but for a merely monotone
cancelable `v` they are different functionals. Composing this file with one that
uses the other form is therefore sound only inside the additive class, where this
rung currently sits. The rung's live conflict —
`FLOWER_MINIMAL_PAYMENT_RESIDUAL_ROTATION_LEMMA_20260810` and
`FLOWER_RESIDUAL_WALL_PAYMENT_POLARITY_LEMMA_20260810` (additive form) against
`CROSS_STAR_HOLE_PIVOT_LEMMA_20260811` (max-deletion) — is recorded at section 8,
item 2 of
[`THREE_NONSINGLETON_CANCELABLE_CONSTRAINT_MAP_20260816.md`](THREE_NONSINGLETON_CANCELABLE_CONSTRAINT_MAP_20260816.md).
Nothing is broken today; the banner exists so the conflict cannot hide when the
rung's proofs are composed. **Labeling only**: no definition and no step in this
file is changed.

## Own-bundle capture identity

Use any response compression with selected disjoint cores `A_i`, missing
source `d`, and residual `W`. Split the selected goods according to their
base provenance:

\[
C=X_d\cap\mathop{\dot\bigcup}_{i\in S}A_i,
\qquad
E=\left(\{f\}+\mathop{\dot\bigcup}_{k\ne d}X_k\right)
\setminus\mathop{\dot\bigcup}_{i\in S}A_i. \tag{1}
\]

Then

\[
W=(X_d\setminus C)+E \tag{2}
\]

and the missing source's exact change is

\[
v_d(W)-v_d(X_d)=v_d(E)-v_d(C). \tag{3}
\]

Thus every unpaid weighted compression has a nonempty own-bundle capture
packet and the strict orientation

\[
v_d(C)>v_d(E). \tag{4}
\]

This is the packet-level content of the assignment-cost inequality: the
selected response cores can exceed the outside-good budget only by capturing
goods originally owned by the missing source.

## Priority split

If `d=r`, condition (4) is the genuine earlier-root obstruction: the bridge
must return enough of `C`, pay `r` from `E`, or change the response cores.

Suppose instead that `d!=r`. Then `r in S`, so `r` receives a common-safe
desired core `A_r` and strictly improves. If `d` is external, then `q in S`
also strictly improves, so an EFX `Z` is exactly the required flexible
endpoint even though the external owner loses. If `d=q`, every other owner
improves and `r` precedes `q`, so an EFX `Z` is a strict global
lexicographic improvement. Thus an EFX endpoint closes in every non-`r`
case, but for the appropriate one of two different reasons.

Put

\[
\delta=v_d(C)-v_d(E)>0. \tag{5}
\]

If `Z` is not EFX, its failures have only the following two forms.

1. **Sacrificed-owner core wall.** Owner `d` may strongly envy a selected
   core `A_i`. Since `A_i` is common-safe relative to `X`, its threshold is
   confined to the exact loss band
   \[
   v_d(X_d)-\delta
   <\tau_d(A_i)\le v_d(X_d). \tag{6}
   \]
2. **Residual wall.** Any source owner `i in S` may strongly envy `W`.

There are no other failures. Every source owner is strictly better than in
`X` and hence remains safe against all three common-safe cores. The
sacrificed owner is automatically EFX-safe against her own residual target
`W`. Therefore only `d -> {A_i}` and `{i in S} -> W` comparisons can fail.

This is a two-sided star, not a general four-target obstruction. A response
to `W` can be handled by the one-wall recapture operation. A wall by `d`
against `A_i` is confined to the loss band (6), so returning part of the
captured packet `C` to `d` or replacing the corresponding core crosses one
quantified deficit rather than reopening arbitrary EFX constraints.

## Singleton specialization

If the missing source is the singleton owner `s`, then an unpaid compression
must capture her unique good `z`: `C={z}`. Hence

\[
v_s(z)>v_s(E), \tag{7}
\]

and exactly one selected response core contains `z`. The entire sacrificed-
owner side of the wall star is therefore rooted at that one core. This does
not by itself pay the source who received `z`, but it reduces the singleton
branch to one explicit good-versus-residual comparison.

The capture identity and wall-band implications replay in
[`lex_sacrificed_response_compression_audit.json`](lex_sacrificed_response_compression_audit.json).

## Claim boundary

This lemma converts every unpaid non-`r` compression into a priority-valid
candidate with an exact two-sided wall star, and converts an unpaid `r`
compression into the own-packet capture inequality (4). It does not
eliminate the wall star, pay the earlier root, prove that a recapture or
captured-packet return terminates, close the `GG` flower, or prove four-agent
additive EFX.

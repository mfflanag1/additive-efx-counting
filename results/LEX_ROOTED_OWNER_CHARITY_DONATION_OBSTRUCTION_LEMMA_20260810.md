# Lex-rooted owner/charity donation obstruction lemma

**Date:** 2026-08-10

**Status:** cap-free analytic component lemma; flower-specific selection and
termination remain open


*Convention note 2026-08-16 (`tau`).* This file uses the **additive form**, stated explicitly in the displayed threshold
`tau_i(R+x) = v_i(R) + max{v_i(x) - min_{z in R} v_i(z), 0}`.

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

## Operation

Let `(X,P)` be an EFX-with-charity allocation for positive additive
valuations.  Let `r` precede `q` in the fixed priority, choose goods
`g in X_r` and `h in X_q`, and form

\[
Y_r=X_r-g+h,
\qquad
Y_q=X_q-h,
\qquad
Q=P+g,
\]

leaving every other owner fixed.  Assume

\[
v_r(h)>v_r(g). \tag{1}
\]

Then `r` strictly improves, so `Y` is a strict lexicographic improvement
whenever it is EFX with charity.  If it is not, at least one of the following
exhaustive walls occurs.

1. **Root charity wall:**
   `v_r(Y_r)<v_r(P+g)`.
2. **Donor payment wall:** `q` fails an EFX comparison against an owner
   target or fails dominance of `P+g`.
3. **External root-target wall:** some `i notin {r,q}` strongly envies
   `X_r-g+h`.  This forces
   \[
   v_i(h)>v_i(g), \tag{2}
   \]
   and an inclusion-minimal envied subset supplies a generalized
   `({h}|{g})` edge into `r`.
4. **External charity wall:** some `i notin {r,q}` envies `P+g`.  Since the
   old charity was dominated, this forces
   \[
   v_i(g)>v_i(X_i)-v_i(P). \tag{3}
   \]
   Any inclusion-minimal envied subset of `P+g` must contain `g`, so the
   wall supplies a charity-to-owner component consuming the newly released
   good.

## Proof

By (1), `r` strictly improves.  Every unchanged target remains safe for
`r`, and target `q` only loses `h`, so its EFX threshold weakly decreases.
Thus `r` can fail only against the enlarged charity.

Agent `q` loses `h`; all of her possible failures are therefore retained as
the donor-payment branch.  This is essential: lexicographic improvement
allows the later donor to lose, so a Pareto-only owner-rooted star does not
cover the operation.

An external observer keeps her old bundle.  All targets except `r,q` are
unchanged, and target `q` only shrinks.  Hence she can fail only against the
changed root target or the enlarged charity.  For a fixed residual bundle
`R=X_r-g`, the threshold

\[
\tau_i(R+x)
=v_i(R)+\max\{v_i(x)-\min_{z\in R}v_i(z),0\}
\]

is nondecreasing in `v_i(x)`.  Old EFX and a strict new wall against
`R+h` therefore force (2).  Taking an inclusion-minimal envied subset gives
the stated generalized edge and releases `g`, plus any additional discard.

For a charity wall, old and new dominance give

\[
v_i(X_i)\ge v_i(P),
\qquad
v_i(X_i)<v_i(P)+v_i(g),
\]

which is (3).  No subset of `P` alone can be envied, so every minimal envied
subset of `P+g` contains `g`.  These cases exhaust every changed inequality.
\(\square\)

## Flower consequence

The exact residual packet countermodel shows this operation is genuinely
needed.  It blocks the eight-allocation global-lex core and the early-root
charity rotation, yet its unique distance-two escape has signature

\[
q\longrightarrow r:h,
\qquad
r\longrightarrow\mathrm{charity}:g,
\]

with `h in B_q` and `g in K`.  The earlier owner improves and the later
owner loses.  Therefore the final flower component theorem cannot require
every changed owner to improve, cannot keep charity cardinality fixed, and
cannot treat the selected later-owner replacement as permanent.

The exact nondegenerate profile and solver-free audit are
[`residual_flower_packet_countermodel.json`](residual_flower_packet_countermodel.json)
and
[`residual_flower_packet_countermodel_audit.json`](residual_flower_packet_countermodel_audit.json).
The dual-solver atomic-versus-packet decision is
[`residual_flower_packet_candidate_audit.json`](residual_flower_packet_candidate_audit.json):
the nine candidates are UNSAT when every packet is atomic but SAT for
realizable arbitrary packets.
The scalar wall implications replay in
[`lex_rooted_owner_charity_donation_obstruction_audit.json`](lex_rooted_owner_charity_donation_obstruction_audit.json).

## Claim boundary

The lemma classifies every failure after `g,h` have been selected.  It does
not prove that the flower always supplies a pair satisfying (1), pay a donor
wall, eliminate an external charity wall, terminate the resulting component,
close `GG`, or prove four-agent additive EFX.

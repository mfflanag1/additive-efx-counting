# Flower later-owner singleton-replacement selector lemma

**Date:** 2026-08-10

**Status:** cap-free analytic selector across every hard flower cell;
dependency closure remains open


*Convention note 2026-08-16 (`tau`).* This file uses `tau` **without defining it** (inherited). Its displayed use,
`tau_q(D_r) = v_q(T_q)` at (2), is phrased in the additive "minimum good" idiom;
the constraint map records that this identity also holds under the max-deletion
reading, via the cancelable biconditional C2.

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

## Statement

Work in the representative full-`X_q` flower cell with priority
`r,q,c,s`.  Write

\[
X_r=T_r\mathbin{\dot\cup}B_r,
\qquad
X_q=T_q\mathbin{\dot\cup}B_q,
\]

where all four packets are nonempty.  The mutual flower bundles

\[
D_r=T_q+f,
\qquad
D_q=T_r+f
\]

are desired by `r` and `q`, respectively.  Suppose every lex-valid
common-safe cover in the full-capture cell fails.

Then there is a good `g in X_q` such that

\[
v_q(f)>v_q(g). \tag{1}
\]

Consequently the one-good packet-for-charity replacement

\[
Y_q=X_q-g+f,
\qquad
P_Y=\{g\}
\]

strictly improves `q` and supplies a cap-free starting operation for the
transfer-component growth process.

## Proof

Assume contrariwise that `v_q(f)<=v_q(g)` for every `g in X_q`.  Since
`T_q` is nonempty, `f` is a minimum good of `D_r=T_q+f`; hence

\[
\tau_q(D_r)=v_q(T_q). \tag{2}
\]

Since `B_q` is nonempty, the same assumption gives
`v_q(B_q)>=v_q(f)`.  Agent `q` desires `D_q`, so

\[
v_q(T_r)+v_q(f)>v_q(T_q)+v_q(B_q).
\]

It follows that

\[
v_q(X_r)>v_q(T_r)>v_q(T_q)=\tau_q(D_r). \tag{3}
\]

Now use the three lex-valid common-safe covers in which `q` receives,
respectively, `A_r`, `X_r`, and `X_c`, while `r` receives `D_r` and the
remaining recipients are fixed or receive displayed desired bundles.  Put

\[
R=v_q(X_r),\quad A=v_q(A_r),\quad C=v_q(X_c),
\]

and

\[
d=\tau_q(D_r),\quad a=\tau_q(A_r),\quad c=\tau_q(X_c).
\]

The bundles `A_r` and `X_c` are nonsingleton, so positivity gives
`a<A` and `c<C`; equation (3) gives `R>d`.  Simultaneous failure of the
three covers forces

\[
A<\max\{d,c\},\qquad
R<\max\{d,c\},\qquad
C<\max\{d,a\}. \tag{4}
\]

The middle inequality and `R>d` imply `R<c<C`, hence `C>R>d`.  The last
inequality in (4) then forces `C<a<A`.  But both `d` and `c` are now below
`C<A`, contradicting the first inequality in (4).  Thus (1) holds.
\(\square\)

## Component consequence

Apply the packet-for-charity replacement obstruction lemma to a selected
good `g` satisfying (1).  Exactly one of the following occurs:

1. the replacement is EFX with charity and lexicographically improves the
   base state;
2. an external target wall has polarity `v_i(f)>v_i(g)` and supplies a
   generalized `({f}|{g})` edge into `q`;
3. an external charity wall has the opposite polarity
   `v_i(g)>v_i(f)`.

Therefore the full-capture flower always supplies a first improving
packet/component.  The earlier endpoint-selection gap is reduced to routing
the two wall types through a finite owner/charity dependency component.

## Verification and claim boundary

The two aggregate implications replay as QF_LRA-UNSAT under Z3 5.0.0 and
4.15.3 in
[`full_capture_single_replacement_selector_audit.json`](full_capture_single_replacement_selector_audit.json).

This proves selection of an improving operation, not termination of its
dependency growth.  It is scoped to the representative full-capture
source/order cell.

## All-hard-cell theorem

The same conclusion holds across the entire hard normal form of the flower,
including the opposite-source crossing cells and the priority-restricted
full-`X_r` dual:

> In every one of the 1,020 cap-free packet-minimum cells surviving the
> common-safe cover theorem, the later owner on the mutual `r,q` champion
> cycle values `f` strictly above at least one good of her current bundle.

The proof above does not use full capture or the identity of the source of
`A_r`.  It uses only that `A_r` is crossing and hence nonsingleton, that
`D_r,D_q` are the two mutual desired bundles, and that the following three
common-safe covers are available when `r` precedes `q`:

1. `r` receives `D_r` and unpaid `q` receives `A_r`;
2. `r` receives `D_r` and unpaid `q` receives `X_r`;
3. `r` receives `D_r` and unpaid `q` receives `X_c`, while `A_r` goes to
   its displayed source.

All remaining recipients are fixed or receive displayed desired bundles.
The strict improvement of `r` precedes the only potentially losing owner
`q`, so all three covers are lex-valid.  Their failure gives exactly the
three-wall cycle used above.  Swapping `r,q` proves the statement when `q`
precedes `r`.  Thus the later mutual-cycle owner is always the selected
owner, for every crossing, full-`X_q`, and priority-restricted full-`X_r`
hard cell.

The exact total/minimum audit verifies that these analytic interfaces cover
every cell in the cap-free hard normal form.  For each surviving
support/source/order cell, it adds the contrary inequality

\[
v_\ell(f)\le \min_{g\in X_\ell}v_\ell(g),
\]

where `ell` is the later of `r,q`.  All 1,020 systems are QF_LRA-UNSAT.
The owner-resolved census is especially simple:

- if `r` precedes `q`, `q` is individually forced in all 501 such cells;
- if `q` precedes `r`, `r` is individually forced in all 519 such cells;
- 121 cells force both mutual-cycle owners individually;
- no cell requires a merely disjunctive all-owner argument.

The replay is
[`three_nonsingleton_flower_single_replacement_selector_family_audit.json`](three_nonsingleton_flower_single_replacement_selector_family_audit.json),
and is independent of packet cardinality.  Swapping `r,q` supplies the four
arm-source-`q` patterns.  Therefore first-operation selection is closed
throughout the eight flower source symmetries.

The normal-form coverage and its encoding still need independent audit.  The
analytic selector proves selection of an improving operation, not
termination of the resulting wall dependency, and it does not close the
remaining seven selected-cycle classes.

## Packet-location refinement

The exact hard-cell census further localizes—but does not completely locate—
the selected good. In 754 of the 1,020 cells, every eligible later-owner good
lies in that owner's displayed bottom packet. The owner-resolved counts are
357 of 501 cells with later owner `q` and 397 of 519 with later owner `r`.
The remaining 266 cells retain a genuine top/bottom disjunction, and no cell
forces eligibility in the top packet alone. See
[`three_nonsingleton_flower_single_replacement_location_census.json`](three_nonsingleton_flower_single_replacement_location_census.json).

This refinement can attach the first dependency directly to a released
bottom edge in most cells. It is not universal, so a cap-free termination
proof must either handle the 266 disjunctive cells separately or avoid using
bottom location as a premise.

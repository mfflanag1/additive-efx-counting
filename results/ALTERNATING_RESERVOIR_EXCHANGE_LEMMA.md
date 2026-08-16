# Alternating reservoir-exchange lemma

**Date:** 2026-08-09

**Status:** cap-free analytic theorem

**Order:** `(p,s,r,q)` with `p={x}` fixed

## Setup

Let `X` be the strict alternating partial EFX allocation, with

\[
X_p=\{x\},\qquad X_s=\{y\},\qquad
X_r=T_r\mathbin{\dot\cup}B_r,\qquad
X_q=T_q\mathbin{\dot\cup}B_q,
\]

and unallocated good `f`.  Put `b_i=v_i(X_i)` and

\[
\tau_i(Z)=\max_{g\in Z}v_i(Z\setminus\{g\}).
\]

A set is *common-safe* when `tau_i(Z)<=b_i` for every agent.  Assume:

1. `D=T_q+f` is desired by `s`;
2. no subset of `X_r+H`, for any `H subseteq B_q`, is desired by `p` or
   `q`; and
3. values are positive and `B_q` is nonempty.

Condition 2 is exactly the absence of the two compatible generalized
champion families from `p` and `q` into `X_r`.

## Minimal-crossing fact

If some agent values a finite pool `P` above her base utility, then `P`
contains a desired set.  Choose, under inclusion, a minimal set `E subseteq
P` on which at least one agent crosses her base utility.  Every one-good
deletion of `E` is below every observer's base utility.  Thus `E` is
common-safe and is desired by an agent who crosses on `E`.

## Theorem

> There are disjoint common-safe sets `A,Q` such that `A` is desired by
> `r` or `s` and `v_q(Q)>=tau_q(A)`.

Consequently the two-safe-bundle reduction gives an EFX allocation that
lexicographically improves `X` in priority order `(p,s,r,q)` while fixing
`p={x}`.

## Adaptive-order escape corollary

Start from an arbitrary one-charity-good alternating champion-cycle state.
If a compatible generalized champion family is present, its standard PI
cycle gives an immediate EFX improvement. Otherwise the two compatible
families into `X_r` are absent, so the theorem above gives an explicit
external-observer-safe EFX improvement in order `(p,s,r,q)`. Half-turn
relabeling gives the same conclusion in order `(s,p,q,r)`.

Thus the surviving-order branch of the adaptive-root/order program is
cap-free: no further root change is needed in `(p,s,r,q)` or `(s,p,q,r)`;
one may use the reservoir exchange directly. The proof does not require a
packet-size cap or a fixed finite move menu. It does not transfer
lexicographic maximality between different priority orders, and therefore
does not itself close the four hard orders listed below. The later
dual-reservoir theorem closes two of them by a different construction.

## Proof

Let

\[
U=X_r+B_q,\qquad t=\tau_q(D).
\]

The sets `D` and `U` are disjoint.  Because `r` owns `X_r` and valuations
are positive,

\[
v_r(U)>v_r(X_r)=b_r.
\tag{1}
\]

The minimal-crossing fact supplies a desired set inside `U`.  Assumption 2
rules out `p` and `q` as its source, so every minimal desired set used below
is desired by `r` or `s`.

First suppose `v_q(U)<t`.  Choose any inclusion-minimal desired set
`A subseteq U`.  Then

\[
\tau_q(A)\le v_q(A)\le v_q(U)<t\le v_q(D).
\]

Both `A` and `D` are common-safe and disjoint, so `(A,D)` is the required
pair.

Now suppose `v_q(U)>=t`.  Choose an inclusion-minimal set `Q subseteq U`
such that `v_q(Q)>=t`.  If `Q` is common-safe, then `(D,Q)` is the required
pair.

Otherwise there are an observer `i` and a good `h in Q` for which

\[
v_i(Q-h)>b_i.
\tag{2}
\]

Apply the minimal-crossing fact inside `Q-h`, obtaining a desired set
`A subseteq Q-h`.  Minimality of `Q` at the `q` threshold gives

\[
v_q(A)\le v_q(Q-h)<t\le v_q(D).
\]

Again `A` is desired by `r` or `s`, and `(A,D)` is a disjoint common-safe
pair satisfying `v_q(D)>=tau_q(A)`.  This exhausts all cases. \(\square\)

## Consequences and boundary

The theorem proves the external-observer-safe lexicographic improvement
lemma for `(p,s,r,q)` for arbitrary packet sizes.  Half-turn relabeling
proves the symmetric order `(s,p,q,r)`.

The external-observer candidate is exactly false in the other six hard
orders.  The separate cap-free root-flip theorem nevertheless closes two of
those orders, `(p,q,r,s)` and `(s,r,q,p)`, by a different rival form.  The
other four hard orders require different constructions, and the later
[`dual-reservoir trichotomy`](ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY.md)
supplies constructions for **all four** of them: `(p,s,q,r)` and `(p,q,s,r)`
directly, and `(s,p,r,q)` and `(s,r,p,q)` by half-turn relabeling.  The
reason is that its alternative 2 (the anchored `q`-handoff) fixes both `p`
and `s` at exactly their base utilities and strictly improves `q`, while `r`
is last in both `p`-rooted orders, so `r`'s loss is never reached; its
alternatives 1 and 3 improve the first-priority agent `p` outright.  The
present theorem does not revive the refuted candidate in any of those orders
and does not by itself prove complete additive EFX.

> *Correction, referee repair 2026-08-16* (gap G3 of the referee report
> [`TWO_NONSINGLETON_COMPOSITION_REFEREE_REPORT_20260816.md`](TWO_NONSINGLETON_COMPOSITION_REFEREE_REPORT_20260816.md)).
> The paragraph above previously
> read that the trichotomy covers only `(p,s,q,r)` and `(s,p,r,q)`, "leaving
> `(p,q,s,r)` and `(s,r,p,q)`".  That sentence was stale and contradicted
> both
> [`ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY.md`](ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY.md)
> (its "Cap-free priority-order consequence") and
> [`ALTERNATING_GLOBAL_LEX_CAPFREE_THEOREM.md`](ALTERNATING_GLOBAL_LEX_CAPFREE_THEOREM.md)
> (item 4 of its order cover), which credit the trichotomy with all four
> orders.  The stale sentence was the error; the four-order claim is correct,
> for the reason now given above.  Nothing in the present lemma's own proof
> changes.

The replay script checks the construction on the frozen exact profiles and
on targeted countermodels to the false fixed-payment strengthenings.  That
audit is corroboration, not a premise of the proof.

Primary replay artifacts:

- [`alternating_reservoir_exchange_audit.json`](alternating_reservoir_exchange_audit.json)
  (18 frozen profiles covering all three proof branches);
- [`audit_alternating_reservoir_exchange.py`](../tracks/parkability/audit_alternating_reservoir_exchange.py);
- [`test_alternating_reservoir_exchange.py`](../tracks/parkability/test_alternating_reservoir_exchange.py); and
- [`alternating_initial_reservoir_refutation_2222.json`](alternating_initial_reservoir_refutation_2222.json),
  showing that the low-reservoir case is genuinely necessary.

The exact root-only obstruction in
[`ADAPTIVE_ROOT_ORDER_BRIDGE_REFUTATION_20260809.md`](ADAPTIVE_ROOT_ORDER_BRIDGE_REFUTATION_20260809.md)
explains why this suffix reallocation is essential: both canonical promoted
root rotations can fail EFX strictly, while a later-priority packet transfer
still escapes. The reservoir theorem supplies the cap-free version of that
missing operation.

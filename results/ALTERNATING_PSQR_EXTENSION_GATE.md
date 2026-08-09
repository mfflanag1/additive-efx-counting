# The `(p,s,q,r)` extension-or-handoff gate

**Date:** 2026-08-09

**Status:** unrestricted cap-free target exactly refuted; cap-free reduction
and completion lemmas retained as route diagnostics

## Final verdict

The anchored-or-any-desired extension lemma is false as stated.  A strictly
positive additive profile already refutes it in the eight-good packet cell
`(1,1,2,1)`, where only `T_q` is split:

| agent | `tr` | `br` | `tq0` | `tq1` | `bq` | `x` | `y` | `f` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `p` | 281 | 265 | 32 | 40 | 273 | 554 | 546 | 281 |
| `r` | 283 | 8 | 243 | 24 | 12 | 4 | 554 | 8 |
| `s` | 22 | 4 | 10 | 16 | 28 | 2 | 255 | 231 |
| `q` | 6 | 2 | 18 | 3 | 28 | 192 | 16 | 19 |

The base utilities are `(554,291,255,49)` for `(p,r,s,q)`.  The only
`p`-desired subset of the champion offer `X_r+f` is `{tr,f}`.

Exact enumeration of all `5^8=390625` partial allocations gives:

- 716 anchored EFX allocations, but zero that improve priority order
  `(p,s,q,r)`;
- 4,096 allocations with `p` on a desired champion-offer subset, but zero
  that are EFX; and
- 4,919 unrestricted EFX allocations, including 174 lexicographic
  improvements.

Thus this refutes the proposed dichotomy, not EFX existence.  For example,

\[
p\leftarrow\{tr,br,tq0,tq1\},\quad
r\leftarrow\{y\},\quad
s\leftarrow\{bq,f\},\quad
q\leftarrow\{x\}
\]

is EFX and strictly improves all four agents.  The new root bundle is not a
desired set relative to the base: its `p`-deletion threshold is 586, above
`b_p=554`, and its `r`-deletion threshold is 550, above `b_r=291`.  It becomes
safe only because `p` and `r` improve simultaneously.  This identifies the
precise defect in the desired-set extension strategy.

Half-turn relabeling gives a byte-explicit counterexample for order
`(s,p,r,q)` in cell `(2,1,1,1)`.  Both profiles are verified by full exact
enumeration, a separate QF_LIA owner encoding, and QF_LRA structural-cell
membership in
[`alternating_psqr_unrestricted_refutation_audit.json`](alternating_psqr_unrestricted_refutation_audit.json).

## Setup

Use the alternating state

\[
X_p=\{x\},\qquad X_s=\{y\},\qquad
X_r=T_r\mathbin{\dot\cup}B_r,\qquad
X_q=T_q\mathbin{\dot\cup}B_q,
\]

with charity good `f`, selected desired blocks `T_r+f` for `p` and `T_q+f`
for `s`, and all four compatible cross-bottom families absent.  Write
`b_i=v_i(X_i)` and

\[
\tau_i(Z)=\max_{g\in Z}v_i(Z-g).
\]

The target priority order is `(p,s,q,r)`.  Its half-turn is `(s,p,r,q)`.

## Exact reduction supplied by the reservoir theorem

Apply the existing reservoir-exchange theorem to

\[
D_s=T_q+f,\qquad U=X_r+B_q.
\]

It returns disjoint common-safe bundles `A,Q`, with `A` desired by `r` or
`s` and `v_q(Q)>=tau_q(A)`.

- If `A` is desired by `s`, the resulting anchored allocation improves the
  second-priority agent and therefore solves `(p,s,q,r)`.
- If `A` is desired by `r` and `v_q(Q)>=b_q`, it keeps `p,s` fixed, weakly
  improves `q`, and strictly improves `r`, so it also solves the order.
- In the remaining output branch, `A` is desired by `r`, `Q=D_s`, and
  `v_q(D_s)<b_q`.

Thus only the last low-`q` branch needs a new construction.  This deduction
is cap-free and does not depend on the exact packet encoding.

## Promotion as a three-by-three threshold matching

Let `D subseteq X_r+f` be desired by `p`, and let `C` be disjoint from
`D,x,y`.  Give `D` to `p` and match the three bundles

\[
\{x\},\quad \{y\},\quad C
\]

bijectively to `r,s,q`.  The resulting allocation is EFX exactly when:

1. `v_p(D)>=tau_p(C)`; and
2. for every suffix agent `i`, its matched bundle dominates `D`, and, unless
   it receives `C`, also dominates `C`, at the corresponding deletion
   thresholds.

Because `D` is desired by `p`, every such matching is a promoted-root
lexicographic improvement.  This is the correct split-packet lift of the
three promoted atomic rivals.  The atomic rivals use `q<-x`; exact binary
profiles also require matchings with `r<-x`, which explains why the earlier
single-observer two-safe gate was false.

## Anchored suffix handoffs

The other sufficient construction fixes `p=x` and `s=y`.  If `A` is a
common-safe desired bundle for `q`, `C` is disjoint and common-safe, and

\[
v_r(C)\geq\tau_r(A),
\]

then assigning `q<-A` and `r<-C` is EFX and improves `(p,s,q,r)`.  The
symmetric suffix construction assigns a desired bundle to `s`, gives `y` to
`r`, and uses a `q`-threshold payment.  These are the packet forms of the
anchored side of the dichotomy.

## Dual-bottom safety lemma

Put `W=B_r+B_q`.  Every subset of `W` has value at most `b_i` for every
agent `i`, and hence every subset of `W` is common-safe.

Indeed, `W` lies in both cross reservoirs `X_r+B_q` and `X_q+B_r`.  The
compatible-family absences exclude `p,q` as sources of desired subsets in
the first reservoir and exclude `r,s` in the second.  If some subset of `W`
crossed any agent's base utility, inclusion-minimal crossing would produce a
desired subset whose source is one of the four agents, contradicting one of
those exclusions.

This is cap-free.  It lifts the automatic safety of the atomic payment
`B_r+B_q` to arbitrary packets.

## Exact proof-mining boundary

The four-rival atomic failure walls reduce to three immediate opposite-sign
pairs and one exceptional four-wall core.  They are replayed in
[`alternating_psqr_atomic_walls.json`](alternating_psqr_atomic_walls.json).

Under the strengthened hard-branch premises

1. `v_q(T_q+f)<b_q`;
2. no `s`-desired subset lies in `X_r+B_q`; and
3. no common-safe subset of `X_r+B_q` pays the `q` threshold of `T_q+f`,

the union of

- promoted threshold matchings,
- anchored `q` handoffs, and
- anchored `s` handoffs

is exact QF_LRA-UNSAT in the atomic cell.  The same direct binary-packet
encoding returns `unknown/timeout`; it is not a theorem or a counterexample.
Blind pool growth is not warranted.

The exact atomic decision is frozen in
[`alternating_psqr_extension_or_suffix_handoff_atom.json`](alternating_psqr_extension_or_suffix_handoff_atom.json).

## Corrected exact-search boundary

The old any-desired split CEGAR pooled a promoted allocation without guarding
that its root bundle remained desired in later master models.  SAT
countermodels remained valid, but a future UNSAT result would have been
unsound.  The v2 encoding now blocks a promoted allocation only under its
symbolic desired-set condition.  A regression test fixes this distinction.
The earlier claimed `(2,1,1,1)` four-rival UNSAT core depended on that
unguarded encoding and has therefore been withdrawn rather than published.

## Retired analytic lemma and successor

Before the counterexample, the residual cap-free statement had been reduced
to the following selection theorem:

> In the low-`q` reservoir branch, either select a `p`-desired
> `D subseteq X_r+f` and a disjoint `C` whose threshold graph on
> `{x,y,C}` has a perfect matching to `{r,s,q}`, or select a disjoint
> desired/payment pair giving an anchored `s`- or `q`-handoff.

The exact profile above is the requested unrestricted counterexample to that
descent: every anchored improvement and every desired root-offer promotion
fails, although coupled off-offer improvement succeeds.

The correct successor must therefore permit an **endogenous promotion**:
the first root may receive a bundle that is unsafe relative to the base but
becomes safe after simultaneous suffix improvements.  Equivalently, the next
potential must track the vector of new owner utilities, not certify each new
bundle against the old bases independently.  The 174 unrestricted escapes in
the refuting profile are the finite anatomy set from which to extract that
coupled extension lemma.

No four-agent or general additive-EFX existence theorem is claimed here.

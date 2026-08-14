# Four-owner current-bundle compensation path-Hall theorem

**Date:** 2026-08-14

**Status:** cap-free exhaustion of every current-bundle compensation path for
a canonical whole-hit current response; the final path-Hall cut remains open

## Input

Use the canonical whole-hit response

\[
 Z_h=D\mathbin{\dot\cup}L,
 \qquad K\subseteq D,
 \qquad L\ne\varnothing,
 \qquad v_t(D)>v_t(Z_t),                         \tag{1}
\]

where `h` is the holder, `t` the current-response source, and `a,b` the two
remaining owners. The response `D` is current-safe and `L` is disjoint from
the named packet `K`.

## Every simple compensation path

Choose a simple directed path of old current bundles from `t` to `h`:

\[
 t=i_0,i_1,\ldots,i_k,h,
 \qquad (i_1,\ldots,i_k)\subseteq(a,b).          \tag{2}
\]

Give `D` to `t`; give old bundle `Z_{i_{j-1}}` to `i_j`; and give
`L+Z_{i_k}` to `h` (with `i_k=t` for the direct path). The transfer edges

\[
 h\to t\to i_1\to\cdots\to i_k\to h            \tag{3}
\]

form one supplier-closed physical cycle. Normalize other retired support in
the moved old bundles before execution; failure supplies a distinct exact
collision/release separator.

The path is weakly paid exactly when

\[
 v_{i_j}(Z_{i_{j-1}})\ge v_{i_j}(Z_{i_j})
 \quad(1\le j\le k),                             \tag{4}
\]

and

\[
 v_h(Z_{i_k})\ge v_h(D).                         \tag{5}
\]

Then `t` strictly improves and every other assigned utility is weakly
nondecreasing. Every target except `D` and `L+Z_{i_k}` is an old target.
Current safety protects `D`, so every genuinely new EFX wall is against the
new holder target. It is disjoint from `K`. Thus an admitted paid path gives
an EFX allocation preserving the strict-priority certificate, a response
avoiding `K`, a distinct normalization collision, or the already typed exact
normalization-bypass recurrence.

## Exhaustive four-owner Hall cut

There are exactly five simple paths from `t` to `h` using `a,b` at most once:

\[
 t h,\quad t a h,\quad t b h,\quad
 t a b h,\quad t b a h.                         \tag{6}
\]

If none is weakly paid, the exact survivor is the conjunction

\[
 v_h(Z_t)<v_h(D),                                \tag{7}
\]

\[
 v_a(Z_t)<v_a(Z_a)\ \text{or}\ v_h(Z_a)<v_h(D), \tag{8}
\]

\[
 v_b(Z_t)<v_b(Z_b)\ \text{or}\ v_h(Z_b)<v_h(D), \tag{9}
\]

\[
 v_a(Z_t)<v_a(Z_a)\ \text{or}\
 v_b(Z_a)<v_b(Z_b)\ \text{or}\ v_h(Z_b)<v_h(D), \tag{10}
\]

and

\[
 v_b(Z_t)<v_b(Z_b)\ \text{or}\
 v_a(Z_b)<v_a(Z_a)\ \text{or}\ v_h(Z_a)<v_h(D). \tag{11}
\]

Equations (7)--(11) are precisely the negations of the five path-payment
conditions; no valuation assumption is hidden. The retirement-supplier
three-cycle is the path `t-u-h` when `u` is one of `a,b`. This theorem also
tests the other owner and both length-three supplier cycles, so it exhausts
all compensation operations that move only whole current bundles.

## Interpretation

The remaining obstruction is no longer “the holder lacks compensation.” It
is an explicit directed path-Hall failure in the graph whose edge `i->j`
means that owner `j` weakly accepts old bundle `Z_i`, with the sink edge
`i->h` benchmarked against `D`. Any final proof must use GG champion/floor
inequalities to force one of these five paths, split an old bundle, or change
the root/anchor. Whole-current-bundle permutations alone are exhausted.

## Claim boundary

This theorem proves physical path feasibility, exact payment conditions,
new-wall localization, and exhaustive cut (7)--(11). It does not force a
path, handle arbitrary subbundle compensation, clear other retired support,
turn base-floor cores into current responses, terminate normalization bypass,
close `T_{L,times}^*`, or prove four-agent/general EFX.

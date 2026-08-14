# Retirement-supplier three-cycle or two-row cut lemma

**Date:** 2026-08-14

**Status:** cap-free supplier-provenance reduction for a canonical whole-hit
current response; the resulting two-row cut and other-retired-support
normalization remain open

## Input

Use the canonical whole-hit setting. The named packet `K` is held by `h`, a
current response `D subseteq Z_h` containing `K` is desired by source `t`,
and

\[
 Z_h=D\mathbin{\dot\cup}L,
 \qquad L\ne\varnothing,
 \qquad L\cap K=\varnothing.                    \tag{1}
\]

Let `u` be the named retirement supplier of `K`. The bilateral lemma already
handles `u in {h,t}`. Assume here that `u,h,t` are distinct, and write their
current bundles as `Z_u,Z_h,Z_t`.

## Physical supplier cycle

Test the three-owner cycle

\[
 Z'_t=D,
 \qquad Z'_u=Z_t,
 \qquad Z'_h=L\mathbin{\dot\cup}Z_u,             \tag{2}
\]

leaving the fourth owner and charity unchanged. The signed transfers are

\[
 h\longrightarrow t:D,
 \qquad t\longrightarrow u:Z_t,
 \qquad u\longrightarrow h:Z_u.                 \tag{3}
\]

Thus every moved packet has its actual current supplier inside one directed
cycle. Before execution, canonically normalize any retired support in
`Z_t+Z_u` other than the already named `K`; a failed normalization is a
separate exact collision/release separator. In the ledger-free compatible
mode, (2) is release-compatible.

The source `t` strictly improves. The other two moved owners are weakly
nonworse exactly when

\[
 v_u(Z_t)\ge v_u(Z_u),                           \tag{4}
\]

and

\[
 v_h(Z_u)\ge v_h(D).                             \tag{5}
\]

The second equivalence uses `Z_h=L+D`.

## Wall localization

Assume (4)--(5). Every owner's assigned utility weakly increases. The
response target `D` is current-safe. The target `Z_t` already existed before
the cycle, so no observer with a weakly higher assigned value can acquire a
new wall against it. Every unchanged target has the same property.

Therefore every genuinely new wall is against the sole new mixed target

\[
 L+Z_u.                                          \tag{6}
\]

It is disjoint from the named `K`. Hence exact response extraction after the
admitted cycle yields an EFX allocation preserving the strict-priority
certificate, a response avoiding `K`, a distinct retired-support collision
introduced by normalization of `Z_u`, or the already typed exact
normalization-bypass recurrence. It cannot immediately reproduce the same
whole-`K` response.

## Exact two-row survivor

If the cycle cannot weakly pay both nonresponse owners, then at least one
strict inequality holds:

\[
 v_u(Z_t)<v_u(Z_u)                               \tag{7}
\]

or

\[
 v_h(Z_u)<v_h(D).                                \tag{8}

\]

Thus the retirement supplier is no longer merely a historical label. A
canonical whole-hit current recurrence survives its natural physical
supplier cycle only by carrying an exact two-row cut: either the supplier
rejects the response source's bundle, or the holder rejects the supplier's
bundle as payment for `D`. Together with the bilateral cut
`v_h(Z_t)<v_h(D)`, this audits the two most direct cyclic compensation modes.

## Claim boundary

This lemma proves the physical cycle, exact payment tests, wall localization,
and disjunction (7)--(8). It does not force either payment inequality, clear
other retired support in `Z_t+Z_u`, terminate a repeated ledger-free response,
handle protected-floor rather than current responses, close
`T_{L,times}^*`, or prove four-agent/general EFX.

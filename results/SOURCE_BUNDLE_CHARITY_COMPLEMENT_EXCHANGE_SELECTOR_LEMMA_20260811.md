# Source-bundle charity-complement exchange selector lemma

**Date:** 2026-08-11

**Status:** cap-free exhaustion of every two-owner-plus-charity repair of the
critical top-up; third-owner compensation/source change remains open

## Exact two-owner pool

Use the recurrent critical-top-up state with paid allocation `(Y,P)`, sole
wall target owner `t`, decorated source `s`, and

\[
 D\subseteq Y_t,
 \qquad R=Y_t\setminus D,
 \qquad v_s(D)>v_s(Y_s).                           \tag{1}
\]

Rather than giving `s` the target owner's old response core, use the complete
recorded source bundle `Y_s`.  For every `J subseteq D`, define the bilateral
exchange

\[
 T(J)=R+Y_s+J,
 \qquad S_0(J)=D\setminus J.                      \tag{2}

Owner `t` receives `T(J)` and source `s` receives `S_0(J)`.  This conserves
the entire current pool `Y_t dotunion Y_s`; all other owner bundles remain
at their paid current values.

Also allow the full current charity packet.  Put

\[
 U(J)=S_0(J)\mathbin{\dot\cup}P.                  \tag{3}

For any `g in U(J)`, give

\[
 S_1(J,g)=U(J)\setminus\{g\}                     \tag{4}

to `s` and make `{g}` the final charity.  This is the most general operation
that partitions `D` between `s,t`, transfers all of `Y_s` to `t`, and uses
charity without recruiting a third owner.  The no-exchange option `S_0(J)`
is retained separately.  This structured family is useful but is not the
whole two-owner pool: a successful repair may also split `Y_s` or `R`.

Therefore put

\[
 \Omega=Y_t\mathbin{\dot\cup}Y_s\mathbin{\dot\cup}P                \tag{5}
\]

and let `mathcal A_2` contain every three-way partition

\[
 \Omega=S\mathbin{\dot\cup}T\mathbin{\dot\cup}P',
 \qquad P'\ne\varnothing,                         \tag{6}
\]

where `S` goes to `s`, `T` goes to `t`, and `P'` is charity.  Equations
(2)--(4) form a distinguished subfamily of `mathcal A_2`.

## Global selector

For each candidate `(T,S,P') in mathcal A_2`, test exactly:

1. `t` meets its priority-valid floor and every direct comparison against
   the unchanged targets, `S`, and `P'`;
2. `s` meets its priority-valid floor and every direct comparison against
   the unchanged targets, `T`, and `P'`; and
3. the fixed lexicographic prefix is preserved.

Choose a feasible candidate maximizing the fixed priority utility vector,
with a deterministic physical tie-break.  No item or value cap occurs: the
selector ranges over every physical allocation of the complete two-owner
pool.  The structured core-return and singleton-exchange candidates remain
available but are not assumed exhaustive by themselves.

Every other owner remains weakly paid.  If all external observers are safe
against `S` and `T`, the candidate is an EFX/lex endpoint.  Any external wall
is against one of these two changed targets and gives a globally minimal
ordinary/full-decorated current response, hence augmentation, current
progress, or an exact new recurrent label.  For a structured candidate the
packet graph is connected:

\[
 t\longrightarrow s:D\setminus J,
 \qquad s\longrightarrow t:Y_s,
 \qquad t\longrightarrow t:J+R,
\]

with the optional charity exchange attached to `s`.  For a general member of
`mathcal A_2`, the transfer graph has only the three vertices `{s,t,charity}`.
After isolated zero-move vertices are discarded, it has at most one
nontrivial component: two vertex-disjoint nontrivial components would require
at least four vertices.  Hence every nonidentity selected repair is connected.

## Exact failure separator

If no candidate passes the two direct-floor tests, then **every** allocation
of the complete pool `Omega` between `s,t` and nonempty charity violates a
named priority or direct EFX inequality of `s` or `t`.  This strictly
strengthens both the old-core complement selector and the structured family
(2)--(4).

At that point no packet operation confined to `Omega` can resolve the
recurrent critical top-up while keeping the other two owners
fixed.  The smallest missing operation is therefore exactly one of:

1. recruit a packet from a third owner's signed-transfer component;
2. change the decorated source/root so a different current bundle is
   released; or
3. replace the recurrent core `D`.

These are permanent component growth, adaptive source/root progress, and
response augmentation—the three remaining outcomes named by the goal.

## Verification and boundary

[`source_bundle_charity_complement_exchange_selector_audit.json`](source_bundle_charity_complement_exchange_selector_audit.json)
exhausts every three-way pool partition through six labeled goods, separately
checks the structured core/charity subfamily, and symbolically verifies the
success/failure floor trichotomy.

This lemma proves exact two-owner-plus-charity exhaustion.  It does not prove
that a candidate always succeeds, force third-owner compensation after
failure, produce a globally maximal GG countermodel, close the mixed-margin
theorem, close GG, or prove four-agent/general additive EFX.

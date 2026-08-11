# Outside-source sink-augmentation lemma

**Date:** 2026-08-10

**Status:** cap-free represented-owner growth theorem; the terminal capture
and all-owner Hall branches remain open

## General augmentation step

Let `X` be the base allocation and let `Y` be a complete allocation whose
changed owner set is `T`.  Assume every owner in `T` strictly prefers her
target `Y_i` to `X_i`, and assume the component's target labels have
pairwise-disjoint, internally supplied incoming packets.

Choose a distinguished sink `a in T`.  Suppose an owner `b notin T` is a
most-envious response source for `Y_a`, with common-safe desired subset

\[
B\subseteq Y_a,
\qquad
v_b(B)>v_b(X_b). \tag{1}

\]

Rotate that subset to the new source and return its complement together
with the new source's old bundle to the sink:

\[
Y'_b=B,
\qquad
Y'_a=X_b+(Y_a\setminus B), \tag{2}

\]

leaving every other target unchanged.  The new allocation is complete.
Owner `b` strictly improves by (1), and every old component owner other than
`a` keeps her strict improvement.

Put

\[
\gamma_a=v_a(Y_a)-v_a(X_a)>0.
\]

The sink remains strictly improved exactly when

\[
v_a(B)<v_a(X_b)+\gamma_a. \tag{3}

\]

If (3) holds, the represented owner set strictly grows from `T` to
`T union {b}`.

If it fails, nondegeneracy gives the exact strict capture wall

\[
v_a(B)>v_a(X_b)+\gamma_a. \tag{4}

\]

Thus every failed augmentation charges not only the new source's entire old
bundle but also the sink's whole accumulated improvement margin.

## Preservation of release compatibility

Write the old sink target as

\[
Y_a=(X_a\setminus O_a)+I_a,

\]

where `I_a` is its incoming set and `O_a` its released base packet.  Split
the desired subset into

\[
B_X=B\cap X_a,
\qquad
B_I=B\cap I_a.

\]

Under (2), replace the old sink label by two labels:

| target | incoming | release |
|---|---|---|
| `b` | `B_X+B_I` | `X_b` |
| `a` | `X_b+(I_a\setminus B_I)` | `O_a+B_X` |

The two new incoming sets are disjoint.  Packet `B_X` is released by the
new sink edge, `X_b` by the new-source edge, and the two cells of `I_a`
inherit the old component's internal supply.  All other labels are
unchanged.  Therefore pairwise disjointness and internal supply are
preserved.

Consequently, after any finite sequence of successful sink augmentations:

1. an EFX endpoint is a complete Pareto/lex improvement;
2. any internal response SDR is a release-compatible PI edge set;
3. an outside response source grows the represented-owner set again;
4. otherwise a minimal Hall-deficient target set is the exact remainder.

With four agents, successful outside-source growth can occur at most three
times from a one-owner root component.  The process cannot run indefinitely.

## Closure of the hardened Q-wall profile

The hardened PI-free flower adversary follows the successful sequence

\[
\{q,s\}\longrightarrow\{q,c,s\}
\longrightarrow\{q,r,c,s\}.

\]

The first new source `c` takes the ordinary subset `X_s={z}`.  The second
new source `r` takes a four-good desired subset of the enlarged `s` target.
Both sink-payment inequalities (3) hold.  The final four-owner allocation is
not EFX, but its response relation has the internal matching

\[
q\leftarrow s,
\qquad
c\leftarrow c,
\qquad
r\leftarrow r,
\qquad
s\leftarrow q.

\]

Its incoming packets are disjoint and internally supplied, so this matching
is PI.  The exact solver-free replay is
[`hardened_q_wall_sink_augmentation_pi_audit.json`](hardened_q_wall_sink_augmentation_pi_audit.json).

The abstract capture and support implications replay in
[`outside_source_sink_augmentation_audit.json`](outside_source_sink_augmentation_audit.json).

## Claim boundary

This lemma proves cap-free finite represented-owner growth and closes the
strongest frozen Q-wall adversary through a generalized PI matching.  It
does not eliminate the capture wall (4), prove that every all-owner response
relation has an SDR, eliminate the full-reservoir R-wall, close the `GG`
flower, or prove four-agent additive EFX.

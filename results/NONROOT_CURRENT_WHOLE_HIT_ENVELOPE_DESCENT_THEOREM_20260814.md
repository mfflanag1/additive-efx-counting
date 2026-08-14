# Nonroot current whole-hit envelope-descent theorem

**Date:** 2026-08-14

**Status:** verified intermediate theorem, superseded by
`NONROOT_SAFE_WHOLE_HIT_ENVELOPE_DESCENT_THEOREM_20260814.md`, which removes
the current-desire premise.

## Exact current-response input

Let `Z` be an actual canonical collision allocation carrying an earlier
first-priority root `r` which is strictly above the globally maximal base.
Let a nonroot current holder `h` own the named packet `K`, and let source
`t != h` have a globally minimum current-safe/current-desired response

\[
 K\subseteq D\subseteq Z_h,
 \qquad v_t(D)>v_t(Z_t).                         \tag{1}
\]

Put `L=Z_h-D`. The holder `h` is the designated later owner whose utility may
be sacrificed; no protected root floor is waived.

## Priority-valid whole-response sacrifice

Form the physical allocation

\[
 Z'_t=D,
 \qquad Z'_h=L,                                  \tag{2}
\]

leave every other owner target fixed, and move the released old source
bundle `Z_t` into charity. The transfer `h->t:D` uses the actual holder as
supplier, and `t` supplies `Z_t` to charity. Other retired support inside
`Z_t` is canonically normalized before execution; a failure is a separately
named collision/release separator.

The source strictly improves. The first-priority root is unchanged unless
`t=r`; in that case the safe response `D` strictly improves the root and is
a valid root-preserving current-anchor reselection after normalizing the
released old root support. Hence an EFX instance of (2) is lexicographically
above the globally maximal base even though `h` may lose.

## Exact wall localization

The target `D` is current-safe at `Z`. Every owner other than `h` keeps or
raises its assigned utility, so none of them acquires a new wall against
`D`. The holder target shrinks to `L`, and every unchanged owner target is
disjoint from `K`. The enlarged charity `P+Z_t` is also disjoint from `K`.

Consequently every response at `Z'` which meets `K` must:

1. target `D`; and
2. have source exactly the sacrificed holder `h`.

If `h` has an EFX wall against `D`, global minimum current-response
extraction gives a proper subset

\[
 E\subsetneq D.                                  \tag{3}
\]

Indeed the wall itself supplies a desired one-good deletion of `D`, so a
minimum response cannot be the whole target.

## Nested-envelope termination

If `E cap K` is empty or proper, the named hitting multiplicity becomes zero
or the collision packet strictly shrinks. If `K subseteq E`, execute the same
sacrifice with current envelope `E`. The physical holder of `K` changes from
`t` back to `h`; all goods in `D-E` remain outside the new envelope and are
never reintroduced during this nested descent.

As long as the current holder is nonroot, every repeated whole hit therefore
produces a strict chain

\[
 D=D_0\supsetneq D_1\supsetneq\cdots\supseteq K. \tag{4}
\]

The chain has length at most `|D|-|K|+1`. At its last possible envelope:

- if a response omits a good of `K`, the collision packet is proper;
- if `K` is a singleton, the target `{g}` is universally EFX-safe and cannot
  be walling; and
- if no wall meets the envelope, every remaining response is ledger-free
  relative to `K`.

Thus an infinite nonroot whole-packet ping-pong is impossible. If the
response source is the protected root, current safety and strict improvement
make the transfer a root-preserving anchor reselection, rather than another
nonroot recurrence.

## Typed consequences

- **Strict capture:** no holder payment is needed; the earlier root's strict
  certificate makes the sacrifice priority-valid.
- **Equality capture:** once a genuine current response is present, the same
  descent applies without using recipient margin.
- **Base-floor debt:** first apply the protected-floor currentization theorem.
  Its source-inactive branch remains separate; its currentized branch enters
  this theorem.
- **Release:** each executed edge uses its current physical supplier. Retired
  support in a released source bundle is normalized before movement.

## Claim boundary

This theorem eliminates the current-response whole-packet recurrence for a
sacrifice-eligible nonroot holder by a finite nested-envelope argument. It
does not eliminate a collision whose holder is already the protected root, the source-inactive
base-floor debt, another retired-support collision exposed during
normalization, close all of `T_{L,times}^*`, or prove four-agent/general EFX.

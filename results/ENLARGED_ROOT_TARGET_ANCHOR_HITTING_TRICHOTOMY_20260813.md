# Enlarged-root-target anchor-hitting trichotomy

**Date:** 2026-08-13

**Status:** cap-free localization of every response to the anchor-retaining
root target; mixed recurrence is an atomic anchor hitting set

## Enlarged target

Use the root-sourced sacrifice handoff and write its sole enlarged target as

\[
 B_r=K_r\mathbin{\dot\cup}E,                     \tag{1}

where `K_r` is the permanent old base-common-safe anchor and `E` is the
disjoint current-safe root response. Suppose `B_r` is unsafe. Among every
agent/subset pair with a subset of `B_r` desired over that agent's assigned
bundle, choose one of minimum cardinality (with deterministic tie-breaking):

\[
 D\subseteq B_r,
 \qquad v_i(D)>v_i(U_i),                          \tag{2}

where `U_i` is `i`'s assigned bundle in the sacrifice handoff. Put

\[
 D_K=D\cap K_r,
 \qquad D_E=D\cap E.                              \tag{3}

If an observer were unsafe against `D`, deleting a least-valued good in that
observer's row would give a strictly smaller desired subset, contradicting
global minimum cardinality. Thus `D` is safe relative to the handoff
allocation. Minimality also makes every good critical in source row `i`:

\[
 v_i(D-g)\le v_i(U_i)<v_i(D)\qquad(g\in D).       \tag{4}

## Exact trichotomy

Exactly one of the following holds.

### 1. Response-side core

If `D_K` is empty, then

\[
 D\subseteq E.                                    \tag{5}

This is a response entirely on the already labeled current-response support.
If its support/label is new, finite response augmentation or strict nested-
support descent applies.  If it is repeated, it is the exact residual/root-
target recurrence already recorded by the compression ledger; no anchor
good is involved.

### 2. Anchor-side core

If `D_E` is empty, then

\[
 D\subseteq K_r.                                  \tag{6}

Downward threshold safety of the old anchor makes `D` base-common-safe.  If
`v_i(U_i)>=v_i(X_i)`, equation (2) makes `D` an old desired response and the
branch is the nested old anchor edge.  If `i` is the sacrificed owner and
`v_i(U_i)<v_i(X_i)`, the strict interval

\[
 v_i(U_i)<v_i(D)\le v_i(X_i)                      \tag{7}

is exactly the source-inactive loss band.  Thus an anchor-only response is
never an unnamed mixed-payment failure.

### 3. Mixed anchor hitting set

If both `D_K` and `D_E` are nonempty, each is a proper subset of the
inclusion-minimal core. Hence neither part alone is desired:

\[
 v_i(D_K)\le v_i(U_i),
 \qquad v_i(D_E)\le v_i(U_i).                     \tag{8}

Nevertheless their union is desired, and cancellation gives the two exact
capture inequalities

\[
 v_i(D_K)>v_i(U_i)-v_i(D_E),
 \qquad
 v_i(D_E)>v_i(U_i)-v_i(D_K).                      \tag{9}

More sharply, every anchor good `g in D_K` is individually response-
critical:

\[
 v_i(g)\ge v_i(D)-v_i(U_i)>0.                    \tag{10}

Thus the mixed recurrence carries an explicit physical hitting set inside
the permanent anchor.  Removing any one of its goods destroys the selected
response.  This is the same atomic obstruction exposed by the root-facing
least-good selector, now derived from the root-target response side.

## Consequence

Every failure of the root-sourced anchor-retaining sacrifice handoff is now
routed as follows:

1. residual-target responses enter ordinary recapture/hole-pivot machinery;
2. response-side root-target cores give support descent or an exact repeated
   response label;
3. anchor-side cores give a nested old edge or source-inactive loss band; and
4. only a mixed core gives an anchor hitting-set certificate (10).

The full-pool capture inequality has disappeared from the terminal list.
The remaining global problem is to show that a repeated mixed anchor hitting
set forces a release-compatible response cycle, strict retained-support
change, or a root-preserving exchange; otherwise it is the smallest missing
operation in the GG architecture.

## Claim boundary

This lemma proves the support trichotomy, hereditary safety, old/source-
inactive split, exact capture identities, and atomic anchor criticality. It
does not terminate a repeated response-side label, reverse the mixed anchor
hitting set, terminate a source-inactive loss band, close GG, or prove four-
agent/general additive EFX.

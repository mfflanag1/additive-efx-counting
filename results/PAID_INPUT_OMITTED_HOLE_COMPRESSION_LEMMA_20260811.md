# Paid-input omitted-hole compression lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of the missing-source payment failure after
a paid four-owner splice; single-residual recapture termination remains open

## Paid all-owner input

Let `Y=(Y_i)_{i in N}` be a complete four-owner allocation obtained from a
connected splice, with

\[
 v_i(Y_i)\ge v_i(X_i)\qquad(i\in N),               \tag{1}
\]

and at least the root strictly improved. Form the common-safe response
relation of its non-EFX changed targets. Suppose the full four-target set is
an inclusion-minimal Hall defect. Its source union `S` has size three; write

\[
 d=N\setminus S.                                   \tag{2}
\]

Thus `d` is the unique missing response source.

## Omit the missing source's own target

Minimal Hall deficiency implies that every proper target subset satisfies
Hall's condition. In particular, the three targets

\[
 N\setminus\{d\}                                   \tag{3}
\]

can be matched to all three sources in `S`. For every matched source `i`,
choose its common-safe desired core `A_i` inside the matched target. Define

\[
 W=\left(\mathop{\dot\bigcup}_{j\in N}Y_j\right)
   \setminus\left(\mathop{\dot\bigcup}_{i\in S}A_i\right).              \tag{4}
\]

No selected core comes from target `Y_d`, so

\[
 Y_d\subseteq W.                                   \tag{5}
\]

Give `A_i` to source `i` and give `W` to `d`.

## Automatic residual payment

Positivity, (1), and (5) give

\[
 v_d(W)\ge v_d(Y_d)\ge v_d(X_d).                  \tag{6}
\]

Every source in `S` receives a desired core and is strictly above base.
Hence the compressed allocation pays every owner automatically. The
aggregate missing-source capture inequality from an arbitrary omitted target
cannot occur on a paid input when target `d` is omitted.

Since the three core targets are common-safe and every observer is weakly
paid, every remaining EFX wall points to `W`. Therefore exactly one of the
following occurs.

1. The compression is EFX and lexicographically improves the base.
2. The recomputed response relation has an internal SDR and is a release-
   compatible generalized PI component.
3. A represented source responds to `W`, giving the single-residual
   recapture polarity. A response by `d` itself immediately completes the
   SDR with the three fixed core edges.

## Application to the bottom-tail splice

Every successful uncompensated or compensated cycle splice pays all four
owners, with the root and hole strict. If its changed targets are not already
EFX and their response relation reaches a minimal all-owner defect, apply the
omitted-hole matching above. The proof cannot return to an unpaid residual
or invoke the aggregate capture branch; only a represented-source recapture
of the paid residual survives.

This is the precise monotonicity advantage of completing the payment layer
before recompression.

## Verification and boundary

[`paid_input_omitted_hole_compression_audit.json`](paid_input_omitted_hole_compression_audit.json)
exhausts all four-by-four inclusion-minimal full Hall defects, verifies that
every prescribed omitted target admits a three-edge matching to the source
union, and checks residual containment and payment symbolically.

This lemma does not eliminate the represented-source recapture polarity,
prove every non-EFX paid splice has a full-set minimal defect rather than a
proper defect, close later support overlap, close GG, or prove four-agent/
general additive EFX.

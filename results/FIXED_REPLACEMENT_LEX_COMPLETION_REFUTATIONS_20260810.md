# Fixed-replacement lex-completion refutations

**Date:** 2026-08-10

**Status:** two natural completion shortcuts are exactly refuted; flexible
later-owner completion remains the live `GG` target

## Refuted statements

Work in the representative full-capture flower cell with priority
`r,q,c,s`, so `q` is the later mutual-cycle owner.  The selector theorem
provides a good `g in X_q` with `v_q(f)>v_q(g)`.

The following two strengthenings are false even in the two-atom packet
model.

1. **Fixed singleton replacement.** There need not be an EFX-with-charity
   completion that fixes `X_q-g+f` as `q`'s bundle and leaves earlier owner
   `r` weakly nonworse.  The frozen witness has three eligible singleton
   goods, and the independent Boolean allocation encoding is UNSAT for all
   three fixed bundles.
2. **Fixed maximal-packet replacement.** Enlarging `g` to an
   inclusion-maximal packet `S subset X_q` satisfying `v_q(S)<v_q(f)` does
   not repair the statement.  A second witness has a unique such maximal
   packet, and its fixed-bundle completion problem is UNSAT.

Both witnesses satisfy positivity, the flower desired-bundle conditions,
base EFX with charity, and simultaneous failure of the nine relevant
common-safe covers.  Both refutations replay under Z3 5.0.0 and 4.15.3 with
a Boolean one-hot allocation encoding distinct from the integer-owner CEGAR
encoding.

## Structural lesson

The selected owner's bundle cannot remain frozen while its dependency is
grown.  This is not evidence against the flower closure itself.  Each frozen
countermodel has a two-good EFX lex escape that fixes `r` and strictly
improves `q`: a good of `X_q` is exchanged with a good of the arm owner's
bundle.  Thus the failure is exactly rigidity of the distinguished bundle,
not absence of a lex-improving endpoint.

The corrected bounded decision target is:

> In every hard flower cell with `r` before `q`, there is some EFX-with-
> charity allocation `Y` with `v_r(Y_r)>=v_r(X_r)` and
> `v_q(Y_q)>v_q(X_q)`, while `Y_q` is allowed to evolve.  The reverse
> priority orientation is symmetric.

An arbitrary-packet proof should express the evolving bundle through an
adaptive transfer component or a released-good exchange with the arm owner,
not through a fixed packet-for-charity endpoint.  The current CEGAR for this
flexible target is proof mining only and is not yet a theorem.

The previously frozen arm-response profile supplies one additional routing
fact. Its two singleton replacements have only target dependencies; every
most-envious response into the changed `q` bundle from `r` or `s` is genuine
and uses `f`. Responses into leaf `r` or `c` are likewise genuine, while the
response into singleton leaf `s` is ordinary because its source already
envies `{z}`. This is an exact profile census, not a universal source theorem.

## Artifacts and claim boundary

- `fixed_replacement_lex_completion_refutation.json`
- `maximal_packet_replacement_lex_completion_refutation.json`
- `fixed_replacement_lex_completion_refutation_audit.json`
- `tracks/parkability/audit_fixed_replacement_lex_completion_refutation.py`

These artifacts refute two proposed selectors.  They do not close `GG`, do
not refute EFX existence, and do not establish the flexible completion
statement.

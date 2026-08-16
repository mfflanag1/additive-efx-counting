# Priority/novelty sweep — 2026-08-16

Two independent web sweeps (goods cell, chores cell), run before restarting frontier work.
Verified firsthand: arXiv:2608.08590 abstract fetched and matches the sweep's reading.

## Goods: (4,8) SCOOPED — retire as standalone

**arXiv:2608.08590** (v1, submitted 2026-08-09): Alkassar, Fouz, Mehlhorn — "Complete EFX
Allocations Exist for Four Additive Agents and Up to Nine Goods." Proves complete **EFX0**
for 4 additive agents, m <= 9, nonnegative reals. Strictly dominates our efx48 theorem on
both axes (m <= 9 vs m = 8; EFX0 vs EFX+/positive). Method: hand reduction lemmas (56/165
branch families) + Z3/cvc5 QF_LRA certificate corpus; disclosed as AI-led (Claude Fable /
Claude Code / Opus 4.8 / ChatGPT 5.5Pro, six audit rounds). Their §8 "Theorem 2 (m=8,
independent)" credits "an earlier independent project" — textual evidence (same approach,
their own Drive archive) says it is their OWN earlier run, not ours; our repo is not cited;
moderate confidence, one email to Mehlhorn would settle it. Our efx48-hybrid-proof release
(2026-07-30, v1.0.1) predates their arXiv post by 10 days but has zero visibility.

Salvage: (a) keep efx48-hybrid-proof as a dated artifact; (b) optional short note positioning
it as independent concurrent verification of their Theorem 2 (their m=8 certificates are
unrefereed in a Drive folder; our independently built Lean-hybrid corroboration has value);
(c) decision + any outreach to Mehlhorn is Max's call.

**Four-agent GENERAL additive EFX: open and uncontested.** Nobody visible on the BCFF
one-charity / global-lex route. Alkassar et al. explicitly argue their certificate method
does not scale to the general theorem (decomposition "does not suffice"; obstruction
localized at near-identical valuations, ~0.14% EFX0 density, incompatible mandatory
structure within one region). That published hardness phenomenon is exactly what the
structural lex-maximal program targets. Program weight moves here.

Corrections to internal notes: Akrami et al. 2604.18216 is at v3 (2026-05-14), stated for
MONOTONE valuations n>=3, m>=n+5 (submodular a corollary). Mackenzie-Suzuki 2605.06451
still v1. Cite 2607.27455 (R(d) < ed) for the rainbow-cycle closure.

## Chores: tri-valued m <= 11 theorem STILL NOVEL — GO

No collision found. He-Tao 2606.08872 still v2 (two citations, both 2026-08-11, both
non-colliding). CORRECTION (2026-08-16, caught during paper drafting): Hosseini-Khurana-
Pathak-Vaish 2608.10397 does NOT state the 3-agent cell is open — its abstract gives
approximation schemes (goods; 3-agent chores) and submodular impossibilities, plus
EFX∨MMS for two-type additive chores. Cite it as concurrent Aug-2026 activity on the cell;
the explicit openness statement is He-Tao §6, verified verbatim: "It is open whether an
EFX allocation always exists for three agents." Nearest-sounding rival Lin-Wu-Zhou "restricted additive"
(2603.17270) is a different model (c_i(e) in {0, c(e)}), no overlap.

FRAMING LAW for the writeup: KMS m <= 2n already covers m <= 6 at n=3, and n=3
personalized bi-valued is settled for all m. The genuine increment is m in {7..11} under
the common tri-valued class — frame as "first crossing of the 2n barrier at n=3 for a
genuinely three-valued cost class," never as the whole m <= 11 range being new.

Race heat: Tao posted 3x in Aug 2026 but moving away from this cell (non-additive, MMS).
Watch Akrami et al. 2608.08864 (cancelable-valuations EFX repair, 2026-08-09) — nearest
usable tool for an existence conversion. EC 2026 and SAGT 2026 accepted lists: clean.

Must-cite list for the chores paper: KMS 2305.04168; He-Tao 2606.08872; Hosseini et al.
2608.10397; Lin-Wu-Zhou 2603.17270 (spell out the definitional difference); Lin-Liu-Tao-
Zhou 2608.10572 (binary marginals, non-additive, 18x53 counterexample); Christoforidis
2605.21448 (3 agents 6 chores subadditive, no alpha-EFX below 2^(1/3)); Garg-Murhekar
2-EFX chores AAAI 2026; Akrami et al. 2608.08864; Aziz-Lindsay-Ritossa-Suzuki two chore
types.

## Shared blind spot

**WINE 2026** (submissions closed 2026-07-02, notifications ~late Sept/Oct, conference
Dec 1-4 HKU): a rival submission on either cell would be invisible until the accepted list
drops. RECHECK BOTH CELLS when it publishes. Also unchecked: ESA/FOCS 2026 lists,
IJCAI 2026 (dynamic page, negative not trusted), Google Scholar, private circulation.

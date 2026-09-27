## Verdict: findings

The audit does not promote anything to universal EFX, and its admission-gap and A0 joint-selection framing match the brief. The corrections below are narrower but consequential.

## Findings

**1. Medium-high: split claim conflicts with the controlling theorem (audit L47, L68–70).**
- Evidence: the audit says the cell defeats four-edge allocations "including its permitted splits" and that "increasing split freedom did not repair the cap." Theorem doc §4′ (L118–123) says the pinned physical residual closes "at four edges with a single split role."
- The only split-proof residuals in the packet are the twelve-atom ones (Theorem C), which are unit packets, not a physical packet cell.
- Correction: name the exact cell and master, and state that the §4′ whole-role residual does close with one split.
- Verification: reconcile against the F4 boundary document. The audit cites 712a40e, while the brief pins eb7f144 and the master at 5d13f17; neither F4 source is in the packet.

**2. Medium: the admission gap is understated (L96–98).**
- Evidence: "not all derived or encoded" implies some of P10–P15 are encoded. Ledger L33–38 and theorem L129–130 say none is; only parts of P13 (a, b, e) are derived or verified, and (d) is inserted.
- Correction: "none encoded; P13 partly derived; the rest assumed or inserted."
- Also name the underived modelling restrictions: the `v<16` value box (P2), the fixed support state (P4) and the chosen root-facing branch (P7).

**3. Medium: missing hypotheses in next step 4 (L172–175).**
- Evidence: the text implies admission, closure, pullback and termination would give four-agent existence. ADMIT4 is frozen under nondegeneracy and a fixed priority order (brief L13), and the brief requires "tie/zero wrappers" (L67).
- Correction: add both.

**4. Medium: archived evidence reads as current (L42–45, L110–112).**
- Evidence: "three implementations enumerate," "independent replay" and "a full retained proof replay" carry no date or run provenance.
- Correction: mark each as archived or re-run this round, as the audit already does for hashes (L121).
- Verification: check against today's logs.

**5. Low-medium: F4 tallies are unsupported and ambiguous (L90–91).**
- Evidence: the 408/405/1/2 figures appear in neither controlling document. The theorem doc records 517 models, two atom residuals and one physical residual.
- Correction: say under which cap the 405 are "closed" and that closure is witness-level (Proposition B, §4 item 3), not a universal certificate.

**6. Low: "repairs" overstates (L46).**
- Evidence: "repairs the conditional exclusion argument" sits beside "candidate… still need external review."
- Correction: use "proposes a repair." The nice-cancelable extension should stay explicitly conditional; its source is not in the packet.

**7. Low: citation check (L75).**
- Evidence: identifier 2609.10585 looks high for a 6 September submission.
- Verification: confirm the identifier and date against arXiv.

## Scope limitations

- I reviewed only the four supplied files and ran nothing.
- Not in the packet: the F4 handoff, the a8e925e consolidation, the BCFF audit, VERIFICATION.md, and all counting and chores artefacts. Claims resting on them are unverified here.
- External arXiv claims were not checked.
- No mathematical claim was re-derived.

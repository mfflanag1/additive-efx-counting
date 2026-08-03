# Published-input audit for the additive EFX \((4,8)\) proof

**Status:** passed on 2026-07-29  
**Machine-readable record:** `literature/PUBLISHED_INPUT_AUDIT.json` in the
frozen certification directory  
**Important limitation:** this audit verifies the theorem statements and
their specialization to the Lean interfaces. It does not formalize the
papers' proofs.

## Lean boundary

The published inputs enter through the positive terminal theorem:

```lean
theorem admitsEFX_4x8_of_standard_published_inputs
    (four_agent_seven_good :
      FourAgentSevenGoodStandardInput)
    (three_agent_seven_good :
      ThreeAgentSevenGoodStandardInput)
    (terminal_cells_unsat : EightTerminalCellsUnsat)
    (weight : Weight48)
    (positive : ∀ agent good, 0 < weight agent good) :
    AdmitsEFX weight
```

The current exported theorem
`admitsEFX_4x8_of_standard_published_inputs_nonnegative` first converts a
hypothetical nonnegative counterexample to a positive one, then invokes this
interface. The published-input variants themselves are unchanged.

The associated lifting module proves that the two standard literature
statements imply the deleted-good hypotheses actually used by the residual
cuts.

## Four agents and seven goods

Pinned source:

- Ryoga Mahara, *Extension of Additive Valuations to General Valuations on
  the Existence of EFX*, arXiv:2107.09901v2.
- PDF:
  <https://arxiv.org/pdf/2107.09901v2>
- SHA-256:
  `69d25460d0711e6156d20632292247c51fc50188a799ef5afa407bf983a1dd23`

Theorem 3 states that general valuations admit a **complete** EFX allocation
when \(m\le n+3\). The paper defines a complete allocation as a partition of
all goods and defines EFX using removal of any good from the target bundle.

The local specialization has \(n=4\) and \(m=7\), so
\(7\le4+3\). Strictly positive additive valuations are normalized at the
empty set, monotone, and nonnegative, hence are a subclass of the paper's
general valuations.

This supplies `FourAgentSevenGoodStandardInput`.

## Three agents and seven goods

Pinned source:

- Bhaskar Ray Chaudhury, Jugal Garg, and Kurt Mehlhorn, *EFX Exists for
  Three Agents*, arXiv:2002.05119v3.
- PDF:
  <https://arxiv.org/pdf/2002.05119v3>
- SHA-256:
  `a4fc17c93ea60f6b1b2d5e4f7651f0c9c463e27bc805fc1bda1c638494340bd3`

Theorem 20 states that every three-agent additive instance admits an EFX
allocation. Its proof explicitly terminates at a **complete** EFX allocation,
and the paper's definition uses removal of any good from the target bundle.
The theorem permits any finite number of goods, so seven goods is a direct
specialization. Strict positivity is a restriction of the paper's
nonnegative additive domain.

This supplies `ThreeAgentSevenGoodStandardInput`.

## Convention comparison

| Issue | Paper statements | Lean proof |
|---|---|---|
| All goods allocated | Complete partition | `ValidAllocation`: every good has exactly one owner |
| Fairness quantifier | Any good in the target bundle | Any good in the target bundle |
| Additivity | Explicit in the three-agent theorem | Bundle value is the sum of item weights |
| Signs | Nonnegative/general monotone | Strictly positive, hence within scope |
| Empty self-comparison | Papers may quantify all agent pairs | Lean omits equal pairs; self-comparisons follow from nonnegativity |
| Goods in smaller instances | Seven | Subtypes excluding one of eight goods |
| Deleted-agent instance | Three active agents | Lifted to four slots with the deleted observer excluded |

There is no EFX-versus-EFX-with-charity mismatch and no EF1-versus-EFX
mismatch.

## Automated check

`tracks/parkability/audit_published_inputs.py`:

1. checks both exact PDF hashes;
2. extracts their text with `pdftotext`;
3. locates the theorem, completeness, and EFX-definition statements;
4. records the specialization to the two Lean input propositions; and
5. hash-binds the Lean definition and lifting files.

The current machine-readable audit has
`"all_passed": true`. Its explicit trust flag
`"paper_theorems_formalized_in_lean": false` prevents the source-statement
check from being mistaken for a formalization of the published proofs.

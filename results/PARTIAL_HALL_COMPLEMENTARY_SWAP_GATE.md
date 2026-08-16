# Complementary-swap eligibility-wall gate

## Current verdict

**Seven- and eight-rival versions refuted; nine-rival version open.** Exact
positive rational models refute the first two conversion menus. Adding the
best distance-five repair from the eight-rival counterexample closes that
comparison cell, but the global nine-rival gate ended `UNKNOWN (TIMEOUT)` after
120 seconds. No global UNSAT theorem has been obtained.

## Candidate conversion

In the canonical partial allocation, exchange goods 6 and 0 or exchange goods
7 and 4 between bundles 0 and 2. When the sum of those two normalized-potential
changes is positive, test the two swaps and six short repairs mined from the
positive-sum eligibility failures in the 134-profile Hall-obstruction corpus.

The exact gate is:

\[
\begin{split}
&v_0(0)+v_0(4)-v_0(6)-v_0(7)\\
&\quad+v_2(6)+v_2(7)-v_2(0)-v_2(4)>0,
\end{split}
\]

together with the canonical EFX and floater-nonenvy premises, failure of all 91
radius-one Hall completions, and failure of the seven listed rivals to be both
eligible and improving.

[`partial_hall_complementary_swap_gate.json`](partial_hall_complementary_swap_gate.json)
preserves the inconclusive seven-rival solver run, while the exact rational
corpus audit identifies its counterexample with valuation hash
`023d18621bee45b13f735868575ef4404ea30c8e97f4b0f8cec36a0eb7fb13f9`.
The eight-rival run is
[`partial_hall_complementary_swap_gate8.json`](partial_hall_complementary_swap_gate8.json).
Its SMT-LIB formula has SHA-256
`5a5866c2cbc9960ef232ed93797ed1cd6d55e005baddad75da42609771a469a1`.
Its exact refutation and independent integer audit are
[`partial_hall_complementary_swap_gate8_counterexample.json`](partial_hall_complementary_swap_gate8_counterexample.json)
and
[`partial_hall_complementary_swap_gate8_counterexample_audit.json`](partial_hall_complementary_swap_gate8_counterexample_audit.json).
The counterexample has positive swap sum (1/2372), blocks all eight rivals,
and still has 25 eligible improving radius-five states. The nine-rival global
formula is recorded in
[`partial_hall_complementary_swap_gate9.json`](partial_hall_complementary_swap_gate9.json)
with SMT-LIB SHA-256
`ba48cc244e829aa077328bbce22f48f84f4f7e0d8a8afc231f76b1c1d5b8ee1d`.

## Evidence motivating the gate

The two complementary swaps cover 67 of 134 stored Hall obstructions. Eight
profiles have positive summed swap gain but neither swap is eligible and
improving. Exact nearest-repair extraction finds short repairs, including both
orientations of the third pairing of goods \(\{0,4,6,7\}\). The original five
repairs cover seven of these profiles; the opposite third pairing covers the
eighth. Thus:

- the seven-rival menu is exactly false on one stored obstruction; and
- the eight-rival menu covers all 26 stored profiles with positive summed gain.

Every failed swap in this eight-profile subcorpus violates EFX; floater nonenvy
usually survives. This localizes the missing proof to an EFX-wall conversion,
consistent with the transfer-component dependency-cycle lemma.

## Related exact cell

The cumulative 15-rival menu does not close the designated trap cell
`partition=90, deficient pair=(0,1)`: after the earlier 60-second Z3 and
120-second cvc5 timeouts, a 300-second Z3 run found an exact SAT model in
109.44 seconds. Thus that finite menu is refuted. The model has 127 improving
radius-five rivals.

Freezing the SAT model's complete eligibility/Hall comparison cell and adding
the eighth opposite-third-pairing rival closes `UNSAT`. Its nine-constraint
core yields the cap-free
[opposite-third-pairing conversion lemma](PARTIAL_HALL_OPPOSITE_THIRD_PAIRING_LEMMA.md).
This eliminates one full comparison cell, not the global eight-rival gate.

## Claim boundary

The seven-rival, eight-rival, and cumulative 15-rival menus are false. The
nine-rival gate is still open despite the newly excluded comparison cells. The fixed
canonical radius-five improvement theorem, the Hall one-good completion lemma,
four-agent complete EFX, and general additive EFX all remain open.

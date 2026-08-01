# Preliminary Novelty Audit: Nonnegative Additive EFX at \((4,8)\)

**Search dates:** 2026-07-29 and refreshed 2026-07-30 EDT  
**Status:** expanded primary-literature search, not a definitive systematic
review or expert confirmation

## Question

Has complete EFX existence already been proved for every nonnegative
additive instance with four agents and eight goods?

## Search performed

Targeted searches covered combinations of:

- “additive EFX four agents eight goods”;
- “complete EFX four agents additive” with 2024--2026 dates;
- “EFX \(m=n+4\) additive valuations”;
- “EFX 4 agents and 8 goods”; and
- current arXiv records on exact, approximate, partial, and counterexample
  results.

The refresh additionally searched 2025--2026 arXiv records and official
AAAI proceedings for four-agent EFX, \(m=n+4\), bounded numbers of goods,
restricted valuation types, hypergraph valuations, and papers citing or
restating the \(m\le n+3\) frontier. Technical conclusions below use primary
papers or official publication pages.

## Closest located results

1. **Mahara, \(m\le n+3\).**  
   [Extension of Additive Valuations to General Valuations on the Existence
   of EFX](https://arxiv.org/abs/2107.09901) proves complete EFX for general
   valuations when the number of goods is at most \(n+3\). At four agents
   this reaches seven goods, not eight.

2. **Chaudhury--Garg--Mehlhorn, three additive agents.**  
   [EFX Exists for Three Agents](https://arxiv.org/abs/2002.05119) covers
   arbitrary finite numbers of goods for three additive agents. It supplies
   one residual input to the present proof but does not cover four agents.

3. **Berger--Cohen--Feldman--Fiat, almost-full four-agent EFX.**  
   [(Almost Full) EFX Exists for Four Agents (and
   Beyond)](https://arxiv.org/abs/2102.10654) proves that four additive
   agents admit an EFX allocation leaving at most one good unallocated. It
   does not prove completeness at eight goods.

4. **Ashuri--Gkatzelis--Sgouritsa, EF2X for four agents.**  
   [EF2X Exists for Four Agents](https://arxiv.org/abs/2412.00254) gives a
   relaxation in which any two goods may be removed. Its abstract explicitly
   describes four-agent additive EFX existence as open.

5. **Akrami--Mayorov--Mehlhorn--Srinivas--Weidenbach, monotone
   counterexamples.**  
   The current v3 of
   [A Counterexample to EFX: \(n\ge3\) Agents, \(m\ge n+5\) Items,
   Submodular Valuations via SAT-Solving](https://arxiv.org/abs/2604.18216)
   gives nonadditive monotone, hence submodular, counterexamples from the
   \(n+5\) frontier and formally verifies its SAT foundations in Lean. It
   also proves EFX existence for three agents and seven goods under monotone
   valuations. That \(m=n+4\) result is direct precedent for certified
   finite search. It does not provide an additive counterexample and does
   not cover the four-agent cell \((4,8)\).

6. **Recent restricted-valuation and approximation results.**  
   Searches located results for graphical/multigraph valuations, few
   valuation types, approximate EFX, epistemic EFX, and EFX with charity.
   None of the located papers states complete EFX for unrestricted positive
   additive \(4\times8\) instances.

7. **Neoh--Teh counting paper, 2025.**  
   [Understanding EFX Allocations: Counting and
   Variants](https://ojs.aaai.org/index.php/AAAI/article/view/33536)
   states in its few-goods discussion that EFX existence was known only for
   \(m\le n+3\). Its Theorem 3.4 also shows why a growing near-diagonal
   existence range would imply the general conjecture. It gives counting
   results through \(m=n+2\), not an \(m=n+4\) existence theorem.

8. **Brânzei local search, October 2025.**  
   [Computing EFX Allocations via Local
   Search](https://arxiv.org/abs/2510.05429) describes additive EFX
   existence as a major open question and reports broad empirical success.
   Its exact theorem is for identical additive valuations; it does not
   establish unrestricted four-agent existence.

9. **AAAI 2026 restricted classes.**  
   [EFX Allocation in
   (Multi)Hypergraphs](https://ojs.aaai.org/index.php/AAAI/article/view/38759)
   and [EFX and PO Allocation Exists for Two Types of
   Goods](https://ojs.aaai.org/index.php/AAAI/article/view/38723) both frame
   unrestricted additive EFX as open and prove results for structured
   subclasses. Neither covers arbitrary positive \(4\times8\) matrices.

## Preliminary conclusion

No prior theorem for unrestricted nonnegative additive \((4,8)\) was located in
either search. The 2025 counting paper's explicit \(m\le n+3\) frontier and
the 2025--2026 papers continuing to call four-agent or general additive EFX
open strengthen the evidence that this result is novel. It would occupy a
clean boundary:

\[
\text{general monotone existence through }m=n+3
\quad\longrightarrow\quad
\boxed{\text{additive }(4,8)}
\quad\longrightarrow\quad
\text{nonadditive failure from }m=n+5.
\]

This is strong documentary evidence, not a proof of novelty. Search indexes
can miss recent preprints, differently worded results, unpublished
manuscripts, theses, and work in progress.

## Required confirmation before a public novelty claim

1. Complete citation chaining in Google Scholar, DBLP, and Semantic Scholar
   from Mahara, Berger et al., the Neoh--Teh counting paper, and the 2026
   counterexample paper. The current search covered direct search results and
   primary papers but not a signed-off exhaustive citation graph.
2. Ask at least two active EFX researchers whether \((4,8)\) is known,
   folklore, or in concurrent work.
3. Use the narrow claim “first previously open four-agent additive cell
   beyond \(n+3\).” Do not claim the first \(m=n+4\) theorem or
   methodological priority.
4. Date-stamp and archive the final bibliography used in the paper.

Until those checks are complete, the appropriate language is:

> **Apparently new in an expanded primary-literature search; novelty not
> independently confirmed by field experts.**

# Designated pair-trap theorem for the canonical cell

## Theorem

Fix four agents, nine goods, the positive-additive partial allocation

\[
X=(\{6,7\},\{1,2,3\},\{0,4\},\{5\}),\qquad f=8.
\]

Assume $X$ is EFX, $v_i(X_i)\ge v_i(f)$ for every agent, and none of the 91
partitions obtained by assigning $f$ and moving at most one old good has an
EFX perfect matching.

Then one of 17 explicit star moves has a pair of agents whose sole acceptable
bundle is its designated bundle. The moves are:

- put $f$ in bundle 0 and move one of $\{3,0,4\}$ into bundle 0;
- put $f$ in bundle 1 and move one of $\{6,7,0,4\}$ into bundle 1;
- put $f$ in bundle 2 and move one of $\{6,7,1,2,3\}$ into bundle 2;
- put $f$ in bundle 3 and move one of $\{6,7\}$ into bundle 3; or
- put $f$ in bundle 3, move good 5 to bundle 0, 1, or 2, and designate that
  destination.

For an incoming-good move the designated bundle is the enlarged floater host.
For an evacuated-singleton move it is the destination receiving good 5.

## Exact verification

The theorem is the UNSAT result obtained after forbidding all $17\times6=102$
designated agent-pair traps while retaining exact base eligibility and all 91
Hall obstructions:

- Z3 formula:
  [`partial_hall_designated_pair_trap.smt2`](partial_hall_designated_pair_trap.smt2),
  SHA-256
  `688bba7b3aa76a00c1e315018a707f03465e0e9040b094ff1c21c84c57ce8106`,
  UNSAT in 11.45 seconds;
- syntax-normalized cvc5 formula:
  [`partial_hall_designated_pair_trap.cvc5.smt2`](partial_hall_designated_pair_trap.cvc5.smt2),
  SHA-256
  `3900b02820f0c6fbfcc38e3a6384504d5c1f73b0cff372311de9ec56113dc554`,
  independently UNSAT under cvc5 1.3.4 in 18.27 seconds.

The complete move ledger is
[`partial_hall_designated_pair_trap.json`](partial_hall_designated_pair_trap.json).

## Immediate analytic corollary

Each trapped agent uniquely ranks the designated bundle first by whole-bundle
value. Indeed, a maximum-valued bundle is always EFX-acceptable by the
[maximum-bundle neighbor lemma](PARTIAL_HALL_NONEMPTY_NEIGHBOR_LEMMA.md). If a
different bundle tied for maximum, it too would be acceptable, contradicting
that the designated bundle is the agent's sole neighbor.

Thus every fixed-cell obstruction contains a star move creating a common
strict favorite for two agents. This converts the original 91 matching
failures into one explicit two-agent preference collision.

## Claim boundary

This is cap-free in valuation magnitudes but fixed to the canonical
$2+3+2+1$ shape and nine goods. It does not yet prove completion: the remaining
conversion must show that the common strict-favorite collision yields either
an EFX matching in another move or an eligible higher-potential exchange.

# Three-target external-source fork edge-cancellation frontier

**Date:** 2026-08-14

**Status:** exact cap-free signed-support census for the remaining `3x2`
external-source Hall fork; valuation feasibility remains open

## Canonical fork

Use one of the two exact selected rank-three matching forms

\[
\begin{aligned}
R_2&:\ r\to q,\ q\to r,\ s\to d,\\
R_3&:\ r\to q,\ q\to s,\ s\to r.
\end{aligned}                                      \tag{1}
\]

After reversing (1), each current target bundle `B_j` consists of retained
support originally supplied by `j`, plus at most one incoming matching packet
from its original supplier.

The external `3x2` Hall defect has target owners `{y,t,v}`, sources `{x,y}`,
and outside owner `x`.  Minimality forces the path responses

\[
 x\longrightarrow y,
 \qquad y\longrightarrow t,                       \tag{2}
\]

where arrows are response source to physical target.  Reverse (2), keep
target `v` unchanged, and give the charity singleton to the sacrificed leaf
`t`.  The physical transfer path is

\[
 charity\longrightarrow t\longrightarrow y\longrightarrow x. \tag{3}
\]

Each response core may use retained support, none/a proper part/all of the
target's incoming matching packet, or both.

## Edge-cancellation identity

Let `E_0` be the three original supplier-recipient pairs created by the
matching reversal, and let `E_1` be the owner-supplier pairs remaining after
the two response transfers in (3), measured relative to the original
saturated allocation.  Put

\[
 A=E_1\setminus E_0,
 \qquad D=E_0\setminus E_1.                        \tag{4}
\]

Because `|E_0|=3`, adding the charity edge gives

\[
 |E_{final}|=4+|A|-|D|.                            \tag{5}

Therefore the fork respects the four-edge bound exactly when

\[
                         |A|\le |D|.               \tag{6}

New pairs in `A` arise from retained-support imports, proper incoming-packet
splits, or redirection to a recipient not already used by that supplier.
Pairs enter `D` only when a whole old supplier-destination cell is exhausted
or a response returns goods to their original supplier.  Thus every extra
branch of the fork must be paid for by an exact signed edge cancellation;
packet cardinality creates no additional case.

## Exhaustive cap-free support census

For each form in (1), the exact audit enumerates:

- all 24 assignments of the distinct roles `(x,y,t,v)`;
- presence/absence of retained support in each response;
- none/proper/all use of each available incoming matching packet; and
- the final original-supplier destination set, including coincident and
  returned edges.

There are 720 nonempty response-support patterns.  Exactly 156 satisfy (6):
78 in `R_2` and 78 in `R_3`.  The exact final edge distribution is

| edges | patterns |
|---:|---:|
| 2 | 3 |
| 3 | 25 |
| 4 | 128 |
| 5 | 282 |
| 6 | 225 |
| 7 | 53 |
| 8 | 4 |

Thus 564 of 720 fork patterns are provably outside the requested edge bound,
before any valuation inequality is considered.  Eighteen `R_2` role
assignments and fifteen `R_3` role assignments admit at least one feasible
support pattern; the others cannot be repaired by this fork at all.

## Remaining exact decision

The universal theorem is now reduced to a finite signed-support disjunction:
for the `2x1` star use the explicit return/redirection theorem, and for the
`3x2` fork use one of the 156 edge-cancelling patterns in this census.  The
next full-premise solver should quantify physical values and response cores
only over those patterns, while retaining global lex maximality, PI-freeness,
all saturation exclusions, and exact observer safety.  SAT outside the
feasible patterns is irrelevant because it cannot meet the four-edge
conclusion.

## Boundary

This theorem proves the complete signed-support/edge-count classification of
the two exact matching forms.  It does not show that any feasible pattern has
the required desired/safety inequalities, that one endpoint is EFX, that the
564 overflowing patterns activate support progress, prove fixed-`U`, or prove
four-agent/general additive EFX.

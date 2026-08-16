# Owner-Threshold Pair-Degree Encoding

**Status:** exact analytic equivalence  
**Scope:** one observer, eight residual goods, favorite value \(F\)  
**Purpose:** sorting-free form of universal owner-threshold failure

Let the residual values be \(x_1\ge\cdots\ge x_8\). Universal failure of
the favorite-singleton owner threshold is already known to be equivalent to

\[
x_5+x_6+x_7>F
\quad\text{and}\quad
\bigl(x_3+x_7>F\ \text{or}\ x_4+x_5>F\bigr).
\tag{1}
\]

This note removes the sorting network from (1).

## Four-set form of the tail inequality

The inequality \(x_5+x_6+x_7>F\) holds if and only if every four residual
goods contain a three-good subset worth more than \(F\).

Indeed, among a fixed four-set the most valuable triple is obtained by
deleting its least-valued good. The minimum, over all four-sets, of this
maximum triple value is attained by the bottom four goods and equals
\(x_5+x_6+x_7\).

## Pair-degree form of the disjunction

Form a graph on the eight residual goods, joining \(g\) and \(h\) exactly
when

\[
v(g)+v(h)>F.
\tag{2}
\]

Ordering vertices by nonincreasing value also orders their degrees
nonincreasingly. For the third-ranked good, the sixth most valuable other
good is \(x_7\). Hence

\[
x_3+x_7>F
\quad\Longleftrightarrow\quad
\text{at least three vertices have degree at least six}.
\tag{3}
\]

For the fourth-ranked good, the fourth most valuable other good is \(x_5\).
Thus

\[
x_4+x_5>F
\quad\Longleftrightarrow\quad
\text{at least four vertices have degree at least four}.
\tag{4}
\]

These equivalences remain valid with tied residual values: equal-valued
vertices have the same adjacency relation to every third vertex, and their
mutual edge is symmetric.

Combining the two parts gives the sorting-free characterization:

> Every four residual goods contain a triple worth more than \(F\), and in
> the pair-sum graph (2), either at least three vertices have degree at least
> six or at least four vertices have degree at least four.

The QF_LRA encoding uses 70 four-set clauses and 28 pair-edge predicates per
row. The executable audit
[efx49_owner_threshold_pair_degree_encoding_audit.json](efx49_owner_threshold_pair_degree_encoding_audit.json)
compares this form with (1) on all 495 residual multisets over
\(\{0,1,2,3,4\}\) and all audited favorite thresholds, for 2,695 exact
equivalence checks. It is a regression test, not a substitute for the proof.

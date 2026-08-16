# Owner-Threshold Shape Envelope

**Status:** exact analytic characterization  
**Scope:** one additive observer, eight residual goods, three residual bundles  
**Not claimed:** that the resident agents admit an EFX matching on the chosen
partition

Let \(f\) be a favorite good of an agent \(a\), write
\(F=v_a(f)\), and sort the values of the other eight goods as

\[
x_1\ge x_2\ge\cdots\ge x_8\ge0.
\]

For a three-bundle partition \(\mathcal P\), define the owner's completion
threshold

\[
\tau_a(\mathcal P)=
\max_{B\in\mathcal P}\left(v_a(B)-\min_{g\in B}v_a(g)\right).
\]

## Exact \(3+3+2\) envelope

Among all residual partitions of shape \(3+3+2\),

\[
\min_{\mathcal P:\,\operatorname{shape}(\mathcal P)=3+3+2}
\tau_a(\mathcal P)
=
\max\{x_1,\ x_3+x_7,\ x_4+x_5\}.
\tag{1}
\]

The partition

\[
\{x_1,x_2\}\mid
\{x_3,x_7,x_8\}\mid
\{x_4,x_5,x_6\}
\tag{2}
\]
attains the right-hand side.

For the lower bound, every \(3+3+2\) partition has threshold at least
\(x_1\), because the bundle containing \(x_1\) retains it after its least
good is removed. Among the five goods \(x_1,\ldots,x_5\), some triple must
contain at least two, so its retained pair is worth at least \(x_4+x_5\).
Finally, if the pair bundle does not contain both \(x_1,x_2\), a triple
contains one of them and at least one of \(x_3,\ldots,x_7\), giving threshold
at least \(x_3+x_7\). If the pair does contain both, the triple containing
\(x_3\) also contains at least one of \(x_4,\ldots,x_7\), giving the same
bound. This proves (1).

## Exact \(4+2+2\) envelope

Among all residual partitions of shape \(4+2+2\),

\[
\min_{\mathcal P:\,\operatorname{shape}(\mathcal P)=4+2+2}
\tau_a(\mathcal P)
=
\max\{x_1,\ x_5+x_6+x_7\}.
\tag{3}
\]

The partition

\[
\{x_1,x_2\}\mid
\{x_3,x_4\}\mid
\{x_5,x_6,x_7,x_8\}
\tag{4}
\]
attains this value. Every partition has threshold at least \(x_1\). Its
four-good bundle retains its three largest members after its minimum is
removed; among all four-subsets, the least possible value of those three
members is \(x_5+x_6+x_7\). This proves the reverse inequality and hence
(3).

## Exact characterization of universal threshold failure

The two envelopes suffice for all residual partition shapes. The positive
three-part compositions of eight are

\[
6+1+1,\quad 5+2+1,\quad 4+3+1,\quad 4+2+2,\quad 3+3+2.
\]

If a \(4+3+1\) partition passes the owner threshold, move any good from its
four-bundle to its singleton. This produces shape \(3+3+2\). The new pair
has threshold at most \(F\), and the new three-bundle retains only two of
the three goods retained by the old four-bundle, so it remains safe.

If a \(5+2+1\) partition passes, move one good from its five-bundle to its
singleton. The result has shape \(4+2+2\); the shortened bundle retains
only three of the four goods retained before. Finally, from a safe
\(6+1+1\) partition, move two goods from the six-bundle, one to each
singleton. Again the result has shape \(4+2+2\), and all thresholds remain
at most \(F\).

Consequently some residual partition passes the owner threshold if and only
if some partition of shape \(3+3+2\) or \(4+2+2\) passes. Equations (1) and
(3), together with \(x_1\le F\), give the exact equivalence

\[
\begin{split}
&\tau_a(\mathcal P)>F\quad\text{for every three-bundle residual partition }
\mathcal P\\
&\qquad\Longleftrightarrow\qquad
x_5+x_6+x_7>F
\quad\text{and}\quad
\bigl(x_3+x_7>F\ \text{or}\ x_4+x_5>F\bigr).
\end{split}
\tag{5}
\]

In particular \(x_5>F/3\): at least five residual goods are individually
worth more than one third of the favorite. Also

\[
\sum_{k=1}^8x_k>\frac73F.
\tag{6}
\]

Indeed, (5) gives \(x_5>F/3\), while
\(\sum_{k=1}^7x_k\ge5x_5+x_6+x_7>F+4x_5>7F/3\).

This exactly converts the universal-threshold-failure subcase into a
concrete per-row density regime and replaces 966 residual-partition
obstructions per owner by two rank conditions. It does not finish the
common-favorite theorem:
a partition that passes the owner's threshold can still fail the
three-resident Hall condition, and (5) alone does not construct a balanced
four-agent matching.

The executable audit
[`efx49_owner_threshold_shape_envelope_audit.json`](efx49_owner_threshold_shape_envelope_audit.json)
checks both shape formulas on every nonincreasing eight-entry vector over
\(\{0,1,2,3,4\}\), across all 280 partitions of shape \(3+3+2\) and all 210
partitions of shape \(4+2+2\). It also compares (5) with literal enumeration
of all 966 residual partitions for every audited favorite threshold
\(F\ge x_1\). It is a regression check, not a substitute for the proof above.

An equivalent sorting-free form replaces the order statistics by one
four-set covering condition and degree thresholds in the residual pair-sum
graph. See
[OWNER_THRESHOLD_PAIR_DEGREE_ENCODING.md](OWNER_THRESHOLD_PAIR_DEGREE_ENCODING.md).

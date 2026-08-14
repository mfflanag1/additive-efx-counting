# Pure-cell response-lift local refutation

**Date:** 2026-08-14

**Status:** exact positive-additive counterexample to the unconditional step
from a mixed desired core to a desired single-supplier component

## Proposed implication

The conditional physical-compression census would apply to an accumulated
reservoir-fan response if every mixed desired core could be replaced by one
of its original-supplier components.  Locally, this would require

\[
 v_i(S+R)>F_i
 \quad\Longrightarrow\quad
 v_i(S)>F_i\text{ or }v_i(R)>F_i,                \tag{1}
\]

where `S` is the target's ordinary supplier cell and `R` is imported root
residual support.

## Exact counterexample

Take two positive goods `s,y`, supplied by different original owners, and a
source floor `F_i=10`.  In the source row set

\[
                         v_i(s)=6,\qquad v_i(y)=5.              \tag{2}
\]

Then the mixed core `E={s,y}` is strictly desired:

\[
                         v_i(E)=11>10,                           \tag{3}
\]

but neither supplier component is desired:

\[
                         v_i(s)=6\le10,qquad v_i(y)=5\le10.    \tag{4}

The response is safe in the source row because deletion of either good
leaves value at most `6<10`.  Give every other observer the same floor `10`
and any positive values at most `6` for the two goods; the core is then
common-safe for every observer.  Thus positivity, additivity, desire, and
common safety do not imply (1).

## Consequence

Routing the entire root-residual component away from the named source can
destroy payment.  Therefore the 42/48 pure-cell census cannot be applied to
the actual accumulated fan without an additional signed saturation theorem.
The unconditional physical object remains

\[
 \Pi=\{(\sigma(g),f(t)):g\in D_t\},
\]

with every original supplier of every selected core retained.

## Claim boundary

Proved: a two-good exact positive-additive local counterexample to the
pure-cell response lift, including common safety.  Not proved: feasibility
of this two-row witness inside the complete fixed-`U` ledger, impossibility
of a stronger saturation-derived lift, the mixed-support Hall cancellation,
or the fixed-`U` theorem.

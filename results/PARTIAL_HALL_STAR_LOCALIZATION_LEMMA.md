# Star-move localization lemma

## Lemma

Let $X=(X_1,\ldots,X_n)$ be a partial EFX allocation under nonnegative
additive valuations, with unallocated good $f$. Choose distinct bundle labels
$h,s$ and a good $x\in X_s$. Form the complete star partition

\[
P_h=X_h\cup\{f,x\},\qquad P_s=X_s\setminus\{x\},\qquad
P_j=X_j\quad(j\notin\{h,s\}).
\]

Fix an agent $a\notin\{h,s\}$. If the unchanged bundle $P_a=X_a$ is not
EFX-acceptable to agent $a$ in $P$, then the violation is caused by the
enlarged host: there is a good $g\in P_h$ such that

\[
v_a(X_a)<v_a(P_h\setminus\{g\}).
\]

## Proof

The agent's candidate own bundle is unchanged. Every target $P_j$ with
$j\notin\{h,s\}$ is also unchanged, so all its one-good residuals are covered
by the EFX inequalities for $X$.

The source target only shrank. For every $y\in P_s$,

\[
P_s\setminus\{y\}\subseteq X_s\setminus\{y\},
\]

and therefore nonnegativity and base EFX give

\[
v_a(P_s\setminus\{y\})
\le v_a(X_s\setminus\{y\})
\le v_a(X_a).
\]

Thus no unchanged or shrunken target can destroy the edge. Any violation must
come from a residual of $P_h$.

## Consequence for the designated pair trap

For each of the first 14 incoming-good moves in the
[designated pair-trap theorem](PARTIAL_HALL_DESIGNATED_PAIR_TRAP_THEOREM.md),
let $\{a,b\}$ be the two agents whose sole neighbor is the enlarged host.
At least one trapped agent is not the host owner.

- If the pair is not exactly $\{h,s\}$, at least one trapped agent lies
  outside $\{h,s\}$, and the lemma produces an explicit preferred residual
  $P_h\setminus\{g\}$.
- The only exceptional incoming case is the source--host pair $\{h,s\}$.

For an evacuated-singleton move, put $P_s=\{f\}$ and move the old singleton
$x$ into a destination $d$, so $P_d=X_d\cup\{x\}$. The same proof applies to
every agent outside $\{d,s\}$: all unchanged targets remain safe, while the
only residual of $P_s$ is empty. Hence loss of the unchanged own edge is again
localized to the enlarged designated bundle $P_d$.

Across all 17 designated moves, the conversion problem therefore separates
into:

1. a regular case with a trapped agent outside the designated owner and move
   source, producing an explicit preferred residual of the designated bundle;
2. exactly 17 labeled exceptional cells in which the trapped pair is the
   designated owner--source pair.

This lemma is cap-free and valid for arbitrary $n$; only its use of the
17-move pair-trap theorem is currently fixed to the canonical four-agent cell.

## Natural one-good release is insufficient

The most direct successor removes one good from the contested designated
bundle, makes it the new floater, and rematches the four residual bundles.
The exact finite-profile audit
[`partial_hall_designated_trap_release_audit.json`](partial_hall_designated_trap_release_audit.json)
shows that this cannot be the general conversion:

- 359 designated traps were observed across six independent obstruction
  profiles;
- 76 admit any EFX release of this form;
- 41 both admit a release and park the removed good; and
- only 18 give a parked release with larger normalized-utilitarian potential.

Within the 285 regular traps, only 15 have an improving parked release. The
owner--source exceptions account for 74 traps and only three improving
releases. These are finite-profile falsifications of the simple successor,
not theorem frequencies. The surviving conversion must use a multi-bundle
exchange or a weighted combination of several eligible rivals.

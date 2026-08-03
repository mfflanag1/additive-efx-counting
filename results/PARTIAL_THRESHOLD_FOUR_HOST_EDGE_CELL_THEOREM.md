# Four-host edge-cell theorem

## Exact theorem

Consider four agents and nine goods with positive additive valuations.  Let

\[
X=01\mid23\mid45\mid67;\qquad f=8
\]

be an eligible one-floater allocation, and suppose goods (1,3,5,7) are the
strict owner minima in their respective pair bundles.  Normalize every
agent's total value to one and define

\[
\Theta(Z)=\sum_{i=0}^3
\bigl(v_i(Z_i)-\min_{g\in Z_i}v_i(g)\bigr).
\]

For each host (h), add (f) to bundle (h) and form the bipartite EFX
feasibility graph from agents to the four complete bundles.  Fix these four
graphs, in host order, to

\[
\begin{array}{c|cccc}
h=0&1000&0110&0011&1000\\
h=1&0100&0100&0011&1001\\
h=2&1100&0010&0010&1001\\
h=3&1100&0110&0001&0001.
\end{array}
\]

Here each four-bit row lists the feasible bundles for one agent.  If (X)
globally maximizes \(\Theta\) over all eligible one-floater allocations, then
some eligible permutation of the five tokens

\[
\{1,3,5,7,8\}
\]

over the four frozen cores and the floater slot admits an EFX completion.

## Exact certificate

The final quantifier-free linear-real formula is UNSAT.  It contains:

1. positivity, row normalization, eligibility of (X), and the four strict
   owner-minimum inequalities;
2. all 64 truth values in the four displayed host graphs;
3. 26 whole-state Hall blockers, each saying that if its token permutation is
   eligible, all four possible floater hosts fail Hall's condition; and
4. 73 global-maximality implications
   \(\operatorname{eligible}(Y)\Rightarrow\Theta(Y)\leq\Theta(X)\).

Any counterexample to the displayed theorem would satisfy every selected Hall
blocker and every selected global-maximality implication, so UNSAT is enough;
the certificate does not need to enumerate all 120 token states or all
589,824 labeled one-floater allocations.

The 73 global inequalities were discovered at valuations where their states
were Hall-completable.  That fact guided cut selection but is not part of the
inequality formula.  All 73 state transfers are connected: 18 have owner
distance two, 30 distance three, and 25 distance four.

## Four-cycle interpretation

The unique inclusion-minimal Hall witnesses for hosts (0,1,2,3) in the
source profile are, respectively,

\[
\{0,3\},\quad\{0,1\},\quad\{1,2\},\quad\{2,3\},
\]

each seeing only the host bundle.  They form a four-cycle.  The theorem above
fixes the complete edge graphs, however, not merely these four deficient
pairs.  Removing the other 32 edge truth values is the next exact gate.

## Claim boundary

This is a new bounded theorem for one exact (4\times9) host-edge subcell.  It
does not prove the same statement for every valuation with a cyclic pair-Hall
obstruction, for arbitrary frozen cores, for all four-agent instances, or for
general additive EFX.  The result is a rigorous proof-development step, not
the resolution of four-agent or general EFX.

## Artifacts and replay

- `minimum_slot_orbit_four_host_cycle_cegar_session2.json`: final UNSAT cut
  pool and provenance, SHA-256
  `910d8d0188db22cce81b44fe8593ec102b42e5cefef6896a7dffe69c7d54e034`;
- `minimum_slot_orbit_four_host_cycle_component_audit.json`: connected
  transfer audit of all 73 global cuts, SHA-256
  `31aead6081bb18717254b40008657bdec8c1c500e84b34271a8f027d4bfdb419`;
- `minimum_slot_orbit_four_host_cycle_cut_type_audit.json`: exact census of
  the 26 Hall-blocked token permutations, SHA-256
  `df150ebe71accb0bbf8f8456fc11e8a8ecae9b996ff926d9be8108cf89292605`;
- `minimum_slot_orbit_four_host_cycle_replay_audit.json`: fresh-solver UNSAT
  replay with exact source hashes, SHA-256
  `86f586b8db909ba2c2452e7b69bb9ad50d370540197a6b87167000116965edb7`;
- `minimum_slot_orbit_four_host_hall_cycle_audit.json`: source edge graphs and
  minimal Hall witnesses, SHA-256
  `ff8de876321bff22095c52f6e10b71f76cd865b2ba92fac101662e48ef5a447c`;
- `minimum_slot_orbit_hall_encoding_audit.json`: zero mismatches across 960
  comparisons between the compact symbolic Hall formula and explicit perfect
  matching enumeration, SHA-256
  `db5c5ef0b58a6f142f54c73fce9f3cdd974c695015491a57383d00db5f441f2f`.

Shortest exact replay of the final formula:

```sh
python tracks/parkability/run_minimum_slot_orbit_cegar.py \
  --seed results/minimum_slot_orbit_four_host_cycle_cegar_session2.json \
  --base-host-edge-cell-source \
    results/minimum_slot_orbit_hall_state_nearest_cegar_session2_orbit_blocked_seed.json \
  --relabeling-mode none --completion-cut-mode orbit_hall \
  --completion-batch-size 8 --global-witness-mode hall_insertable \
  --solver-profile default --timeout-seconds 600 --max-iterations 1 \
  --output /tmp/minimum-slot-four-host-edge-cell-replay.json
```

The required successful status is `FIXED_PAIR_TOKEN_ORBIT_FORCED` with
`global_cut_count=73`, `orbit_hall_cut_count=26`, and
`solver_reason_unknown=null`.

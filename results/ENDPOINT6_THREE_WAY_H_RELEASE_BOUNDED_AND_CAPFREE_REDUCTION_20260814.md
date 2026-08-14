# Endpoint-6 three-way whole-`H` release theorem and cap-free reduction

**Date:** 2026-08-14

**Status:** dual-verified exact bounded theorem; cap-free reduction to a
physical endpoint, PI/external/Hall exit, or an explicit hidden-minimum split

## Exact bounded theorem

Work in the exact twelve-atom allocated-`E` form-2 master.  Use the current
support allocation

\[
Y=(A+H,Q,W,E;P)
\]

in owner order `(r,q,d,s; charity)`.  Assume:

1. endpoint `Z6` is complete EFX;
2. `q` and `s` weakly retain their normalized base utilities at `Z6`;
3. after restoring the current root bundle, the retained `q` target
   `(Q-J)+M+P` is strictly below `q`'s base utility; and
4. every generalized-PI family in the exact exclusion pool is absent.

Then at least one of the following three complete allocations is EFX:

\[
\begin{aligned}
C_d&=(A,Q,H+L+W,(E-L)+P),\\
C_s&=(A,Q,L+W,H+(E-L)+P),\\
C_q&=(A,H+(Q-J)+M+P,J+(W-M),E).
\end{aligned}                                      \tag{1}
\]

Every allocation in (1) preserves the permanent root packet `A`, releases
the entire current root packet `H`, empties charity, and uses at most four
directed supplier-to-recipient edges.  Their exact edge sets are

\[
\begin{array}{c|c}
C_d&c\to s,\ r\to d,\ s\to d\\
C_s&c\to s,\ r\to s,\ s\to d\\
C_q&c\to q,\ r\to q,\ q\to d,\ d\to q.
\end{array}                                        \tag{2}
\]

Thus the genuine endpoint-6 `{d,q}` debt cannot remain on the root-fixed
face: in the exact cell, generalized PI or one of three whole-`H` release
allocations is forced.

## Certificate and independent replay

The complete producer searched all 10,428 complete allocations that release
exactly one current-root atom and use at most four support edges.  It restored
46,683 initial generalized-PI exclusions, discovered 231 further exclusions,
and lazily added 33 EFX witnesses before returning
`UNSAT_PI_OR_SINGLE_ROOT_RELEASE_EFX`.

Assumption-core extraction reduces the final contradiction to:

- 289 generalized-PI exclusions; and
- exactly the three allocations in (1).

The independent replay does not use the producer's EFX or response formulas:
it uses direct literal single-atom deletion inequalities for EFX and the
nested-minimum `base_response` definition for every PI core.  It returns
UNSAT on the 292-assumption core.

The resulting theorem is stronger than the menu headline: its proof needs
only the three whole-`H` releases in (1), not the remaining 10,425 allocations.

## Cap-free physical lift

Now let each of the twelve symbols denote an arbitrary nonempty physical
packet piece, and assume the physical state has the declared allocated-`E`
form-2 premises and endpoint-6 payment/debt premises above.  Compress each
piece to its additive total.

At least one of the following holds:

1. one of `C_d,C_s,C_q` is a complete **physical** EFX allocation using the
   same at-most-four supplier edges;
2. one of the 289 compressed PI families expands to a physical generalized
   PI;
3. its expansion has an external common-safe desired response;
4. its internal physical response graph has an inclusion-minimal Hall
   deficiency, hence exactly one missing source and a near-perfect matching;
5. a compressed/physical response-premise mismatch or a compressed EFX
   endpoint failure exposes a nonsingleton packet `C` with a least physical
   good `g` satisfying

   \[
   v_i(g)<v_i(S)-1\le
   \min_{D\in\mathcal C(S)}v_i(D).               \tag{3}
   \]

Here (3) is the strict hidden-minimum split.  It is independent of packet
cardinality and supplies a proper physical split of `C`.

### Proof

Compression preserves all packet-total, payment, debt, completeness, and
supplier-edge statements.  If the compressed master and the 289 PI
exclusions hold, the independently replayed bounded theorem supplies one of
the three compressed EFX allocations in (1).  Physical expansion either
preserves EFX or the packet-compression hidden-minimum lemma gives (3).

If instead a compressed PI exclusion fails, expand its three- or four-core
family.  The physical Hall-lift lemma gives physical PI, an external source,
or an inclusion-minimal Hall deficiency.  If a compressed response predicate
has no physical analogue, globally minimal physical extraction or the
hidden-minimum lemma gives the corresponding Hall/hidden-split exit.  These
cases are exhaustive.

## Verification record

- Producer:
  `allocated_e_form2_endpoint6_single_root_release_cegar.json`, SHA-256
  `69b5c9879c27257551d9e747e6c709c8a51aeb249b2093ed1953c01922d99440`.
- Minimized core:
  `allocated_e_form2_endpoint6_single_root_release_unsat_core.json`, SHA-256
  `6acebc240a48f3b76b6d883b2a01495999a5bc2e87b4de97b0f69f861856e465`.
- Independent replay:
  `allocated_e_form2_endpoint6_single_root_release_compact_core_audit.json`,
  SHA-256
  `11eb9a52b9cf6d590a25751230ee5b2df1d929239dad9926bfb2b33e3af46d72`.
- Packet/edge audit:
  `allocated_e_form2_endpoint6_three_way_h_release_lift_audit.json`, SHA-256
  `5b0d9acb26691c33df8f0e9caf083fdc2016030a40340fb8be2060bf913f2b70`.
- Physical hidden-minimum and Hall-lift inputs are independently audited in
  `packet_compression_hidden_minimum_audit.json` and
  `disjoint_compressed_core_hall_lift_audit.json`.

The focused release unit gate has four tests.  A broader integration gate over
the sharp endpoint theorem, root-fixed refutation, hidden-minimum/Hall inputs,
the physical-tail machinery, and the new release artifacts has 29 passing
tests in 38.82 seconds in the
frozen Z3 5.0.0 environment.

## Direct physical-tail adversarial decision

A follow-up decision replaces every named packet by its total and least-good
value.  Its relaxed form (`0<least<=total`) is SAT.  Adding the exact common
cardinality realizability disjunction—each named piece is either singleton
for every observer or satisfies `total>=2*least` for every observer—also
remains SAT.  This shows that the three compressed endpoints do not lift by
tail algebra alone.

The realizable SAT profile expands exactly to 22 positive physical goods.
Independent exhaustive core extraction finds the one-owner generalized PI

\[
r:\ \{a_0.1,g_r.1\}.
\]

It is therefore **not** a countermodel to the physical theorem.  A dedicated
physical-PI CEGAR subsequently learned 135 one-owner subpacket cuts.  Its
first self-PI-free model exposed 1,000 multi-owner PI families, of which 918
use owner set `{d,q,r}`; shortest witnesses use seven physical goods.  A
sparse independent continuation instead reached two `{q,r}` PI cycles built
around a proper split of `J`.  The accumulated continuation reached 1,135
physical PI cuts, but its next solver check was canceled/UNKNOWN.  These are
replayable obstruction data, not an UNSAT theorem.

This sharpens outcome 5 above: every physically realizable model found after
failure of the three whole-`H` releases exits through an actual proper-
subpacket generalized PI.  What remains unproved is exhaustion of that
pattern over all singleton/two-piece cardinality classes.

## Exact remaining claim boundary

Proved: the exact bounded three-way whole-`H` release theorem; its independent
formula replay; exact packet identities and support-edge counts; and the
cap-free reduction of physical expansion to the five outcomes above.

Not proved: that saturation eliminates every external-response exit at the
same record; that the one-hole Hall family is supplier-compatible; that every
hidden-minimum split is an admissible controlled `H` release preserving all
owner floors; that the resulting record change is well-founded; the universal
saturated rank-three fixed-`U` four-edge theorem; or general additive EFX.

The next load-bearing lemma is therefore precise: after excluding proper
one-owner cores, show that simultaneous physical failure of `C_d,C_s,C_q`
forces the observed closed `{q,r}`/`{d,q,r}` subpacket family (or the Hall/
external exits), then convert it to an admitted release-compatible PI cycle
at the same fixed-`U` record.

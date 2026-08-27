# Fixed-U normal-form premise ledger (frozen 2026-08-26)

Branch `fable/efx-fixed-u-normal-form` from `codex/efx-fixed-u-resume-20260820` @ `69c1dcd`.
This ledger freezes, literally and with provenance, every hypothesis used between "saturated
root-facing rank-three fixed-U separator" and "form 2", and states for each whether it is
**encoded** (in the twelve-atom master `build_rank_three_master`), **assumed** (only in prose),
**derived** (proved from the others), or **inserted** (asserted as saturation without a proof).
Line references: `L:` = `FIXED_U_RANK_THREE_FOUR_EDGE_PREMISE_LEDGER_20260813.md`,
`H:` = `EFX_FIXED_U_HANDOFF_20260814.md`, `C:` = `EXACT_RANK_THREE_FIVE_RESPONSE_CLASSIFICATION_LEMMA_20260813.md`,
`O:` = `PAID_SINGLETON_CHARITY_RANK_THREE_OWNER_CYCLE_LEMMA_20260813.md`,
`T:` = `run_fixed_u_full_packet_terminal_cegar.py`, `R:` = `run_fixed_u_rank_three_relation_cegar.py`.

## 0. Naming conventions (a live hazard)

"Form 2" = code index 2 = `corrected_forms[2]` = `{r->q, q->s, s->r, d->q, d->r}` = the lemma's
**R3** (C:57-61).  Code index 0 = `{r->q, q->r, s->d, d->q, d->r}` = the lemma's **R2**.  The
`FORM2_*` documents concern index 2 (R3).  Indices 1 and 3 are the two excluded forms (C:28-51).
Throughout this ledger "form 2" means code index 2.

## 1. The physical object

| # | premise | source | status |
|---|---|---|---|
| P1 | four owners `r,q,d,s`; twelve atomic goods `a0,a1,h,j,k,q0,l,e,m,gq,gr,p`; base allocation `X`: r{a0,m}, q{q0,a1}, d{h,k,gq}, s{e,p}, charity{j,l,gr} | T:15-23 | encoded |
| P2 | positive additive valuations with `0 < v(g,o) < 16` | T:81-87 | encoded (the value box is a modelling restriction never discussed as such) |
| P3 | base normalization `v_o(X_o)=1`; base charity safe `v_o(charity)<=1`; base EFX: `tail_o(X_t)<=1` for `t!=o` | T:89-94 | encoded |
| P4 | the support state `Y`: r{a0,a1,h}, q{j,k,q0}, d{m,gq,gr}, s{l,e}, charity{p}; split and reassembly states as listed | T:41-61 | encoded (fixed combinatorial data, not derived) |
| P5 | named packet inequalities: `A(r)>1, Q(q)>1, E(s)>1, Q(d)>1`; inclusion-minimal `K`; q-budget `K(q)-W(q)>mu_q`, `J(q)>=theta_q`; `nu_d+L(d)-J(d)>0`; `B_q>=0`, `kappa_s>0`; full residual-selector failure over all subsets of `W`; split/reassembly utility signs | T:96-147 | encoded |
| P6 | retained cores: `A`, `Q`, `E` are base-common-safe desired cores of `r,q,s` in the support state | R:126-127 | encoded |
| P7 | root-facing wall: `v_d(W) < tail_d(A)`, `v_d(W) >= tail_d(Q), tail_d(E), v_d(p)` | R:134-138 | encoded (the "root-facing branch" is thereby *chosen*, L:362 lists it as item 6 without definition) |
| P8 | no rank-four response matching at the support (base+current), split (base only) and reassembly (base+current) states | R:144-148, 197-211 | encoded |
| P9 | self responses excluded from the relation (`exclude_self_responses`) | R:76-78 | encoded by option; the generalized self-PI exclusion is a separate cap-free lemma (L:423) |
| P10 | global lexicographic maximality of `(X,{p})` in owner priority (item 1, L:345-346) | prose | **assumed** — not encoded in any master; the only machine check is a single-profile SAT witness (`audit_fixed_u_global_lex_premise.py`) |
| P11 | generalized-PI-freeness / release-compatible PI exclusion (item 10, L:374) | prose | **assumed** — `build_rank_three_master` and the physical-minimum wrapper contain no PI constraint; PI cuts exist only in the allocated-E capture drivers |
| P12 | reachability of `Y` with the complete signed packet vector; ledgers `(U,V,S,T)` with a deterministic selector record (items 2-3, L:347-352) | prose | **assumed** |
| P13 | **item 4**: a selected nonself matching of rank exactly three containing `r->q`, representing `r,q,s`; the sacrificed source `d` has `d->q` and the strong-wall response `d->r`; charity is not a response target; "the exact support relation has five edges containing one of the corrected short cycles" (L:353-358) | prose; O:8-32, C:8-24 | partly derived, partly **inserted** — see §2 |
| P14 | item 5: every selected/decorated response carries a nonempty desired core inside its literal target support, released residual, floors, observer thresholds (L:359-361) | prose | assumed; "nonempty" is asserted in the liquidation lemma, not in item 5's text |
| P15 | items 7-12: saturation = the listed continuation exits have been checked and are unavailable (L:365-382) | prose | assumed; L:437 "Not yet encoded as one implication" |

## 2. Item 4 dissected: what is derived and what is inserted

- (a) `d->q` always holds (**verified**, twelve-atom and physical).  `d->r` always holds for
  atoms (**verified**, 316/316) but **not for packets**: 363 of the 679 physical relations lack
  it, so "forced by the literal strong-envy wall" (O:22-25, item 4) is an atom-level fact.
- (b) No response into charity.  **Derived** (O:8-28) for paid represented sources; **verified**
  for all sources in the census (0 of 316 relations has a charity target — a stronger statement
  than the lemma, which excludes only paid sources).
- (c) The selected matching contains `r->q`, represents `r,q,s` with distinct owner targets.  This
  is a property of the *selected* matching, i.e. of the ledger record, assumed.
- (d) **"The exact support relation has five edges."**  This is the inserted step.  The
  classification lemma (C:22-24) passes from "four possible selected matchings" to "four
  five-edge response relations" with no argument that the relation contains no further edges.
  Under P1-P9 the exact relation can have 2 to 9 edges; 80 of the 316 realizable relations have
  exactly five edges and only two of those are the named forms.  No lemma in the reference set
  derives (d) from items 7-12; L:407 records the classification as "cap-free five-edge relation;
  exactly two forms survive", which describes (c)+(e), not (d).
- (e) Of the four five-edge relations of (c), index 3 contains a rank-four owner matching and
  index 1 forces `q->r` (C:28-51).  **Derived and verified**: exact-relation masters for indices
  1 and 3 are UNSAT; for 0 and 2 SAT.

Consequently the *literal* predicate (items 1-12) reduces to `{form 0, form 2}` — by premise (d),
not by a theorem — and the states of the master outside (d) are the 314 further chart cells.

## 3. The step chain to form 2, with status as the documents state it

| step | document | declared status | what it actually establishes |
|---|---|---|---|
| generalized PI capture | `FIXED_U_GENERALIZED_PI_CAPTURE_CHECKPOINT_20260813.md` | "cap-free structural progress; universal four-edge conclusion open" | bounded twelve-atom theorems in the allocated-E cell; a 6-good combinatorial identity; the capture *reversal* is open |
| retained-support termination | `FIXED_U_RETAINED_SUPPORT_TERMINATION_THEOREM_20260813.md` | "candidate composition, not yet a theorem" | a hand-declared 19-node phase graph; its audit hard-codes three checks as `True` and reports `RANK_THREE_REPEAT_GATE_OPEN`; cannot run on this branch (dependencies live only on `cc/efx-fixed-u-salvage-20260814`) |
| charity exchange | `FIXED_U_GLOBAL_LEX_CHARITY_EXCHANGE_EXCLUSION_20260811.md` | "exact exclusion of [one] countermodel" | one profile's SAT witness; nothing general |
| root liquidation | `FIXED_U_ROOT_RESIDUAL_NONEMPTY_LIQUIDATION_REDUCTION_LEMMA_20260814.md` | "cap-free universal reduction; post-probe response recurrence open" | `Y_r` nonempty and a 3-edge probe; its audit checks a tautology and string presence |
| response saturation | items 7-12, H:188-196, H:1249-1250, L:414 | "not yet encoded as one implication" | **inserted** everywhere it is used |
| five-response classification | C, O | "cap-free reduction … to two forms" | (c)+(e) above; (d) inserted |

## 4. Genuinely load-bearing premises (for the reduction established in this session)

1. P1-P9 (the twelve-atom master) — everything computed here holds on exactly this premise set.
2. Item 4(d), "exactly five edges" — the only premise separating the two named forms from the
   other 314 realizable relations.  It is not load-bearing for the *conclusion* if every cell is
   closed by an immediate complete EFX allocation (see the companion theorem document), in which
   case the classification into forms is unnecessary for the twelve-atom objective.
3. P10 (global lex maximality) and P11 (PI-freeness) are load-bearing only for the *termination*
   arguments (a lex-improving or PI-closing exit); they are not needed for a direct complete-EFX
   closure and are never encoded.
4. The value box `v < 16` and the twelve-atom (unit-packet) model — every UNSAT statement here is
   a twelve-atom theorem; the cap-free (arbitrary packet) lift is the physical-minimum wrapper and
   is treated separately.
5. **The four-edge support cap** is the single most load-bearing premise of the frozen objective:
   two exact states of `M` (P1–P9 verified, outside the named forms) have no four-edge complete
   EFX allocation and are closed by five edges.  Any theorem carrying the cap must exclude those
   states by P10–P15, which are unencoded; a theorem without the cap (five edges) has no known
   obstruction on `M`.

## 5. Silent assumptions found and removed from the record

- "response saturation" as a hypothesis (items 7-12) is never encoded; wherever a document says a
  non-EFX probe "yields a decorated response repeat", that is the inserted step.
- The naming collision R2/R3 versus index 0/2 (§0).
- `v_q(a1) > v_q(W)`, used to exclude index 1, is invoked as "the named packet inequality"; it is
  not among the encoded P5 inequalities (the exclusion nevertheless verifies: the exact index-1
  master is UNSAT, so the inequality is implied by P1-P9 in that cell).
- Several audits (termination, liquidation) check strings in their own markdown or literal
  `True` values; none of them was relied on here.

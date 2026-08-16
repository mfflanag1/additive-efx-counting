# Full critical-cut two-source gradient target

## Exact target

Let \((X,f)\) be an eligible four-agent one-floater EFX allocation that
globally maximizes normalized owner-threshold potential.  Among those
maximizers, choose a state maximizing the direct-completion bottleneck margin

\[
\beta=H(X,f)<0.
\]

Fix a host \(h\) attaining \(H\).  In the completion \(P=C_h(X,f)\), form
the strict critical graph of edges whose normalized EFX slack is greater than
\(\beta\).  Suppose its smallest Hall-deficient agent set is the full set of
four agents.  The full-cut normal form gives a unique missing bundle label
\(b\) and a matching with exactly one equality edge \(a\to b\); its other
three edges are strict.

The live subtheorem is:

> For some owner-minimum good in \(X_h\) or \(X_b\), the corresponding
> floater swap is eligible and has direct-completion margin strictly greater
> than \(\beta\).

This contradicts secondary maximality and rules out the full-cut branch of a
four-agent counterexample.

The hypothesis of *global* threshold maximality is essential.  It cannot be
replaced by the local condition that every eligible owner-minimum floater swap
preserves the source threshold.

## Why the two sources are canonical

The host and missing bundle are distinct.  Base EFX gives

\[
v_h(X_h)\ge\max_{j\ne h}\tau_h(X_j).
\]

After inserting \(f\) into \(h\), the self-edge therefore has slack at least

\[
\frac{v_h(f)}{v_h(M)}>0>\beta.
\]

Thus bundle \(h\) lies in the strict neighborhood and cannot be the missing
bundle \(b\).

The two owner-minimum swaps generate exactly the receiver moves singled out
by the completion-move reduction:

1. swapping at source \(h\) and completing the released good into \(b\)
   transfers a positive good from \(h\) to \(b\); or
2. swapping at source \(b\) and completing the released good into \(h\)
   exchanges the old floater in \(h\) with an owner-minimum good in \(b\).

The transfer strictly improves every observer's edge to \(b\), so in
particular the equality edge \(a\to b\) becomes strict.  The exchange does
the same whenever \(v_a(f)>v_a(g_b)\).  The remaining proof obligation is to
show that at least one partial swap is eligible and that a strict matching on
the other three agents survives.

## Exact wall form of a failure

For either nonsingleton source, the owner-minimum swap obstruction lemma says
that ineligibility has only two causes:

- an external observer's incoming-target wall, which forces that observer to
  value \(f\) above the released good; or
- the source owner's shortfall wall, which forces the source owner to value
  \(f\) below the released good.

If the swap is eligible but the old one-bottleneck matching does not become
strict, the improved equality edge forces at least one of the other three
matched edges to fall to \(\beta\) or below.  This supplies a quantitative
matching-edge blocker.  The remaining analytic task is therefore finite:
combine the two sources' EFX walls and matching-edge blockers into either a
strict matching for one receiver move or an impossible weighted cycle.
Singleton sources remain a separate branch.

## Exact evidence and boundary

`partial_hall_threshold_plateau_exact_path_audit.json` contains 4,459 selected
strict-gradient steps whose minimum critical Hall witness is the full
four-agent set.  For every one of the 4,459 source states, exhaustive exact
enumeration of all global-threshold-maximal states finds a strict
Hall-margin-improving owner-minimum swap from source \(h\) or source \(b\).

Artifact SHA-256:
`16d1d9041c32278cf243462d8bea679926cced30817c21b34b9f2f53448fcdb2`.

This is finite evidence, not a proof of the two-source target.  Proving it
would close the dominant full-cut branch of the Hall-gradient lemma, but the
proper deficient-set branches of sizes two and three would still remain.

## Exact local falsifications

The corresponding statement for an arbitrary locally compatible state is
false.  An exact positive-integer \(4\times9\) model in the canonical
four-pair cell has:

- an eligible base with \(H=-5/3478\) and minimum critical-witness size four;
- an eligible host-source owner-minimum swap whose best margin remains exactly
  \(-5/3478\);
- an ineligible missing-bundle-source swap (its unconstrained best margin is
  larger); and
- no eligible strict improvement among the two sources.

The base is not globally threshold-maximal.  Its threshold potential is
\(13205/13912\), while the global maximum is \(13585/13912\).  A Hall-
completable maximum is only owner distance two away, obtained by exchanging
goods 1 and 2 while retaining floater 8; the exact potential gain is
\(95/3478\).

The artifact is
`threshold_full_cut_two_source_natural_4x9_identity_session1.json`, SHA-256
`8be934496dbea7732d73abe7f25a108b7d39968f34b15d84bc7bab1bff8c07e7`.
Its frozen SMT-LIB has SHA-256
`056717565db36d95ce1e0647f9387a116c4ff6e5775b882d08b19aefe6609201`.

Even adding all four old-good swaps between the two canonical two-good
bundles does not yield a valid local exchange-or-gradient lemma.  A second
exact model has no eligible strict two-source gradient and no eligible
improving cross-bundle swap.  One cross swap would improve \(\Theta\) but is
ineligible.  The nearest global threshold maximizer is owner distance six,
is Hall-completable, and improves \(\Theta\) by \(869/13976\).

That artifact is
`threshold_full_cut_exchange_or_gradient_min03_4x9_identity_session1.json`,
SHA-256
`62e55fe85f9d4d1b8e87740c7c6807447e90fe8b833be41e2e2935f722711970`.
Its frozen SMT-LIB has SHA-256
`24e13cea8359c561526fd62ee0e4d7b874bf752643e44707a70e46f1b4492765`.

These falsifications sharpen the surviving theorem: global maximality must
be used through an unbounded connected-restart or extremal argument.  A fixed
radius-one menu around the critical host and missing bundle is insufficient.

The cap-free `PARTIAL_THRESHOLD_MINIMUM_SLOT_PERMUTATION_LEMMA.md` now gives
the natural global move family.  At a global threshold maximum, any eligible
simultaneous permutation of the four selected owner minima and the floater
remains on the same plateau.  The full-cut target should therefore be attacked
as a minimum-slot cycle-augmentation lemma: single-source failures create
wall dependencies, and a complete dependency cycle is applied at once rather
than enlarged by a fixed-radius menu.

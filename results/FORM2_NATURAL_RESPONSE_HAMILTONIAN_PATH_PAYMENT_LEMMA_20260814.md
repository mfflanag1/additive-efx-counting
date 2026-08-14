# Form-2 natural-response Hamiltonian-path payment lemma

**Date:** 2026-08-14

**Status:** cap-free exact four-edge payment reduction; observer continuation
and universal selection remain open

This is the `d->q`, omit-`r` branch of
`THREE_CYCLE_SIX_BRANCH_CHARITY_COMPLETION_LEMMA_20260813.md`, isolated here
because it is the natural fourth topology for the current exact menu.  The
new information is its direct comparison with the later `q-d` swap frontier,
not a claim that the underlying path was previously unknown.

## Response chain

Let `B` be the physical form-2 support allocation with singleton charity
`p`.  Use three response cores on the natural chain

\[
 C_s\subseteq B_r,\qquad C_q\subseteq B_s,\qquad
 C_d\subseteq B_q.                                  \tag{1}
\]

Here `C_s` and `C_q` are the selected ordinary-or-current common-safe
responses of represented owners `s` and `q`, and `C_d` is the ordinary
base-desired `d->q` core.  Thus each core strictly pays its receiving owner
even if that owner releases an arbitrary part of its current bundle.

## Four-edge allocation

Reverse the three response cores and donate charity to the only owner that
does not receive a response:

\[
\begin{aligned}
 Z_r&=(B_r\setminus C_s)+p,\\
 Z_s&=(B_s\setminus C_q)+C_s,\\
 Z_q&=(B_q\setminus C_d)+C_q,\\
 Z_d&=B_d+C_d.                                      \tag{2}
\end{aligned}
\]

The support-provenance graph is the Hamiltonian path

\[
       \mathrm{charity}\to r\to s\to q\to d,       \tag{3}
\]

so (2) uses exactly four transfer pairs, independently of packet sizes.

Owners `s`, `q`, and `d` are strictly base-paid.  For `q` and `s`, this is
the signed-margin response identity: a base-desired incoming core alone is
strictly above the base floor, while a current-desired incoming core is
strictly above the entire current bundle.  For `d`, the ordinary core
`C_d` alone is strictly above `v_d(X_d)`.

Writing

\[
                 \Delta_r=v_r(B_r)-v_r(X_r),
\]

the sole owner-payment condition is therefore

\[
                 v_r(C_s)\le \Delta_r+v_r(p).       \tag{4}
\]

Failure has the exact root-capture form

\[
                 v_r(C_s)>\Delta_r+v_r(p).          \tag{5}
\]

This is stronger than the root condition in the previously recorded
`q-d` swap topology, which did not give charity to the root.  It also removes
that topology's separate `q`-compensation inequality by using the actual
`q->s` response core.

## Observer continuation

Common safety of the three incoming cores does not by itself make the
enlarged final bundles in (2) observer-safe.  If (4) holds but (2) is not
EFX, the failed comparison is a paid four-edge decorated response and must
be routed through the frozen saturation exclusions.  Consequently this
lemma adds a clean fourth topology to the form-2 menu, but does not claim
that the topology is universally selected.

## Claim boundary

Proved: physical conservation, the exact four support edges, strict payment
of `s,q,d`, and the unique root-payment separator (4)--(5), with unrestricted
packet sizes.

Not proved: observer safety of (2), incompatibility of (5) with all other
menu failures, exhaustion of four-edge topologies, the saturated fixed-`U`
theorem, or general EFX.

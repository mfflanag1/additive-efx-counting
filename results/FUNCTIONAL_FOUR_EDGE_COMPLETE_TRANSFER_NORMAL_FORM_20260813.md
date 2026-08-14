# Functional four-edge complete-transfer normal form

**Date:** 2026-08-13

**Status:** cap-free graph classification; packet feasibility and saturated
payment remain open

## Statement

Start from four owner bundles and a nonempty charity packet.  Consider a
complete reallocation whose active support-provenance graph has exactly four
directed edges and in which each physical supplier sends at most one packet.
Retained goods create no edge.  Because the final charity is empty, charity
has no incoming edge and must send its packet to one owner.  The other three
edges have distinct owner sources, leaving one owner as the unique
source-hole.

For four owners, every such graph belongs to exactly one of four classes:

1. a charity-rooted Hamiltonian path through all four owners;
2. a connected acyclic charity-rooted branching tree;
3. the charity path feeding a directed owner cycle; or
4. a directed owner cycle disconnected from the charity component.

There is no disconnected acyclic case: a forest on five vertices with four
edges is connected.

## Exact census

There are 432 labeled graphs:

| class | graphs |
|---|---:|
| charity-rooted Hamiltonian path | 24 |
| connected acyclic branching | 232 |
| charity-fed owner cycle | 120 |
| disconnected owner cycle | 56 |

[`audit_functional_four_edge_complete_transfer_normal_form.py`](../tracks/parkability/audit_functional_four_edge_complete_transfer_normal_form.py)
enumerates all choices of the three active owner suppliers and every legal
recipient, verifies the functional and completeness conventions, and
classifies all 432 graphs.  Its exact manifest is
[`functional_four_edge_complete_transfer_normal_form_audit.json`](functional_four_edge_complete_transfer_normal_form_audit.json).

## Relevance to the fixed-U gate

Every one of the first seven exact adversarial root-facing profiles admits a
four-edge-or-better complete EFX allocation in this functional family.  The
sharp profile has no completion through three edges and has ten feasible
functional four-edge topologies.  A three-topology functional cover suffices
for the seven-profile census.

The four graph classes identify the exact analytic obligations.  Payment and
observer safety must be proved along the path/tree classes.  In the cycle
classes, full signed release compatibility must yield PI or saturated
component extraction; the existence of a bare ordinary response cycle is
not enough.

The expanded 22-profile census is adversarially informative: a minimum
functional topology cover has size four.  One exact minimum cover is

\[
\begin{array}{ll}
c\to d, q\to s, s\to r, r\to q
  &\text{(disconnected owner cycle)},\\
c\to q, q\to d, d\to s, r\to d
  &\text{(connected branching)},\\
c\to s, d\to q, q\to r, r\to d
  &\text{(a second disconnected owner cycle)},\\
c\to s, s\to r, r\to d, d\to q
  &\text{(Hamiltonian path)}.
\end{array}
\]

Thus path, branching, and disconnected-cycle mechanisms are all necessary
to this minimum cover; no single one of them explains the current census.
Charity-fed cycles occur in the full feasible topology census but are not
needed by this particular minimum cover.  Additional signed saturation may
still eliminate a class, but that must be proved rather than inferred from
its shape.

## Boundary

This is a graph theorem, not the four-edge EFX theorem.  It neither proves
that a feasible packet system exists for arbitrary positive additive values
nor permits cycle classes to be discarded without checking signed residual
payment.  Packet sizes and the number of underlying goods are unrestricted.

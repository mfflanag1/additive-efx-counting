# Permanent-anchor nonroot three-placement response-transfer lemma

**Date:** 2026-08-14

**Status:** cap-free reduction of every disjoint singleton-relay response to
an explicit four-edge probe or one root-target capture inequality

## Three nonroot anchor probes

Start from a current allocation `(Y,{p})` with positive singleton charity and
permanent root anchor

\[
 A\subseteq Y_q,\qquad v_r(A)>v_r(X_r).          \tag{1}
\]

Move `A` from `q` to the root and leave `p` unallocated, obtaining the partial
allocation

\[
 B_r=Y_r\mathbin{\dot\cup}A,\qquad
 B_q=Y_q\setminus A,\qquad B_j=Y_j\ (j\notin\{r,q\}).           \tag{2}
\]

For each nonroot owner `a`, test the complete allocation `Z^a` obtained by
giving `p` to `a`.  Every probe uses only `q -> r:A` and
`charity -> a:p`.  The singleton is never root-held, so every packet-hitting
response enters the independently proved nonroot safe-envelope descent.

Assume all three probes are non-EFX and choose a globally minimum response
over them.  If it hits `p`, it enters the separately proved nonroot
singleton-hit envelope descent; this lemma does not claim that the descent's
changed endpoint is one of the original three probes.  Consider the disjoint
branch.  The response-transport proof is pairwise and applies verbatim to
this three-state family, so the selected physical core `E` is safe at every
probe and desired at every probe except possibly the placement at its own
source.  Let `i` be its source and `t` its target.  Since responses are
nonself, `i!=t`.

If `t` is nonroot, use `Z^t`.  If `t=r`, choose any nonroot placement `Z^h`
with `h!=i`; at least two such choices exist.  In either case the singleton
is not parked at the response source, so

\[
                         v_i(E)>v_i(B_i).         \tag{3}
\]

## Transfer at the selected nonroot placement

Give `E` to its source.  Leave the singleton with `t` when `t` is nonroot,
and at the selected nonroot holder `h` when `t=r`:

\[
 C_i=B_i\mathbin{\dot\cup}E,\qquad C_t=B_t\setminus E.          \tag{4}
\]

Adjoin `p` to `C_t` when `t` is nonroot and to `C_h` when `t=r`; every other
bundle is `B_j`.

This is a complete allocation.  Source `i` strictly improves by (3).

## Universal edge bound

If `t!=r`, target `B_t` is supplied by one current owner, so moving `E` adds
at most the single pair `t -> i`.  Together with `q -> r:A` and
`charity -> t:p`, allocation (4) uses at most three pairs.

If `t=r`, the target has only two supplier cells, `Y_r` from `r` and `A` from
`q`.  Moving `E` to `i` creates at most `r -> i` and `q -> i`; any unselected
part of `A` leaves `q -> r` active, and `p` creates `charity -> h`.  Thus even
this mixed-root case uses at most four pairs.  No packet-size bound is used.

## Root alternative

Put

\[
                         \delta_r=v_r(B_r)-v_r(X_r)>0.           \tag{5}
\]

When `t!=r`, the strict root bundle is unchanged or enlarged, so (4) is
priority-valid.  When `t=r`, its final utility is

\[
                         v_r(B_r)-v_r(E),                         \tag{6}
\]

and remains strictly above base exactly when

\[
                         v_r(E)<\delta_r.                         \tag{7}
\]

Failure is the exact capture separator

\[
                         v_r(E)\ge\delta_r.                       \tag{8}
\]

Thus every disjoint response whose target is nonroot, and every root-target
response not satisfying (8), gives an explicit priority-valid complete probe
through at most four edges.

If that probe is EFX, it contradicts global lexicographic maximality and is
the required endpoint.  If it is non-EFX, globally minimal extraction gives
the next exact decorated response at (4).  A new record, support change,
full-owner recruitment, or PI is a saturated exit; otherwise only an exact
old-record recurrence remains.

## Consequence and boundary

The permanent-anchor singleton relay no longer needs a Hall matching merely
to turn a disjoint response into a bounded-edge probe.  Its exact survivor is
now:

1. the separately typed nonroot singleton-hit envelope continuation;
2. a root-target response satisfying the capture inequality (8); or
3. an exact repeated decorated response after the explicit transfer (4).

This lemma avoids the unresolved root-held singleton-hit branch entirely.
It does not contradict (8), close the exact transfer-response repeat,
independently validate the global fixed-`U` transition registry, prove the
fixed-`U` theorem, or prove general EFX.

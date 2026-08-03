import itertools


def has_perfect_matching(edges, n=4):
    return any(
        all((agent, permutation[agent]) in edges for agent in range(n))
        for permutation in itertools.permutations(range(n))
    )


def neighbors(edges, agents):
    return {bundle for agent, bundle in edges if agent in agents}


def test_unique_defect_hall_trichotomy_exhaustive():
    bad = 0
    host = 1
    fixed = {(agent, agent) for agent in range(4) if agent != bad} | {
        (bad, host)
    }
    optional = [
        (agent, bundle)
        for agent in range(4)
        for bundle in range(4)
        if (agent, bundle) not in fixed and (agent, bundle) != (bad, bad)
    ]
    for mask in range(1 << len(optional)):
        edges = fixed | {
            edge for index, edge in enumerate(optional) if mask & (1 << index)
        }
        if has_perfect_matching(edges):
            continue
        pair = neighbors(edges, {bad, host}) == {host}
        triples = any(
            neighbors(edges, {bad, host, external}) == {host, external}
            for external in (2, 3)
        )
        full = all((agent, bad) not in edges for agent in range(4))
        assert pair or triples or full

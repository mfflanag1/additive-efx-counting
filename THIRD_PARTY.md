# Third-party tools

No third-party source tree or solver binary is vendored in this repository.
The project uses the following packages and external proof tools:

| Tool | Role | Pinned version |
|---|---|---|
| NumPy | Vectorized exact counting and chamber verification | 2.2.6 |
| OR-Tools | CP-SAT protected-slot master | 9.15.6755 |
| python-sat | CNF construction and solver bindings | 1.9.dev7 |
| Z3 / z3-solver | SMT and exact-real research masters | 5.0.0.0 |
| CaDiCaL | Producing solver for the frozen K4 CNF | 1.9.5, commit `146207318796f094dcded87349a64f0c6927309e` |
| drat-trim | Independent DRAT proof checker | commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` |

The repository includes generated formulas, solver records, and a compressed
DRAT proof. It does not relicense the tools that produced or checked them.
Consult each upstream project for its license and build instructions:

- <https://numpy.org/>
- <https://developers.google.com/optimization>
- <https://github.com/pysathq/pysat>
- <https://github.com/Z3Prover/z3>
- <https://github.com/arminbiere/cadical>
- <https://github.com/marijnheule/drat-trim>

The paper's bibliography is the authority for scholarly prior work.
